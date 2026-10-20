"""Freenove adapter wiring tests — fake vendor modules injected into
sys.modules so the mapping logic runs on the Mac with no hardware. These
verify OUR wiring (speed maps, command shapes, fail-safe sensor handling),
not vendor behavior; physical correctness waits for the stand (CALIBRATE
tags in the adapter)."""

import sys
import types
from unittest.mock import patch

import pytest


class FakeServo:
    def __init__(self):
        self.angles = {}
        self.relaxed = False

    def set_servo_angle(self, channel, angle):
        self.angles[channel] = angle

    def relax(self):
        self.relaxed = True


class FakeGPIO:
    def __init__(self):
        self.state = "off"

    def on(self):
        self.state = "on"

    def off(self):
        self.state = "off"


class FakeControl:
    def __init__(self):
        self.servo = FakeServo()
        self.servo_power_disable = FakeGPIO()
        self.current_angles = [[90, 0, 0]] * 6
        self.gait_calls = []
        self.positions = []
        self.relax_calls = []

    def run_gait(self, data):
        self.gait_calls.append(list(data))

    def move_position(self, x, y, z):
        self.positions.append((x, y, z))

    def relax(self, flag):
        self.relax_calls.append(flag)
        if flag:
            self.servo.relax()


class FakeUltrasonic:
    def __init__(self, *a, **k):
        self.value = 120.0

    def get_distance(self):
        return self.value


class FakeADC:
    def __init__(self):
        self.readings = (7.9, 7.7)

    def read_battery_voltage(self):
        return self.readings


@pytest.fixture
def hand(tmp_path, monkeypatch):
    """Build a FreenoveHand against injected fake vendor modules."""
    fakes = {}
    for name, cls in [("control", FakeControl), ("servo", FakeServo),
                      ("ultrasonic", FakeUltrasonic), ("adc", FakeADC)]:
        mod = types.ModuleType(name)
        setattr(mod, name.capitalize() if name != "adc" else "ADC", cls)
        fakes[name] = mod
    import hand.freenove_hand as fh
    monkeypatch.setattr(fh, "VENDOR_DIR", tmp_path)  # harmless chdir target
    with patch.dict(sys.modules, fakes):
        yield fh.FreenoveHand()


class TestAdapterWiring:
    def test_walk_issues_one_gait_cycle_per_step(self, hand):
        r = hand.walk(heading_deg=0, steps=3, speed=0.5)
        assert r["status"] == "walked" and r["steps"] == 3
        assert len(hand.control.gait_calls) == 3
        cmd, gait, x, y, speed, angle = hand.control.gait_calls[0]
        assert cmd == "CMD_MOVE" and angle == "0"
        assert (int(x), int(y)) == (0, 25)     # heading 0 = straight ahead
        assert speed == "6"                    # 0.5 -> vendor midpoint

    def test_speed_mapping_bounds(self, hand):
        hand.walk(0, 1, 0.2)
        hand.walk(0, 1, 0.8)
        assert hand.control.gait_calls[0][4] == "2"
        assert hand.control.gait_calls[1][4] == "10"

    def test_cycle_hook_interrupts_walk(self, hand):
        hook_results = iter([True, False])
        hand.cycle_hook = lambda: next(hook_results)
        r = hand.walk(0, 5, 0.5)
        assert r["status"] == "interrupted" and r["steps_done"] == 2
        # stop() ran: relax(False) holds pose
        assert hand.control.relax_calls[-1] is False

    def test_turn_cycles_scale_with_angle(self, hand):
        hand.turn(90)
        assert len(hand.control.gait_calls) == 9    # 90deg / 10deg per cycle
        assert hand.control.gait_calls[0][5] == "10"
        hand.control.gait_calls.clear()
        hand.turn(-30)
        assert len(hand.control.gait_calls) == 3
        assert hand.control.gait_calls[0][5] == "-10"

    def test_look_maps_to_head_channels(self, hand):
        hand.look(pan_deg=-30, tilt_deg=20)
        assert hand.servo.angles[0] == 60      # 90 + (-30)
        assert hand.servo.angles[1] == 110     # 90 + 20

    def test_posture_stances(self, hand):
        hand.posture("high")
        hand.posture("low")
        assert hand.control.positions == [(0, 0, 15), (0, 0, -15)]

    def test_torque_off_relaxes_and_cuts_rail(self, hand):
        hand.torque_off()
        assert hand.control.servo.relaxed is True
        assert hand.control.servo_power_disable.state == "on"

    def test_battery_tuple_gated_on_min(self, hand):
        hand.adc.readings = (8.1, 6.5)
        assert hand.battery_v() == 6.5

    def test_sonar_none_reads_as_obstacle(self, hand):
        hand.ultrasonic.value = None
        assert hand.sonar_cm() == 0.0          # fail-safe: unknown = obstacle
        hand.ultrasonic.value = 55.5
        assert hand.sonar_cm() == 55.5

    def test_never_imports_killed_vendor_modules(self):
        import hand.freenove_hand as fh
        src = open(fh.__file__).read()
        for banned in ("import server", "import main", "import buzzer",
                       "import led", "import camera"):
            assert banned not in src
