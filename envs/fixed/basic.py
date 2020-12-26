# Created by ALuier Bondar on 2020/12/13.
import random
import numpy as np

from envs.base import BaseEnvironment, StateFormat
from enum import Enum


class BasicFixedEnvironment(BaseEnvironment):
    """Basic environment implementation with fixed main character"""

    ALIVE_REWARD = 1.0
    DEAD_REWARD = -1.0
    PARTITIONS = 4
    ARROW_DISTANCE = 2

    ACTOR_POINT_VALUE = 1
    ARROW_POINT_VALUE = 1

    class Action(Enum):
        LEFT = 0
        RIGHT = 1
        NONE = 2

    ACTIONS = [
        Action.LEFT,
        Action.RIGHT,
        Action.NONE
    ]

    def __init__(
            self,
            partitions=PARTITIONS,
            arrow_distance=ARROW_DISTANCE,
            random_reset=True,
            state_format=StateFormat.VECTOR):
        self.partitions = partitions
        self.max_arrow_distance = arrow_distance
        self.random_reset = random_reset
        self.state_format = state_format
        if state_format == StateFormat.MATRIX:
            self.matrix_actor_width = 2
            self.matrix_arrow_width = self.max_arrow_distance
            self.matrix_full_width = self.matrix_actor_width + self.matrix_arrow_width * 2
        self.reset()

    def step(self, action):
        self.__actor_step(action)
        self.__arrow_step()
        dead = self.__is_dead()

        return self.__get_state(), self.__reward(dead), dead

    def reset(self):
        self.__reset_actor()
        self.__reset_arrow()

        return self.__get_state()

    def __reward(self, dead):
        """Calculate reward after previous action."""
        return self.DEAD_REWARD if dead else self.ALIVE_REWARD

    def __actor_step(self, action):
        if action == self.Action.LEFT:
            self.actor_facing = (self.actor_facing - 1) % self.partitions
        elif action == self.Action.RIGHT:
            self.actor_facing = (self.actor_facing + 1) % self.partitions
        elif action == self.Action.NONE:
            pass
        else:
            assert False, 'Unexpected action given!'

    def __arrow_step(self):
        if self.current_arrow_distance == 0:
            # print('v Last arrow is dodged!')
            self.__reset_arrow()
        else:
            self.current_arrow_distance -= 1

    def __reset_actor(self):
        self.actor_facing = random.randint(0, self.partitions - 1) if \
            self.random_reset else 0

    def __reset_arrow(self):
        self.arrow_direction = random.randint(0, self.partitions - 1) if \
            self.random_reset else self.partitions // 2
        self.current_arrow_distance = self.max_arrow_distance

    def __is_dead(self):
        return self.current_arrow_distance == 0 and \
               self.actor_facing != self.arrow_direction

    def __get_state(self):
        if self.state_format == StateFormat.VECTOR:
            return self.actor_facing, self.arrow_direction
        elif self.state_format == StateFormat.MATRIX:
            return self.__make_state_matrix()

    def __make_state_matrix(self):
        if self.partitions == 4:
            matrix = np.zeros((self.matrix_full_width, self.matrix_full_width))
            arrow_position = None
            moves = self.max_arrow_distance - self.current_arrow_distance
            if self.arrow_direction == 0:
                arrow_position = [self.matrix_full_width - 1, 0]
                arrow_position[0] += -1 * moves
                arrow_position[1] += +1 * moves
            elif self.arrow_direction == 1:
                arrow_position = [self.matrix_full_width - 1, self.matrix_full_width - 1]
                arrow_position[0] += -1 * moves
                arrow_position[1] += -1 * moves
            elif self.arrow_direction == 2:
                arrow_position = [0, self.matrix_full_width - 1]
                arrow_position[0] += +1 * moves
                arrow_position[1] += -1 * moves
            elif self.arrow_direction == 3:
                arrow_position = [0, 0]
                arrow_position[0] += +1 * moves
                arrow_position[1] += +1 * moves
            matrix[arrow_position[0], arrow_position[1]] = self.ARROW_POINT_VALUE

            actor_position = [self.matrix_arrow_width, self.matrix_arrow_width]
            if self.actor_facing == 0:
                actor_position[0] += 1
            elif self.actor_facing == 1:
                actor_position[0] += 1
                actor_position[1] += 1
            elif self.actor_facing == 2:
                actor_position[1] += 1
            elif self.actor_facing == 3:
                pass
            matrix[actor_position[0], actor_position[1]] = self.ACTOR_POINT_VALUE

            return matrix
        else:
            raise NotImplementedError

    def get_state_shape(self):
        if self.state_format == StateFormat.VECTOR:
            return (self.PARTITIONS,) * 2
        elif self.state_format == StateFormat.MATRIX:
            return (self.matrix_full_width,) * 2
