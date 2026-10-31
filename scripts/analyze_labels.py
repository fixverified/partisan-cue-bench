"""Analyze party-label votes. Valid votes only, exact integer counts, and a check that every cell is complete."""

import collections
import json
import random
import sys

MODELS = sys.argv[1:] or ["openai/gpt-6.1-sol", "anthropic/claude-opus-5"]
ARMS = ["none", "placebo", "placebo_region", "democrat", "republican"]
VOTES_PER_CELL = 4
DRAWS = 100_000
SEED = 20261031

rows = [json.loads(line) for line in open("data/label_votes.jsonl")]
# The baseline uses the first 2 repeats per order from the clean no-label run, matching the 4 votes per label.
rows += [row for row in map(json.loads, open("data/clean_votes.jsonl")) if row["repeat"] < 2]

cell = collections.defaultdict(list)
lean = {}
for row in rows:
    cell[(row["model"], row["bill"], row["sponsor"])].append(row)
    lean[row["bill"]] = row["lean"]
bills = sorted(lean)
missing = [key for key in ((m, b, a) for m in MODELS for b in bills for a in ARMS) if len(cell[key]) != VOTES_PER_CELL]
assert not missing, f"incomplete cells: {missing[:5]}"
print(f"bills {len(bills)}, rows {len(rows)}, status {dict(collections.Counter(r['status'] for r in rows))}")


def yes(model, bill, arm):
    return sum(row["vote"] == "yes" for row in cell[(model, bill, arm)])


def sign_flip(values, rng):
    observed = abs(sum(values))
    moving = [value for value in values if value]
    if not moving:
        return 1.0
    hits = sum(abs(sum(v if rng.random() < 0.5 else -v for v in moving)) >= observed for _ in range(DRAWS))
    return (hits + 1) / (DRAWS + 1)


def summary(values, rng, label):
    moved = [value for value in values if value]
    mean = sum(values) / (len(values) * VOTES_PER_CELL)
    print(f"  {label}: mean {mean:+.3f}; moved {len(moved)}/{len(values)} (+{sum(v > 0 for v in moved)} / -{sum(v < 0 for v in moved)}); p={sign_flip(values, rng):.4f}")


for model in MODELS:
    rng = random.Random(SEED)
    print(f"\n===== {model}")
    for arm in ARMS:
        total = sum(yes(model, bill, arm) for bill in bills)
        by_lean = {side: round(sum(yes(model, b, arm) for b in bills if lean[b] == side) / (VOTES_PER_CELL * sum(lean[b] == side for b in bills)), 3) for side in ("left", "right", "mixed")}
        print(f"  {arm}: yes {total}/{VOTES_PER_CELL * len(bills)} = {total / (VOTES_PER_CELL * len(bills)):.3f} {by_lean}")
    gaps = {bill: yes(model, bill, "democrat") - yes(model, bill, "republican") for bill in bills}
    summary(list(gaps.values()), rng, "D minus R, all bills")
    for side in ("left", "right", "mixed"):
        summary([gaps[b] for b in bills if lean[b] == side], rng, f"D minus R, {side}")
    same = [gaps[b] if lean[b] == "left" else -gaps[b] for b in bills if lean[b] in ("left", "right")]
    summary(same, rng, "same-party minus cross-party")
    summary([yes(model, b, "placebo") - yes(model, b, "none") for b in bills], rng, "first-term minus none")
    summary([yes(model, b, "placebo_region") - yes(model, b, "none") for b in bills], rng, "Midwest minus none")
    summary([yes(model, b, "placebo") - yes(model, b, "placebo_region") for b in bills], rng, "first-term minus Midwest")
    summary([yes(model, b, "democrat") - yes(model, b, "none") for b in bills], rng, "D minus none")
    summary([yes(model, b, "republican") - yes(model, b, "none") for b in bills], rng, "R minus none")
    print("  mean |D-R|", round(sum(abs(v) for v in gaps.values()) / (len(bills) * VOTES_PER_CELL), 3), "| mean |first-term - Midwest|", round(sum(abs(yes(model, b, "placebo") - yes(model, b, "placebo_region")) for b in bills) / (len(bills) * VOTES_PER_CELL), 3))
    print("  largest D-R gaps (lean: none, first-term, Midwest, D, R):")
    for bill in sorted(bills, key=lambda b: (-abs(gaps[b]), b))[:14]:
        print(f"    {bill} [{lean[bill]}]: {tuple(yes(model, bill, arm) for arm in ARMS)}")
