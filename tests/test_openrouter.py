import json
from types import SimpleNamespace

from partisan_cue_bench import stage1
from partisan_cue_bench.stage1 import call_model, openrouter_routing

BILL = {"id": "b", "lean": "left", "topic": "t", "text": "Does a thing."}


def fake_client(monkeypatch, sent, arguments='{"vote": "yes"}', finish="tool_calls"):
    call = {"function": {"name": "record_vote", "arguments": arguments}}
    message = SimpleNamespace(model_dump=lambda: {"content": None, "tool_calls": [call]})
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=message, finish_reason=finish)],
        model="deepseek/deepseek-chat",
        provider="DeepInfra",
        usage=SimpleNamespace(model_dump=lambda: {"prompt_tokens": 5, "completion_tokens": 2}),
    )

    def create(**kwargs):
        sent.update(kwargs)
        return response

    class Client:
        def __init__(self, base_url, api_key):
            sent["base_url"] = base_url
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=create))

    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    monkeypatch.setattr("openai.OpenAI", Client)


def test_routing_requires_tools_and_blocks_fallbacks():
    assert openrouter_routing(None) == {"require_parameters": True, "allow_fallbacks": False}
    assert openrouter_routing("DeepInfra")["order"] == ["DeepInfra"]


def test_openrouter_call_sends_required_tool_and_records_host(monkeypatch):
    sent = {}
    fake_client(monkeypatch, sent)
    row = call_model("openrouter/deepseek/deepseek-chat", BILL, "democrat", 0, 0, provider="DeepInfra")
    assert sent["base_url"] == stage1.OPENROUTER_BASE_URL
    assert sent["model"] == "deepseek/deepseek-chat"
    assert sent["tool_choice"]["function"]["name"] == "record_vote"
    assert sent["extra_body"]["provider"]["order"] == ["DeepInfra"]
    assert (row["status"], row["vote"], row["provider"]) == ("valid", "yes", "DeepInfra")


def test_openrouter_extra_fields_stay_invalid(monkeypatch):
    fake_client(monkeypatch, {}, arguments=json.dumps({"vote": "yes", "reason": "r"}))
    assert call_model("openrouter/x/y", BILL, "none", 0, 0)["status"] == "malformed"
