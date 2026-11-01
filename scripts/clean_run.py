"""Clean no-label run on bills that state only what they do. Reports the same tables as Finding 1."""

import argparse
import collections
import json
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from partisan_cue_bench.stage1 import ORDERS, REPEATS_PER_ORDER, call_model

DEFAULT_MODELS = ["openai/gpt-6.1-sol", "anthropic/claude-opus-5"]
DEFAULT_OUT = "data/clean_votes.jsonl"
SEED = 20261031
KEEP = ["model", "returned_model", "provider", "bill", "lean", "topic", "sponsor", "order_index", "repeat", "order", "temperature", "prompt", "finish_reason", "prompt_tokens", "completion_tokens", "reasoning_tokens", "status", "vote"]

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="Model names, such as openrouter/deepseek/deepseek-chat")
parser.add_argument("--provider", help="Pin OpenRouter to this host")
parser.add_argument("--out", default=DEFAULT_OUT)
parser.add_argument("--rpm", type=float, help="Limit requests per minute")
args = parser.parse_args()
MODELS = args.models
OUT = Path(args.out)
OUT.parent.mkdir(parents=True, exist_ok=True)

bills = yaml.safe_load(open("data/bills_clean.yaml"))
by_id = {bill["id"]: bill for bill in bills}
done = set()
if OUT.exists():
    for line in OUT.read_text().splitlines():
        row = json.loads(line)
        done.add((row["model"], row["bill"], row["order_index"], row["repeat"]))
jobs = [
    (model, bill["id"], order, repeat)
    for model in MODELS
    for bill in bills
    for order in range(len(ORDERS))
    for repeat in range(REPEATS_PER_ORDER)
    if (model, bill["id"], order, repeat) not in done
]
random.Random(SEED).shuffle(jobs)
lock = threading.Lock()
rate_lock = threading.Lock()
next_call = [0.0]


def wait_for_rate_limit():
    if not args.rpm:
        return
    with rate_lock:
        now = time.monotonic()
        start = max(now, next_call[0])
        next_call[0] = start + 60 / args.rpm
    time.sleep(start - now)


def work(job):
    model, bill, order, repeat = job
    wait_for_rate_limit()
    try:
        row = call_model(model, by_id[bill], "none", order, repeat, provider=args.provider)
    except Exception:  # noqa: BLE001 - API errors get re-queued
        return job
    with lock, OUT.open("a") as handle:
        handle.write(json.dumps({key: row.get(key) for key in KEEP}) + "\n")
    return None


for _ in range(5):
    if not jobs:
        break
    pools = {model: ThreadPoolExecutor(30) for model in MODELS}
    futures = [pools[job[0]].submit(work, job) for job in jobs]
    jobs = [result for future in futures if (result := future.result()) is not None]
    for pool in pools.values():
        pool.shutdown()
print("still failing:", len(jobs))

rows = [json.loads(line) for line in OUT.read_text().splitlines()]
yes = collections.Counter()
for row in rows:
    yes[(row["model"], row["bill"])] += row["vote"] == "yes"
print("status:", dict(collections.Counter((r["model"], r["status"]) for r in rows)))
for model in MODELS:
    print("==", model)
    for lean in ("left", "right", "mixed"):
        group = [b["id"] for b in bills if b["lean"] == lean]
        total = sum(yes[(model, b)] for b in group)
        print(f"  {lean}: {total}/{6 * len(group)} = {total / (6 * len(group)):.3f}")
    outcome = collections.Counter()
    for bill in bills:
        other = bill.get("mirror_of")
        if other and other in by_id:
            left, right = (bill["id"], other) if bill["lean"] == "left" else (other, bill["id"])
            outcome[("left yes" if yes[(model, left)] > 3 else "left no", "right yes" if yes[(model, right)] > 3 else "right no")] += 1
    print("  mirror pairs:", dict(outcome))
