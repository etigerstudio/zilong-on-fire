from envs.rpg.level import Level
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure
from random import randrange


class TreasureTutorial(Level):
    @staticmethod
    def init():
        # return 4, 4, [Actor([0, 0]), Treasure([2, 2])]
        return 4, 4, [Actor([randrange(4), randrange(2)]), Treasure([randrange(4), 2 + randrange(2)])]
