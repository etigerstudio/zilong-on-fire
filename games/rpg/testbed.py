from envs.base import StateFormat
from envs.rpg.rpg import RPGEnvironment
from envs.rpg.levels.teasure_tutorial import TreasureTutorial
from envs.rpg.levels.medium_tutorial import MediumTutorial
from envs.rpg.levels.large_tutorial import LargeTutorial
from envs.rpg.levels.small_tutorial import SmallTutorial
from envs.rpg.levels.slash_spike import SlashSpike
from renderers.rpg.text import TextRPGRenderer
from agents.dqn import DeepQNet
from agents.nets.cnn import CNNNet
from agents.nets.cnn2 import CNN2Net
from games.rpg.game import RPGGame

import numpy as np
import random
import tensorflow as tf

np.random.seed(1)
random.seed(1)
tf.random.set_seed(1)

if __name__ == "__main__":
    # 初始化环境、智能体、渲染器、游戏控制器
    env = RPGEnvironment(SlashSpike)
    agent = DeepQNet(env.get_state_shape(),
                     RPGEnvironment.ACTIONS,
                     CNN2Net,
                     state_format=StateFormat.MATRIX,
                     eps_initial=1,
                     eps_minimum=0.15,
                     eps_decay_steps=15000,
                     train_freq=4,
                     target_update_freq=100,
                     buffer_size=2000,
                     learning_rate=0.001,
                     batch_size=64)
    renderer = TextRPGRenderer()
    game = RPGGame(env,
                   agent,
                   renderer,
                   max_rounds=100000,
                   test_interval=200,
                   should_render_training=False)
    game.begin()
