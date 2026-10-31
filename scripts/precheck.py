"""Bill pre-check from docs/PREREGISTRATION.md: no-label votes only, then pick the final 100 bills."""

import collections
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from partisan_cue_bench.stage1 import ORDERS, REPEATS_PER_ORDER, call_model

MODELS = ["openai/gpt-6.1-sol", "anthropic/claude-opus-5"]
SEED = 20261031
OUT = Path("results/precheck.jsonl")
RECOGNIZABLE = {
    "imm_child_arrivals_residence",
    "soc_permanent_daylight",
    "gun_suppressor_registration",
    "hc_medicaid_work_hours",
    "gov_major_rule_approval",
    "gov_dc_statehood",
    "gov_proof_citizenship",
    "edu_scholarship_credit",
}
QUOTAS = {"left": 38, "right": 38, "mixed": 24}
PASSES = 5
WORKERS = 30

bills = [b for b in yaml.safe_load(open("data/candidates.yaml")) if b["id"] not in RECOGNIZABLE]
assert len(bills) == 192
by_id = {b["id"]: b for b in bills}
OUT.parent.mkdir(exist_ok=True)
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
print(f"{len(jobs)} calls to run", flush=True)
lock = threading.Lock()


def work(job):
    model, bill, order, repeat = job
    try:
        row = call_model(model, by_id[bill], "none", order, repeat)
    except Exception as error:  # noqa: BLE001 - API errors get re-queued
        print("error", type(error).__name__, flush=True)
        return job
    with lock, OUT.open("a") as handle:
        handle.write(json.dumps(row, default=str) + "\n")
    return None


for _ in range(PASSES):
    if not jobs:
        break
    pools = {model: ThreadPoolExecutor(WORKERS) for model in MODELS}
    futures = [pools[job[0]].submit(work, job) for job in jobs]
    jobs = [result for future in futures if (result := future.result()) is not None]
    for pool in pools.values():
        pool.shutdown()
print(f"{len(jobs)} calls still failing", flush=True)

rows = [json.loads(line) for line in OUT.read_text().splitlines()]
yes = collections.defaultdict(collections.Counter)
statuses = collections.Counter()
for row in rows:
    statuses[(row["model"], row["status"])] += 1
    yes[row["bill"]][row["model"]] += row["vote"] == "yes"
print("status", dict(statuses))

rng = random.Random(SEED)
scored = []
for bill in bills:
    counts = [yes[bill["id"]][model] for model in MODELS]
    split = sum(0 < count < 6 for count in counts)
    closeness = abs(sum(counts) / (len(MODELS) * 6) - 0.5)
    scored.append((-split, closeness, rng.random(), bill))
scored.sort(key=lambda item: item[:3])

chosen, spare = [], []
remaining = dict(QUOTAS)
for item in scored:
    lean = item[3]["lean"]
    if remaining[lean] > 0:
        remaining[lean] -= 1
        chosen.append(item)
    else:
        spare.append(item)
shortfall = sum(remaining.values())
if shortfall:
    print("quota shortfall", remaining, flush=True)
    chosen += spare[:shortfall]
assert len(chosen) == 100

final = [item[3] for item in chosen]
with open("data/bills_final.yaml", "w") as handle:
    yaml.safe_dump(final, handle, sort_keys=False, width=1000)

for model in MODELS:
    print(model, "split bills in all 192:", sum(0 < yes[b["id"]][model] < 6 for b in bills), "in final:", sum(0 < yes[b["id"]][model] < 6 for b in final))
print("final by split count", collections.Counter(-item[0] for item in chosen), "by lean", collections.Counter(b["lean"] for b in final), "by topic", collections.Counter(b["topic"] for b in final))
for model in MODELS:
    print(model, "final yes rate", round(sum(yes[b["id"]][model] for b in final) / 600, 3), {lean: round(sum(yes[b["id"]][model] for b in final if b["lean"] == lean) / (6 * max(1, sum(b["lean"] == lean for b in final))), 3) for lean in QUOTAS})
