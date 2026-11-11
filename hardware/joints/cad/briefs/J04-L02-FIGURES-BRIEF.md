# J04-L02-F01 — build brief: three labelled still figures of the leg, drawn from the CAD model

Quality bar: beyond-Apple quality — the machine notices, the human never checks; one plain
sentence at the moment it is needed; state visible on the surface; nothing superfluous.
Design principle served: make the interface truthful. Every outline and number in a figure is
computed from the model or read from its reports; nothing is typed from memory.

A settled brief with no open ruling. If you meet a decision it does not settle, stop and return
it under OPEN. One bounded run.

## RULING for rerun 2 (2026-11-11, from the judge after viewing the rendered figures; overrides earlier text where they differ)

The three figures rendered and are truthful, but the leg is too small to read on a phone and
the link dimensions in figure 1 cross each other. Keep everything that works; change only this:
1. SCALE. In `leg-axes.svg` and `actuator-space.svg` draw the body CROPPED: only its lowest
   30 mm, closed at the top by a dashed break line, and scale each view so the leg from the
   cradle plate to the ground line fills at least 58 % of the canvas height (about 580 px).
   The body label becomes `Body (clock) 80 × 91 × 112 mm · cropped`. In `knee-layouts.svg`
   keep the whole body (the height comparison needs it) and scale so the taller layout fills
   about 68 % of the canvas height.
2. LINK DIMENSIONS in `leg-axes.svg`: one dimension line per link, parallel to that link,
   offset 30 px to the side away from the label column, with short perpendicular ticks at its
   two axis points and its text centred beside the line: `Upper link 50 mm`, `Lower link 30 mm`
   (values still read from the parameters). The two dimension lines must not cross each other
   or sit on a label.
3. Add under the FRONT/SIDE captions of `leg-axes.svg` one small legend line:
   `ring = joint axis seen end-on · dash-dot = joint axis in the page`.
4. GROUND LINE stays at the foot's lowest point. In the hand-back, list every solid whose
   projection extends below that line in any view, with how many millimetres (the belt-knee
   view shows one); do not hide or clip it.
5. Leaders in one view must not cross each other (reorder the label column top to bottom by
   the height of the feature each label points at).

## RULING for rerun 1 (2026-11-11, from the judge; overrides the LABEL RULE below where they differ)

The first run stopped correctly: the J2 actuator sits inside the carrier plates, so no straight
leader can reach it without crossing leg geometry. Ruling:
- Leaders MAY cross leg geometry. They may not cross another leader or pass through another
  label's text box. Label text boxes still may not intersect each other or any drawn leg
  polygon's bounding box (labels stay in the free margins).
- In `actuator-space.svg` the three actuator blocks are drawn LAST, on top of everything in
  each view regardless of depth (an x-ray view), solid dark with the white outline, and the
  figure says so in one small line: `Actuators drawn on top; the hip-swing actuator sits inside its carrier`.
- In `knee-layouts.svg` the knee actuator and the belt, pulleys and shaft are likewise drawn on top.
- In `leg-axes.svg` normal painter order stays; axis marks, arrows and dimension lines are
  drawn on top of the geometry.
A partial `leg_figures.py` from the first run exists; continue from it.

## What you build

`hardware/joints/cad/leg_figures.py`, run with
`runtime/cad/venv/bin/python hardware/joints/cad/leg_figures.py` (Python 3.12, build123d 0.12.0;
no pip, no network, no browser). It imports `leg_packaging.py` (read it and
`leg_animation.py` first for how the model is built, posed and tessellated; change neither),
builds placement A from `hardware/joints/cad/j04-l02.candidate-A-under.json` with the direct
knee and again with the proximal knee, poses the front-left leg at stance (12, -35, 70), and
writes three SVG files into a new folder `hardware/joints/figures/`:

1. `leg-axes.svg` — "One leg, three powered axes".
2. `actuator-space.svg` — "Where the three actuators sit".
3. `knee-layouts.svg` — "Two knee layouts, neither chosen".

Plus `figures-check.json` (see Checks). No other file changes.

## Drawing method (all three)

