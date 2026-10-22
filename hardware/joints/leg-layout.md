# Mack — design the leg before the dock

J04-L01-D02 · 2026-10-22 · **proposed architecture; catalog body size available, hardware unselected**.

Bill put joint and mechanical design ahead of docking controls. The immediate
design unit is one complete leg and its connection to the structural base.
The accepted little-Mac appearance remains the target. The current C01 cartridge
is a synthetic single-pivot study; it is not the finished hip or a size commitment.

For discussion with a coworker: [one-page mechanical review brief](../../output/pdf/mack-mechanical-review-brief.pdf)
(2026-10-22, revision 1). It separates catalog facts from proposals, sketches the
joint chain, compares knee-drive placement and asks four focused review questions.
Its editable authoring source is [build_mechanical_brief.py](../../tools/build_mechanical_brief.py).

## The starting arrangement

Use three powered hinges per leg. Two form the hip; the third forms the knee.
Finish the foot with a small, bounded passive tilt and replaceable rubber-like
pad. Four such legs give twelve driven axes before any separate recovery aid.
This is the engineering baseline proposed for the next study, not a new user
approval of parts, dimensions or performance.

| Part | What it does | Where it mounts |
| --- | --- | --- |
| Hip spread, J1 | Moves the leg outward/inward for stance width and lateral foot placement. | A fore/aft shaft carried by the structural cradle. |
| Hip swing, J2 | Moves the upper leg forward/backward. | A transverse shaft in the carrier rotated by J1. |
| Knee, J3 | Bends the lower leg to lift the foot, shorten the leg and crouch. | A shaft at the upper/lower-link junction, parallel to J2 in the leg frame. |
| Passive foot | Accommodates small local surface angles and contact deformation. | A retained elastomer seat with hard travel limits; no powered ankle. |

The two hip axes may be offset to fit real bearings, motors and wires. They do
not have to intersect at an ideal point. A free ball-and-socket would not supply
the independently controlled, supported rotations required here. A powered ankle
would add mass, wiring and packaging before we have shown a need for independent
foot orientation. Turning the robot comes from coordinated foot placement.

Keep the compact visible link covers and rounded dark feet. Place the hip carrier
under the lower side of the body; its loads go into the cradle. The cosmetic clock
case does not become the bearing bracket. Covers must be removable without
disturbing bearing fits, and must clear the full loaded link and harness sweep.

## Start with a direct knee drive, compare a proximal drive

For the first complete-leg design, use a motor/reducer fixed to the upper link
near the knee, driving J3 through its supported output. Two motors stay near the
body; the knee motor moves with the upper link. This is a straightforward baseline
for isolating joint loads and testing the leg.

Also reserve a comparison with the knee motor beside the hip, driving the knee
through a belt or linkage. Moving that mass inward can reduce leg inertia, but
the complete transmission adds pulleys, supports, tensioning, space and possible
coupling between hip and knee motion. Its routing and motor-to-joint mapping must
be derived; a sketch with an omitted belt is not a completed design.

Choose between them using the actual actuator envelopes, complete leg mass and
inertia, loaded motion requirements, cable clearance and service access. If the
direct knee drive cannot fit the short-leg target or its inertia prevents the
required motion, revise the arrangement before detailed parts are released.
This choice does not authorize ordinary high-reduction hobby servos as suitable
for impacts or self-righting.

## Make the load path and drive path explicit

**Structural load:** foot → lower link → knee bearings and shaft → upper link →
hip-swing bearings → hip carrier → hip-spread bearings → cradle.

**Driving torque:** motor → reduction/coupling → supported shaft/hub → moving link.
Bearing friction and transmission reactions remain real loads; separating these
paths means the motor horn is not the sole support for the robot's leg.

For the next cartridge revision, detail these interfaces together:

