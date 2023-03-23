import random
from .Agent import Agent


class RandomAgent(Agent):
    """This agent randomly picks one of the allowed actions."""

    def step(self, game_state, allowed_actions_mask):
        allowed_actions = []
        for index, value in enumerate(allowed_actions_mask):
            if value == 1:
                allowed_actions.append(index)
        return random.choice(allowed_actions)
