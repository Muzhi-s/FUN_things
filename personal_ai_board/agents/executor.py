from agents.base import Agent


class ExecutorAgent(Agent):
    name = "Executor"
    prompt_file = "executor.md"


Executor = ExecutorAgent
