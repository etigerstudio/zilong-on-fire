# Game controller implementation
from envs.rpg.world import World
from matplotlib import pyplot as plt
import datetime

class RPGGame:
    def __init__(self,
                 env,
                 agent,
                 renderer,
                 max_rounds=100000,
                 test_interval=2000,
                 complete_threshold=25,
                 should_render_training=True,
                 return_t_when_step=False):
        """

        Args:
            env: The environment to interact with.
            agent: The agent to use to choose actions and learn from the environment.
            renderer:
            train_freq:
            max_rounds: The maximum rounds to play.
            test_interval: The round interval between tests.
            complete_threshold: The alive step threshold to complete training.
            should_render_training:
        """

        self.env = env
        self.agent = agent
        self.renderer = renderer
        self.max_rounds = max_rounds
        self.current_rounds = 0
        self.current_alive_steps = 0
        self.current_timestep = 0
        self.test_interval = test_interval
        self.complete_threshold = complete_threshold
        self.training_complete = False
        self.should_render_training = should_render_training
        self.return_t_when_step = return_t_when_step
        self.survival_time_all = []
        self.reward_count = 0
        self.reward_count_all = []
        self.save_path = "default"

    def begin(self):
        """启动游戏 & 开始训练智能体"""
        while self.current_rounds < self.max_rounds:
            self.current_alive_steps = 0
            state = self.env.reset()
            self.__render_new_round(state)
            while True:
                action = self.agent.choose_action(state)
                new_state, reward, game_over = self.env.step(action)
                if not self.training_complete:
                    self.agent.learn(state, action, reward, new_state, game_over)
                self.__render_round_step(new_state, (action, reward))
                self.reward_count += reward

                if not game_over:
                    state = new_state
                    self.current_alive_steps += 1
                    self.current_timestep += 1
                else:
                    self.survival_time_all.append(self.current_alive_steps)
                    self.reward_count_all.append(self.reward_count)
                    self.reward_count = 0
                    self.__render_round_end()
                    break

            self.__stop_training_if_necessary()
            self.current_timestep += 1
            self.current_rounds += 1

    def __stop_training_if_necessary(self):
        """判断是否需要停止训练"""
        if self.current_rounds % self.test_interval == 0:
            state = self.env.reset()
            self.agent.set_exploration_enabled(False)
            rounds_won = 0
            alive_history = []
            current_alive_steps = 0
            while True:
                action = self.agent.choose_action(state)
                state, reward, game_over = self.env.step(action)

                if game_over:
                    alive_history.append(current_alive_steps)
                    if self.env.world.status == World.Status.WON:
                        rounds_won += 1
                        # 若连续生存步数超过阈值则停止训练
                        if rounds_won >= self.complete_threshold:
                            self.training_complete = True
                            print(f'DQN is frozen! round:{self.current_rounds} timestep:{self.current_timestep}\n')
                            self.save_path = str(datetime.datetime.now().timestamp())
                            self.agent.train_net.save("../../models/rpg/" + self.save_path)
                            self.agent.print_loss_plot(self.save_path)
                            self.__print_survival_time_plot()
                            self.__print_accumulated_reward_plot()
                            break
                        state = self.env.reset()
                    else:
                        print(f'DQN training. r:{self.current_rounds} t:{self.current_timestep} -> '
                              f'w:{rounds_won} a:{sum(alive_history) / (rounds_won + 1)}\n')
                        self.agent.set_exploration_enabled(True)
                        break
                else:
                    current_alive_steps += 1

    def __render_new_round(self, state):
        """渲染新的回合"""
        if self.__should_render():
            self.renderer.setup(info={'text': self.current_rounds})
            self.renderer.update(state)

    def __render_round_step(self, new_state, action):
        """渲染回合内新的一步"""
        if self.__should_render():
            self.renderer.update(new_state, action)

    def __render_round_end(self):
        """渲染回合结束"""
        if self.__should_render():
            self.renderer.close(info={'text': self.current_alive_steps})

    def __should_render(self):
        """是否需要渲染"""
        return self.training_complete or \
               self.should_render_training and \
               self.current_rounds % self.test_interval == 0

    def __print_survival_time_plot(self):
        # 计算滑动平均, 取前50组的平均值
        average_x = [50]
        average_y = []
        sum = 0
        for i in range(0, 50):
            sum += self.survival_time_all[i]
        average_y.append(sum/50)
        for i in range(50, len(self.survival_time_all)):
            sum = sum + self.survival_time_all[i] - self.survival_time_all[i-50]
            average_x.append(i)
            average_y.append(sum/50)
        plt.title('Survival Time Curve')  # 图片标题
        plt.xlabel('Round')  # x轴变量名称
        plt.ylabel('Survival Time')  # y轴变量名称
        plt.plot(self.survival_time_all, label="$Survival Time$")  # 逐点画出survival_time值并连线，连线图标是Survival Time
        plt.plot(average_x, average_y, label="$Average Survival Time$")  # 逐点画出average_survival_time值并连线，连线图标是Average survival time
        plt.legend()  # 画出曲线图标
        plt.savefig("../../model/rpg/" + self.save_path + '/Survival Time Curve.png')
        # plt.savefig('./Survival Time Curve.png')
        plt.show()  # 画出图像

    def __print_accumulated_reward_plot(self):
        average_x = [50]
        average_y = []
        sum = 0
        for i in range(0, 50):
            sum += self.reward_count_all[i]
        average_y.append(sum/50)
        for i in range(50, len(self.reward_count_all)):
            sum = sum + self.reward_count_all[i] - self.reward_count_all[i - 50]
            average_x.append(i)
            average_y.append(sum/50)
        plt.title('Accumulated Reward Curve')  # 图片标题
        plt.xlabel('Round')  # x轴变量名称
        plt.ylabel('Accumulated Reward')  # y轴变量名称
        plt.plot(self.reward_count_all, label="$Accumulated Reward$")  # 逐点画出reward值并连线，连线图标是Accumulated Reward
        plt.plot(average_x, average_y, label="$Average Accumulated Reward$")  # 逐点画出reward值并连线，连线图标是Accumulated Reward
        plt.legend()  # 画出曲线图标
        plt.savefig("../../model/rpg/" + self.save_path + '/Accumulated Reward Curve.png')
        plt.show()  # 画出图像
