"""Rewrite bills to state only what they do, using a non-Claude model that isn't shown any lean label."""

import json
import re
from concurrent.futures import ThreadPoolExecutor

import yaml
from openai import OpenAI

MODEL = "gpt-6.1-sol"
EXCLUDED = {
    "imm_child_arrivals_residence",
    "soc_permanent_daylight",
    "gun_suppressor_registration",
    "hc_medicaid_work_hours",
    "gov_major_rule_approval",
    "gov_dc_statehood",
    "gov_proof_citizenship",
    "edu_scholarship_credit",
}
INSTRUCTIONS = """Rewrite this bill summary so it states only what the bill legally does.

Rules:
- Keep the bill's legal provisions, including its amounts, thresholds and dates when they define what the law requires.
- Remove every stated cost, saving, revenue figure, benefit, harm, tradeoff, purpose, prediction and number of people affected.
- Use plain, neutral language. Start with a verb such as "Requires", "Prohibits" or "Sets".
- Do not add any new provisions or details.
- Return only the rewritten summary, as one sentence.

Bill summary: {text}"""
# Flags phrases that usually describe effects rather than provisions, for review.
EFFECT_WORDS = re.compile(
    r"\b(saving|savings|costing|costs?|revenue|benefit\w*|harm\w*|estimated|projected|lowering|raising about|adding about|reducing|giving up|leaving|avoiding|tradeoff|billion a year|million a year)\b",
    re.IGNORECASE,
)

client = OpenAI()
bills = [bill for bill in yaml.safe_load(open("data/candidates.yaml")) if bill["id"] not in EXCLUDED]
assert len(bills) == 192


def rewrite(bill):
    response = client.responses.create(model=MODEL, input=INSTRUCTIONS.format(text=bill["text"]), max_output_tokens=4000)
    return {**bill, "text": response.output_text.strip(), "original_text": bill["text"]}


with ThreadPoolExecutor(30) as pool:
    clean = list(pool.map(rewrite, bills))

with open("data/bills_clean.yaml", "w") as handle:
    yaml.safe_dump(clean, handle, sort_keys=False, width=1000)

flagged = [bill for bill in clean if EFFECT_WORDS.search(bill["text"])]
print(json.dumps({"bills": len(clean), "flagged": len(flagged), "words_before": sum(len(b["original_text"].split()) for b in clean) // len(clean), "words_after": sum(len(b["text"].split()) for b in clean) // len(clean)}))
for bill in flagged:
    print("FLAG", bill["id"], "|", bill["text"][:150])
for bill in clean[:6]:
    print("OK?", bill["lean"], "|", bill["text"][:150])
