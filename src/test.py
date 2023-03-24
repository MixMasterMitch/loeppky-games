import importlib

from src import Board, CellState
from src.agents import Agent

AGENT_NAME = "CenterAgent"

BOARD_STRING = """
---------------------
[ ][ ][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ][ ]
[O][ ][ ][ ][O][ ][ ]
[O][ ][ ][O][O][ ][ ]
[O][X][ ][O][O][ ][ ]
---------------------
"""


def create_agent(agent_name: str) -> Agent:
    """Dynamically imports the specified agent"""
    module = importlib.import_module(f"src.agents.{agent_name}")
    agent_class = getattr(module, agent_name)
    return agent_class()


# Setup game board
board = Board.from_board_string(BOARD_STRING)
print("Parsed game board:")
print(board)

# Setup agent
agent = create_agent(AGENT_NAME)

# Execute step
action = agent.step(board)
print(f"Agent requested a piece be placed in column {action}")
if action < 0 or action >= board.columns_count or board.is_column_full(action):
    print(f"[ERROR] This is an invalid action")
    exit()

# Place the piece in a new board
fresh_board = Board.from_board_string(BOARD_STRING)
for row in reversed(range(fresh_board.rows_count)):
    if fresh_board.get_cell_state(row, action) == CellState.EMPTY:
        fresh_board.set_cell_state(row, action, CellState.OUR_PIECE)
        break
print("Game board with new piece:")
print(fresh_board)
