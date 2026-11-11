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

---

# J04-L02-F01 — figures rerun 2 report

STATE: BUILT

Written 2026-11-11T09:51:03-08:00.

This rerun supersedes the rerun-1 scale and dimension placement recorded above. Both cropped figures show only the lowest 30 mm of the body, with a dashed top break. Each leg spans 580 px from cradle top to foot-ground. The knee comparison retains both complete bodies, a shared scale and aligned foot-ground lines. Its taller layout spans 680 px.

Implementation choices within the ruling were to place the leg-axes SIDE feature column on the left and the two link dimensions 30 px to its right, centre the horizontal dimension text beside each line in the free right margin, wrap the cropped-body label and actuator callout, and move captions and fact blocks to retain clear margins at the larger scale. The two main dimension lines are parallel to their projected links and have perpendicular endpoint ticks. Feature labels follow their anchor heights.

The normal painter order, final x-ray layers, model colours, axis marks, arrows and report-derived facts are retained. The exact axis legend and x-ray disclosure are present.

## Files

- `hardware/joints/cad/leg_figures.py` — 32002 bytes.
- `hardware/joints/figures/leg-axes.svg` — 36621 bytes.
- `hardware/joints/figures/actuator-space.svg` — 32603 bytes.
- `hardware/joints/figures/knee-layouts.svg` — 47054 bytes.
- `hardware/joints/figures/figures-check.json` — 30480 bytes.
- `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF-REPORT.md` — 14116 bytes after this append.

## Numbers used and sources

The table below is generated from the final check file. It includes every printed numeric token, grouped by source. The check file also records every occurrence by figure. Written-number counts come from the model actuator blocks and the animation leg inventory.

| Printed value | Source file | Key |
| --- | --- | --- |
| 04 | `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF.md` | `Drawing method / masthead` |
| 04 | `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF.md` | `Drawing method / footer / study identifier` |
| 02 | `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF.md` | `Drawing method / footer / study identifier` |
| 2 | `hardware/joints/cad/leg_packaging.py` | `Model.axes[1] / hip swing` |
| 3 | `hardware/joints/cad/leg_packaging.py` | `Model.axes[2] / knee` |
| 80 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `body.width_Y` |
| 91 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `body.depth_X` |
| 112 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `body.height_Z` |
| 1 | `hardware/joints/cad/leg_packaging.py` | `Model.axes[0] / hip spread` |
| 50 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `links.L1_direct` |
| 30 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `links.L2` |
| 20 | `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF.md` | `Drawing method / scale bar` |
| 2 | `hardware/joints/cad/leg_packaging.py` | `Model.build / j2_actuator` |
| 3 | `hardware/joints/cad/leg_packaging.py` | `Model.build / knee_actuator / third axis` |
| 1 | `hardware/joints/cad/leg_packaging.py` | `Model.build / j1_actuator` |
| 20 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `actuator.W` |
| 34 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `actuator.H` |
| 26 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `actuator.D` |
| 18 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `actuator.mass_g` |
| Three | `hardware/joints/cad/leg_packaging.py` | `Model.build / actuator blocks per leg` |
| twelve | `hardware/joints/cad/leg_animation.py` | `LEGS × Model.build actuator count` |
| 223.8 | `hardware/joints/cad/exports/l02-comparison.json` | `sweeps.A-under-direct · fine.stance.overall_height_mm` |
| 97.1 | `hardware/joints/cad/exports/l02-comparison.json` | `sweeps.A-under-direct · fine.mass.leg_total_g` |
| 207.8 | `hardware/joints/cad/exports/l02-comparison.json` | `sweeps.A-under-proximal · fine.stance.overall_height_mm` |
| 117.9 | `hardware/joints/cad/exports/l02-comparison.json` | `sweeps.A-under-proximal · fine.mass.leg_total_g` |
| 30 | `hardware/joints/cad/j04-l02.candidate-A-under.json` | `links.L1_proximal` |

