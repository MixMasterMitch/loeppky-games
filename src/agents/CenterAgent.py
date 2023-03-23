from src.agents import Agent
from src import Board


class CenterAgent(Agent):
    """This agent picks whichever column is available closest to the center."""

    def step(self, board: Board) -> int:
        for action in [3, 2, 4, 1, 5, 0, 6]:
            if not board.is_column_full(action):
                return action
