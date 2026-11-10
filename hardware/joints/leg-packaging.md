# Mack — one leg with its actuators in place

J04-L02-D01 · 2026-11-10 · **packaging study with benchmark actuator blocks; nothing selected,
fitted or load-qualified**.

[The leg layout study](leg-layout.md) asked for the next output: one complete three-axis leg
packaged with candidate component blocks, joint datums, travel envelopes, mass accounting and a
list of actual interferences, with the direct knee drive compared against a proximal drive. This
study is that output. Its numbers come from an editable model, [leg_packaging.py](cad/leg_packaging.py),
built from the brief in [cad/briefs/J04-L02-BUILD-BRIEF.md](cad/briefs/J04-L02-BUILD-BRIEF.md);
the builder's hand-back is [cad/briefs/J04-L02-BUILD-BRIEF-REPORT.md](cad/briefs/J04-L02-BUILD-BRIEF-REPORT.md).
Every value below is measured on that model's rigid envelopes, at the poses it sampled. None is a
measurement of Bill's clock, of a purchased part or of a load.

## What the model contains

One front-left leg, built at its neutral pose in the body frame (origin at the clock bottom
centre, +X through the face, +Y left, +Z up), posed by the chain in the layout study:
`P2 = P1 + Rx(a)(0, d, −h2)`, `P3 = P2 + Rx(a)Ry(b)(0, 0, −L1)`, `P4 = P3 + Rx(a)Ry(b+c)(0, 0, −L2)`.
The drop `h2` is new: the sketch had none, and the actuator blocks need one.

| Group | Solids | What they stand for |
| --- | --- | --- |
| Body | `body_envelope`, `cradle` | The WB-8 catalog box (80 × 91 × 112 mm) and a 4 mm structural plate under it. The interior is unknown; anything the model places inside the box is reported as inside-shell volume, never as a clear fit. |
| Hip spread, J1 | `j1_actuator` (+horn, +idler), `j1_mount` | The benchmark actuator block fixed to the cradle, output axis along X. |
| Carrier | two X-plates, two hubs, `carrier_web`, `j2_actuator` (+horn, +idler) | The part J1 turns. It holds the hip-swing actuator by its side faces; the plates sit on the J1 horn and idler, so the J1 output is supported on both sides of the case. |
| Upper link | two Y-plates on the J2 horn and idler, `upper_web` | A hinge frame wrapping the near end of the J2 case: supported on both sides, driven by the horn. |
| Knee, direct | `knee_actuator` in the same Y band as J2, two X-channel plates | The knee actuator rides the upper link, clamped by its side faces; the lower link is a hinge frame on its horn and idler. |
| Knee, proximal | `knee_actuator` coaxial with J2, `knee_mount`, two pulleys, `belt`, `knee_shaft`, two bearing envelopes | The knee actuator stays at the hip axis, on the upper link, and drives the knee through a fixed-length belt; the lower link straddles the upper link on a bearing-supported shaft. |
| Lower link and foot | two Y-plates, `lower_web`, `foot` | A hinge frame down to the foot pivot and a 18 × 16 × 10 mm pad. The passive tilt seat is not modelled. |
| Neighbours | mirrored copies at the stance pose | The other three legs as static envelopes, for leg-to-leg clearance. |

The actuator block is the ROBOTIS XL330-M288-T size and mass benchmark, 20 × 34 × 26 mm and
18 g, output axis along the 26 mm dimension. Its output-axis position along the case is a
recalled value, 11 mm from the near end, **not read from the manufacturer's drawing this sitting**;
the drawing is a download the session did not take without Bill's word. The horn and idler bosses
are proposed 12 × 2 mm envelopes. Plates are 2 mm, printed-polymer density assumed; pulleys,
belt, shaft and bearings are proposed GT2-class envelopes. Each joint carries a 6 g hardware
allowance. None of this selects a part.

## Why the sketch's hips cannot hold these blocks

The layout sketch placed the hip-spread axis 10 mm under the clock bottom with the hip-swing
axis 12 mm outboard and no drop, and 30 + 30 mm links. With a 34 mm actuator case at each joint,
that placement produces the collisions listed in the results below: the J1 case rises into the
cradle, the J2 case's near end rises into the cradle and body, and a direct knee actuator on a
30 mm upper link overlaps the J2 case by the model's measured amount. These are not model defects;
they are the sketch meeting a real case size. The candidates that follow move the hips to clear
them and report what each move costs in height, width and inertia.

### The three placements compared

