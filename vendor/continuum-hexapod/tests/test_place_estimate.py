"""Place estimation v1 tests — dead reckoning + confidence decay."""

import pytest

from continuum.place_estimate import PlaceEstimate


class TestPlaceEstimate:
    def test_unknown_until_confirmed(self):
        pe = PlaceEstimate()
        assert "unknown" in pe.as_context()

    def test_confirm_resets_reckoning(self):
        pe = PlaceEstimate()
        pe.apply_action("walk", {"heading_deg": 0, "steps": 4})
        pe.confirm("kitchen")
        assert pe.place_label == "kitchen"
        assert pe.displacement_steps == 0
        assert pe.confidence == 0.9

    def test_walk_accumulates_displacement(self):
        pe = PlaceEstimate()
        pe.confirm("kitchen")
        pe.apply_action("walk", {"heading_deg": 0, "steps": 3})
        assert pe.dy == pytest.approx(3)
        assert pe.dx == pytest.approx(0)
        pe.apply_action("walk", {"heading_deg": 90, "steps": 2})
        assert pe.dx == pytest.approx(2)
        assert pe.displacement_steps == pytest.approx((9 + 4) ** 0.5)

    def test_turn_changes_heading_for_later_walks(self):
        pe = PlaceEstimate()
        pe.confirm("kitchen")
        pe.apply_action("turn", {"heading_deg": 90})
        pe.apply_action("walk", {"heading_deg": 0, "steps": 2})
        assert pe.dx == pytest.approx(2)   # walked "forward" after turning 90
        assert pe.dy == pytest.approx(0, abs=1e-9)

    def test_confidence_decays_with_motion(self):
        pe = PlaceEstimate()
        pe.confirm("kitchen")
        c0 = pe.confidence
        pe.apply_action("walk", {"heading_deg": 0, "steps": 5})
        assert pe.confidence < c0
        assert "kitchen" in pe.as_context()
