# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.basic import BasicFixedEnvironment, StateFormat
from agents.dqn import DeepQNet
# from agents.nets.fc import FCNet
from agents.nets.cnn import CNNet

if __name__ == "__main__":
    env = BasicFixedEnvironment(state_format=StateFormat.MATRIX)
    agent = DeepQNet(env.get_state_shape(),
                     BasicFixedEnvironment.ACTIONS,
                     CNNet)
    game = FixedGame(env,
                     agent,
                     max_rounds=100000,
                     test_interval=2000)
    game.begin()
