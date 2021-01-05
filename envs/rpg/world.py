from enum import Enum
import numpy as np
from envs.rpg.entities.actor import Actor
from envs.rpg.entities.treasure import Treasure
from envs.rpg.entity import Entity


class World:
    BLANK_SPACE_VALUE = 0
    ACTOR_ALIVE_REWARD = 0
    ACTOR_DEAD_REWARD = -1
    TIMESTEP_EXPIRATION_REWARD = -1

    class Status(Enum):
        PLAYING = 0
        WON = 1
        DEFEATED_ACTOR_DIED = 2
        DEFEATED_MAX_TIMESTEP_EXPIRED = 3

    def __init__(self,
                 level,
                 alive_reward=ACTOR_ALIVE_REWARD,
                 dead_reward=ACTOR_DEAD_REWARD,
                 timestep_expiration_reward=TIMESTEP_EXPIRATION_REWARD):
        self.level_stub = level
        self.alive_reward = alive_reward
        self.dead_reward = dead_reward
        self.timestep_expiration_reward = timestep_expiration_reward
        self.__reset_world()

    def step(self, actor_movement, actor_spell):
        """Take a step in the world.

        Args:
            actor_movement:
            actor_spell:

        Returns:
            game_over:
            reward:
        """
        # Forwarding input
        self.input = actor_movement, actor_spell
        prev_default_reward = self.__get_current_default_reward()

        game_over, reward = False, 0
        for e in self.entities:  # TODO: Ensure actor is updated first.
            r = e.update(self)
            if r is not None:
                reward += r
        if reward == 0:
            reward = self.ACTOR_ALIVE_REWARD
            # reward = self.__get_current_default_reward() - prev_default_reward

        # Check if actor has died
        if self.status == World.Status.DEFEATED_ACTOR_DIED:
            game_over = True
            reward = World.ACTOR_DEAD_REWARD

        # Check if maximum timestep has expired
        self.time_elapsed += 1
        if self.time_elapsed == self.time_limit:
            self.status = World.Status.DEFEATED_MAX_TIMESTEP_EXPIRED
            game_over = True
            reward = World.TIMESTEP_EXPIRATION_REWARD

        # Check if the actor has won the game
        if self.status == World.Status.WON:
            game_over = True

        return game_over, reward

    def reset(self):
        self.__reset_world()

    def __reset_world(self):
        self.level_width, \
        self.level_height, \
        self.time_limit, \
        self.entities = self.level_stub.init()
        self.__start_entities()
        self.__reset_default_rewards()
        self.status = self.Status.PLAYING
        self.time_elapsed = 0
        self.input = None, None

    def __start_entities(self):
        for e in self.entities:
            e.start(self)

    def __reset_default_rewards(self):
        max_distance = self.level_width + self.level_height - 2
        pos_x, pos_y = self.get_entity_by_type(Treasure).position

        self.default_rewards = np.zeros((self.level_width, self.level_height))
        for x in range(0, self.level_width):
            for y in range(0, self.level_height):
                self.default_rewards[x][y] = 1 - (abs(x - pos_x) + abs(y - pos_y)) / max_distance

    def __get_current_default_reward(self):
        actor_position = self.get_actor_entity().position
        return self.default_rewards[(*actor_position,)]

    def get_actor_entity(self):
        return self.get_entity_by_type(Actor)

    def get_entity_by_type(self, etype):
        """Find an entity by its type."""
        for e in self.entities:
            if isinstance(e, etype):
                return e

        return None

    def get_entity_by_position(self, position):
        """Find an entity by its position."""
        for e in self.entities:
            if e.position == position:
                return e

        return None

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def get_matrix_representation(self):
        matrix = np.zeros((self.level_width, self.level_height))

        for e in self.entities:
            matrix[(*e.position,)] = e.REPRESENTATION / Entity.ENTITY_TYPE_COUNT
        matrix[(*self.get_actor_entity().position,)] = 1  # Reset actor's representation in case of overlapping

        matrix = np.pad(matrix, ((2, 2), (2, 2)), 'constant', constant_values=((0.25, 0.25), (0.25, 0.25)))
        return matrix

    def get_text_representation(self):
        return "TO BE IMP"  # TODO: Implement text rep

