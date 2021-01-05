from envs.rpg.entity import Entity


class Treasure(Entity):
    REPRESENTATION = 3
    TREASURE_REWARD = 1

    def start(self, world):
        pass

    def update(self, world):
        actor = world.get_actor_entity()
        if actor.position == self.position and \
                actor.pose == actor.Pose.STANDING:
            world.status = world.Status.WON
            return self.TREASURE_REWARD

    def destroy(self, world):
        pass