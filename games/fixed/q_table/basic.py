# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.basic import BasicFixedEnvironment
from agents.q_table import QTable

if __name__ == "__main__":
    game = FixedGame(BasicFixedEnvironment,
                     QTable(BasicFixedEnvironment.STATE_SHAPE, BasicFixedEnvironment.ACTIONS))
    game.begin()
