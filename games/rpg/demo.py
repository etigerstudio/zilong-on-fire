from envs.rpg.world import World
from envs.rpg.levels.teasure_tutorial import TreasureTutorial

world = World(TreasureTutorial())
print(world.get_matrix_representation())
print(world.get_text_representation())