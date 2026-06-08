from __future__ import annotations

import argparse

from agents.base import AgentResponse
from core.llm import LLMConfig, LLMService
from core.meeting import MeetingEngine
from core.report import save_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Personal AI Board CLI")
    parser.add_argument("question", nargs="*", help="要让 AI 董事会分析的问题")
    parser.add_argument("--model", default="qwen3:4b", help="Ollama 模型名，默认 qwen3:4b")
    parser.add_argument("--temperature", type=float, default=0.7, help="模型温度，默认 0.7")
    parser.add_argument("--timeout", type=float, default=300.0, help="模型请求超时时间，默认 300.0 秒")
    return parser.parse_args()


def prompt_question(initial_question: str) -> str:
    if initial_question.strip():
        return initial_question.strip()

    print("请输入问题：", flush=True)
    return input("> ").strip()


def print_section(title: str, content: str) -> None:
    print(f"\n{title}")
    print(content.strip() if content.strip() else "（无内容）")


def get_response(result, role: str) -> str:
    for response in result.analyses:
        if response.role == role:
            return response.content
    if result.final_summary.role == role:
        return result.final_summary.content
    return ""


def main() -> None:
    args = parse_args()
    question = prompt_question(" ".join(args.question))

    print(f"\n正在启动 Personal AI Meeting Assistant，模型：{args.model}", flush=True)
    print("提示：Ollama 本地模型首次加载可能需要一点时间。", flush=True)

    llm = LLMService(LLMConfig(model=args.model, temperature=args.temperature, timeout=args.timeout))
    engine = MeetingEngine(llm)

    def show_start(role: str) -> None:
        print(f"\n[{role}] 正在分析...", flush=True)

    def show_done(response: AgentResponse) -> None:
        print(f"[{response.role}] 分析完成。", flush=True)

    result = engine.run(question, on_agent_start=show_start, on_agent_done=show_done)
    report_path = save_report(result)
    print("\n" + "=" * 60, flush=True)
    print_section("Planner", get_response(result, "Planner"))
    print_section("Executor", get_response(result, "Executor"))
    print_section("Challenger", get_response(result, "Challenger"))
    print_section("Coordinator", get_response(result, "Coordinator"))
    print(f"\n报告已保存到：{report_path}", flush=True)


if __name__ == "__main__":
    main()
