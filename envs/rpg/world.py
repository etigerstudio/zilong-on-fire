from enum import Enum


class World:
    BLANK_SPACE_VALUE = 0
    TIME_LIMIT = 10
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
                 time_limit=TIME_LIMIT,
                 alive_reward=ACTOR_ALIVE_REWARD,
                 dead_reward=ACTOR_DEAD_REWARD,
                 timestep_expiration_reward=TIMESTEP_EXPIRATION_REWARD):
        self.level_stub = level
        self.time_limit = time_limit
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

        game_over, reward = False, 0
        for e in self.entities:  # TODO: Ensure actor is updated first.
            r = e.update(self)
            if r is not None:
                reward += r
        if reward == 0:
            reward = World.ACTOR_ALIVE_REWARD

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
        self.entities = self.level_stub.init()
        self.__start_entities()
        self.status = self.Status.PLAYING
        self.time_elapsed = 0
        self.input = None, None

    def __start_entities(self):
        for e in self.entities:
            e.start(self)

    def get_actor_entity(self):
        return self.entities[0]  # TODO: More robust logic

    def get_entity_by_position(self, position):
        """Find an entity by its position."""
        for e in self.entities:
            if e.position == position:
                return e

        return None

    def get_matrix_representation(self):
        matrix = []
        for i in range(0, self.level_height):
            matrix.append([0] * self.level_width)

        for e in self.entities:
            matrix[e.position[0]][e.position[1]] = e.REPRESENTATION

        return matrix

    def get_text_representation(self):
        return "TO BE IMP"  # TODO: Implement text rep

