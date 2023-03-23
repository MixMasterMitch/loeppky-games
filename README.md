# loeppky-games

## The Game
The game is [Connect 4](https://en.wikipedia.org/wiki/Connect_Four).

### Tournament Rules

Running the `main.py` script executes a tournament between the specified agents. The tournament is executed as a round-robin tournament where each agent plays a match of n games against every other agent.
The winner of each match is the agent of the pairing that gets the most game wins in the match. So if Agent1 plays a match of 7 games against Agent2 and Agent1 wins 4 of the games, then Agent1 is the winner of the match. Once an agent has won over half of the total number of games (e.g. 4 game wins in a 7 game match), the match is concluded. The agent that goes first is randomly selected before each game.
The winner of the tournament is the agent with the most match wins. 

#### Match Tiebreakers
If multiple agents are tied on match wins, the tiebreaker is total game wins. If there is still a tie, the tournament is re-run until a winner is decided. The randomness of which player starts each game, should prevent a stalemate.

#### Game Tiebreaker
If a game ends in a draw (i.e. the board is filled with no winner), the game is re-run. If there is another draw on the second attempt, the winner is chosen randomly.

#### Limits
Each agent will be given 1 second of wall-clock time to execute each turn and pick a column to place a piece in. If the agent times out taking its turn, it forfeits the game.
This timeout is subject to the context of the execution (computer hardware, other processes running, etc.), but assume the tournament will be run on an ARM based Mac with no other processes running.

Note: the execution timeout is disabled when running the debugger.

There is currently no limit enforced on memory usage and threads. But please do not use more than 1MB of memory or any additional threads.

## Project Setup
All the instructions assume PyCharm is being used as the IDE. 
Perform the following steps in order to set up PyCharm and run the source code:
1. Create a GitHub account at [github.com](https://github.com/)
2. Install Homebrew. This is necessary to easily install other prerequisites. See instructions at [brew.sh](https://brew.sh/).
3. Install `git`. This is necessary to push and pull code to and from GitHub. You can install this using Homebrew by running `brew install git` in the Terminal. Or, if you are not familiar with `git`, you can install [GitHub Desktop](https://desktop.github.com/) to help learn, and it comes with `git` included.
4. Install `pipenv`. This is necessary to get the right version of Python and all the libraries setup to run the code. You can install this using Homebrew by running `brew install pipenv` in the Terminal.
5. Install [PyCharm CE](https://www.jetbrains.com/pycharm/download/#section=mac). This is necessary to edit the source code files. But it will also be used to run `git` commands and run the code.
6. Open PyCharm and click the "Get from VCS" button. Specify `https://github.com/MixMasterMitch/loeppky-games.git` as the URL. When the project is created it will ask if you want to create a new pipenv environment, and click "Ok".
7. You can then run code by right-clicking on the `main.py` file and clicking "Run 'main'". This will run the tournament application with the default agents (i.e. players). From then on, you can run or debug the app by clicking the triangle/run or bug/debug buttons in the top right of the IDE window.

## Developing an Agent
The following instructions demonstrate how to develop a new agent (i.e. virtual player) for the game.

### Create Agent Class
Add a new file in the `src/agents` directory named `<Name>Agent.py`, replacing `<Name>` with some name like `SuperSmart`.

Copy and paste the following code into the new agent file:
```python
from src.agents import Agent
from src import Board, CellState


class <Name>Agent(Agent):

    def step(self, board: Board) -> int:
        # Implementation goes here
        return 0
```

Again, replace `<Name>` with your new agent name.

Your agent implementation will eventually go where it says `# Implementation goes here`, but for now, we will leave the skeleton code as-is.

### Add Agent to Game
Open the file `src/main.py` file. Add the name of your agent to the `TOURNAMENT_AGENTS` array. To play against just the `RandomAgent`, set the array to be as follows:
```python
TOURNAMENT_AGENTS: list[str] = [
    "RandomAgent",
    "<Name>Agent",
]
```
Now run the `main.py` file and observe the output. The output should be something like:
```text
================================
Agent RandomAgent-1 won 0 matches and 40 games
Agent TestAgent-1 won 1 matches and 501 games
================================
TestAgent-1 WINS!

Process finished with exit code 0
```
Wow! Doing pretty well for a one line implementation!

### Controlling the Tournament
We have already seen how the `TOURNAMENT_AGENTS` can be modified to control which agents are used in the tournament. There are some additional variables that can be
controlled to adjust the tournament execution. The first is `GAMES_PER_MATCH`. As the name suggests, this controls how many games are played in each match. This should always be an odd number to avoid ties.
The other variable is `GAME_STEP_DELAY`. This controls how long to delay between executing each game step. If the value is greater than 0, a GUI will also be rendered on each step to show the current state of the game.
This is useful for visually inspecting the behavior of the agents.

The step execution timeout can also be adjusted by modifying `STEP_TIMEOUT`. Modifying this should not be necessary unless you want to test out a slower algorithm during development.

### Implementing an Agent
Back in your new agent file, we can start implementing the agent. Technically, your new agent is a child class of the `Agent` base class, meaning we are using Object-Oriented programming. However, the usage here is simple enough that you do not need to know anything about OO programming to be successful in implementing an agent.
The important thing is that you implement the `step` method (i.e. function). The game engine calls the `step` method whenever it wants the agent to play another piece. So the `step` method receives the current game state as input and should return a column index to place a piece in. More specifically, the `step` method has the following input parameters:
* `self` - This is the current instance of your agent class. You can safely ignore this; it is for OO programming.
* `board` - This is the current state of the game. It is effectively a 2D grid of the board with a state for each cell (empty, our piece, opponent piece). More on this later.

The `step` method needs to return an `int` value from 0 to 6 indicating the index of the column to place the piece in. If an invalid index is returned (i.e. if the column is full), then the agent will be disqualified and lose the round.

It is likely that you will want to create utility functions. You can define these before the class definition and call them from the `step` method. For example:
```python
from src.agents import Agent
from src import Board, CellState

def is_cell_occupied(board: Board, row: int, col: int) -> bool:
    cell_state = board.get_cell_state(row, col)
    return cell_state != CellState.EMPTY

class SuperCoolAgent(Agent):

    def step(self, board: Board) -> int:
        # Implementation goes here
        return 0 if is_cell_occupied(board, 0, 0) else 1
```

#### Game State / Board
The `board` object provides functions and properties for accessing the current game state.

For illustrative purposes, lets assume the board represents the following state (X's are our pieces, and O's are the opponent's pieces):
```text
-----------------
| O             |
| X             |
| O             |
| X     O O   O |
| X O O X O X X |
| O X X O X X O |
-----------------
```

The `get_cell_state` function returns the current state at a given row and column (note that row 0 represents the top row). So calling `board.get_cell_state(3, 6)` in this example should return the state `OPPONENT_PIECE`. You can use the state as follows:
```python
cell_state = board.get_cell_state(3, 6)
is_empty = cell_state == CellState.EMPTY # False
is_ours = cell_state == CellState.OUR_PIECE # False
is_opponents = cell_state == CellState.OPPONENT_PIECE # True
```

The `is_column_full` function returns `True` if there are no open spaces in the column. So calling `board.is_column_full(0)` in this example should return `True`.

The `rows_count` and `columns_count` return the number of rows and columns respectively. This can be useful for iterating through every cell. For example:
```python
for row in range(board.rows_count):
  for col in range(board.columns_count):
    cell_state = board.get_cell_state(row, col)
    is_cell_empty = cell_state == CellState.EMPTY
```

Finally, you can print the board state to the console using `print(board)` and it will output something like the example board shown above.

### Tips
1. You can create multiple agents and have them play against each other to make sure your final agent is not susceptible to specific opposing strategies.

## Submitting an Agent for Competition
TODO