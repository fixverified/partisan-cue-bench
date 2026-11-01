"""Party-label run on the clean bills: Democrat, Republican and two placebo labels, 4 votes per bill and label."""

import argparse
import json
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from partisan_cue_bench.stage1 import ORDERS, call_model

DEFAULT_MODELS = ["openai/gpt-6.1-sol", "anthropic/claude-opus-5"]
ARMS = ["democrat", "republican", "placebo", "placebo_region"]
REPEATS_PER_ORDER = 2
DEFAULT_OUT = "data/label_votes.jsonl"
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
        done.add((row["model"], row["bill"], row["sponsor"], row["order_index"], row["repeat"]))
jobs = [
    (model, bill["id"], arm, order, repeat)
    for model in MODELS
    for bill in bills
    for arm in ARMS
    for order in range(len(ORDERS))
    for repeat in range(REPEATS_PER_ORDER)
    if (model, bill["id"], arm, order, repeat) not in done
]
random.Random(SEED).shuffle(jobs)
print("to run:", len(jobs), flush=True)
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
    model, bill, arm, order, repeat = job
    wait_for_rate_limit()
    try:
        row = call_model(model, by_id[bill], arm, order, repeat, provider=args.provider)
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
print("still failing:", len(jobs), flush=True)
