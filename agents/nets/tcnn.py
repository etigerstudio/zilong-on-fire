from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input
import tensorflow as tf


class TCNNNet(Model):
    def __init__(self, output_dim):
        """

        Args:
            output_dim: 网络需要n个输出，对应n个动作的累积回报
        """
        super(TCNNNet, self).__init__()
        self.c1 = Conv2D(filters=16, kernel_size=(4, 4), strides=2, activation='relu')  # 卷积层
        self.c2 = Conv2D(filters=32, kernel_size=(2, 2), strides=1, activation='relu')  # 卷积层
        self.flatten = Flatten()
        self.d1 = Dense(64, activation='relu')
        self.d2 = Dense(output_dim)

    def call(self, x):
        x, t = x
        x = self.c1(x)
        x = self.c2(x)
        x = tf.concat([self.flatten(x), tf.reshape(tf.cast(t[:, 0] / t[:, 1], dtype=tf.float32), (-1, 1))], axis=1)
        x = self.d1(x)
        y = self.d2(x)
        return y
