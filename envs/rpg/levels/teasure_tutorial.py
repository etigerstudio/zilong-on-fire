from envs.rpg.level import Level
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure


class TreasureTutorial(Level):
    @staticmethod
    def init():
        return 8, 8, [Actor([3, 0]), Treasure([4, 7])]
