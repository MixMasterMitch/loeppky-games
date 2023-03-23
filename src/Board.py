from enum import IntEnum


class CellState(IntEnum):
    EMPTY = 0
    OUR_PIECE = 1
    OPPONENT_PIECE = 2


class Board:
    """Represents the current game board.

    The board is represented as a 2D grid, where each cell is in the state `EMPTY`, `OUR_PIECE` or `OPPONENT_PIECE`.
    Row 0 represents the top of the board and column 0 represents the left side of the board.
    """
    def __init__(self, game_state: list[list[list[int]]]):
        self._game_state = game_state

    @property
    def rows_count(self) -> int:
        """Returns the number of rows in the board."""
        return len(self._game_state)

    @property
    def columns_count(self) -> int:
        """Returns the number of columns in the board."""
        return len(self._game_state[0])

    def get_cell_state(self, row: int, col: int) -> CellState:
        """Returns the state of the cell specified by the given row and col."""
        cell = self._game_state[row][col]
        if cell[0] == 1:
            return CellState.OUR_PIECE
        if cell[1] == 1:
            return CellState.OPPONENT_PIECE
        return CellState.EMPTY

    def is_column_full(self, col: int) -> bool:
        """Returns True if the specified column is full of pieces."""
        return self.get_cell_state(0, col) != CellState.EMPTY

    def set_cell_state(self, row: int, col: int, cell_state: CellState) -> None:
        """Modifies the state at the specified cell.

        This is useful for evaluating possible moves.
        """
        cell = [
            1 if cell_state == CellState.OUR_PIECE else 0,
            1 if cell_state == CellState.OPPONENT_PIECE else 0
        ]
        self._game_state[row][col] = cell

    def __str__(self):
        divider = ''.ljust(self.columns_count * 2 + 3, '-') + '\n'
        output = divider
        for row in range(self.rows_count):
            output += '| '
            for col in range(self.columns_count):
                cell_state = self.get_cell_state(row, col)
                if cell_state == CellState.OUR_PIECE:
                    output += 'X'
                elif cell_state == CellState.OPPONENT_PIECE:
                    output += 'O'
                else:
                    output += ' '
                output += ' '
            output += '|\n'
        output += divider
        return output
