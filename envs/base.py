# Base environment implementation


class BaseEnvironment:
    def step(self, action):
        """Perform one timestep.

        Args:
            action: action to be performed.

        Returns:
            new_state: The new environment state.
            reward: The reward for the action.
            dead: Whether the actor has died or not.
        """
        raise NotImplementedError

    def reset(self):
        """Reset the environment.
        """
        raise NotImplementedError
