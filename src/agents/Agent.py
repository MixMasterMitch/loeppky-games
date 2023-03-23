from src import Board


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

    def step(self, board: Board) -> int:
        """This function is called each time it is this agent's turn to make a move.

        When the game is in a terminal state (i.e. one of the agents has won or the board is full), this function will
        not be called until after the next game is started and init is called, if there is a next game.
        See https://pettingzoo.farama.org/environments/classic/connect_four/
        :param board: An object representing the current state of the game board. See the Board class for more details.
        :return: The action to take. Specifically, the actions 0 through 6 signify placing a piece in the first through
        seventh columns respectively. For example returning a value of 3 will place a piece in the fourth column of the
        board. If an invalid action is returned (e.g. placing a piece in a full column), then the agent will immediately
        be disqualified and lose the game.
        """
        for col in range(board.columns_count):
            if not board.is_column_full(col):
                return col
