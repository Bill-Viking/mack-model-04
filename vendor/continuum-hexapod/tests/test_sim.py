"""Sim world tests: geometry, sensors, Spine safety integration in the
virtual world, rendering legibility, and the full Brain loop against the sim.
The sim exists so Brain/Continuum changes can debut here — these tests are
that rung of the ladder."""

import io
import json
import math

import pytest
from PIL import Image

from brain.brain import Brain, LocalSpineClient
from sim.render import frame_jpeg, render_frame
from sim.sim_hand import SimFrameSource, SimHand
from sim.world import ROBOT_RADIUS, World, Wall, build_apartment
from spine.spine import Spine
from tests.conftest import act
from tests.test_brain import FakeClaude, action_json


@pytest.fixture
def world():
    return build_apartment(seed=42)


@pytest.fixture
def sim_hand(world):
    return SimHand(world)


@pytest.fixture
def sim_spine(sim_hand, limits, scribe, clock):
    return Spine(hand=sim_hand, limits=limits, scribe=scribe, clock=clock)


class TestWorldPhysics:
    def test_walk_moves_forward(self, world, sim_hand):
        x0, y0 = world.x, world.y
        sim_hand.walk(heading_deg=0, steps=4, speed=0.5)
        assert world.y > y0 + 0.15          # heading 0 = +y
        assert abs(world.x - x0) < 0.15     # noise stays small

    def test_turn_is_ccw_positive(self, world, sim_hand):
        sim_hand.turn(90)
        assert 70 < world.heading_deg < 110
        x0 = world.x
        sim_hand.walk(0, 4, 0.5)
        assert world.x < x0                 # CCW from north -> walking -x

    def test_walls_block_walking(self, world, sim_hand):
        world.heading_deg = 180.0           # face the south wall (0.6 m away)
        for _ in range(10):
            sim_hand.walk(0, 10, 0.8)
        assert world.y > ROBOT_RADIUS - 0.01   # never tunnels out
        assert world.collisions > 0

    def test_blocked_steps_report_advanced_count(self, world, sim_hand):
        world.x, world.y, world.heading_deg = 2.0, 0.3, 180.0  # nearly touching
        r = sim_hand.walk(0, 5, 0.5)
        assert r["steps"] == 5              # legs churned every cycle...
        assert r["advanced"] < 5            # ...but the wall won

    def test_objects_block_walking(self, world, sim_hand):
        world.x, world.y = 1.2, 1.4         # just south of the blue ball
        world.heading_deg = 0.0
        for _ in range(10):
            sim_hand.walk(0, 5, 0.5)
        ball = next(o for o in world.objects if o.label == "blue ball")
        assert math.hypot(world.x - ball.x, world.y - ball.y) \
            >= ROBOT_RADIUS + ball.radius - 0.01

    def test_battery_drains_with_motion(self, world, sim_hand):
        v0 = sim_hand.battery_v()
        sim_hand.walk(0, 10, 0.5)
        sim_hand.turn(180)
        assert sim_hand.battery_v() < v0

    def test_determinism_by_seed(self):
        a, b = build_apartment(seed=7), build_apartment(seed=7)
        ha, hb = SimHand(a), SimHand(b)
        ha.walk(0, 5, 0.5), hb.walk(0, 5, 0.5)
        assert (a.x, a.y, a.heading_deg) == (b.x, b.y, b.heading_deg)

    def test_true_place_ground_truth(self, world, sim_hand):
        assert world.true_place() == "living room"
        world.x, world.y = 2.0, 5.0
        assert world.true_place() == "kitchen"


class TestSonar:
    def test_reads_distance_to_wall(self, world):
        world.x, world.y, world.heading_deg = 2.0, 1.0, 180.0  # 1 m to south wall
        d = world.sonar_cm()
        assert 75 < d < 95      # 100 cm minus 12 cm robot radius, +/- noise

    def test_pan_swings_the_beam(self, world, sim_hand):
        world.x, world.y, world.heading_deg = 0.3, 1.5, 0.0   # west wall to the left
        ahead = sim_hand.sonar_cm()
        sim_hand.look(pan_deg=80, tilt_deg=0)                 # pan left (CCW)
        left = sim_hand.sonar_cm()
        assert left < 25 < ahead

    def test_capped_at_max_range(self):
        w = World(walls=[Wall(0, 100, 1, 100)], objects=[], places=[],
                  start=(0.5, 0, 0), seed=0)
        assert w.sonar_cm() <= 300.0


