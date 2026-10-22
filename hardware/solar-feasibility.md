# Mack S04 — optional solar charging

Feasibility study S04-D01 · 2026-10-21 · **calculated scenarios, no panel or charger selected**.

Bill would like a roof solar panel if it generates enough useful energy. Reserve
it as an option to evaluate, not a requirement to install regardless of benefit.
The roof's usable area, battery, compute and actuator loads are still unknown.

**Recommendation:** investigate a recessed roof panel for slow charging while
parked in direct sun. Keep battery/dock power as the primary supply. Ordinary room
lighting is unlikely to make a meaningful contribution to active conversation or
walking. A larger stationary solar panel feeding a charging dock is the stronger
solar option if energy autonomy matters more than keeping every panel on Mack.

## Evidence and size of the opportunity

Primary sources checked 2026-10-21; no supplier files copied or orders placed.

| Reference | Published figure | Meaning for Mack |
| --- | --- | --- |
| [Voltaic P124, August 2026 datasheet](https://voltaicsystems.com/content/P124_ds.pdf) | 113 × 66 × 2.6 mm, 31.6 g. Nominal 1.35 W; expected 1.14 W, about 6.01 V at maximum power. | A real small-panel benchmark, not a verified roof fit. The expected figure accounts for cell cutting/lamination losses; it is not a daily average or a guarantee through a window. |
| [Epishine MultiCell v1.6.5](https://www.epishine.com/hubfs/MultiCell_Data_Sheet_1.6.5.pdf), tables 1–2 and §6 | Mean 20.3 µW/cm² at 500 lux; warm-white LED, white backing, 22 ± 2°C. LEH3_50x50_6 has 22 cm² active area and 447 µW typical output. | Indoor harvesting is at milliwatt scale. These are indoor-specific cells, not the P124's indoor performance. Active area excludes packaging margins. |
| [Raspberry Pi 5 launch engineering discussion](https://www.raspberrypi.com/news/introducing-raspberry-pi-5/) | Around 12 W peak on the most intensive workloads. | A compute-only comparison showing why a small roof panel is supplemental. This is neither Mack's selected board nor her typical draw; display, audio and motion add separate loads. |

The P124's representative curve uses 1,000 W/m² and 25°C. Real roof orientation,
shade, cell temperature and protective covers change the result. Its 24.4% cell
efficiency is not whole-module efficiency. Use the module output rating directly;
do not multiply it by cell efficiency a second time.

An independent area sanity check is `P = irradiance × active cell area × efficiency`.
With an **assumed** 100 cm² active area, 1,000 W/m² and 20% efficiency, this gives
2 W before further losses. This is not Mack's measured roof area or a selected
panel rating. At Epishine's specified indoor conditions, 100 cm² active area would
instead give approximately **2.03 mW**, before conversion loss. Eight illuminated
hours would yield **0.01624 Wh**. Different cell technologies and spectra are being
compared; lux cannot be converted to solar irradiance by one universal factor.

## A daily-energy example, with assumptions exposed

Use the P124's **1.14 W expected output** as the reference and assume:

- Four equivalent full-sun hours on the panel plane per day. This is an illustrative
  solar exposure, not a local weather prediction or four clock hours outdoors.
- 80% additional delivered-energy factor for charging/conversion and residual
  installation effects. This is an assumption to replace with measurements; the
  panel's cell-cutting/lamination allowance is already included in 1.14 W.
- Enough battery headroom to accept the energy, within its charge limits.

`E_delivered = 1.14 W × 4 h × 0.80 = 3.648 Wh/day`

This is before subtracting Mack's parked consumption and any additional harvester
standby load not included in the factor. For scale, spending that energy later at
these **hypothetical battery-side total loads** would give:

| Assumed total load | Extra operating time from 3.648 Wh, with no parked draw deducted |
| --- | --- |
| 5 W | 43.8 minutes |
| 15 W | 14.6 minutes |
| 50 W | 4.4 minutes |

These are energy-equivalent examples, not runtime predictions or measured walking
loads. A complete battery capacity and mode schedule are still needed.

At 0.10 W continuous parked draw, 24 hours consumes 2.4 Wh, leaving **1.248 Wh**
from this example day before other loads. At 0.50 W, parked draw alone is 12 Wh and
the battery loses energy despite the panel. Break-even average load is only
**0.152 W** for this assumed day. Useful solar replenishment therefore needs a
genuinely low-power parked mode, measured across the complete power system.
Sleep/wake behavior is not implemented by this study.

## Mechanical and electrical integration

- Measure usable roof patches after excluding vents, the handle/recess, guards,
  wiring access and mounting margins. Do not assume the full top rectangle is usable.
- Recess the panel below the [R04 protective envelope](joints/recovery-envelope.md).
  Roof-down and diagonal loads must go through structural guards, not the cells.
  Check glass/laminate damage, retaining features and wiring through the full roll.
- Account for guard shadows and partial shading. A protective transparent layer
  must be tested for transmission and temperature; it is not optically free.
- Include panel, mount, wiring and charger mass in CoM/inertia and recovery loads.
  Avoid blocking cooling. Direct sun can raise shell, compute and battery
  temperatures; enforce the selected battery's actual charging-temperature limits.
- Use a solar-capable, chemistry-compatible charger with input power regulation,
  reverse-current protection, battery temperature monitoring and a defined load
  power path. The panel does not connect directly to the cells or motor rail.
  Verify voltage headroom and cold open-circuit voltage against all input limits.
- A roughly 6 V panel is not automatically compatible with a multi-cell robot
  pack. A boost/buck-boost path or different panel wiring may be needed. No pack
  voltage, charger IC or schematic is chosen. [TI BQ24650](https://www.ti.com/product/BQ24650)
  illustrates solar-input regulation and temperature monitoring, but is a **buck**
  example, not an approved Mack part or a solution for boosting into a higher pack.
- Meter incoming panel power and net battery power. Show “solar contributing”
  separately from “battery charging”; the battery can still discharge in sunlight.
  No automatic sun-seeking movement is authorized or implemented by this option.

## Decide from a bench measurement

Record usable roof area and selected module revision; then compare bare-panel and
mounted output in direct sun, window sunlight and ordinary room light. Log panel
angle, shade, temperature, spectrum/light description, voltage, current, delivered
Wh and net battery Wh. Measure the complete awake, parked, shutdown and dark
harvester loads. Include charge taper/full-battery rejection and a shaded start.

Compare the resulting daily energy with the actual mode schedule and added mass,
heat, cost and recovery constraints. Keep the roof option only if that measured
benefit is worthwhile to Bill. A separate solar dock can carry more area without
adding roof mass or compromising the rollover guards; its panel and storage still
need location-specific sizing. No meaningful solar-autonomy claim is established
until harvested energy and all consumption are measured over representative days.
