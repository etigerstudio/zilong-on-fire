# DeepQ network implementation
import tensorflow as tf
from tensorflow.keras import Model
import random
import numpy as np


class DeepQNet(Model):
    def __init__(self,
                 state_shape,
                 actions,
                 net,
                 eps_greedy=0.15,
                 eps_decay=1,
                 reward_decay=0.9,
                 optimizer=tf.optimizers.Adam(lr=0.001),
                 target_update_frequency=20,
                 buffer_size=2000,
                 batch_size=100,
                 gamma_discount=0.9,
                 use_one_hot=False):
        super(DeepQNet, self).__init__()
        self.state_shape = state_shape
        self.state_len = len(state_shape)
        self.state_one_hot_len = np.sum(state_shape)
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
        self.buffer_count = 0
        self.buffer_size = buffer_size
        self.buffer = np.zeros((self.buffer_size, self.state_len * 2 + 2))
        self.batch_size = batch_size
        self.gamma_discount = gamma_discount
        self.use_one_hot = use_one_hot
        self.__init_net_weights()

    def choose_action(self, state):
        # print(state, np.shape(state))
        if self.exploration_enabled and random.random() < self.eps_greedy:
            return random.choice(self.actions)
        else:
            state = np.reshape(state, (1, self.state_len))
            return self.actions[np.argmax(self.train_net(self.__to_one_hot_if_needed(state)))]

    def learn(self, old_state, action, reward, new_state):
        # 将与环境交互所得的序列存入buffer
        self.buffer[self.buffer_count % self.buffer_size][0:self.state_len] = old_state
        # print("action:", action)
        self.buffer[self.buffer_count % self.buffer_size][self.state_len:self.state_len + 1] = action.value
        self.buffer[self.buffer_count % self.buffer_size][self.state_len + 1:self.state_len + 2] = reward
        self.buffer[self.buffer_count % self.buffer_size][self.state_len + 2:self.state_len * 2 + 2] = new_state
        self.buffer_count += 1

        if self.buffer_count == self.buffer_size:
            print("DQN Training Began!\n")
        if self.buffer_count >= self.buffer_size:
            # 每训练20次更新net2
            if self.learn_time % self.target_update_frequency == 0:
                self.target_net.set_weights(self.train_net.get_weights())
            # 随机从buffer中取batchsize的数据
            index = random.randint(0, self.buffer_size - self.batch_size - 1)
            b_s = self.buffer[index:index + self.batch_size, 0:self.state_len]
            b_a = tf.constant(self.buffer[index:index + self.batch_size,
                              self.state_len:self.state_len + 1], dtype=tf.int32)
            b_r = tf.constant(self.buffer[index:index + self.batch_size,
                              self.state_len + 1:self.state_len + 2], dtype=tf.float32)
            b_s_ = self.buffer[index:index + self.batch_size, self.state_len + 2:self.state_len * 2 + 2]

            # 训练网络
            with tf.GradientTape() as tape:
                # 计算R(s)
                q_output = self.train_net(self.__to_one_hot_if_needed(b_s))

                # 使用b_a来选取net中最终采取的抉择带来的Q值，防止选最大一方为最后Q值后，忽略了随机选择的存在。
                index = tf.expand_dims(tf.constant(np.arange(0, self.batch_size), dtype=tf.int32), 1)
                index_b_a = tf.concat((index, b_a), axis=1)
                R = tf.expand_dims(tf.gather_nd(q_output, index_b_a), 1)

                # 计算R(s+1)
                R_next = tf.expand_dims(tf.reduce_max(self.target_net(self.__to_one_hot_if_needed(b_s_)), axis=1), 1)

                # 计算R(s+1) + r1
                R_truth = b_r + self.gamma_discount * R_next

                # 计算loss
                loss = tf.reduce_mean(tf.losses.MSE(R_truth, R))
                # print("loss = %f" % loss)

                # 计算梯度更新网络
                gradients = tape.gradient(loss, self.train_net.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, self.train_net.trainable_variables))

            self.learn_time += 1
        self.eps_greedy *= self.eps_decay

    def set_exploration_enabled(self, enabled):
        self.exploration_enabled = enabled

    def __init_net_weights(self):
        if self.use_one_hot:
            self.train_net(tf.zeros((1, self.state_one_hot_len)))
            self.target_net(tf.zeros((1, self.state_one_hot_len)))
        else:
            self.train_net(tf.zeros((1, self.state_len)))
            self.target_net(tf.zeros((1, self.state_len)))

    def __to_one_hot_if_needed(self, state):
        return tf.constant(tf.reshape(tf.one_hot(state, 4), [-1, self.state_one_hot_len]), dtype=tf.float32) \
            if self.use_one_hot else tf.constant(state, dtype=tf.float32)
