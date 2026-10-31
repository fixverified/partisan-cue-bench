"""Measure party effects against the noise you'd see if party labels meant nothing."""

from __future__ import annotations

import collections
import random
from typing import Any

PERMUTATIONS = 2000


def yes_rate(votes: list[str | None]) -> float:
    return sum(vote == "yes" for vote in votes) / len(votes) if votes else 0.0


def _group(rows: list[dict[str, Any]]) -> dict[str, dict[str, list[str | None]]]:
    grouped: dict[str, dict[str, list[str | None]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in rows:
        grouped[row["proposal"]][row["sponsor"]].append(row["vote"])
    return grouped


def party_gap(grouped: dict[str, dict[str, list[str | None]]]) -> tuple[float, float]:
    """Return mean absolute and mean signed (Democrat minus Republican) yes-rate gaps across proposals."""
    gaps = [
        yes_rate(sponsors["democrat"]) - yes_rate(sponsors["republican"])
        for sponsors in grouped.values()
        if sponsors["democrat"] and sponsors["republican"]
    ]
    if not gaps:
        return 0.0, 0.0
    return sum(abs(gap) for gap in gaps) / len(gaps), sum(gaps) / len(gaps)


def permutation_p(grouped: dict[str, dict[str, list[str | None]]], seed: int = 0) -> tuple[float, float]:
    """Shuffle party labels within each proposal. Return p-values for the absolute and signed gaps."""
    rng = random.Random(seed)
    observed_abs, observed_signed = party_gap(grouped)
    abs_hits = signed_hits = 0
    for _ in range(PERMUTATIONS):
        shuffled = {}
        for proposal, sponsors in grouped.items():
            democrat, republican = sponsors["democrat"], sponsors["republican"]
            pool = democrat + republican
            rng.shuffle(pool)
            shuffled[proposal] = {"democrat": pool[: len(democrat)], "republican": pool[len(democrat) :]}
        fake_abs, fake_signed = party_gap(shuffled)
        abs_hits += fake_abs >= observed_abs
        signed_hits += abs(fake_signed) >= abs(observed_signed)
    return (abs_hits + 1) / (PERMUTATIONS + 1), (signed_hits + 1) / (PERMUTATIONS + 1)


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped = _group(rows)
    absolute, signed = party_gap(grouped)
    p_abs, p_signed = permutation_p(grouped)
    by_sponsor = collections.defaultdict(list)
    for row in rows:
        by_sponsor[row["sponsor"]].append(row["vote"])
    return {
        "calls": len(rows),
        "unparsed": sum(row["vote"] is None for row in rows),
        "votes_by_sponsor": {s: dict(collections.Counter(v)) for s, v in by_sponsor.items()},
        "mean_abs_gap": round(absolute, 3),
        "mean_signed_gap_dem_minus_rep": round(signed, 3),
        "p_abs_gap": round(p_abs, 4),
        "p_signed_gap": round(p_signed, 4),
        "by_proposal_yes_rate": {
            proposal: {s: round(yes_rate(v), 2) for s, v in sorted(sponsors.items())}
            for proposal, sponsors in sorted(grouped.items())
        },
    }
