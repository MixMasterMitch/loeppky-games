import math

from .Agent import Agent


class TieAgent(Agent):
    """This agent will always cause a draw when playing against itself."""
    turn = 0
    is_first = True

    def init(self, is_first):
        self.turn = 0
        self.is_first = is_first


    def step(self, game_state, allowed_actions):
        base_col = math.floor(self.turn / 3) * 2
        if (self.is_first):
            base_col += 1
        action = base_col % 7
        self.turn += 1
        return action
