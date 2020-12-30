from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input


class FCNet(Model):
    def __init__(self, output_dim=3):
        """

        Args:
            output_dim: 网络需要三个输出，对应3个动作的累积回报
        """
        super(FCNet, self).__init__()
        self.d1 = Dense(8, activation='relu')
        self.d2 = Dense(24, activation='relu')
        self.d3 = Dense(output_dim)

    def call(self, x):
        x = self.d1(x)
        x = self.d2(x)
        y = self.d3(x)
        return y

    def model(self):
        x = Input(shape=(1, 2))
        return Model(inputs=[x], outputs=self.call(x))