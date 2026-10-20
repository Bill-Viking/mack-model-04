"""Hand layer contract — the boundary between the Spine and hardware.

The real adapter (freenove_hand.py, Phase 2.5) will implement this by importing
ONLY the vendor keeper modules (Control, Servo/PCA9685, Ultrasonic, ADC).
MockHand implements the same interface so the Spine and Brain are testable
with no robot attached.

The Hand performs NO validation — it trusts that the Spine has already
schema-checked and limit-checked every command. Nothing above the Spine may
call a Hand directly.
"""

from abc import ABC, abstractmethod


class HandInterface(ABC):
    # --- motion primitives (the Spine's dispatch targets) ---

    @abstractmethod
    def walk(self, heading_deg: float, steps: int, speed: float) -> dict:
        """Walk `steps` steps toward `heading_deg` at `speed`. Returns a result dict."""

    @abstractmethod
    def turn(self, heading_deg: float) -> dict:
        """Rotate in place by `heading_deg` (positive = counterclockwise)."""

    @abstractmethod
    def look(self, pan_deg: float, tilt_deg: float) -> dict:
        """Point the pan/tilt head."""

    @abstractmethod
    def posture(self, stance: str) -> dict:
        """Assume a body stance: normal | high | low."""

    @abstractmethod
    def stop(self) -> dict:
        """Immediately halt all locomotion. Must be safe to call at any time."""

    def idle(self) -> dict:
        """No-op tick. Default implementation is fine for all hands."""
        return {"status": "idle"}

    @abstractmethod
    def torque_off(self) -> None:
        """Dead-man: cut servo torque. Must be safe to call at any time."""

    # --- sensors ---

    @abstractmethod
    def sonar_cm(self) -> float:
        """Current ultrasonic range reading in cm."""

    @abstractmethod
    def battery_v(self) -> float:
        """Current battery rail voltage."""

    @abstractmethod
    def joint_angles(self) -> dict:
        """Last commanded joint/head angles."""
