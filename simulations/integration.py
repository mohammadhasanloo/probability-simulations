"""Estimating an integral by averaging the integrand at random points.

The quarter circle is the example because its answer is known exactly: the
integral of sqrt(1 - x^2) from 0 to 1 is pi/4, so the estimate can be scored
rather than merely reported.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

TRUE_VALUE = math.pi / 4


@dataclass(frozen=True)
class Estimate:
    """One run: the mean of the integrand, its spread, and how far off it was."""

    samples: int
    mean: float
    variance: float

    @property
    def error(self) -> float:
        return abs(self.mean - TRUE_VALUE)

    @property
    def standard_error(self) -> float:
        """The spread the estimate itself should have, from this run's variance."""
        return math.sqrt(self.variance / self.samples)

    def format(self) -> str:
        return (
            f"{self.samples:>8,} samples  mean {self.mean:.5f}  "
            f"variance {self.variance:.5f}  error {self.error:.5f}  "
            f"predicted {self.standard_error:.5f}"
        )


def integrand(x: np.ndarray) -> np.ndarray:
    return np.sqrt(1 - x**2)


def estimate(samples: int, seed: int = 0) -> Estimate:
    values = integrand(np.random.default_rng(seed).random(samples))
    return Estimate(samples, float(values.mean()), float(values.var()))


def convergence(sizes, seed: int = 0) -> list[Estimate]:
    return [estimate(int(n), seed=seed + i) for i, n in enumerate(sizes)]
