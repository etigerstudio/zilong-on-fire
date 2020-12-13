import random
import numpy as np


class QTable:
    def __init__(self, state_shape, actions, eps_greedy=0.9, reward_decay=0.9, learning_rate=0.05):
        self.state_shape = state_shape
        self.actions = actions
        self.q_table = np.random.random_sample((*state_shape, len(actions)))
        self.eps_greedy = eps_greedy
        self.reward_decay = reward_decay
        self.learning_rate = learning_rate

    def choose_action(self, state):
        if random.random() > self.eps_greedy:
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
