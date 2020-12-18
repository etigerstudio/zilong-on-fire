# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.slash import SlashFixedEnvironment
from agents.q_table import QTable

if __name__ == "__main__":
    game = FixedGame(SlashFixedEnvironment,
                     QTable(SlashFixedEnvironment.STATE_SHAPE, SlashFixedEnvironment.ACTIONS))
    game.begin()
