from renderers.base import BaseRenderer
from time import sleep
from envs.base import StateFormat


class TextFixedRenderer(BaseRenderer):
    def __init__(self, delay=0.1, state_format=StateFormat.VECTOR):
        self.delay = delay
        self.state_format = state_format

    def setup(self, info=None):
        print(f'GAME START {self.__get_info_text(info)}')
        sleep(self.delay)

    def update(self, state, info=None):
        if self.state_format == StateFormat.VECTOR:
            print(f'Zilong:{state[0]} Arrow:{state[1]}'
                  f' {self.__get_info_text(info)}')
        elif self.state_format == StateFormat.MATRIX:
            print(f'{state}'
                  f' {self.__get_info_text(info)}')
        sleep(self.delay)

    def close(self, info=None):
        print(f'GAME OVER {self.__get_info_text(info)}\n')
        sleep(self.delay)

    def __get_info_text(self, info):
        if info is not None and 'text' in info:
            return info['text']

        return ''
