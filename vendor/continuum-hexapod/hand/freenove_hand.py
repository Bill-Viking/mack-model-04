"""Freenove Hand adapter — Phase 2.5. Wraps vendor code behind HandInterface.

Written against the vendor repo as of 2026-07-17 (Code/Server/: control.py,
servo.py, ultrasonic.py, adc.py). NOT yet executed on hardware — every
mapping tagged CALIBRATE below must be verified on the test stand before
floor use.

Vendor policy (build doc, Phase 2):
- Imports ONLY keeper modules: control, servo, ultrasonic, adc. Never
  main/server/buzzer/led/camera modules.
- Imports are lazy (inside __init__): vendor modules pull in gpiozero/smbus/
  numpy at import time, so importing this file on the Mac stays safe.
- We do NOT start Control.condition_monitor (the vendor command-queue thread
  with its own 10s auto-relax) — the Spine owns scheduling and safety. We call
  the primitives directly: run_gait, move_position, relax, set_servo_angle.

Vendor facts discovered on read (confirm on hardware):
- ADC.read_battery_voltage() returns a TUPLE (channel0, channel4) despite its
  `-> float` annotation. We gate on min() of the two — conservative — until
  the servo-rail channel is confirmed. CALIBRATE.
- Ultrasonic.get_distance() returns cm, or None on a runtime warning. None is
  treated as 0.0 -> reads as obstacle -> Spine stops the walk. Fail-safe.
- Control.__init__ reads 'point.txt' with a relative path — we chdir to the
  vendor dir during construction.
- Head: servo channel 0 = pan, channel 1 = tilt (per server.py CMD_HEAD),
  0-180 range, 90 = center. CALIBRATE the center and sense on hardware.
- Control.run_gait(['CMD_MOVE', gait, x, y, speed, angle]) runs ONE gait
  cycle, blocking, x/y in -35..35, speed in 2..10, angle rotates in place.
"""

import contextlib
import logging
import math
import os
import sys
from pathlib import Path
from typing import Callable, Optional

from .hand_interface import HandInterface

log = logging.getLogger("freenove_hand")

VENDOR_DIR = Path(os.environ.get(
    "HEXAPOD_VENDOR_DIR",
    Path.home() / "Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi/Code/Server"))

# CALIBRATE: mapping constants — verify all of these on the stand.
GAIT = "1"              # tripod gait; "2" is the slower wave gait
XY_MAGNITUDE = 25       # per-cycle stride command in vendor units (max 35)
DEG_PER_TURN_CYCLE = 10  # approximate body rotation per run_gait cycle
PAN_CENTER, TILT_CENTER = 90, 90
STANCE_Z = {"low": -15, "normal": 0, "high": 15}   # vendor CMD_POSITION z units


@contextlib.contextmanager
def _in_vendor_dir():
    prev = os.getcwd()
    os.chdir(VENDOR_DIR)
    try:
        yield
    finally:
        os.chdir(prev)


def _vendor_speed(speed: float) -> int:
    """Map Spine speed 0.2..0.8 -> vendor 2..10."""
    return round(2 + (speed - 0.2) / 0.6 * 8)


