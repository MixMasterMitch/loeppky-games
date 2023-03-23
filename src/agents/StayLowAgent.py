from src.agents import Agent
from src import Board, CellState


class StayLowAgent(Agent):
    """This agent picks whichever column has the fewest pieces in it.

    If multiple columns are tied for the fewest number of pieces, the leftmost column is chosen.
    """

    def step(self, board: Board) -> int:
        column_chip_counts = [0] * board.columns_count
        # Count the number of chips in each column
        for row in range(board.rows_count):
            for col in range(board.columns_count):
                #  Check if the cell is occupied
                if board.get_cell_state(row, col) != CellState.EMPTY:
                    column_chip_counts[col] += 1

        # Find the column with the lowest chip count
        min_column_index = None
        min_column_num_chips = None
        for column_index, column_num_chips in enumerate(column_chip_counts):
            # Check if this is the new best column
            if min_column_num_chips is None or column_num_chips < min_column_num_chips:
                min_column_index = column_index
                min_column_num_chips = column_num_chips
        return min_column_index
