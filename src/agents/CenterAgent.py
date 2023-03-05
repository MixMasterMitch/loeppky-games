import random


class CenterAgent:
    @staticmethod
    def init():
        print("Initialized agent")

    @staticmethod
    def step(game_state, allowed_actions):
        # Picks whichever column is available closest to the center
        for action in [3, 2, 4, 1, 5, 0, 6]:
            if allowed_actions[action] == 1:
                return action
