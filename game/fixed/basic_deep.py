# Game controller implementation
import numpy as np
import random

from game.fixed.base import FixedGame
from env.fixed.basic import BasicFixedEnvironment

if __name__ == "__main__":
    game = FixedGame(BasicFixedEnvironment, max_rounds=10000, render_interval=200)
    game.begin()
