# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.basic import BasicFixedEnvironment, StateFormat
from agents.dqn import DeepQNet
from agents.nets.fc import FCNet
from agents.nets.cnn import CNNNet
from renderers.fixed.text import TextFixedRenderer

if __name__ == "__main__":
    env = BasicFixedEnvironment(state_format=StateFormat.MATRIX, random_reset=True)
    # agent = DeepQNet(env.get_state_shape(),
    #                  BasicFixedEnvironment.ACTIONS,
    #                  FCNet,
    #                  state_format=StateFormat.VECTOR)
    agent = DeepQNet(env.get_state_shape(),
                     BasicFixedEnvironment.ACTIONS,
                     CNNNet,
                     state_format=StateFormat.MATRIX)
    renderer = TextFixedRenderer(state_format=StateFormat.MATRIX)
    game = FixedGame(env,
                     agent,
                     renderer,
                     max_rounds=100000,
                     test_interval=200)
    game.begin()
