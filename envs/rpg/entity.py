class Entity:
    REPRESENTATION = 0
    ENTITY_TYPE_COUNT = 4  # Count of all entity types

    def __init__(self, position):
        """Initialize an entity with its position."""
        self.position = position
        self.representation = self.REPRESENTATION

    def start(self, world):
        """Gets called once when added to a world."""
        raise NotImplementedError

    def update(self, world):
        """Gets called every timestep.

            Returns:
                reward: The reward for current timestep.
                    None means 0 rewards.
        """
        raise NotImplementedError

    def destroy(self, world):
        """Gets called after destroyed."""
        raise NotImplementedError
