# J04-L02-F01 — figures rerun 1 report

STATE: BUILT

Completed the judge’s rerun-1 ruling from the existing partial generator. Leaders may cross geometry; they cannot intersect each other or any text box. The actuator views use the ruled final x-ray layer, and actuator-space.svg carries the exact disclosure. Leg-axes.svg retains normal far-to-near order with axis marks, arrows and dimensions above the geometry.

The earlier stopped run is superseded by this rerun. No commit or push was made.

## Files

- `hardware/joints/cad/leg_figures.py` — 27878 bytes.
- `hardware/joints/figures/leg-axes.svg` — 36049 bytes.
- `hardware/joints/figures/actuator-space.svg` — 32078 bytes.
- `hardware/joints/figures/knee-layouts.svg` — 47031 bytes.
- `hardware/joints/figures/figures-check.json` — 25750 bytes.
- `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF-REPORT.md` — 5795 bytes.

## Numbers used and sources

The full per-figure numeric provenance is in `hardware/joints/figures/figures-check.json` under `figures.<filename>.numbers`. Values below are read from the artifacts, not from the study’s expected-value sentence.

Parameter source: `hardware/joints/cad/j04-l02.candidate-A-under.json`. Comparison source: `hardware/joints/cad/exports/l02-comparison.json`.

| Figure / quantity | Printed value | File key |
| --- | --- | --- |
| Knee layouts / direct leg mass | 97.1 g | Comparison: `sweeps["A-under-direct · fine"].mass.leg_total_g` |
| Knee layouts / direct standing height and height dimension | 223.8 mm | Comparison: `sweeps["A-under-direct · fine"].stance.overall_height_mm` |
| Knee layouts / direct upper link | 50 mm | Parameters: `links.L1_direct` |
| Knee layouts / proximal leg mass | 117.9 g | Comparison: `sweeps["A-under-proximal · fine"].mass.leg_total_g` |
| Knee layouts / proximal standing height and height dimension | 207.8 mm | Comparison: `sweeps["A-under-proximal · fine"].stance.overall_height_mm` |
| Knee layouts / proximal upper link | 30 mm | Parameters: `links.L1_proximal` |
| Leg axes / body | 80 × 91 × 112 mm | Parameters: `body.width_Y`, `body.depth_X`, `body.height_Z` |
| Leg axes / links | 50 mm; 30 mm | Parameters: `links.L1_direct`, `links.L2` |
| Actuator space / block | 20 × 34 × 26 mm · 18 g | Parameters: `actuator.W`, `actuator.H`, `actuator.D`, `actuator.mass_g` |
| Actuator space / counts | Three per leg · twelve in all | `leg_packaging.py`: `Model.build` actuator blocks; `leg_animation.py`: `LEGS` × actuator count |
| Leg axes and actuator space / joint numbers | J1, J2, J3 | `leg_packaging.py`: `Model.axes` and `Model.build` named actuators |
| All / scale bar | 20 mm | `briefs/J04-L02-FIGURES-BRIEF.md`: Drawing method / scale bar |
| All / identifiers | Model 04; J04-L02 | Same brief: masthead and footer |

The stance is [12.0, -35.0, 70.0] degrees in a/b/c order, read from `poses.stance`. Each view uses the same 2.2 px/mm projection scale; the 20 mm bar spans 44 px. The titles and scope statements follow the brief. Colours come from `leg-viewer-template.html` and each CAD part’s model metadata.

## Checks run

- Ran `PYTHONDONTWRITEBYTECODE=1 runtime/cad/venv/bin/python hardware/joints/cad/leg_figures.py`; exit 0. The generator enforces a 180-second alarm.
- Rebuilt and posed direct and proximal placement A. Tessellated 25 direct and 30 proximal solids (front-left leg, body and cradle only). Both parameter fingerprints match the fine-grid reports. Recomputed mass and standing height agree within 0.000001; all six rounded study cross-check values agree.
- Each SVG parses as XML, contains the exact footer, uses no external reference, and has no font below 24 px. Titles are 44 px. The background and viewBox match the brief.
- All text boxes are mutually clear and clear of every drawn polygon bounding box. Feature labels are stacked at least 56 px apart in each margin. Leaders are straight, end in feature dots, and do not cross or touch another leader or pass through any text box. Geometry crossings follow the rerun ruling.
- `leg-axes.svg`: 5 feature labels, 5 leaders, 14 text boxes; overlap assertions passed.
- `actuator-space.svg`: 3 feature labels, 3 leaders, 14 text boxes; overlap assertions passed.
- `knee-layouts.svg`: 3 feature labels, 3 leaders, 18 text boxes; overlap assertions passed.
- Independently parsed the written SVGs and verified actual polygon order against the receipt: normal depth order in leg-axes; all three actuator blocks last in each actuator-space view; knee actuator and transmission last in the knee views. Equal scales and aligned knee ground lines are recorded in the check file.
- Recomputed every recorded output and source SHA-256 against disk. The check file records the three SVG hashes and script hash. `git diff --check` passed. The model, animation, parameter, template and comparison source files have no working-tree diff.

## Limits

- SVGs were not rendered to pixels. Visual quality at phone size, actual font metrics and raster appearance remain unproved.
- Browser and GUI proofs are UNRUN here and belong to the caller. No browser or GUI application was launched.
- Brain freshness is unverified: no supplied evidence established it. No wake pull or heartbeat kick was run.
- These are rigid packaging-envelope illustrations, preserving the model’s known interferences. No physical testing, load qualification or new collision acceptance is claimed.
- No network, package installation, commit, push, permission change or safety-check change was performed. Unrelated builder files and the existing loose PNG were not edited. No STATUS, opener or hub file was written.

OPEN: none.

FIGURES BUILD DONE — Three model-derived SVGs and figures-check.json built; headless checks passed; pixel and browser proofs unrun.
