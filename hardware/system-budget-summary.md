# Mack — first-pass system budget

**Walker: 661–699 g. Complete robot: 973–1,332 g.** These are estimates, not measured limits or selections. The walker uses bench power and Mac conversation/audio/display. Full face electronics, battery, compute, recovery, guards and docking wait. Solar is optional and excluded; off-robot Mac, supply, tether and stationary dock are outside totals. [CSV](system-budget.csv) gives tags, sources and missing evidence.

| Quantity | Tethered walker, low–high | Complete product, low–high |
|---|---:|---:|
| Mass, g | 661–699 | 973–1,332 |
| Twelve motors at stall, 5.0 V: A / W | 17.6–17.6 / 88.2–88.2 | 17.6–17.6 / 88.2–88.2 |
| Walking leg rail, A / W | 3.5–7.1 / 17.6–35.3 | 3.5–7.1 / 17.6–35.3 |
| Battery nominal energy, Wh | Out of scope | 21.6–36.0 typical; 20.8–35.0 cell-minimum examples |
| Usable energy, Wh | Out of scope | 17.3–28.8 |
| Recorded price subtotal, USD | $355.18–$355.18 | $355.18–$355.18 |

Rail = CATALOG 1470 mA × 12 × 5.0 V; walking = ASSUMED 20–40% of stall current. Recovery motors, electronics and conversion losses remain additional unknown loads; this is not a whole-product peak. The [bench supply](bench-list.md) allows 5.0 A, below walking high and stall. No supply qualification or runtime claim follows.

[L03 direct](joints/cad/exports/l03-summary.json) gives each leg 91 g: three 18 g motors plus 37 g structure/foot, including three 6 g hardware allowances. Four legs total 362 g. Base is 47 g: model total minus legs, shell, payload and battery. Its 982 g total contains 225 g payload and 118 g battery placeholders, replaced here. Totals use unrounded inputs once; displayed rows may not sum exactly.

Cost = one $52.79 kit + eleven $27.49 servos ([first order](first-order.md), store read **2026-11-10**). CSV allocation: twelve motors $329.88; controller remainder $25.30, not a standalone quote. All other assemblies remain unpriced: donor, display, compute/cooling, audio, sensors, battery, conversion/protection, base, leg structure/feet, harness, recovery, guards, docking and optional solar. Recorded filament/wire/inserts lack consumption counts. Workshop tools are excluded. USD excludes tax/shipping; RECALLED prices are unused.

| Five mass drivers, ranked by high | Walker, g | Complete product, g |
|---|---:|---:|
| 1 | Donor 229–229 | Donor 229–229 |
| 2 | Motors 216–216 | Motors 216–216 |
| 3 | Structure/feet 146–146 | Pack 114–182 |
| 4 | Base 47–47 | Recovery 91–181 |
| 5 | Harness 10–25 | Structure/feet 146–146 |

Power has one quantified driver (leg motors); controller, compute, sensors and recovery remain unknown. Energy has only the battery row. Cost has only two priced rows; compute, battery and display are three further unpriced candidates, not a price ranking.

| Every ASSUMED budget input | Range and reason |
|---|---|
| Counts/scope | 12 motors, 4 legs; other included rows one assembly each; sensor/recovery bundle counts are not device/axis counts; Mac face/audio, deferred guards and omitted solar as above |
| Donor reserve | 229–229 g, whole-clock catalog proxy; electronics inactive, replacement face/audio additional; weigh removed parts |
| CAD mass model | Polymer 1.25 g/cm³; foot 1.2 g/cm³; hardware 6 g/joint; proposed solid envelopes in [parameters](joints/cad/j04-l03.base-short.json) |
| Display; compute/cooling | 20–50 g; 40–100 g: face assembly and largest electronics share |
| Controller; audio | 5–15 g; 10–25 g: interface board and mic/speaker assembly |
| Sensors | Full 5–15 g; walker motion-only 2–5 g, no camera |
| Power hardware; harness | Full 10–25 g; walker distribution 5–15 g; residual harness 10–25 g both |
| Allocation anchor | Seven electronics/harness rows 100–255 g + base = 147–302 g, near [review](../docs/review/design-review-2026-11-11.md) finding 4's 150–300 g **including base**, counted once |
| Battery | Two-cell comparison: 94–142 g cell allowances + 20–40 g pack overhead; [B04](battery-power.md) checked 2026-10-21; topology/fit unknown |
| Energy reserve | B04's 80% of typical energy, not converter efficiency |
| Recovery | One–two complete-leg masses, whole-system allowance including any motors; no mechanism chosen |
| Guards; docking | 20–50 g, roughly half–one base mass; 10–25 g contacts/detection, comparable to harness |
| Walking fraction | 20–40% of stall current: broad planning allowance around review/L03 static torque shares plus motion, not a torque/current law |
