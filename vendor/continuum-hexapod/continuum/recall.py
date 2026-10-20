"""recall(state, goal) — the Brain's read-only window into the Continuum.

Pulls the top-k places/objects/skills by naive relevance (token overlap with
the goal, weighted by confidence/success where available) and formats them as
a compact context block for the system prompt. Opens the store read-only:
this code path physically cannot write.
"""

import re
from pathlib import Path

from .store import DEFAULT_DB_PATH, open_readonly

_WORD = re.compile(r"[a-z0-9]+")


def _tokens(text: str | None) -> set[str]:
    return set(_WORD.findall((text or "").lower()))


def _score(goal_tokens: set[str], *fields: str | None, weight: float = 1.0) -> float:
    row_tokens = set()
    for f in fields:
        row_tokens |= _tokens(f)
    if not row_tokens:
        return 0.0
    return len(goal_tokens & row_tokens) * weight


def recall(state: dict, goal: str, db_path: str | Path = DEFAULT_DB_PATH,
           k: int = 5) -> str:
    """Return a compact text block of the k most goal-relevant rows per table.
    `state` is the Spine /state snapshot (reserved for place-estimation v1)."""
    goal_tokens = _tokens(goal)
    conn = open_readonly(db_path)
    try:
        sections = []

        rows = conn.execute("SELECT * FROM places").fetchall()
        scored = sorted(rows, key=lambda r: (-_score(
            goal_tokens, r["label"], r["descriptor"],
            weight=(r["confidence"] or 0.5) + 0.5), -(r["confidence"] or 0)))
        if scored:
            sections.append("PLACES:\n" + "\n".join(
                f"- {r['label']}: {r['descriptor']} (confidence {r['confidence']}, "
                f"last seen {r['last_seen']})" for r in scored[:k]))

        rows = conn.execute("SELECT * FROM objects").fetchall()
        scored = sorted(rows, key=lambda r: -_score(
            goal_tokens, r["label"], r["descriptor"], r["notes"]))
        if scored:
            sections.append("OBJECTS:\n" + "\n".join(
                f"- {r['label']}: {r['descriptor']} (last place id {r['last_place']}, "
                f"last seen {r['last_seen']})" for r in scored[:k]))

        rows = conn.execute("SELECT * FROM skills").fetchall()
        scored = sorted(rows, key=lambda r: (-_score(
            goal_tokens, r["name"], r["context"],
            weight=(r["success_rate"] or 0.5) + 0.5), -(r["uses"] or 0)))
        if scored:
            sections.append("SKILLS:\n" + "\n".join(
                f"- {r['name']} [{r['context']}] params={r['params']} "
                f"(success {r['success_rate']}, uses {r['uses']})" for r in scored[:k]))

        if not sections:
            return "MEMORY: (empty — first session)"
        return "MEMORY RECALL (top matches for goal):\n" + "\n\n".join(sections)
    finally:
        conn.close()
