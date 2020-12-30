import random
import numpy as np


class QTable:
    """基于Q表的强化学习"""
    def __init__(self, state_shape, actions, eps_greedy=0.15, eps_decay=1, reward_decay=0.9, learning_rate=0.03):
        self.state_shape = state_shape
        self.actions = actions
        self.q_table = np.random.random_sample((*state_shape, len(actions)))
        self.eps_greedy = eps_greedy
        self.eps_decay = eps_decay
        self.reward_decay = reward_decay
        self.learning_rate = learning_rate
        self.exploration_enabled = True

    def choose_action(self, state):
        """包含探索情况下，根据当前状态选取动作

        Args:
            state: 当前状态

        Returns:
            action：选取的动作
        """
        if self.exploration_enabled and random.random() < self.eps_greedy:
            return random.choice(self.actions)
        else:
            return self.actions[np.argmax(self.q_table[state])]

    def learn(self, old_state, action, reward, new_state):
        """

        Args:
            old_state: 当前状态
            action: 当前状态下采取的动作
            reward: 该动作的奖励
            new_state: 采取动作后环境的新状态

        """
        self.q_table[old_state][action.value] = \
            self.q_table[old_state][action.value] + \
            self.learning_rate * (
                    reward +
                    self.reward_decay * np.max(self.q_table[new_state]) -
                    self.q_table[old_state][action.value]
            )
        self.eps_greedy *= self.eps_decay

    def set_exploration_enabled(self, enabled):
        self.exploration_enabled = enabled
