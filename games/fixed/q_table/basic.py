# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.basic import BasicFixedEnvironment
from agents.q_table import QTable

if __name__ == "__main__":
    env = BasicFixedEnvironment()
    agent = QTable(env.get_state_shape(),
                   BasicFixedEnvironment.ACTIONS)
    game = FixedGame(env, agent)
    game.begin()
