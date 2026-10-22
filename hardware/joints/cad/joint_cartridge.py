"""Mack J04-C01: original, provisional hip-spread cartridge packaging geometry.

Local Z is the shaft axis; local +Y is the link's zero-angle direction. Map local
Z onto body +X for the hip-spread joint after the body datums have been measured.
No real bearing, motor, structural material, tolerance or load rating is selected.
"""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import build123d as cad

HERE = Path(__file__).resolve().parent
COLORS = {
    "yoke": "#d8c6a6", "shaft": "#697684", "output_link": "#6f97a2",
    "bearing_rear": "#c3cbd0", "bearing_front": "#c3cbd0",
    "motor_envelope": "#4a5261",
}


def read_parameters(path):
    p = json.loads(path.read_text())
    positive = (
        "bearing_id", "bearing_od", "bearing_width", "ear_radius", "fork_gap",
        "base_width", "base_thickness", "mount_pitch", "mount_hole_diameter",
        "shaft_length", "hub_radius", "link_thickness", "link_width", "link_pitch",
        "link_hole_diameter", "motor_width", "motor_length", "sweep_step_deg",
    )
    for key in positive:
        if not isinstance(p[key], (int, float)) or not math.isfinite(p[key]) or p[key] <= 0:
            raise ValueError(f"{key} must be finite and positive")
    for key in ("base_bottom_y", "motor_front_z", "sweep_min_deg", "sweep_max_deg"):
        if not isinstance(p[key], (int, float)) or not math.isfinite(p[key]):
            raise ValueError(f"{key} must be finite")
    checks = {
        "bearing diameters": p["bearing_id"] < p["bearing_od"] < 2*p["ear_radius"],
        "link between fork ears": p["link_thickness"] < p["fork_gap"],
        "hub outside shaft": p["hub_radius"] > p["bearing_id"]/2,
        "link and end hole": p["link_hole_diameter"] < p["link_width"] < 2*p["hub_radius"],
        "link beyond hub": p["link_pitch"] > p["hub_radius"],
        "stem below ear": p["base_bottom_y"] < -p["ear_radius"],
        "base below bearing": p["base_bottom_y"] + p["base_thickness"] < -p["ear_radius"],
        "mount holes inside base": p["mount_pitch"] + p["mount_hole_diameter"] < p["base_width"],
        "shaft spans fork": p["shaft_length"] > p["fork_gap"] + 2*p["bearing_width"],
        "motor outside shaft": p["motor_front_z"] < -p["shaft_length"]/2,
        "sweep ordering": -180 <= p["sweep_min_deg"] < p["sweep_max_deg"] <= 180,
        "bounded sample count": (p["sweep_max_deg"]-p["sweep_min_deg"])/p["sweep_step_deg"] <= 1000,
    }
    for key, valid in checks.items():
        if not valid:
            raise ValueError(f"Invalid design-study parameters: {key}")
    return p


def build(p):
    """Return separate named solids; bearing rings and motor are envelopes only."""
    w, gap, radius = p["bearing_width"], p["fork_gap"], p["ear_radius"]
    span = gap + 2*w
    z_bearing = (gap+w)/2
    bottom = p["base_bottom_y"]
    # The stems deliberately overlap the circular ears and mounting base.
    stem_top = -radius/2
    ear = (cad.Cylinder(radius, w)
           + cad.Pos(0, (bottom+stem_top)/2, 0)
           * cad.Box(2*radius, stem_top-bottom, w))
    ear -= cad.Cylinder(p["bearing_od"]/2, w+2)
    yoke = (cad.Pos(0, 0, -z_bearing)*ear + cad.Pos(0, 0, z_bearing)*ear
            + cad.Pos(0, bottom+p["base_thickness"]/2, 0)
            * cad.Box(p["base_width"], p["base_thickness"], span))
    for x in (-p["mount_pitch"]/2, p["mount_pitch"]/2):
        yoke -= cad.Pos(x, bottom+p["base_thickness"]/2, 0)*cad.Rot(90, 0, 0)*cad.Cylinder(
            p["mount_hole_diameter"]/2, p["base_thickness"]+2)
    ring = cad.Cylinder(p["bearing_od"]/2, w) - cad.Cylinder(p["bearing_id"]/2, w+2)
    thickness, pitch, link_radius = p["link_thickness"], p["link_pitch"], p["link_width"]/2
    link = (cad.Cylinder(p["hub_radius"], thickness)
            + cad.Pos(0, pitch/2, 0)*cad.Box(p["link_width"], pitch, thickness)
            + cad.Pos(0, pitch, 0)*cad.Cylinder(link_radius, thickness))
    link -= cad.Cylinder(p["bearing_id"]/2, thickness+2)
    link -= cad.Pos(0, pitch, 0)*cad.Cylinder(p["link_hole_diameter"]/2, thickness+2)
    parts = {
        "yoke": yoke,
        "shaft": cad.Cylinder(p["bearing_id"]/2, p["shaft_length"]),
        "output_link": link,
        "bearing_rear": cad.Pos(0, 0, -z_bearing)*ring,
        "bearing_front": cad.Pos(0, 0, z_bearing)*ring,
        "motor_envelope": cad.Pos(0, 0, p["motor_front_z"]-p["motor_length"]/2)
            * cad.Box(p["motor_width"], p["motor_width"], p["motor_length"]),
    }
    for name, shape in parts.items():
        shape.label = name
        shape.color = cad.Color(COLORS[name])
    return parts


