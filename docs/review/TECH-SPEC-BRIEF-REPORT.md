# Technical specification draft report

STATE: DRAFTED

Created the two requested new deliverables and this explicitly requested hand-back. No existing file was edited by this job. No browser, GUI, service launcher, wake pull, heartbeat, commit, push, permission change or approval prompt was used. Brain freshness is unverified; no freshness evidence was supplied.

## Deliverables

| File | Bytes | Words |
| --- | ---: | ---: |
| `docs/technical-spec.md` | 30683 | 3649 |
| `.github/ISSUE_TEMPLATE/design-feedback.md` | 333 | 50 |

The specification is a single continuous Markdown page, within the requested word range, rather than a paginated print artifact. Word count uses whitespace splitting, including Markdown table and diagram tokens. The feedback template has 14 lines.

## Checks run here

| Check | Result |
| --- | --- |
| Spec word count | PASS — 3649; required 2,600–3,800 |
| Relative paths | PASS — 135 link/image occurrences, 56 unique destinations; every path exists |
| Markdown section anchors | PASS — local heading-slug check, including review-finding anchors |
| Mermaid | PASS — flowchart block, 16 paired node brackets, balanced nesting, no HTML; no renderer run |
| Home paths | PASS — none in specification or template |
| Standing tags | PASS — only DECIDED, PROPOSED, CATALOG, CALCULATED, ASSUMED, MEASURED, OPEN used as standing tags |
| Five-word status states | PASS — all subsystem state cells contain five whitespace-separated words |
| Reviewer questions | PASS — 16 numbered discipline-grouped questions; all nine review findings represented; sections Mechanical through AI each end with two or three questions |
| Issue template | PASS — required front matter, four prompts, fewer than twenty lines |
| Numerical census | PASS — 99 distinct visible digit-bearing tokens mapped below; values checked against cited source lines |

Links that failed: none.

## Number-to-source table

Every visible digit-bearing value or identifier is accounted for below. Repeated numbers with different meanings have separate rows. Link destinations and the reviewer list's ordinal labels are navigation/structure rather than engineering quantities. The spelled-out engineering counts follow the main table. Dates are ruling dates, not new targets. Source line references were checked against the working tracked documents in this run. No ignored runtime, private media or memory folder was read.

