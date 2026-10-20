"""Continuum store invariants: memory writes land only through the Scribe;
invalid ops are dropped; the Brain's recall path is physically read-only."""

import sqlite3

import pytest

from continuum.recall import recall
from continuum.store import open_readonly
from tests.conftest import act


def count(scribe, table):
    return scribe.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


class TestWritesOnlyThroughScribe:
    def test_memory_ops_via_act_land_in_store(self, spine, scribe):
        r = act(spine, "stop", memory_ops=[
            {"op": "upsert", "table": "objects",
             "data": {"label": "red mug", "descriptor": "ceramic mug on floor"}}])
        assert r["ok"] is True
        assert r["memory_results"] == [
            {"committed": True, "table": "objects", "id": 1}]
        assert count(scribe, "objects") == 1

    def test_rejected_action_writes_nothing(self, spine, scribe):
        # Out-of-limit action carrying valid memory_ops: nothing may land.
        r = act(spine, "walk", {"heading_deg": 0, "steps": 99, "speed": 0.5},
                memory_ops=[{"op": "upsert", "table": "objects",
                             "data": {"label": "ghost object"}}])
        assert r["ok"] is False
        assert count(scribe, "objects") == 0

    def test_recall_connection_cannot_write(self, scribe, db_path):
        ro = open_readonly(db_path)
        with pytest.raises(sqlite3.OperationalError):
            ro.execute("INSERT INTO objects (label) VALUES ('smuggled')")
        ro.close()
        assert count(scribe, "objects") == 0

    def test_episodes_land_via_scribe(self, scribe):
        scribe.log_episode("s1", "explore", {"action": "walk"},
                           "moves forward", "moved forward", surprise=False)
        row = scribe.conn.execute("SELECT * FROM episodes").fetchone()
        assert row["goal"] == "explore" and row["surprise"] == 0


class TestScribeValidation:
    def test_bad_table_dropped(self, scribe):
        res = scribe.apply([{"op": "upsert", "table": "episodes",
                             "data": {"goal": "sneaky direct episode"}}])
        assert res[0]["committed"] is False and "not writable" in res[0]["error"]

    def test_unknown_field_dropped(self, scribe):
        res = scribe.apply([{"op": "upsert", "table": "objects",
                             "data": {"label": "mug", "weight_kg": 0.3}}])
        assert res[0]["committed"] is False and "not in objects schema" in res[0]["error"]
        assert count(scribe, "objects") == 0

    def test_confidence_out_of_range_dropped(self, scribe):
        res = scribe.apply([{"op": "upsert", "table": "places",
                             "data": {"label": "kitchen", "confidence": 1.7}}])
        assert res[0]["committed"] is False and "confidence" in res[0]["error"]

    def test_missing_key_dropped(self, scribe):
        res = scribe.apply([{"op": "upsert", "table": "places",
                             "data": {"descriptor": "a room with no name"}}])
        assert res[0]["committed"] is False and "label" in res[0]["error"]

    def test_upsert_dedupes_by_label(self, scribe):
        scribe.apply([{"op": "upsert", "table": "places",
                       "data": {"label": "kitchen", "confidence": 0.5}}])
        scribe.apply([{"op": "upsert", "table": "places",
                       "data": {"label": "kitchen", "confidence": 0.9,
                                "descriptor": "tile floor, north wall"}}])
        assert count(scribe, "places") == 1
        row = scribe.conn.execute("SELECT * FROM places").fetchone()
        assert row["confidence"] == 0.9 and "tile floor" in row["descriptor"]

    def test_mixed_batch_partial_commit(self, scribe):
        res = scribe.apply([
            {"op": "upsert", "table": "objects", "data": {"label": "ball"}},
            {"op": "upsert", "table": "objects", "data": {"nope": True}},
        ])
        assert [r["committed"] for r in res] == [True, False]
        assert count(scribe, "objects") == 1


class TestRecall:
    def test_recall_ranks_relevant_rows(self, scribe, db_path):
        scribe.apply([
            {"op": "upsert", "table": "places",
             "data": {"label": "kitchen", "descriptor": "tile floor near fridge",
                      "confidence": 0.9}},
            {"op": "upsert", "table": "places",
             "data": {"label": "hallway", "descriptor": "long corridor",
                      "confidence": 0.9}},
            {"op": "upsert", "table": "objects",
             "data": {"label": "red mug", "descriptor": "mug seen in kitchen"}},
        ])
        block = recall({}, "find the mug in the kitchen", db_path=db_path, k=2)
        assert "kitchen" in block and "red mug" in block

    def test_recall_empty_store(self, scribe, db_path):
        assert "empty" in recall({}, "anything", db_path=db_path)
