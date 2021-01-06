from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input
import tensorflow as tf


class TCNNNet(Model):
    def __init__(self, output_dim=3):
        """

        Args:
            output_dim: 网络需要n个输出，对应n个动作的累积回报
        """
        super(TCNNNet, self).__init__()
        self.c1 = Conv2D(filters=16, kernel_size=(4, 4), strides=2, activation='relu')  # 卷积层
        self.c2 = Conv2D(filters=32, kernel_size=(3, 3), strides=1, activation='relu')  # 卷积层
        self.flatten = Flatten()
        self.d1 = Dense(64, activation='relu')
        self.d3 = Dense(output_dim)
        self.t = 0
        self.t_max = None

    def call(self, x):
        x, t = x
        x = self.c1(x)
        # x = self.c2(x)
        x = tf.concat([self.flatten(x), tf.reshape(tf.cast(t / self.t_max, dtype=tf.float32), (1, 1))], axis=1)
        x = self.d1(x)
        x = self.d2(x)
        y = self.d3(x)
        return y

    def model(self):
        x = Input(shape=(6, 6, 1))
        return Model(inputs=[x], outputs=self.call(x))

    def init_t(self, t_max):
        self.t_max = t_max

    def set_t(self, t):
        self.t = t
