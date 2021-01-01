class Level:
    @staticmethod
    def init():
        """Initialize this level.

        Returns:
            level_width: The width of the level.
            level_height: The height of the level.
            entities: All entities. The Actor entity must be place at index 0.

        """
        raise NotImplementedError