| Number or identifier in spec | Standing / scope | Source file and line | Meaning |
| --- | --- | --- | --- |
| `04` | Identifier | `docs/product-spec.md:15` | Formal product designation, not a quantity |
| `2026-10-20` | DECIDED | `README.md:29` | Bill confirmed the appearance target |
| `2026-10-20` | DECIDED | `docs/product-spec.md:9` | Bill confirmed Linux foundation |
| `2026-10-21` | DECIDED | `docs/product-spec.md:19–24` | Curved face direction and primary lithium-ion power |
| `2026-10-21` | DECIDED | `software/mack/VOICE.md:4–5` | Accepted light-echo voice |
| `2026-10-21` | DECIDED | `docs/model-strategy.md:54` | Onboard local mode and optional cloud assistance |
| `2026-11-10`, `P2S` | DECIDED | `hardware/workshop-road.md:56` | Printer only, unpurchased |
| `P01` | PROPOSED requirement ID | `docs/product-spec.md:59` | Condensed acceptance requirement; not passed on hardware |
| `P02` | PROPOSED requirement ID | `docs/product-spec.md:60` | Condensed acceptance requirement; not passed on hardware |
| `P03` | PROPOSED requirement ID | `docs/product-spec.md:61` | Condensed acceptance requirement; not passed on hardware |
| `P04` | PROPOSED requirement ID | `docs/product-spec.md:62` | Condensed acceptance requirement; not passed on hardware |
| `P05` | PROPOSED requirement ID | `docs/product-spec.md:63` | Condensed acceptance requirement; not passed on hardware |
| `P06` | PROPOSED requirement ID | `docs/product-spec.md:64` | Condensed acceptance requirement; not passed on hardware |
| `P07` | PROPOSED requirement ID | `docs/product-spec.md:65` | Condensed acceptance requirement; not passed on hardware |
| `P08` | PROPOSED requirement ID | `docs/product-spec.md:66` | Condensed acceptance requirement; not passed on hardware |
| `P09` | PROPOSED requirement ID | `docs/product-spec.md:67` | Condensed acceptance requirement; not passed on hardware |
| `P10` | PROPOSED requirement ID | `docs/product-spec.md:68` | Condensed acceptance requirement; not passed on hardware |
| `P11` | PROPOSED requirement ID | `docs/product-spec.md:69` | Condensed acceptance requirement; not passed on hardware |
| `P12` | PROPOSED requirement ID | `docs/product-spec.md:70` | Condensed acceptance requirement; not passed on hardware |
| `P13` | PROPOSED requirement ID | `docs/product-spec.md:71` | Condensed acceptance requirement; not passed on hardware |
| `G0` | Gate ID; source state | `docs/roadmap.md:7` | G0 reported built; G1 through G8 open |
| `G1` | Gate ID; source state | `docs/roadmap.md:8` | G0 reported built; G1 through G8 open |
| `G2` | Gate ID; source state | `docs/roadmap.md:9` | G0 reported built; G1 through G8 open |
| `G3` | Gate ID; source state | `docs/roadmap.md:10` | G0 reported built; G1 through G8 open |
| `G4` | Gate ID; source state | `docs/roadmap.md:11` | G0 reported built; G1 through G8 open |
| `G5` | Gate ID; source state | `docs/roadmap.md:12` | G0 reported built; G1 through G8 open |
| `G6` | Gate ID; source state | `docs/roadmap.md:13` | G0 reported built; G1 through G8 open |
| `G7` | Gate ID; source state | `docs/roadmap.md:14` | G0 reported built; G1 through G8 open |
| `G8` | Gate ID; source state | `docs/roadmap.md:15` | G0 reported built; G1 through G8 open |
| `WB-8` | Identifier | `hardware/joints/leg-layout.md:129–131` | Donor clock model |
| `80`, `91`, `112`, `229` | CATALOG | `hardware/joints/leg-layout.md:131` | Body envelope in mm; whole donor mass in g |
| `50`, `30` | PROPOSED | `hardware/joints/leg-packaging.md:66–68` | Direct and proximal upper-link lengths in mm |
| `30` | PROPOSED | `hardware/joints/leg-layout.md:145` | Lower-link length in mm; packaging datums also retain this pitch |
| `223.8`, `97.1` | CALCULATED | `hardware/joints/leg-packaging.md:82` | A direct: height in mm and mass per leg in g |
| `207.8`, `117.9` | CALCULATED | `hardware/joints/leg-packaging.md:83` | A proximal: height in mm and mass per leg in g |
| `203.7`, `97.7` | CALCULATED | `hardware/joints/leg-packaging.md:84` | C direct: height in mm and mass per leg in g |
| `187.7`, `118.5` | CALCULATED | `hardware/joints/leg-packaging.md:85` | C proximal: height in mm and mass per leg in g |
| `180.9`, `120.1` | CALCULATED | `hardware/joints/leg-packaging.md:86` | D direct: height in mm and mass per leg in g |
| `164.9`, `140.9` | CALCULATED | `hardware/joints/leg-packaging.md:87` | D proximal: height in mm and mass per leg in g |
| `XL330-M288-T` | Identifier; CATALOG benchmark | `hardware/first-order.md:11` | Size benchmark and sample order-study identity |
| `20`, `34`, `26`, `18`, `5` | CATALOG | `hardware/first-order.md:43` | Benchmark case mm, mass g and supply V |
| `0.52`, `1.47` | CATALOG | `hardware/first-order.md:44` | Stall torque N·m and stall current A |
| `11` | ASSUMED | `hardware/joints/leg-packaging.md:35` | Recalled axis offset mm; not independently verified |
| `XL330`, `XC330`, `STS3032`, `SCS0009` | PROPOSED candidate identifiers | `hardware/workshop-road.md:88` | Candidate names only; recalled shortlist not a current catalog verification |
| `OpenRB-150` | PROPOSED candidate identifier | `hardware/first-order.md:11–36` | Sample kit and possible local controller; not selected for fitted body |
| `B04` | Identifier | `hardware/battery-power.md:1` | Battery study |
| `P30B`, `47`, `188`, `43.2` | CATALOG cell / CALCULATED aggregate | `hardware/battery-power.md:48` | Cell maximum mass g; four-cell mass g and typical Wh |
| `P50B`, `71`, `284`, `72.0` | CATALOG cell / CALCULATED aggregate | `hardware/battery-power.md:49` | Cell maximum mass g; four-cell mass g and typical Wh |
| `80` | ASSUMED | `hardware/battery-power.md:64` | Usable-energy percentage, not conversion efficiency |
| `34.56`, `57.6` | CALCULATED | `hardware/battery-power.md:71` | Usable Wh under the example allowance |
| `30`, `1.15`, `1.92` | ASSUMED load / CALCULATED runtime | `hardware/battery-power.md:74` | Battery-side W and example hours, respectively |
| `D04` | Identifier | `hardware/charging-dock.md:1` | Dock study |
| `P124`, `1.14` | CATALOG | `hardware/solar-feasibility.md:21` | Panel identifier and expected W |
| `4` | ASSUMED | `hardware/solar-feasibility.md:49` | Equivalent full-sun hours per day; prose assumption at line 42 |
| `80` | ASSUMED | `hardware/solar-feasibility.md:44` | Delivered-energy percentage |
| `3.648` | CALCULATED | `hardware/solar-feasibility.md:49` | Delivered Wh/day before parked draw |
| `M2` | Host identifier | `docs/model-strategy.md:7` | Development computer, not onboard choice |
| `ESP32-S3`, `RP2040` | PROPOSED candidate identifiers | `hardware/workshop-road.md:73` | Possible body-controller classes |
| `BNO08x`, `ICM-42688` | PROPOSED candidate identifiers | `hardware/workshop-road.md:91` | Orientation sensors |
| `VL53L1X`, `VL53L4` | PROPOSED candidate identifiers | `hardware/workshop-road.md:92` | Dock ranging sensors |
| `INA219`, `INA228` | PROPOSED candidate identifiers | `hardware/workshop-road.md:94` | Power monitors |
| `0.3` | Software version; reported host evidence | `software/desktop/README.md:1` | Local AI release identifier |
| `Qwen3.6:35b` | Model identifier; reported host evidence | `docs/model-strategy.md:7` | Existing local conversation artifact |
| `Qwen3-ASR` | Model identifier; reported host evidence | `software/mack/LISTENING.md:82–85` | Local recognition model family |
| `Qwen3-TTS`, `v1` | Model/voice identifiers; DECIDED voice | `software/mack/VOICE.md:4–5` | Synthesis family and accepted voice revision |
| `388`, `471` | CALCULATED | `docs/review/design-review-2026-11-11.md:57` | Four-leg aggregate mass range g |
| `229` | CATALOG | `docs/review/design-review-2026-11-11.md:58` | Maximum whole-donor contribution g; retained content unknown |
| `94`, `142` | CALCULATED | `docs/review/design-review-2026-11-11.md:59` | Two-cell mass comparison g; excludes pack hardware |
| `150`, `300` | ASSUMED | `docs/review/design-review-2026-11-11.md:60` | Remaining assembly discussion allowance g |
| `0.85`, `1.15` | CALCULATED rough estimate incorporating ASSUMED inputs | `docs/review/design-review-2026-11-11.md:61` | Whole-robot discussion range kg, copied rather than recomputed or adopted |
| three axes per leg; four legs; twelve actuators | PROPOSED | `hardware/joints/leg-layout.md:17–20` | Baseline drive count; recovery axes excluded |
| single knee-bend branch | PROPOSED | `hardware/joints/leg-layout.md:96–101` | First load-bearing prototype; separate reversible-knee study |
| four-cell examples | CALCULATED | `hardware/battery-power.md:45–54` | Cell-only comparisons, no chosen pack topology |
| two-cell comparison; four legs | CALCULATED | `docs/review/design-review-2026-11-11.md:57–59` | Review mass-estimate quantities |

