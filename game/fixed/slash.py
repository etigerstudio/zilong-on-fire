# Game controller implementation
import numpy as np
import random

from game.fixed.base import FixedGame
from env.fixed.slash import SlashFixedEnvironment

if __name__ == "__main__":
    game = FixedGame(SlashFixedEnvironment)
    game.begin()
