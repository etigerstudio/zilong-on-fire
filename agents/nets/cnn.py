from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input


class CNNet(Model):
    def __init__(self, output_dim=3):
        super(CNNet, self).__init__()
        self.c1 = Conv2D(filters=6, kernel_size=(3, 3), padding='same', activation='relu')  # 卷积层
        self.c2 = Conv2D(filters=6, kernel_size=(3, 3), padding='same', activation='relu')  # 卷积层
        self.flatten = Flatten()
        self.d1 = Dense(128, activation='relu')
        # self.d2 = Dense(32, activation='relu')
        self.d3 = Dense(output_dim, activation='softmax')

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

