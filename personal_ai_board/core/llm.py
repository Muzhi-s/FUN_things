from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import ollama


Message = dict[str, str]
DEFAULT_MODEL = "qwen3:4b"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TIMEOUT = 120.0


@dataclass
class LLMConfig:
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    timeout: float = DEFAULT_TIMEOUT


class LLMService:
    """Unified service for all local model calls."""

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig()
        self.client = ollama.Client(timeout=self.config.timeout)

    def chat(self, messages: Iterable[Message]) -> str:
        response = self.client.chat(
            model=self.config.model,
            messages=list(messages),
            options={"temperature": self.config.temperature},
        )
        return response["message"]["content"].strip()

    def ask(self, system_prompt: str, user_prompt: str) -> str:
        return self.chat(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )


_default_service: LLMService | None = None


def get_llm_service(config: LLMConfig | None = None) -> LLMService:
    global _default_service

    if config is not None:
        return LLMService(config)

    if _default_service is None:
        _default_service = LLMService()
    return _default_service


def ask_llm(
    prompt: str,
    system_prompt: str = "你是一个清晰、务实、以行动为导向的个人 AI 助理。",
    model: str | None = None,
    temperature: float | None = None,
    timeout: float | None = None,
) -> str:
    config = None
    if model is not None or temperature is not None or timeout is not None:
        config = LLMConfig(
            model=model or DEFAULT_MODEL,
            temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )

    return get_llm_service(config).ask(system_prompt=system_prompt, user_prompt=prompt)


OllamaLLM = LLMService
