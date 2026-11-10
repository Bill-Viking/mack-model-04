"""Summarise J04-L02 leg-packaging runs into one comparison table.

Reads each run folder's geometry-check.json (written by leg_packaging.py) and prints a Markdown
table plus per-run finding lists; --json writes a compact comparison file. Every number is copied
from those reports; nothing is recomputed. Rigid envelopes on sampled poses: no structural or
walking claim, and no claim about the unmeasured clock interior.
"""
import argparse, json
from pathlib import Path


def kind(parts):
    if any(p.startswith("nb_") for p in parts):
        return "neighbour"
    if "body_envelope" in parts:
        return "shell box"
    if "cradle" in parts:
        return "cradle"
    return "own leg"


def pair_row(i):
    return {"parts": i["parts"], "kind": kind(i["parts"]), "colliding_poses": i["colliding_poses"],
            "max_overlap_mm3": round(i.get("maximum_overlap_mm3", 0.0), 2),
            "min_distance_mm": round(i.get("minimum_distance_mm", 0.0), 2),
            "at_pose_deg": i.get("minimum_distance_pose_deg")}


def summarise(folder):
    r = json.loads((folder / "geometry-check.json").read_text())
    st, m, sw = r["stance"], r["mass"], r["sweep"]
    pairs = [pair_row(i) for i in sw["interferences"]]
    by_kind = {k: sum(1 for p in pairs if p["kind"] == k) for k in ("own leg", "shell box", "cradle", "neighbour")}
    ex = st["body_bbox_exceedance"]
    clear_all = sw.get("clear_poses_deg")
    clear_no_nb = sw.get("clear_poses_ignoring_neighbours_deg")
    stance_pose = [st["pose_deg"][k] for k in ("a", "b", "c")]
    stance_row = next((row for row in sw.get("pose_table", []) if row["pose_deg"] == stance_pose), None)
    return {
        "run": folder.name, "run_folder": str(folder), "variant": r["variant"], "revision": r["revision"], "quick": sw.get("quick"),
        "poses": r["total_poses"], "colliding_poses": r["colliding_poses"],
        "colliding_poses_ignoring_neighbours": sw.get("colliding_poses_ignoring_neighbours"),
        "clear_poses": (len(clear_all) if clear_all is not None else None),
        "clear_poses_ignoring_neighbours": (len(clear_no_nb) if clear_no_nb is not None else None),
        "clear_poses_deg": clear_all, "clear_poses_ignoring_neighbours_deg": clear_no_nb,
        "stance_pose_in_grid": stance_row,
        "colliding_pairs": len(pairs), "colliding_pairs_by_kind": by_kind,
        "near_miss_pairs": len(sw["near_misses"]),
        "parameter_findings": [{k: (round(v, 1) if isinstance(v, float) else v) for k, v in i.items()} for i in r.get("parameter_interferences", [])],
        "neutral_overlaps_own": [{"parts": o["parts"], "volume_mm3": round(o["volume_mm3"], 1)} for o in r.get("neutral_overlaps", []) if kind(o["parts"]) != "neighbour"],
        "inside_shell": [{"parts": e["parts"], "volume_mm3": round(e["volume_mm3"], 1), "z_mm": e.get("z_range_mm")} for e in r.get("inside_shell_envelope", [])],
        "cradle_windows": r.get("cradle_windows", []),
        "overall_height_mm": round(st["overall_height_mm"], 1),
        "clock_bottom_clearance_mm": round(st["clock_bottom_clearance_mm"], 1),
        "stance_width_mm": round(st["stance_width_mm"], 1),
        "beyond_shell_side_mm": round(ex["Y_plus_mm"], 1),
        "beyond_shell_front_mm": round(max(ex["X_plus_mm"], ex["X_minus_mm"]), 1),
        "leg_extents_stance_mm": st["leg_extents_mm"],
        "collision_free_reach_count": r["reach"]["collision_free_subset"]["count"],
        "leg_total_g": round(m["leg_total_g"], 1), "four_legs_g": round(m["four_legs_g"], 1),
        "frame_group_g": {k: round(v, 1) for k, v in m["frame_group_g"].items()},
        "moving_about_j2_g": round(m["moving_about_j2_g"], 1),
        "inertia_j2_neutral_gmm2": round(m["moving_inertia_about_j2_gmm2"]["neutral"]),
        "inertia_j2_stance_gmm2": round(m["moving_inertia_about_j2_gmm2"]["stance"]),
        "colliding_pairs_detail": pairs,
        "near_misses_detail": [pair_row(i) for i in sw["near_misses"]],
        "brief_conflicts": r.get("brief_conflicts", []),
        "sweep_seconds": round(r["sweep_seconds"]),
        "generator_sha256": r["generator_sha256"], "parameter_sha256": r["parameter_sha256"], "step_sha256": r.get("step_sha256"),
    }


