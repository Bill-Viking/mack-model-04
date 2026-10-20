"""Sim runner — boot the full stack against the virtual world.

    python -m sim.run                          # Spine on :8080 over SimHand
    python -m sim.run --save-frame view.jpg    # render current view, exit
    python -m sim.run --brain 5 --goal "explore and map this room"
                                               # live Brain ticks in-process
                                               # (needs ANTHROPIC_API_KEY)

The sim gets its OWN database (~/continuum/sim-<world>.db) — virtual memories
must never mix with real-world recall.
"""

import argparse
import json
import logging
from pathlib import Path

from continuum.scribe import Scribe
from spine.limits import load_limits
from spine.spine import Spine, create_app

from .sim_hand import SimFrameSource, SimHand
from .world import build_apartment

ROOT = Path(__file__).resolve().parent.parent
WORLDS = {"apartment": build_apartment}


def build_stack(world_name: str = "apartment", seed: int = 0,
                db_path: Path | None = None):
    world = WORLDS[world_name](seed=seed)
    hand = SimHand(world)
    db = db_path or Path.home() / "continuum" / f"sim-{world_name}.db"
    scribe = Scribe(db)
    spine = Spine(hand=hand, limits=load_limits(ROOT / "limits.yaml"),
                  scribe=scribe)
    return world, hand, scribe, spine, db


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--world", default="apartment", choices=sorted(WORLDS))
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--db", type=Path, default=None,
                   help="override sim db path (default ~/continuum/sim-<world>.db)")
    p.add_argument("--save-frame", type=Path, metavar="PATH",
                   help="render the robot's current view to PATH and exit")
    p.add_argument("--brain", type=int, metavar="N",
                   help="run N live Brain ticks in-process (needs ANTHROPIC_API_KEY)")
    p.add_argument("--goal", default="explore and map this place")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO)
    world, hand, scribe, spine, db = build_stack(args.world, args.seed, args.db)

    if args.save_frame:
        from .render import render_frame
        render_frame(world).save(args.save_frame)
        print(f"saved {args.save_frame} (pose: {hand.joint_angles()})")
        return 0

    if args.brain:
        from brain.brain import Brain, LocalSpineClient
        brain = Brain(spine=LocalSpineClient(spine),
                      frame_source=SimFrameSource(world, hand),
                      scribe=scribe, db_path=db, session_id=f"sim-{args.world}")
        for i in range(args.brain):
            result = brain.tick(args.goal)
            print(f"tick {i}: {json.dumps(result)}")
            print(f"  pose={hand.joint_angles()} "
                  f"true_place={world.true_place()} battery={hand.battery_v()}")
        return 0

    import uvicorn
    print(f"sim world '{args.world}' on http://127.0.0.1:{args.port} — "
          f"drive it with tools/hexctl.py; db: {db}")
    uvicorn.run(create_app(spine), host="127.0.0.1", port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
