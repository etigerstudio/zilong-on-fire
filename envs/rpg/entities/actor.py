from envs.rpg.entity import Entity
from enum import Enum


class Actor(Entity):
    REPRESENTATION = 4

    class Pose(Enum):
        STANDING = 0
        CROUCHING = 1
        JUMPING = 2

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
        self.prev_movement_offset = None  # For jump direction & wall collision

    def update(self, world):
        self.__handle_actor_input(world, *world.input)
        world.input = None

    def destroy(self, world):
        self.status = Actor.Status.DEAD
        world.status = world.Status.DEFEATED_ACTOR_DIED

    def __handle_actor_input(self, world, actor_movement, actor_spell):
        # Handle jumping in 2nd timestep
        if self.pose == Actor.Pose.JUMPING:
            self.pose = Actor.Pose.STANDING
            self.__move_actor(world, *self.prev_movement_offset)
            return

        # Handle standing or crouching
        if actor_movement == Actor.Movement.CROUCH:
            self.pose = Actor.Pose.CROUCHING
            return
        elif actor_movement == Actor.Movement.IDLE:
            self.pose = Actor.Pose.STANDING
            return
        else:  # Handle moving
            offset_x, offset_y = None, None
            if actor_movement == Actor.Movement.LEFTWARD:
                offset_x, offset_y = -1, 0
            elif actor_movement == Actor.Movement.FORWARD:
                offset_x, offset_y = 0, 1
            elif actor_movement == Actor.Movement.RIGHTWARD:
                offset_x, offset_y = 1, 0
            elif actor_movement == Actor.Movement.BACKWARD:
                offset_x, offset_y = 0, -1

            if actor_spell == Actor.Spell.IDLE:
                pass
            elif actor_spell == Actor.Spell.JUMP:
                # Handle jumping in 1st timestep
                self.pose = Actor.Pose.JUMPING
            elif actor_spell == Actor.Spell.SLASH:
                # Handle slashing
                slash_position = [self.position[0] + offset_x,
                                  self.position[1] + offset_y]
                entity = world.get_entity_by_position(slash_position)
                if entity is not None:
                    entity.destroy(world)
                offset_x, offset_y = 0, 0
            else:
                raise NotImplementedError

            # Save current movement offset
            self.prev_movement_offset = offset_x, offset_y
            self.__move_actor(world, offset_x, offset_y)

    def __move_actor(self, world, offset_x, offset_y):
        new_position_x = self.position[0] + offset_x
        new_position_y = self.position[1] + offset_y
        if new_position_x >= world.level_width or new_position_x < 0:
            new_position_x = self.position[0]
            self.destroy(world)  # Moved out of the world, punish!
        if new_position_y >= world.level_height or new_position_y < 0:
            new_position_y = self.position[1]
            self.destroy(world)  # Moved out of the world, punish!

        self.position = [new_position_x, new_position_y]
