#!/usr/bin/env python3
"""Package only the installable skill folder into a deterministic ZIP."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "product-one-pager"
DEFAULT_OUTPUT = ROOT / "dist" / "product-one-pager.zip"
IGNORED_NAMES = {".DS_Store", "__pycache__"}


def included_files() -> list[Path]:
    symlinks = [path for path in SKILL_DIR.rglob("*") if path.is_symlink()]
    if symlinks:
        names = ", ".join(str(path.relative_to(SKILL_DIR)) for path in symlinks)
        raise ValueError(f"skill folder must not contain symbolic links: {names}")
    return [
        path
        for path in sorted(SKILL_DIR.rglob("*"))
        if path.is_file()
        and path.name not in IGNORED_NAMES
        and path.suffix not in {".pyc", ".pyo"}
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()

    if not SKILL_DIR.is_dir():
        parser.error(f"missing skill folder: {SKILL_DIR}")
    if SKILL_DIR.resolve() == output or SKILL_DIR.resolve() in output.parents:
        parser.error("output ZIP must be outside the installable skill folder")

    try:
        files = included_files()
    except ValueError as error:
        parser.error(str(error))
    if not files:
        parser.error("skill folder contains no packageable files")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            relative = path.relative_to(SKILL_DIR.parent)
            info = zipfile.ZipInfo.from_file(path, arcname=relative.as_posix())
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            with path.open("rb") as source:
                archive.writestr(info, source.read(), compress_type=zipfile.ZIP_DEFLATED)

    shown = output.relative_to(ROOT) if ROOT in output.parents else output
    print(f"Packaged {len(files)} files: {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