| Candidate | Hip-spread actuator | Hip-swing actuator | Intent |
| --- | --- | --- | --- |
| A · under | Flush under the cradle, inside the shell footprint | Dropped 23 mm, hanging below the J1 case | Nothing inside the shell; the simplest cradle. |
| C · hip inside | On the cradle top, inside the shell bottom | Just under the cradle | Trades unmeasured shell interior for height. |
| D · hips inside | Inside the shell bottom | Also inside, its axis 9 mm above the clock bottom; the leg exits through a cradle window | Targets the sketch's standing height; needs the most interior and the largest windows. |

Each candidate was run with the direct knee (upper link lengthened so the knee case clears the J2
case) and the proximal knee (sketch-length upper link). The knee actuator sits inboard under the
body for A and C, and outboard at hip level for D, because the inboard position collides with the
opposite leg there.

## Results

Eight runs: the sketch and the three placements, each with the direct knee (upper link 50 mm, the
shortest the model's knee case allows when it hangs output-down) and the proximal knee (the sketch's
30 mm). Geometry and mass below are the same on the coarse and fine pose grids; the interference
counts come from the grid named in each table. The compact record of every run is
[cad/exports/l02-comparison.json](cad/exports/l02-comparison.json); the full reports, STEP files and
viewers of the sketch and of placement A in both drives are in `cad/exports/l02-*/`.

### Stance geometry and mass

At the stance pose (12° spread, hip swing −35°, knee 70°). Height is clock top to foot bottom;
"past shell" is how far the leg's own hardware stands outside the 80 × 91 mm box at that pose.

| Run | Knee | Height, mm | Under the clock, mm | Foot-centre width, mm | Past shell side, mm | Past shell front, mm | Inside the shell | Cradle window, mm | Leg, g | Four legs, g | Swung by the hip swing, g | Σm·r² about hip swing, g·mm² |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sketch | direct | 182.3 | 70.3 | 113.6 | 34.5 | 16.2 | 1.1 cm³ (J1 case in the cradle plate) | X 7–43 · Y 22–62 | 90.5 | 362 | 34.3 | 32,200 |
| sketch | proximal | 182.3 | 70.3 | 113.6 | 73.1 | 10.7 | 1.1 cm³ | X 7–43 · Y 22–62 | 115.4 | 462 | 59.3 | 40,100 |
| A · under | direct | 223.8 | 111.8 | 129.8 | 42.5 | 24.7 | none | none | 97.1 | 388 | 38.5 | 85,800 |
| A · under | proximal | 207.8 | 95.8 | 123.0 | 42.6 | 7.7 | none | none | 117.9 | 471 | 59.3 | 40,100 |
| C · hip inside | direct | 203.7 | 91.7 | 131.4 | 43.4 | 24.7 | 17.7 cm³ (J1 case, Z 0–20) | X 6–48 · Y 17–62 | 97.7 | 391 | 38.5 | 85,800 |
| C · hip inside | proximal | 187.7 | 75.7 | 124.6 | 43.4 | 7.7 | 17.7 cm³ | X 6–48 · Y 17–62 | 118.5 | 474 | 59.3 | 40,100 |
| D · hips inside | direct | 180.9 | 68.9 | 92.4 | 23.9 | 24.7 | 37.1 cm³ (J1 case Z 22–42 and its 19.4 cm³ mount block) plus the J2 case 10.4 cm³ into the box | X 6–48 · Y 11–43 | 120.1 | 481 | 38.5 | 85,800 |
| D · hips inside | proximal | 164.9 | 52.9 | 85.6 | 59.1 | 7.7 | 37.1 cm³ plus 10.4 cm³ | X 6–48 · Y 11–43 | 140.9 | 564 | 59.3 | 40,100 |

Reading the table honestly:

- The sketch's 172.6 mm came from a line drawing. With the blocks in place the same hip origins
  stand 182.3 mm and collide (next section). Every placement that clears the collisions is taller:
  A by 41 mm (direct) or 25 mm (proximal); C by 21 or 5 mm while putting a 17.7 cm³ actuator case
  inside the unmeasured shell bottom; only D comes in under the sketch, by putting both hip cases
  and a mount block inside the shell.
- The proximal rows for the sketch and for D carry the knee actuator outboard (that is the 73 and
  59 mm past the shell side); for A and C it sits inboard under the body, because the inboard
  position collides with the opposite leg at D.
- The direct rows use a 50 mm upper link, the proximal rows 30 mm, so the height and inertia
  differences between the two drives include a 20 mm link difference. With the knee case turned
  output-up the direct link could be 35.5 mm by the same datums; that case was not run.
