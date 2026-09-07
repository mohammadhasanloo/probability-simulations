"""Run the three simulations and write their numbers and figures."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from . import figures, integration, monty_hall, st_petersburg

SIZES = (10, 100, 1_000, 10_000, 100_000, 1_000_000)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=Path("results/simulations.json"))
    parser.add_argument("--docs", type=Path, default=Path("docs"))
    arguments = parser.parse_args(argv)

    print("Monty Hall")
    doors = {s: monty_hall.convergence(s, SIZES) for s in ("stay", "switch", "coin")}
    for runs in doors.values():
        print("  " + runs[-1].format())
    figures.monty_hall(doors, arguments.docs / "monty_hall.png")

    print("\nQuarter circle by Monte Carlo")
    estimates = integration.convergence(SIZES)
    for estimate in estimates:
        print("  " + estimate.format())
    figures.integration(estimates, arguments.docs / "integration.png")

    print("\nSt Petersburg")
    rounds = st_petersburg.convergence(SIZES)
    for round_ in rounds:
        print("  " + round_.format())
    figures.st_petersburg(rounds, arguments.docs / "st_petersburg.png")

    arguments.results.parent.mkdir(parents=True, exist_ok=True)
    arguments.results.write_text(
        json.dumps(
            {
                "monty_hall": {s: [_row(r) for r in runs] for s, runs in doors.items()},
                "integration": [_row(e) for e in estimates],
                "st_petersburg": [asdict(r) for r in rounds],
            },
            indent=2,
        )
        + "\n"
    )
    return 0


def _row(item) -> dict:
    row = asdict(item)
    for name in ("rate", "error", "standard_error"):
        if hasattr(item, name):
            row[name] = getattr(item, name)
    return row


if __name__ == "__main__":
    raise SystemExit(main())
