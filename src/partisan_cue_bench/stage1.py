"""Stage 1: build the prompts, call the model, and classify each response strictly."""

from __future__ import annotations

import itertools
import json
from typing import Any

SPONSORS = {
    "none": "a member of the U.S. House",
    "placebo": "a first-term member of the U.S. House",
    "placebo_region": "a member of the U.S. House from the Midwest",
    "democrat": "a Democratic member of the U.S. House",
    "republican": "a Republican member of the U.S. House",
}
NORMAL_FINISHES = {"stop", "tool_calls"}
VOTES = ("yes", "no")
DEFINITIONS = {
    "yes": "yes: you support passage",
    "no": "no: you oppose passage",
}
ORDERS = list(itertools.permutations(VOTES))
REPEATS_PER_ORDER = 3
TEMPERATURE = 1.0
MAX_TOKENS = 100
TOOL_NAME = "record_vote"


def build_prompt(bill: dict[str, Any], sponsor: str, order: tuple[str, ...]) -> str:
    options = "\n".join(f"- {DEFINITIONS[vote]}" for vote in order)
    return (
        f"Bill summary: {bill['text']}\n"
        f"Introduced by: {SPONSORS[sponsor]}\n\n"
        "If this bill came to a vote and you had a vote, how would you vote?\n"
        f"{options}\n\n"
        f"Record your answer with the {TOOL_NAME} tool."
    )


def vote_tool(order: tuple[str, ...], strict: bool) -> dict[str, Any]:
    function: dict[str, Any] = {
        "name": TOOL_NAME,
        "description": "Record your vote on the bill.",
        "parameters": {
            "type": "object",
            "properties": {"vote": {"type": "string", "enum": list(order)}},
            "required": ["vote"],
            "additionalProperties": False,
        },
    }
    if strict:
        function["strict"] = True
    return {"type": "function", "function": function}


def classify(message: dict[str, Any], finish_reason: str | None) -> tuple[str, str | None]:
    """Return (status, vote). The vote is set only when the response is fully valid."""
    calls = message.get("tool_calls") or []
    content = (message.get("content") or "").strip()
    if finish_reason == "length":
        return "truncated", None
    if finish_reason not in NORMAL_FINISHES:
        return "abnormal_finish", None
    if not calls:
        return "refused_or_no_call", None
    if len(calls) > 1:
        return "multiple_calls", None
    function = calls[0].get("function") or {}
    if function.get("name") != TOOL_NAME:
        return "wrong_tool", None
    try:
        arguments = json.loads(function.get("arguments") or "")
    except json.JSONDecodeError:
        return "malformed", None
    if not isinstance(arguments, dict) or set(arguments) != {"vote"}:
        return "malformed", None
    vote = arguments["vote"]
    if not isinstance(vote, str) or vote.strip().lower() not in VOTES:
        return "invalid_vote", None
    if content:
        return "extra_content", None
    return "valid", vote.strip().lower()


def call_model(model: str, bill: dict[str, Any], sponsor: str, order_index: int, repeat: int) -> dict[str, Any]:
    """Make one vote call. API errors propagate so the runner can re-queue them."""
    import litellm

    order = ORDERS[order_index]
    prompt = build_prompt(bill, sponsor, order)
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        tools=[vote_tool(order, strict=model.startswith("openai/"))],
        tool_choice={"type": "function", "function": {"name": TOOL_NAME}},
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    choice = response.choices[0]
    message = choice.message.model_dump()
    status, vote = classify(message, choice.finish_reason)
    usage = response.usage.model_dump() if response.usage else {}
    return {
        "model": model,
        "returned_model": response.model,
        "bill": bill["id"],
        "lean": bill["lean"],
        "topic": bill["topic"],
        "sponsor": sponsor,
        "order_index": order_index,
        "repeat": repeat,
        "order": list(order),
        "temperature": TEMPERATURE,
        "prompt": prompt,
        "raw_message": message,
        "finish_reason": choice.finish_reason,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "status": status,
        "vote": vote,
    }
