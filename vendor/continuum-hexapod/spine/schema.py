"""Action schema — the Brain↔Spine return contract as pydantic models.

Anything that does not parse into these models exactly is rejected before it
gets near a motor. extra="forbid" everywhere: unknown fields are a schema
violation, not something to silently drop. Never "best effort" a motor command.
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

ACTION_NAMES = ("walk", "turn", "look", "posture", "stop", "idle")


class ActionParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    heading_deg: Optional[float] = None
    steps: Optional[int] = None
    speed: Optional[float] = None
    pan_deg: Optional[float] = None
    tilt_deg: Optional[float] = None
    stance: Optional[str] = None


class MemoryOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["upsert", "append"]
    table: Literal["places", "objects", "skills"]
    data: dict


class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["walk", "turn", "look", "posture", "stop", "idle"]
    params: ActionParams = Field(default_factory=ActionParams)
    rationale: str = ""
    expected_outcome: str = ""
    memory_ops: list[MemoryOp] = Field(default_factory=list)
