# J04-L03 — review brief: judge the short-leg build by its own numbers

You are the independent judge of a finished headless build. You wrote neither the brief nor the
build. Rule from the files below; change nothing except the one file you write. The owner ruled
on 2026-11-11: short legs under a low base, to match the build-target picture. The requirement
taken from the picture is an under-shell height of 55 mm (allowed 50 to 60, ASSUMED).

## Row

Lane RayCue/Research, project status to-do: "Read the review of the J04-L03 build, put its
rulings to the owner". A project lane's work; there is no build-queue row.

## Commits

`bc37ddd` (parameters and build brief) · `f0e3c51` (generator, both runs, summary, report).

## Gate output

From the builder's report: generator runs exit 0 (quick, direct full, proximal full); its own
verification exit 0 on the second run (the first stopped on a verifier error, corrected);
five-pose centroid error 1.4e-14 mm direct, 3.1e-14 mm proximal, limit 1e-6; STEP re-import 80
and 112 valid solids; inputs matched their pre-build SHA-256. Browser proof by the managing
window: both `preview.html` files captured in headless Chrome, each draws shell, base, four legs.

## Real-case numbers

Direct knee at 55.0 mm: hip spread 12.0, hip swing -50.6, knee 101.2 degrees; overall height
167.0 mm (first iteration 223.8); straight leg 78.2 mm; width across hips 158.5 mm (shell 80);
25.8 mm beyond the face; base 27.0 mm below the shell; track 105.3, wheelbase 56.3 mm; leg
90.5 g; robot 981.5 g; hip-spread / knee torque share of stall for 1.0 kg: 13 / 12 percent on
four feet, 18 / 17 on three, 27 / 25 on two; margins 28.1 mm fore-aft, 52.6 mm sideways, 0.0 mm
with one foot lifted; 175 poses, 21 clear (first iteration 0); `ground_contact_ok` false (a
shank channel 1.1 mm below the foot); one own-leg overlap at the stance, 32.8 mm³.
Belt knee at 55.0 mm: stance 12.0 / -51.5 / 103.1; ground contact true; leg 118.2 g; robot
1,092.2 g; neutral envelope 249.8 mm wide; 25 of 175 poses clear.

## Files to read

- `hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF.md` and `j04-l03.base-short.json` beside the generator.
- `hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF-REPORT.md` and `exports/l03-summary.json`.
- `exports/l03-base-direct/geometry-check.json` and the proximal one: large; query by script.
- `hardware/joints/cad/leg_base_packaging.py`, only where a number's meaning is in doubt.
- `docs/review/design-review-2026-11-11.md`, findings 2, 3, 5, 6; `concepts/raycue-build-target.png`.

Do not open `STATUS.md`, `OPENER.md` or any `*.log`. No browser. No network.

## Calls made without a judge (overrule any)

Base 27 mm, wholly below the shell, plates 56 mm wide · hip-spread actuators flat inside it;
hip-swing actuator flat beside it at its level · thigh = two plates; direct knee actuator is the
shank · round foot r 5; equal links 30 / 30 · stance solved from the height with hip swing =
minus half the knee bend · belt knee carried over, not redrawn · CoM inputs ASSUMED (clock
229 g, payload 225 g at the body centre, battery 118 g just above the base).

## Rule on these, from the model's numbers

1. Did the build follow the brief? Name each deviation that changes what a number means.
2. Cross-check with your own unrounded script from the brief's chain: the solved stance, the
   straight-leg height and one static-torque row. Where do you and the model differ, who is right?
3. Is the requirement met? At what angles? Is the foot the lowest solid? What collides there?
4. What does the requirement cost: knee bend, knee torque share and reach beyond the face
   against height. Name the lowest height you would call a workable standing pose, and why.
5. Proportions against the picture's reference values; for each gap, the parameter driving it.
6. Torque shares against the design review's 17, 22 and 33 percent at the hip-spread joint.
7. Stability: margins, tip angle, three-foot margins; which ASSUMED inputs matter most.
8. Direct against belt knee: mass, inertia, width, clear poses. Is the belt knee worth redrawing?
9. The three changes that most improve the next iteration, each with the number it should move.

## Hand back

Write `hardware/joints/cad/briefs/J04-L03-REVIEW.md`: answers 1 to 9; then `FOR THE OWNER:` at
most 120 plain everyday words with the model's numbers; `RULINGS NEEDED:` each one question a
stranger could answer, two or three choices, your pick marked, one line of why (you cannot ask;
the managing window puts them to the owner); `LIMITS:` what you could not check. End with the
verdict line the launcher asks for: CARRY FORWARD, REVISE or STOP, and one sentence.
