STATE: DONE
Filled the first-pass budget, separated the tethered walker from the complete product, and checked the arithmetic without selecting parts.

## Totals

These are planning ranges incorporating assumptions, not measured bounds or procurement totals.

| Quantity | Tethered walker, low–high | Complete product, low–high |
|---|---:|---:|
| Robot mass, g | 661–699 | 973–1,332 |
| Twelve benchmark leg actuators at stall, 5.0 V, A | 17.6–17.6 | 17.6–17.6 |
| Twelve benchmark leg actuators at stall, W | 88.2–88.2 | 88.2–88.2 |
| ASSUMED walking leg-rail current, A | 3.5–7.1 | 3.5–7.1 |
| ASSUMED walking leg-rail power, W | 17.6–35.3 | 17.6–35.3 |
| Two-cell comparison nominal energy, Wh | Not in scope | 21.6–36.0 typical; 20.8–35.0 cell-minimum examples |
| ASSUMED usable energy, Wh | Not in scope | 17.3–28.8 |
| Recorded-price subtotal, USD before tax/shipping | $355.18–$355.18 | $355.18–$355.18 |

The complete-product rail figure covers the twelve leg actuators only. Additional recovery actuators, other electronics, converter losses, current transients and returned braking energy remain unresolved. No whole-product peak, operating runtime, continuous actuator rating or qualified supply is asserted. The recorded bench supply is limited to 5.0 A, below both the walking high estimate and aggregate stall demand.

The walker includes the whole-donor mass reserve, direct legs, base, controller, motion-only sensor bundle, distribution/stop hardware and residual harness. Display/audio/conversation are assumed to remain on the Mac for this first milestone. Onboard compute, battery, camera, complete optical face, recovery, full protective rails and docking are deferred. Complete-product mass includes allowances for those required assemblies. Solar is optional and excluded from both baselines. Off-robot Mac, bench supply, tether beyond the robot connector and stationary dock are outside robot mass and assembly cost.

## Accounting and evidence

- Preserved all 17 row identities and all 12 original columns. Inserted the nine requested range/basis columns immediately after `power_peak_each_W`; appended `in_tethered_walker`, for 22 columns total. Existing mass, idle/active/peak power, rail and dimension cells remain empty. Existing status text and each evidence prefix are preserved.
- Added quantity 1 to the formerly blank sensor and recovery rows solely as one budget assembly each. Sensor device count and recovery axis count remain unselected. The optional solar quantities remain blank. In `basis`, each quantity-family tag applies to both low and high endpoints; quantity tags identify concept/bundle counts.
- Direct L03 leg mass is 91 g printed: 54 g of actuators plus 37 g structure/foot. The latter retains three 6 g hardware allowances. Across four legs, actuators contribute 216 g and structure/feet 146 g, totaling 362 g before display rounding. No joint allowance is charged again in harness.
- The named L03 summary has no standalone base-mass field. Base is CALCULATED as `direct.total_mass_g - direct.four_leg_mass_g - shell_g - payload_g - battery_g` using the parameter mass model, giving 47 g printed. The model's 982 g total and its 225 g payload/118 g battery placeholders are not added to the new budget.
- Review finding 4's 150–300 g group includes base, whereas L03's payload wording omits it. This draft allocates seven electronics/harness rows to 100–255 g and counts the base separately, yielding 147–302 g for the comparable group. It does not add either aggregate as another row.
- Shell mass is an ASSUMED 229–229 g reserve based on the CATALOG complete donor, not a measured empty shell. Original electronics are assumed inactive; new face/audio parts are incremental. Retained-part weighing will release the mass reserve for discarded donor contents.
- Battery mass is an ASSUMED 114–182 g: two-cell comparison allowances of 94–142 g plus 20–40 g for internal protection, interconnects, insulation, enclosure and connectors. B04's cell numbers are catalog maxima/energy examples, not a finished-pack specification. The two-cell comparison and 80% usable fraction select neither topology nor pack.
- Recovery mass is an ASSUMED whole-system allowance equal to one–two direct complete-leg masses, including any motors and mounting. It is a scale analogy, not a mechanism or axis-count decision; its high endpoint is not a demonstrated upper bound.
- Price accounting uses one kit at $52.79 plus eleven individual benchmark servos at $27.49 from `hardware/first-order.md` and `hardware/buy-list.md`, store read 2026-11-10. CSV allocation assigns twelve servos $329.88 and the residual controller $25.30, so the bundled servo is counted once. The controller allocation is CALCULATED, not a standalone board price. No recalled workshop-road price was used.
- Store-priced tools, filament, wire and inserts were read in the authorized order sheets. Tool purchases are not robot assembly cost; material/fastener consumption and suitability are not established, so their package prices were not assigned to arbitrary component rows.

## What remains blank and what would fill it

