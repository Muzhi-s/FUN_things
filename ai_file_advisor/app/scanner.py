"""
负责文件扫描与过滤
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
    """递归扫描目录并返回所有文件

    每个项目包含:
    - path: 文件完整路径
    - name: 文件名
    - size: 文件大小（字节）
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
    """过滤出程序相关的文件（如 .exe, .dll, .msi 等）"""

    filtered_files: list[dict[str, object]] = []
    for file_info in files:
        file_name = str(file_info.get("name", ""))
        if Path(file_name).suffix.lower() in PROGRAM_EXTENSIONS:
            filtered_files.append(file_info)
    return filtered_files


def scan_program_files(root_dir: str | Path) -> list[dict[str, object]]:
    """扫描目录并返回程序相关的文件列表"""
    return filter_program_files(scan_directory(root_dir))


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m app.scanner <directory>")

    result = scan_program_files(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
