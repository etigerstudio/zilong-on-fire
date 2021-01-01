class Entity:
    REPRESENTATION = 0

    def __init__(self, position):
        """Initialize an entity with its position."""
        self.position = position

    def start(self, world):
        """Gets called once when added to a world."""
        raise NotImplementedError

    def update(self, world):
        """Gets called every timestep."""
        raise NotImplementedError

    def destroy(self, world):
        """Gets called after destroyed."""
        raise NotImplementedError
