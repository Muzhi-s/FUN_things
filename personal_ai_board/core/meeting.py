from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from agents.base import Agent, AgentResponse
from agents.challenger import ChallengerAgent
from agents.coordinator import CoordinatorAgent
from agents.executor import ExecutorAgent
from agents.planner import PlannerAgent
from core.llm import LLMService


@dataclass
class MeetingResult:
    question: str
    analyses: list[AgentResponse]
    final_summary: AgentResponse

    def to_markdown(self) -> str:
        sections = [f"# Personal AI Meeting Assistant\n\n## Question\n\n{self.question}"]
        for response in self.analyses:
            sections.append(f"## {response.role}\n\n{response.content}")
        sections.append(f"## Coordinator Action Plan\n\n{self.final_summary.content}")
        return "\n\n".join(sections)


class MeetingEngine:
    def __init__(self, llm: LLMService, agents: Iterable[Agent] | None = None) -> None:
        self.llm = llm
        self.agents = list(agents) if agents is not None else [
            PlannerAgent(llm),
            ExecutorAgent(llm),
            ChallengerAgent(llm),
        ]
        self.coordinator = CoordinatorAgent(llm)

    def run(
        self,
        question: str,
        on_agent_start: Callable[[str], None] | None = None,
        on_agent_done: Callable[[AgentResponse], None] | None = None,
    ) -> MeetingResult:
        question = question.strip()
        if not question:
            raise ValueError("question cannot be empty")

        analyses = []
        for agent in self.agents:
            if on_agent_start:
                on_agent_start(agent.name)
            response = agent.analyze(question)
            analyses.append(response)
            if on_agent_done:
                on_agent_done(response)

        if on_agent_start:
            on_agent_start(self.coordinator.name)
        final_summary = self.coordinator.analyze(question, context=self._format_context(analyses))
        if on_agent_done:
            on_agent_done(final_summary)

        return MeetingResult(question=question, analyses=analyses, final_summary=final_summary)

    @staticmethod
    def _format_context(responses: list[AgentResponse]) -> str:
        return "\n\n".join(f"[{response.role}]\n{response.content}" for response in responses)
