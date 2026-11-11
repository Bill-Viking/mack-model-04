# J04-L02-F01 figures build report

STATE: STOPPED

The requested build exited 1 at the J2 actuator callout. The required straight leader crosses the carrier geometry. No SVG files were written. The implementation is a partial draft.

## Files

- `hardware/joints/cad/leg_figures.py` — 26,858 bytes. Partial generator, syntax parsed, build exits non-zero.
- `hardware/joints/figures/figures-check.json` — 1,946 bytes. STOPPED receipt, error, diagnostic limits, source hashes and script hash.
- `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF-REPORT.md` — 4428 bytes. This hand-back.

## Blocking geometry

The FRONT-view convex hull of `j2_actuator` is completely contained in each of `carrier_horn_plate` and `carrier_idler_plate`. Every J2 hull vertex is inside each convex carrier hull, which establishes complete hull containment. A leader reaching J2 in that view must cross a carrier polygon.

A bounded geometric diagnostic also sampled both SIDE and FRONT views, both free margins, leader-start heights from 220 through 778 px in 2 px steps, and 21 points along every J2 hull edge. It found zero unobstructed straight leaders. This is a sampled margin search. The FRONT hull-containment result is exact for the tessellated convex projections.

OPEN: The brief needs a ruling on how to expose and label J2 while retaining its geometry and leader rules. The current views enclose the actuator.

## Numbers and sources

The two models were rebuilt and posed from `hardware/joints/cad/j04-l02.candidate-A-under.json`, using `poses.stance` in a/b/c order. The values are [12.0, -35.0, 70.0] degrees. Model-report agreement passed within 0.000001, and the rounded study cross-checks agreed.

- Direct knee — leg mass 97.0542828117 g, displayed value 97.1 g, from `hardware/joints/cad/exports/l02-comparison.json`, `sweeps["A-under-direct · fine"].mass.leg_total_g`. Standing height 223.7882159432 mm, displayed value 223.8 mm, from the same run, `stance.overall_height_mm`. Upper link 50 mm from the parameter file, `links.L1_direct`. These display values were prepared in memory. No figure was emitted.
- Proximal knee — leg mass 117.8677691009 g, displayed value 117.9 g, from `hardware/joints/cad/exports/l02-comparison.json`, `sweeps["A-under-proximal · fine"].mass.leg_total_g`. Standing height 207.7631838080 mm, displayed value 207.8 mm, from the same run, `stance.overall_height_mm`. Upper link 30 mm from the parameter file, `links.L1_proximal`. These display values were prepared in memory. No figure was emitted.

- Body 80 × 91 × 112 mm comes from the parameter file, `body.width_Y`, `body.depth_X`, `body.height_Z`.
- Actuator 20 × 34 × 26 mm and 18 g come from the parameter file, `actuator.W`, `actuator.H`, `actuator.D`, `actuator.mass_g`.
- Lower link 30 mm comes from the parameter file, `links.L2`.
- The requested 20 mm scale bar and Model 04 / J04-L02 identifiers are read from `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF.md`.
- The actuator count comes from the three actuator blocks in `leg_packaging.Model.build`. Four leg instances come from `leg_animation.LEGS`. Their product is twelve.
- Style constants follow the brief. Type and palette colours are read from `leg-viewer-template.html`.

## Verification and limits

- Ran the requested Python entry point once. It built both models, tessellated 25 direct and 30 proximal front-left/body/cradle solids, and verified rebuilt mass and standing height against the fine-grid report. It then failed at J2 leader placement.
- Ran one bounded, read-only geometric diagnostic with a 45-second alarm. It completed in approximately five seconds.
- Parsed the script with Python AST. Source files `leg_packaging.py`, `leg_animation.py`, the placement-A parameter file, viewer template and comparison report match their HEAD bytes.
- Complete-figure XML, footer, external-reference, font-size, label-overlap and SVG hash checks remain unrun because the build stopped before SVG output.
- SVG pixel rendering was unrun. Browser proofs were unrun here and belong to the caller.
- Brain freshness is unverified. The caller supplied no freshness evidence.
- The original loose PNG and other builders’ files were preserved. No commit, push, network access, GUI launch or permission change was performed.

FAIL — J2 actuator callout cannot satisfy the prescribed straight-leader clearance rule in the current projected carrier geometry.
