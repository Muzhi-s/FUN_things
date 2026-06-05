from agents.base import Agent


class CoordinatorAgent(Agent):
    name = "Coordinator"
    prompt_file = "coordinator.md"


Coordinator = CoordinatorAgent
