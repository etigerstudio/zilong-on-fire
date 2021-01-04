from envs.rpg.entity import Entity


class Wall(Entity):
    REPRESENTATION = 5

    def start(self, world):
        pass

    def update(self, world):
        actor = world.get_actor_entity()
        if actor.position == self.position:
            offset = actor.prev_movement_offset
            actor.position[0] -= offset[0]
            actor.position[1] -= offset[1]

    def destroy(self, world):
        pass
