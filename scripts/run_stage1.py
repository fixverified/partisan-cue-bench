"""Run Stage 1. Jobs are shuffled, saved as they finish, and resumable. API errors get re-queued."""

import argparse
import json
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import litellm
import yaml

from partisan_cue_bench.stage1 import ORDERS, REPEATS_PER_ORDER, SPONSORS, call_model

MODELS = ["openai/gpt-6.1-sol", "anthropic/claude-opus-5"]
SEED = 20261031
PASSES = 5
SUBSET_BY_LEAN = {"left": 4, "right": 3, "mixed": 3}

parser = argparse.ArgumentParser()
parser.add_argument("--out", default="results/stage1.jsonl")
parser.add_argument("--subset", action="store_true", help="Use the pre-set 10-bill subset")
parser.add_argument("--workers", type=int, default=30, help="Threads per model")
args = parser.parse_args()

litellm.suppress_debug_info = True
bills = yaml.safe_load(open("data/bills_final.yaml"))
if args.subset:
    rng = random.Random(SEED)
    bills = [
        bill
        for lean, count in SUBSET_BY_LEAN.items()
        for bill in rng.sample([b for b in bills if b["lean"] == lean], count)
    ]
    print("subset:", [bill["id"] for bill in bills], flush=True)
path = Path(args.out)
path.parent.mkdir(parents=True, exist_ok=True)
errors_path = path.with_suffix(".errors.jsonl")
done = set()
if path.exists():
    for line in path.read_text().splitlines():
        row = json.loads(line)
        done.add((row["model"], row["bill"], row["sponsor"], row["order_index"], row["repeat"]))
by_id = {bill["id"]: bill for bill in bills}
all_jobs = [
    (model, bill["id"], sponsor, order, repeat)
    for model in MODELS
    for bill in bills
    for sponsor in SPONSORS
    for order in range(len(ORDERS))
    for repeat in range(REPEATS_PER_ORDER)
]
jobs = [job for job in all_jobs if job not in done]
random.Random(SEED).shuffle(jobs)
print(f"{len(all_jobs)} planned, {len(done)} done, {len(jobs)} to run", flush=True)

lock = threading.Lock()


def work(job):
    model, bill, sponsor, order_index, repeat = job
    try:
        row = call_model(model, by_id[bill], sponsor, order_index, repeat)
        row["finished_at"] = time.time()
    except Exception as error:  # noqa: BLE001 - API errors get re-queued and logged
        with lock, errors_path.open("a") as handle:
            handle.write(json.dumps({"job": job, "error": type(error).__name__, "at": time.time()}) + "\n")
        return job
    with lock, path.open("a") as handle:
        handle.write(json.dumps(row, default=str) + "\n")
    return None


def run_all(pending):
    pools = {model: ThreadPoolExecutor(args.workers) for model in MODELS}
    futures = [pools[job[0]].submit(work, job) for job in pending]
    failed = [result for future in futures if (result := future.result()) is not None]
    for pool in pools.values():
        pool.shutdown()
    return failed


for attempt in range(PASSES):
    if not jobs:
        break
    jobs = run_all(jobs)
    print(f"pass {attempt + 1}: {len(jobs)} failed", flush=True)
    if jobs:
        time.sleep(20 * (attempt + 1))
print(f"finished; {len(jobs)} jobs still failing", flush=True)
