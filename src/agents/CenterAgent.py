from .Agent import Agent


class CenterAgent(Agent):
    """This agent picks whichever column is available closest to the center."""

    def step(self, game_state, allowed_actions):
        for action in [3, 2, 4, 1, 5, 0, 6]:
            if allowed_actions[action] == 1:
                return action
