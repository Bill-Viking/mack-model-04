"""Brain loop — Phase 4.

One tick: capture frame -> GET /state -> recall() -> Claude -> POST /act ->
log episode. Event-driven, not continuous: a tick fires on action completion,
reflex interrupt, operator command, or timeout — dozens of calls per session,
not thousands.

Safety note: nothing here may ever enforce (or relax) a limit — limits,
reflexes, and the watchdog are Spine-local by design. The Brain proposes;
the Spine disposes. The contract prompt renders current bounds from
limits.yaml at runtime purely as guidance; the Spine's copy decides.

Runs on the Mac during development (HTTPSpineClient over Wi-Fi), on the Pi
later (SPINE_URL=http://127.0.0.1:8080 — config change only). API key comes
from the environment (ANTHROPIC_API_KEY / keychain); never committed, never
logged.
"""

import json
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import yaml

from continuum.recall import recall
from continuum.store import DEFAULT_DB_PATH

log = logging.getLogger("brain")

ROOT = Path(__file__).resolve().parent.parent
SPINE_URL = "http://127.0.0.1:8080"

# Model split per CONTINUUM_HEXAPOD_BUILD.md: sonnet for frequent ticks,
# opus for occasional planning passes (consolidation, route planning).
TICK_MODEL = "claude-sonnet-4-6"
PLANNING_MODEL = "claude-opus-4-8"


# --- frame sources ---------------------------------------------------------

class FrameSource(ABC):
    @abstractmethod
    def capture_b64(self) -> Optional[str]:
        """Return a base64-encoded JPEG, or None if no camera is available."""


class StaticFrameSource(FrameSource):
    """Dev frame source: a fixed image file (or nothing). Lets the full loop
    run on the Mac with no camera."""

    def __init__(self, path: str | Path | None = None):
        self._b64: Optional[str] = None
        if path is not None:
            import base64
            self._b64 = base64.standard_b64encode(Path(path).read_bytes()).decode()

    def capture_b64(self) -> Optional[str]:
        return self._b64


class PiCameraFrameSource(FrameSource):
    """picamera2 -> JPEG -> b64. Hardware-dependent; wire up in Phase 4 on the Pi."""

    def capture_b64(self) -> Optional[str]:
        raise NotImplementedError("picamera2 capture requires the Pi (Phase 4)")


# --- spine clients ---------------------------------------------------------

class SpineClient(ABC):
    @abstractmethod
    def act(self, payload: dict) -> dict: ...

    @abstractmethod
    def state(self) -> dict: ...


class HTTPSpineClient(SpineClient):
    """Talks to the Spine daemon over HTTP (Mac -> Pi, or localhost on the Pi)."""

    def __init__(self, base_url: str = SPINE_URL, timeout: float = 10.0):
        import httpx
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def act(self, payload: dict) -> dict:
        return self._client.post("/act", json=payload).json()

    def state(self) -> dict:
        return self._client.get("/state").json()


class LocalSpineClient(SpineClient):
    """Wraps an in-process Spine instance — full Brain->Spine->Hand integration
    tests with no server."""

    def __init__(self, spine):
        self.spine = spine

    def act(self, payload: dict) -> dict:
        return self.spine.handle_act(payload)

    def state(self) -> dict:
        return self.spine.handle_state()


# --- contract prompt -------------------------------------------------------

def render_contract_prompt(skill_path: str | Path = ROOT / "SKILL.md",
                           limits_path: str | Path = ROOT / "limits.yaml") -> str:
    """Load SKILL.md and render {{LIMITS}} from the live limit table, so the
    numbers keep a single source of truth in limits.yaml."""
    template = Path(skill_path).read_text()
    with open(limits_path) as f:
        limits = yaml.safe_load(f)
    action_limits = {k: v for k, v in limits.items()
                     if k in ("walk", "turn", "look", "posture")}
    rendered = "\n".join(f"    {line}" for line in
                         yaml.safe_dump(action_limits, sort_keys=False).splitlines())
    return template.replace("{{LIMITS}}", rendered)


# --- strict JSON parsing ---------------------------------------------------

_FENCE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)


def parse_json_strict(text: str) -> Optional[dict]:
    """Accept exactly one JSON object (optionally in a ```json fence).
    Anything else -> None. The caller no-ops and retries; never guess."""
    text = text.strip()
    m = _FENCE.match(text)
    if m:
        text = m.group(1)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


# --- the loop --------------------------------------------------------------

class Brain:
    def __init__(self, spine: SpineClient, frame_source: FrameSource,
                 scribe=None, db_path: str | Path = DEFAULT_DB_PATH,
                 client=None, model: str = TICK_MODEL, session_id: str = "dev"):
        self.spine = spine
        self.frame_source = frame_source
        self.scribe = scribe          # for episode logging (co-located only)
        self.db_path = db_path
        self._client = client         # injectable for tests; lazy otherwise
        self.model = model
        self.session_id = session_id
        self.contract_prompt = render_contract_prompt()

    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic()
        return self._client

    def tick(self, goal: str) -> dict:
        frame = self.frame_source.capture_b64()
        state = self.spine.state()
        recall_block = recall(state, goal, db_path=self.db_path)

        content: list[dict] = []
        if frame:
            content.append({"type": "image",
                            "source": {"type": "base64",
                                       "media_type": "image/jpeg",
                                       "data": frame}})
        content.append({"type": "text",
                        "text": f"Goal: {goal}\nState: {json.dumps(state)}\n"
                                f"Respond ONLY with action JSON."})

        msg = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.contract_prompt + "\n\n" + recall_block,
            output_config={"effort": "low"},   # frequent ticks: fast and cheap
            messages=[{"role": "user", "content": content}],
        )
        text = next((b.text for b in msg.content if b.type == "text"), "")

        action = parse_json_strict(text)
        if action is None:
            # Fail -> no-op + retry next tick. Never "best effort" a motor command.
            log.warning("unparseable action from model, no-op: %.200s", text)
            return {"ok": False, "error": "unparseable model output", "retry": True}

        result = self.spine.act(action)

        if self.scribe is not None:
            surprise = (not result.get("ok")
                        or "interrupted" in (result.get("result") or {}))
            self.scribe.log_episode(
                session=self.session_id, goal=goal, action=action,
                expected=action.get("expected_outcome", ""),
                actual=json.dumps(result), surprise=surprise)
        return result


if __name__ == "__main__":
    # Dev loop against a local Spine: python -m brain.brain "<goal>" [n_ticks]
    import sys
    from continuum.scribe import Scribe

    logging.basicConfig(level=logging.INFO)
    goal = sys.argv[1] if len(sys.argv) > 1 else "describe what you see and look around"
    ticks = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    brain = Brain(spine=HTTPSpineClient(), frame_source=StaticFrameSource(),
                  scribe=Scribe(DEFAULT_DB_PATH))
    for i in range(ticks):
        print(f"tick {i}:", json.dumps(brain.tick(goal), indent=2))
