# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.basic import BasicFixedEnvironment
from agents.dqn import DeepQNet
from agents.nets.fc import FCNet

if __name__ == "__main__":
    game = FixedGame(BasicFixedEnvironment,
                     DeepQNet(BasicFixedEnvironment.STATE_SHAPE,
                              BasicFixedEnvironment.ACTIONS,
                              FCNet),
                     max_rounds=10000,
                     test_interval=200)
    game.begin()
