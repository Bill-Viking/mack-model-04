"""Limit table enforcement.

Loads limits.yaml and checks a schema-valid Action against it. Per-action
param policy is explicit: motion params must be provided (no silent defaults
for motor commands) and only the params that belong to an action are accepted.
Returns an error string on the first violation, or None if the action is
within limits.
"""

from pathlib import Path
from typing import Optional

import yaml

from .schema import Action

# Which params each action accepts, and which it must supply. A param that is
# allowed but not required may be omitted; a param outside the allowed set is
# a rejection even if it is within its numeric range.
PARAM_POLICY = {
    "walk":    {"required": {"heading_deg", "steps", "speed"}, "allowed": {"heading_deg", "steps", "speed"}},
    "turn":    {"required": {"heading_deg"}, "allowed": {"heading_deg"}},
    "look":    {"required": {"pan_deg", "tilt_deg"}, "allowed": {"pan_deg", "tilt_deg"}},
    "posture": {"required": {"stance"}, "allowed": {"stance"}},
    "stop":    {"required": set(), "allowed": set()},
    "idle":    {"required": set(), "allowed": set()},
}


def load_limits(path: str | Path) -> dict:
    with open(path) as f:
        limits = yaml.safe_load(f)
    if not isinstance(limits, dict):
        raise ValueError(f"limits file {path} did not parse to a mapping")
    return limits


def validate(action: Action, limits: dict) -> Optional[str]:
    """Return an error string if the action violates the limit table, else None."""
    policy = PARAM_POLICY[action.action]
    given = {k: v for k, v in action.params.model_dump().items() if v is not None}

    unknown = set(given) - policy["allowed"]
    if unknown:
        return f"params not valid for action '{action.action}': {sorted(unknown)}"

    missing = policy["required"] - set(given)
    if missing:
        return f"action '{action.action}' missing required params: {sorted(missing)}"

    table = limits.get(action.action, {})
    for name, value in given.items():
        rule = table.get(name)
        if rule is None:
            return f"no limit rule for '{action.action}.{name}' — refusing unbounded param"
        if "allowed" in rule and value not in rule["allowed"]:
            return (f"'{action.action}.{name}' value {value!r} not in "
                    f"allowed set {rule['allowed']}")
        if "min" in rule and value < rule["min"]:
            return f"'{action.action}.{name}' = {value} below min {rule['min']}"
        if "max" in rule and value > rule["max"]:
            return f"'{action.action}.{name}' = {value} above max {rule['max']}"
    return None
