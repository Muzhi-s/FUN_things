from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path


import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.cache import load_cached_analysis, store_cached_analysis


class CacheTests(unittest.TestCase):
    def test_store_and_load_cached_analysis(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / "sample.exe"
            db_path = temp_path / "advisor.db"

            file_path.write_bytes(b"abc")

            payload = {
                "path": str(file_path),
                "metadata": {"name": "sample.exe"},
                "risk": {"risk_level": "low"},
                "analysis": {"content": "cached"},
            }

            self.assertIsNone(load_cached_analysis(file_path, db_path=db_path))
            store_cached_analysis(file_path, payload, db_path=db_path)

            loaded = load_cached_analysis(file_path, db_path=db_path)

            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["path"], str(file_path))
            self.assertEqual(loaded["metadata"]["name"], "sample.exe")
            self.assertEqual(loaded["analysis"]["content"], "cached")

    def test_cache_miss_when_file_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / "sample.dll"
            db_path = temp_path / "advisor.db"

            file_path.write_bytes(b"abc")
            store_cached_analysis(file_path, {"path": str(file_path)}, db_path=db_path)

            time.sleep(0.01)
            file_path.write_bytes(b"abcdef")

            self.assertIsNone(load_cached_analysis(file_path, db_path=db_path))


if __name__ == "__main__":
    unittest.main()