import random


class StayLowAgent:
    @staticmethod
    def init():
        print("Initialized agent")

    @staticmethod
    def step(game_state, allowed_actions):
        num_columns = len(game_state[0])
        column_chip_counts = [0] * num_columns
        # Count the number of chips in each column
        for row in game_state:
            for column_index, cell in enumerate(row):
                #  Check if the cell is occupied
                if cell[0] == 1 or cell[1] == 1:
                    column_chip_counts[column_index] += 1

        # Find the column with the lowest chip count
        min_column_index = None
        min_column_num_chips = None
        for column_index, column_num_chips in enumerate(column_chip_counts):
            # Check if this is the new best column
            if min_column_num_chips is None or column_num_chips < min_column_num_chips:
                min_column_index = column_index
                min_column_num_chips = column_num_chips
        return min_column_index
