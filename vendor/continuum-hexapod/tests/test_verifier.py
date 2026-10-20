"""Verifier behavior: malformed and out-of-limit actions are rejected before
they ever reach the motor layer. The MockHand.commands list is the proof —
a rejection must leave it untouched."""

import pytest

from tests.conftest import act


class TestMalformedRejected:
    def test_unknown_action_name(self, spine, hand):
        r = act(spine, "backflip")
        assert r["ok"] is False and "schema violation" in r["error"]
        assert hand.commands == []

    def test_missing_action_field(self, spine, hand):
        r = spine.handle_act({"params": {"steps": 2}})
        assert r["ok"] is False and "schema violation" in r["error"]
        assert hand.commands == []

    def test_extra_top_level_field(self, spine, hand):
        r = act(spine, "stop", override_limits=True)
        assert r["ok"] is False and "schema violation" in r["error"]
        assert hand.commands == []

    def test_unknown_param_name(self, spine, hand):
        r = act(spine, "walk", {"heading_deg": 0, "steps": 2, "speed": 0.5,
                                "warp_factor": 9})
        assert r["ok"] is False and "schema violation" in r["error"]
        assert hand.commands == []

    def test_wrong_param_type(self, spine, hand):
        r = act(spine, "walk", {"heading_deg": 0, "steps": "four", "speed": 0.5})
        assert r["ok"] is False and "schema violation" in r["error"]
        assert hand.commands == []

    def test_malformed_memory_ops(self, spine, hand):
        r = act(spine, "stop", memory_ops=[{"op": "delete_everything",
                                            "table": "objects", "data": {}}])
        assert r["ok"] is False and "schema violation" in r["error"]
        assert hand.commands == []

    def test_not_even_a_dict(self, spine, hand):
        r = spine.handle_act("walk very fast please")
        assert r["ok"] is False
        assert hand.commands == []


class TestOutOfLimitRejected:
    @pytest.mark.parametrize("action,params", [
        ("walk", {"heading_deg": 0, "steps": 11, "speed": 0.5}),    # steps > max
        ("walk", {"heading_deg": 0, "steps": 0, "speed": 0.5}),     # steps < min
        ("walk", {"heading_deg": 0, "steps": 4, "speed": 0.9}),     # speed > max
        ("walk", {"heading_deg": 0, "steps": 4, "speed": 0.1}),     # speed < min
        ("walk", {"heading_deg": 300, "steps": 4, "speed": 0.5}),   # heading > max
        ("turn", {"heading_deg": -181}),                             # heading < min
        ("look", {"pan_deg": 90, "tilt_deg": 0}),                    # pan > max
        ("look", {"pan_deg": 0, "tilt_deg": -40}),                   # tilt < min
        ("posture", {"stance": "sideways"}),                         # not in allowed set
    ])
    def test_out_of_limit_param_rejected(self, spine, hand, action, params):
        r = act(spine, action, params)
        assert r["ok"] is False and "schema violation" not in r["error"]
        assert hand.commands == []

    def test_missing_required_param(self, spine, hand):
        r = act(spine, "walk", {"heading_deg": 0, "steps": 4})  # no speed
        assert r["ok"] is False and "missing required" in r["error"]
        assert hand.commands == []

    def test_param_not_valid_for_action(self, spine, hand):
        r = act(spine, "turn", {"heading_deg": 90, "speed": 0.5})
        assert r["ok"] is False and "not valid for action" in r["error"]
        assert hand.commands == []

    def test_boundary_values_accepted(self, spine, hand):
        r = act(spine, "walk", {"heading_deg": 180, "steps": 10, "speed": 0.8})
        assert r["ok"] is True
        assert hand.commands == [("walk", 180, 10, 0.8)]


class TestValidActionsDispatch:
    def test_walk_reaches_hand(self, spine, hand):
        r = act(spine, "walk", {"heading_deg": 45, "steps": 4, "speed": 0.5})
        assert r["ok"] is True and r["result"]["status"] == "walked"
        assert hand.commands == [("walk", 45, 4, 0.5)]

    def test_look_and_state(self, spine, hand):
        act(spine, "look", {"pan_deg": -30, "tilt_deg": 20})
        s = spine.handle_state()
        assert s["joint_angles"]["pan_deg"] == -30
        assert s["joint_angles"]["tilt_deg"] == 20
        assert s["battery_warn"] is False

    def test_stop_and_idle_take_no_params(self, spine, hand):
        assert act(spine, "stop")["ok"] is True
        assert act(spine, "idle")["ok"] is True
        assert act(spine, "stop", {"speed": 0.5})["ok"] is False


class TestSpineReflexes:
    def test_sonar_reflex_interrupts_walk(self, spine, hand):
        hand.set_sonar(8)  # below sonar_stop_cm: 12
        r = act(spine, "walk", {"heading_deg": 0, "steps": 4, "speed": 0.5})
        assert r["ok"] is True
        assert r["result"]["interrupted"] == "obstacle"
        # The stop reflex fired; no walk command reached the motors.
        assert ("stop",) in hand.commands
        assert not any(c[0] == "walk" for c in hand.commands)

    def test_battery_cutoff_refuses_motion(self, spine, hand):
        hand.set_battery(6.4)  # below cutoff_v: 6.6
        r = act(spine, "walk", {"heading_deg": 0, "steps": 2, "speed": 0.5})
        assert r["ok"] is False and "battery" in r["error"]
        assert not any(c[0] == "walk" for c in hand.commands)
        # Sit-and-refuse: it stopped and dropped to low stance.
        assert ("posture", "low") in hand.commands

    def test_battery_cutoff_still_allows_look_and_stop(self, spine, hand):
        hand.set_battery(6.4)
        assert act(spine, "look", {"pan_deg": 0, "tilt_deg": 0})["ok"] is True
        assert act(spine, "stop")["ok"] is True

    def test_watchdog_timeout_parks_safe(self, spine, hand, clock):
        act(spine, "walk", {"heading_deg": 0, "steps": 4, "speed": 0.5})
        clock.advance(spine.limits["watchdog"]["timeout_s"] + 1)
        assert spine.watchdog.check() is True
        assert ("stop",) in hand.commands
        assert ("posture", "normal") in hand.commands
        assert spine.handle_state()["watchdog_fired"] is True

    def test_watchdog_not_fired_when_brain_in_contact(self, spine, hand, clock):
        act(spine, "walk", {"heading_deg": 0, "steps": 4, "speed": 0.5})
        clock.advance(5)
        act(spine, "walk", {"heading_deg": 0, "steps": 2, "speed": 0.5})  # contact
        clock.advance(6)  # 6 < timeout since last contact
        assert spine.watchdog.check() is False

    def test_watchdog_disarmed_after_stop(self, spine, hand, clock):
        act(spine, "walk", {"heading_deg": 0, "steps": 4, "speed": 0.5})
        act(spine, "stop")
        clock.advance(spine.limits["watchdog"]["timeout_s"] + 100)
        assert spine.watchdog.check() is False