- D's leg mass includes the 24 g mount block the model fills between a J1 case and the cradle;
  at D that block sits in the hip-swing actuator's path, so D as drawn is not a working placement.

### Where the parts are: placement A, body frame, mm

| Datum | Direct knee | Proximal knee |
| --- | --- | --- |
| J1 hip-spread axis | along X through (27, 29, −14); case X 14–40, Y 6–40, Z −24 to −4; horn face at X 40 | same |
| Cradle | 4 mm plate, Z −4 to 0, inset 2 mm; the J1 case top meets its underside; no window | same |
| Carrier | two X-plates on the J1 horn and idler, 14 mm wide, reaching down to Z −60, web under the J2 case at Z −62.5 | same |
| J2 hip-swing axis | along Y through (27, 46, −37); case X 17–37, Y 33–59, Z −60 to −26 (output end up); horn face at Y 59, outboard | same |
| Upper link | Y-plates at Y 29–31 and 61–63, web over the J2 case at Z −24.5 to −22.5, channel plates at X 15.5 and 38.5 | Y-plates and web as direct, no channels |
| Knee actuator | axis along Y through (27, 46, −87); case Z −98 to −64 (output end down), Y 33–59 | coaxial with J2, mounted inboard on the upper link: case Y 1–27, horn face at Y 1 toward the body centre |
| Knee pivot | the actuator's output at P3 = (27, 46, −87) | Ø5 shaft through P3 = (27, 46, −67), two 5 × 11 × 4 bearing envelopes, Ø12 pulleys at the hip and knee, belt between |
| Foot pivot, neutral | (27, 46, −117) | (27, 46, −97) |
| Foot at stance | centre (35.6, 64.9), bottom Z −111.8 | centre (24.1, 61.5), bottom Z −95.8 |
| Leg box at stance | X 9–70 · Y 6–83 · Z −112 to −4 | X 9–53 · Y −3 to 83 · Z −102 to −4 |
| Foot-pivot reach over the sampled grid, kinematic only | X −53 to 107 · Y −2 to 90 · Z −106 to −3 | smaller by the 20 mm link |

Cable envelopes are **not** modelled: no loop, no bend radius, no cover. The sweep extents above
are the travel envelope of the rigid hardware alone, and a cable route has to be added before any
of these clearances is believed.

### Mass accounting at placement A, per leg

| Item | Direct knee, g | Proximal knee, g |
| --- | --- | --- |
| Three actuator blocks, 18 g each | 54.0 | 54.0 |
| Carrier plates, hubs and web | 10.6 | 10.6 |
| Upper link plates, web and channels | 6.5 | 4.1 |
| Knee mount, two pulleys, belt, Ø5 steel shaft, two bearings | — | 1.4 + 3.7 + 3.0 + 11.9 + 2.0 = 22.0 |
| Lower link plates and web | 4.5 | 5.8 |
| Foot pad | 3.5 | 3.5 |
| Hardware allowance, 6 g per joint | 18.0 | 18.0 |
| **Leg** | **97.1** | **117.9** |
| Four legs | 388 | 471 |
| Cradle plate | 33 | 33 |
| Moving about the hip swing (knee, links, foot, their allowances) | 38.5 | 59.3 |
| Σm·r² about the hip swing, stance / neutral | 85,800 / 98,100 | 40,100 / 48,100 |

The clock itself is 229 g in the catalog; how much of it stays is unmeasured, and battery, compute,
cables and covers are absent, so there is no robot mass here. The proximal knee adds 20.8 g to the
leg and takes 53 percent off the hip-swing inertia at stance, with the link-length caveat above;
the 11.9 g solid steel shaft across the full lower-link width is the largest single transmission
item and is an envelope, not a design.

### Interferences at the stance pose

One pose per run, the stance pose exactly. Each entry is a pair of solids with the overlap volume
the model measured.

