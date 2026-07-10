"""由Ollama驱动的AI文件顾问分析功能"""

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
    """使用 Ollama 生成自然语言文件说明。"""

    #决定使用哪个聊天函数：如果提供了 chat_fn，则使用它；否则使用默认的 ollama.chat
    chat_callable = chat_fn or ollama.chat

    #构建消息列表
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

    #调用ollama api进行分析
    response = chat_callable(model=model, messages=messages)
    content = _extract_message_content(response)

    #返回结构化结果
    return {
        "model": model,
        "messages": messages,
        "content": content,
        "raw_response": response,
    }

# 构建用户提示词
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
        'Return ONLY valid JSON. Do not use markdown. Do not explain. Format: {"summary": "", "purpose": "", "risk": "", "advice": "", "confidence": 90}',
    ]
    return "\n".join(lines)

# 提取消息内容
def _extract_message_content(response: Any) -> str:
    """兼容新版和旧版 Ollama SDK"""

    # 新版 ollama SDK（ChatResponse）
    if hasattr(response, "message"):
        message = response.message
        if hasattr(message, "content"):
            return str(message.content or "")
        if isinstance(message, dict):
            return str(message.get("content") or "")

    # 旧版 SDK（dict）
    if isinstance(response, dict):
        message = response.get("message", {})
        if isinstance(message, dict):
            return str(message.get("content") or "")
        if hasattr(message, "content"):
            return str(message.content or "")

    return ""