Orthographic line-and-fill drawings, engineering style. For each posed solid take its
tessellated vertices, project them onto the view plane and draw the 2D convex hull as a filled
polygon with a thin darker outline, painter-sorted far to near along the view direction.
- SIDE view: looking along −Y from the robot's left (X to the right = forward, Z up).
- FRONT view: looking along −X from the front (Y horizontal, Z up).
Same millimetre scale in every view of one figure; state it with a 20 mm scale bar. Draw the
body as the 80 x 91 x 112 mm box outline in thin grey, the cradle plate, and a ground line at
the foot's lowest point. Only the front-left leg is drawn (plus body and cradle); say
"front-left leg shown" in small text.

Canvas: `viewBox="0 0 1600 1000"`, background #f4f1e8, palette and type colours taken from
`leg-viewer-template.html`. Font stack `Helvetica, Arial, sans-serif`. No text smaller than
24 px; titles 44 px. The figures are viewed on phones: prefer few, large labels.

LABEL RULE (the part that usually goes wrong): no label or leader may cross or sit on the leg
geometry or on another label. Put labels in a column in the free margin beside each view,
stacked at least 56 px apart, each joined to its feature by one straight thin leader ending in
a small dot on the feature. Compute each label's text box (estimate width as 0.56 x font size
x characters) and assert in code that no two label boxes intersect and that no label box
intersects any drawn leg polygon's bounding box; fail the run if they do.

Every figure carries, bottom left, 24 px:
`CAD packaging study J04-L02 · example dimensions · nothing is built or tested`
and top left a small-caps line `M.A.C. MODEL 04 · MECHANICAL DEVELOPMENT` above the title.

## Figure 1 — `leg-axes.svg`
SIDE view on the left half, FRONT view on the right half. Leg parts in the model's colours.
Mark each joint axis: where an axis is perpendicular to the view, a ring with a centre dot at
its point (P1, P2 or P3); where it lies in the view plane, a dash-dot centre line through it.
Add one curved double-headed arrow per joint in the view where its motion is visible (J1 in
FRONT, J2 and J3 in SIDE). Labels: `J1 hip spread`, `J2 hip swing`, `J3 knee`, `Foot`,
`Body (clock) 80 × 91 × 112 mm`. Dimension the two link lengths on the SIDE view from the
model (hip-swing axis to knee axis, knee axis to foot point), e.g. `50 mm`, `30 mm`, read from
the parameters.

## Figure 2 — `actuator-space.svg`
Same two views. Everything except the three actuator blocks drawn pale (links, carrier, body
at about 35 % strength). The three actuator blocks drawn solid dark slate with a white 2 px
outline. One label per block: `J1 actuator`, `J2 actuator`, `J3 actuator (knee)`. One callout
box in free space, text read from the parameter file's actuator entry:
`Each block: 20 × 34 × 26 mm · 18 g` and under it `Size and mass benchmark, not a selected motor`.
Also one line: `Three per leg · twelve in all`.

## Figure 3 — `knee-layouts.svg`
Two SIDE views side by side at one scale, ground lines aligned: left `Direct knee` (actuator
at the knee), right `Belt-driven knee` (actuator near the hip; draw its pulleys, belt and shaft
envelopes in an accent colour and label `belt and pulleys`). In each, the knee actuator block
is drawn dark and labelled `knee actuator`. Under each view a three-line fact block, values
read from `hardware/joints/cad/exports/l02-comparison.json` (find the placement-A direct and
proximal runs; if a value is not there, compute it with `leg_packaging`'s own report functions):
`Leg mass <x> g` · `Standing height <y> mm` · `Upper link <L1> mm`.
Expected from the study, for your cross-check only (do not type them in): direct 97.1 g,
223.8 mm, 50 mm; belt 117.9 g, 207.8 mm, 30 mm. If your numbers differ, stop and report.
A height dimension line from ground to clock top beside each view.

## Checks (`figures-check.json`, and exit non-zero on failure)
Each SVG parses as XML; has the footer line; uses no external reference; font sizes ≥ 24;
label-overlap assertions passed (count of labels per figure recorded); every number printed in
a figure is listed with the file and key it was read from; sha256 of the three SVGs and of the
script.

## Hand-back
`STATE:` BUILT or STOPPED · files with sizes · the numbers used and their sources · what you
could not check (you did not render the SVGs to pixels: say so) · `OPEN:` or none.
End with `FIGURES BUILD DONE`.
