from envs.rpg.level import Level
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure


class TreasureTutorial(Level):
    def init(self):
        return 8, 8, [Actor([7, 3]), Treasure([0, 3])]
