# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.slash import SlashFixedEnvironment, StateFormat
from agents.dqn import DeepQNet
from agents.nets.fc import FCNet
from renderers.fixed.text import TextFixedRenderer

if __name__ == "__main__":
    env = SlashFixedEnvironment()
    agent = DeepQNet(SlashFixedEnvironment.STATE_SHAPE,
                     SlashFixedEnvironment.ACTIONS,
                     FCNet)
    renderer = TextFixedRenderer(state_format=StateFormat.MATRIX)
    game = FixedGame(env,
                     agent,
                     renderer,
                     max_rounds=10000,
                     test_interval=200)
    game.begin()
