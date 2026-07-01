from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.pipeline import analyze_file


class PipelineCacheTests(unittest.TestCase):
    def test_analyze_file_uses_cache_on_second_call(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / "demo.exe"
            db_path = temp_path / "advisor.db"
            file_path.write_bytes(b"abc")

            fake_metadata = {
                "path": str(file_path),
                "name": "demo.exe",
                "is_pe": True,
                "product_name": "Demo Product",
                "company_name": "Demo Company",
                "file_description": "Demo file",
                "version": "1.0.0.0",
                "file_version": "1.0.0.0",
                "product_version": "1.0.0.0",
            }
            fake_risk = {
                "path": str(file_path),
                "name": "demo.exe",
                "risk_level": "low",
                "reason": "test",
                "matched_rule": "downloads_directory",
                "metadata": fake_metadata,
            }
            fake_analysis = {
                "model": "qwen3:4b",
                "messages": [],
                "content": "{\"summary\":\"ok\"}",
                "raw_response": {"message": {"content": "ok"}},
            }

            with patch("app.pipeline.extract_pe_metadata", return_value=fake_metadata) as extract_mock, patch(
                "app.pipeline.assess_file_risk", return_value=fake_risk
            ) as risk_mock, patch("app.pipeline.analyze_with_ollama", return_value=fake_analysis) as analyze_mock:
                first_result = analyze_file(file_path, db_path=db_path)
                second_result = analyze_file(file_path, db_path=db_path)

            self.assertFalse(first_result["cache_hit"])
            self.assertTrue(second_result["cache_hit"])
            self.assertEqual(first_result["metadata"]["name"], "demo.exe")
            self.assertEqual(second_result["metadata"]["name"], "demo.exe")
            self.assertEqual(extract_mock.call_count, 1)
            self.assertEqual(risk_mock.call_count, 1)
            self.assertEqual(analyze_mock.call_count, 1)


if __name__ == "__main__":
    unittest.main()