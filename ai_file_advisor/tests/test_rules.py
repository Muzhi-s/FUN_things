from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rules import assess_file_risk


class RulesTests(unittest.TestCase):
    def test_windows_directory_is_high_risk(self):
        result = assess_file_risk(r"C:\Windows\System32\kernel32.dll")

        self.assertEqual(result["risk_level"], "high")
        self.assertEqual(result["matched_rule"], "windows_system_directory")

    def test_program_files_is_medium_high_risk(self):
        result = assess_file_risk(r"C:\Program Files\Example App\app.exe")

        self.assertEqual(result["risk_level"], "medium-high")
        self.assertEqual(result["matched_rule"], "program_files_directory")

    def test_downloads_is_low_risk(self):
        result = assess_file_risk(r"C:\Users\Alice\Downloads\installer.exe")

        self.assertEqual(result["risk_level"], "low")
        self.assertEqual(result["matched_rule"], "downloads_directory")

    def test_temp_is_low_risk(self):
        result = assess_file_risk(r"C:\Users\Alice\AppData\Local\Temp\cache.dll")

        self.assertEqual(result["risk_level"], "low")
        self.assertEqual(result["matched_rule"], "temporary_directory")

    def test_unknown_path_defaults_to_unknown(self):
        result = assess_file_risk(r"D:\Projects\tool\plugin.dll")

        self.assertEqual(result["risk_level"], "unknown")
        self.assertIsNone(result["matched_rule"])


if __name__ == "__main__":
    unittest.main()