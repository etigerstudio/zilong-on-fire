from envs.rpg.level import Level
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure
from envs.rpg.entities.spike import Spike
from envs.rpg.entities.barrier import Barrier
from random import randrange


class SlashSpike(Level):
    @staticmethod
    def init():
        entities = [
            Actor([randrange(4), 0]),
            *Level.make_entities(0, 1, 3, 1, Barrier),
            *Level.make_entities(0, 2, 3, 2, Spike),
            Treasure([randrange(4), 3])
        ]

        return 4, 4, 18, entities
