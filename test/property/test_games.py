from dataphilly import GuessingGame, RockPaperScissors

from typing import List, Tuple, Union
from random import randint

from hypothesis import given
from hypothesis.strategies import integers


def guessing_game(n: int, length: int) -> GuessingGame:
    """Constructs guessing game in *args or **kwargs form."""
    return GuessingGame(
        {"n": n, "length": length}
    )


def rock_paper_scissors(n: int, length: int) -> RockPaperScissors:
    """Constructs rock paper scissors having destructed dict"""
    return RockPaperScissors(
        {"n": n, "length": length}
    )


def gg_agent(n: int) -> int:
    """Selects an action if the action space is gym.spaces.Discrete(n)"""
    return randint(0, n - 1)


def rps_agents(n: int) -> List[callable]:
    return [lambda: gg_agent(n) for _ in range(n - 1)]


gg = {
    "constructor": guessing_game,
    "agent": gg_agent
}

rps = {
    "constructor": rock_paper_scissors,
    "agent": rps_agents
}


def agent_(game_cfg: dict, num_moves: int) -> Tuple[Union[callable, dict], type, type, type]:
    _agent = game_cfg["agent"]
    if isinstance(_agent(2), int):
        return _agent, int, float, bool
    # else: isinstance(_agent(2), list)
    return lambda n: {f"agent{k}": _agent(num_moves)[k]() for k in range(num_moves - 1)}, dict, dict, dict


def meta_test_step_return(game_config: dict) -> callable:
    constructor = game_config["constructor"]

    @given(
        n=integers(min_value=2, max_value=25),
        length=integers(min_value=10, max_value=2**20)
    )
    def test_step_return(n: int, length: int):
        agent, obs_type, reward_type, done_type = agent_(game_config, n)
        game = constructor(n, length)
        for _ in range(10):
            step_item = game.step(agent(n))
            assert isinstance(step_item, tuple), "Step is not returning a tuple"
            assert len(step_item) == 4, f"Step is returning {len(step_item)} items."
            assert isinstance(step_item[0], obs_type), "Observation is wrong type."
            assert isinstance(step_item[1], reward_type), "Reward is wrong type."
            assert isinstance(step_item[2], done_type), "Done is wrong type."
            assert isinstance(step_item[3], dict), "Info is wrong type."

    return test_step_return


test_step_return_gg = meta_test_step_return(gg)
test_step_return_rps = meta_test_step_return(rps)


def meta_test_done(game_config: dict) -> callable:
    constructor = game_config["constructor"]

    @given(
        n=integers(min_value=2, max_value=25),
        length=integers(min_value=10, max_value=2**8)
    )
    def test_done(n: int, length: int):
        game = constructor(n, length)
        agent, _, _, _ = agent_(game_config, n)
        _ = game.reset()
        for step in range(length - 1):
            _, _, done, _ = game.step(agent(n))
            if isinstance(done, bool):
                assert not done, f"Game finished prematurely at step {step}."
            else:  # isinstance(done, dict)
                assert not all(done.values()), f"Game finished prematurely at step {step}."

        _, _, done, _ = game.step(agent(n))

        if isinstance(done, bool):
            assert done, "Game continued past it's intended time."
        else:  # isinstance(done, dict)
            assert all(done.values()), "Game continued past it's intended time."

    return test_done


test_done_gg = meta_test_done(gg)
test_done_rps = meta_test_done(rps)


@given(
    n=integers(min_value=2, max_value=1000),
    length=integers(min_value=10, max_value=2**20)
)
def test_obs_bounded_gg(n: int, length: int):
    game = guessing_game(n, length)
    assert 0 <= game.reset() <= n
    for _ in range(100):
        next_obs, _, done, _ = game.step(gg_agent(n))
        if done:
            game.reset()
        assert 0 <= next_obs <= n