The packaging document calls its values measurements on rigid envelopes; the draft labels these CALCULATED to avoid suggesting physical measurements. Its direct/proximal comparison uses different upper-link lengths and the draft preserves that limitation. The recalled actuator-axis offset is labeled ASSUMED, never CATALOG or MEASURED. The review's whole-robot mass range is retained as a rough calculation incorporating assumptions, not a selected mass target.

## Source conflicts retained or resolved in presentation

| Difference | Draft treatment |
| --- | --- |
| Architecture lists earlier read-only tools; desktop guide includes archive search | Describes the desktop guide's set and names the discrepancy; does not claim code verification |
| Workshop road has an older closing statement saying no printer selected | Uses the explicit dated P2S ruling, while preserving not-ordered status |
| Old sample-servo/adapter proposal differs from later first-order sheet | Uses the sample-kit study; no fitted actuator/controller selection claimed |
| Appearance animation diverges from accepted target | Links the kinematic viewer with its scope and the review's withdrawal from sharing |

## Proofs not run and limits

Browser proofs are UNRUN here and belong to the caller: GitHub Markdown/Mermaid rendering, figure legibility and final visual composition, model rotation, HTML viewer interaction and animation rendering. Link checks establish target existence, not browser behavior. Figures were being redrawn by another builder and were not edited or visually accepted by this job.

No software runtime, microphone, inference, speech, CAD generator, physics, electrical or hardware test was run. Existing host and CAD checks are explicitly attributed to repository evidence, never claimed as this job's proof. No external catalog freshness or supplier availability was checked; no purchasing recommendation is made. No physical robot qualification is established.

Nothing in the bounded drafting brief remains incomplete. The requested report is the only file written in addition to the two new deliverables. Existing files and other builders' work were left untouched by this job; concurrent repository changes are not this job's changes.

OPEN: No new design decisions made. Decisions left open include base proportions, hip placement, knee drive, actuator choice and continuous duty, structural materials, cable routes, recovery mechanisms, pack/topology/rail protection, dock interlocks, compute/controller selection, stop strategy, sensing, optics, camera retention, numeric budgets, and any earlier tethered-walker milestone. Public logo/interface treatment remains for the owner; this draft neither clears nor rejects it.

SPEC DRAFT DONE — 3,649-word specification and feedback template drafted; source and text checks pass; browser proofs unrun.