The stance is read from `j04-l02.candidate-A-under.json`, `poses.stance`. Body crop and scale targets come from the same brief’s rerun-2 ruling. Both rebuilt masses and standing heights match the fine-grid comparison reports within 0.000001. All six rounded study cross-check values agree.

| Figure | Shared scale, px/mm | Labels | Text boxes | Leaders |
| --- | --- | --- | --- | --- |
| `leg-axes.svg` | 5.188382292 | 5 | 15 | 5 |
| `actuator-space.svg` | 5.188382292 | 3 | 14 | 3 |
| `knee-layouts.svg` | 3.038587162 | 3 | 18 | 3 |

## Solids below the ground line

Ground is the foot’s lowest Z point from the model’s stance report. The following list covers every view in all three figures. No solid is clipped at ground.

| Figure | View | Solid | Ground Z, mm | Lowest projected Z, mm | Below ground, mm |
| --- | --- | --- | --- | --- | --- |
| `knee-layouts.svg` | proximal | `lower_plate_in` | -95.763183808 | -101.585841173 | 5.822657365 |

This is the complete below-ground list. The four direct-knee views in the first two figures and the direct-knee comparison view have no solid below their foot-ground line. The listed proximal solid is computed from its posed tessellated vertices and is visible below the line.

## Checks run

- Ran the requested CAD interpreter and generator with a 180-second alarm. The first invocation stopped on the belt label exceeding the right margin. The second stopped on crossing link dimensions. Both stopped before writing any SVG. Corrected those layout failures, then the final invocation exited 0 and wrote the complete set.
- Built and posed 25 direct and 30 proximal front-left/body/cradle solids. Parameter SHA-256 values agree with the source reports. Normal drawing uses far-to-near order. The ruled actuator and transmission overlays remain final layers.
- Generator assertions passed for XML parsing, exact footer, local-only references, minimum 24 px type, text-box separation from every solid bounding box and other text, label stacks of at least 56 px, anchor-height ordering, leader separation from all text and other leaders, dimension-line separation, dimensions clear of all text, and all solid extents inside the canvas.
- An independent read of the written SVGs and JSON passed numeric-token provenance, every source/output SHA-256, XML, footer, font sizes, reference checks, actual painter/x-ray order, body paths and dashed break lines, 580 px cropped leg spans, equal scales per figure, aligned comparison ground lines, 680 px taller-layout span, and 30 px dimension offsets with parallel lines.
- `git diff --check` passed. The model, animation, parameter, comparison, template and brief source files have no working-tree diff.

## Fingerprints

| File | SHA-256 |
| --- | --- |
| `hardware/joints/cad/leg_figures.py` | `0a8ad8bc4bff135e36f6e5325f45a14dd8065a308941ed86f6b678fd0a9dd704` |
| `hardware/joints/figures/leg-axes.svg` | `5ed1dcf14bacbdde8013f23b308e00c036d47af85bd3db34337e525e910e86cf` |
| `hardware/joints/figures/actuator-space.svg` | `f5836e17d112ce37ca0c81814354e6d3030fce891ad4e015b0b533ba99276e92` |
| `hardware/joints/figures/knee-layouts.svg` | `bf098ce61b34dfc826f3e358da7be4f51972f63f3412ac3461b7a94dcae1da06` |

## Limits

- SVGs were not rendered to pixels. Phone-size appearance, actual font metrics and raster quality remain unproved.
- Browser and GUI proofs are UNRUN here and belong to the caller. No browser or GUI application was launched.
- Brain freshness is unverified because no supplied evidence established it. No wake pull or heartbeat kick ran.
- These remain rigid packaging-envelope illustrations. Physical testing, load qualification and collision acceptance are outside this build.
- Writes were confined to the requested script, three SVGs, check JSON and this report. Unrelated concurrent builder work was left alone. No commit, push, network request, package installation, permission change, hub stamp, STATUS edit or opener write occurred.

OPEN: none.

FIGURES BUILD DONE — Three SVGs rebuilt to rerun-2 ruling; headless checks passed; pixel and browser proofs unrun.
