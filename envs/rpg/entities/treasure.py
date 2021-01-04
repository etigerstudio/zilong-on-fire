from envs.rpg.entity import Entity


class Treasure(Entity):
    REPRESENTATION = 3
    TREASURE_REWARD = 10  # if 1, net won't converge

    def start(self, world):
        pass

    def update(self, world):
        actor = world.get_actor_entity()
        if actor.position == self.position:
            world.status = world.Status.WON
            return self.TREASURE_REWARD

    def destroy(self, world):
        pass