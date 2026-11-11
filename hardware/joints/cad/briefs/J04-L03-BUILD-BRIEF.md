# J04-L03 — build brief: a base module and one short leg (packaging model)

Quality bar: beyond-Apple quality — the machine notices, the human never checks; one plain
sentence at the moment it is needed; state visible on the surface; nothing superfluous.
Design principles served: make the interface truthful (every number in the report is measured
on the model it describes); prove quality before declaring completion (the generator's own
checks run on every build and the report records their scope).

complexity: complex — a new generator with a stance solver, a mass model and two variants.

## Why this build exists

The first leg iteration (J04-L02) stands 223.8 mm with 111.8 mm of leg under the shell. The
confirmed build-target picture shows about half that. The owner ruled: short legs under a low
base. This build measures how close the benchmark actuator block gets to that picture, and
what it costs in knee bend, joint torque, width, length and stability. Listing what does not
fit is the purpose; do not tune anything to make it fit.

## Read first, and do not open

Read: `hardware/joints/cad/leg_packaging.py` (the J04-L02 generator: reuse its conventions and
helpers), `hardware/joints/cad/leg-viewer-template.html`, `hardware/joints/cad/briefs/J04-L02-BUILD-BRIEF.md`
(§1, §2, §4, §5 define the frames, the actuator block builder, posing and the report this build
extends), and `hardware/joints/cad/j04-l03.base-short.json` (the parameters; do NOT change its values).

Do NOT open: `STATUS.md`, `OPENER.md`, anything under `docs/review/`, any `*.log`, any other
brief's report. They are not inputs.

Interpreter: `runtime/cad/venv/bin/python` (Python 3.12, build123d 0.12.0). No pip installs, no
network, no other interpreter, no browser or GUI application.

## What you build

A NEW generator `hardware/joints/cad/leg_base_packaging.py`. Do not modify
`leg_packaging.py` or any J04-L02 file; import from it or copy what you need. It reads
`j04-l03.base-short.json`, takes `--parameters`, `--out`, `--variant direct|proximal`, `--quick`,
and writes per run, like J04-L02: `j04-l03-<variant>.step`, `geometry-check.json`, `preview.html`
(three sliders, from `leg-viewer-template.html`). Default out folders:
`hardware/joints/cad/exports/l03-base-direct/` and `.../l03-base-proximal/`.
Then one compact `hardware/joints/cad/exports/l03-summary.json` (§7).

Everything is a rigid-solid packaging envelope. The script never raises on a collision; it
records it. It raises only on invalid parameters, invalid solids or a failed STEP round trip.

## 1. Frames and chain (changes from J04-L02 in bold)

Body frame, units, `s`, outboard/inboard, the actuator block builder and the posing order are
J04-L02's. Joint points at neutral, front-left leg:

- `P1 = hip.P1` — hip-spread axis J1, direction +X.
- **`P2 = P1 + (hip.j2_dx, s·d, −h2)`**, with `d = hip.d_direct` or `hip.d_proximal` by variant.
  Posed: `P2(a) = P1 + (j2_dx, 0, 0) + Rx(a)·(0, s·d, −h2)`.
- `P3 = P2 + (0, 0, −L1)`; `P4 = P3 + (0, 0, −L2)`; posed as in J04-L02.
- **Foot axis point `P5 = P4 + (0, 0, −foot.radius)`** in the lower frame.

Run J04-L02's five-triple pose-formula check on the foot solid's centroid against the chain
(with `P5` and the `j2_dx` term); maximum error < 1e-6 mm.

## 2. Solids

**Static (frame `body`)**
- `body_envelope`: as J04-L02. No cradle.
- `base_top_plate`: box X ±(depth_X/2 − plate_inset_X), Y ±plate_half_width_Y,
  Z [z_top − top_plate_thickness, z_top].
