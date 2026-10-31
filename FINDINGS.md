# Findings

## Finding 1: without a party label, votes split sharply by the bill's political coding

In the bill pre-check, `gpt-6.1-sol` said yes to 96% of left-coded bills and none of the right-coded ones. `claude-opus-5` said yes to 76% and 2%.

| Model | Left-coded yes | Right-coded yes | Mixed yes |
|---|---|---|---|
| `gpt-6.1-sol` | 428/444 (96%) | 0/420 (0%) | 169/288 (59%) |
| `claude-opus-5` | 338/444 (76%) | 9/420 (2%) | 198/288 (69%) |

21 mirror pairs push one policy in opposite directions. Neither model ever voted no on the left-coded bill and yes on its right-coded mirror:

| Model | Yes left, no right | No on both | No left, yes right |
|---|---|---|---|
| `gpt-6.1-sol` | 20 | 1 | 0 |
| `claude-opus-5` | 13 | 8 | 0 |

**Data:** [`data/precheck_votes.jsonl`](data/precheck_votes.jsonl), with 192 bills, 6 votes per model and bill, and 2,304 votes, all valid. Each vote was a required yes/no tool call in a fresh conversation, with no system prompt and no party named.

**How to read it:** this is a strong, measured result for these bills, this prompt and these models. It's separate from the main question of whether party labels change votes. Random mislabeling can't explain a result this extreme.

**Limits:**
- It wasn't the planned test. It came from a pre-check for choosing bills, so it should be replicated.
- The bills are AI-written, and a Claude model is a test subject. Wording could favor one side, including how costs and benefits are stated.
- The bills aren't a representative sample of policy, and votes are forced yes/no choices, so this doesn't by itself show how the models respond elsewhere.

**Next test:** rewrite the mirror pairs with costs and benefits stated evenly, add bills from other authors, including right-leaning people and other model families, and see whether the gap holds.
