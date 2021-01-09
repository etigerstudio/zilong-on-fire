from envs.base import BaseEnvironment
from envs.rpg.world import World
from envs.rpg.levels.teasure_tutorial import TreasureTutorial
from envs.rpg.entities.actor import Actor
from enum import Enum
import numpy as np


class RPGEnvironment(BaseEnvironment):
    STATE_PADDING = 2

    class Action(Enum):
        """动作枚举"""
        # IDLE = 0

        LEFTWARD_WALK = 0
        FORWARD_WALK = 1
        RIGHTWARD_WALK = 2
        BACKWARD_WALK = 3

        LEFTWARD_JUMP = 4
        FORWARD_JUMP = 5
        RIGHTWARD_JUMP = 6
        BACKWARD_JUMP = 7

        LEFTWARD_SLASH = 8
        FORWARD_SLASH = 9
        RIGHTWARD_SLASH = 10
        BACKWARD_SLASH = 11

        # CROUCH = 12

    ACTIONS = [
        # Action.IDLE,
        Action.LEFTWARD_WALK,
        Action.FORWARD_WALK,
        Action.RIGHTWARD_WALK,
        Action.BACKWARD_WALK,
        Action.LEFTWARD_JUMP,
        Action.FORWARD_JUMP,
        Action.RIGHTWARD_JUMP,
        Action.BACKWARD_JUMP,
        Action.LEFTWARD_SLASH,
        Action.FORWARD_SLASH,
        Action.RIGHTWARD_SLASH,
        Action.BACKWARD_SLASH,
        # Action.CROUCH
    ]

    __ACTION_MAPPINGS = {
        # Action.IDLE: (Actor.Movement.IDLE, Actor.Spell.IDLE),
        Action.LEFTWARD_WALK: (Actor.Movement.LEFTWARD, Actor.Spell.IDLE),
        Action.FORWARD_WALK: (Actor.Movement.FORWARD, Actor.Spell.IDLE),
        Action.RIGHTWARD_WALK: (Actor.Movement.RIGHTWARD, Actor.Spell.IDLE),
        Action.BACKWARD_WALK: (Actor.Movement.BACKWARD, Actor.Spell.IDLE),
        Action.LEFTWARD_JUMP: (Actor.Movement.LEFTWARD, Actor.Spell.JUMP),
        Action.FORWARD_JUMP: (Actor.Movement.FORWARD, Actor.Spell.JUMP),
        Action.RIGHTWARD_JUMP: (Actor.Movement.RIGHTWARD, Actor.Spell.JUMP),
        Action.BACKWARD_JUMP: (Actor.Movement.BACKWARD, Actor.Spell.JUMP),
        Action.LEFTWARD_SLASH: (Actor.Movement.LEFTWARD, Actor.Spell.SLASH),
        Action.FORWARD_SLASH: (Actor.Movement.FORWARD, Actor.Spell.SLASH),
        Action.RIGHTWARD_SLASH: (Actor.Movement.RIGHTWARD, Actor.Spell.SLASH),
        Action.BACKWARD_SLASH: (Actor.Movement.BACKWARD, Actor.Spell.SLASH),
        # Action.CROUCH: (Actor.Movement.CROUCH, Actor.Spell.IDLE)
    }

    def __init__(self,
                 level,
                 return_t_in_states=False,):
        self.world = World(level)
        self.return_t_in_states = return_t_in_states

    def step(self, action):
        game_over, reward = self.world.step(*RPGEnvironment.__ACTION_MAPPINGS[action])
        if self.return_t_in_states:
            return (np.array(self.world.get_matrix_representation()),
                    (self.world.time_elapsed, self.world.time_limit)), \
                   reward, game_over
        else:
            return np.array(self.world.get_matrix_representation()), \
                   reward, game_over

    def reset(self):
        self.world.reset()
        if self.return_t_in_states:
            return np.array(self.world.get_matrix_representation()), (self.world.time_elapsed, self.world.time_limit)
        else:
            return np.array(self.world.get_matrix_representation())

    def get_state_shape(self):
        return self.world.level_width + self.STATE_PADDING * 2,\
               self.world.level_height + self.STATE_PADDING * 2