COLS = [("run", "Run"), ("overall_height_mm", "Height, mm"), ("stance_width_mm", "Foot width, mm"),
        ("beyond_shell_side_mm", "Past shell side, mm"), ("beyond_shell_front_mm", "Past shell front, mm"),
        ("leg_total_g", "Leg, g"), ("moving_about_j2_g", "Swung by hip, g"), ("inertia_j2_stance_gmm2", "Σmr² hip swing, g·mm²"),
        ("poses", "Poses"), ("clear_poses_ignoring_neighbours", "Clear of own leg and shell"), ("clear_poses", "Clear of everything"),
        ("colliding_pairs", "Colliding pairs"), ("near_miss_pairs", "Near-miss pairs")]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folders", nargs="+", type=Path)
    ap.add_argument("--json", type=Path, help="write the compact comparison here")
    ap.add_argument("--detail", action="store_true", help="print per-run finding lists")
    ap.add_argument("--map", action="store_true", help="print each run's pose grid with hit counts")
    a = ap.parse_args()
    rows = [summarise(f) for f in a.folders if (f / "geometry-check.json").exists()]
    print("| " + " | ".join(c[1] for c in COLS) + " |")
    print("|" + "---|" * len(COLS))
    for r in rows:
        print("| " + " | ".join(str(r[c[0]]) for c in COLS) + " |")
    if a.detail:
        for r in rows:
            print(f"\n## {r['run']}  ({r['variant']}, quick={r['quick']}, sweep {r['sweep_seconds']} s)")
            print("pairs by kind:", r["colliding_pairs_by_kind"])
            print("clear poses (own leg and shell):", r["clear_poses_ignoring_neighbours_deg"])
            print("clear poses (everything):", r["clear_poses_deg"])
            if r["stance_pose_in_grid"]:
                print("stance pose row:", r["stance_pose_in_grid"])
            print("parameter findings:", json.dumps(r["parameter_findings"]))
            print("neutral overlaps (own leg / shell / cradle):", json.dumps(r["neutral_overlaps_own"]))
            print("inside shell:", json.dumps(r["inside_shell"]))
            print("cradle windows:", json.dumps(r["cradle_windows"]))
            print("frame groups g:", r["frame_group_g"], "| clearance under clock mm:", r["clock_bottom_clearance_mm"],
                  "| collision-free reach samples:", r["collision_free_reach_count"])
            for p in r["colliding_pairs_detail"]:
                print(f"  HIT  {p['kind']:9} {'+'.join(p['parts']):52} poses {p['colliding_poses']:3}  max {p['max_overlap_mm3']} mm³")
            for p in r["near_misses_detail"]:
                print(f"  NEAR {p['kind']:9} {'+'.join(p['parts']):52} min {p['min_distance_mm']} mm at {p['at_pose_deg']}")
    if a.map:
        for r in rows:
            rep = json.loads((Path(r["run_folder"]) / "geometry-check.json").read_text())["sweep"]
            g = rep["grids_deg"]
            print(f"\n## {r['run']} pose map · columns c={g['c']} · cell = own-leg/shell/neighbour pair counts, '.' = clear")
            rows_by = {tuple(x["pose_deg"]): x for x in rep["pose_table"]}
            for aa in g["a"]:
                for bb in g["b"]:
                    cells = []
                    for cc in g["c"]:
                        x = rows_by[(aa, bb, cc)]
                        cells.append("." if not (x["own_leg_pairs"] or x["shell_cradle_pairs"] or x["neighbour_pairs"]) else f"{x['own_leg_pairs']}/{x['shell_cradle_pairs']}/{x['neighbour_pairs']}")
                    print(f"  a={aa:>4} b={bb:>4} : " + " ".join(f"{c:>8}" for c in cells))
    if a.json:
        a.json.write_text(json.dumps({
            "scope": "Copied from each run's geometry-check.json (leg_packaging.py). Rigid nominal envelopes on sampled poses; "
                     "benchmark actuator blocks; no structural, thermal or walking claim; the clock interior is unmeasured.",
            "runs": rows}, indent=1) + "\n")
        print("\nwrote", a.json)


if __name__ == "__main__":
    main()