| Run | Knee | Own-leg pairs | Shell or cradle pairs | Neighbour pairs | The pairs, largest overlap first (mm³) |
|---|---|---|---|---|---|
| sketch | direct | 13 | 2 | 0 | `knee_actuator`+`j2_actuator` 4869; `j2_actuator`+`j1_actuator` 4809; `knee_actuator`+`j1_actuator` 1025; `knee_actuator`+`carrier_horn_plate` 692; `knee_actuator`+`carrier_web` 642; `upper_idler_plate`+`j1_actuator` 509; … 9 more |
| sketch | proximal | 7 | 2 | 0 | `j2_actuator`+`j1_actuator` 4809; `upper_idler_plate`+`j1_actuator` 599; `j2_actuator`+`body_envelope` 284; `j2_actuator_idler`+`j1_actuator` 226; `upper_web`+`body_envelope` 220; `knee_shaft`+`carrier_web` 157; … 3 more |
| A · under | direct | 7 | 0 | 0 | `knee_actuator`+`carrier_web` 278; `upper_web`+`j2_actuator` 138; `knee_actuator`+`carrier_horn_plate` 101; `upper_web`+`j1_actuator` 85; `upper_idler_plate`+`carrier_horn_plate` 29; `lower_web`+`knee_actuator` 4; … 1 more |
| A · under | proximal | 8 | 0 | 8 | `pulley_hip`+`nb_FR_pulley_hip` 329; `belt`+`nb_FR_belt` 160; `upper_web`+`j2_actuator` 138; `pulley_hip`+`nb_FR_belt` 120; `belt`+`nb_FR_pulley_hip` 120; `lower_plate_in`+`nb_FR_lower_plate_in` 119; … 10 more |
| C · hip inside | direct | 6 | 5 | 0 | `carrier_horn_plate`+`body_envelope` 606; `carrier_idler_plate`+`body_envelope` 606; `knee_actuator`+`carrier_web` 278; `carrier_hub_horn`+`body_envelope` 254; `carrier_hub_idler`+`body_envelope` 254; `upper_web`+`j2_actuator` 138; … 5 more |
| C · hip inside | proximal | 6 | 5 | 5 | `carrier_horn_plate`+`body_envelope` 606; `carrier_idler_plate`+`body_envelope` 606; `carrier_hub_horn`+`body_envelope` 254; `carrier_hub_idler`+`body_envelope` 254; `pulley_hip`+`nb_FR_pulley_hip` 151; `upper_web`+`j2_actuator` 138; … 10 more |
| D · hips inside | direct | 10 | 8 | 0 | `j2_actuator`+`body_envelope` 8827; `j2_actuator`+`j1_mount` 7028; `carrier_horn_plate`+`body_envelope` 1738; `carrier_idler_plate`+`body_envelope` 1738; `upper_web`+`body_envelope` 667; `upper_idler_plate`+`body_envelope` 510; … 12 more |
| D · hips inside | proximal | 9 | 8 | 0 | `j2_actuator`+`body_envelope` 8827; `j2_actuator`+`j1_mount` 7028; `carrier_horn_plate`+`body_envelope` 1738; `carrier_idler_plate`+`body_envelope` 1738; `upper_web`+`body_envelope` 667; `upper_idler_plate`+`body_envelope` 510; … 11 more |

### Interferences over the sampled travel

The coarse grid (spread −30/0/30°, swing −90/−30/30/90°, knee 0/60/120°; 36 poses) for all eight
runs, and the fine grid (steps of 15°, 30° and 30°; 175 poses) for the three runs the repository
carries. "Clear" means no overlapping pair at that pose; the neighbours are the other three legs
frozen at their stance pose.

| Run | Knee | Grid | Poses | Clear of own leg and shell | Clear of everything | Colliding pairs: own / shell / neighbour | Pairs under 1.5 mm |
|---|---|---|---|---|---|---|---|
| sketch | direct | coarse | 36 | 0 | 0 | 31 / 16 / 28 | 27 |
| sketch | proximal | coarse | 36 | 0 | 0 | 28 / 13 / 20 | 28 |
| A · under | direct | coarse | 36 | 0 | 0 | 10 / 3 / 54 | 21 |
| A · under | proximal | coarse | 36 | 0 | 0 | 20 / 5 / 92 | 44 |
| C · hip inside | direct | coarse | 36 | 0 | 0 | 9 / 13 / 53 | 15 |
| C · hip inside | proximal | coarse | 36 | 0 | 0 | 19 / 25 / 94 | 36 |
| D · hips inside | direct | coarse | 36 | 0 | 0 | 16 / 33 / 78 | 24 |
| D · hips inside | proximal | coarse | 36 | 0 | 0 | 29 / 33 / 55 | 39 |
| sketch | direct | fine | 175 | 0 | 0 | 33 / 16 / 39 | 27 |
| A · under | direct | fine | 175 | 0 | 0 | 14 / 4 / 86 | 20 |
| A · under | proximal | fine | 175 | 0 | 0 | 21 / 5 / 113 | 48 |

