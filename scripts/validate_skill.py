#!/usr/bin/env python3
"""Validate the distributable Product One-Pager skill with no third-party packages."""

from __future__ import annotations

import json
import re
import struct
import sys
from html import unescape
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "product-one-pager"
SKILL_MD = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"
DESIGN_REFERENCE = SKILL_DIR / "references" / "design-reference.md"
CLAUDE_PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
EXAMPLE_HTML = ROOT / "examples" / "fictional-designed-brief.html"
EXAMPLE_LANDSCAPE_PNG = ROOT / "examples" / "fictional-designed-brief.png"
EXAMPLE_PORTRAIT_PNG = ROOT / "examples" / "fictional-designed-brief-portrait.png"
EXAMPLE_LANDSCAPE_PDF = ROOT / "examples" / "fictional-designed-brief.pdf"
EXAMPLE_PORTRAIT_PDF = ROOT / "examples" / "fictional-designed-brief-portrait.pdf"

SECTIONS = [
    "Executive Summary",
    "Problem",
    "Opportunity",
    "Proposed Solution",
    "Target User",
    "Why This Will Win",
    "Business Impact",
    "Success Metrics",
    "MVP & Scope",
    "Key Risks & Assumptions",
    "Recommendation",
]

PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bFIXME\b", re.IGNORECASE),
    re.compile(r"\bTKTK\b", re.IGNORECASE),
    re.compile(r"\[PLACEHOLDER\]", re.IGNORECASE),
    re.compile(r"\bREPLACE[_ -]?ME\b", re.IGNORECASE),
]


def fail(message: str) -> None:
    raise ValueError(message)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    except UnicodeDecodeError as error:
        fail(f"file is not valid UTF-8: {path.relative_to(ROOT)} ({error})")
    raise AssertionError("unreachable")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        fail("SKILL.md must begin with closed YAML frontmatter")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.fullmatch(r"([a-zA-Z][a-zA-Z0-9_-]*):\s*(.+)", line)
        if not item:
            fail(f"unsupported or malformed frontmatter line: {line!r}")
        metadata[item.group(1)] = item.group(2).strip().strip("'\"")
    return metadata


def validate_metadata(skill_text: str, ui_text: str) -> None:
    metadata = parse_frontmatter(skill_text)
    if metadata.get("name") != "product-one-pager":
        fail("frontmatter name must be 'product-one-pager'")
    description = metadata.get("description", "")
    if not description or len(description) > 1024:
        fail("frontmatter description must contain 1–1024 characters")

    if "\t" in ui_text:
        fail("agents/openai.yaml must not contain tabs")
    for key in ("interface:", "display_name:", "short_description:", "default_prompt:"):
        if not re.search(rf"^\s*{re.escape(key)}", ui_text, re.MULTILINE):
            fail(f"agents/openai.yaml is missing required metadata: {key[:-1]}")
    if "$product-one-pager" not in ui_text:
        fail("agents/openai.yaml default_prompt must mention $product-one-pager")


def validate_sections(skill_text: str) -> None:
    found = re.findall(r"^### ([1-9]|1[01])\. (.+)$", skill_text, re.MULTILINE)
    expected = [(str(index), title) for index, title in enumerate(SECTIONS, start=1)]
    if found != expected:
        fail(f"expected the eleven numbered sections in order; found: {found}")


def validate_output_contract(skill_text: str, design_text: str) -> None:
    required_skill_phrases = (
        "landscape 16:9 by default",
        "portrait 9:16",
        "self-contained HTML/CSS slide",
        "Static preview",
        "no visual generation is available",
        "Never describe a raster image as editable",
        "references/design-reference.md",
    )
    for phrase in required_skill_phrases:
        if phrase not in skill_text:
            fail(f"SKILL.md is missing output-contract language: {phrase!r}")

    required_design_phrases = (
        "Refero Styles",
        "not an official shadcn design-system specification",
        "#F5F5F5",
        "#FFFFFF",
        "#0A0A0A",
        "#E7000B",
        "Shorten copy before reducing type",
        "Problem framing",
        "Audience and advantage",
        "Test and decide",
    )
    for phrase in required_design_phrases:
        if phrase not in design_text:
            fail(f"design reference is missing required guidance: {phrase!r}")


def png_dimensions(path: Path) -> tuple[int, int]:
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        fail(f"missing rendered example: {path.relative_to(ROOT)}")
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"invalid PNG example: {path.relative_to(ROOT)}")
    return struct.unpack(">II", data[16:24])


