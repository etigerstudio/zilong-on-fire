from envs.rpg.entity import Entity


class Barrier(Entity):
    REPRESENTATION = 2
    BARRIER_REWARD = -1
    DESTROY_REWARD = 0.25

    def start(self, world):
        pass

    def update(self, world):
        actor = world.get_actor_entity()
        if actor.position == self.position:
            actor.destroy(world)
            return self.BARRIER_REWARD

    def destroy(self, world):
        world.remove_entity(self)
        return self.DESTROY_REWARD
