# J04-L02 — build brief: one complete three-axis leg and cradle interface (packaging model)

Quality bar: beyond-Apple quality — the machine notices, the human never checks; one plain
sentence at the moment it is needed; state visible on the surface; nothing superfluous.
Design principles served: make the interface truthful (every number in the report is measured
on the model it describes); prove quality before declaring completion (the generator's own
checks run on every build and the report records their scope).

## What you build

A build123d 0.12.0 generator `hardware/joints/cad/leg_packaging.py` that reads
`hardware/joints/cad/j04-l02.example.json` (already written, do not change its values), builds
ONE front-left leg with its hip carrier and the cradle plate it hangs from, plus static envelopes
of the body and the three other legs, and writes to an output folder:

- `j04-l02-<variant>.step` — assembly of all named, coloured solids (one Compound, children = solids).
- `geometry-check.json` — the report described below.
- `preview.html` — an offline WebGL viewer with three sliders (hip spread a, hip swing b, knee c),
  derived from `hardware/joints/cad/viewer-template.html` (reuse its look, controls, zoom and
  parts-separation code; read it first). Parts are embedded at the neutral pose with a `frame`
  tag; the viewer poses them in JavaScript (transforms in §4).

Interpreter: `runtime/cad/venv/bin/python` (Python 3.12, build123d 0.12.0 installed). No pip
installs, no network, no other interpreter. Read `hardware/joints/cad/joint_cartridge.py` first and
keep its conventions (argparse `--parameters`, `--out`; labelled coloured solids; STEP export with a
fixed timestamp; a report JSON with sha256 of parameters, generator and STEP; STEP round-trip check).
Default `--out` is `hardware/joints/cad/exports/l02/`. Add `--variant direct|proximal` (default: the
JSON's `knee.variant`) and `--quick` (sweep step doubled) flags.

Everything below is a rigid-solid packaging envelope. The script asserts NOTHING about strength,
bearings, motors or walking. Where this brief says "report", it means write it into the JSON;
where it says "interference", the script records it and continues — it never raises on a
collision, because listing collisions is the purpose of this model. It raises only on invalid
parameters, invalid solids or a failed STEP round trip.

## 1. Frames and parameters

Body frame B: origin at the clock bottom centre, +X forward (face), +Y left, +Z up. Millimetres,
grams, degrees. The front-left leg has hip origin `P1 = (x1, y1, z1)` from `hip.P1`;
`s = sign(y1)` (+1 for a left leg) is the outboard sign. "Outboard" = +s·Y, "inboard" = −s·Y,
"down" = −Z, "up" = +Z, "forward" = +X, "rearward" = −X.

Actuator block (§2) dimensions `W, H, D`, output axis along D, axis offset `e` from the near end
along H. Plates have thickness `tp = links.plate_thickness`, clearance `c = links.clearance`,
horn/idler boss height `hg = actuator.horn_height` (= idler_height).

Joint points at neutral (a = b = c = 0):
- `P1` — hip-spread axis J1, direction +X.
- `P2 = P1 + (0, s·d, −h2)` — hip-swing axis J2, direction +Y (parallel to Y at neutral).
- `P3 = P2 + (0, 0, −L1)` — knee axis J3, direction +Y.
- `P4 = P3 + (0, 0, −L2)` — foot pivot point.

Posed chain, active right-hand rotations (as hardware/joints/leg-layout.md):
`P2(a) = P1 + Rx(a)·(0, s·d, −h2)`; `P3 = P2 + Rx(a)·Ry(b)·(0,0,−L1)`;
`P4 = P3 + Rx(a)·Ry(b+c)·(0,0,−L2)`.
Frame transforms used for posing solids (each solid is built at neutral in body coordinates):
- carrier frame: `T_c(a)` = rotate about the line through P1 along X by a.
- upper frame: `T_u(a,b)` = `T_c(a)` ∘ rotate about the line through P2 (neutral) along Y by b.
- lower frame: `T_l(a,b,c)` = `T_u(a,b)` ∘ rotate about the line through P3 (neutral) along Y by c.
Positive b moves the upper link toward −X for this convention; do not "fix" that.

## 2. Actuator block builder

`actuator(label, axis_dir, long_dir, point, axial_offset, horn_dir)` returns three solids:
`<label>` (case box), `<label>_horn` (cylinder, diameter `horn_diameter`, height `hg`, standing on
the case face in `horn_dir`), `<label>_idler` (same, on the opposite face). The case is a box with
D along `axis_dir`, centred along the axis at `point + axial_offset·axis_dir`; along `long_dir` it
spans from `−e` (near end) to `+(H − e)` (far end) relative to the axis line; along
`w_dir = axis_dir × long_dir` it spans ±W/2. Report for each actuator its `axis_point`,
`axis_dir`, `near_end_point`, `far_end_point`, `horn_face_centre`, `idler_face_centre` and
`case_bbox` — these are the component output datums the study is for.
Mass: `actuator.mass_g` for the case; horn and idler carry 0 g (included).

## 3. Solids (front-left leg), by frame

**Static (frame `body`)**
- `body_envelope`: box X ±depth_X/2, Y ±width_Y/2, Z [0, height_Z]. No mass counted (catalog
  complete clock 229 g, retained mass unknown — say so in the report).
- `cradle`: box X ±(depth_X/2 − inset), Y ±(width_Y/2 − inset), Z [z_top − thickness, z_top].
  Window rule (§5) may cut rectangular windows out of it.
- `j1_actuator` (+horn, +idler): `actuator("j1_actuator", +X, long_dir per hip.j1_case_long_dir,
  P1, 0, hip.j1_horn_dir)`.
- `j1_mount`: box bridging the j1 case to the cradle along Z: XY footprint = the case's XY bbox;
  Z from the case's top face to the cradle's bottom face when the case is below the cradle, or
  from the case's bottom face to the cradle's top face when it is above. If the case's Z range
  overlaps the cradle's, build no mount and record interference `j1_case_into_cradle` with the
  overlap depth in mm.
- Neighbour envelopes (`nb_FR_*`, `nb_RL_*`, `nb_RR_*`): copies of EVERY front-left solid of the
  carrier, upper and lower frames posed at the `poses.stance` pose, mirrored: FR = mirror about the
  XZ plane (Y → −Y); RL = mirror about the YZ plane (X → −X); RR = both. Also mirror the j1
  actuator/horn/idler and j1_mount. Only built when `neighbors` is true. They carry no mass in the
  per-leg totals (the ×4 total is computed arithmetically).

**Carrier (frame `carrier`, rotates with a about J1)**
- `carrier_horn_plate`, `carrier_idler_plate`: plates perpendicular to X at
  X = x1 ± carrier_plate_half_span (the horn-side plate on the `j1_horn_dir` side), thickness tp
  (the plate occupies [half_span − tp, half_span] from x1). Outline in the (Y, Z) plane: union of a
  disc of radius `carrier_hub_radius` centred at (y1, z1) and a rectangle spanning
  Y from min(y1, j2 case Ymin) to max(y1, j2 case Ymax) and Z from the j2 case far-end Z (its
  bottom for long_dir "down") to z1. Extrude tp.
- `carrier_hub_horn`, `carrier_hub_idler`: cylinders of radius `carrier_hub_radius` along X on
  the J1 axis, from the horn (idler) boss outer face to the inner face of the matching plate.
- `carrier_web`: box X between the two plates' inner faces, Y = j2 case Y span, Z = [j2 far-end
  face − c − tp, j2 far-end face − c] (a cap under the J2 case's far end).
- `j2_actuator` (+horn, +idler): `actuator("j2_actuator", +Y, long_dir "down" (only this value is
  supported in D01; refuse others with a clear ValueError), P2, hip.j2_axial_offset,
  outboard/inboard per hip.j2_horn_dir)`.
  The carrier plates must hold the J2 case by its ±X side faces: if the J2 case's X half-width
  (W/2) ≥ half_span − tp, record interference `j2_case_into_carrier_plates`.

**Upper link (frame `upper`, rotates with b about J2)**
- `upper_horn_plate`, `upper_idler_plate`: plates perpendicular to Y, sitting on the J2 horn and
  idler boss outer faces (plate inner face = boss outer face; thickness tp outward). Outline in
  (X, Z): disc radius `links.hub_radius` at P2 ∪ rectangle X ±plate_width/2 from Z = z2 down to
  Z_end ∪ disc radius `links.hub_radius` at P3 (only when the plate reaches P3).
  - proximal variant: Z_end = z3 (plates reach the knee hub; bearing holes below).
  - direct variant: Z_end = knee case far-end Z + c (the plates stop above the knee case; see
    the direct-knee construction). If Z_end < z2 − (H − e) − c (i.e. the plates would not reach
    below the J2 case to meet the channel), record interference `upper_plates_too_short`.
- `upper_web`: box X ±web_half_width, Y from the idler plate outer face to the horn plate outer
  face, Z [z2 + e + c, z2 + e + c + tp] (wraps the J2 case near end at the top).
- Direct variant (always inline; `knee.mount_side` is read only by the proximal variant):
  - `knee_actuator` (+horn, +idler): `actuator("knee_actuator", +Y, long_dir "up" or "down" per
    knee.case_long_dir, P3, 0, outboard/inboard per knee.horn_dir)`. It sits in the same Y band
    as the J2 case ("inline").
  - `upper_channel_plus`, `upper_channel_minus`: plates perpendicular to X at
    X = x2 ± (W/2 + c + tp/2) (thickness tp), Y spanning between the upper plates' inner faces,
    Z from (j2 case far-end face − c) down to the knee case axis Z + 0.25·(far-end Z − axis Z)
    (they clamp the far half of the knee case by its ±X side faces).
  - If the knee case's Z range overlaps the J2 case's Z range (both in the same Y band), record
    interference `knee_case_into_j2_case` with the overlap in mm — this is the sketch's expected
    finding at L1 = 30.
- Proximal variant (`knee.mount_side` "inboard" or "outboard"; refuse any other value):
  - `knee_actuator` (+horn, +idler): axis +Y on the J2 axis line (coaxial), long_dir "down",
    horn facing AWAY from the upper link (outboard for mount_side outboard, inboard for inboard),
    idler boss touching the matching upper plate's outer face: case starts at plate outer face + hg.
  - `knee_mount`: shelf box X ±W/2, Y from that upper plate's outer face to the knee case outer
    face, Z [case far-end face − tp, case far-end face].
  - `pulley_hip`: cylinder diameter `pulley_diameter`, width `pulley_width`, on the J2 axis, Y
    band starting at the knee horn boss outer face, extending away from the leg.
  - `pulley_knee`: same, on the J3 axis, same Y band.
  - `belt`: box X ±pulley_diameter/2, Y = pulley band, Z [z3, z2]; mass = knee.belt_mass_g.
  - `knee_shaft`: cylinder diameter `shaft_diameter` along Y on the J3 axis, from the outer face
    of the far lower-link plate to the outer face of the near lower-link plate (spans everything
    at the knee).
  - `knee_bearing_in`, `knee_bearing_out`: annular envelopes ID/OD/width from `bearing_id_od_w`,
    centred on each upper plate at J3 (a matching OD hole is cut in that plate). Mass
    `bearing_mass_g` each.

**Lower link (frame `lower`, rotates with c about J3)**
- Direct: `lower_horn_plate`, `lower_idler_plate` on the knee horn/idler boss outer faces
  (perpendicular to Y), outline: disc hub_radius at P3 ∪ rectangle ±plate_width/2 from z3 to
  z4 ∪ disc hub_radius at P4; `lower_web`: box X ±web_half_width, Y between the lower plates'
  outer faces, at the knee case NEAR end: Z [near-end face − c − tp, near-end face − c] when the
  near end is down (case_long_dir "up"), else above the far end — pick the end of the knee case
  that faces away from the J2 case.
- Proximal: `lower_plate_in`, `lower_plate_out` perpendicular to Y, each outside the upper link
  stack at the knee by c: the plate on the belt side sits at pulley outer face + c; the other at
  the other upper plate's outer face + c (bearing envelopes protrude 1 mm, which is < c).
  Outline as above (P3 hub, bar, P4 hub); `lower_web`: box X ±web_half_width, Y between the two
  plates' outer faces, Z [z3 − hub_radius − c − tp, z3 − hub_radius − c] (wraps under the upper
  link's knee hub).
- `foot`: box X ±foot.X/2, Y ±foot.Y/2, Z [z4 − foot.Z, z4] centred under P4, carried in the
  lower frame.

All solids: label as named, colour per frame (body grey, carrier tan, upper blue-grey, j1/j2/knee
actuators dark slate, transmission parts steel grey, foot dark), `shape.label` and `shape.color`
set as in joint_cartridge.py.

## 4. Posing

`pose(solids_by_frame, a, b, c)` applies `T_c`, `T_u`, `T_l` (§1) to the carrier, upper and lower
frame solids with build123d `rotate(Axis(origin, direction), angle)`, composing in the order
lower-about-J3, then upper-about-J2, then carrier-about-J1 (all axes at their neutral positions)
— i.e. rotate a lower solid about the neutral J3 axis by c, then about the neutral J2 axis by b,
then about the J1 axis by a. Check once against the chain formulas: the posed foot box centre must
equal `P4(a,b,c) + Rx(a)·Ry(b+c)·(0,0,−foot.Z/2)` (the pad is rigid in the lower frame and
rotates with it; the first issue of this brief wrote the unrotated offset, which the builder
correctly reported as contradicting rigid posing) within 1e-6 for five fixed test triples
(0,0,0), (12,−35,70), (−30,90,120), (30,−90,0), (15,45,−30); write the maximum error to the report.

The viewer applies the same three rotations in JavaScript to the embedded neutral meshes (embed
P1, P2, P3 and the frame tag per part in MODEL_DATA). Sliders: a ∈ [−45, 45], b ∈ [−120, 120],
c ∈ [−30, 150], starting at the stance pose; a variant label and a "stance" button that resets
to it. Draw a floor plane at the lowest foot Z of the stance pose (visual only). Keep the parts
separation control from the template. No network, no account.

## 5. Checks and report (`geometry-check.json`)

1. `solids`: name, frame, mass_class, mass_g (actuator: 18 fixed; belt, bearings: fixed
   allowances; others: volume × class density), volume_mm3, centroid_mm. Invalid, empty or
   multi-solid parts → ValueError.
2. `neutral_overlaps`: every pair with common volume > 1e-5 mm³, with the volume. Touching faces
   are fine (zero volume). Expected zero for the carrier/plate/boss contacts; anything else is
   listed, not raised.
3. Cradle windows: if any carrier-frame solid or the j2 actuator intersects the cradle at neutral,
   cut from the cradle a rectangular through-window = the XY bbox of the intersecting solids
   expanded by `cradle.window_clearance`, record `cradle_windows` (XY extents) and repeat the
   neutral check. If after that the J1 case or j1_mount still intersects the cradle or the
   `body_envelope`, list it under `inside_shell_envelope` (volume and Z range), not as an
   interference — the shell interior is unknown and that volume is a measured question for the
   physical intake.
4. `sweep`: for every (a, b, c) on the `poses.sweep` grids (inclusive ends; `--quick` doubles the
   steps) pose the leg and test these pairs for common volume > 1e-5 and minimum distance:
   carrier solids vs {cradle, body_envelope, j1_actuator(+horn/idler), j1_mount, neighbours};
   upper solids vs {all carrier solids except the j2 horn/idler bosses they sit on, cradle,
   body_envelope, j1 parts, neighbours}; lower solids vs {all upper solids except the knee
   horn/idler bosses or knee shaft/bearings they sit on, carrier, cradle, body_envelope, j1 parts,
   neighbours}. Skip the nominal intentional contacts (plate on boss, bearing in plate hole,
   shaft in bearing/pulley/plate, belt on pulleys) — list the skipped pairs in the report.
   Record per pair: minimum distance over the sweep, the pose where it occurs, the number of
   colliding poses and up to 8 colliding poses with overlap volume. Summaries: `interferences`
   (pairs with any collision), `near_misses` (no collision, min distance < `clearance_floor`),
   `total_poses`, `colliding_poses`.
5. `stance`: at `poses.stance`: foot bottom Z, overall height = body height_Z − foot bottom Z,
   clock-bottom clearance = −(foot bottom Z), foot centre (X, Y), stance width = 2·|Y|, the
   leg's outermost Y and X extents (all leg solids, posed), and the leg's extents in the neutral
   pose. Also `body_bbox_exceedance`: how far any leg solid reaches outside the body envelope's
   X and Y footprint at stance (mm, per side).
6. `reach`: foot point P4 over the sweep grid: min/max X, Y, Z (kinematic only) and the subset
   with no collision.
7. `mass`: per frame group totals; `leg_total_g` (carrier + upper + lower + foot + 3 × hardware
   allowance; j1 actuator and j1_mount counted in the carrier group as "hip hardware fixed to
   the cradle"); `four_legs_g = 4 × leg_total_g`; `cradle_g`; `moving_about_j2_g` (upper + lower
   + foot + knee allowance). `moving_inertia_about_j2_gmm2` at neutral and at stance: Σ m·r²
   over the moving solids with r = distance of each solid's centroid from the posed J2 axis
   (centroid-lumped; say so). `leg_centroid_stance_mm` in the body frame.
8. Datums (§2) for the three actuators and the shaft/pulley axes, in the neutral body frame.
9. Provenance echo: copy `status`, `provenance`, every `*_provenance` string from the JSON;
   `build123d` version; sha256 of parameters, generator and the STEP; `step_round_trip` as in
   joint_cartridge.py; `no_structural_analysis_or_physical_testing: true`;
   `scope: "Nominal rigid envelopes; discrete pose samples, not a continuous collision proof. No cables, fasteners, stops, encoders, covers, batteries or measured shell interior."`

Print the report to stdout as JSON. Exit 0 whenever the model built, even with interferences.

## 6. Expected result on the example file

The example JSON holds the sketch's own values (P1 Z = −10, d = 12, h2 = 0, L1 = 30); its
`knee.mount_side` is `outboard` so the proximal variant builds (the first issue said `inline`,
which the proximal rule refuses — the builder's report caught that too). Expect,
and do NOT tune away: `j1_case_into_cradle` (the J1 case reaches Z = 0), the J2 case into the
cradle/body (its near end reaches Z = +1), `knee_case_into_j2_case` in the direct variant, and
sweep interferences. The second run `--variant proximal` on the same file must also build. Do not
edit the JSON; a candidate that clears is the design session's work, not yours.

## 7. Done when

- `runtime/cad/venv/bin/python hardware/joints/cad/leg_packaging.py --quick` and
  `... --variant proximal --quick` both exit 0 and write the three outputs under
  `hardware/joints/cad/exports/l02/` (direct) and `hardware/joints/cad/exports/l02-proximal/`
  (proximal; make the default out folder depend on the variant).
- `geometry-check.json` carries every field of §5 and the five pose-formula errors are < 1e-6.
- `preview.html` opens offline; sliders pose the leg; the console is clean (check with a quick
  headless load if a browser is available to you; otherwise say it was not browser-checked).
- A full (non-quick) direct run completes; record its wall time in the report as `sweep_seconds`.
- Write `hardware/joints/cad/briefs/J04-L02-BUILD-BRIEF-REPORT.md`: what was built, the commands you
  ran with their exit codes and wall times, the interference list the example produced for both
  variants (names and overlap mm or mm³), anything in this brief you could not do exactly and
  what you did instead, and anything you noticed that the design session should rule on. Facts
  only; no proposals of a fitted candidate.
- Commit nothing. Touch nothing outside hardware/joints/cad/ (new files: leg_packaging.py,
  leg-viewer-template.html if you need a separate template, exports/l02*/, briefs/J04-L02-BUILD-BRIEF-REPORT.md)
  and runtime/cad/ for scratch. Do not modify joint_cartridge.py, j04-c01.example.json,
  viewer-template.html, exports/*.step of C01, or j04-l02.example.json.
