from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.llm import LLMService


PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"


@dataclass
class AgentResponse:
    role: str
    content: str


class Agent:
    name = "Agent"
    prompt_file = ""

    def __init__(self, llm: LLMService | None = None) -> None:
        self.llm = llm or LLMService()

    @property
    def system_prompt(self) -> str:
        if not self.prompt_file:
            return "你是一个严谨的 AI 决策顾问。"

        prompt_path = PROMPT_DIR / self.prompt_file
        return prompt_path.read_text(encoding="utf-8").strip()

    def analyze(self, question: str, context: str = "") -> AgentResponse:
        return AgentResponse(role=self.name, content=self.run(question, context))

    def run(self, question: str, context: str = "") -> str:
        question = question.strip()
        if not question:
            raise ValueError("question cannot be empty")

        user_prompt = self._build_user_prompt(question, context)
        return self.llm.ask(self.system_prompt, user_prompt)

    def _build_user_prompt(self, question: str, context: str = "") -> str:
        parts = [
            f"用户问题：{question}",
            "请基于你的角色给出结构化分析，重点清晰、可执行。",
        ]
        if context:
            parts.insert(1, f"已有会议上下文：\n{context}")
        return "\n\n".join(parts)
