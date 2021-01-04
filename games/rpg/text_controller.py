from envs.rpg.rpg import RPGEnvironment
from envs.rpg.levels.large_tutorial import LargeTutorial

import numpy as np
import random

np.random.seed(1)
random.seed(1)


def adjust_matrix(matrix):
    return np.flip(np.transpose(matrix), axis=0)

if __name__ == "__main__":
    env = RPGEnvironment(LargeTutorial)
    print(adjust_matrix(env.reset()))

    game_over = False
    while not game_over:
        action = input("""Enter action: 
        IDLE = 0
        LEFTWARD_WALK = 1
        FORWARD_WALK = 2
        RIGHTWARD_WALK = 3
        BACKWARD_WALK = 4
        LEFTWARD_JUMP = 5
        FORWARD_JUMP = 6
        RIGHTWARD_JUMP = 7
        BACKWARD_JUMP = 8
        LEFTWARD_SLASH = 9
        FORWARD_SLASH = 10
        RIGHTWARD_SLASH = 11
        BACKWARD_SLASH = 12
        CROUCH = 13\n""")
        new_state, reward, game_over = env.step(RPGEnvironment.Action(int(action)))
        print(adjust_matrix(new_state))
        print(f'reward: {reward}, game_over: {game_over} time_elapsed: {env.world.time_elapsed}')

    print(f'Game is over, reason: {env.world.status}')