# Game controller implementation
import numpy as np
import random

from env.fixed.basic import BasicFixedEnvironment
from net.q_table import QTable
from renderer.fixed.text import TextFixedRenderer


class Game:
    STATE_SHAPE = (BasicFixedEnvironment.PARTITIONS,) * 2
    ACTIONS = [
        BasicFixedEnvironment.Action.LEFT,
        BasicFixedEnvironment.Action.RIGHT,
        BasicFixedEnvironment.Action.NONE
    ]

    def __init__(self, max_rounds=100000, render_interval=2000):
        np.random.seed(1)
        random.seed(1)

        self.env = BasicFixedEnvironment()
        self.q_table = QTable(self.STATE_SHAPE, self.ACTIONS)
        self.renderer = TextFixedRenderer()
        self.max_rounds = max_rounds
        self.current_rounds = 0
        self.current_alive_steps = 0
        self.render_interval = render_interval

    def begin(self):
        state = self.env.reset()
        self.renderer.setup(info={'text': 0, 'delay': 0.0})
        self.renderer.update(state)

        while True:
            action = self.q_table.choose_action(state)
            new_state, reward, dead = self.env.step(action)
            self.q_table.learn(state, action, reward, new_state)

            if self.current_rounds % self.render_interval == 0:
                self.renderer.update(new_state, info={'text': action})

            if dead:
                if self.current_rounds % self.render_interval == 0:
                    self.renderer.close(info={'text': self.current_alive_steps})

                if self.current_rounds + 1 < self.max_rounds:
                    self.current_rounds += 1
                    self.current_alive_steps = 0
                    state = self.env.reset()

                    if self.current_rounds % self.render_interval == 0:
                        self.renderer.setup(info={'text': self.current_rounds})
                        self.renderer.update(state)

                    continue
                else:
                    break

            state = new_state
            self.current_alive_steps += 1


if __name__ == "__main__":
    game = Game()
    game.begin()
