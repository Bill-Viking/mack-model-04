lane: RayCue/Research
written: 2026-11-10T12:55:10-08:00
by: ACT — RayCue/Research: Mack joint design
on: MAC
head: 37540a2 (the printer-comparison commit follows)
status_updated: 2026-11-10T12:55:10-08:00
where: Leg packaged; workshop road and printer comparison written; rulings and printer pick wait on Bill
next: bill
depends_on: nothing
open_in: /Users/bill/Projects/RayCue Mac · fresh Claude session · ACT — RayCue/Research: Mack joint design
model: FABLE · EXTRA for the rulings below; SOL headless (via tools/offload.py) for the generator changes and re-runs
judgment: decide whether to download the ROBOTIS XL330 drawing; rule on the placement to carry (A is the study's comparison baseline, not a choice); accept or amend the three hinge-frame changes before the builder's brief; choose the printer from the priced comparison
remaining: 2 sittings
---
Read the project status/memory first. Pick up RayCue/Research on the Mac: read STATUS.md's 2026-11-10 entry, then hardware/joints/leg-packaging.md (J04-L02-D01) and its Results. The leg packaging model exists (hardware/joints/cad/leg_packaging.py, exports/l02-*). Three things wait on Bill: (1) his word on downloading XL330.pdf from ROBOTIS, to replace the recalled 11 mm output-axis offset in every parameter file; (2) which placement to carry forward (A keeps everything outside the shell at +25 to +41 mm of height; C and D need the unmeasured shell interior); (3) the three hinge-frame changes named in the study's "What remains, and why". With those, write the builder's brief (web stand-off ≥ 16.4 mm or no wrap; carrier plates ending above the hip-swing axis; h2 ≥ 27 at A; an output-up knee case with a 35.5 mm link; equal-link direct/proximal re-run), run it on Sol headless, and measure the result by the clear-pose count on the same grid (compare_l02_runs.py --map). Then a cable route per joint. Separately, Bill asked on 2026-11-10 for a workshop road (hardware/workshop-road.md, W04-D01: printer, electronics bench, parts buyable today). The printer comparison is done (hardware/printer-comparison.md, US store pages read 2026-11-10; it recommends the Bambu Lab P2S, printer only, and names four alternatives). His next word there is which printer, and he orders it himself. The headless builder has no network, so any further live-price reading runs in the attended window; bench and parts prices in the road are still RECALLED. The small first order (calipers, scale, two benchmark servos and adapter) needs his go and would settle the recalled offset by measurement. Keep Mack and the old preview servers stopped; voice, memory and appearance untouched; no iCloud; the loose root PNG stays untracked. Dock controls stay deferred.