- **Mass/count:** optional solar panel/mount and charger/path need a defined optional configuration, geometry and maker mass data. Complete baseline mass is filled with clearly tagged allowances, not qualified hardware values.
- **Power:** compute/cooling, controller, display, audio, sensors, battery internal electronics, external conversion/protection, recovery, docking and optional solar circuitry lack applicable assembly ratings or measurements. These remain blank. Passive structure rows have calculated zero consumer power; the retained donor's zero assumes inactive electronics. Walking current needs a logged representative gait; conversion needs measured efficiency and topology; recovery needs a mechanism and motor count before its peak can be summed.
- **Price:** donor, display/mount, compute/cooling, audio, sensors, battery, conversion/protection, base, leg structure/feet, residual harness/fasteners, recovery, guards, docking and solar need dated first-hand assembly prices or a counted BOM with dated component prices. Their blank costs are not zero. Both $355.18 figures are known-price subtotals only.
- **Measured columns:** physical weighing, dimensional intake and electrical measurements are still required. No new measured values were manufactured from estimates.
- **Missing named source:** `docs/product-definition.md` does not exist. Continued using the authorized technical specification, roadmap, review and model strategy. B04 was found at `hardware/battery-power.md`; compute discussion at `docs/model-strategy.md`.

## Checks actually run

Read-only searches in `tests/` and `tools/` found no `system-budget`/`system_budget`/`budget.csv` references and no apparent parser for this sheet; no parser columns or test code were changed. The wider initial discovery search was too broad, as recorded below.

A bounded Python standard-library check reread the CSV and source JSON. It passed row order/count, exact column placement, original-cell and evidence preservation, paired ranges, low ≤ high, tag coverage, requested numeric precision, price read dates, the actuator/structure split, unrounded mass totals, kit/servo cost reconciliation, rail arithmetic, battery-energy arithmetic and summary-link existence. A separate in-memory comparison against the original specification confirmed exactly the authorized sentence replacement. No test files or temporary artifacts were written.

Browser, GUI, native spreadsheet, print-pagination and visual proofs are **unrun here and belong to the caller**. No CAD generation, physical measurements, motor tests, gait proof, battery qualification or runtime test was run. No network, browser/GUI launch, wake pull, heartbeat kick, commit, push, permission change or safety-check change occurred. Brain freshness was not established or claimed.

## Departures and interpretations

1. Initial source discovery searched broadly across non-excluded `hardware/` and `docs/` content, returning excerpts from other documents and generated exports before narrowing to the named sources. This exceeded the intended narrow read scope. `STATUS.md`, `OPENER.md` and `*.log` were excluded and were not opened. Those extra excerpts were not used as numerical evidence.
2. The spreadsheet skill instruction file was read outside the task's source allowlist under the session's skill-use instruction. The explicit four-file CSV/Markdown scope took precedence over its workbook/dependency/output workflow; standard-library CSV editing was used and no extra artifact was written.
3. A separate mass range per milestone cannot fit in the requested single set of range columns. CSV ranges therefore describe the complete baseline; the two `partial` rows carry walker-only mass ranges in evidence and the summary assumption table. Those explicit partial masses, not a guessed percentage, feed walker totals.
4. Sensor and recovery quantities now mean one budget bundle, as explained above; no device or axis count is selected. The base is derived by subtraction because the named summary omits a base field. Both interpretations are exposed in evidence.
5. Five mass drivers are listed for each milestone. Five numerical drivers cannot honestly be listed for every other total: there are only two priced rows, one quantified rail row and one energy-storage row. The summary names unresolved candidates instead of inventing price or power contributions.
6. The Markdown summary is condensed to 684 words as a single-page brief; physical print pagination was not tested. Only the specified sentence in `docs/technical-spec.md` changed, so its historical review table and older reviewer question remain as they were; the new linked summary governs this draft's current totals.

## OPEN: owner choices

- OPEN: Keep the full-donor 229 g reserve until weighing **[pick]**, or substitute a lighter retained-shell guess now.
- OPEN: Keep Mac display/audio for the first tethered walker **[pick]**, or include the full fitted face/audio assembly in that milestone.
- OPEN: Keep the two-cell mass/energy comparison as an estimate **[pick]**, or carry a separate four-cell comparison before pack selection.
- OPEN: Keep the one–two leg-equivalent recovery mass allowance visible **[pick]**, or leave complete-product mass open-ended until a recovery mechanism exists.
- OPEN: Keep 20–40% aggregate stall current as a planning range pending logged walking **[pick]**, or leave walking power blank until bench evidence arrives.

Files written: `hardware/system-budget.csv`, `hardware/system-budget-summary.md`, the single authorized sentence in `docs/technical-spec.md`, and this report.

STATE: — DONE: estimated budgets written and checked; no parts selected.
