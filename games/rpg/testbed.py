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
                     eps_initial=1,
                     eps_minimum=0.35,
                     eps_decay_steps=5000,
                     target_update_frequency=50,
                     buffer_size=2000,
                     learning_rate=0.0005)
    renderer = TextRPGRenderer()
    game = RPGGame(env,
                   agent,
                   renderer,
                   max_rounds=100000,
                   test_interval=100,
                   should_render_training=False)
    game.begin()
