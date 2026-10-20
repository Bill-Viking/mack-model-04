"""HTTP-layer tests: the same verifier guarantees hold over the wire
(FastAPI TestClient, available now that httpx is installed)."""

import pytest
from fastapi.testclient import TestClient

from spine.spine import create_app


@pytest.fixture
def client(spine):
    app = create_app(spine)
    with TestClient(app) as c:
        yield c
    spine.watchdog.shutdown()


class TestHTTP:
    def test_valid_act_roundtrip(self, client, hand):
        r = client.post("/act", json={
            "action": "walk",
            "params": {"heading_deg": 0, "steps": 2, "speed": 0.5},
            "rationale": "t", "expected_outcome": "t"})
        assert r.status_code == 200
        assert r.json()["ok"] is True
        assert hand.commands == [("walk", 0, 2, 0.5)]

    def test_malformed_action_rejected_over_http(self, client, hand):
        r = client.post("/act", json={"action": "backflip"})
        assert r.json()["ok"] is False
        assert hand.commands == []

    def test_non_json_body_rejected(self, client, hand):
        r = client.post("/act", content=b"walk very fast",
                        headers={"Content-Type": "application/json"})
        assert r.status_code == 422       # FastAPI body validation
        assert hand.commands == []

    def test_out_of_limit_rejected_over_http(self, client, hand):
        r = client.post("/act", json={
            "action": "walk",
            "params": {"heading_deg": 0, "steps": 2, "speed": 9.9}})
        assert r.json()["ok"] is False and "speed" in r.json()["error"]
        assert hand.commands == []

    def test_state_endpoint(self, client):
        s = client.get("/state").json()
        assert {"battery_v", "sonar_cm", "joint_angles",
                "watchdog_fired"} <= set(s)

    def test_memory_op_over_http(self, client, scribe):
        client.post("/act", json={
            "action": "stop", "params": {},
            "memory_ops": [{"op": "upsert", "table": "objects",
                            "data": {"label": "http mug"}}]})
        assert scribe.conn.execute(
            "SELECT COUNT(*) FROM objects").fetchone()[0] == 1
