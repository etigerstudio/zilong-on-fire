# Game controller implementation
from games.fixed.base import FixedGame
from envs.fixed.basic import BasicFixedEnvironment, StateFormat
from agents.q_table import QTable
from renderers.fixed.text import TextFixedRenderer

if __name__ == "__main__":
    # 初始化环境、智能体、渲染器、游戏控制器
    env = BasicFixedEnvironment()
    agent = QTable(env.get_state_shape(),
                   BasicFixedEnvironment.ACTIONS)
    renderer = TextFixedRenderer(state_format=StateFormat.MATRIX)
    game = FixedGame(env, agent, renderer)
    game.begin()
