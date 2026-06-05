from __future__ import annotations

import argparse

from core.llm import LLMConfig, LLMService
from agents.base import AgentResponse
from core.meeting import MeetingEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Personal AI Board CLI")
    parser.add_argument("question", nargs="*", help="要让 AI 董事会分析的问题")
    parser.add_argument("--model", default="qwen3:4b", help="Ollama 模型名，默认 qwen3:4b")
    parser.add_argument("--temperature", type=float, default=0.7, help="模型温度，默认 0.7")
    parser.add_argument("--timeout", type=float, default=120.0, help="模型请求超时时间，默认 120 秒")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    question = " ".join(args.question).strip() or input("请输入要分析的问题：").strip()

    print(f"正在启动 Personal AI Board，模型：{args.model}", flush=True)
    print("提示：Ollama 本地模型首次加载可能需要一段时间。", flush=True)

    llm = LLMService(LLMConfig(model=args.model, temperature=args.temperature, timeout=args.timeout))
    engine = MeetingEngine(llm)

    def show_start(role: str) -> None:
        print(f"\n[{role}] 正在分析...", flush=True)

    def show_done(response: AgentResponse) -> None:
        print(f"[{response.role}] 分析完成。", flush=True)

    result = engine.run(question, on_agent_start=show_start, on_agent_done=show_done)
    print("\n" + "=" * 60 + "\n", flush=True)
    print(result.to_markdown())


if __name__ == "__main__":
    main()
