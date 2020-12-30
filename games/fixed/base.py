# Game controller implementation
import numpy as np
import random

from renderers.fixed.text import TextFixedRenderer
# from renderers.fixed.twoD import TwoDFixedRenderer


class FixedGame:
    def __init__(self, env, agent, renderer, max_rounds=100000, test_interval=2000, complete_threshold=200):
        """

        Args:
            env: The environment to interact with.
            agent: The agent to use to choose actions and learn from the environment.
            max_rounds: The maximum rounds to play.
            test_interval: The round interval between tests.
            complete_threshold: The alive step threshold to complete training.
        """
        np.random.seed(1)
        random.seed(1)

        self.env = env
        self.agent = agent
        self.renderer = renderer
        self.max_rounds = max_rounds
        self.current_rounds = 0
        self.current_alive_steps = 0
        self.test_interval = test_interval
        self.complete_threshold = complete_threshold
        self.training_complete = False

    def begin(self):
        """启动游戏 & 开始训练智能体"""
        while self.current_rounds < self.max_rounds:
            self.current_alive_steps = 0
            state = self.env.reset()
            self.__render_new_round(state)

            while True:
                action = self.agent.choose_action(state)
                new_state, reward, dead = self.env.step(action)
                if not self.training_complete:
                    self.agent.learn(state, action, reward, new_state)
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
        """判断是否需要停止训练"""
        if self.current_rounds % self.test_interval == 0:
            state = self.env.reset()
            dead = False
            alive_steps = 0
            self.agent.set_exploration_enabled(False)
            while not dead:
                action = self.agent.choose_action(state)
                state, reward, dead = self.env.step(action)
                if alive_steps >= self.complete_threshold:
                    break
                alive_steps += 1

            print(f'{self.current_rounds} -> {alive_steps}\n')
            # 若连续生存步数超过阈值则停止训练
            if alive_steps >= self.complete_threshold:
                self.training_complete = True
                print('DQN is frozen!\n')
            else:
                self.agent.set_exploration_enabled(True)

    def __render_new_round(self, state):
        """渲染新的回合"""
        if self.__should_render():
            self.renderer.setup(info={'text': self.current_rounds})
            self.renderer.update(state)

    def __render_round_step(self, new_state, action):
        """渲染回合内新的一步"""
        if self.__should_render():
            self.renderer.update(new_state, info={'text': f'{action} '
                                                          f'{self.env.current_arrow_distance}'})

    def __render_round_end(self):
        """渲染回合结束"""
        if self.__should_render():
            self.renderer.close(info={'text': self.current_alive_steps})

    def __should_render(self):
        """是否需要渲染"""
        return self.training_complete or \
               self.current_rounds % self.test_interval == 0
