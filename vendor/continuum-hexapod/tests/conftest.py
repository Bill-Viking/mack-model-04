import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from continuum.scribe import Scribe          # noqa: E402
from hand.mock_hand import MockHand          # noqa: E402
from spine.limits import load_limits         # noqa: E402
from spine.spine import Spine                # noqa: E402


class FakeClock:
    """Manually advanced monotonic clock for watchdog tests."""
    def __init__(self):
        self.t = 0.0

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


@pytest.fixture
def limits():
    return load_limits(ROOT / "limits.yaml")


@pytest.fixture
def hand():
    return MockHand()


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "continuum.db"


@pytest.fixture
def scribe(db_path):
    s = Scribe(db_path)
    yield s
    s.close()


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def spine(hand, limits, scribe, clock):
    return Spine(hand=hand, limits=limits, scribe=scribe, clock=clock)


def act(spine, action, params=None, **extra):
    """Build and submit a well-formed /act payload."""
    payload = {"action": action, "params": params or {},
               "rationale": "test", "expected_outcome": "test", **extra}
    return spine.handle_act(payload)
