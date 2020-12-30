# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.slash import SlashFixedEnvironment, StateFormat
from agents.q_table import QTable
from renderers.fixed.text import TextFixedRenderer

if __name__ == "__main__":
    # 初始化环境、智能体、渲染器、游戏控制器
    env = SlashFixedEnvironment()
    agent = QTable(SlashFixedEnvironment.STATE_SHAPE,
                   SlashFixedEnvironment.ACTIONS)
    renderer = TextFixedRenderer(state_format=StateFormat.MATRIX)
    game = FixedGame(env, agent, renderer)
    game.begin()
