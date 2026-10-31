import json

import pytest
import yaml

from partisan_cue_bench.stage1 import ORDERS, SPONSORS, build_prompt, classify, vote_tool

BILLS = yaml.safe_load(open("data/proposals_v2.yaml"))
BILL = BILLS[0]


def tool_message(arguments, name="record_vote", content=None, extra=False):
    call = {"function": {"name": name, "arguments": json.dumps(arguments)}}
    return {"content": content, "tool_calls": [call, call] if extra else [call]}


def test_bills_are_complete_and_unique():
    assert len(BILLS) == 100
    assert len({bill["id"] for bill in BILLS}) == 100


def test_prompts_differ_only_in_the_sponsor_text():
    base = build_prompt(BILL, "none", ORDERS[0])
    for sponsor, text in SPONSORS.items():
        assert build_prompt(BILL, sponsor, ORDERS[0]) == base.replace(SPONSORS["none"], text)


def test_prompt_hides_analysis_labels_and_has_no_role_or_reason_request():
    prompt = build_prompt(BILL, "democrat", ORDERS[0])
    assert BILL["lean"] not in prompt.split("Introduced by")[0]
    assert "You are" not in prompt
    assert "reason" not in prompt.lower()
    assert "in this order" not in prompt


def test_every_order_is_used_and_shown():
    assert len(set(ORDERS)) == 2
    for order in ORDERS:
        prompt = build_prompt(BILL, "none", order)
        assert prompt.index(order[0] + ":") < prompt.index(order[1] + ":")


def test_tool_has_only_the_vote_field():
    parameters = vote_tool(ORDERS[0], strict=True)["function"]["parameters"]
    assert list(parameters["properties"]) == ["vote"]
    assert parameters["additionalProperties"] is False


@pytest.mark.parametrize(
    ("message", "finish", "expected"),
    [
        (tool_message({"vote": "yes"}), "tool_calls", ("valid", "yes")),
        (tool_message({"vote": " No "}), "tool_calls", ("valid", "no")),
        (tool_message({"vote": "yes"}, content="  "), "tool_calls", ("valid", "yes")),
        (tool_message({"vote": "yes"}, content="I support this."), "tool_calls", ("extra_content", None)),
        (tool_message({"vote": "yes", "reason": "r"}), "tool_calls", ("malformed", None)),
        (tool_message({"vote": "abstain"}), "tool_calls", ("invalid_vote", None)),
        (tool_message({"vote": "maybe"}), "tool_calls", ("invalid_vote", None)),
        (tool_message({"vote": "yes"}, extra=True), "tool_calls", ("multiple_calls", None)),
        (tool_message({"vote": "yes"}, name="other"), "tool_calls", ("wrong_tool", None)),
        (tool_message({"vote": "yes"}), "length", ("truncated", None)),
        (tool_message({"vote": "yes"}), "content_filter", ("abnormal_finish", None)),
        (tool_message({"vote": "yes"}), None, ("abnormal_finish", None)),
        ({"content": "I can't vote.", "tool_calls": None}, "stop", ("refused_or_no_call", None)),
    ],
)
def test_classify_is_strict(message, finish, expected):
    assert classify(message, finish) == expected


def test_malformed_json_fails():
    message = {"content": None, "tool_calls": [{"function": {"name": "record_vote", "arguments": "{oops"}}]}
    assert classify(message, "tool_calls") == ("malformed", None)
