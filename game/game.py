# Game controller implementation
from env.basic import BasicEnvironment
from net.deep_q import DeepQNet
from renderer.base import BaseRenderer


class Game:
    def __init__(self):
        self.env = BasicEnvironment()
        self.net = DeepQNet()
        self.renderer = BaseRenderer()

    def begin(self):
        pass