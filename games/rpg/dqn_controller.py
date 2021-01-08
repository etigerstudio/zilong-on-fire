from envs.rpg.rpg import RPGEnvironment
from envs.rpg.levels.large_tutorial import LargeTutorial
from envs.rpg.levels.small_tutorial import SmallTutorial
from envs.rpg.levels.slash_spike import SlashSpike

import numpy as np
import random
import tensorflow as tf

np.random.seed(1)
random.seed(1)

model_save_path = 'destroy_reward=0.125 vain=-0.125'

def adjust_matrix(matrix):
    return np.flip(np.transpose(matrix), axis=0)

if __name__ == "__main__":
    env = RPGEnvironment(SlashSpike)
    state = env.reset()
    print(adjust_matrix(env.reset()))
    model = tf.keras.models.load_model('../../model/rpg/' + model_save_path)
    action_history = []
    game_over = False
    while not game_over:
        state = tf.expand_dims(tf.constant(state, dtype=tf.float32), -1)
        state = state[tf.newaxis, ...]
        action = tf.argmax(model.predict(state), axis=1)
        action_history.append(int(action))
        new_state, reward, game_over = env.step(RPGEnvironment.Action(int(action)))
        state = new_state
        print(adjust_matrix(new_state))
        print(f'reward: {reward}, game_over: {game_over} time_elapsed: {env.world.time_elapsed}')

    print(f'Game is over, reason: {env.world.status}')
    print('action history: ', action_history)