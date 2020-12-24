# Game controller implementation
import numpy as np
import random

from net.q_table import QTable
# from renderer.fixed.text import TextFixedRenderer
from renderer.fixed.twoD import TwoDFixedRenderer

class FixedGame:
    def __init__(self, environment, max_rounds=100000, render_interval=10, complete_threshold=100):
        np.random.seed(1)
        random.seed(1)

        self.env = environment(random_reset=True)
        self.q_table = QTable(environment.STATE_SHAPE, environment.ACTIONS)
        self.renderer = TwoDFixedRenderer()
        self.max_rounds = max_rounds
        self.current_rounds = 0
        self.current_alive_steps = 0
        self.render_interval = render_interval
        self.complete_threshold = complete_threshold
        self.training_complete = False

    def begin(self):
        while self.current_rounds < self.max_rounds:
            self.current_alive_steps = 0
            state = self.env.reset()
            self.__render_new_round(state)

            while True:
                action = self.q_table.choose_action(state)
                new_state, reward, dead = self.env.step(action)
                if not self.training_complete:
                    self.q_table.learn(state, action, reward, new_state)
                self.__render_round_step(new_state, action)

                if not dead:
                    state = new_state
                    self.current_alive_steps += 1
                else:
                    self.__render_round_end()
                    break

            self.__stop_training_if_necessary()
            self.current_rounds += 1

    def __stop_training_if_necessary(self):
        if self.current_rounds % self.render_interval == 0:
            state = self.env.reset()
            dead = False
            alive_steps = 0
            self.q_table.set_exploration_enabled(False)
            while not dead:
                action = self.q_table.choose_action(state)
                state, reward, dead = self.env.step(action)
                if alive_steps >= self.complete_threshold:
                    break
                alive_steps += 1

            print(f'{self.current_rounds} -> {alive_steps}\n')
            if alive_steps >= self.complete_threshold:
                self.training_complete = True
                print('QTable is frozen!\n')
            else:
                self.q_table.set_exploration_enabled(True)

    def __render_new_round(self, state):
        if self.__should_render():
            self.renderer.setup(info={'text': self.current_rounds, 'delay': 0})
            self.renderer.update(state)

    def __render_round_step(self, new_state, action):
        if self.__should_render():
            self.renderer.update(new_state, info={'text': f'{action} '
                                                          f'{self.env.current_arrow_distance}'})

    def __render_round_end(self):
        if self.__should_render():
            self.renderer.close(info={'text': self.current_alive_steps})

    def __should_render(self):
        return self.training_complete or \
               self.current_rounds % self.render_interval == 0
