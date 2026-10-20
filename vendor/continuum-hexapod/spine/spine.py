"""Spine daemon — Phase 3.

A single service wrapping the Hand behind a validated action API. All safety
logic (schema, limits, reflexes, watchdog, battery gate) is local to this
process and never depends on the network or the Brain.

The core logic lives in the Spine class, framework-free, so tests exercise it
directly with a MockHand. create_app() wraps it in FastAPI for the real
daemon (uvicorn, localhost only).
"""

import logging
import time
from pathlib import Path

from pydantic import ValidationError

from hand.hand_interface import HandInterface

from .limits import load_limits, validate
from .schema import Action
from .watchdog import Watchdog

log = logging.getLogger("spine")

MOTION_ACTIONS = {"walk", "turn", "posture"}  # gated by the battery cutoff


class Spine:
    def __init__(self, hand: HandInterface, limits: dict, scribe=None,
                 clock=time.monotonic):
        self.hand = hand
        self.limits = limits
        self.scribe = scribe
        self.clock = clock
        self.started_at = clock()
        self.last_result: dict | None = None
        # Mid-walk reflex: hands that execute multi-cycle walks (Freenove, Sim)
        # expose a cycle_hook called between gait cycles; the Spine owns it and
        # wires its sonar check so a walk aborts INSIDE the command, not just at
        # the pre/post checks. (MockHand's walks are instantaneous — pre/post
        # checks cover it.) Found the hard way in sim: without this, a
        # multi-step walk crosses the whole 12 cm envelope and bumps the wall.
        if hasattr(hand, "cycle_hook"):
            hand.cycle_hook = self._walk_may_continue
        self.watchdog = Watchdog(
            timeout_s=limits["watchdog"]["timeout_s"],
            on_timeout=self._watchdog_timeout,
            clock=clock,
        )

    # --- safety reactions ---

    def _walk_may_continue(self) -> bool:
        """cycle_hook body: keep walking only while the sonar envelope is clear."""
        return self.hand.sonar_cm() >= self.limits["reflex"]["sonar_stop_cm"]

    def _watchdog_timeout(self) -> None:
        log.warning("watchdog timeout: Brain silent mid-task -> posture(safe), stop")
        self.hand.stop()
        self.hand.posture("normal")   # safe stance
        self.last_result = {"interrupted": "watchdog_timeout"}

    # --- API surface ---

    def handle_act(self, payload: dict) -> dict:
        """Validate and dispatch one action. Malformed/out-of-limit -> reject,
        log, no-op; the motor layer is never touched on a rejection."""
        self.watchdog.touch()

        try:
            action = Action.model_validate(payload)
        except ValidationError as e:
            log.warning("rejected malformed action: %s", e)
            return {"ok": False, "error": f"schema violation: {e.errors()}"}

        err = validate(action, self.limits)
        if err:
            log.warning("rejected out-of-limit action %s: %s", action.action, err)
            return {"ok": False, "error": err}

        # Battery gate: below cutoff the robot sits and refuses all motion.
        battery = self.hand.battery_v()
        if action.action in MOTION_ACTIONS and battery < self.limits["battery"]["cutoff_v"]:
            log.warning("battery %.2fV below cutoff — sit and refuse", battery)
            self.hand.stop()
            self.hand.posture("low")
            return {"ok": False,
                    "error": f"battery {battery:.2f}V below cutoff "
                             f"{self.limits['battery']['cutoff_v']}V — sitting, refusing motion"}

        result = self._dispatch(action)
        self.last_result = result

        memory_results = []
        if action.memory_ops:
            if self.scribe is None:
                log.warning("memory_ops received but no Scribe attached — dropped")
                memory_results = [{"committed": False, "error": "no scribe"}
                                  for _ in action.memory_ops]
            else:
                # Memory writes go through the Scribe, never direct.
                memory_results = self.scribe.apply(action.memory_ops)

        return {"ok": True, "result": result, "memory_results": memory_results}

    def _dispatch(self, action: Action) -> dict:
        p = action.params
        if action.action == "walk":
            # Reflex: obstacle inside sonar_stop_cm -> immediate stop.
            if self.hand.sonar_cm() < self.limits["reflex"]["sonar_stop_cm"]:
                self.hand.stop()
                return {"interrupted": "obstacle", "sonar_cm": self.hand.sonar_cm()}
            self.watchdog.set_active(True)
            result = self.hand.walk(p.heading_deg, p.steps, p.speed)
            # Post-step reflex check (the mock walks instantaneously; the real
            # adapter will interleave this per gait cycle).
            if self.hand.sonar_cm() < self.limits["reflex"]["sonar_stop_cm"]:
                self.hand.stop()
                return {"interrupted": "obstacle", "sonar_cm": self.hand.sonar_cm(),
                        "partial": result}
            return result
        if action.action == "turn":
            self.watchdog.set_active(True)
            return self.hand.turn(p.heading_deg)
        if action.action == "look":
            return self.hand.look(p.pan_deg, p.tilt_deg)
        if action.action == "posture":
            return self.hand.posture(p.stance)
        if action.action == "stop":
            self.watchdog.set_active(False)
            return self.hand.stop()
        if action.action == "idle":
            self.watchdog.set_active(False)
            return self.hand.idle()
        raise AssertionError(f"unreachable action {action.action}")  # schema guards this

    def handle_state(self) -> dict:
        battery = self.hand.battery_v()
        return {
            "joint_angles": self.hand.joint_angles(),
            "last_result": self.last_result,
            "sonar_cm": self.hand.sonar_cm(),
            "battery_v": battery,
            "battery_warn": battery < self.limits["battery"]["warn_v"],
            "battery_cutoff": battery < self.limits["battery"]["cutoff_v"],
            "uptime_s": self.clock() - self.started_at,
            "watchdog_fired": self.watchdog.fired,
        }


def create_app(spine: Spine):
    """Wrap a Spine in FastAPI. Routes are thin: all logic is in Spine."""
    from contextlib import asynccontextmanager

    from fastapi import Body, FastAPI

    @asynccontextmanager
    async def lifespan(app):
        spine.watchdog.run()
        yield
        spine.watchdog.shutdown()

    app = FastAPI(title="continuum-hexapod spine", lifespan=lifespan)

    @app.post("/act")
    def act(payload: dict = Body(...)):
        return spine.handle_act(payload)

    @app.get("/state")
    def state():
        return spine.handle_state()

    return app


def build_default_app():
    """Entry point for uvicorn. Uses MockHand until the hardware adapter
    exists (swap to the Freenove adapter in Phase 2.5)."""
    logging.basicConfig(level=logging.INFO)
    from continuum.scribe import Scribe
    from continuum.store import DEFAULT_DB_PATH
    from hand.mock_hand import MockHand

    root = Path(__file__).resolve().parent.parent
    limits = load_limits(root / "limits.yaml")
    spine = Spine(hand=MockHand(), limits=limits, scribe=Scribe(DEFAULT_DB_PATH))
    return create_app(spine)


if __name__ == "__main__":
    # Run from the repo root as: python -m spine.spine
    import uvicorn
    # localhost only — the Spine is never exposed off-box.
    uvicorn.run(build_default_app(), host="127.0.0.1", port=8080)
