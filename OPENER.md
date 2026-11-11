lane: RayCue/Research
written: 2026-11-11T12:35:58-08:00
by: ACT — RayCue/Research: Mack short legs and base
on: MAC
head: e6959c9 (the opener's own commit follows)
status_updated: 2026-11-11T12:35:58-08:00
where: Short-leg model built and judged: revise; 55 mm kept; two rulings wait on Bill
next: bill
depends_on: nothing
open_in: /Users/bill/Projects/RayCue Mac · fresh Claude session · ACT — RayCue/Research: Mack leg iteration L04
model: FABLE · EXTRA for the J04-L04 leg brief (ASTRA headless if Fable is past its warn line); filing Bill's rulings needs no flagship
judgment: design the J04-L04 leg iteration from Bill's rulings and the review's three changes; judge its build
remaining: 2 sittings
---
WHERE WE ARE (deliver this first, in plain words, before anything dense)
Goal of this arc: design Mack's legs and body so a first walking prototype can be built at home, and keep the public repo clear enough for engineers to follow and critique.
What already happened:
1. GitHub Pages is on: the leg viewers open in a browser at bill-viking.github.io/mack-model-04.
2. Bill ruled: short legs under a low base; the first milestone is the tethered walker; fill the budget with ranges; the next leg design keeps 55 mm under the shell.
3. A short-leg model was built (J04-L03) and judged by an independent review: the numbers are sound, but the leg cannot stand at 55 mm as drawn. Two layout faults, hips 158.5 mm wide against about 100 in the picture, and no balance margin with one foot lifted.
4. The budget sheet holds first-pass ranges: tethered walker 661 to 699 g; recorded prices $355.18 so far.
Where things stand right now: everything is committed and pushed; nothing is running. The two posts are not out; Bill paused them.
Bill's next moves: rule on how closely the hips and base must match the picture; rule on which knee to build next (direct or belt); decide on the logo and interface look; place the orders when he chooses (the bench list's 5 A supply is too small for twelve motors walking).
The machine's next moves: on his rulings, brief the next leg iteration (J04-L04), have Sol build it, and have a judge rule from its numbers.

Read the project status/memory first. Pick up RayCue/Research on the Mac: read STATUS.md's 2026-11-11 entries from the top (BUTTONED UP first), then `hardware/joints/cad/briefs/J04-L03-REVIEW-BRIEF-VERDICT.md` (the judge's nine answers, its three changes and its RULINGS NEEDED). Put to Bill, one question per reply, each filed in STATUS.md the turn he answers: (1) the appearance goal: pursue about 15 mm of visible base and 100 mm across the hips (the judge's pick; needs smaller motors than the 20 x 34 x 26 mm benchmark, a different arrangement, or measured room inside the clock) or accept 27 mm and 158.5 mm; (2) the knee layout: direct (the judge's pick) or belt; (3) the design review's last suggestion: a logo and interface-look decision before wider publicity (the build-target picture and the desktop carry another company's logo and look); (4) tell him the bench list's supply is 5 A against a 7.1 A high walking estimate and 17.6 A stall, and ask whether to price a larger 5 V supply. Then write the J04-L04 build brief beside the J04-L03 one (`hardware/joints/cad/briefs/`), new parameters file beside `j04-l03.base-short.json`, generator extended from `leg_base_packaging.py`: clear the thigh-plate / carrier-plate overlap (32.8 mm³) to zero; end the shank channel at least 1.5 mm above the foot floor (it is 1.07 mm below); compute the contact point at the foot cylinder's true lowest rim point; design a weight shift so the three-foot margin goes from 0.0 to about +5 mm and report equilibrium foot loads; and whatever the appearance ruling requires. Look at `concepts/raycue-build-target.png` before any leg work. Launch it as ONE Sol headless build through `tools/offload.py` with a waiter, check both viewers in headless Chrome (`--use-angle=swiftshader --enable-unsafe-swiftshader`), then ONE headless review: the review launcher wants a one-page brief (at most 80 lines) with headings that start Row, Commits, Gate output, Real-case numbers, Files to read, names its own verdict file, takes no --report, and refuses to start while any tracked file is uncommitted. Also open: write the tethered-walker milestone into the roadmap and the technical specification; move figure 1's 'J3 knee' leader to the knee axis ring; record the two post permalinks when the Resonance/Posts window mails them. Standing constraints: keep Mack and the old preview servers stopped; voice, private memory and appearance untouched; no iCloud writes; the loose root PNG stays untracked; Bill places every order himself; nothing with his employer's name in any file; headless run logs stay untracked.