def common_volume(a, b):
    common = a & b
    return 0.0 if common is None else sum(s.volume for s in common.solids())


def verify(parts, p):
    volumes = {}
    for name, shape in parts.items():
        if not shape.is_valid or len(shape.solids()) != 1 or shape.volume <= 0:
            raise ValueError(f"{name}: invalid, disconnected or empty solid")
        volumes[name] = round(shape.volume, 6)
    maximum_overlap = 0.0
    for (name_a, a), (name_b, b) in itertools.combinations(parts.items(), 2):
        overlap = common_volume(a, b)
        maximum_overlap = max(maximum_overlap, overlap)
        if overlap > 1e-5:
            raise ValueError(f"Unintended neutral overlap: {name_a}/{name_b}: {overlap} mm³")
    count = math.ceil((p["sweep_max_deg"]-p["sweep_min_deg"])/p["sweep_step_deg"])
    angles = sorted(set([min(p["sweep_min_deg"]+i*p["sweep_step_deg"], p["sweep_max_deg"])
                         for i in range(count+1)] + [0.0]))
    minimum_clearance = float("inf")
    # Nominal shaft/bore contact is intentional and is not a bearing-fit design.
    obstacles = {key: value for key, value in parts.items() if key not in ("shaft", "output_link")}
    for angle in angles:
        moving = parts["output_link"].rotate(cad.Axis.Z, angle)
        for name, obstacle in obstacles.items():
            overlap = common_volume(moving, obstacle)
            if overlap > 1e-5:
                raise ValueError(f"Link collision at {angle}° with {name}: {overlap} mm³")
            minimum_clearance = min(minimum_clearance, moving.distance_to(obstacle))
    return {
        "solid_volumes_mm3": volumes,
        "neutral_max_overlap_mm3": round(maximum_overlap, 8),
        "sampled_angles_deg": angles,
        "sampled_link_clearance_mm": round(minimum_clearance, 6),
        "scope": "Nominal rigid solids only; discrete samples, not a continuous collision proof. No cables, fasteners, coupler, stops, motor shaft, enclosure or other joints included.",
    }


def export(parts, p, report, out_dir, parameter_path):
    out_dir.mkdir(parents=True, exist_ok=True)
    # Export leaves before parenting them into the assembly tree.
    for name in ("yoke", "output_link", "shaft"):
        cad.export_step(parts[name], out_dir/f"{name}-draft.step", timestamp="2026-10-21T00:00:00+00:00")
    assembly = cad.Compound(label=p["revision"], children=list(parts.values()))
    output_file = out_dir / "j04-c01-draft.step"
    cad.export_step(assembly, output_file, timestamp="2026-10-21T00:00:00+00:00")
    restored = cad.import_step(output_file)
    original_volume = sum(s.volume for s in parts.values())
    volume_error = abs(restored.volume-original_volume)
    bbox_error = max(abs(a-b) for a, b in zip(assembly.bounding_box().size, restored.bounding_box().size))
    if not restored.is_valid or len(restored.solids()) != len(parts) or volume_error > 1e-4 or bbox_error > 1e-5:
        raise ValueError("STEP assembly round trip failed geometry checks")
    report.update({
        "revision": p["revision"], "status": p["status"], "build123d": cad.__version__,
        "parameter_sha256": hashlib.sha256(parameter_path.read_bytes()).hexdigest(),
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "step_sha256": hashlib.sha256(output_file.read_bytes()).hexdigest(),
        "step_round_trip": {"solids": len(restored.solids()), "volume_error_mm3": volume_error,
                            "bounding_box_error_mm": bbox_error},
        "assembly_size_mm": [round(v, 6) for v in assembly.bounding_box().size],
        "no_structural_analysis_or_physical_testing": True,
    })
    (out_dir/"geometry-check.json").write_text(json.dumps(report, indent=2)+"\n")
    meshes = []
    for name, shape in parts.items():
        vertices, triangles = shape.tessellate(0.25, 0.2)
        meshes.append({"name": name, "color": COLORS[name],
                       "vertices": [[round(v.X, 4), round(v.Y, 4), round(v.Z, 4)] for v in vertices],
                       "triangles": triangles})
    data = {"parts": meshes, "parameters": p, "report": report}
    template = (HERE/"viewer-template.html").read_text()
    embedded = json.dumps(data, separators=(",", ":")).replace("<", "\\u003c")
    (out_dir/"preview.html").write_text(template.replace("/* MODEL_DATA */", embedded))
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parameters", type=Path, default=HERE/"j04-c01.example.json")
    parser.add_argument("--out", type=Path, default=HERE/"exports")
    args = parser.parse_args()
    p = read_parameters(args.parameters)
    parts = build(p)
    export(parts, p, verify(parts, p), args.out, args.parameters)


if __name__ == "__main__":
    main()
