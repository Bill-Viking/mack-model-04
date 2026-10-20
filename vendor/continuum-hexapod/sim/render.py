"""First-person frame renderer — Wolfenstein-style column raycaster on PIL.

Deliberately crude (rectangles and distance shading, nothing more): the goal
is frames Claude can navigate by, not pretty pictures. Prettiness is out of
scope by design — see the build doc's sim rationale.

Camera model: FOV 70deg horizontal, pan rotates the view with the head
(positive = left/CCW, matching the turn convention), tilt shifts the horizon
(positive = up). Walls are full-height slices; objects are shorter slices
sitting on the floor line at their distance, drawn over walls when nearer.
"""

import base64
import io
import math

from PIL import Image, ImageDraw

from .world import World, _fwd

WIDTH, HEIGHT = 320, 240
FOV_DEG = 70.0
N_COLUMNS = 160
COLUMN_W = WIDTH // N_COLUMNS
K_WALL = 150.0            # wall slice height at 1 m
OBJECT_HEIGHT = 0.55      # object slice height as a fraction of wall height
TILT_PX_PER_DEG = 2.0
CEILING = (222, 224, 230)
FLOOR = (72, 64, 58)
MAX_DRAW_M = 12.0


def _shade(color, dist_m):
    f = 1.0 / (1.0 + 0.35 * dist_m)
    return tuple(int(c * f) for c in color)


def render_frame(world: World, pan_deg: float = 0.0,
                 tilt_deg: float = 0.0) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), CEILING)
    draw = ImageDraw.Draw(img)
    horizon = HEIGHT // 2 + int(tilt_deg * TILT_PX_PER_DEG)
    draw.rectangle([0, horizon, WIDTH, HEIGHT], fill=FLOOR)

    cam_heading = world.heading_deg + pan_deg
    for i in range(N_COLUMNS):
        # Leftmost column = most-CCW ray.
        offset = FOV_DEG / 2 - i * FOV_DEG / (N_COLUMNS - 1)
        dx, dy = _fwd(cam_heading + offset)
        cos_corr = math.cos(math.radians(offset))   # fisheye correction
        x0, x1 = i * COLUMN_W, (i + 1) * COLUMN_W

        wall_d, wall_color = world.raycast_wall(world.x, world.y, dx, dy)
        if wall_color is not None and wall_d < MAX_DRAW_M:
            d = max(0.05, wall_d * cos_corr)
            half = K_WALL / (2 * d)
            draw.rectangle([x0, horizon - half, x1, horizon + half],
                           fill=_shade(wall_color, d))

        obj_d, obj = world.raycast_object(world.x, world.y, dx, dy)
        if obj is not None and obj_d < min(wall_d, MAX_DRAW_M):
            d = max(0.05, obj_d * cos_corr)
            floor_line = horizon + K_WALL / (2 * d)
            obj_h = (K_WALL / d) * OBJECT_HEIGHT
            draw.rectangle([x0, floor_line - obj_h, x1, floor_line],
                           fill=_shade(obj.color, d * 0.6))
    return img


def frame_jpeg(world: World, pan_deg: float = 0.0, tilt_deg: float = 0.0,
               quality: int = 70) -> bytes:
    buf = io.BytesIO()
    render_frame(world, pan_deg, tilt_deg).save(buf, "JPEG", quality=quality)
    return buf.getvalue()


def frame_b64(world: World, pan_deg: float = 0.0, tilt_deg: float = 0.0) -> str:
    return base64.standard_b64encode(frame_jpeg(world, pan_deg, tilt_deg)).decode()