class FreenoveHand(HandInterface):
    """The real Hand. Construct only on the Pi with the shield attached.

    cycle_hook: optional callable invoked between gait cycles; return False
    to abort the remaining cycles (the Spine wires its sonar reflex here so
    a multi-step walk can be interrupted mid-action, not just before/after).
    """

    def __init__(self, cycle_hook: Optional[Callable[[], bool]] = None):
        if str(VENDOR_DIR) not in sys.path:
            sys.path.insert(0, str(VENDOR_DIR))
        # Keeper modules only — see module docstring.
        with _in_vendor_dir():
            import adc as vendor_adc
            import control as vendor_control
            import ultrasonic as vendor_ultrasonic
            # Control() touches hardware at construction: inits IMU + PCA9685,
            # reads point.txt calibration, sets legs to calibrated stance.
            self.control = vendor_control.Control()
        self.servo = self.control.servo   # Servo() instance Control already made
        self.ultrasonic = vendor_ultrasonic.Ultrasonic()
        self.adc = vendor_adc.ADC()
        self.cycle_hook = cycle_hook
        self._pose = {"stance": "normal", "pan_deg": 0.0, "tilt_deg": 0.0,
                      "heading_deg": 0.0}
        self._last_sonar_cm = 300.0

    # --- motion primitives ---

    def walk(self, heading_deg: float, steps: int, speed: float) -> dict:
        rad = math.radians(heading_deg)
        # CALIBRATE: assumes vendor +y is robot-forward, +x is right.
        x = round(XY_MAGNITUDE * math.sin(rad))
        y = round(XY_MAGNITUDE * math.cos(rad))
        data = ["CMD_MOVE", GAIT, str(x), str(y), str(_vendor_speed(speed)), "0"]
        done = 0
        for _ in range(steps):
            self.control.run_gait(data)      # one blocking gait cycle
            done += 1
            if self.cycle_hook is not None and not self.cycle_hook():
                self.stop()
                return {"status": "interrupted", "steps_done": done,
                        "steps_requested": steps}
        return {"status": "walked", "heading_deg": heading_deg,
                "steps": done, "speed": speed}

    def turn(self, heading_deg: float) -> dict:
        # CALIBRATE: sign convention (positive = CCW) and deg-per-cycle.
        cycles = max(1, round(abs(heading_deg) / DEG_PER_TURN_CYCLE))
        angle = DEG_PER_TURN_CYCLE if heading_deg > 0 else -DEG_PER_TURN_CYCLE
        data = ["CMD_MOVE", GAIT, "0", "0", "6", str(angle)]
        done = 0
        for _ in range(cycles):
            self.control.run_gait(data)
            done += 1
            if self.cycle_hook is not None and not self.cycle_hook():
                self.stop()
                break
        self._pose["heading_deg"] = (self._pose["heading_deg"]
                                     + math.copysign(done * DEG_PER_TURN_CYCLE,
                                                     heading_deg)) % 360
        return {"status": "turned", "heading_deg": heading_deg,
                "cycles": done}

    def look(self, pan_deg: float, tilt_deg: float) -> dict:
        # Spine has already range-checked pan/tilt against limits.yaml.
        self.servo.set_servo_angle(0, int(PAN_CENTER + pan_deg))
        self.servo.set_servo_angle(1, int(TILT_CENTER + tilt_deg))
        self._pose["pan_deg"] = pan_deg
        self._pose["tilt_deg"] = tilt_deg
        return {"status": "looking", "pan_deg": pan_deg, "tilt_deg": tilt_deg}

    def posture(self, stance: str) -> dict:
        self.control.move_position(0, 0, STANCE_Z[stance])
        self._pose["stance"] = stance
        return {"status": "posture", "stance": stance}

    def stop(self) -> dict:
        # Hold pose with torque on (relax(False) re-asserts current leg angles).
        self.control.relax(False)
        return {"status": "stopped"}

    def torque_off(self) -> None:
        # Dead-man: PWM off on all leg channels, then cut the servo power rail.
        self.control.relax(True)                  # -> Servo.relax()
        self.control.servo_power_disable.on()     # GPIO4: disable servo power

    # --- sensors ---

    def sonar_cm(self) -> float:
        d = self.ultrasonic.get_distance()
        if d is None:
            # Fail-safe: unknown range reads as an obstacle at 0 cm.
            log.warning("ultrasonic returned None — treating as obstacle")
            return 0.0
        self._last_sonar_cm = d
        return d

    def battery_v(self) -> float:
        readings = self.adc.read_battery_voltage()   # tuple (ch0, ch4)!
        if isinstance(readings, tuple):
            return min(readings)   # conservative until channel roles confirmed
        return readings

    def joint_angles(self) -> dict:
        return {**self._pose,
                "leg_angles": [list(a) for a in self.control.current_angles]}
