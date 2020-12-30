# DeepQ network implementation
import tensorflow as tf
from tensorflow.keras import Model
import random
import numpy as np
from envs.base import StateFormat


class DeepQNet(Model):
    """基于神经网络的强化学习"""
    def __init__(self,
                 state_shape,
                 actions,
                 net,
                 state_format=StateFormat.MATRIX,
                 eps_greedy=0.25,
                 eps_decay=1,
                 reward_decay=0.9,
                 optimizer=tf.optimizers.Adam(lr=0.001),
                 target_update_frequency=50,
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
            eps_decay: 探索衰减率
            reward_decay: 回报衰减率
            optimizer: 网络优化器
            target_update_frequency: 每多少轮训练后更新目标网络
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
        self.eps_greedy = eps_greedy
        self.eps_decay = eps_decay
        self.reward_decay = reward_decay
        self.optimizer = optimizer
        self.exploration_enabled = True
        self.learn_time = 0
        self.target_update_frequency = target_update_frequency
        self.sample_count = 0
        self.buffer_size = buffer_size
        self.__init_buffer()
        self.batch_size = batch_size
        self.gamma_discount = gamma_discount
        self.use_one_hot = use_one_hot
        self.__init_net_weights()

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

    def learn(self, old_state, action, reward, new_state):
        """缓存游戏的经验并训练网络

        Args:
            old_state: 当前状态
            action: 当前状态下采取的动作
            reward: 该动作的奖励
            new_state: 采取动作后环境的新状态
        """
        self.__save_to_buffer(old_state, action.value, reward, new_state)
        self.sample_count += 1

        if self.sample_count == self.buffer_size:
            print("DQN Training Began!\n")
        if self.sample_count >= self.buffer_size:
            if self.learn_time % self.target_update_frequency == 0:
                self.target_net.set_weights(self.train_net.get_weights())
            b_s, b_a, b_r, b_s_ = self.__sample_from_buffer()
            with tf.GradientTape() as tape:
                q_output = self.train_net(self.__preprocess_state(b_s))
                index = tf.expand_dims(tf.constant(np.arange(0, self.batch_size), dtype=tf.int32), -1)
                index_b_a = tf.concat((index, b_a), axis=1)

                R = tf.expand_dims(tf.gather_nd(q_output, index_b_a), 1)
                R_next = tf.expand_dims(tf.reduce_max(self.target_net(self.__preprocess_state(b_s_)), axis=1), 1)
                R_truth = b_r + self.gamma_discount * R_next

                loss = tf.reduce_mean(tf.losses.MSE(R_truth, R))
                gradients = tape.gradient(loss, self.train_net.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, self.train_net.trainable_variables))

            self.learn_time += 1
        self.eps_greedy *= self.eps_decay

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

    def __reshape_state(self, state):
        if self.state_format == StateFormat.VECTOR:
            return np.reshape(state, (1, self.state_len))
        elif self.state_format == StateFormat.MATRIX:
            return np.reshape(state, (1, 6, 6, 1))
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
        random_buffer = None
        b_s, b_a, b_r, b_s_ = None, None, None, None
        if self.state_format == StateFormat.VECTOR:
            random_buffer = random.sample(range(self.buffer_size), self.batch_size)
            b_s = tf.constant(self.buffer[random_buffer, 0:self.state_len], dtype=tf.float32)
            b_a = tf.constant(self.buffer[random_buffer, self.state_len:self.state_len + 1], dtype=tf.int32)
            b_r = tf.constant(self.buffer[random_buffer, self.state_len + 1:self.state_len + 2], dtype=tf.float32)
            b_s_ = tf.constant(self.buffer[random_buffer, self.state_len + 2:self.state_len * 2 + 2], dtype=tf.float32)
        elif self.state_format == StateFormat.MATRIX:
            random_buffer = random.sample(self.buffer, self.batch_size)
            b_s = [store[0] for store in random_buffer]
            b_a = [store[1] for store in random_buffer]
            b_r = [store[2] for store in random_buffer]
            b_s_ = [store[3] for store in random_buffer]
            b_s = tf.cast(tf.expand_dims(b_s, -1), dtype=tf.float32)
            b_a = tf.expand_dims(b_a, -1)
            b_r = tf.expand_dims(b_r, -1)
            b_s_ = tf.cast(tf.expand_dims(b_s_, -1), dtype=tf.float32)
        else:
            raise NotImplementedError
        return b_s, b_a, b_r, b_s_

    def __save_to_buffer(self, old_state, action, reward, new_state):
        if self.state_format == StateFormat.VECTOR:
            self.buffer[self.sample_count % self.buffer_size][0:self.state_len] = old_state
            self.buffer[self.sample_count % self.buffer_size][self.state_len:self.state_len + 1] = action
            self.buffer[self.sample_count % self.buffer_size][self.state_len + 1:self.state_len + 2] = reward
            self.buffer[self.sample_count % self.buffer_size][self.state_len + 2:self.state_len * 2 + 2] = new_state
        elif self.state_format == StateFormat.MATRIX:
            self.buffer[self.sample_count % self.buffer_size] = (old_state, action, reward, new_state)
        else:
            raise NotImplementedError