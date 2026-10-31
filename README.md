# vote-bench

Does an AI model's vote change when only the bill's party label changes?

Each model votes `yes` or `no` on the same bill in fresh conversations, with the bill's sponsor given as a Democratic member, a Republican member, a first-term member, or just a member. The bill text never changes.

**Status:** work in progress, with no conclusions yet. The method is still being improved, and the 100-bill run hasn't happened. See:

- [`PREREG.md`](PREREG.md): the analysis plan
- [`METHOD_REVIEW.md`](METHOD_REVIEW.md): flaws found in the method, and what changed

An earlier 3-option pilot and a 10-bill yes/no test helped shape the method. They're too limited to support claims about model bias.

## Try it

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
cp .env.example .env   # then add your keys
set -a; . ./.env; set +a
.venv/bin/python scripts/make_proposals_v2.py
.venv/bin/python scripts/run_stage1.py --subset --out results/stage1_subset.jsonl
.venv/bin/python scripts/analyze_stage1.py results/stage1_subset.jsonl
```
