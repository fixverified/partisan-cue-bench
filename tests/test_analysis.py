"""Run the analysis on simulated data with known effects, so it's checked before real data."""

import json
import random
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "analyze_stage1.py"
MODELS = ["model/a", "model/b"]
ARMS = ["none", "placebo", "placebo_region", "democrat", "republican"]


def simulate(path, probability, bills=100, seed=1):
    rng = random.Random(seed)
    with open(path, "w") as handle:
        for model in MODELS:
            for index in range(bills):
                base = rng.random()
                lean = ["left", "right", "mixed"][index % 3]
                for arm in ARMS:
                    for repeat in range(6):
                        vote = "yes" if rng.random() < probability(base, arm, lean) else "no"
                        handle.write(
                            json.dumps(
                                {
                                    "model": model,
                                    "returned_model": model,
                                    "bill": f"b{index}",
                                    "lean": lean,
                                    "sponsor": arm,
                                    "order": ["yes", "no"] if repeat % 2 else ["no", "yes"],
                                    "status": "valid",
                                    "vote": vote,
                                    "prompt_tokens": 1,
                                    "completion_tokens": 1,
                                }
                            )
                            + "\n"
                        )


def analyze(path):
    return subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, check=True).stdout


def primary(output):
    lines = output.split("PRIMARY, Holm across models:")[1].split("SECONDARY")[0].strip().splitlines()
    return [line.split("->")[1].strip() for line in lines]


def test_planted_democrat_lean_is_detected(tmp_path):
    path = tmp_path / "planted.jsonl"
    simulate(path, lambda base, arm, lean: min(1, base + 0.15) if arm == "democrat" else base)
    assert primary(analyze(path)) == ["lean", "lean"]


def test_no_effect_is_not_called_a_lean(tmp_path):
    path = tmp_path / "null.jsonl"
    simulate(path, lambda base, arm, lean: base)
    assert "lean" not in primary(analyze(path))


def test_planted_same_party_effect_shows_in_secondary(tmp_path):
    path = tmp_path / "same_party.jsonl"

    def probability(base, arm, lean):
        match = (lean == "left" and arm == "democrat") or (lean == "right" and arm == "republican")
        return min(1, base + 0.2) if match else base

    simulate(path, probability)
    lines = [line for line in analyze(path).splitlines() if "same-party" in line]
    assert len(lines) == 2
    assert all(float(line.split("adjusted p=")[1]) < 0.05 for line in lines)


def test_analysis_counts_invalid_as_not_yes_and_keeps_going(tmp_path):
    path = tmp_path / "invalid.jsonl"
    simulate(path, lambda base, arm, lean: 1.0, bills=3)
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    rows[0].update(status="malformed", vote=None)
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    assert "malformed" in analyze(path)
