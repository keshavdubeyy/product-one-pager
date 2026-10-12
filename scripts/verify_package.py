#!/usr/bin/env python3
"""Verify the skill ZIP is safe and exactly matches the installable source folder."""

from __future__ import annotations

import argparse
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "product-one-pager"
DEFAULT_ARCHIVE = ROOT / "dist" / "product-one-pager.zip"
IGNORED_NAMES = {".DS_Store", "__pycache__"}


def expected_files() -> dict[str, bytes]:
    result = {}
    for path in sorted(SKILL_DIR.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"skill source contains symbolic link: {path.relative_to(SKILL_DIR)}")
        if (
            path.is_file()
            and path.name not in IGNORED_NAMES
            and path.suffix not in {".pyc", ".pyo"}
        ):
            name = path.relative_to(SKILL_DIR.parent).as_posix()
            result[name] = path.read_bytes()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?", type=Path, default=DEFAULT_ARCHIVE)
    args = parser.parse_args()
    archive_path = args.archive.resolve()

    if not archive_path.is_file():
        parser.error(f"archive does not exist: {archive_path}")

    try:
        expected = expected_files()
    except ValueError as error:
        parser.error(str(error))
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            parser.error("archive CRC validation failed")
        names = archive.namelist()
        if len(names) != len(set(names)):
            parser.error("archive contains duplicate paths")
        for info in archive.infolist():
            name = info.filename
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts:
                parser.error(f"archive contains unsafe path: {name}")
            if not path.parts or path.parts[0] != "product-one-pager":
                parser.error(f"archive path is outside the top-level skill folder: {name}")
            file_type = (info.external_attr >> 16) & 0o170000
            if info.is_dir() or file_type not in (0, stat.S_IFREG):
                parser.error(f"archive contains a non-regular file: {name}")

        if set(names) != set(expected):
            missing = sorted(set(expected) - set(names))
            extra = sorted(set(names) - set(expected))
            parser.error(f"archive contents differ from source; missing={missing}, extra={extra}")
        for name, source_bytes in expected.items():
            if archive.read(name) != source_bytes:
                parser.error(f"archive file differs from source: {name}")

    print(f"Verified {len(expected)} files in {archive_path.name}; ZIP matches the skill source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
