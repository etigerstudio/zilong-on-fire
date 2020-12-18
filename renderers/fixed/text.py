from renderers.base import BaseRenderer
from time import sleep


class TextFixedRenderer(BaseRenderer):
    def __init__(self):
        self.delay = 0.5

    def setup(self, info=None):
        if info is not None and 'delay' in info:
            self.delay = info['delay']
        print(f'GAME START {self.__get_info_text(info)}')
        sleep(self.delay)

    def update(self, state, info=None):
        print(f'Zilong:{state[0]} Arrow:{state[1]}'
              f' {self.__get_info_text(info)}')
        sleep(self.delay)

    def close(self, info=None):
        print(f'GAME OVER {self.__get_info_text(info)}\n')
        sleep(self.delay)

    def __get_info_text(self, info):
        if info is not None and 'text' in info:
            return info['text']

        return ''