- `base_bottom_plate`: same XY, Z [z_top − H_base, z_top − H_base + bottom_plate_thickness],
  where `H_base = top_plate_thickness + interior_height + bottom_plate_thickness`.
- `base_spine`: box X ±spine_half_width_X, same Y, Z between the two plates.
- `j1_actuator` (+horn, +idler): `actuator(+X, long_dir inboard, P1, 0, hip.j1_horn_dir)`.
  It lies flat: W is vertical. Record interference `j1_case_into_base_plate` with the overlap
  in mm if its Z range meets either plate.
- `j1_mount`: box filling the gap between the J1 case top face and the top plate underside, XY =
  the case's XY bbox clipped to the top plate's footprint. Omit if the gap is zero.
- Neighbour envelopes `nb_FR_*`, `nb_RL_*`, `nb_RR_*`: as J04-L02 (every front-left leg solid and
  the J1 parts, posed at the SOLVED stance pose of §3, mirrored). The base solids are not copied.

**Carrier (frame `carrier`, rotates with a about J1)**
- `j2_actuator` (+horn, +idler): `actuator(+Y, long_dir rearward (−X), P2, 0, outboard)`.
  It lies flat: W is vertical, H runs along X, centred on x1.
- `carrier_horn_plate`, `carrier_idler_plate`: perpendicular to X, occupying
  [half_span − tp, half_span] from x1 on each side, so each inner face touches one end face of
  the J2 case. Outline in (Y, Z): disc radius `carrier_hub_radius` at (y1, z1) ∪ neck rectangle
  Y from y1 to the J2 case's inboard face, Z = z1 ± `carrier_neck_half_height` ∪ end rectangle
  Y = the J2 case's Y span, Z = z2 ± W/2.
- `carrier_hub_horn`, `carrier_hub_idler`: as J04-L02 (from the J1 boss outer face to the plate
  inner face).
- No `carrier_web`: the J2 case clamped between the plates is the tie. Say so in the report.

**Thigh (frame `upper`, rotates with b about J2) — both variants**
- `upper_horn_plate`, `upper_idler_plate`: perpendicular to Y on the J2 horn and idler boss
  outer faces, thickness tp outward. Outline in (X, Z): disc `links.hub_radius` at P2 ∪ bar
  X = x2 ± plate_width/2 from z2 to z3 ∪ disc `links.hub_radius` at P3.
- No `upper_web`.

**Direct variant**
- `knee_actuator` (+horn, +idler), frame `lower`: `actuator(+Y, long_dir down, P3, 0, outboard)`.
  The knee actuator IS the shank. Its bosses' outer faces lie in the thigh plates' inner faces
  (intentional contact; skip those pairs and list them).
- `shank_channel_plus`, `shank_channel_minus`, frame `lower`: plates perpendicular to X at
  x3 ± (W/2 + tp/2), thickness tp, Y = the knee case's Y span, Z [z4, z3 + e].
- `foot`, frame `lower`: cylinder radius `foot.radius`, axis along Y through P5, Y = the knee
  case's Y span.

**Proximal variant** (a comparison run; build it from J04-L02's proximal rules with only these
changes; if a rule below cannot be built, stop THIS run, say exactly which rule failed, and
still deliver the direct run)
- `knee_actuator`, `knee_mount`, `pulley_hip`, `pulley_knee`, `belt`, `knee_shaft`,
  `knee_bearing_in`, `knee_bearing_out`: J04-L02's proximal rules, `mount_side` outboard, frame
  `upper`, knee case long_dir down.
- `upper_tie`, frame `upper`: box X = x2 ± 6, Y between the thigh plates' inner faces,
  Z [z3 − 4, z3 + 4]; the knee shaft passes through it (intentional; skip that pair).
- `lower_plate_in`, `lower_plate_out`, frame `lower`: J04-L02's Y positions. Outline: disc
  `links.hub_radius` at P3 ∪ bar X = x3 ± plate_width/2 from z3 to z4, ending FLAT at z4 (no
  disc at P4). No `lower_web`.
