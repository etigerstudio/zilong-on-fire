# Basic environment implementation


class BasicEnvironment:
    def __init__(self, partitions=8):
        self.partitions = partitions
        self.actor_facing = 0
        self.arrow_direction = 0

    def reward(self):
        return (self.arrow_direction - self.actor_facing) % self.partitions

    def step(self, action):
        if action == 'LEFT':
            self.actor_facing = (self.actor_facing - 1) % self.partitions
        elif action == 'RIGHT':
            self.actor_facing = (self.actor_facing + 1) % self.partitions
        else:
            pass  # Take no action

        return self.reward()