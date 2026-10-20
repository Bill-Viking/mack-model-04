"""Continuum store — Phase 5. SQLite at ~/continuum/continuum.db
(user-owned, rsync-able, MYTHOS pattern).

Write access is the Scribe's alone (scribe.py). Everything else — the Brain's
recall, debugging, analytics — opens the database read-only via
open_readonly(); SQLite itself then refuses writes on that connection.
"""

import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / "continuum" / "continuum.db"

# Schema verbatim from CONTINUUM_HEXAPOD_BUILD.md, Phase 5.
SCHEMA = """
CREATE TABLE IF NOT EXISTS places   (id INTEGER PRIMARY KEY, label TEXT, descriptor TEXT,
                                     links TEXT, last_seen TEXT, confidence REAL);
CREATE TABLE IF NOT EXISTS objects  (id INTEGER PRIMARY KEY, label TEXT, descriptor TEXT,
                                     last_place INTEGER, last_seen TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS skills   (id INTEGER PRIMARY KEY, name TEXT, context TEXT,
                                     params TEXT, success_rate REAL, uses INTEGER);
CREATE TABLE IF NOT EXISTS episodes (id INTEGER PRIMARY KEY, session TEXT, ts TEXT, goal TEXT,
                                     action TEXT, expected TEXT, actual TEXT, surprise INTEGER);
"""


def init_db(db_path: str | Path) -> sqlite3.Connection:
    """Create/open the store read-write and ensure the schema exists.
    Only the Scribe should hold the connection this returns."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    # check_same_thread=False: the daemon serves requests from a threadpool.
    # Safe because the Scribe serializes all writes behind its own lock.
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def open_readonly(db_path: str | Path) -> sqlite3.Connection:
    """Read-only connection (SQLite URI mode=ro). Any write attempt raises
    sqlite3.OperationalError — this is what the Brain's recall uses."""
    conn = sqlite3.connect(f"file:{Path(db_path)}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn
