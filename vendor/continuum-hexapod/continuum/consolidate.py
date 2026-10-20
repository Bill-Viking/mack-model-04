"""Consolidation — the dreaming pass (Phase 5, end of session).

Reads the session's episodes and:
1. Mechanically updates the skills table: per-action success rate and use
   counts (no model needed).
2. Optionally asks a cheap model to propose promotions (repeated observations
   -> places/objects rows). The model's proposals are ordinary memory_ops and
   flow through the Scribe's validation like everything else — consolidation
   gets no special write path.
3. Writes a session summary episode row.

Run manually or via cron after a session: python -m continuum.consolidate
The model_fn is injectable: tests use a fake; the real one wraps the Claude
API (PLANNING/cheap model, one call per session).
"""

import json
import logging
from typing import Callable, Optional

from .scribe import Scribe

log = logging.getLogger("consolidate")

SUMMARY_GOAL = "__session_summary__"

CONSOLIDATION_PROMPT = """You are the consolidation pass for a hexapod robot's memory.
Below are this session's episodes (goal, action, expected, actual, surprise).
Propose memory_ops that promote repeated observations into durable memory:
places seen more than once, objects confirmed across episodes. Respond ONLY
with a JSON array of memory_ops:
[{"op": "upsert", "table": "places"|"objects"|"skills", "data": {...}}]
Respond with [] if nothing recurs. Do not invent observations.

EPISODES:
"""


def _episode_rows(scribe: Scribe, session: str) -> list:
    return scribe.conn.execute(
        "SELECT * FROM episodes WHERE session = ? AND goal != ? ORDER BY id",
        (session, SUMMARY_GOAL)).fetchall()


def _update_skills(scribe: Scribe, rows) -> dict:
    """Per-action success stats -> skills table (mechanical, no model)."""
    stats: dict[str, list[int]] = {}   # action -> [successes, uses]
    for row in rows:
        try:
            action_name = json.loads(row["action"]).get("action", "unknown")
        except (json.JSONDecodeError, TypeError):
            continue
        s = stats.setdefault(action_name, [0, 0])
        s[1] += 1
        if not row["surprise"]:
            s[0] += 1
    for name, (ok, uses) in stats.items():
        scribe.apply([{"op": "upsert", "table": "skills",
                       "data": {"name": name, "context": "primitive action",
                                "success_rate": round(ok / uses, 3),
                                "uses": uses}}])
    return {k: {"success_rate": v[0] / v[1], "uses": v[1]}
            for k, v in stats.items()}


def consolidate(scribe: Scribe, session: str,
                model_fn: Optional[Callable[[str], str]] = None) -> dict:
    """Run the dreaming pass for one session. Returns a report dict.
    model_fn: prompt -> model text (a JSON array of memory_ops), or None to
    run the mechanical part only."""
    rows = _episode_rows(scribe, session)
    if not rows:
        return {"session": session, "episodes": 0, "skills": {},
                "promotions": [], "summary_id": None}

    skills = _update_skills(scribe, rows)

    promotions = []
    if model_fn is not None:
        episodes_text = "\n".join(
            f"- goal={r['goal']} action={r['action']} expected={r['expected']} "
            f"actual={r['actual']} surprise={bool(r['surprise'])}" for r in rows)
        try:
            raw = model_fn(CONSOLIDATION_PROMPT + episodes_text)
            ops = json.loads(raw.strip())
            if isinstance(ops, list):
                # Scribe validates each op — invalid proposals drop harmlessly.
                promotions = scribe.apply(ops)
            else:
                log.warning("consolidation model returned non-list; ignored")
        except (json.JSONDecodeError, Exception) as e:  # model output is untrusted
            log.warning("consolidation model pass failed, skipping: %s", e)

    surprises = sum(1 for r in rows if r["surprise"])
    summary = (f"{len(rows)} episodes, {surprises} surprises; "
               f"skills: {json.dumps(skills, sort_keys=True)}; "
               f"promotions committed: "
               f"{sum(1 for p in promotions if p.get('committed'))}")
    summary_id = scribe.log_episode(session=session, goal=SUMMARY_GOAL,
                                    action={}, expected="", actual=summary,
                                    surprise=False)
    return {"session": session, "episodes": len(rows), "skills": skills,
            "promotions": promotions, "summary_id": summary_id}


def claude_model_fn(prompt: str) -> str:
    """Real model_fn: one cheap call. Requires ANTHROPIC_API_KEY in env."""
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-haiku-4-5",          # cheap: this is bookkeeping, not planning
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}])
    return next((b.text for b in msg.content if b.type == "text"), "[]")


if __name__ == "__main__":
    import sys
    from .store import DEFAULT_DB_PATH

    logging.basicConfig(level=logging.INFO)
    session = sys.argv[1] if len(sys.argv) > 1 else "dev"
    use_model = "--with-model" in sys.argv
    scribe = Scribe(DEFAULT_DB_PATH)
    report = consolidate(scribe, session,
                         model_fn=claude_model_fn if use_model else None)
    print(json.dumps(report, indent=2, default=str))
