# Created by ALuier Bondar on 2020/12/13.
import random

from envs.base import BaseEnvironment
from enum import Enum


class BasicFixedEnvironment(BaseEnvironment):
    """Basic environment implementation with fixed main character"""

    ALIVE_REWARD = 1.0
    DEAD_REWARD = -1.0
    PARTITIONS = 4
    ARROW_DISTANCE = 2

    class Action(Enum):
        LEFT = 0
        RIGHT = 1
        NONE = 2

    STATE_SHAPE = (PARTITIONS,) * 2
    ACTIONS = [
        Action.LEFT,
        Action.RIGHT,
        Action.NONE
    ]

    def __init__(self, partitions=PARTITIONS, arrow_distance=ARROW_DISTANCE, random_reset=False):
        self.partitions = partitions
        self.max_arrow_distance = arrow_distance
        self.random_reset = random_reset
        self.reset()

    def step(self, action):
        self.__actor_step(action)
        self.__arrow_step()
        dead = self.__is_dead()

        return (self.actor_facing, self.arrow_direction), self.__reward(dead), dead

    def reset(self):
        self.__reset_actor()
        self.__reset_arrow()

        return self.actor_facing, self.arrow_direction

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
