# Mack — design review, 2026-11-11

A candid review of the whole project as the repository records it on this date, written at
Bill's request ("review our work so far"). Prepared with AI assistance from the tracked
documents; the cross-document fact digest it rests on is
[FACTS-PASS-BRIEF-REPORT.md](FACTS-PASS-BRIEF-REPORT.md). Nothing here is a decision. Each
finding ends with the action it suggests, for Bill to rule on.

Tags used for numbers: CATALOG (a maker's figure), CALCULATED (from the CAD model or
arithmetic shown), ASSUMED (a planning guess, stated as such), MEASURED (none yet on hardware).

## What is strong

- **The record is honest.** Every study separates catalog facts, assumptions and unproven
  performance, and no document claims hardware that does not exist.
- **The host software works, by the record.** Conversation with a local model, a durable
  memory with inspect/correct/restore, read-only tools, local speech recognition and the
  approved voice run on the development Mac (README, architecture). Not re-run for this review.
- **The control contract is thought through before any motor exists**: bounded named actions,
  deadlines, no replay after restart, a stop path independent of the AI (architecture).
- **The gates are evidence gates** (roadmap G0 to G8) with a written definition of complete
  (product definition P01 to P13).

## Findings, most important first

### 1. Nothing physical has been measured, and nothing is ordered
Three weeks of mechanical work rest on one catalog envelope (80 × 91 × 112 mm, 229 g) whose
axis mapping is unverified, and on one recalled servo dimension. `measurements.csv` is blank.
G1 (measured intake) has been the stated next physical step since 2026-10-20.
**Suggests:** order the printer, the first servo and the measuring tools; measure the clock
and the servo before any further CAD iteration.

### 2. The packaged leg has drifted from the confirmed build target
The build-target image confirmed on 2026-10-20 shows short covered legs under a compact base.
Leg under-body height in that picture is roughly half the body height, about 55 to 60 mm
(ASSUMED, scaled from the image). The J04-L02 packaging study's clear placement stands
223.8 mm with 111.8 mm of leg under the body (CALCULATED). The "final-design concept"
animation made on 2026-11-11 followed the study, not the build target, and is withdrawn from
sharing for that reason.
**Suggests:** make "matches the build target's proportions" a stated requirement of the next
leg iteration, with a number for the allowed under-body height.

### 3. The study never used the base the build target grants
The picture has a compact base directly beneath the Mac, and the system budget lists a
`structural_base`. The packaging model has only a 4 mm cradle plate, so every hip actuator
either hangs below it (tall legs) or intrudes into the unmeasured shell.
**Suggests:** study a base module about 25 to 30 mm tall that houses the four hip-spread
actuators lying flat and carries the battery low; then re-run the leg with only hip swing and
knee in the leg itself.

### 4. There is no budget: mass, power, energy and cost are all blank
`system-budget.csv` has no number in any row. G1's own rule is that numerical targets are
recorded before part selection. A first-pass estimate for discussion only:

| Item | Mass | Tag |
| --- | --- | --- |
| Four legs with benchmark actuators | 388 to 471 g | CALCULATED (J04-L02, placement A) |
| Clock shell and whatever of its 229 g is retained | up to 229 g | CATALOG |
| Battery, two cells of the B04 example chemistry | about 94 to 142 g | CALCULATED from B04's four-cell figures |
| Compute, display, audio, sensors, base structure, harness | 150 to 300 g | ASSUMED |
| **Whole robot** | **about 0.85 to 1.15 kg** | estimate, not a target |

**Suggests:** fill the budget with ranges now and tighten them as parts are measured.

### 5. The benchmark actuator looks marginal for that mass
Static holding torque at the stance pose, from the model's own joint and foot positions
(vertical load only, no motion, no friction), for a 1.0 kg robot:

| Feet on the ground | Load per foot | Hip spread J1 | Hip swing J2 | Knee J3 | J1 as share of 0.52 N·m stall |
| --- | --- | --- | --- | --- | --- |
| 4 | 2.5 N | 0.086 N·m | 0.028 N·m | 0.042 N·m | 17 % |
| 3 (a crawl) | 3.3 N | 0.115 N·m | 0.038 N·m | 0.056 N·m | 22 % |
| 2 (a trot) | 4.9 N | 0.172 N·m | 0.056 N·m | 0.084 N·m | 33 % |

All CALCULATED; the stall figure is CATALOG at 5 V. Small geared servos are usually run
continuously at a fraction of stall, and walking adds dynamic load on top of these static
values. The hip-spread joint carries the most because the foot stands 35 mm outboard of its
axis. No torque requirement exists anywhere in the repository.
**Suggests:** measure the first servo's holding current and temperature at 0.1 and 0.2 N·m
before ordering eleven more; compare the metal-gear sibling in the same case; shorten the
hip-spread lever arm in the next layout.

### 6. The stance is tall and short
At stance the feet stand 76.9 mm apart fore and aft and 128.1 mm side to side (CALCULATED)
under a body whose top is 223.8 mm up. No centre-of-mass estimate or static stability check
exists, and the walk animation checks neither.
**Suggests:** add a centre-of-mass estimate and a support-polygon margin to the next model
run; expect a slow crawl first.

### 7. The onboard computer is the tightest packaging question and is still open
The body's gross volume is about 0.8 litre. The conversation model in use today runs on a
64 GB desktop-class machine. The model strategy already says a smaller onboard model must be
compared after compute, battery and cooling are budgeted, and the product definition wants
ordinary interaction without a home server.
**Suggests:** choose the compute board class early, because it sets the battery, the heat path
and how much conversation quality the no-network mode can have.

### 8. The definition of complete is a multi-stage product, not a first build
P11 (self-righting from every qualified pose), P12 (a camera concealed behind a curved face)
and P13 (autonomous return and recharge) are each a project of their own.
**Suggests:** name a first milestone short of G7, for example "tethered walker": four legs
under the real shell, walking under supervision on bench power, with conversation served from
the development Mac.

### 9. Smaller items
- The electrical design has no rail plan: twelve benchmark actuators can each draw 1.47 A at
  stall (CATALOG), 17.6 A together, on a 5 V rail that must not brown out the computer.
- In the belt-knee model the inboard lower-link plate reaches 5.8 mm below the foot sole at
  stance (CALCULATED from the model, found while drawing the figures). That layout's 207.8 mm
  standing height is measured to the foot, so the plate would touch the ground first; the
  plate needs shortening before the two knee layouts are compared on height.
- Cable routes through three moving joints per leg are still undrawn.
- The build-target image and desktop mock-up carry another company's logo and interface
  look. Worth a deliberate decision before wider publicity.
- An engineer arriving at the repository could not find the joint design. The front page now
  needs the figures, the 3D models and one technical specification.
- Process cost paid on 2026-11-11: a figure build stopped on an over-strict labelling rule,
  and one animation was made against the wrong reference. Both are corrected.

## Three months of spare time: what is realistic
The complete product (G7, P01 to P13) is not a three-month build. A tethered walker as
defined in finding 8 is plausible in about 100 to 140 hands-on hours (ASSUMED: printing,
assembly, wiring, testing), provided parts are ordered now and the first servo measurement
does not force a different actuator size.
