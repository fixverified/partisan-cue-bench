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

## Finding 2: the split largely remains after removing stated costs and benefits

The same 192 bills were rewritten by `gpt-6.1-sol` to state only what they do, with no party or lean shown, and both models voted again. Bills weren't changed after seeing results.

| Model | Left-coded yes | Right-coded yes | Mixed yes |
|---|---|---|---|
| `gpt-6.1-sol` | 437/444 (98%) | 4/420 (1%) | 175/288 (61%) |
| `claude-opus-5` | 340/444 (77%) | 59/420 (14%) | 218/288 (76%) |

Mirror pairs, out of 21:

| Model | Yes left, no right | No on both | No left, yes right |
|---|---|---|---|
| `gpt-6.1-sol` | 20 | 1 | 0 |
| `claude-opus-5` | 13 | 7 | 1 |

**Data:** [`data/clean_votes.jsonl`](data/clean_votes.jsonl) and [`data/bills_clean.yaml`](data/bills_clean.yaml), with 2,304 votes, all valid.

**How to read it:** removing stated costs and benefits doesn't explain the split. `gpt-6.1-sol` barely changed. `claude-opus-5`'s yes rate on right-coded bills rose from 2% to 14%, so stated effects mattered somewhat for that model.

**Limits:** the lean labels and original bills came from Claude, and `gpt-6.1-sol` did the rewriting and is also tested. Bills are still from one AI-written set, votes are forced yes/no, and independent bill sources haven't been tested.

## Finding 3: party labels had little overall effect, with one exploratory signal for Claude

Both models voted on the same 192 cleaned bills under Democratic, Republican and placebo sponsors. Each model, bill and label got 4 votes. Baseline votes are the matching votes from the earlier no-label run.

| Yes rate | No party | First-term | Midwest | Democrat | Republican |
|---|---|---|---|---|---|
| `gpt-6.1-sol` | 53.6% | 53.1% | 53.8% | 54.6% | 54.0% |
| `claude-opus-5` | 53.4% | 51.2% | 53.0% | 55.9% | 57.8% |

| Democrat minus Republican | Mean gap | Bills moved (toward D / toward R) | p |
|---|---|---|---|
| `gpt-6.1-sol` | +0.5 points | 6 of 192 (4 / 2) | 0.63 |
| `claude-opus-5` | -2.0 points | 23 of 192 (8 / 15) | 0.16 |

Neither model showed a detectable overall lean toward one sponsor party. Neither gap is large enough to rule out a small effect.

**Exploratory signal:** compared with no party named, `claude-opus-5` said yes more often under a Republican sponsor, on 19 bills up and 2 down (+4.4 points, p=0.0001). A Democratic sponsor showed a smaller rise, on 15 up and 6 down (+2.5 points, p=0.03). The placebo labels didn't show this rise. `gpt-6.1-sol` showed no such pattern. These comparisons need confirming with new data.

**Data:** [`data/label_votes.jsonl`](data/label_votes.jsonl) and [`data/clean_votes.jsonl`](data/clean_votes.jsonl), analyzed with [`scripts/analyze_labels.py`](scripts/analyze_labels.py). All 6,144 label votes and 2,304 no-label votes were valid.

**Limits:**
- The analysis was changed before seeing results, following a review, and it differs from the earlier plan. p-values aren't corrected across all comparisons.
- Most bills are unanimous, so a label has little visible room to move votes.
- The baseline came from a separate earlier run, so timing could contribute to differences from no-party votes.
- Four votes per cell can't confirm any single bill.
- Claude-authored bills and lean labels, and forced yes/no votes, limit how far this applies.

## Finding 4: GLM 5.3 showed the same wide split, and Grok 4.3 was close to even

`z-ai/glm-5.3` (hosted by Wafer) and `x-ai/grok-4.3` (hosted by xAI) ran the same 192 bills through OpenRouter, with the same prompt and temperature 1. A partial DeepSeek run hit a rate limit for new accounts, was dropped before any analysis, and isn't included.

| Model | Left-coded yes | Right-coded yes | Mixed yes | Yes left, no right | No on both | No left, yes right | Yes on both |
|---|---|---|---|---|---|---|---|
| `z-ai/glm-5.3` | 419/444 (94%) | 94/420 (22%) | 232/288 (81%) | 19 | 1 | 1 | 0 |
| `x-ai/grok-4.3` | 278/444 (63%) | 236/420 (56%) | 211/288 (73%) | 9 | 3 | 7 | 2 |

| Yes rate | No party | First-term | Midwest | Democrat | Republican | D minus R | p |
|---|---|---|---|---|---|---|---|
| `z-ai/glm-5.3` | 64.3% | 61.8% | 65.0% | 62.8% | 63.3% | -0.5 points | 0.78 |
| `x-ai/grok-4.3` | 62.5% | 58.1% | 61.2% | 58.9% | 61.5% | -2.6 points | 0.16 |

Neither model showed a detectable overall lean toward one sponsor party.

**Exploratory signal:** both models said yes more often when a sponsor's party matched a bill's coding: `x-ai/grok-4.3` by 6.4 points (41 bills up, 20 down, p=0.003), and `z-ai/glm-5.3` by 3.5 points (31 up, 18 down, p=0.04). These comparisons need confirming with new data. Both models' votes also moved under neutral labels: the average bill-level gap between Democrat and Republican was about the same as between first-term and Midwest (13.5 vs. 13.0 points for Grok, 10.2 vs. 10.7 for GLM).

**Data:** [`data/openrouter/`](data/openrouter), analyzed with [`scripts/analyze_labels.py`](scripts/analyze_labels.py). All 4,224 GLM votes were valid. Of 4,224 Grok votes, 52 were invalid because they added text, and these count as not voting yes. Mirror-pair outcomes use the majority of a bill's 6 no-label votes.

**Limits:**
- These results describe these models on these hosts. `x-ai/grok-4.3` is an April 2026 release, and newer Grok versions weren't run. In a 12-vote check, Grok 4.7 and 4.5 added text to 6 and 3 votes, so they weren't used. Grok 4.6 was skipped because of cost.
- Bill coding and bill text still come from AI models, and neither of these models was involved in writing them.
- `x-ai/grok-4.3` averaged about 435 reasoning tokens per vote, and `z-ai/glm-5.3` about 18, so differences between models may partly reflect how much they reason.
- The limits in Finding 3 on p-value correction, four votes per cell and separate baseline runs also apply.
