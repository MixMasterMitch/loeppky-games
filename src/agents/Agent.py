class Agent:
    """Base class for all agents"""

    name: str
    """Name assigned to this particular agent when it is created. This should only be set by the game engine."""

    def init(self, is_first: bool) -> None:
        """This function is called before each game is started.

        This can be used to reset any state saved during execution of the game.
        :param is_first: True if this agent will be going first. False if the opponent will be going first.
        """
        pass

    def step(self, game_state: list[list[list[int]]], allowed_actions: list[int]) -> int:
        """This function is called each time it is this agent's turn to make a move.

        When the game is in a terminal state (i.e. one of the agents has won or the board is full), this function will
        not be called until after the next game is started and init is called, if there is a next game.
        See https://pettingzoo.farama.org/environments/classic/connect_four/
        :param game_state: A 3D array of numbers representing the current game state. The dimensions are rows, columns,
        and cell state. The rows has a size of 6, the columns has a size of 7, and the cell state has a length of 2. A 1
        at index 0 in the cell state indicates this agent has a piece in the cell, and a 1 at index 1 indicates the
        opposing agent has a piece in the cell. For example, a 1 at game_state[2][3][1] indicates at row 3, column 4,
        the opposing agent has a piece.
        :param allowed_actions: A 1D array of 7 numbers indicating if each action, 0-6 is allowed or not. In other
        words, indicating if each column is full or not. A value of 0 indicates the action is not allowed (i.e. the
        column is full) and a value of 1 indicates the action is allowed (i.e. the column is not full). This information
        could be derived directly from the game state, but is provided for convenience.
        :return: The action to take. Specifically, the actions 0 through 6 signify placing a piece in the first through
        seventh columns respectively. For example returning a value of 3 will place a piece in the fourth column of the
        board. If an invalid action is returned (e.g. placing a piece in a full column), then the agent will immediately
        be disqualified and lose the game.
        """
        for allowed, index in enumerate(allowed_actions):
            if allowed:
                return index
