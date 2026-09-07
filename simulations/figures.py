"""Figures drawn from measured runs."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .integration import TRUE_VALUE  # noqa: E402

COLOURS = {"stay": "#d1495b", "switch": "#1f6feb", "coin": "#8a6d3b"}


def monty_hall(outcomes: dict[str, list], path: Path) -> Path:
    """Win rate against the number of games, with the exact answer drawn in."""
    figure, axis = plt.subplots(figsize=(8, 5))

    for strategy, runs in outcomes.items():
        colour = COLOURS[strategy]
        axis.plot([r.trials for r in runs], [r.rate for r in runs], "o-",
                  color=colour, lw=2, label=strategy)
        axis.axhline(runs[0].expected, color=colour, linestyle=":", lw=1.2)
        axis.text(runs[-1].trials * 1.5, runs[0].expected,
                  f"{runs[0].expected:.3f}", color=colour, fontsize=9, va="center")

    axis.set_xscale("log")
    axis.set_xlim(right=outcomes["stay"][-1].trials * 3)
    axis.set_ylim(0, 1)
    axis.set_xlabel("games played")
    axis.set_ylabel("share won")
    axis.set_title("Three doors, three strategies")
    axis.legend(loc="upper right")
    axis.grid(alpha=0.3)

    figure.tight_layout()
    return _save(figure, path)


def integration(estimates: list, path: Path) -> Path:
    """The estimate closing on pi/4, and its error against the 1/sqrt(n) rate."""
    figure, (value, error) = plt.subplots(1, 2, figsize=(12.5, 4.8))

    sizes = [e.samples for e in estimates]
    value.plot(sizes, [e.mean for e in estimates], "o-", color="#1f6feb", lw=2)
    value.axhline(TRUE_VALUE, color="#d1495b", linestyle="--", lw=1.4)
    value.text(sizes[0], TRUE_VALUE + 0.004, f"  pi/4 = {TRUE_VALUE:.5f}",
               color="#d1495b", fontsize=9)
    value.set_xscale("log")
    value.set_xlabel("samples")
    value.set_ylabel("estimate")
    value.set_title("Estimating the integral")
    value.grid(alpha=0.3)

    error.loglog(sizes, [e.error for e in estimates], "o-", color="#1f6feb",
                 lw=2, label="measured error")
    reference = [estimates[0].error * math.sqrt(sizes[0] / n) for n in sizes]
    error.loglog(sizes, reference, "--", color="#7f8c8d", lw=1.4,
                 label="1 / sqrt(n)")
    error.set_xlabel("samples")
    error.set_ylabel("distance from pi/4")
    error.set_title("Ten times the samples buys about three times the accuracy")
    error.legend()
    error.grid(alpha=0.3, which="both")

    figure.tight_layout()
    return _save(figure, path)


def st_petersburg(rounds: list, path: Path) -> Path:
    """The average payout that keeps climbing, against log2(n)/2 + 1."""
    figure, axis = plt.subplots(figsize=(8, 5))

    sizes = [r.games for r in rounds]
    axis.plot(sizes, [r.mean_payout for r in rounds], "o-", color="#1f6feb",
              lw=2, label="mean payout")
    axis.plot(sizes, [r.predicted for r in rounds], "--", color="#d1495b",
              lw=1.6, label="log2(n) / 2 + 1")

    axis.set_xscale("log")
    axis.set_xlabel("games played")
    axis.set_ylabel("mean payout")
    axis.set_title("An average that never settles")
    axis.legend()
    axis.grid(alpha=0.3)

    figure.tight_layout()
    return _save(figure, path)


def _save(figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=130)
    plt.close(figure)
    return path
