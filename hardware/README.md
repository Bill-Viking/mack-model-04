# M.A.C. Model 04 — hardware workspace

The original RayCue shell and accepted four-leg appearance are the starting constraints. All dimensions and loads need measurement.

The [integration plan](integration-plan.md) treats electronics, sensing, battery, structure and walking as one assembly. The [product definition](../docs/product-spec.md) sets the completion requirements. Sensor methods and packaging zones are proposed; no wiring or motor selection is approved yet.

## Mack joint and recovery concept

The [J04 design study](joints/README.md) proposes three powered axes per leg, a
bearing-supported cartridge, compliant feet, protective frame rails and a reserved
rear recovery-arm interface. It includes a [concept drawing](joints/joint-concept.svg),
load calculations to perform and a staged recovery test plan. This is a design
proposal, not printable load-qualified CAD.

## Direct CAD and the Dell engineering tools

The [first J04-C01 cartridge](joints/cad/README.md) has editable build123d source,
example parameters, STEP solids and an interactive offline preview. The Mac can
generate and check this geometry directly. It is an untoleranced packaging study;
the RayCue dimensions and purchased components remain unknown.

Bill's home Dell has personal Creo and Ansys installations. The
[engineering workflow](engineering-workflow.md) defines their roles, load cases,
prototype sequence and Protolabs release package. The [Dell brief](dell-cad-handoff.md)
starts with actual version/module inspection and a neutral-format import trial.
No Dell connection, native CAD import, FEA result or manufacturing order is claimed.

## Existing design files

The [F04 face and vision study](display-and-vision.md) compares a curved clear
cover with concealed border cameras, a folded beamsplitter display and true
under-display OLED. It includes a [section drawing](face-optics-concept.svg),
documented component leads and a removable optical-fixture plan. No optical
performance or fit has been demonstrated yet.

- [Screen bezel STL](../vendor/macintosh-mini/maclock-screen-bezel/maclock-screen-bezel.stl): upstream printable frame and clips.
- [Screen bezel STEP](../vendor/macintosh-mini/maclock-screen-bezel/maclock-screen-bezel.step): editable solids.
- [CAD parameters](../vendor/macintosh-mini/maclock-screen-bezel/params.py) and [geometry source](../vendor/macintosh-mini/maclock-screen-bezel/bezel.py): unchanged build123d source.
- [Breakout schematic](../vendor/macintosh-mini/maclock-pcb/maclock-breakout.kicad_sch) and [board layout](../vendor/macintosh-mini/maclock-pcb/maclock-breakout.kicad_pcb): KiCad reference, not approved Mack wiring.
- [Upstream build guide](../vendor/macintosh-mini/BUILD.md): read with [our corrections](../docs/references.md).

The source location and CERN-OHL-S-2.0 notices travel with the CAD and PCB. Create adaptations outside `vendor/` with their required notices; leave the imported originals unchanged.

## Design inputs

[measurements.csv](measurements.csv) records observations. Empty values mean unknown, not zero. [parts.csv](parts.csv) is a candidate list, not an order list. Unspecified counts remain empty.

[system-budget.csv](system-budget.csv) starts the assembly mass, power and space budget. It deliberately has no invented numbers. Record peak/average power by operating mode and avoid counting consumers both individually and in their supply assembly.

Measure mounting points from named datums. Record outside versus inside clearances and hole centers. Weigh the complete clock and removable pieces so the robot mass budget does not double-count them.

## Printing and assembly

Initial recommendation: an A1-class FDM printer. PLA for fit checks, PETG for candidate housings/brackets, and TPU for feet. Print parts separately; multicolor equipment is optional. [Research notes](../docs/research-notes.md) contain source links and the estimated printer budget.

Design around actual servo dimensions and shafts. Use purchased fasteners and joint bearings/bushings where appropriate. Choose print orientation and walls for the loads, then test. A good-looking print is not proof of load capacity.

Open checks: clock revision, bezel fit, motor/battery placement, total mass and balance, shared pin map, regulated compute supply, motor power, and one-leg range/load/current/stopping.
