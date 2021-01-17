from envs.rpg.rpg import RPGEnvironment
from envs.rpg.levels.large_tutorial import LargeTutorial
from envs.rpg.levels.small_tutorial import SmallTutorial
from envs.rpg.levels.slash_spike import SlashSpike
import json

import numpy as np
import random
import tensorflow as tf

np.random.seed(1)
random.seed(1)

model_save_path = 'destroy_reward=0.125 vain=-0.125'
json_save_path = '/data.json'

def adjust_matrix(matrix):
    return np.flip(np.transpose(matrix), axis=0)


actions_repre = {
    0: ["LEFTWARD", "WALK"],
    1: ["FORWARD", "WALK"],
    2: ["RIGHTWARD", "WALK"],
    3: ["BACKWARD", "WALK"],
    4: ["LEFTWARD", "JUMP"],
    5: ["FORWARD", "JUMP"],
    6: ["RIGHTWARD", "JUMP"],
    7: ["BACKWARD", "JUMP"],
    8: ["LEFTWARD", "SlASH"],
    9: ["FORWARD", "SlASH"],
    10: ["RIGHTWARD", "SlASH"],
    11: ["BACKWARD", "SlASH"],
}

entities_repre = {
    1: "SPIKE",
    2: "BARRIER",
    3: "TREASURE",
    4: "ACTOR"
}

def generate_actions_list(actions_history):
    actions_list = []
    for action in actions_history:
        actions_list.append(actions_repre[action])
    return actions_list


def generate_entities_list(entities):
    entities_list = []
    for entity in entities:
        entity_data = {"x": entity.position[0],
                       "y": entity.position[1],
                       "type": entities_repre[entity.representation]}
        entities_list.append(entity_data)
    return entities_list


if __name__ == "__main__":
    env = RPGEnvironment(SlashSpike)
    state = env.reset()
    entities = env.world.entities
    width = env.world.level_width
    height = env.world.level_height
    entities_list = generate_entities_list(entities)
    print(adjust_matrix(state))
    model = tf.keras.models.load_model('../../model/rpg/' + model_save_path)
    actions_history = []
    game_over = False
    while not game_over:
        state = tf.expand_dims(tf.constant(state, dtype=tf.float32), -1)
        state = state[tf.newaxis, ...]
        action = tf.argmax(model.predict(state), axis=1)
        actions_history.append(int(action))
        new_state, reward, game_over = env.step(RPGEnvironment.Action(int(action)))
        state = new_state
        print(adjust_matrix(new_state))
        print(f'reward: {reward}, game_over: {game_over} time_elapsed: {env.world.time_elapsed}')

    print(f'Game is over, reason: {env.world.status}')
    print('action history: ', actions_history)

    actions_list = generate_actions_list(actions_history)
    save_data = {"level": {"width": width, "height": height, "entities": entities_list},
                 "action": actions_list}
    with open('../../model/rpg/' + model_save_path + json_save_path, 'w') as file_obj:
        json.dump(save_data, file_obj)
