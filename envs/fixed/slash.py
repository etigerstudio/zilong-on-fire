# Created by ALuier Bondar on 2020/12/13.
import random

from envs.base import BaseEnvironment, StateFormat
from enum import Enum


class SlashFixedEnvironment(BaseEnvironment):
    """Environment implementation with fixed main character
     who could also slash his sword to intercept arrows

     子龙位置固定、支持挥剑拦截弓箭的环境实现
     """

    ALIVE_REWARD = 1.0  # 存活奖励
    DEAD_REWARD = -1.0  # 阵亡奖励
    PARTITIONS = 4  # 角度分区数
    ARROW_DISTANCE = 4  # 弓箭起始距离
    SLASH_RANGE = 1  # 挥击范围
    SLASHED_ARROW_DISTANCE = -1  # 挥击击中后的弓箭距离标记

    class Action(Enum):
        """动作枚举"""
        TURN_LEFT = 0
        TURN_RIGHT = 1
        SLASH = 2
        NONE = 3

    STATE_SHAPE = (PARTITIONS,) * 2  # 状态形状
    ACTIONS = [
        Action.TURN_LEFT,
        Action.TURN_RIGHT,
        Action.SLASH,
        Action.NONE
    ]

    def __init__(self,
                 partitions=PARTITIONS,
                 arrow_distance=ARROW_DISTANCE,
                 random_reset=True):
        """

        Args:
            partitions: 角度分区总数
            arrow_distance: 弓箭起始距离
            random_reset: 是否开启随机生成子龙/弓箭角度
        """
        self.partitions = partitions
        self.max_arrow_distance = arrow_distance
        self.random_reset = random_reset
        self.reset()

    def step(self, action):
        """与环境互动一步

        Args:
            action: 采取的动作

        Returns:
            状态, 奖励, 是否阵亡
        """
        self.__actor_step(action)
        self.__arrow_step()
        dead = self.__is_dead()

        return (self.actor_facing, self.arrow_direction), self.__reward(dead), dead

    def reset(self):
        """重设环境

        Returns:
            最新状态
        """
        self.__reset_actor()
        self.__reset_arrow()

        return self.actor_facing, self.arrow_direction

    def __reward(self, dead):
        """Calculate reward after previous action."""
        return self.DEAD_REWARD if dead else self.ALIVE_REWARD

    def __actor_step(self, action):
        """子龙执行一步操作"""
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
        """弓箭前进一步"""
        if self.current_arrow_distance == 0 or \
                self.current_arrow_distance == self.SLASHED_ARROW_DISTANCE:
            self.__reset_arrow()
        else:
            self.current_arrow_distance -= 1

    def __reset_actor(self):
        """重设子龙"""
        self.actor_facing = random.randint(0, self.partitions - 1) if \
            self.random_reset else 0

    def __reset_arrow(self):
        """重设弓箭"""
        self.arrow_direction = random.randint(0, self.partitions - 1) if \
            self.random_reset else self.partitions // 2
        self.current_arrow_distance = self.max_arrow_distance

    def __is_dead(self):
        """是否阵亡"""
        return self.current_arrow_distance == 0

    def __slash_arrow(self):
        """向前方挥击尝试拦截弓箭"""
        if self.current_arrow_distance <= self.SLASH_RANGE and \
                self.actor_facing == self.arrow_direction:
            self.current_arrow_distance = self.SLASHED_ARROW_DISTANCE
            # print('v Slashed an arrow!')
