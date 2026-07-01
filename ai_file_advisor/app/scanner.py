"""
File scanning and filtering for AI File Advisor.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

PROGRAM_EXTENSIONS = {
    ".exe",
    ".dll",
    ".msi",
    ".sys",
    ".bat",
    ".ps1",
}


def scan_directory(root_dir: str | Path) -> list[dict[str, object]]:
    """Recursively scan a directory and return all files.

    Each item contains:
    - path: full file path as a string
    - name: file name
    - size: file size in bytes
    """

    root_path = Path(root_dir)
    if not root_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {root_path}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_path}")

    files = sorted(path for path in root_path.rglob("*") if path.is_file())
    return [
        {
            "path": str(file_path),
            "name": file_path.name,
            "size": file_path.stat().st_size,
        }
        for file_path in files
    ]


def filter_program_files(files: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    """Keep only program-related files by extension."""

    filtered_files: list[dict[str, object]] = []
    for file_info in files:
        file_name = str(file_info.get("name", ""))
        if Path(file_name).suffix.lower() in PROGRAM_EXTENSIONS:
            filtered_files.append(file_info)
    return filtered_files


def scan_program_files(root_dir: str | Path) -> list[dict[str, object]]:
    """Scan a directory and return only program-related files."""
    return filter_program_files(scan_directory(root_dir))


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m app.scanner <directory>")

    result = scan_program_files(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
