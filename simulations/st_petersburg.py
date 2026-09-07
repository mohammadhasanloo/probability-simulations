"""A game worth infinity that nobody would pay much to play.

A coin is tossed until it comes up tails. A run of k heads pays 2^k. The
expected payout is the sum over k of (1/2)^k times 2^k, which is one for every
k and so does not converge: the game's expectation is infinite.

The point of simulating it is that the sample mean never settles. It grows
about like log2 of the number of games played, so any figure quoted as "the
average payout" is really a statement about how long the run was.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Round:
    """What a run of games paid, and what its length predicts it should pay."""

    games: int
    mean_payout: float
    largest_payout: int
    predicted: float

    def format(self) -> str:
        return (
            f"{self.games:>9,} games  mean payout {self.mean_payout:>9.2f}  "
            f"largest {self.largest_payout:>12,}  "
            f"log2(n)/2 + 1 = {self.predicted:.2f}"
        )


def payouts(games: int, seed: int = 0) -> np.ndarray:
    """The payout of each game.

    The number of heads before the first tail is geometric, so it is drawn
    directly rather than by tossing a coin in a loop, which would spend most of
    its time on the runs that pay least.
    """
    heads = np.random.default_rng(seed).geometric(0.5, games) - 1
    return np.power(2.0, heads)


def play(games: int, seed: int = 0) -> Round:
    values = payouts(games, seed=seed)
    return Round(
        games=games,
        mean_payout=float(values.mean()),
        largest_payout=int(values.max()),
        predicted=math.log2(games) / 2 + 1,
    )


def convergence(sizes, seed: int = 0) -> list[Round]:
    return [play(int(n), seed=seed + i) for i, n in enumerate(sizes)]
