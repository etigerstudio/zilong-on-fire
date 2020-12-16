# Created by ALuier Bondar on 2020/12/13.

import random

from env.base import BaseEnvironment
from enum import Enum


class SlashFixedEnvironment(BaseEnvironment):
    """Basic environment implementation with fixed main character"""

    ALIVE_REWARD = 1.0
    DEAD_REWARD = -1.0
    PARTITIONS = 4
    ARROW_DISTANCE = 4
    SLASH_RANGE = 1
    SLASHED_ARROW_DISTANCE = -1

    class Action(Enum):
        TURN_LEFT = 0
        TURN_RIGHT = 1
        SLASH = 2
        NONE = 3

    STATE_SHAPE = (PARTITIONS,) * 2
    ACTIONS = [
        Action.TURN_LEFT,
        Action.TURN_RIGHT,
        Action.SLASH,
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
        if action == self.Action.TURN_LEFT:
            self.actor_facing = (self.actor_facing - 1) % self.partitions
        elif action == self.Action.TURN_RIGHT:
            self.actor_facing = (self.actor_facing + 1) % self.partitions
        elif action == self.Action.SLASH:
            self.__slash_arrow()
        elif action == self.Action.NONE:
            pass
        else:
            assert False, 'Unexpected action given!'

    def __arrow_step(self):
        if self.current_arrow_distance == 0 or \
                self.current_arrow_distance == self.SLASHED_ARROW_DISTANCE:
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
        return self.current_arrow_distance == 0

    def __slash_arrow(self):
        if self.current_arrow_distance <= self.SLASH_RANGE and \
                self.actor_facing == self.arrow_direction:
            self.current_arrow_distance = self.SLASHED_ARROW_DISTANCE
            # print('v Slashed an arrow!')
