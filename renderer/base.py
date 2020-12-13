# Base renderer class declaration

class BaseRenderer:
    def setup(self, info=None):
        raise NotImplementedError

    def update(self, state, info=None):
        raise NotImplementedError

    def close(self, info=None):
        raise NotImplementedError