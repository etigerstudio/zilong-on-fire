import random
import numpy as np


class QTable:
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
        if self.exploration_enabled and random.random() < self.eps_greedy:
            return random.choice(self.actions)
        else:
            return self.actions[np.argmax(self.q_table[state])]

    def learn(self, old_state, action, reward, new_state):
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
