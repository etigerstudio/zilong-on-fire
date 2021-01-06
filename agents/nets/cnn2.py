from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input


class CNN2Net(Model):
    def __init__(self, output_dim=3):
        """

        Args:
            output_dim: 网络需要三个输出，对应3个动作的累积回报
        """
        super(CNN2Net, self).__init__()
        self.c1 = Conv2D(filters=16, kernel_size=(4, 4), strides=2, activation='relu')  # 卷积层
        self.c2 = Conv2D(filters=32, kernel_size=(2, 2), strides=1, activation='relu')  # 卷积层
        self.flatten = Flatten()
        self.d1 = Dense(64, activation='relu')
        self.d3 = Dense(output_dim)

    def call(self, x):
        x = self.c1(x)
        x = self.c2(x)
        x = self.flatten(x)
        x = self.d1(x)
        # x = self.d2(x)
        y = self.d3(x)
        return y

    def model(self):
        x = Input(shape=(6, 6, 1))
        return Model(inputs=[x], outputs=self.call(x))

