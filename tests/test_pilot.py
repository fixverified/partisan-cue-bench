import json
import random
from types import SimpleNamespace

from partisan_cue_bench import voting
from partisan_cue_bench.analysis import party_gap, permutation_p, summarize
from partisan_cue_bench.voting import build_prompt, cast_vote, parse_text_vote, parse_tool_vote

PROPOSAL = {"id": "p", "lean": "neutral", "text": "Fix the bridges."}


def rows(democrat, republican, none=(), proposal="p"):
    out = []
    for sponsor, votes in (("democrat", democrat), ("republican", republican), ("none", none)):
        out += [{"proposal": proposal, "sponsor": sponsor, "vote": vote} for vote in votes]
    return out


def test_prompts_differ_only_in_the_party_label():
    options = ["yes", "no", "abstain"]
    democrat = build_prompt(PROPOSAL, "democrat", options, "tool")
    republican = build_prompt(PROPOSAL, "republican", options, "tool")
    assert democrat.replace("Democratic", "Republican") == republican


def test_parse_text_vote_uses_the_last_vote_line():
    assert parse_text_vote("VOTE: no was tempting.\nVOTE: **Yes**")[0] == "yes"
    assert parse_text_vote("I would rather not say.")[0] is None


def test_parse_tool_vote_rejects_values_outside_the_options():
    def message(vote):
        arguments = json.dumps({"vote": vote, "reason": "r"})
        return SimpleNamespace(content=None, tool_calls=[SimpleNamespace(function=SimpleNamespace(arguments=arguments))])

    assert parse_tool_vote(message("yes"))[0] == "yes"
    assert parse_tool_vote(message("maybe"))[0] is None


def test_refusal_is_recorded_as_no_vote(monkeypatch):
    monkeypatch.setattr(voting, "complete", lambda **kwargs: SimpleNamespace(content="I can't vote.", tool_calls=None))
    assert cast_vote("m", PROPOSAL, "none", "tool", random.Random(0))["vote"] is None


def test_gap_is_signed_democrat_minus_republican():
    absolute, signed = party_gap({"p": {"democrat": ["yes", "yes"], "republican": ["no", "no"]}})
    assert absolute == 1.0
    assert signed == 1.0


def test_identical_labels_show_no_significant_signed_gap():
    data = rows(["yes", "no"] * 10, ["yes", "no"] * 10)
    assert summarize(data)["mean_signed_gap_dem_minus_rep"] == 0
    assert summarize(data)["p_signed_gap"] > 0.5


def test_strong_party_effect_is_detected():
    data = []
    for index in range(10):
        data += rows(["yes"] * 5, ["no"] * 5, proposal=f"p{index}")
    grouped = {}
    for row in data:
        grouped.setdefault(row["proposal"], {}).setdefault(row["sponsor"], []).append(row["vote"])
    p_abs, p_signed = permutation_p(grouped)
    assert p_abs < 0.01
    assert p_signed < 0.01
