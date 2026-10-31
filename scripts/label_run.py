"""Party-label run on the clean bills: Democrat, Republican and two placebo labels, 4 votes per bill and label."""

import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from partisan_cue_bench.stage1 import ORDERS, call_model

MODELS = ["openai/gpt-6.1-sol", "anthropic/claude-opus-5"]
ARMS = ["democrat", "republican", "placebo", "placebo_region"]
REPEATS_PER_ORDER = 2
OUT = Path("data/label_votes.jsonl")
SEED = 20261031
KEEP = ["model", "returned_model", "bill", "lean", "topic", "sponsor", "order_index", "repeat", "order", "temperature", "prompt", "finish_reason", "prompt_tokens", "completion_tokens", "reasoning_tokens", "status", "vote"]

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


def work(job):
    model, bill, arm, order, repeat = job
    try:
        row = call_model(model, by_id[bill], arm, order, repeat)
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
