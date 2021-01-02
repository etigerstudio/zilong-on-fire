from renderers.base import BaseRenderer
from time import sleep
import numpy as np


class TextRPGRenderer(BaseRenderer):
    def __init__(self, delay=0.1):
        self.delay = delay

    def setup(self, info=None):
        print(f'GAME START')
        sleep(self.delay)

    def update(self, state, info=None):
        print(self.__adjust_matrix(state))
        sleep(self.delay)

    def close(self, info=None):
        print(f'GAME OVER\n')
        sleep(self.delay)

    def __adjust_matrix(self, matrix):
        return np.flip(np.transpose(matrix), axis=0)