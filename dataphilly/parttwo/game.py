from functools import partial
from collections import OrderedDict
from typing import Dict, Tuple

from numpy import ndarray, array  # type: ignore
import gym  # type: ignore
from gym.spaces import Discrete, Box  # type: ignore
from ray.rllib.env import MultiAgentEnv


class RockPaperScissors(MultiAgentEnv, gym.Env):
    class Item:
        """Atransitive comparators."""

        ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

        def __init__(self, modulus: int, k: int):
            assert modulus <= 25, "Not enough item letters"
            assert k <= modulus, "k out of range for given modulus"
            self.modulus = modulus
            self.k = k
            self.alphabet = self.ALPHABET[:modulus]
            self.letter = self.alphabet[k]
            self.letter_id = ord(self.letter) - 97

        def __lshift__(self, other) -> int:
            """returns the reward given to self."""
            assert self.modulus == other.modulus, "Types are not compatible"
            if self == other:
                return 0
            other_letter = self.alphabet[other.k]
            other_letter_id = ord(other_letter) - 97
            if (self.letter_id + 1) % self.modulus == other_letter_id:
                return -1
            if (self.letter_id - 1) % self.modulus == other_letter_id:
                return 1
            return 0

        def __repr__(self) -> str:
            return f"{self.letter} (mod {self.alphabet[-1]})"

    def __init__(self, env_config):
        self.length = self.remaining_rounds = env_config["length"]
        self.n = env_config["n"]
        self.items = partial(self.Item, modulus=self.n)  # Some atransitive comparator
        self.num_agents = self.n - 1
        self.observation_space = Box(-1, 1, (self.num_agents,), int)
        self.action_space = Discrete(self.n)
        self.previous_obs = None

    def reset(self) -> ndarray:
        self.remaining_rounds = self.length
        return {
            f"player{k}": array([0] * self.num_agents) for k in range(self.num_agents)
        }

    def step(
        self, actions_dict: Dict[str, int]
    ) -> Tuple[Dict[str, ndarray], Dict[str, float], Dict[str, bool], dict]:
        actions = OrderedDict(
            (agent_id, self.items(k=k)) for agent_id, k in actions_dict.items()
        )

        rewards = {
            agent_id: sum(
                actions[agent_id] << actions[other_agent_id]
                for other_agent_id in actions.keys()
            )
            for agent_id in actions.keys()
        }

        self.remaining_rounds -= 1

        isdone = self.remaining_rounds <= 0
        done = {agent_id: isdone for agent_id in actions_dict.keys()}
        done["__all__"] = isdone

        # each agents' observation is an array of the score it got in each position.
        # so other agents are ordered in a sense.
        observations = {
            agent_id: array(
                [actions[agent_id] << action for action in actions.values()]
            )
            for agent_id in actions.keys()
        }

        return (observations, rewards, done, {})
