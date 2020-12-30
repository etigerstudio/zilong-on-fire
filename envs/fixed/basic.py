# Created by ALuier Bondar on 2020/12/13.
import random
import numpy as np

from envs.base import BaseEnvironment, StateFormat
from enum import Enum


class BasicFixedEnvironment(BaseEnvironment):
    """Basic environment implementation with fixed main character

    子龙位置固定的基本环境实现
    """

    ALIVE_REWARD = 1.0  # 存活奖励
    DEAD_REWARD = -1.0  # 阵亡奖励
    PARTITIONS = 4  # 角度分区数
    ARROW_DISTANCE = 2  # 弓箭起始距离

    ACTOR_POINT_VALUE = 1  # 子龙在矩阵点上的表示值
    ARROW_POINT_VALUE = 1  # 弓箭在矩阵点上的表示值

    class Action(Enum):
        """动作枚举"""
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
        """

        Args:
            partitions: 角度分区总数
            arrow_distance: 弓箭起始距离
            random_reset: 是否开启随机生成子龙/弓箭角度
            state_format: 状态格式
        """
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
        """与环境互动一步

        Args:
            action: 采取的动作

        Returns:
            状态, 奖励, 是否阵亡
        """
        self.__actor_step(action)
        self.__arrow_step()
        dead = self.__is_dead()

        return self.__get_state(), self.__reward(dead), dead

    def reset(self):
        """重设环境

        Returns:
            最新状态
        """
        self.__reset_actor()
        self.__reset_arrow()

        return self.__get_state()

    def __reward(self, dead):
        """Calculate reward after previous action."""
        return self.DEAD_REWARD if dead else self.ALIVE_REWARD

    def __actor_step(self, action):
        """子龙执行一步操作"""
        if action == self.Action.LEFT:
            self.actor_facing = (self.actor_facing - 1) % self.partitions
        elif action == self.Action.RIGHT:
            self.actor_facing = (self.actor_facing + 1) % self.partitions
        elif action == self.Action.NONE:
            pass
        else:
            assert False, 'Unexpected action given!'

    def __arrow_step(self):
        """弓箭前进一步"""
        if self.current_arrow_distance == 0:
            # print('v Last arrow is dodged!')
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
        return self.current_arrow_distance == 0 and \
               self.actor_facing != self.arrow_direction

    def __get_state(self):
        """获取当前状态"""
        if self.state_format == StateFormat.VECTOR:
            return self.actor_facing, self.arrow_direction
        elif self.state_format == StateFormat.MATRIX:
            return self.__make_state_matrix()

    def __make_state_matrix(self):
        """构建状态矩阵"""
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
        """获取状态形状"""
        if self.state_format == StateFormat.VECTOR:
            return (self.PARTITIONS,) * 2
        elif self.state_format == StateFormat.MATRIX:
            return (self.matrix_full_width,) * 2
