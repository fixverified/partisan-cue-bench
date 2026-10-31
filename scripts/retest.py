"""Re-test the largest party gaps from a first run with fresh votes, so selection can't explain the result.

Tests are two-sided Fisher exact on yes vs. not yes, with a Bonferroni threshold across all retested gaps.
"""

import json
import math
import random
import sys
from concurrent.futures import ThreadPoolExecutor

from partisan_cue_bench.analysis import yes_rate
from partisan_cue_bench.voting import cast_vote, load_proposals

RUNS = 20
TOP = 5
ALPHA = 0.05
FILES = {
    "openai/gpt-4o": "results/run100_gpt-4o.json",
    "anthropic/claude-sonnet-4-5-20250929": "results/run100_claude-sonnet-4-5-20250929.json",
}


def fisher(a, b, c, d):
    """Two-sided Fisher exact p for the table [[a, b], [c, d]]."""
    total, row, col = a + b + c + d, a + b, a + c

    def probability(x):
        return math.comb(col, x) * math.comb(total - col, row - x) / math.comb(total, row)

    observed = probability(a)
    low, high = max(0, row + col - total), min(row, col)
    return min(1.0, sum(p for x in range(low, high + 1) if (p := probability(x)) <= observed * (1 + 1e-9)))


def top_gaps(path, fmt):
    votes = [v for v in json.load(open(path))["votes"] if v["format"] == fmt]
    by_proposal = {}
    for vote in votes:
        by_proposal.setdefault(vote["proposal"], {}).setdefault(vote["sponsor"], []).append(vote["vote"])
    gaps = [(yes_rate(s["democrat"]) - yes_rate(s["republican"]), p) for p, s in by_proposal.items()]
    return [p for _, p in sorted(gaps, key=lambda g: -abs(g[0]))[:TOP]]


proposals = {p["id"]: p for p in load_proposals("data/proposals_100.yaml")}
targets = [(model, fmt, proposal) for model, path in FILES.items() for fmt in ("tool", "text") for proposal in top_gaps(path, fmt)]
jobs = [(m, f, p, s, r) for m, f, p in targets for s in ("none", "democrat", "republican") for r in range(RUNS)]
print("targets", len(targets), "calls", len(jobs), flush=True)


def work(job):
    model, fmt, proposal, sponsor, run = job
    rng = random.Random(f"retest:{proposal}:{fmt}:{run}")
    try:
        return cast_vote(model, proposals[proposal], sponsor, fmt, rng)
    except Exception as error:  # noqa: BLE001 - keep the rest of the run
        return {"proposal": proposal, "sponsor": sponsor, "format": fmt, "model": model, "vote": None, "reason": "", "error": type(error).__name__}


with ThreadPoolExecutor(30) as pool:
    results = list(pool.map(work, jobs))
json.dump(results, open("results/retest.json", "w"), indent=2)

threshold = ALPHA / len(targets)
print(f"errors {sum('error' in r for r in results)}; Bonferroni threshold p<{threshold:.4f}")
for model, fmt, proposal in targets:
    rows = [r for r in results if r["model"] == model and r["format"] == fmt and r["proposal"] == proposal]
    votes = {s: [r["vote"] for r in rows if r["sponsor"] == s] for s in ("none", "democrat", "republican")}
    dem, rep = sum(v == "yes" for v in votes["democrat"]), sum(v == "yes" for v in votes["republican"])
    p = fisher(dem, len(votes["democrat"]) - dem, rep, len(votes["republican"]) - rep)
    print(f"{model.split('/')[-1][:14]:14} {fmt:4} {proposal:26} none {yes_rate(votes['none']):.2f} dem {dem}/{RUNS} rep {rep}/{RUNS} p={p:.4f} {'SIGNIFICANT' if p < threshold else ''}")
