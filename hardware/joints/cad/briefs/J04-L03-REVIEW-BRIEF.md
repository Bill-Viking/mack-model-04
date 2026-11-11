# J04-L03 — review brief: judge the short-leg build by its own numbers

One page. You are the independent judge of a finished headless build. You did not write the
brief or the build. Rule from the files below; change nothing except the one file you write.

## What was built, and why

The owner ruled on 2026-11-11: short legs under a low base, to match the build-target picture.
The requirement taken from that picture is an under-shell height of 55 mm (allowed 50 to 60,
ASSUMED). A headless builder wrote a new packaging generator and ran two knee variants.

## Files to read (and nothing else)

- `hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF.md` — the brief the builder worked from.
- `hardware/joints/cad/j04-l03.base-short.json` — the parameters.
- `hardware/joints/cad/briefs/J04-L03-BUILD-BRIEF-REPORT.md` — the builder's hand-back.
- `hardware/joints/cad/exports/l03-summary.json` — the headline numbers.
- `hardware/joints/cad/exports/l03-base-direct/geometry-check.json` and the proximal one —
  large; query them with a short script, do not read them whole.
- `hardware/joints/cad/leg_base_packaging.py` — only where a number's meaning is in doubt.
- `docs/review/design-review-2026-11-11.md` — findings 2, 3, 5 and 6 are what this build answers.
- `concepts/raycue-build-target.png` — the picture, if you can view images.

Do not open `STATUS.md`, `OPENER.md` or any `*.log`. No browser. No network.

Browser proof already run by the managing window: both `preview.html` files were captured in
headless Chrome on 2026-11-11 and draw the shell, the base and four legs at the solved stance.

## Calls the managing window made without a judge (overrule any of them)

1. Base 27 mm tall, entirely below the shell; plates 56 mm wide, narrower than the 80 mm shell.
2. Hip-spread actuators flat inside the base; hip-swing actuator flat beside the base at the
   base's level, held by its end faces (adds width, no height).
3. Thigh = two plates; in the direct variant the knee actuator itself is the shank.
4. Round foot, radius 5 mm. Equal links, 30 mm and 30 mm.
5. Stance solved from the height requirement with hip swing = minus half the knee bend.
6. The belt knee carried over from the first iteration as a comparison, not redrawn for this hip.
7. Centre-of-mass inputs ASSUMED: clock 229 g and payload 225 g at the body centre, battery
   118 g just above the base.
8. Hand estimates given to the builder as a cross-check only: stance near (12, −50.6, 101.2)
   degrees; straight-leg under-shell height near 78.2 mm; 66.7 mm at the reference pose.

## Rule on these, each from the model's numbers

1. Did the build follow the brief? Name every deviation that changes what a number means.
2. Cross-check with your own short unrounded script, from the chain in the brief alone: the
   solved stance, the straight-leg height, the reference-pose height and one static-torque row.
   Say where the model agrees and where it does not, and which is right.
3. Is the requirement met (50 to 60 mm)? At what joint angles? Is the foot the lowest solid?
   What collides at that stance?
4. What does the requirement cost? From the height sweep: knee bend, knee torque share and
   reach beyond the face against height. Name the lowest height you would call a workable
   standing pose and say by what criterion.
5. Proportions against the picture's reference values: width across the hips, track, base
   height. For each gap, the one parameter that drives it.
6. Static torque shares of stall at the stance for 4, 3 and 2 feet, against the design
   review's 17, 22 and 33 percent at the hip-spread joint. Better or worse, and why.
7. Stability: support margins, tip angle, the three-foot margins. Say which ASSUMED inputs the
   answer depends on most.
8. Direct against belt knee on equal links: mass, inertia about the hip-swing axis, width,
   clear poses. Is the belt knee worth redrawing for this hip?
9. The three changes that would most improve the next iteration, in order, each with the
   number it is expected to move.

## Hand back

Write `hardware/joints/cad/briefs/J04-L03-REVIEW.md`:
- First line: `VERDICT: CARRY FORWARD | REVISE | STOP` and one sentence.
- Your answers to 1 to 9, numbers to the precision the summary prints.
- `FOR THE OWNER:` at most 120 plain words, everyday language, the model's numbers, no jargon.
- `RULINGS NEEDED:` each as one question a stranger could answer, two or three choices, your
  pick marked, one line of why. You cannot ask; the managing window puts them to the owner.
- `LIMITS:` what you could not check.