| Interface | Proposed construction to develop | Evidence still required |
| --- | --- | --- |
| Radial and moment support | Two spaced bearing supports with a forked carrier where packaging permits. | Actual bearing load spectrum, shaft deflection and fit selection. |
| Torque transfer | Positive keyed, splined or selected actuator-specific shaft/hub connection. | Sized connection and purchased interface; a round loose bore is insufficient. |
| Axial retention | Shoulders, spacers and positive end retention; a located bearing with controlled accommodation for assembly/thermal variation where needed. | Ring-specific retention, tolerance stack and no unintended preload or binding. |
| Motor mounting | Dowel/locating features where needed and accessible retained fasteners. | Alignment, fastener loads, tool access and coupling tolerance. |
| Angle sensing | Output-angle feedback independent of any upstream transmission compliance. | Selected encoder, mounting, reference, resolution and cable route. |
| Stops and harness | Stops tied to structure; guarded flexible service loop. | Qualified stop energy, bend radius, twist, pinch clearance and repeated-cycle test. |
| Foot connection | Mechanically retained pad/seat with hard tilt/compression limits. | Retention under inversion, traction, wear and foot-contact sensing. |

These are construction choices to resolve, not dimensioned manufacturing notes.
The bearing arrangement depends on the chosen bearing type; do not clamp both
rings of both bearings into an accidental preload using generic spacers.

## Motion before strength

First model all three joints together, including the body, neighboring legs,
actuator envelopes, covers, battery and harness. Establish standing, crouching,
foot lift, outward reach and forward/back reach. The first load-bearing prototype
uses one knee-bend branch; the earlier reversible-knee proposal remains a later
recovery investigation, not an instruction to pass through a straight loaded knee.

Longer links increase reach but also change moments and the accepted short-leg
appearance. Wider hips help some foot positions while making the body wider and
loading the cradle differently. These tradeoffs must be solved with the actual
mass and usable dimensions rather than the example cartridge's old dimensions.

Self-righting remains a separate whole-body check under [R04](recovery-envelope.md).
Even a very strong leg cannot push on a floor it cannot reach from an inverted
body. Establish reachable contacts in each direction before deciding whether an
extra recovery mechanism is required. No all-direction recovery is established
by the three-axis arrangement.

## What the motion illustration represents

The conversation illustration shows one front-left leg in front and side
projection. Both views come from the same three-dimensional chain, with body
axes +X forward, +Y left, +Z up. It is dimensionless: upper link 1.0, lower link
0.95 and sideways hip offset 0.25 are illustrative proportions, not measurements.
The displayed body is a reference crop, not the fitted shell.

For angles a (hip spread), b (hip swing), c (knee), use active right-hand rotations:

- P1 = origin of hip spread.
- P2 = P1 + Rx(a) [0, d, 0].
- P3 = P2 + Rx(a) Ry(b) [0, 0, -L1].
- P4 = P3 + Rx(a) Ry(b + c) [0, 0, -L2].

J2 and J3 axes rotate with J1. Positive b moves the upper link toward -X under
this convention. Positive c bends the lower link in the same mathematical sense.
The control labels describe each joint's job; they are not motor sign settings.
The illustration changes pose only. It has no contact solver, collision test,
motor model, mass model or body-stability result. Slider endpoints are viewing
limits, not component or controller limits. It supplies no actuator commands.

## Catalog scale now available

