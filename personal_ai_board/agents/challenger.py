from agents.base import Agent


class ChallengerAgent(Agent):
    name = "Challenger"
    prompt_file = "challenger.md"


Challenger = ChallengerAgent
