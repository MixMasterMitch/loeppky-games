import random
from src.agents import Agent
from src import Board


class RandomAgent(Agent):
    """This agent randomly picks one of the allowed actions."""

    def step(self, board: Board) -> int:
        allowed_actions = []
        for col in range(board.columns_count):
            if not board.is_column_full(col):
                allowed_actions.append(col)
        return random.choice(allowed_actions)