class TestSpineSafetyInSim:
    def test_spine_wires_reflex_into_cycle_hook(self, sim_spine, sim_hand):
        assert sim_hand.cycle_hook is not None
        assert sim_hand.cycle_hook() is True      # open floor: keep walking

    def test_sonar_reflex_stops_walk_before_contact(self, sim_spine, sim_hand,
                                                    world):
        """Drive at the south wall through the real Spine: the mid-walk reflex
        must abort INSIDE the multi-step command — the robot never touches the
        wall. (Regression: without cycle_hook wiring, a long walk crossed the
        whole 12 cm envelope between the pre/post checks and bumped.)"""
        world.heading_deg = 180.0
        interrupted = False
        for _ in range(20):
            r = act(sim_spine, "walk",
                    {"heading_deg": 0, "steps": 10, "speed": 0.8})
            if r["ok"] and r["result"].get("interrupted") == "obstacle":
                interrupted = True
                break
        assert interrupted
        assert world.collisions == 0    # reflex won; geometry never had to
        assert world.sonar_cm() < 15    # parked at the reflex envelope

    def test_battery_gate_fires_in_sim(self, sim_spine, sim_hand, world):
        world.battery_v = 6.5
        r = act(sim_spine, "walk", {"heading_deg": 0, "steps": 2, "speed": 0.4})
        assert r["ok"] is False and "battery" in r["error"]


class TestRenderer:
    def test_produces_valid_jpeg(self, world):
        img = Image.open(io.BytesIO(frame_jpeg(world)))
        assert img.format == "JPEG" and img.size == (320, 240)

    def test_view_changes_when_robot_turns(self, world, sim_hand):
        before = frame_jpeg(world)
        sim_hand.turn(90)
        assert frame_jpeg(world) != before

    def test_object_visible_when_faced(self, world):
        # Stand south of the blue ball, facing it: blue pixels should appear.
        world.x, world.y, world.heading_deg = 1.2, 1.2, 0.0

        def blue_fraction(img):
            raw = img.tobytes()
            px = [(raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw), 3)]
            blue = sum(1 for r, g, b in px if b > 100 and b > r + 30 and b > g + 30)
            return blue / len(px)

        facing = blue_fraction(render_frame(world))
        world.heading_deg = 180.0
        away = blue_fraction(render_frame(world))
        assert facing > 0.01
        assert facing > away * 5

    def test_tilt_moves_horizon(self, world):
        level = render_frame(world)
        up = render_frame(world, tilt_deg=40)
        # Looking up: more ceiling pixels (ceiling is the brightest surface).
        def bright(img):
            raw = img.tobytes()
            return sum(1 for i in range(0, len(raw), 3)
                       if raw[i] > 200 and raw[i + 2] > 200)
        assert bright(up) > bright(level)

    def test_frame_source_returns_b64_jpeg(self, world, sim_hand):
        b64 = SimFrameSource(world, sim_hand).capture_b64()
        import base64
        img = Image.open(io.BytesIO(base64.b64decode(b64)))
        assert img.format == "JPEG"


class TestBrainInSim:
    def test_full_loop_brain_to_sim_world(self, sim_spine, sim_hand, world,
                                          scribe, db_path):
        """Brain (fake model) -> Spine -> SimHand: a walk action moves the
        robot in the world, the frame is a real render, the episode logs."""
        walk = action_json(action="walk",
                           params={"heading_deg": 0, "steps": 3, "speed": 0.5})
        brain = Brain(spine=LocalSpineClient(sim_spine),
                      frame_source=SimFrameSource(world, sim_hand),
                      scribe=scribe, db_path=db_path,
                      client=FakeClaude([walk]), session_id="sim-test")
        y0 = world.y
        result = brain.tick("explore north")
        assert result["ok"] is True
        assert world.y > y0
        # The request carried a real rendered frame.
        content = brain._client.requests[0]["messages"][0]["content"]
        assert content[0]["type"] == "image"
        assert len(content[0]["source"]["data"]) > 1000
        row = scribe.conn.execute("SELECT * FROM episodes").fetchone()
        assert row["session"] == "sim-test"

    def test_memory_survives_across_sim_sessions(self, world, limits, db_path,
                                                 clock):
        """Rung 5 in miniature: session 1 records a place; a brand-new stack
        over the same db recalls it in session 2's system prompt."""
        from continuum.scribe import Scribe as ScribeCls
        look = action_json(memory_ops=[
            {"op": "upsert", "table": "places",
             "data": {"label": "living room",
                      "descriptor": "warm room with a blue ball",
                      "confidence": 0.8}}])
        s1 = ScribeCls(db_path)
        hand1 = SimHand(world)
        spine1 = Spine(hand=hand1, limits=limits, scribe=s1, clock=clock)
        Brain(spine=LocalSpineClient(spine1),
              frame_source=SimFrameSource(world, hand1), scribe=s1,
              db_path=db_path, client=FakeClaude([look]),
              session_id="sim-s1").tick("look around")
        s1.close()

        world2 = build_apartment(seed=1)         # "power cycle": fresh world
        s2 = ScribeCls(db_path)                  # same continuum db
        hand2 = SimHand(world2)
        spine2 = Spine(hand=hand2, limits=limits, scribe=s2, clock=clock)
        brain2 = Brain(spine=LocalSpineClient(spine2),
                       frame_source=SimFrameSource(world2, hand2), scribe=s2,
                       db_path=db_path, client=FakeClaude([action_json()]),
                       session_id="sim-s2")
        brain2.tick("find the blue ball")
        system = brain2._client.requests[0]["system"]
        assert "living room" in system and "blue ball" in system
        s2.close()