- `foot`, frame `lower`: cylinder radius `foot.radius`, axis along Y through P5, Y from the
  outer face of `lower_plate_in` to the outer face of `lower_plate_out`.

Labels, colours, mass classes, hardware allowance: as J04-L02. Base solids use `base.density_g_cm3`.

## 3. Stance, solved from the requirement

`under_shell(a, b, c)` = z_top of the shell bottom (0) minus the lowest Z of the posed `foot`
solid (take it from the posed solid's bounding box).

- **Solved stance**: a = `poses.stance_spread_a`, b = −c/2, c found by bisection on [0, 130] so
  that `under_shell` = `requirements.under_shell_height_mm.target` within 0.01 mm. If the target
  is outside what c ∈ [0, 130] reaches, use the nearest end and record `stance_reached: false`
  with the achievable range. This solved pose is "the stance" for every stance output below, for
  the neighbours and for the viewer's start pose and stance button.
- **Height sweep**: the same solve for each value in `poses.height_sweep_mm`; one row per value
  (see §5.4).
- **Reference pose**: `poses.reference_pose`, reported beside the stance.

## 4. Checks carried over from J04-L02

All of J04-L02 §5 items 1, 2, 4, 5, 6, 7, 8, 9 on the new solids, with the base solids in the
static group that the carrier, thigh and shank solids are tested against, the same sweep grid
and the same pair-skipping rule for intentional contacts. Item 3 (cradle windows) is dropped;
any solid's volume inside `body_envelope` at neutral is listed under `inside_shell_envelope`.
Report `clear_poses_deg` and `clear_poses_ignoring_neighbours_deg` as J04-L02 does.

## 5. New checks

1. `requirement`: target, min, max, the solved stance pose, `under_shell_height_mm`,
   `overall_height_mm` (= body height + under-shell height), `stance_reached`, `within_range`.
   Also `straight_leg_under_shell_mm` at (stance_spread_a, 0, 0).
2. `ground`: at the stance, for every posed leg solid other than `foot`, its lowest Z minus the
   foot's lowest Z. `ground_contact_ok` is true when none is negative; list any that are, with mm.
   Also the lowest non-foot solid and its clearance above the floor.
3. `proportions`: at the stance, over all four legs (mirrors) and the base: `width_across_hips_mm`
   (2 × the largest |Y| of any carrier or thigh solid), `overall_width_mm` and
   `overall_length_mm` (bounding box of everything below z = 0), `beyond_face_mm` (how far any
   leg solid reaches beyond X = depth_X/2), `track_width_mm` and `wheelbase_mm` (between contact
   points, below), `base_height_mm`, `base_below_shell_mm`, `inside_shell_mm` (0 here). Echo
   `requirements.build_target_reference_mm` beside them with the differences.
4. `height_sweep`: for each height: solved (a, b, c), `stance_reached`, the knee's forward offset
   from P2 in X, `beyond_face_mm`, the own-leg / base / shell / neighbour colliding pair counts
   at that single pose, and the static torques of item 6 for the reference mass with 4 feet.
5. `contact_point`: at a pose, the point (x, y, z) = (X of the posed P5, Y of the foot solid's
   lowest end, the foot's lowest Z). For Y use the posed foot axis end that is lower; if a = 0
   use the axis midpoint.
6. `static_torque`: at the stance and at the reference pose, for a vertical force F at the
   contact point, the holding torque about each joint axis = |((C − A) × F) · u|, A a point on
   the posed axis, u its unit direction. Rows for 4, 3 and 2 feet sharing the weight equally;
   two tables, one for `mass_model.reference_mass_kg` and one for the model's own total mass
   (item 7). Columns: load per foot (N), J1, J2, J3 (N·m), and each as a share of
   `actuator.stall_torque_Nm`.
7. `mass_and_com`: at the stance, a list of (name, mass_g, centroid) for: every leg solid of all
   four legs, hardware allowances at their joint points, the four J1 groups, the base solids,
   and the three `mass_model` items. Then `total_mass_g`, `com_mm` (body frame), `com_height_above_floor_mm`.
8. `support`: the four contact points; with four feet down, the distance from the CoM's ground
   projection to each side of their rectangle (`margin_front`, `rear`, `left`, `right`) and
   the tip angle for the smallest (atan(margin / CoM height above the floor)); with each leg
   lifted in turn, the signed distance from the CoM projection to the nearest edge of the
   remaining triangle (negative = outside). State that masses and positions tagged ASSUMED in
   the parameters drive this result.
9. Provenance echo as J04-L02, plus every `*_provenance` string of the new sections.

Printed tables (report file and summary): mm to 0.1, degrees to 0.1, grams to 0.1, N·m to
0.001, percentages to whole numbers, each rounded once from the unrounded value. The JSON keeps
full floats.

## 6. Independent estimates, for your own cross-check (do not tune toward them)

Hand arithmetic by the design session from the chain alone, direct variant, a = 12°:
`P2(12°)` ≈ (32.0, 56.77, −7.03); solved stance at 55 mm ≈ (12, −50.6, 101.2), within 1.5° on
b and c; straight-leg under-shell height ≈ 78.2 mm; under-shell height at the reference pose
≈ 66.7 mm; at 70 mm the knee bend ≈ 59°. If the model differs by more than 1.5° or 1.5 mm, do
not change the model: say so in the report and show the model's own derivation of that number.

Expected and NOT to be tuned away: collisions with the shell at a = +30 (the hip rises as it
spreads), collisions at b = +60 and +90 (the thigh pointing along the flat J2 case and at the
rear leg), a knee that stands forward of the face at the 55 mm stance, and a wide proximal run.

## 7. Summary file and report

`exports/l03-summary.json`: for each variant that built: the solved stance, under-shell and
overall height, `within_range`, `ground_contact_ok`, leg mass and four-leg mass, total mass,
CoM, the support margins, the stance static-torque rows, the proportions, the sweep's total /
colliding / clear pose counts and pair counts by class (own leg, base, shell, neighbour), and
the height-sweep rows. Beside them, for comparison, read from
`exports/l02-A-under-direct/geometry-check.json` WITHOUT changing it: overall height,
clock-bottom clearance, leg mass, stance width, total and colliding poses.

`hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF-REPORT.md`, facts only:
- First line: `STATE: DONE | PARTIAL | FAIL` and one sentence.
- The commands you ran, exit codes, wall times.
- A results table per variant with the summary's headline numbers.
- The height-sweep table.
- The interference list at the stance and the pair classes over the sweep.
- Each place this brief could not be followed exactly and what you did instead.
- `OPEN:` items the design session must rule on. No proposals of a fitted candidate.

## 8. Done when

- `runtime/cad/venv/bin/python hardware/joints/cad/leg_base_packaging.py --quick` exits 0, then
  the full direct run and the full proximal run (or the proximal run's recorded stop).
- Both `preview.html` files exist and embed the model; you do NOT open a browser. Say they were
  not browser-checked; the design session checks them.
- `geometry-check.json` carries §4 and §5; pose-formula error < 1e-6 mm.
- The summary and the report are written.
- Commit nothing. Touch nothing outside `hardware/joints/cad/` (new: `leg_base_packaging.py`,
  `exports/l03-base-direct/`, `exports/l03-base-proximal/`, `exports/l03-summary.json`,
  `briefs/J04-L03-BUILD-BRIEF-REPORT.md`) and `runtime/cad/` for scratch. Do not modify
  `j04-l03.base-short.json`, `leg_packaging.py`, any `j04-l02*` or `j04-c01*` file, any existing
  export, template or brief.
- One run, no retries of your own beyond fixing your own errors inside this run.
