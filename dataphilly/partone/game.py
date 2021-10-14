from typing import Tuple

import gym  # type: ignore
from gym.spaces import Discrete  # type: ignore


class GuessingGame(gym.Env):
    def __init__(self, env_config):
        self.length = self.remaining_rounds = env_config["length"]
        self.n = env_config["n"]
        self.observation_space = Discrete(self.n)
        self.action_space = Discrete(self.n)
        self.previous_obs = None

    def reset(self) -> int:
        self.remaining_rounds = self.length
        self.previous_obs = self.observation_space.sample()
        return self.observation_space.sample()

    def step(self, action: int) -> Tuple[int, float, bool, dict]:
        self.previous_obs = self.observation_space.sample()

        self.remaining_rounds -= 1

        return (
            self.observation_space.sample(),
            float(action == self.previous_obs),
            self.remaining_rounds <= 0,
            {}
        )
