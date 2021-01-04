from envs.rpg.level import Level
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure
from envs.rpg.entities.spike import Spike
from random import randrange


class SmallTutorial(Level):
    @staticmethod
    def init():
        entities = [
            Actor([randrange(3), 0]),
            Spike([1, 1]),
            Treasure([randrange(3), 2])
        ]

        return 3, 3, 10, entities
