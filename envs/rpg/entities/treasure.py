from envs.rpg.entity import Entity


class Treasure(Entity):
    REPRESENTATION = 2

    def start(self, world):
        pass

    def update(self, world):
        actor = world.get_actor_entity()
        if actor.position == self.position:
            world.status = world.Status.WON

    def destroy(self, world):
        pass