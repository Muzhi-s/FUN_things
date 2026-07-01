from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.analyzer import DEFAULT_MODEL, analyze_with_ollama


class AnalyzerTests(unittest.TestCase):
    def test_analyze_with_ollama_uses_default_model(self):
        fake_chat = Mock(return_value={"message": {"content": "This is a test explanation."}})

        result = analyze_with_ollama(
            {
                "path": r"D:\fun_th1ngs\auto_shutdown\shutdown_tool.exe",
                "name": "shutdown_tool.exe",
                "size": 1024,
                "product_name": "Auto Shutdown Tool",
                "company_name": "Fun Things Studio",
                "file_description": "Shutdown helper",
                "version": "1.0.0.0",
            },
            {
                "risk_level": "unknown",
                "reason": "当前规则未覆盖该路径，需要结合文件元信息进一步判断。",
            },
            chat_fn=fake_chat,
        )

        self.assertEqual(result["model"], DEFAULT_MODEL)
        self.assertEqual(result["content"], "This is a test explanation.")
        fake_chat.assert_called_once()

        called_kwargs = fake_chat.call_args.kwargs
        self.assertEqual(called_kwargs["model"], DEFAULT_MODEL)
        self.assertEqual(len(called_kwargs["messages"]), 2)

    def test_analyze_with_ollama_uses_custom_model(self):
        fake_chat = Mock(return_value={"message": {"content": "Custom model response."}})

        result = analyze_with_ollama(
            {"path": "D:/sample.dll", "name": "sample.dll", "size": 1},
            {"risk_level": "low", "reason": "test"},
            model="qwen3:4b",
            chat_fn=fake_chat,
        )

        self.assertEqual(result["model"], "qwen3:4b")
        self.assertEqual(result["content"], "Custom model response.")


if __name__ == "__main__":
    unittest.main()