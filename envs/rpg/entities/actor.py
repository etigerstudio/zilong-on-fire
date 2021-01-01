from envs.rpg.entity import Entity
from enum import Enum
from envs.rpg.world import World


class Actor(Entity):
    REPRESENTATION = 1

    class Pose(Enum):
        STANDING = 0
        CROUCHING = 1
        JUMPING = 1

    class Movement(Enum):
        IDLE = 0
        LEFTWARD = 1
        FORWARD = 2
        RIGHTWARD = 3
        BACKWARD = 4
        CROUCH = 5

    class Spell(Enum):
        IDLE = 0
        JUMP = 1
        SLASH = 2

    class Status(Enum):
        ALIVE = 0
        DEAD = 1

    def start(self, world):
        self.pose = Actor.Pose.STANDING
        self.status = Actor.Status.ALIVE

    def update(self, world):
        self.__handle_actor_input(world, *world.input)
        world.input = None

    def destroy(self, world):
        self.status = Actor.Status.DEAD
        world.status = World.Status.DEFEATED

    def __handle_actor_input(self, world, actor_movement, actor_spell):
        if actor_movement == Actor.Movement.IDLE:
            self.pose = Actor.Pose.STANDING
        elif actor_movement == Actor.Movement.CROUCH:
            self.pose = Actor.Pose.CROUCHING
        elif actor_spell == Actor.Spell.SLASH:
            raise NotImplementedError  # TODO: Implement Slash Spell
        elif actor_movement == Actor.Movement.LEFTWARD:
            self.__move_actor(world, -1, 0)
        elif actor_movement == Actor.Movement.FORWARD:
            self.__move_actor(world, 0, 1)
        elif actor_movement == Actor.Movement.RIGHTWARD:
            self.__move_actor(world, 1, 0)
        elif actor_movement == Actor.Movement.BACKWARD:
            self.__move_actor(world, 0, -1)

        if actor_spell == Actor.Spell.JUMP:
            self.pose = Actor.Pose.JUMPING

    def __move_actor(self, world, offset_x, offset_y):
        new_position_x = self.position[0] + offset_x
        new_position_y = self.position[1] + offset_y
        if new_position_x >= world.level_width or new_position_x < 0:
            new_position_x = self.position[0]
        if new_position_y >= world.level_height or new_position_y < 0:
            new_position_y = self.position[1]

        return [new_position_x, new_position_y]
