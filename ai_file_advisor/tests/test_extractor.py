from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.extractor import extract_pe_metadata


class ExtractorTests(unittest.TestCase):
    def test_extract_pe_metadata_reads_version_strings(self):
        fake_string_info = SimpleNamespace(
            Key=b"StringFileInfo",
            StringTable=[
                SimpleNamespace(
                    entries={
                        b"ProductName": b"Auto Shutdown Tool",
                        b"CompanyName": b"Fun Things Studio",
                        b"FileDescription": b"Shutdown helper",
                        b"FileVersion": b"1.2.3.4",
                    }
                )
            ],
        )
        fake_pe = SimpleNamespace(
            FileInfo=[[fake_string_info]],
            VS_FIXEDFILEINFO=[SimpleNamespace(FileVersionMS=0, FileVersionLS=0)],
            close=lambda: None,
        )

        with patch("app.extractor.pefile.PE", return_value=fake_pe):
            result = extract_pe_metadata("D:/fun_th1ngs/auto_shutdown/shutdown_tool.exe")

        self.assertEqual(result["path"], "D:/fun_th1ngs/auto_shutdown/shutdown_tool.exe")
        self.assertEqual(result["name"], "shutdown_tool.exe")
        self.assertTrue(result["is_pe"])
        self.assertEqual(result["product_name"], "Auto Shutdown Tool")
        self.assertEqual(result["company_name"], "Fun Things Studio")
        self.assertEqual(result["file_description"], "Shutdown helper")
        self.assertEqual(result["version"], "1.2.3.4")

    def test_extract_pe_metadata_returns_empty_metadata_when_parse_fails(self):
        pe_error = getattr(sys.modules["app.extractor"].pefile, "PEFormatError")

        with patch("app.extractor.pefile.PE", side_effect=pe_error("bad pe")):
            result = extract_pe_metadata("D:/fun_th1ngs/auto_shutdown/readme.txt")

        self.assertFalse(result["is_pe"])
        self.assertIsNone(result["product_name"])
        self.assertIsNone(result["company_name"])
        self.assertIsNone(result["file_description"])
        self.assertIsNone(result["version"])


if __name__ == "__main__":
    unittest.main()