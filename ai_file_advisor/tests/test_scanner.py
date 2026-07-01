from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.scanner import filter_program_files, scan_directory, scan_program_files


class ScannerTests(unittest.TestCase):
    def test_scan_directory_collects_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            nested_dir = temp_path / "nested"
            nested_dir.mkdir()
            executable_file = nested_dir / "demo.exe"
            text_file = temp_path / "notes.txt"

            executable_file.write_bytes(b"abc")
            text_file.write_text("hello", encoding="utf-8")

            result = scan_directory(temp_path)

            self.assertEqual(
                result,
                [
                    {"path": str(executable_file), "name": "demo.exe", "size": 3},
                    {"path": str(text_file), "name": "notes.txt", "size": 5},
                ],
            )

    def test_filter_program_files_keeps_program_extensions(self):
        files = [
            {"path": "C:/temp/a.exe", "name": "a.exe", "size": 1},
            {"path": "C:/temp/b.txt", "name": "b.txt", "size": 2},
            {"path": "C:/temp/c.PS1", "name": "c.PS1", "size": 3},
        ]

        result = filter_program_files(files)

        self.assertEqual(
            result,
            [
                {"path": "C:/temp/a.exe", "name": "a.exe", "size": 1},
                {"path": "C:/temp/c.PS1", "name": "c.PS1", "size": 3},
            ],
        )

    def test_scan_program_files_combines_scan_and_filter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "keep.dll").write_bytes(b"1234")
            (temp_path / "drop.md").write_text("ignore", encoding="utf-8")

            result = scan_program_files(temp_path)

            self.assertEqual(
                result,
                [
                    {"path": str(temp_path / "keep.dll"), "name": "keep.dll", "size": 4},
                ],
            )


if __name__ == "__main__":
    unittest.main()