# DeepQ network implementation
import tensorflow as tf
from tensorflow.keras import Model
import random
import numpy as np
from envs.base import StateFormat
from matplotlib import pyplot as plt


class DeepQNet(Model):
    """基于神经网络的强化学习"""
    def __init__(self,
                 state_shape,
                 actions,
                 net,
                 state_format=StateFormat.MATRIX,
                 eps_initial=1.0,
                 eps_minimum=0.15,
                 eps_decay_mode="LINEAR",
                 eps_decay_steps=1000,
                 eps_decay=1.0,
                 reward_decay=0.9,
                 optimizer=tf.optimizers.Adam,
                 use_double=True,
                 learning_rate=0.001,
                 train_freq=4,
                 target_update_freq=50,
                 buffer_size=2000,
                 batch_size=32,
                 gamma_discount=0.9,
                 use_one_hot=False):
        """

        Args:
            state_shape: 状态的shape
            actions: 动作
            net: 选取的网络
            state_format: 状态的格式，默认是矩阵
            eps_greedy: 探索的概率
            eps_initial: 探索概率的初始值
            eps_minimun：探索概率的最小值
            eps_decay_mode: 探索概率的衰减模式，可以是LINEAR或者EXPONENTIAL
            eps_decay_steps: 探索概率将在多少轮后衰减到最小值，仅在探索概率衰减模式是LINEAR时有用
            eps_decay: 探索衰减率，仅在探索概率衰减模式是EXPONENTIAL时有用
            reward_decay: 回报衰减率
            optimizer: 网络优化器
            train_freq: 连续网络训练轮次之间间隔的时间步
            target_update_freq: 每多少轮训练后更新目标网络
            buffer_size: 记忆的容量
            batch_size: 每次训练的batch的大小
            gamma_discount: 计算真实累积回报时，R_next的比重
            use_one_hot: 是否使用独热码
        """
        super(DeepQNet, self).__init__()
        self.state_shape = state_shape
        self.state_len = len(state_shape)
        self.state_one_hot_len = np.sum(state_shape)
        self.state_format = state_format
        self.actions = actions
        self.train_net = net(len(actions))
        self.target_net = net(len(actions))
        self.eps_initial = eps_initial
        self.eps_minimum = eps_minimum
        self.eps_greedy = self.eps_initial
        self.eps_decay_mode = eps_decay_mode
        self.eps_decay_steps = eps_decay_steps
        self.eps_decay = eps_decay
        self.reward_decay = reward_decay
        self.optimizer = optimizer(lr=learning_rate)
        self.use_double = use_double
        self.exploration_enabled = True
        self.network_train_times = 0
        self.sample_learn_times = 0
        self.train_freq = train_freq
        self.target_update_freq = target_update_freq
        self.buffer_size = buffer_size
        self.__init_buffer()
        self.batch_size = batch_size
        self.gamma_discount = gamma_discount
        self.use_one_hot = use_one_hot
        self.__init_net_weights()
        self.loss_history = []
        self.train_loss_results = []

    def choose_action(self, state):
        """通过当前状态选择一个动作

        Args:
            state: 输入状态

        Returns:
            action：选择的动作

        """
        # print(state, np.shape(state))
        if self.exploration_enabled and random.random() < self.eps_greedy:
            return random.choice(self.actions)
        else:
            state = self.__reshape_state(state)
            return self.actions[np.argmax(self.train_net(self.__preprocess_state(state)))]

    def learn(self, old_state, action, reward, new_state, game_over=None):
        """缓存游戏的经验并训练网络

        Args:
            old_state: 当前状态
            action: 当前状态下采取的动作
            reward: 该动作的奖励
            new_state: 采取动作后环境的新状态
        """
        # Storing
        self.__save_to_buffer(old_state, action.value, reward, new_state, game_over)
        self.sample_learn_times += 1

        if self.sample_learn_times == self.buffer_size:
            print("DQN Training Began!\n")

        # Training
        if self.sample_learn_times % self.train_freq == 0 and \
                self.sample_learn_times >= self.buffer_size:
            if self.network_train_times % self.target_update_freq == 0:
                self.target_net.set_weights(self.train_net.get_weights())
            b_s, b_a, b_r, b_s_, b_d = self.__sample_from_buffer()

            if self.use_double:
                actions = tf.expand_dims(tf.argmax(self.train_net(self.__preprocess_state(b_s_)), axis=1), 1)
                R_next = tf.expand_dims(
                    tf.gather_nd(self.target_net(self.__preprocess_state(b_s_)), actions, batch_dims=1), 1)
            else:
                R_next = tf.expand_dims(tf.reduce_max(self.target_net(self.__preprocess_state(b_s_)), axis=1), 1)
            R_truth = b_r + (1 - b_d) * self.gamma_discount * R_next  # b_d == 1 when in terminal state

            with tf.GradientTape() as tape:
                q_output = self.train_net(self.__preprocess_state(b_s))
                R = tf.expand_dims(tf.gather_nd(q_output, b_a, batch_dims=1), 1)
                loss = tf.reduce_mean(tf.losses.MSE(R_truth, R))
                gradients = tape.gradient(loss, self.train_net.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, self.train_net.trainable_variables))

            self.network_train_times += 1

            self.loss_history.append(loss)
            self.train_loss_results.append(loss)
            if self.network_train_times % 200 == 0:  # Loss dumper, will be removed in future
                print(f'loss: {np.sum(self.loss_history) / 200} epoch: {self.network_train_times}\n')
                self.loss_history = []
            self.__update_eps()

    def set_exploration_enabled(self, enabled):
        self.exploration_enabled = enabled

    def __init_net_weights(self):
        if self.state_format == StateFormat.VECTOR:
            if self.use_one_hot:
                self.train_net(tf.zeros((1, self.state_one_hot_len)))
                self.target_net(tf.zeros((1, self.state_one_hot_len)))
            else:
                self.train_net(tf.zeros((1, self.state_len)))
                self.target_net(tf.zeros((1, self.state_len)))
        elif self.state_format == StateFormat.MATRIX:
            self.train_net.build((1, *self.state_shape, 1))
            self.target_net.build((1, *self.state_shape, 1))
        else:
            raise NotImplementedError

        self.target_net.set_weights(self.train_net.get_weights())

    def __reshape_state(self, state):
        if self.state_format == StateFormat.VECTOR:
            return np.reshape(state, (1, self.state_len))
        elif self.state_format == StateFormat.MATRIX:
            return np.reshape(state, (1, *self.state_shape, 1))
        else:
            raise NotImplementedError

    def __preprocess_state(self, state):
        return tf.constant(tf.reshape(tf.one_hot(state, 4), [-1, self.state_one_hot_len]), dtype=tf.float32) \
            if self.use_one_hot else tf.constant(state, dtype=tf.float32)

    def __init_buffer(self):
        if self.state_format == StateFormat.VECTOR:
            self.buffer = np.zeros((self.buffer_size, self.state_len * 2 + 2))
        elif self.state_format == StateFormat.MATRIX:
            self.buffer = [None] * self.buffer_size
        else:
            raise NotImplementedError

    def __sample_from_buffer(self):
        if self.state_format == StateFormat.VECTOR:
            random_buffer = random.sample(range(self.buffer_size), self.batch_size)
            b_s = tf.constant(self.buffer[random_buffer, 0:self.state_len], dtype=tf.float32)
            b_a = tf.constant(self.buffer[random_buffer, self.state_len:self.state_len + 1], dtype=tf.int32)
            b_r = tf.constant(self.buffer[random_buffer, self.state_len + 1:self.state_len + 2], dtype=tf.float32)
            b_s_ = tf.constant(self.buffer[random_buffer, self.state_len + 2:self.state_len * 2 + 2], dtype=tf.float32)
            b_d = tf.constant(self.buffer[random_buffer, self.state_len * 2 + 2:self.state_len * 2 + 3], dtype=tf.float32)
        elif self.state_format == StateFormat.MATRIX:
            random_buffer = random.sample(self.buffer, self.batch_size)
            b_s, b_a, b_r, b_s_, b_d = [], [], [], [], []
            for s, a, r, s_, d in random_buffer:
                b_s.append(s)
                b_a.append(a)
                b_r.append(r)
                b_s_.append(s_)
                b_d.append(d)
            b_s = tf.cast(tf.expand_dims(b_s, -1), dtype=tf.float32)
            b_a = tf.cast(tf.expand_dims(b_a, -1), dtype=tf.int32)
            b_r = tf.cast(tf.expand_dims(b_r, -1), dtype=tf.float32)
            b_s_ = tf.cast(tf.expand_dims(b_s_, -1), dtype=tf.float32)
            b_d = tf.cast(tf.expand_dims(b_d, -1), dtype=tf.float32)
        else:
            raise NotImplementedError

        return b_s, b_a, b_r, b_s_, b_d

    def __save_to_buffer(self, old_state, action, reward, new_state, game_over=None):
        if self.state_format == StateFormat.VECTOR:
            self.buffer[self.sample_learn_times % self.buffer_size][0:self.state_len] = old_state
            self.buffer[self.sample_learn_times % self.buffer_size][self.state_len:self.state_len + 1] = action
            self.buffer[self.sample_learn_times % self.buffer_size][self.state_len + 1:self.state_len + 2] = reward
            self.buffer[self.sample_learn_times % self.buffer_size][self.state_len + 2:self.state_len * 2 + 2] = new_state
            self.buffer[self.sample_learn_times % self.buffer_size][self.state_len * 2 + 2:self.state_len * 2 + 3] = game_over
        elif self.state_format == StateFormat.MATRIX:
            self.buffer[self.sample_learn_times % self.buffer_size] = (old_state, action, reward, new_state, game_over)
        else:
            raise NotImplementedError

    def __update_eps(self):
        if self.eps_decay_mode is not None:
            if self.eps_decay_mode == 'LINEAR':
                eps = self.eps_initial - (self.eps_initial - self.eps_minimum) * self.network_train_times / self.eps_decay_steps
                if eps > self.eps_minimum:
                    self.eps_greedy = eps
                else:
                    self.eps_greedy = self.eps_minimum
            elif self.eps_decay_mode == 'EXPONENTIAL':
                self.eps_greedy *= self.eps_decay
            else:
                raise NotImplementedError

    def print_loss_plot(self):
        # 计算滑动平均, 取前50组的平均值
        average_x = [50]
        average_y = []
        sum = 0
        for i in range(0, 50):
            sum += self.train_loss_results[i]
        average_y.append(sum/50)
        for i in range(50, len(self.train_loss_results)):
            sum = sum + self.train_loss_results[i] - self.train_loss_results[i-50]
            average_x.append(i)
            average_y.append(sum/50)
        # 绘制 loss 曲线
        plt.title('Loss Function Curve')  # 图片标题
        plt.xlabel('Epoch')  # x轴变量名称
        plt.ylabel('Loss')  # y轴变量名称
        plt.plot(self.train_loss_results, label="$Loss$")  # 逐点画出trian_loss_results值并连线，连线图标是Loss
        plt.plot(average_x, average_y, label="$Average Loss$")  # 逐点画出average_loss值并连线，连线图标是Average Loss
        plt.legend()  # 画出曲线图标
        plt.show()  # 画出图像
