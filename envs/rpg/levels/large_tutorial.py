from envs.rpg.level import Level
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure
from envs.rpg.entities.spike import Spike
from envs.rpg.entities.barrier import Barrier
from random import randrange


class LargeTutorial(Level):
    @staticmethod
    def init():
        entities = [
            Actor([5, 0]),
            *Level.make_entities(1, 2, 5, 3, Spike),
            Spike([2, 0]),
            Spike([2, 1]),
            Barrier([4, 0]),
            Barrier([4, 1]),
            Barrier([0, 2]),
            Barrier([0, 3]),
            Spike([3, 5]),
            Barrier([3, 4]),
            Barrier([5, 4]),
            Treasure([5, 5])
        ]

        return 6, 6, 30, entities
