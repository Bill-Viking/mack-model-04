"""Consolidation (dreaming pass) tests — fake model_fn, real Scribe."""

import json

from continuum.consolidate import SUMMARY_GOAL, consolidate


def log_walk(scribe, session="s1", surprise=False):
    scribe.log_episode(session=session, goal="explore",
                       action={"action": "walk", "params": {"steps": 2}},
                       expected="moves", actual="moved", surprise=surprise)


class TestMechanicalPass:
    def test_skill_stats_from_episodes(self, scribe):
        log_walk(scribe)
        log_walk(scribe)
        log_walk(scribe, surprise=True)
        report = consolidate(scribe, "s1")
        assert report["episodes"] == 3
        row = scribe.conn.execute(
            "SELECT * FROM skills WHERE name='walk'").fetchone()
        assert row["uses"] == 3
        assert abs(row["success_rate"] - 2 / 3) < 0.01

    def test_summary_row_written(self, scribe):
        log_walk(scribe)
        report = consolidate(scribe, "s1")
        row = scribe.conn.execute(
            "SELECT * FROM episodes WHERE goal = ?", (SUMMARY_GOAL,)).fetchone()
        assert row is not None and "1 episodes" in row["actual"]
        assert report["summary_id"] == row["id"]

    def test_empty_session_is_noop(self, scribe):
        report = consolidate(scribe, "nothing-here")
        assert report["episodes"] == 0 and report["summary_id"] is None

    def test_rerun_does_not_double_count(self, scribe):
        # Summary rows are excluded from the episode scan on re-run.
        log_walk(scribe)
        consolidate(scribe, "s1")
        report = consolidate(scribe, "s1")
        assert report["episodes"] == 1


class TestModelPass:
    def test_valid_promotions_land_via_scribe(self, scribe):
        log_walk(scribe)
        ops = [{"op": "upsert", "table": "places",
                "data": {"label": "kitchen", "confidence": 0.8}}]
        report = consolidate(scribe, "s1", model_fn=lambda p: json.dumps(ops))
        assert report["promotions"][0]["committed"] is True
        assert scribe.conn.execute(
            "SELECT COUNT(*) FROM places").fetchone()[0] == 1

    def test_invalid_promotions_dropped_by_scribe(self, scribe):
        log_walk(scribe)
        ops = [{"op": "upsert", "table": "episodes",   # not writable
                "data": {"goal": "sneaky"}},
               {"op": "upsert", "table": "places",
                "data": {"label": "hall", "confidence": 5.0}}]  # out of range
        report = consolidate(scribe, "s1", model_fn=lambda p: json.dumps(ops))
        assert all(p["committed"] is False for p in report["promotions"])

    def test_garbage_model_output_skipped(self, scribe):
        log_walk(scribe)
        report = consolidate(scribe, "s1",
                             model_fn=lambda p: "I think the kitchen is nice")
        assert report["promotions"] == []
        # Mechanical pass still ran.
        assert scribe.conn.execute(
            "SELECT COUNT(*) FROM skills").fetchone()[0] == 1

    def test_prompt_contains_episodes(self, scribe):
        log_walk(scribe)
        seen = {}
        consolidate(scribe, "s1",
                    model_fn=lambda p: seen.update(prompt=p) or "[]")
        assert "goal=explore" in seen["prompt"]