def validate_examples() -> None:
    html = unescape(read_text(EXAMPLE_HTML))
    for index, title in enumerate(SECTIONS, start=1):
        if f"{index}. {title}" not in html:
            fail(f"designed HTML example is missing section {index}: {title}")
    for phrase in (
        'contenteditable="true"',
        "width: 1600px",
        "height: 900px",
        "width: 900px",
        "height: 1600px",
        'get("orientation") === "portrait"',
        "@media print",
        "illustrative-one-pager.md",
    ):
        if phrase not in html:
            fail(f"designed HTML example is missing: {phrase!r}")

    if png_dimensions(EXAMPLE_LANDSCAPE_PNG) != (1600, 900):
        fail("landscape PNG preview must be exactly 1600x900")
    if png_dimensions(EXAMPLE_PORTRAIT_PNG) != (900, 1600):
        fail("portrait PNG preview must be exactly 900x1600")

    expected_pdf_geometry = {
        EXAMPLE_LANDSCAPE_PDF: b"/MediaBox [0 0 960 540]",
        EXAMPLE_PORTRAIT_PDF: b"/MediaBox [0 0 540 960]",
    }
    source_url = b"https://github.com/keshavdubeyy/product-one-pager/blob/main/examples/illustrative-one-pager.md"
    for path, media_box in expected_pdf_geometry.items():
        try:
            data = path.read_bytes()
        except FileNotFoundError:
            fail(f"missing PDF example: {path.relative_to(ROOT)}")
        if data[:5] != b"%PDF-":
            fail(f"invalid PDF example: {path.relative_to(ROOT)}")
        if b"/Count 1" not in data or media_box not in data:
            fail(f"PDF example must contain one page at the intended aspect ratio: {path.name}")
        if source_url not in data:
            fail(f"PDF example is missing its portable supporting-analysis link: {path.name}")


def read_json(path: Path) -> dict:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as error:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {error}")
    if not isinstance(data, dict):
        fail(f"expected a JSON object in {path.relative_to(ROOT)}")
    return data


def validate_claude_packaging() -> None:
    plugin = read_json(CLAUDE_PLUGIN)
    marketplace = read_json(CLAUDE_MARKETPLACE)

    if plugin.get("name") != "pm-one-pager":
        fail("Claude plugin name must be 'pm-one-pager'")
    if plugin.get("repository") != "https://github.com/keshavdubeyy/product-one-pager":
        fail("Claude plugin repository URL is missing or incorrect")
    if plugin.get("skills") != "./skills/":
        fail("Claude plugin must discover the single source skill through './skills/'")
    for unsupported in ("hooks", "mcpServers"):
        if unsupported in plugin:
            fail(f"Claude plugin must not declare unnecessary {unsupported}")

    skill_scan = (ROOT / plugin["skills"]).resolve()
    if skill_scan != (ROOT / "skills").resolve() or not skill_scan.is_dir():
        fail("Claude plugin skills path does not resolve to the repository skills directory")

    if marketplace.get("name") != "keshav-pm-skills":
        fail("Claude marketplace name must be 'keshav-pm-skills'")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        fail("Claude marketplace must contain exactly one plugin entry")
    entry = entries[0]
    if not isinstance(entry, dict) or entry.get("name") != plugin["name"]:
        fail("Claude marketplace entry name must match the plugin manifest")
    if entry.get("source") != "./":
        fail("Claude marketplace plugin source must be the repository root './'")

    manifests = sorted(ROOT.rglob("SKILL.md"))
    if manifests != [SKILL_MD]:
        shown = [str(path.relative_to(ROOT)) for path in manifests]
        fail(f"SKILL.md must have one source of truth; found: {shown}")


def local_markdown_targets(text: str) -> list[str]:
    targets = []
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        cleaned = target.strip().split(maxsplit=1)[0].strip("<>")
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#)", cleaned, re.IGNORECASE):
            continue
        targets.append(unquote(cleaned.split("#", 1)[0].split("?", 1)[0]))
    return targets


def validate_references(skill_files: dict[Path, str]) -> None:
    skill_root = SKILL_DIR.resolve()
    for path, text in skill_files.items():
        targets = [(target, path.parent) for target in local_markdown_targets(text)]
        if path == OPENAI_YAML:
            targets.extend(
                (value.strip().strip("'\""), SKILL_DIR)
                for value in re.findall(
                    r"^\s*icon_(?:small|large):\s*(\S.+?)\s*$", text, re.MULTILINE
                )
            )
        for target, base in targets:
            resolved = (base / target).resolve()
            if resolved != skill_root and skill_root not in resolved.parents:
                fail(f"local reference escapes the skill folder: {target} in {path.name}")
            if not resolved.exists():
                fail(f"missing local resource: {target} referenced by {path.relative_to(ROOT)}")

    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        for target in local_markdown_targets(read_text(path)):
            resolved = (path.parent / target).resolve()
            if resolved != ROOT.resolve() and ROOT.resolve() not in resolved.parents:
                fail(f"repository reference escapes the project: {target} in {path.name}")
            if not resolved.exists():
                fail(f"missing local resource: {target} referenced by {path.relative_to(ROOT)}")


def validate_placeholders(files: dict[Path, str]) -> None:
    for path, text in files.items():
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                fail(f"unfinished placeholder matched {pattern.pattern!r} in {path.relative_to(ROOT)}")


def main() -> int:
    skill_text = read_text(SKILL_MD)
    ui_text = read_text(OPENAI_YAML)
    design_text = read_text(DESIGN_REFERENCE)
    files = {
        path: read_text(path)
        for path in sorted(SKILL_DIR.rglob("*"))
        if path.is_file()
    }
    validate_metadata(skill_text, ui_text)
    validate_sections(skill_text)
    validate_output_contract(skill_text, design_text)
    validate_claude_packaging()
    validate_references(files)
    validate_placeholders(files)
    validate_examples()
    print(
        "Validated skill metadata, eleven sections, designed-output contract, "
        "Claude packaging, local references, placeholders, and example artifacts."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        sys.exit(1)
