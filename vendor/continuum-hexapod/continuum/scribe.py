"""Scribe — the sole writer to the Continuum store.

Validates every memory_op (field whitelist per table, required keys,
confidence rules, dedupe on upsert) and either commits it or drops it with a
reason. The Brain never writes: its memory_ops travel through the Spine to
here, and its recall path uses a read-only connection.
"""

import json
import logging
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path

from .store import init_db

log = logging.getLogger("scribe")

# Writable-by-memory_ops tables and their permitted fields. `id` is
# deliberately absent: rows are addressed by label/name, never raw ids.
TABLE_FIELDS = {
    "places":  {"label", "descriptor", "links", "last_seen", "confidence"},
    "objects": {"label", "descriptor", "last_place", "last_seen", "notes"},
    "skills":  {"name", "context", "params", "success_rate", "uses"},
}

# The natural key the Scribe dedupes upserts on, per table.
TABLE_KEY = {"places": "label", "objects": "label", "skills": "name"}

# Fields that must be a probability in [0, 1] if present.
UNIT_INTERVAL_FIELDS = {"confidence", "success_rate"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Scribe:
    def __init__(self, db_path: str | Path):
        self.conn: sqlite3.Connection = init_db(db_path)
        # Sole-writer guarantee: every write is serialized behind this lock,
        # so the shared connection is safe across the daemon's threadpool.
        self._lock = threading.Lock()

    # --- memory_ops (from Spine /act) ---

    def apply(self, memory_ops) -> list[dict]:
        """Validate and commit each op; invalid ops are dropped (logged),
        never partially applied. Returns one result dict per op, in order."""
        results = []
        for op in memory_ops:
            # Accept the pydantic MemoryOp model or a plain dict.
            op_d = op.model_dump() if hasattr(op, "model_dump") else dict(op)
            err = self._validate_op(op_d)
            if err:
                log.warning("dropped memory_op %s: %s", op_d, err)
                results.append({"committed": False, "error": err})
                continue
            with self._lock:
                row_id = self._commit_op(op_d)
            results.append({"committed": True, "table": op_d["table"], "id": row_id})
        return results

    def _validate_op(self, op: dict) -> str | None:
        kind = op.get("op")
        if kind not in ("upsert", "append"):
            return f"unknown op {kind!r}"
        table = op.get("table")
        if table not in TABLE_FIELDS:
            return f"table {table!r} is not writable via memory_ops"
        data = op.get("data")
        if not isinstance(data, dict) or not data:
            return "data must be a non-empty object"
        unknown = set(data) - TABLE_FIELDS[table]
        if unknown:
            return f"fields not in {table} schema: {sorted(unknown)}"
        key = TABLE_KEY[table]
        if not isinstance(data.get(key), str) or not data.get(key, "").strip():
            return f"{table} op requires non-empty '{key}'"
        for field in UNIT_INTERVAL_FIELDS & set(data):
            v = data[field]
            if not isinstance(v, (int, float)) or not (0.0 <= v <= 1.0):
                return f"{field} must be a number in [0, 1], got {v!r}"
        return None

    def _commit_op(self, op: dict) -> int:
        table, data = op["table"], dict(op["data"])
        key = TABLE_KEY[table]
        if "last_seen" in TABLE_FIELDS[table]:
            data.setdefault("last_seen", _now())
        # Serialize structured payloads (links/params) for storage.
        for field in ("links", "params"):
            if field in data and not isinstance(data[field], (str, type(None))):
                data[field] = json.dumps(data[field])

        existing = self.conn.execute(
            f"SELECT id FROM {table} WHERE {key} = ?", (data[key],)
        ).fetchone()

        if op["op"] == "upsert" and existing:
            sets = ", ".join(f"{f} = ?" for f in data)
            self.conn.execute(
                f"UPDATE {table} SET {sets} WHERE id = ?",
                (*data.values(), existing["id"]),
            )
            row_id = existing["id"]
        else:
            cols = ", ".join(data)
            marks = ", ".join("?" for _ in data)
            cur = self.conn.execute(
                f"INSERT INTO {table} ({cols}) VALUES ({marks})",
                tuple(data.values()),
            )
            row_id = cur.lastrowid
        self.conn.commit()
        return row_id

    # --- episode log (called by the Brain loop via its Scribe handle) ---

    def log_episode(self, session: str, goal: str, action: dict,
                    expected: str, actual: str, surprise: bool) -> int:
        with self._lock:
            return self._log_episode_locked(session, goal, action, expected,
                                            actual, surprise)

    def _log_episode_locked(self, session, goal, action, expected, actual,
                            surprise) -> int:
        cur = self.conn.execute(
            "INSERT INTO episodes (session, ts, goal, action, expected, actual, surprise) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (session, _now(), goal, json.dumps(action), expected, actual,
             1 if surprise else 0),
        )
        self.conn.commit()
        return cur.lastrowid

    def close(self) -> None:
        self.conn.close()