The named pairs, run by run, are in the reports; the comparison file carries each pair with its
pose count and largest overlap. What they come to:

**The sketch, with these blocks.** The hip-spread case rises 4.0 mm into the cradle plate. The
hip-swing case's upper end stands 11 mm above its axis, so with no drop it runs 4,840 mm³ into the
hip-spread case at every pose and 140 mm³ into the body box at neutral. A direct knee on a 30 mm
upper link overlaps the hip-swing case by 16 mm, 8,320 mm³. These are the three facts that force
the drop `h2` and the longer direct-knee link in every candidate.

**What the candidates fixed.** At A and C no case touches another case at neutral, nothing is
inside the shell at A, and no window is cut at A. At D the model's own mount block fills the 22 mm
between the raised J1 case and the cradle and lands in the J2 case's path (10,613 mm³ at every
pose); D needs a different mount before it can be compared.

**What remains, and why.** Nearly every own-leg collision left at A and C traces to three choices
in how the model draws its hinge frames, not to where the hips are:

1. *Webs that wrap an actuator's output end at 12.5 mm from the axis.* The benchmark case is
   20 mm wide and its output axis sits 11 mm from the end, so the case corner is 14.9 mm from the
   axis. The upper-link web (over the J2 case) and the lower-link web (over the knee case) are
   drawn at 12.5 mm, and they clip the case corners as the joint turns. On the fine grid
   `upper_web + j2_actuator` collides at ±30° and ±60° of swing (138 mm³ at stance) and is clear
   at 0° and ±90°; `lower_web + knee_actuator` collides at knee angles of 30°, 60° and 120°.
   The web stand-off needs to be at least 16.4 mm, or the web must not wrap the output end.
2. *Carrier side plates and web that reach 23 to 26.5 mm below the hip-swing axis* (they hold
   the J2 case by its side faces down to its far end). The knee case on the swinging upper link
   runs into them at ±30° of swing and is past them by ±60° (`knee_actuator + carrier_web`
   278 mm³ at stance), the upper link's idler plate folds into them from ±30° outward, and the
   proximal knee shaft meets the web at ±30°.
   Holding the J2 case above its axis, or by its end faces, frees that swing; the same change
   removes the 104 mm³ neutral overlap between each channel plate and the carrier web.
3. *A 23 mm drop that leaves 2 mm between the J2 case's upper end and the J1 case.* The upper
   web then overlaps the J1 case by 1.5 mm at neutral (198 mm³, 85 mm³ at stance), the J2 case
   grazes the J1 case at the 12° spread (0.2 mm³; 48 mm³ at 30°), and the proximal knee case,
   sitting beside J2 at the same height, clips the J1 case at ±30° and ±60° of swing, and at
   every swing angle at −15° and −30° of spread (130 of 175 fine-grid poses, up to 1,529 mm³). At A
   that is `h2` ≥ 27 or so, costing 4 to 5 mm of height; at C the J1 case is above the cradle and
   the J2 case has the room.

Beyond those, the lower-link web meets the upper link's channel plate when the knee folds to 90° and beyond
(the fold-back limit of this frame), and the lower web overlaps its own two plates by 48 mm³,
which is a drawing seam inside one rigid part, not a collision.

**Neighbours and the shell.** With the direct knee at A the only leg-to-leg contacts are with the
rear leg on the same side: on the fine grid the front leg touches it in 14 of 25 poses at +30° of
rearward swing and in every pose from +60°, and nothing reaches the leg across the body at the
sampled spreads. The leg meets the cradle and the body box only folded up under the body (swing
+90°, 15 of 25 poses, the knee at 60° or more). With the proximal knee at A the inboard knee
actuator's pulley and belt cross the body centreline and meet the opposite front leg's at the
stance pose itself (`pulley_hip + nb_FR_pulley_hip` 329 mm³, `belt + nb_FR_belt` 160 mm³), so an
inboard proximal drive at A needs either a narrower transmission or the knee actuator on the
other side. On the fine grid that variant has 113 colliding neighbour pairs to the direct
knee's 86: 66 with the opposite front leg, at every swing angle, 37 with the rear leg on its own
side and 10 with the diagonal leg. These are range and arrangement limits to carry forward once the frames above are
redrawn, not placement faults.

