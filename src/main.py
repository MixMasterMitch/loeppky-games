from pettingzoo.classic import connect_four_v3
import time
import random
import os
from itertools import combinations

# Number of games executed between each pair of agents. This should be an odd number to avoid ties
GAMES_PER_MATCHUP = 1000
# Sleep time (in seconds) between each step of each game. Set this to a higher value to be able to watch the game
# execution. If this is set to 0, then the game state will not be rendered at all (much faster execution).
GAME_STEP_DELAY = 0
# Set of agents to compete in the competition. Every agent will pay a series of games (a "matchup") against every other
# agent. There should be at least two agents in the list. Duplicates of the same agent are acceptable. The agent names
# provided should match a file name (without the ".py" extension) in the "src/agents" directory. The agent class should
# also be imported in "src/agents/__init__.py".
TOURNAMENT_AGENTS = [
    "RandomAgent",
    "StayLowAgent",
    "CenterAgent",
    "RandomAgent",
    "StayLowAgent",
    "CenterAgent",
]


# Dynamically imports the agent at the specified path.
def import_agent(path):
    components = path.split('.')
    mod = __import__(path)
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


# Dynamically imports all agents in the "src/agents" directory.
def import_agents():
    agent_paths = []
    for (dirpath, dirnames, filenames) in os.walk("./agents"):
        for filename in filenames:
            file = os.path.splitext(filename)[0]
            if file == '__init__':
                continue
            agent_paths.append(f"agents.{file}")
        break
    agent_classes = {}
    for agent_path in agent_paths:
        agent_class = import_agent(agent_path)
        agent_classes[agent_class.__name__] = agent_class
    return agent_classes


# Instantiates an instance of each of the agents specified in TOURNAMENT_AGENTS
def setup_agents():
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


# Executes a game between the given agents in the given game environment. The agent to go first is randomly selected.

def run_game(env, agent_1, agent_2):
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


# Executes GAMES_PER_MATCHUP number of games between the given agents to determine which agent is better.
def run_matchup(env, agent_1, agent_2):
    agent_1_wins = 0
    agent_2_wins = 0
    for game_num in range(1, GAMES_PER_MATCHUP + 1):
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


# Executes a round-robin tournament between all combinations of the given agents.
def run_roundrobin(agents):
    env = connect_four_v3.env(render_mode="human" if GAME_STEP_DELAY > 0 else None)
    matchup_wins = {}
    game_wins = {}
    for agent_1, agent_2 in combinations(agents, 2):
        print("================================")
        print(f"Starting matchup: {agent_1.name} vs {agent_2.name}")
        (agent_1_wins, agent_2_wins) = run_matchup(env, agent_1, agent_2)
        if agent_1.name not in game_wins:
            game_wins[agent_1.name] = 0
        game_wins[agent_1.name] += agent_1_wins
        if agent_2.name not in game_wins:
            game_wins[agent_2.name] = 0
        game_wins[agent_2.name] += agent_2_wins
        winner = agent_1 if agent_1_wins > agent_2_wins else agent_2
        if winner.name not in matchup_wins:
            matchup_wins[winner.name] = 0
        matchup_wins[winner.name] += 1
        print(f"{winner.name} is the winner of the matchup")

    print("================================")
    for agent in agents:
        num_matchup_wins = 0
        if agent.name in matchup_wins:
            num_matchup_wins = matchup_wins[agent.name]
        num_game_wins = 0
        if agent.name in game_wins:
            num_game_wins = game_wins[agent.name]
        print(f"Agent {agent.name} won {num_matchup_wins} matchups and {num_game_wins} games")
    print("================================")

    # Find winner of most matchups
    victors = []
    max_matchup_wins = 0
    for agent_name, wins in matchup_wins.items():
        if wins > max_matchup_wins:
            max_matchup_wins = wins
            victors = [agent_name]
        elif wins == max_matchup_wins:
            victors.append(agent_name)
    if len(victors) == 1:
        print(f"{victors[0]} WINS!")
        return

    # Find winner of most matchups with most game wins
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
