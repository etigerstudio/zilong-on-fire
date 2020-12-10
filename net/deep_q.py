# DeepQ network implementation
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense


class DeepQ(Model):
    def __init__(self):
        super(DeepQ, self).__init__()
        self.d1 = Dense(8, activation='relu')
        self.d2 = Dense(24, activation='relu')
        self.d3 = Dense(8)

    def call(self, x, **kwargs):
        x = self.d1(x)
        x = self.d2(x)
        x = self.d3(x)
        return x
