#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace

import ray  # type: ignore
from ray.rllib.agents import ppo  # type: ignore
from gym.spaces import Discrete, Box  # type: ignore

from dataphilly import GuessingGame, RockPaperScissors


games = {
    "g": GuessingGame,
    "rps": RockPaperScissors
}


def arguments() -> ArgumentParser:
    parser = ArgumentParser(description="Learn to play games with ray.")
    parser.add_argument(
        "--game",
        help="g for guessinggame, rps for rockpaperscissors",
        type=str,
        default="g"
    )
    parser.add_argument(
        "--n",
        help="if game==g then n is observation/action size, if game==rps then n-1 is number of agents.",
        type=int,
        default="2"
    )

    def validate_args(arguments: Namespace) -> Namespace:
        """The proper way to do this is to use the callable validator design pattern.

        here https://youtu.be/S_ipdVNSFlo?t=2153

        For valditor v put `type=v` in `.add_argument`
        """
        assert arguments.game in games.keys(), "--game argument wrong."
        if arguments.game == "rps":
            assert arguments.n >= 3, "--n must be >= 3 for rps."
        assert arguments.n >=  2, "--n must be >= 2."
        return arguments
        
    return validate_args(parser.parse_args())

def multiagent_config(n: int) -> dict:
    rps_player = (
        None,
        Box(
            -1,
            1,
            (n - 1,),
            int
        ),  # observations
        Discrete(n),  # actions
        {}
    )
    return {
        "multiagent": {
            "policies": {"rps_player": rps_player},
            "policy_mapping_fn": lambda agent_id, episode: "rps_player"
        },
        "model": {
            "dim": 3,
            "conv_filters": [
                [16, [4, 4], 1],
                [32, [n - 1], 1]
            ]
        }
    }

if __name__ == "__main__":
    args = arguments()

    env_config = {"length": 1000, "n": args.n}

    run_config = {
        "env_config": env_config,
        "framework": "torch",
    }
    if args.game == "rps":
        run_config = {**run_config, **multiagent_config(args.n)}

    ray.init()
    trainer = ppo.PPOTrainer(
        env=games[args.game],
        config=run_config
    )

    while True:
        print(trainer.train())
