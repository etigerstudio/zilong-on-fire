# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.basic import BasicFixedEnvironment, StateFormat
from agents.dqn import DeepQNet
from agents.nets.fc import FCNet

if __name__ == "__main__":
    env = BasicFixedEnvironment(state_format=StateFormat.VECTOR)
    agent = DeepQNet(env.get_state_shape(),
                     BasicFixedEnvironment.ACTIONS,
                     FCNet)
    game = FixedGame(env,
                     agent,
                     max_rounds=10000,
                     test_interval=200)
    game.begin()
