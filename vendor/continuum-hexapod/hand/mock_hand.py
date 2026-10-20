"""Mock Hand — same interface as the future Freenove adapter, no hardware.

Records every command it receives (``commands`` list) so tests can assert
exactly what reached the motor layer. Sensor readings are settable attributes
so tests can simulate obstacles and low battery.
"""

from .hand_interface import HandInterface


class MockHand(HandInterface):
    def __init__(self, sonar_cm: float = 100.0, battery_v: float = 7.8):
        self.commands: list[tuple] = []   # every motion call, in order
        self._sonar_cm = sonar_cm
        self._battery_v = battery_v
        self.torque_on = True
        self._pose = {"stance": "normal", "pan_deg": 0.0, "tilt_deg": 0.0,
                      "heading_deg": 0.0}
        self.walking = False

    # --- test knobs ---

    def set_sonar(self, cm: float) -> None:
        self._sonar_cm = cm

    def set_battery(self, volts: float) -> None:
        self._battery_v = volts

    # --- motion primitives ---

    def walk(self, heading_deg: float, steps: int, speed: float) -> dict:
        self.commands.append(("walk", heading_deg, steps, speed))
        self.torque_on = True
        self._pose["heading_deg"] = heading_deg
        return {"status": "walked", "heading_deg": heading_deg,
                "steps": steps, "speed": speed}

    def turn(self, heading_deg: float) -> dict:
        self.commands.append(("turn", heading_deg))
        self.torque_on = True
        self._pose["heading_deg"] = heading_deg
        return {"status": "turned", "heading_deg": heading_deg}

    def look(self, pan_deg: float, tilt_deg: float) -> dict:
        self.commands.append(("look", pan_deg, tilt_deg))
        self._pose["pan_deg"] = pan_deg
        self._pose["tilt_deg"] = tilt_deg
        return {"status": "looking", "pan_deg": pan_deg, "tilt_deg": tilt_deg}

    def posture(self, stance: str) -> dict:
        self.commands.append(("posture", stance))
        self._pose["stance"] = stance
        return {"status": "posture", "stance": stance}

    def stop(self) -> dict:
        self.commands.append(("stop",))
        self.walking = False
        return {"status": "stopped"}

    def torque_off(self) -> None:
        self.commands.append(("torque_off",))
        self.torque_on = False

    # --- sensors ---

    def sonar_cm(self) -> float:
        return self._sonar_cm

    def battery_v(self) -> float:
        return self._battery_v

    def joint_angles(self) -> dict:
        return dict(self._pose)
