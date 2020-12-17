# DeepQ network implementation
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense
import random
import numpy as np


class MyNet(Model):
    def __init__(self):
        super(MyNet, self).__init__()
        self.d1 = Dense(8, activation='relu')
        self.d2 = Dense(24, activation='relu')
        self.d3 = Dense(3)

    def call(self, x):
        x = self.d1(x)
        x = self.d2(x)
        y = self.d3(x)
        return y


class DeepQNet(Model):
    def __init__(self, state_shape, actions, eps_greedy=0.15, eps_decay=1,
                 reward_decay=0.9, optimizer=tf.optimizers.Adam(lr=0.001)):
        super(DeepQNet, self).__init__()
        self.net1 = MyNet()
        self.net2 = MyNet()
        self.output1 = self.net1(tf.ones([1, state_shape]))
        self.output2 = self.net2(tf.ones([1, state_shape]))
        # self.state_shape = state_shape
        self.state_shape = 2
        self.actions = actions
        self.eps_greedy = eps_greedy
        self.eps_decay = eps_decay
        self.reward_decay = reward_decay
        self.optimizer = optimizer
        self.exploration_enabled = True
        self.learn_time = 0
        self.update_time = 20
        self.buffer_count = 0
        self.buffer_size = 200
        self.buffer = np.zeros((self.buffer_size, self.state_shape*2+2))
        self.batch_size = 100
        self.gamma = 0.9

    def choose_action(self, state):
        # print(state, np.shape(state))
        if self.exploration_enabled and random.random() < self.eps_greedy:
            return random.choice(self.actions)
        else:
            state = np.reshape(state, (1, self.state_shape))
            return self.actions[np.argmax(self.net1(state))]

    def learn(self, old_state, action, reward, new_state):
        # 将与环境交互所得的序列存入buffer
        self.buffer[self.buffer_count % self.buffer_size][0:self.state_shape] = old_state
        # print("action:", action)
        self.buffer[self.buffer_count % self.buffer_size][self.state_shape:self.state_shape+1] = action.value
        self.buffer[self.buffer_count % self.buffer_size][self.state_shape+1:self.state_shape+2] = reward
        self.buffer[self.buffer_count % self.buffer_size][self.state_shape+2:self.state_shape*2+2] = new_state
        self.buffer_count += 1

        if self.buffer_count > self.buffer_size:
            #每训练20次更新net2
            if self.learn_time % self.update_time == 0:
                self.net2.set_weights(self.net1.get_weights())
            # 随机从buffer中取batchsize的数据
            index = random.randint(0, self.buffer_size - self.batch_size - 1)
            b_s = tf.constant(self.buffer[index:index + self.batch_size, 0:self.state_shape], dtype=tf.float32)
            b_a = tf.constant(self.buffer[index:index + self.batch_size, self.state_shape:self.state_shape+1],
                              dtype=tf.int32)
            b_r = tf.constant(self.buffer[index:index + self.batch_size, self.state_shape+1:self.state_shape+2],
                              dtype=tf.float32)
            b_s_ = tf.constant(self.buffer[index:index + self.batch_size, self.state_shape+2:self.state_shape*2+2],
                               dtype=tf.float32)

            # 训练网络
            with tf.GradientTape() as tape:
                # 计算R(s)
                q_output = self.net1(b_s)

                # 使用b_a来选取net中最终采取的抉择带来的Q值，防止选最大一方为最后Q值后，忽略了随机选择的存在。
                index = tf.expand_dims(tf.constant(np.arange(0, self.batch_size), dtype=tf.int32), 1)
                index_b_a = tf.concat((index, b_a), axis=1)
                R = tf.expand_dims(tf.gather_nd(q_output, index_b_a), 1)

                # 计算R(s+1)
                R_next = tf.expand_dims(tf.reduce_max(self.net2(b_s_), axis=1), 1)

                # 计算R(s+1) + r1
                R_truth = b_r + self.gamma * R_next

                # 计算loss
                loss = tf.reduce_mean(tf.losses.MSE(R_truth, R))
                # print("loss = %f" % loss)

                # 计算梯度更新网络
                gradients = tape.gradient(loss, self.net1.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, self.net1.trainable_variables))

            self.learn_time += 1
        self.eps_greedy *= self.eps_decay

    def set_exploration_enabled(self, enabled):
        self.exploration_enabled = enabled

