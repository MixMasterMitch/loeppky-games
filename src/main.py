from typing import Mapping
from pettingzoo.classic import connect_four_v3
import time
import random
import os
import importlib
from itertools import combinations
from agents import Agent
from agents.CenterAgent import CenterAgent

# Set of agents to compete in the competition. Every agent will pay a series of games (a "match") against every other
# agent. There should be at least two agents in the list. Duplicates of the same agent are acceptable. The agent names
# provided should match a file name (without the ".py" extension) in the "src/agents" directory.
TOURNAMENT_AGENTS: list[str] = [
    "RandomAgent",
    "StayLowAgent",
    "CenterAgent",
    "RandomAgent",
    "StayLowAgent",
    "CenterAgent",
]
# Number of games executed between each pair of agents. This should be an odd number to avoid ties
GAMES_PER_MATCH: int = 1001
# Sleep time (in seconds) between each step of each game. Set this to a higher value to be able to watch the game
# execution. If this is set to 0, then the game state will not be rendered at all (much faster execution).
GAME_STEP_DELAY: float = 0.1


def import_agent(module_path: str, agent_name: str) -> type[Agent]:
    """Dynamically imports the agent at the specified path."""
    module = importlib.import_module(module_path)
    return getattr(module, agent_name)


def import_agents() -> Mapping[str, type[Agent]]:
    """Dynamically imports all agents in the "src/agents" directory."""
    print("Found the following agents:")
    agent_classes = {}
    for (dirpath, dirnames, filenames) in os.walk("./agents"):
        for filename in filenames:
            file = os.path.splitext(filename)[0]
            if file == '__init__' or file == 'Agent':
                continue
            module_name = f"agents.{file}"
            agent_name = file
            agent_class = import_agent(module_name, agent_name)
            print(f"  {agent_class.__name__}")
            agent_classes[agent_class.__name__] = agent_class
        break
    return agent_classes


def setup_agents() -> list[Agent]:
    """Instantiates an instance of each of the agents specified in TOURNAMENT_AGENTS"""
    agent_classes = import_agents()
    agents = []
    agent_counts = {}
    for agent in TOURNAMENT_AGENTS:
        agent_count = 0
        if agent in agent_counts:
            agent_count = agent_counts[agent]
        agent_count += 1
        agent_counts[agent] = agent_count
        if agent not in agent_classes:
            raise Exception(f"Could not find {agent} class")
        agent_class = agent_classes[agent]
        agent_instance = agent_class()
        agent_instance.name = f"{agent}-{agent_count}"
        agents.append(agent_instance)
    return agents


def run_game(env, agent_1: Agent, agent_2: Agent) -> Agent:
    """Executes a game between the given agents in the given game environment. The agent to go first is randomly selected."""
    env.reset()
    agent_1.init()
    agent_2.init()
    winner = None
    for agent_name in env.agent_iter():
        agent = agent_1 if agent_name == 'player_0' else agent_2
        observation, reward, termination, truncation, info = env.last()
        if reward == 1:
            winner = agent
        if termination:
            env.step(None)
            continue
        action = agent.step(observation['observation'], observation['action_mask'])
        env.step(action)
        time.sleep(GAME_STEP_DELAY)
    return winner


def run_match(env, agent_1: Agent, agent_2: Agent) -> (int, int):
    """Executes GAMES_PER_MATCH number of games between the given agents to determine which agent is better."""
    agent_1_wins = 0
    agent_2_wins = 0
    for game_num in range(1, GAMES_PER_MATCH + 1):
        coin_flip = random.choice([True, False])
        if coin_flip:
            player_1 = agent_1
            player_2 = agent_2
        else:
            player_1 = agent_2
            player_2 = agent_1
        print(f"Starting game {game_num} with {agent_1.name if coin_flip else agent_2.name} going first.")
        winner = None
        while winner is None:
            winner = run_game(env, player_1, player_2)
            if winner is None:
                print(f"No winner for game {game_num}. Re-running game {game_num}.")
            elif winner == agent_1:
                print(f"Winner of game {game_num} is {agent_1.name}")
                agent_1_wins += 1
            else:
                print(f"Winner of game {game_num} is {agent_2.name}")
                agent_2_wins += 1
    print(f"{agent_1.name} won {agent_1_wins} games and {agent_2.name} won {agent_2_wins} games")
    return agent_1_wins, agent_2_wins


#
def run_roundrobin(agents: list[Agent]) -> None:
    """Executes a round-robin tournament between all combinations of the given agents."""
    env = connect_four_v3.env(render_mode="human" if GAME_STEP_DELAY > 0 else None)
    match_wins = {}
    game_wins = {}
    for agent_1, agent_2 in combinations(agents, 2):
        print("================================")
        print(f"Starting match: {agent_1.name} vs {agent_2.name}")
        (agent_1_wins, agent_2_wins) = run_match(env, agent_1, agent_2)
        if agent_1.name not in game_wins:
            game_wins[agent_1.name] = 0
        game_wins[agent_1.name] += agent_1_wins
        if agent_2.name not in game_wins:
            game_wins[agent_2.name] = 0
        game_wins[agent_2.name] += agent_2_wins
        winner = agent_1 if agent_1_wins > agent_2_wins else agent_2
        if winner.name not in match_wins:
            match_wins[winner.name] = 0
        match_wins[winner.name] += 1
        print(f"{winner.name} is the winner of the match")

    print("================================")
    for agent in agents:
        num_match_wins = 0
        if agent.name in match_wins:
            num_match_wins = match_wins[agent.name]
        num_game_wins = 0
        if agent.name in game_wins:
            num_game_wins = game_wins[agent.name]
        print(f"Agent {agent.name} won {num_match_wins} matches and {num_game_wins} games")
    print("================================")

    # Find winner of most matches
    victors = []
    max_match_wins = 0
    for agent_name, wins in match_wins.items():
        if wins > max_match_wins:
            max_match_wins = wins
            victors = [agent_name]
        elif wins == max_match_wins:
            victors.append(agent_name)
    if len(victors) == 1:
        print(f"{victors[0]} WINS!")
        return

    # Find winner of most matches with most game wins
    max_game_wins = 0
    for agent_name in victors:
        wins = game_wins[agent_name]
        if wins > max_game_wins:
            max_game_wins = wins
            victors = [agent_name]
        elif wins == max_game_wins:
            victors.append(agent_name)
    if len(victors) == 1:
        print(f"{victors[0]} WINS!")
        return

    # Declare it a tie
    print(f"No winner. The following agents tied: {victors}")


# Main execution
agents = setup_agents()
run_roundrobin(agents)
