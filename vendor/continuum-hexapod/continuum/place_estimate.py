"""Place estimation v1 — last confirmed landmark + dead reckoning.

(Open item from the build doc.) The Brain confirms a landmark by naming a
known place; between confirmations we dead-reckon from walk/turn actions and
decay confidence with distance moved. The estimate feeds recall() so memory
retrieval can weight rows near the robot's believed location.

Deliberately crude: no SLAM, no map. Good enough to bias recall and to stamp
`last_place` on observed objects. Replace when Phase 6 rung 3 shows its limits.
"""

import math
from dataclasses import dataclass, field

# Confidence decays by this factor per commanded stride/turn unit of motion.
DECAY_PER_STEP = 0.9
DECAY_PER_TURN = 0.98


@dataclass
class PlaceEstimate:
    place_label: str | None = None      # last confirmed landmark
    confidence: float = 0.0
    # Dead-reckoned displacement since confirmation, in "step units" — the
    # commanded stride count, not measured distance (no odometry on this rig).
    dx: float = 0.0
    dy: float = 0.0
    heading_deg: float = 0.0

    def confirm(self, place_label: str, confidence: float = 0.9) -> None:
        """The Brain recognized a known place — reset dead reckoning."""
        self.place_label = place_label
        self.confidence = max(0.0, min(1.0, confidence))
        self.dx = self.dy = 0.0

    def apply_action(self, action: str, params: dict) -> None:
        """Fold one executed action into the estimate."""
        if action == "walk":
            steps = params.get("steps") or 0
            heading = (self.heading_deg + (params.get("heading_deg") or 0))
            rad = math.radians(heading)
            self.dx += steps * math.sin(rad)
            self.dy += steps * math.cos(rad)
            self.confidence *= DECAY_PER_STEP ** steps
        elif action == "turn":
            self.heading_deg = (self.heading_deg
                                + (params.get("heading_deg") or 0)) % 360
            self.confidence *= DECAY_PER_TURN

    @property
    def displacement_steps(self) -> float:
        return math.hypot(self.dx, self.dy)

    def as_context(self) -> str:
        """Compact block for the recall/context path."""
        if self.place_label is None:
            return "PLACE ESTIMATE: unknown (no landmark confirmed yet)"
        return (f"PLACE ESTIMATE: near '{self.place_label}' "
                f"(confidence {self.confidence:.2f}), "
                f"~{self.displacement_steps:.1f} steps away at heading "
                f"{self.heading_deg:.0f}deg since confirmation")
