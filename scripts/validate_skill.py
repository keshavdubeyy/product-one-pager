#!/usr/bin/env python3
"""Validate the distributable Product One-Pager skill with no third-party packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "product-one-pager"
SKILL_MD = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"

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
    files = {
        path: read_text(path)
        for path in sorted(SKILL_DIR.rglob("*"))
        if path.is_file()
    }
    validate_metadata(skill_text, ui_text)
    validate_sections(skill_text)
    validate_references(files)
    validate_placeholders(files)
    print("Validated skill metadata, eleven sections, local references, and placeholders.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        sys.exit(1)