Bill supplied a search screenshot on 2026-10-22. The
[RayCue WB-8 product listing](https://www.raycue.com/products/maclock) independently
confirms **80 × 91 × 112 mm** and **229 g net mass**. The working mapping is
80 mm width, 91 mm depth and 112 mm height, following the screenshot. RayCue's
text does not label the dimension axes, so that mapping still needs a unit check.
These are catalog values, not measurements of Bill's clock or its interior.
The screenshot's 9.9 oz / 0.28 kg conversion is inconsistent with 229 g;
229 g is 8.08 oz / 0.229 kg. Use the manufacturer's metric value.

[catalog-scale.json](catalog-scale.json) records the evidence and separates the
catalog dimensions from proposed leg dimensions. The old C01 example is
40 × 108 × 100 mm including its motor placeholder. That is approximately the
scale of the entire donor body, not a credible repeated compact leg package.
Do not shrink its shafts, bearings and clearances proportionally and assume
that the resulting hardware will carry the load.

The first scaled sketch uses **30 mm upper and lower links**, measured between
joint axes. Four hip-spread origins sit at X = ±30 mm, Y = ±34 mm,
Z = −10 mm relative to the clock's bottom center. The second hip axis is
12 mm outward from the first, rotated by the hip-spread angle. These placements
are proposals; the sketch does not establish available underside mounting space.
It shows the whole catalog body instead of the earlier cropped body.

For a symmetric stance with 12° outward spread and 70° knee bend, the hip swing
is half the knee bend in the opposite sense. Mirror front/rear knee directions
and left/right spread. With a 10 mm high illustrative foot, this produces about
**60.6 mm clearance from the ground to the clock bottom**, **172.6 mm overall
height**, and **111.9 mm between left/right foot centers**. These are calculated
proportions, not measured robot dimensions. A crouch changes the stance width
and body height together. The preview places a floor beneath the resulting feet;
it does not solve contact, balance, friction or collision.

Use the compact [ROBOTIS XL330-M288-T](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)
only as a packaging benchmark: its published case dimensions are
20 × 34 × 26 mm (W × H × D) and its mass is 18 g. Twelve sum to 216 g, before
horns, external bearings, brackets, wiring or links. Its 34 mm case dimension is
already larger than the proposed 30 mm link pitch. Axis positions and case
orientation could permit overhang, but a knee package cannot be treated as a
small circle or presumed to fit inside the cosmetic link. This is the immediate
reason to compare direct and proximal knee drives in actual component CAD.
The reference has plastic gears; no load, impact, wear or continuous-torque
suitability is inferred from its size or published stall torque.

The 229 g donor mass is not a retained-shell mass or a robot target. Adding it
to the 216 g motor example gives 445 g only for the hypothetical combination
of an unchanged clock and twelve bare actuators. Removing donor electronics
changes that subtotal; adding compute, battery and structure changes it again.
Keep the completed-system mass budget open.

## Inputs for the next fitted CAD assembly

Use the catalog envelope for proportion studies now. Confirm the actual model,
axis order and exterior dimensions when the unit is available, then inspect
usable underside space, structural mounting possibilities, retained shell/display
mass and internal keep-outs. These observations belong in
[measurements.csv](../measurements.csv), with their method and uncertainty.

The assembled robot will weigh more than the donor clock. Include all twelve
actuators, cradle, links, bearings, covers, battery, compute, sensors and wiring
in the mass budget. Establish hip locations, complete center of mass and load
cases before sizing motor torque, bearings, shafts and link sections.

Next output: a complete three-axis leg packaging assembly with candidate component
blocks, joint datums, travel/cable envelopes, mass accounting and a list of actual
interferences. Then finish one bearing-supported joint and its restrained fixture.
Docking control work waits behind this joint-design arc.

## Source checks

Read 2026-10-22; references only, no hardware or source imported.

- [Open Dynamic Robot Initiative](https://open-dynamic-robot-initiative.github.io/)
  describes torque-controlled modular actuation. Its
  [hardware repository](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware)
  provides three-degree-of-freedom legs, Solo12 and a leg test stand. These are
  architectural references, not proof of fit or performance for Mack.
- [ROBOTIS XM430-W350 manual](https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/)
  documents current and current-based position modes and explicitly distinguishes
  stall torque from continuous output. It is an actuator-family example, not a
  selected part or a claim of safe backdrivability. Current sensing is not a
  calibrated foot-force measurement.

Mack-specific placement and prototype sequencing above are engineering proposals.
No exact motor, gear ratio, shaft diameter, bearing, material or final travel is
selected in this revision.
