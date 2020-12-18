# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.slash import SlashFixedEnvironment
from agents.dqn import DeepQNet
from agents.nets.fc import FCNet

if __name__ == "__main__":
    game = FixedGame(SlashFixedEnvironment,
                     DeepQNet(SlashFixedEnvironment.STATE_SHAPE,
                              SlashFixedEnvironment.ACTIONS,
                              FCNet),
                     max_rounds=10000,
                     test_interval=200)
    game.begin()
