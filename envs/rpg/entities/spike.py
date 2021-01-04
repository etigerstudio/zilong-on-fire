from envs.rpg.entity import Entity


class Spike(Entity):
    REPRESENTATION = 1
    SPIKE_REWARD = -1

    def start(self, world):
        pass

    def update(self, world):
        actor = world.get_actor_entity()
        if not actor.pose == actor.Pose.JUMPING and \
                actor.position == self.position:
            world.status = world.Status.DEFEATED_ACTOR_DIED
            return self.SPIKE_REWARD

    def destroy(self, world):
        pass
