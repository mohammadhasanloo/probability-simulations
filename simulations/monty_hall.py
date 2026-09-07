"""The three doors, and the three things a contestant can do about them."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

DOORS = 3


@dataclass(frozen=True)
class Outcome:
    """How often a strategy won, against the probability theory predicts."""

    strategy: str
    trials: int
    wins: int
    expected: float

    @property
    def rate(self) -> float:
        return self.wins / self.trials

    @property
    def error(self) -> float:
        return abs(self.rate - self.expected)

    def format(self) -> str:
        return (
            f"{self.strategy:<8} {self.trials:>7,} trials  won {self.rate:.4f}  "
            f"expected {self.expected:.4f}  off by {self.error:.4f}"
        )


EXPECTED = {"stay": 1 / 3, "switch": 2 / 3, "coin": 1 / 2}


def play(strategy: str, trials: int, seed: int = 0) -> Outcome:
    """Run one strategy for ``trials`` games.

    The host always opens a losing door, which is what makes switching win two
    thirds of the time: the contestant's first pick is right one time in three,
    and switching wins in exactly the other two.
    """
    generator = np.random.default_rng(seed)
    prize = generator.integers(0, DOORS, trials)
    chosen = generator.integers(0, DOORS, trials)
    first_pick_was_right = chosen == prize

    if strategy == "stay":
        won = first_pick_was_right
    elif strategy == "switch":
        won = ~first_pick_was_right
    elif strategy == "coin":
        switched = generator.integers(0, 2, trials).astype(bool)
        won = np.where(switched, ~first_pick_was_right, first_pick_was_right)
    else:
        raise ValueError(f"unknown strategy: {strategy}")

    return Outcome(strategy, trials, int(won.sum()), EXPECTED[strategy])


def convergence(strategy: str, sizes, seed: int = 0) -> list[Outcome]:
    return [play(strategy, int(n), seed=seed + i) for i, n in enumerate(sizes)]
