from envs.rpg.level import Level
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure
from envs.rpg.entities.spike import Spike
from random import randrange


class MediumTutorial(Level):
    @staticmethod
    def init():
        entities = [
            Actor([randrange(6), randrange(2)]),
            Spike([0, 3]),
            Spike([2, 3]),
            Spike([3, 3]),
            Spike([4, 3]),
            Spike([0, 2]),
            Spike([2, 2]),
            Spike([3, 2]),
            Spike([5, 2]),
            Treasure([randrange(6), 4 + randrange(2)])
        ]

        return 6, 6, 15, entities