On the fine grid no pose at A is clear of the leg's own parts: each of the 175 carries between
one and eight own-leg pairs with the direct knee, one to fifteen with the proximal. No single
pair is there at every pose. The upper web into the J1 case (item 3) is there in 105 poses, all
within ±60° of swing; at −30° to −90° and at +30° to +90° the upper link's idler plate is folded
into a carrier plate in every pose (item 2), and the six direct-knee poses with a single pair
are that one. So the clear-pose count stays at zero until all three items are redrawn; the pair
list, not the pose count, is the useful reading of this revision.

**A misnamed check.** The generator reports `upper_plates_too_short 1.0 mm` for every direct run
at A, C and D. Its own datums say otherwise: the J2 case bottom is at Z −60 and the knee case top
at Z −64, a 4.0 mm gap, and the neutral overlap list has no J2–knee pair. The printed number is
that gap less two 1.5 mm clearances, a margin reported as a defect; the datums win, and the check
is noted for the next builder brief.

### Direct against proximal, at placement A

| | Direct knee | Proximal knee |
| --- | --- | --- |
| Leg mass | 97.1 g | 117.9 g (+20.8) |
| Mass the hip swing moves | 38.5 g | 59.3 g |
| Σm·r² about the hip swing at stance | 85,800 g·mm² | 40,100 g·mm² (−53 %) |
| Standing height | 223.8 mm | 207.8 mm |
| Knee hardware past the shell front at stance | 24.7 mm | 7.7 mm |
| Transmission | none | two pulleys, belt, shaft, two bearings, mount: 22 g, 7 more solids |
| Collision classes of its own | knee case into the carrier at ±30° of swing | knee case into the J1 case in 130 of 175 fine-grid poses; shaft into the carrier web; inboard pulley and belt meeting the opposite leg's at the centreline (329 mm³ at stance); belt and pulleys into the cradle at C and D |
| Link length used | 50 mm (35.5 mm possible with the case output-up; not run) | 30 mm |

The numbers favour the proximal drive on inertia and height and the direct drive on mass and
part count, as the layout study expected; the margin on inertia is overstated by the 20 mm link
difference and should be re-run with equal links before it is quoted. Neither is selected.

## Reading these numbers

- Heights and widths are rigid-envelope stance geometry at 12° spread and a 70° knee, with the
  hip swing at half the knee angle. They move together when the leg crouches.
- Inertia about the hip-swing axis is a centroid-lumped sum, Σ m·r² over the moving solids. It
  omits each part's own inertia and every cable, cover and fastener. Use it to compare the two
  knee drives, not as a controller input.
- A sweep collision count is a count over the sampled grid, not a continuous proof, and a clean
  grid does not prove a clear mechanism: stops, cable loops, covers and the passive foot are
  absent, and the body is a box.
- Inside-shell volume is a question for the physical intake, not an answer: the retained shell's
  interior, wall thickness, feet and recesses are unmeasured.

## What this does and does not settle

Settled by the model: the sketch geometry collides with the benchmark block at both hip joints
and at a direct knee; the drop and the longer direct-knee upper link are forced by the case size,
and the proximal drive is what keeps the sketch's link length. Each candidate's standing height,
width beyond the shell, interior claim and knee-drive inertia are now numbers to argue with. The
collisions that remain at the two outside-the-shell placements are named pair by pair, and three
drawing choices in the hinge frames account for nearly all of them, each with the dimension that
clears it.

Not settled: the actuator (the benchmark has plastic gears and an unverified continuous rating),
the shell interior, the retained mass, bearings, couplings, stops, encoders, cable routes, covers,
the passive foot seat and every load. The cradle windows the model cuts are envelope cutouts, not
a structural design. Self-righting reach stays under [R04](recovery-envelope.md).

## Next

1. Redraw the three hinge-frame choices in the generator (web stand-off ≥ 16.4 mm or no wrap;
   carrier plates ending above the hip-swing axis; `h2` ≥ 27 at A), add the output-up knee case
   with a 35.5 mm link, and re-run A in both drives with equal links. A builder's brief; the
   measure is the clear-pose count on the same grid.
2. Read the XL330 drawing (or the drawing of whichever actuator is actually considered) and
   replace the recalled output-axis offset and boss envelopes with drawn values.
3. Physical intake of the actual unit: underside and interior geometry, retained shell mass,
   wall thickness and the dimension-axis mapping ([measurements.csv](../measurements.csv)); it
   decides whether C's 17.7 cm³ inside the shell exists.
4. Add a cable route and loop envelope to each joint before any clearance is believed.
5. Choose the placement and knee drive against those facts, then detail one bearing-supported
   joint and its restrained fixture per [engineering-workflow.md](../engineering-workflow.md).
