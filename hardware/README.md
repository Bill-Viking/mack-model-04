# M.A.C. Model 04 — hardware workspace

The original RayCue shell and accepted four-leg appearance are the starting constraints. All dimensions and loads need measurement.

## Existing design files

- [Screen bezel STL](../vendor/macintosh-mini/maclock-screen-bezel/maclock-screen-bezel.stl): upstream printable frame and clips.
- [Screen bezel STEP](../vendor/macintosh-mini/maclock-screen-bezel/maclock-screen-bezel.step): editable solids.
- [CAD parameters](../vendor/macintosh-mini/maclock-screen-bezel/params.py) and [geometry source](../vendor/macintosh-mini/maclock-screen-bezel/bezel.py): unchanged build123d source.
- [Breakout schematic](../vendor/macintosh-mini/maclock-pcb/maclock-breakout.kicad_sch) and [board layout](../vendor/macintosh-mini/maclock-pcb/maclock-breakout.kicad_pcb): KiCad reference, not approved Mack wiring.
- [Upstream build guide](../vendor/macintosh-mini/BUILD.md): read with [our corrections](../docs/references.md).

The source location and CERN-OHL-S-2.0 notices travel with the CAD and PCB. Create adaptations outside `vendor/` with their required notices; leave the imported originals unchanged.

## Design inputs

[measurements.csv](measurements.csv) records observations. Empty values mean unknown, not zero. [parts.csv](parts.csv) is a candidate list, not an order list. Unspecified counts remain empty.

Measure mounting points from named datums. Record outside versus inside clearances and hole centers. Weigh the complete clock and removable pieces so the robot mass budget does not double-count them.

## Printing and assembly

Initial recommendation: an A1-class FDM printer. PLA for fit checks, PETG for candidate housings/brackets, and TPU for feet. Print parts separately; multicolor equipment is optional. [Research notes](../docs/research-notes.md) contain source links and the estimated printer budget.

Design around actual servo dimensions and shafts. Use purchased fasteners and joint bearings/bushings where appropriate. Choose print orientation and walls for the loads, then test. A good-looking print is not proof of load capacity.

Open checks: clock revision, bezel fit, motor/battery placement, total mass and balance, shared pin map, regulated compute supply, motor power, and one-leg range/load/current/stopping.
