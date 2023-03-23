import math

from src.agents import Agent
from src import Board


class TieAgent(Agent):
    """This agent will always cause a draw when playing against itself."""
    turn = 0
    is_first = True

    def init(self, is_first):
        self.turn = 0
        self.is_first = is_first

    def step(self, board: Board) -> int:
        base_col = math.floor(self.turn / 3) * 2
        if self.is_first:
            base_col += 1
        action = base_col % 7
        self.turn += 1
        return action
