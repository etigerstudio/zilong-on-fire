from enum import Enum


class World:
    BLANK_SPACE_VALUE = 0

    class Status(Enum):
        PLAYING = 0
        WON = 1
        DEFEATED = 2

    def __init__(self, level):
        self.level_width, self.level_height, self.entities = level.init()
        self.status = self.Status.PLAYING
        self.time_elapsed = 0
        self.__start_entities()
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

    def step(self, actor_movement, actor_spell):
        self.input = actor_movement, actor_spell

        for e in self.entities:  # TODO: Ensure actor is updated first.
            e.update(self)

