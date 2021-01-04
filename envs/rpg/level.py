class Level:
    @staticmethod
    def init():
        """Initialize this level.

        Returns:
            level_width: The width of the level.
            level_height: The height of the level.
            time_limit: The timestep limit of the level.
            entities: All entities. The Actor entity must be place at index 0.

        """
        raise NotImplementedError

    @staticmethod
    def make_entities(begin_x, begin_y, end_x, end_y, etype):
        return [etype((begin_x + x, begin_y + y))
                     for x in range(end_x - begin_x + 1)
                    for y in range(end_y - begin_y + 1)]
