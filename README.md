# loeppky-games

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
from .Agent import Agent


class <Name>Agent(Agent):

    def step(self, game_state, allowed_actions):
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
Agent RandomAgent-1 won 0 matches and 63 games
Agent TestAgent-1 won 1 matches and 937 games
================================
TestAgent-1 WINS!

Process finished with exit code 0
```
Wow! Doing pretty well for a one line implementation!

### Controlling the Tournament
Running `main.py` executes a tournament between the agents. The tournament is executed as a round-robin tournament where each agent plays a match of n games against every other agent.
The winner of the match is the agent of the pairing that gets the most game wins in the match. So if Agent1 plays a match of 7 games against Agent2 and Agent1 wins 5 of the games, then Agent1 is the winner of the match.
The winner of the tournament is the agent with the most match wins. If multiple agents are tied on match wins, the tiebreaker is total game wins. For this reason, all games in a match are played, even if an agent has already won the match.

We have already seen how the `TOURNAMENT_AGENTS` can be modified to control which agents are used in the tournament. There are two additional variables that can be
controlled to adjust the tournament execution. The first is `GAMES_PER_MATCH`. As the name suggests, this controls how many games are played in each match. This should always be an odd number to avoid ties.
The other variable is `GAME_STEP_DELAY`. This controls how long to delay between executing each game step. If the value is greater than 0, a GUI will also be rendered on each step to show the current state of the game.
This is useful for visually inspecting the behavior of the agents.

### Implementing an Agent
Back in your new agent file, we can start implementing the agent. Technically, your new agent is a child class of the `Agent` base class, meaning we are using Object-Oriented programming. However, the usage here is simple enough that you do not need to know anything about OO programming to be successful in implementing an agent.
The important thing is that you implement the `step` method (i.e. function). The game engine calls the `step` method whenever it wants the agent to play another piece. So the `step` method receives the current game state as input and should return a column index to place a piece in. More specifically, the `step` method has the following input parameters:
* `self` - This is the current instance of your agent class. You can safely ignore this; it is for OO programming.
* `game_state` - This is the current state of the game. It is effectively two planes: a 2D grid of where the current agent's pieces are, and a 2D grid of where the opponent agent's pieces are. More on this later.
* `allowed_actions` - This an array of 7 (number of rows) 1's or 0's indicating if a piece is allowed to go in each column or not (i.e. if the column is full). A 1 indicates a piece can go in that column, and a 0 indicates that it cannot. This information can be derived from the `game_state`, but is provided for convenience.

The `self` method needs to return an `int` value from 0 to 6 indicating the index of the column to place the piece in. If an invalid index is returned (i.e. if the column is full), then the agent will be disqualified and lose the round.

It is likely that you will want to create utility functions. You can define these before the class definition and call them from the `step` method. For example:
```python
from .Agent import Agent

def is_cell_occupied(game_state, row, col):
    cell = game_state[row][col]
    return cell[0] == 1 or cell[1] == 1

class SuperCoolAgent(Agent):

    def step(self, game_state, allowed_actions):
        # Implementation goes here
        return 0 if is_cell_occupied(game_state, 0, 0) else 1
```

#### Game State
The "observation space" (i.e. game state) is also described in some detail [here](https://pettingzoo.farama.org/environments/classic/connect_four/).

As an example, if the current board was like this:
```text
---------
|       |
|       |
|       |
|     B |
|B    R |
|RB R B |
---------
```

Then the `game_state` would be:
```text
[
  [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
  [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
  [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
  [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 0]],
  [[0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [1, 0], [0, 0]],
  [[1, 0], [0, 1], [0, 0], [1, 0], [0, 0], [0, 1], [0, 0]],
]
```
Note that row 0 refers to the top of the game board, not the bottom.

### Tips
1. You can create multiple agents and have them play against each other to make sure your final agent is not susceptible to specific opposing strategies.

## Submitting an Agent for Competition
TODO