from tensorflow.keras import Model
from tensorflow.keras.layers import Dense


class FCNet(Model):
    def __init__(self, output_dim=3):
        super(FCNet, self).__init__()
        self.d1 = Dense(8, activation='relu')
        self.d2 = Dense(24, activation='relu')
        self.d3 = Dense(output_dim)

    def call(self, x):
        x = self.d1(x)
        x = self.d2(x)
        y = self.d3(x)
        return y
