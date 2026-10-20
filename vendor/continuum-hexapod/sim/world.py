"""Tier-1 virtual world: 2D geometry, no physics engine — deliberately crude.

Rooms are wall segments, objects are colored cylinders, the robot is a pose
(x, y, heading) with a radius. Continuous units are meters. Heading follows
the Spine contract: 0 = +y ("north"), positive = counterclockwise (turn(+30)
rotates CCW), so the forward unit vector is (-sin H, cos H).

This is a Continuum simulator, not a hexapod simulator: no gait dynamics, no
balance — walk translates the pose with noise, walls stop it (legs churn,
robot doesn't advance; the Brain notices via sonar/camera, which is exactly
the expected-vs-actual learning signal Continuum feeds on).
"""

import math
import random
from dataclasses import dataclass, field

ROBOT_RADIUS = 0.12          # m — matches sonar standoff: readings are edge-relative
STANDOFF = ROBOT_RADIUS + 0.02
SONAR_MAX_CM = 300.0         # vendor sensor max_distance = 3 m
BATTERY_FULL_V = 8.2
DRAIN_PER_STEP_V = 0.003
DRAIN_PER_TURN_V = 0.002
DRAIN_PER_MISC_V = 0.0005

# Commanded stride per gait cycle, scaled by speed (0.2 -> ~4 cm, 0.8 -> 8 cm).
def step_length_m(speed: float) -> float:
    return 0.03 + 0.0625 * speed


@dataclass
class Wall:
    x1: float
    y1: float
    x2: float
    y2: float
    color: tuple = (150, 150, 160)


@dataclass
class SimObject:
    label: str
    x: float
    y: float
    radius: float
    color: tuple


@dataclass
class Place:
    """Ground truth for debugging/eval only — never exposed through the Hand.
    Continuum has to *discover* places; these let tests check what it found."""
    label: str
    x: float
    y: float
    radius: float


def _fwd(heading_deg: float) -> tuple:
    rad = math.radians(heading_deg)
    return (-math.sin(rad), math.cos(rad))


class World:
    def __init__(self, walls: list, objects: list, places: list,
                 start: tuple = (0.0, 0.0, 0.0), seed: int = 0):
        self.walls = walls
        self.objects = objects
        self.places = places
        self.x, self.y, self.heading_deg = start
        self.battery_v = BATTERY_FULL_V
        self.rng = random.Random(seed)
        self.collisions = 0          # debug counter: steps that hit geometry

    # --- geometry helpers ---

    @staticmethod
    def _ray_segment(px, py, dx, dy, w: Wall):
        """Distance along ray (px,py)+t(dx,dy) to wall w, or None."""
        sx, sy = w.x2 - w.x1, w.y2 - w.y1
        denom = dx * sy - dy * sx
        if abs(denom) < 1e-12:
            return None
        ax, ay = w.x1 - px, w.y1 - py
        t = (ax * sy - ay * sx) / denom
        u = (ax * dy - ay * dx) / denom
        if t > 1e-9 and -1e-9 <= u <= 1 + 1e-9:
            return t
        return None

    @staticmethod
    def _ray_circle(px, py, dx, dy, cx, cy, r):
        """Nearest positive distance along unit ray to circle, or None."""
        ox, oy = px - cx, py - cy
        b = 2 * (dx * ox + dy * oy)
        c = ox * ox + oy * oy - r * r
        disc = b * b - 4 * c
        if disc < 0:
            return None
        t = (-b - math.sqrt(disc)) / 2
        return t if t > 1e-9 else None

    @staticmethod
    def _point_segment_dist(px, py, w: Wall) -> float:
        sx, sy = w.x2 - w.x1, w.y2 - w.y1
        seg_len2 = sx * sx + sy * sy
        if seg_len2 < 1e-12:
            return math.hypot(px - w.x1, py - w.y1)
        u = ((px - w.x1) * sx + (py - w.y1) * sy) / seg_len2
        u = max(0.0, min(1.0, u))
        return math.hypot(px - (w.x1 + u * sx), py - (w.y1 + u * sy))

    def raycast_wall(self, px, py, dx, dy):
        """(distance, color) of nearest wall along ray, or (inf, None)."""
        best, color = math.inf, None
        for w in self.walls:
            t = self._ray_segment(px, py, dx, dy, w)
            if t is not None and t < best:
                best, color = t, w.color
        return best, color

    def raycast_object(self, px, py, dx, dy):
        """(distance, object) of nearest object along ray, or (inf, None)."""
        best, obj = math.inf, None
        for o in self.objects:
            t = self._ray_circle(px, py, dx, dy, o.x, o.y, o.radius)
            if t is not None and t < best:
                best, obj = t, o
        return best, obj

    def _clear_at(self, px, py) -> bool:
        for w in self.walls:
            if self._point_segment_dist(px, py, w) < ROBOT_RADIUS:
                return False
        for o in self.objects:
            if math.hypot(px - o.x, py - o.y) < ROBOT_RADIUS + o.radius:
                return False
        return True

    # --- robot actuation (called by SimHand only) ---

    def do_turn_cycle(self, delta_deg: float) -> None:
        noise = self.rng.gauss(0, 2.0)
        self.heading_deg = (self.heading_deg + delta_deg + noise) % 360
        self.battery_v -= DRAIN_PER_TURN_V

    def do_step(self, body_relative_heading_deg: float, speed: float) -> bool:
        """One gait cycle of travel. Returns True if the robot advanced,
        False if geometry blocked it (legs churned in place)."""
        self.battery_v -= DRAIN_PER_STEP_V
        direction = (self.heading_deg + body_relative_heading_deg
                     + self.rng.gauss(0, 3.0))
        dist = step_length_m(speed) * (1 + self.rng.gauss(0, 0.1))
        dx, dy = _fwd(direction)
        for fraction in (1.0, 0.75, 0.5, 0.25):
            nx = self.x + dx * dist * fraction
            ny = self.y + dy * dist * fraction
            if self._clear_at(nx, ny):
                self.x, self.y = nx, ny
                return True
        self.collisions += 1
        return False

    def drain_misc(self) -> None:
        self.battery_v -= DRAIN_PER_MISC_V

    # --- sensors ---

    def sonar_cm(self, pan_deg: float = 0.0) -> float:
        """Edge-relative range along body heading (+ head pan), like the real
        HC-SR04 on the pan head."""
        dx, dy = _fwd(self.heading_deg + pan_deg)
        wall_d, _ = self.raycast_wall(self.x, self.y, dx, dy)
        obj_d, _ = self.raycast_object(self.x, self.y, dx, dy)
        d_m = min(wall_d, obj_d) - ROBOT_RADIUS
        d_cm = d_m * 100 * (1 + self.rng.gauss(0, 0.02))
        return round(max(0.0, min(SONAR_MAX_CM, d_cm)), 1)

    # --- debug/eval only ---

    def true_place(self):
        best, best_d = None, math.inf
        for p in self.places:
            d = math.hypot(self.x - p.x, self.y - p.y)
            if d <= p.radius and d < best_d:
                best, best_d = p.label, d
        return best


