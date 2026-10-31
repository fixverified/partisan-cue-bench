"""Run votes and summarize them."""

from __future__ import annotations

import argparse
import json
import random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .analysis import summarize
from .voting import SPONSORS, ask_self_report, cast_vote, load_proposals


def main() -> None:
    parser = argparse.ArgumentParser(prog="vote-bench")
    parser.add_argument("--model", required=True, help="litellm model name")
    parser.add_argument("--proposals", default="data/proposals.yaml")
    parser.add_argument("--runs", type=int, default=5, help="Votes per proposal, sponsor and format")
    parser.add_argument("--formats", default="tool,text")
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=20261031)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    proposals = load_proposals(args.proposals)
    formats = args.formats.split(",")
    jobs = [(p, s, f, run) for p in proposals for s in SPONSORS for f in formats for run in range(args.runs)]

    def work(job):
        proposal, sponsor, fmt, run = job
        # The same run number gets the same option order across sponsors, so order can't explain a gap.
        rng = random.Random(f"{args.seed}:{proposal['id']}:{fmt}:{run}")
        try:
            return cast_vote(args.model, proposal, sponsor, fmt, rng)
        except Exception as error:  # noqa: BLE001 - one failed call shouldn't lose a long run
            return {"proposal": proposal["id"], "lean": proposal["lean"], "sponsor": sponsor, "format": fmt, "model": args.model, "options": [], "vote": None, "reason": "", "error": type(error).__name__}

    def report(proposal):
        try:
            return ask_self_report(args.model, proposal)
        except Exception as error:  # noqa: BLE001
            return {"proposal": proposal["id"], "model": args.model, "says_party_matters": None, "text": "", "error": type(error).__name__}

    with ThreadPoolExecutor(args.workers) as pool:
        votes = list(pool.map(work, jobs))
        reports = list(pool.map(report, proposals))

    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"votes": votes, "self_reports": reports}, indent=2))

    output = {"model": args.model, "by_format": {}}
    for fmt in formats:
        output["by_format"][fmt] = summarize([v for v in votes if v["format"] == fmt])
    output["says_party_matters"] = {
        answer: sum(r["says_party_matters"] == answer for r in reports) for answer in ("yes", "no", None)
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
