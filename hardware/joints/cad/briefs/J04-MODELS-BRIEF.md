# J04-M01 — build brief: 3D model files a visitor can spin in the browser on the repository page

Quality bar: beyond-Apple quality — the machine notices, the human never checks; one plain
sentence at the moment it is needed; state visible on the surface; nothing superfluous.
Design principle served: ship the whole product. A visitor opens one folder and can turn each
model with the mouse, because the repository host renders `.stl` files as interactive 3D views.

A settled brief, one bounded run. Decisions it does not settle go under OPEN.

## What you build
`hardware/joints/cad/export_models.py`, run with
`runtime/cad/venv/bin/python hardware/joints/cad/export_models.py` (Python 3.12, build123d
0.12.0; no pip, no network, no browser). It imports `joint_cartridge.py`, `leg_packaging.py`
and `leg_animation.py` (read them first; change none of them, nor any parameter file, nor
anything in `hardware/joints/figures/` or `leg_figures.py`, which another builder is writing)
and writes binary STL files, millimetres, into `hardware/joints/models/`:

1. `joint-cartridge.stl` — the J04-C01 joint cartridge assembly from
   `hardware/joints/cad/j04-c01.example.json`, all its solids in one file.
2. `leg-direct-knee.stl` — the front-left leg (carrier, links, three actuator blocks, foot) at
   stance, placement A (`j04-l02.candidate-A-under.json`), direct knee, with the cradle plate.
3. `leg-belt-knee.stl` — the same with the proximal (belt) knee and its transmission envelopes.
4. `mack-four-legs-prototype.stl` — body box, cradle and all four legs at stance, direct knee
   (other legs mirrored the way `leg_animation.py` mirrors them, with correct outward normals).

Each file under 5 MB (coarsen the tessellation tolerance if needed; record the tolerance).
Orient every model Z up. Also write `hardware/joints/models/README.md`:
a table (file, what it is, bounding box in mm, triangle count), one line telling a visitor
"click a file to turn it with the mouse", a line that these are packaging-study envelopes with
benchmark actuator blocks, example dimensions, nothing built or tested, and links to the
editable sources (`../cad/`), the STEP files (`../cad/exports/`) and the study
(`../leg-packaging.md`). Plain words, no first person.

## Checks (write `hardware/joints/models/models-check.json`; exit non-zero on failure)
For each STL: file size equals 84 + 50 × triangle count from its header; bounding box computed
from the written triangles; for files 2 to 4 the box agrees with the model's own extents at
stance within 0.5 mm; no degenerate file (at least 200 triangles); sha256 of each file and of
the script; tessellation tolerance used.

## Hand-back
`STATE:` BUILT or STOPPED · files with sizes and triangle counts · check results · what you
could not check (you did not view the models: say so) · `OPEN:` or none.
End with `MODELS BUILD DONE`.
