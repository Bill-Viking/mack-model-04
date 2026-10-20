"""SimHand — the virtual body. Third HandInterface implementation, alongside
MockHand (unit tests) and FreenoveHand (hardware). The Spine and Brain cannot
tell the difference; that is the point.

SimFrameSource is the matching camera: renders what the robot would see from
its current pose (including head pan/tilt) as a base64 JPEG for the Brain's
vision loop.
"""

from typing import Optional

from hand.hand_interface import HandInterface

from .world import World


class SimHand(HandInterface):
    def __init__(self, world: World):
        self.world = world
        self._pose = {"stance": "normal", "pan_deg": 0.0, "tilt_deg": 0.0}
        self.torque_on = True
        # Same contract as FreenoveHand: the Spine installs its reflex check
        # here; called between gait cycles, False aborts the walk.
        self.cycle_hook = None

    # --- motion primitives ---

    def walk(self, heading_deg: float, steps: int, speed: float) -> dict:
        advanced = 0
        for done in range(1, steps + 1):
            if self.world.do_step(heading_deg, speed):
                advanced += 1
            if self.cycle_hook is not None and not self.cycle_hook():
                return {"status": "interrupted", "steps_done": done,
                        "steps_requested": steps, "advanced": advanced}
        # Like the real robot: legs executed every commanded cycle; whether the
        # body actually moved is for the sensors to reveal.
        return {"status": "walked", "heading_deg": heading_deg,
                "steps": steps, "speed": speed, "advanced": advanced}

    def turn(self, heading_deg: float) -> dict:
        # Mirror FreenoveHand: ~10deg per gait cycle, noisy.
        cycles = max(1, round(abs(heading_deg) / 10))
        per_cycle = heading_deg / cycles
        for _ in range(cycles):
            self.world.do_turn_cycle(per_cycle)
        return {"status": "turned", "heading_deg": heading_deg,
                "cycles": cycles}

    def look(self, pan_deg: float, tilt_deg: float) -> dict:
        self.world.drain_misc()
        self._pose["pan_deg"] = pan_deg
        self._pose["tilt_deg"] = tilt_deg
        return {"status": "looking", "pan_deg": pan_deg, "tilt_deg": tilt_deg}

    def posture(self, stance: str) -> dict:
        self.world.drain_misc()
        self._pose["stance"] = stance
        return {"status": "posture", "stance": stance}

    def stop(self) -> dict:
        return {"status": "stopped"}

    def torque_off(self) -> None:
        self.torque_on = False

    # --- sensors ---

    def sonar_cm(self) -> float:
        # The ultrasonic rides the pan head, like the real robot.
        return self.world.sonar_cm(pan_deg=self._pose["pan_deg"])

    def battery_v(self) -> float:
        return round(self.world.battery_v, 2)

    def joint_angles(self) -> dict:
        return {**self._pose, "heading_deg": round(self.world.heading_deg, 1)}


class SimFrameSource:
    """FrameSource over the sim world — renders the robot's current view."""

    def __init__(self, world: World, hand: SimHand):
        self.world = world
        self.hand = hand

    def capture_b64(self) -> Optional[str]:
        from .render import frame_b64
        pose = self.hand.joint_angles()
        return frame_b64(self.world, pan_deg=pose["pan_deg"],
                         tilt_deg=pose["tilt_deg"])
