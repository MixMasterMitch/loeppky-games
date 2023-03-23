import random
from .Agent import Agent


class RandomAgent(Agent):

    def step(self, game_state, allowed_actions_mask):
        # Randomly picks one of the allowed actions
        allowed_actions = []
        for index, value in enumerate(allowed_actions_mask):
            if value == 1:
                allowed_actions.append(index)
        return random.choice(allowed_actions)
