"""Ollama-backed analysis for AI File Advisor."""

from __future__ import annotations

from typing import Any, Callable

import ollama

DEFAULT_MODEL = "qwen3:4b"


def analyze_with_ollama(
    file_metadata: dict[str, Any],
    risk_result: dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
    chat_fn: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """Generate a natural-language file explanation with Ollama.

    The prompt is intentionally simple at this stage; Step 6 will refine it.
    """

    chat_callable = chat_fn or ollama.chat
    messages = [
        {
            "role": "system",
            "content": (
                "You are a local Windows file analysis assistant. "
                "Explain what the file is, what it does, whether it is safe to delete, "
                "and how confident you are. If information is insufficient, say so clearly."
            ),
        },
        {
            "role": "user",
            "content": _build_user_prompt(file_metadata, risk_result),
        },
    ]

    response = chat_callable(model=model, messages=messages)
    content = _extract_message_content(response)

    return {
        "model": model,
        "messages": messages,
        "content": content,
        "raw_response": response,
    }


def _build_user_prompt(file_metadata: dict[str, Any], risk_result: dict[str, Any]) -> str:
    lines = [
        "Analyze this Windows file:",
        f"Path: {file_metadata.get('path', '')}",
        f"Name: {file_metadata.get('name', '')}",
        f"Size: {file_metadata.get('size', '')}",
        f"Product Name: {file_metadata.get('product_name') or ''}",
        f"Company Name: {file_metadata.get('company_name') or ''}",
        f"File Description: {file_metadata.get('file_description') or ''}",
        f"Version: {file_metadata.get('version') or ''}",
        f"Risk Level: {risk_result.get('risk_level', 'unknown')}",
        f"Risk Reason: {risk_result.get('reason', '')}",
        "Return a concise explanation with these parts: summary, purpose, deletion advice, confidence.",
    ]
    return "\n".join(lines)


def _extract_message_content(response: Any) -> str:
    if isinstance(response, dict):
        message = response.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str):
                return content

    return str(response)
