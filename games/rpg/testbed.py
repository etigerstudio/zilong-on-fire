from envs.base import StateFormat
from envs.rpg.rpg import RPGEnvironment
from envs.rpg.levels.teasure_tutorial import TreasureTutorial
from renderers.rpg.text import TextRPGRenderer
from agents.dqn import DeepQNet
from agents.nets.cnn import CNNNet
from games.rpg.game import RPGGame

if __name__ == "__main__":
    # 初始化环境、智能体、渲染器、游戏控制器
    env = RPGEnvironment(TreasureTutorial)
    agent = DeepQNet(env.get_state_shape(),
                     RPGEnvironment.ACTIONS,
                     CNNNet,
                     state_format=StateFormat.MATRIX,
                     eps_minimum=0.35,
                     eps_decay_steps=2500)
    renderer = TextRPGRenderer()
    game = RPGGame(env,
                   agent,
                   renderer,
                   max_rounds=100000,
                   test_interval=75)
    game.begin()
