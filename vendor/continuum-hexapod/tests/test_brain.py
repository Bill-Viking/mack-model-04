"""Brain loop tests: full Brain -> Spine -> Hand in process, with a fake
Claude client. Proves the tick shape, strict parsing (fail -> no-op), that
the Brain cannot bypass Spine validation, and episode logging."""

import json
from types import SimpleNamespace

import pytest

from brain.brain import (Brain, LocalSpineClient, StaticFrameSource,
                         parse_json_strict, render_contract_prompt)


class FakeClaude:
    """Scripted stand-in for anthropic.Anthropic — records every request."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.requests = []
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.requests.append(kwargs)
        text = self._responses.pop(0)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=text)])


def make_brain(spine, scribe, responses, db_path):
    return Brain(spine=LocalSpineClient(spine),
                 frame_source=StaticFrameSource(),
                 scribe=scribe, db_path=db_path,
                 client=FakeClaude(responses), session_id="test")


def action_json(**over):
    a = {"action": "look", "params": {"pan_deg": 10, "tilt_deg": 0},
         "rationale": "r", "expected_outcome": "e", "memory_ops": []}
    a.update(over)
    return json.dumps(a)


class TestTick:
    def test_valid_action_reaches_hand_and_logs_episode(self, spine, hand,
                                                        scribe, db_path):
        brain = make_brain(spine, scribe, [action_json()], db_path)
        result = brain.tick("look around")
        assert result["ok"] is True
        assert hand.commands == [("look", 10, 0)]
        row = scribe.conn.execute("SELECT * FROM episodes").fetchone()
        assert row["goal"] == "look around" and row["surprise"] == 0
        assert json.loads(row["action"])["action"] == "look"

    def test_unparseable_output_is_noop(self, spine, hand, scribe, db_path):
        brain = make_brain(spine, scribe,
                           ["Sure! I'll walk forward now."], db_path)
        result = brain.tick("explore")
        assert result["ok"] is False and result.get("retry") is True
        assert hand.commands == []

    def test_fenced_json_accepted(self, spine, hand, scribe, db_path):
        brain = make_brain(spine, scribe,
                           ["```json\n" + action_json() + "\n```"], db_path)
        assert brain.tick("look")["ok"] is True
        assert hand.commands == [("look", 10, 0)]

    def test_model_cannot_bypass_limits(self, spine, hand, scribe, db_path):
        evil = action_json(action="walk",
                           params={"heading_deg": 0, "steps": 99, "speed": 0.5})
        brain = make_brain(spine, scribe, [evil], db_path)
        result = brain.tick("run far away")
        assert result["ok"] is False
        assert hand.commands == []
        # Surprise flagged: rejection is a mismatch with expectation.
        row = scribe.conn.execute("SELECT * FROM episodes").fetchone()
        assert row["surprise"] == 1

    def test_memory_ops_flow_through_scribe(self, spine, scribe, db_path):
        a = action_json(memory_ops=[{"op": "upsert", "table": "objects",
                                     "data": {"label": "red mug"}}])
        brain = make_brain(spine, scribe, [a], db_path)
        result = brain.tick("catalog the room")
        assert result["memory_results"][0]["committed"] is True
        assert scribe.conn.execute(
            "SELECT COUNT(*) FROM objects").fetchone()[0] == 1

    def test_recall_block_in_system_prompt(self, spine, scribe, db_path):
        scribe.apply([{"op": "upsert", "table": "places",
                       "data": {"label": "kitchen", "descriptor": "tile floor"}}])
        brain = make_brain(spine, scribe, [action_json()], db_path)
        brain.tick("go to the kitchen")
        system = brain._client.requests[0]["system"]
        assert "kitchen" in system and "MEMORY RECALL" in system

    def test_state_included_in_user_turn(self, spine, scribe, db_path):
        brain = make_brain(spine, scribe, [action_json()], db_path)
        brain.tick("look")
        req = brain._client.requests[0]
        text = req["messages"][0]["content"][-1]["text"]
        assert "battery_v" in text and "Goal: look" in text


class TestContractPrompt:
    def test_limits_rendered_from_yaml(self):
        prompt = render_contract_prompt()
        assert "{{LIMITS}}" not in prompt
        assert "0.8" in prompt          # walk speed max from limits.yaml
        assert "sonar_stop_cm" not in prompt   # spine-internals stay out

    def test_no_hardcoded_limit_enforcement_language(self):
        # The prompt must present limits as informational, Spine as decider.
        prompt = render_contract_prompt()
        assert "the Spine's copy is the one that decides" in prompt


class TestParseJsonStrict:
    @pytest.mark.parametrize("bad", [
        "", "not json", '["a", "list"]', '"just a string"',
        '{"ok": true} trailing garbage', "```json\n{broken\n```"])
    def test_rejects(self, bad):
        assert parse_json_strict(bad) is None

    def test_accepts_plain_and_fenced(self):
        assert parse_json_strict('{"action": "stop"}') == {"action": "stop"}
        assert parse_json_strict('```json\n{"a": 1}\n```') == {"a": 1}
        assert parse_json_strict('```\n{"a": 1}\n```') == {"a": 1}
