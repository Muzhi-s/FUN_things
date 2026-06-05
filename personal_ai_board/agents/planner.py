from agents.base import Agent


class PlannerAgent(Agent):
    name = "Planner"
    prompt_file = "planner.md"


Planner = PlannerAgent