def _split_span(lo, hi, gaps):
    """Split [lo, hi] into sub-spans, removing (offset, width) gaps measured
    from lo. Returns [(a, b), ...] of remaining solid spans."""
    spans, cursor = [], lo
    for off, width in sorted(gaps):
        if lo + off > cursor:
            spans.append((cursor, lo + off))
        cursor = max(cursor, lo + off + width)
    if cursor < hi:
        spans.append((cursor, hi))
    return spans


def _room(x, y, w, h, color, doors=()):
    """Axis-aligned room outline as wall segments, with door gaps.
    doors: (side, offset, width) triples; side in n/s/e/w; offset measured
    from the room's min-x (for n/s) or min-y (for e/w) corner."""
    by_side = {"n": [], "s": [], "e": [], "w": []}
    for side, off, width in doors:
        by_side[side].append((off, width))
    walls = []
    for a, b in _split_span(x, x + w, by_side["n"]):
        walls.append(Wall(a, y + h, b, y + h, color))
    for a, b in _split_span(x, x + w, by_side["s"]):
        walls.append(Wall(a, y, b, y, color))
    for a, b in _split_span(y, y + h, by_side["e"]):
        walls.append(Wall(x + w, a, x + w, b, color))
    for a, b in _split_span(y, y + h, by_side["w"]):
        walls.append(Wall(x, a, x, b, color))
    return walls


def build_apartment(seed: int = 0) -> World:
    """Default world: living room (south), hallway (middle), kitchen (north).

    Layout (meters), doorways 0.6 m wide:

        y=6  +----------------+
             |    kitchen     |   red mug near the counter (north wall)
        y=4  +---##-----------+
             |    hallway     |   green plant at the east end
        y=3  +---------##-----+
             |  living room   |   blue ball mid-room; robot starts at south
        y=0  +----------------+
             x=0             x=4
    """
    lr = (170, 160, 150)    # living room: warm gray
    hall = (140, 150, 170)  # hallway: cool gray
    kit = (180, 180, 140)   # kitchen: yellowish
    walls = []
    walls += _room(0, 0, 4, 3, lr, doors=[("n", 2.6, 0.6)])
    walls += _room(0, 3, 4, 1, hall, doors=[("s", 2.6, 0.6), ("n", 0.9, 0.6)])
    walls += _room(0, 4, 4, 2, kit, doors=[("s", 0.9, 0.6)])
    objects = [
        SimObject("blue ball", 1.2, 1.8, 0.10, (40, 80, 220)),
        SimObject("green plant", 3.6, 3.5, 0.15, (40, 160, 60)),
        SimObject("red mug", 1.5, 5.6, 0.06, (210, 40, 40)),
    ]
    places = [
        Place("living room", 2.0, 1.5, 1.6),
        Place("hallway", 2.0, 3.5, 1.6),
        Place("kitchen", 2.0, 5.0, 1.5),
    ]
    return World(walls, objects, places, start=(2.0, 0.6, 0.0), seed=seed)
