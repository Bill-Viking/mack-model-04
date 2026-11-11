# Budget fill — brief: first-pass ranges for mass, power, energy and cost

Quality bar: beyond-Apple quality — the machine notices, the human never checks; one plain
sentence at the moment it is needed; state visible on the surface; nothing superfluous.
Design principle served: make the interface truthful — every number carries where it came from.

complexity: complex — this is a judgment draft: it estimates, tags and sums; it selects nothing.

## Why

`hardware/system-budget.csv` has no number in any row. The owner ruled on 2026-11-11: fill it
with rough ranges now, each labelled as an estimate, and tighten them as parts are measured.
He also ruled that the first milestone is the **tethered walker**: four legs under the real
shell, walking under supervision, powered by a cable from the bench, with conversation served
from the development Mac. Battery, onboard computer, self-righting, the concealed camera and
return-and-recharge belong to the complete product, not to that milestone.

## Read (and do not open anything else outside these)

- `hardware/system-budget.csv` — the sheet to fill. Check `tests/` and `tools/` for anything
  that parses it before changing its columns; say what you found.
- `docs/review/design-review-2026-11-11.md` — finding 4 (first mass estimate), 5 (torque), 9 (rail).
- `hardware/joints/cad/exports/l03-summary.json` — the short-leg model's masses (direct variant
  is the working layout): leg, four legs, base, total. `hardware/joints/cad/j04-l03.base-short.json`
  for the actuator's CATALOG figures and the ASSUMED mass-model inputs.
- `hardware/first-order.md`, `hardware/buy-list.md`, `hardware/bench-list.md`,
  `hardware/printer-comparison.md` — store prices read first-hand, each with its read date.
- `hardware/workshop-road.md` — its prices are RECALLED; never use them as evidence.
- The battery and power studies and the compute or model-strategy study, wherever the repository
  keeps them (search `hardware/` and `docs/` for B04 and for the compute discussion), and
  `docs/technical-spec.md`, `docs/product-definition.md` if present, `docs/roadmap.md`.

Do NOT open `STATUS.md`, `OPENER.md`, any `*.log`. No network, no browser, no price look-ups:
a price not already recorded in the repository with its read date stays blank.

## What you write

1. `hardware/system-budget.csv`: keep every existing row and column. ADD these columns after
   `power_peak_each_W`: `mass_each_low_g`, `mass_each_high_g`, `power_active_each_low_W`,
   `power_active_each_high_W`, `power_peak_each_low_W`, `power_peak_each_high_W`,
   `cost_each_low_usd`, `cost_each_high_usd`, `basis`. The old single-value columns stay empty
   until something is measured. `basis` holds one tag per filled quantity: CATALOG (a maker's
   figure), CALCULATED (from the CAD model or arithmetic), ASSUMED (a planning guess), RECALLED
   (remembered, unverified). Put the source file, and the read date for a price, in `evidence`,
   keeping the row's existing evidence text. A cell you cannot support from the repository stays
   empty and its `evidence` says what would fill it.
   Add one column `in_tethered_walker` (yes / no / partial) from the milestone's definition above.
   Do not double count: the leg model's leg mass includes three actuators and three hardware
   allowances; split it between `leg_actuator` and `leg_structure_and_foot` and show the split.
2. `hardware/system-budget-summary.md`, one page: for the tethered walker and for the complete
   product separately, low and high totals for mass; worst-case current and power on the
   actuator rail (all twelve at CATALOG stall, and a stated ASSUMED walking fraction); energy
   (Wh) only where a battery is in scope; cost from recorded prices only, with what is still
   unpriced named. Then the five rows that drive each total, and the list of every ASSUMED
   figure in one table so the owner can correct them. Plain words first, tables after.
3. In `docs/technical-spec.md`, change only the sentence that says the engineering budget is
   blank, so it states truthfully what the sheet now holds and links the summary.
4. `docs/review/BUDGET-FILL-BRIEF-REPORT.md`: first line `STATE: DONE | PARTIAL | FAIL` and one
   sentence; the totals; what you could not fill and why; each place you departed from this
   brief; `OPEN:` questions for the owner as one-sentence choices with your pick marked.

## Rules

- Select nothing. A range is not a choice of part.
- Ranges, not points: when the repository gives one figure, the range is that figure both ends
  with its tag; when it gives none, an ASSUMED range must say what it was reasoned from.
- Money in US dollars before tax and shipping, as the order sheets are.
- Printed numbers: grams to whole numbers, watts and amperes to 0.1, dollars to cents, each
  rounded once from the unrounded value. Totals are summed from unrounded values.
- Commit nothing. Write only the four files named above.
- One run. If a source the brief names does not exist, say so and carry on.
