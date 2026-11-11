# FACTS PASS — M.A.C. Model 04

Read boundary: tracked files listed in `git ls-files`; ignored folders excluded. CAD JSON inspection was limited to top-level keys, provenance and requested comparison headlines. This is a document digest; the repository reports browser proofs from prior sessions, but no browser was launched in this pass. Brain freshness is unverified; no pull or heartbeat was run under the headless instruction.

## IDS

- **M.A.C. Model 04 / Mack** names the formal project/product and everyday name. — README.md:1-3
- **P01–P13** name product acceptance requirements; P01–P10 are integrated-product/ownership criteria and P11–P13 cover recovery, protective/dock requirements in the product and hardware plans. — docs/product-spec.md:53-103
- **G0–G8** name evidence gates from foundation through reproducible build; Optional is vintage apps. — docs/roadmap.md:5-16
- **J04** names the joint/leg and recovery workstream; **J04-C01** is the example cartridge; **J04-L01** is the leg-layout study; **J04-L02** is the packaged leg study; **J04-L02-D01** is its dated revision; **J04-L02-V01** names the animation/sharing views. — hardware/joints/README.md:1-4; hardware/joints/cad/README.md:1-5; hardware/joints/leg-layout.md:1-4; hardware/joints/leg-packaging.md:1-5; STATUS.md:5,11
- **R04** names the directed recovery/contact envelope and qualification matrix. — hardware/joints/recovery-envelope.md:1-5
- **B04** names battery/power engineering direction and requirements. — hardware/battery-power.md:1-4
- **D04** names the autonomous docking concept and charging state machine. — hardware/charging-dock.md:1-4
- **F04** names the curved display/face and concealed-camera optical study. — hardware/display-and-vision.md:1-4
- **S04** names optional roof solar feasibility. — hardware/solar-feasibility.md:1-4
- **T04** names the virtual practice-room / physics-training track. — docs/motion-training.md:1-4
- **W04** names the workshop road; **W04-D01** is its 2026-11-10 revision. — hardware/workshop-road.md:1-4
- **G1–G5 references in W04** are roadmap gates: measurement intake, sample actuator, printer, bench, and one-leg test are stage links. — hardware/workshop-road.md:13-20
- **M.A.C. identity ID** is `mack-model-04`; pronouns are she/her. — software/mack/identity.json:2-6

## DECIDED

- Bill named the product M.A.C. Model 04, everyday name Mack, on 2026-10-20. — docs/product-spec.md:13-18
- Bill selected Mack's own complete system on Linux on 2026-10-20; no new kernel is in baseline. — docs/product-spec.md:7-11
- Bill accepted the compact Mac appearance concept on 2026-10-19 and confirmed the exact image as build target on 2026-10-20. — docs/product-spec.md:18; README.md:27-30
- Bill specified she/her and a long-term humanoid embodiment goal on 2026-10-21; the first physical target remains the four-legged Mac. — docs/product-spec.md:15-17
- Bill chose SAL 9000's voice and manner as direction on 2026-10-21; accepted the light-echo audition as voice v1 on 2026-10-21. — docs/personality-and-voice.md:6-15; docs/product-spec.md:49-51
- Bill chose lithium-ion as primary power on 2026-10-21; capacity and voltage remain open. — docs/product-spec.md:22-24
- Bill redirected work to joints before dock controls on 2026-10-22; the leg-layout document says this did not approve motors or manufacturing release. — hardware/joints/leg-layout.md:1-5; STATUS.md:95
- Bill selected Bambu Lab P2S, printer only, on 2026-11-10; it was not ordered. — hardware/workshop-road.md:52-57; STATUS.md:9
- Bill's order for a home-printing/workshop road is recorded 2026-11-10. No purchase authorization or purchase is recorded. — hardware/workshop-road.md:3-7; STATUS.md:9
- Bill asked to price the bench on 2026-11-11; no items were ordered. — hardware/bench-list.md:1-7; STATUS.md:7
- STATUS says Bill approved two social post drafts on 2026-11-11, but they remained unposted at the newest entry. — STATUS.md:5, 294

## COMPLETION

- Finished product: an integrated personal robot in accepted compact Mac form; own Linux-based system, personality, memory, sensing, electronics and four-leg mechanism; walking and sensing are core. — docs/product-spec.md:5-11
- Product proof is P01–P13. P01 boot-to-interface without dev terminal; P03 truthful spoken interaction and interruption with latency/audibility measured under motor operation; P04 reboot-persistent inspectable/correctable/exportable/recoverable memory; P05 timestamped sensor health and obstacle/floor/tilt/power tests; P06 measured movement envelope; P07 independent stop/fault/link/restart behavior; P08 battery and bounded offline operation; P09 closed/serviceable shell and recorded mass/CoM/rails/heat/sound; P10 repeatable install/calibration/backup/update recovery/service; P11 qualified recovery. — docs/product-spec.md:53-103
- First prototype gates: G1 measured envelope/budgets; G2 runtime/memory/mock-body rejection, expiry and recovery; G3 spoken interaction, latency, disconnect/cancellation/offline behavior; G4 stationary assembled Mack; G5 restrained loaded leg; G6 qualified four-leg base and R04 recovery; G7 integrated personal robot meeting P01–P09 and P11–P13; G8 repeatable build meeting P10. — docs/roadmap.md:5-15
- Roadmap says gates remain open until tests pass; it is not a calendar. Current G1/G2/G3/G4/G5/G6/G7/G8 status is open except G0 built. — docs/roadmap.md:3-15
- Integration proof order: fit models → supported joint → restrained loaded leg → four-leg base with dummy mass → stationary Mack → restrained integrated motion → supervised floor walking. — hardware/integration-plan.md:87-89
- Current body status is desktop; `physical_connection=false`, with no sensors or motion actions. — docs/architecture.md:57-61; STATUS.md:183-185

## MECHANICAL

### SAYS
- WB-8 catalog envelope is 80 × 91 × 112 mm and 229 g (CATALOG); physical intake remains blank and working W/D/H axis mapping is unverified. — hardware/joints/catalog-scale.json:1-8; hardware/measurements.csv:1-29; STATUS.md:89
- J04-L02 study uses benchmark blocks 20 × 34 × 26 mm, 18 g each (CATALOG); these are not selected actuators. — hardware/joints/leg-packaging.md:1-20
- Packaging study reports placement A height 223.8 mm (MEASURED) direct-knee / 207.8 mm (MEASURED) proximal; C 203.7 / 187.7 mm (MEASURED); D 180.9 / 164.9 mm (MEASURED), with D mount block in J2 path. These are rigid-envelope model results, not fit/load proof. — STATUS.md:11
- Placement A mass estimate is 97.1 g (CALCULATED) direct / 117.9 g (CALCULATED) proximal per leg; hip-swing Σm·r² is 85,800 / 40,100 g·mm² (CALCULATED); direct used a 50 mm link and proximal 30 mm, so STATUS says comparison margin is overstated. — STATUS.md:11
- Animation is scripted kinematics: stride 24 mm (UNTAGGED), lift 10 mm (UNTAGGED); IK error and stance-foot slip each under 0.00001 mm (UNTAGGED); no physics, stability, load or motion interference check. — STATUS.md:5
- Known CAD frame revisions named: web stand-off 12.5 → ≥16.4 mm (UNTAGGED); carrier plates extending 23–26.5 mm below hip-swing axis (UNTAGGED); a 23 mm drop leaves 2 mm to J1 case (UNTAGGED). — STATUS.md:11
- Concept preserves beige compact-Mac shell, underside base, four short articulated legs, rounded dark feet, vents/handle recess/floppy-slot detail. — README.md:50-58

### SELECTED OR NOT
- **Selected:** accepted appearance and WB-8 donor clock; no engineered/approved leg placement. — docs/product-spec.md:18,25; hardware/joints/leg-layout.md:1-5
- **Proposed:** three-axis leg; direct-knee baseline compared with proximal belt drive; supported shafts/bearings and replaceable feet. — hardware/joints/leg-layout.md:20-95; hardware/joints/README.md:20-43
- **Not selected:** direct vs proximal knee; A/C/D placement; materials, print orientation, final cradle, foot compliance, cable routing. — hardware/joints/leg-packaging.md:1-30; STATUS.md:11
- **P2S selected** for printer only; not ordered. — hardware/printer-comparison.md:86-111; STATUS.md:9

### OPEN
- Measure actual clock and retained parts, internal clearances, mass and datums. — hardware/measurements.csv:1-29; docs/roadmap.md:8
- Redraw hinge frames, evaluate output-up knee, rerun placement A with equal links; add joint cable loops; measure real servo offset. — STATUS.md:279-281
- Determine contact reach, clearances, usable forces and protective envelope for R04. — hardware/integration-plan.md:24-30,91-93
- No physical leg, load-qualified geometry or manufacture-ready BOM is recorded. — docs/roadmap.md:33-38

## ACTUATION

### SAYS
- The study uses XL330-M288-T as size/mass benchmark: 20 × 34 × 26 mm, 18 g, 5 V, 0.52 N·m and 1.47 A stall (CATALOG); axis offset 11 mm is RECALLED pending measurement. — hardware/first-order.md:8-19; STATUS.md:9,11
- Twelve leg actuators are the J04 concept count (three per leg); recovery axes/count remain TBD. — hardware/system-budget.csv:11,14
- Bus servo candidates report position/current feedback, but actual feedback, thermal behavior and continuous torque are unqualified. — hardware/workshop-road.md:84-95; hardware/integration-plan.md:30,43

### SELECTED OR NOT
- **Selected for first order sheet, not purchased:** one XL330-M288-T bundled in ROBOTIS OpenRB-150 Starter Kit. **Not selected as fitted actuator.** — hardware/first-order.md:1-28; STATUS.md:9
- **Candidates:** XL330-M288-T, XC330, Feetech STS3032/SCS0009; no fitted motor selection. — hardware/workshop-road.md:86-90
- **Not selected:** actuator count for recovery, drive ratio, bus/controller, continuous torque or thermal limits. — hardware/system-budget.csv:11,14; hardware/integration-plan.md:30

### OPEN
- Measure torque/speed/current/heat and joint envelope; G5 restrained load/range/current/temperature/stop/fault tests. — hardware/workshop-road.md:18-20,86-90; docs/roadmap.md:12
- Define bus deadlines, calibration, overload response, command expiry and safe stop for actual actuator/controller pair. — docs/architecture.md:38-42,121-138

## ELECTRICAL AND POWER

### SAYS
- B04 sets protected lithium-ion direction; pack voltage/capacity, usable Wh and peak-current capability are not selected. — hardware/battery-power.md:1-28; docs/product-spec.md:22-24
- Separate compute/audio/sensor power from actuator peak demand; include regulated rails, protection, charge, return paths, connectors, startup/brownout and returned motor energy. — docs/architecture.md:156-159; hardware/integration-plan.md:54-65
- Solar examples: P124 1.14 W expected output; assumed 4 equivalent full-sun h/day and 80% delivery gives calculated 3.648 Wh/day; scenarios are not runtime predictions. — hardware/solar-feasibility.md:19-23,38-68
- D04 proposes return/align/seat/charge/undock state machine, local energy reserve and charge confirmation; no dock service is implemented. — docs/architecture.md:140-147

### SELECTED OR NOT
- Lithium-ion is primary; hydrogen hybrid is separate feasibility work. — docs/product-spec.md:22-24; hardware/integration-plan.md:75-80
- Solar roof is optional, unselected; dock solar is an alternative study. — hardware/solar-feasibility.md:7-13; hardware/system-budget.csv:16-17
- Battery, charger, fuse, wire gauge, dock contacts and power topology remain unselected. — hardware/integration-plan.md:63-65; hardware/system-budget.csv:8-9,18

### OPEN
- Measure battery bay and loaded-joint demand; select and qualify complete pack/power system. — STATUS.md:298
- Review schematic/harness/pin map; measure consumer rail voltage, transient current, temperatures, reset behavior and charge/run modes. — hardware/integration-plan.md:63-65
- Measure dock geometry, return energy, net charge and blocked-route/power-loss response. — STATUS.md:300; hardware/integration-plan.md:75-80
- Solar: measure roof area, awake/parked/shutdown draw and net harvested Wh before deciding. — hardware/solar-feasibility.md:96-109; STATUS.md:302

## COMPUTE AND CONTROL

### SAYS
- Host implementation runs on development Mac: browser desktop, local runtime, Ollama inference, SQLite memory and read-only tools; bootable Mack Linux image and physical controller are proposed. — docs/architecture.md:30-43,105-119
- Body-controller contract calls for monotonic deadlines, bounded named actions, acknowledgement/result separation, telemetry, stale/duplicate rejection, no auto-rearm after reconnect/reboot, modes unarmed/ready/executing/stopping/fault. — docs/architecture.md:121-138
- Tool limits: maximum four calls, three model requests, 120-second conversation deadline; only status, local time and saved-fact search tools. — docs/architecture.md:75-103

### SELECTED OR NOT
- Linux is product foundation; local onboard compute/control is self-contained target. — docs/product-spec.md:7-11,27-29
- Buildroot, ROS 2 and micro-ROS are references only, not selected; controller board/rates/deadlines unknown. — docs/architecture.md:38-42,105-110,136-139
- OpenRB-150 selected as first-order adapter/board sheet, no purchase; ESP32-S3 or RP2040 class remains bench-plan candidate. — hardware/first-order.md:8-28; hardware/workshop-road.md:68-75

### OPEN
- Implement simulated body and prove expiry, rejection, interruption and recovery. — STATUS.md:264
- Select onboard board/controller, interfaces, loop/deadline and local stop response; produce device image and boot recovery. — docs/architecture.md:38-43,105-110

## SENSING

### SAYS
- Proposed sensing functions include microphone, IMU, short-range obstacle range/contact, floor/edge, joint state/current/temperature and camera. — hardware/integration-plan.md:32-47
- Physical runtime currently reports no sensors or motion actions. — docs/architecture.md:57-61

### SELECTED OR NOT
- Candidate IMUs BNO08x/ICM-42688; dock ToF VL53L1X/VL53L4; foot contact FSR, microswitch or servo current; current monitor INA219/INA228; none selected. — hardware/workshop-road.md:90-95
- Camera count and optical route unselected; local microphone capture is implemented on host, but physical microphone acceptance pending. — hardware/integration-plan.md:38-46; software/mack/LISTENING.md:145-174

### OPEN
- Choose sensors, count, placement, interface, health/freshness and environmental coverage; test representative materials, angles, surfaces, tilt and invalid readings. — hardware/integration-plan.md:36-47
- Bill's built-in microphone trial, broader recognition, streaming/latency and disconnected reboot remain open in STATUS. — STATUS.md:275

## DISPLAY AND FACE

### SAYS
- Intent is convex CRT-like face, concealed camera, ideally behind screen; optical path remains open. — docs/product-spec.md:19
- F04 compares curved cover/hidden-window/under-display options and optical paths. — hardware/display-and-vision.md:1-35

### SELECTED OR NOT
- Accepted appearance image is selected as visual target; no display, cover, camera or optical stack selected. — README.md:27-30,50-58; hardware/integration-plan.md:49-53

### OPEN
- Cover distortion/transmission, display crosstalk, sightline, aperture, baffles, service access, viewing angle and camera acceptance. — hardware/integration-plan.md:9-12,45-53

## AI AND SOFTWARE

### SAYS
- Mack Local AI 0.3 runs on development Mac; local Qwen3.6:35b via Ollama, SQLite archive/facts, installed-model selector, read-only status/time/memory tools, local Qwen3-ASR and approved local voice v1. — README.md:31-39; docs/architecture.md:75-99,113-119
- Voice v1 is reference-conditioned Qwen3-TTS/MLX with light echo; SAL resemblance is direction, not guaranteed likeness. — software/mack/VOICE.md:1-24; docs/personality-and-voice.md:6-15
- Memory is explicit fact store plus conversation archive; learning/routines, automated backups and Continuum integration remain future work. — docs/product-spec.md:30-51; docs/architecture.md:37,95-103

### SELECTED OR NOT
- Local-first; optional cloud assistance for harder tasks is a direction, no cloud adapter configured. — docs/model-strategy.md:1-20; docs/architecture.md:101-103,117-119
- Authentic Mac OS 9.0.4/legacy apps are optional, not prerequisite. — README.md:73; docs/roadmap.md:16
- Continuum/Terrarium/Exocortex bridges proposed only; imported Continuum code is not adapted for this body. — docs/model-strategy.md:64-96; software/README.md:1-23

### OPEN
- Offline reboot, longer speech, onboard performance, everyday microphone acceptance, model quality/latency, staged upgrades/rollback and simulated body contract. — README.md:39-48,80; STATUS.md:264,273-277

## SAFETY AND TEST

### SAYS
- Stop and required protection inputs must reach independent controller, bypassing browser/AI; exact topology and response not engineered. — docs/architecture.md:28-29
- STATUS reports process-scoped offline checks for Mac speech/conversation/recall, recorded-speech tests and accepted voice generation; no physical motion hardware connected. — README.md:71; docs/architecture.md:115-119; docs/build-log.md:7-23
- Leg animation and CAD are kinematic/rigid-envelope only, with no structural analysis or physical testing. — STATUS.md:5,11; hardware/joints/cad/exports/l02-comparison.json:1-8

### SELECTED OR NOT
- Independent local stop, local limits, bounded action contract and deliberate arming are design requirements; no qualified controller or stop circuit selected. — docs/architecture.md:28,121-138

### OPEN
- G5 load/range/current/temperature/stop/fault; G6 stability, surfaces, edges, link-loss, R04 recovery; G7 integration; P10 recovery/install/service. — docs/roadmap.md:12-15
- Define safe response to torque removal, power loss, invalid/stale sensing, overheating, brownout and reconnect. — docs/architecture.md:134-138; hardware/integration-plan.md:63-65,87-93

## BUDGETS

- Retained clock shell mass: blank, `unmeasured`; display/mount, compute/cooling, controller and audio: blank, `unselected`. — hardware/system-budget.csv:2-6
- Battery assembly: B04 direction, pack unselected; no mass, rail or power figures. — hardware/system-budget.csv:8
- Twelve leg actuators: J04 concept count, unselected; actual mass/power/duty unmeasured. — hardware/system-budget.csv:11
- Structure/feet undesigned; harness unmeasured; recovery assembly conditional and count/axes TBD. — hardware/system-budget.csv:12-14
- Roof solar panel/path optional and unselected; dock interface proposed/unselected. — hardware/system-budget.csv:16-18
- Solar study: 1.14 W P124 expected CATALOG; 4 h/day and 80% factor ASSUMED; 3.648 Wh/day CALCULATED; hypothetical 5 W/15 W/50 W loads and 43.8/14.6/4.4 min CALCULATED. — hardware/solar-feasibility.md:19-23,38-68
- Budget CSV has no populated total robot mass, power, energy or cost; blank cells remain unknown. — hardware/system-budget.csv:1-18

## CONTRADICTIONS

- Printer: older W04 road says printer candidates not picks / lean enclosed class; later STATUS records Bill selecting P2S on 2026-11-10; road itself updates that selection. — hardware/workshop-road.md:38-57; STATUS.md:9
- First order: older road says two benchmark servos/U2D2 as sensible order; later first-order decision prices one servo and OpenRB-150, and STATUS explicitly records replacement. — hardware/workshop-road.md:97-103; hardware/first-order.md:1-28; STATUS.md:9
- Screen/voice: old STATUS entries call stock Samantha a temporary/current study; later entries accept reference-conditioned light-echo voice v1 and README says approved voice v1 default. Older dated text remains in log as history, while current status supersedes it. — STATUS.md:213,199,193; README.md:39,43-48
- Project repository: STATUS says created private on 2026-10-20, then public on 2026-10-21; the first is explicitly superseded. — STATUS.md:217,221
- Earlier layout height of about 173 mm and crouch about 158 mm in captured handoff are superseded by the 2026-11-10 J04-L02 placement results; old snippet remains in STATUS. — STATUS.md:11, captured handoff around lines 60-75
- CAD comparison JSON has revision `J04-L02-D01` with headline sweep outputs; STATUS's 2026-11-11 kinematic crawl uses different script conditions and explicitly says no physics/interference proof. These are different evidence scopes, not equivalent walk claims. — hardware/joints/cad/exports/l02-comparison.json:1-8; STATUS.md:5

## SILENT

- **MECHANICAL:** quantified shell strength, material fatigue/creep, fastener retention under repeated gait, wear life, ingress rating, acoustic vibration limits.
- **ACTUATION:** continuous torque curve, gearbox life/backlash, actuator duty cycle and measured thermal derating.
- **ELECTRICAL AND POWER:** selected pack chemistry/capacity/voltage, fuse values, wire gauges, schematic, connector ratings, EMC/ESD qualification.
- **COMPUTE AND CONTROL:** chosen MCU/compute, real-time deadlines, bus electrical standard and firmware release process.
- **SENSING:** selected sensor instances/counts, calibrated accuracy and false-positive/negative rates.
- **DISPLAY AND FACE:** selected panel, cover material, luminance/brightness target and optical prescription.
- **AI AND SOFTWARE:** privacy/retention policy for camera data and a completed offline recovery image.
- **SAFETY AND TEST:** formal hazard analysis and independent third-party qualification.
- **BUDGETS:** total assembled mass, center of gravity, runtime, total power and approved total cost.

## MAP
- `README.md` — M.A.C. Model 04; last date mentioned: 2026-10-20. — README.md:1
- `STATUS.md` — STATUS — M.A.C. Model 04 (Mack); last date mentioned: 2026-11-11. — STATUS.md:1
- `docs/architecture.md` — M.A.C. Model 04 — system architecture; last date mentioned: 2026-10-21. — docs/architecture.md:1
- `docs/build-log.md` — Building Mack in public; last date mentioned: 2026-11-10. — docs/build-log.md:1
- `docs/model-strategy.md` — Mack’s intelligence and model strategy; last date mentioned: 2026-10-21. — docs/model-strategy.md:1
- `docs/motion-training.md` — Mack's virtual practice room; last date mentioned: 2026-10-21. — docs/motion-training.md:1
- `docs/personality-and-voice.md` — Mack's personality and voice; last date mentioned: 2026-10-21. — docs/personality-and-voice.md:1
- `docs/product-spec.md` — M.A.C. Model 04 — product definition; last date mentioned: 2026-10-21. — docs/product-spec.md:1
- `docs/public-introduction.md` — Mack — public introduction; last date mentioned: 2026-10-23. — docs/public-introduction.md:1
- `docs/references.md` — M.A.C. Model 04 — references and reuse; last date mentioned: 2026-10-21. — docs/references.md:1
- `docs/research-notes.md` — Research notes — M.A.C. Model 04; last date mentioned: 2026-11-10. — docs/research-notes.md:1
- `docs/roadmap.md` — M.A.C. Model 04 — build roadmap; last date mentioned: no date stated. — docs/roadmap.md:1
- `hardware/README.md` — M.A.C. Model 04 — hardware workspace; last date mentioned: 2026-11-11. — hardware/README.md:1
- `hardware/battery-power.md` — Mack B04 — lithium-ion power system; last date mentioned: 2026-10-21. — hardware/battery-power.md:1
- `hardware/bench-list.md` — Bench list: where to click (W04, stage 3); last date mentioned: 2026-11-11. — hardware/bench-list.md:1
- `hardware/buy-list.md` — Buy list: where to click (W04, stages 0 to 2); last date mentioned: 2026-11-10. — hardware/buy-list.md:1
- `hardware/charging-dock.md` — Mack D04 — return home and recharge; last date mentioned: 2026-10-21. — hardware/charging-dock.md:1
- `hardware/dell-cad-handoff.md` — Home Dell — Mack CAD and analysis handoff; last date mentioned: 2026-10-21. — hardware/dell-cad-handoff.md:1
- `hardware/display-and-vision.md` — Mack — curved face and concealed vision; last date mentioned: 2026-10-21. — hardware/display-and-vision.md:1
- `hardware/dock-parameters.csv` — hardware/dock-parameters.csv; last date mentioned: no date stated. — hardware/dock-parameters.csv:1
- `hardware/engineering-workflow.md` — Mack — from joint concept to manufactured hardware; last date mentioned: 2026-10-21. — hardware/engineering-workflow.md:1
- `hardware/first-order.md` — W04 stages 0 and 1 — the small first order, priced; last date mentioned: 2026-11-10. — hardware/first-order.md:1
- `hardware/integration-plan.md` — Mack — fitted electronics and walking body; last date mentioned: 2026-10-21. — hardware/integration-plan.md:1
- `hardware/joints/README.md` — Mack J04 — joint and recovery design study; last date mentioned: 2026-11-10. — hardware/joints/README.md:1
- `hardware/joints/cad/README.md` — J04-C01 — editable joint cartridge study; last date mentioned: no date stated. — hardware/joints/cad/README.md:1
- `hardware/joints/cad/briefs/J04-L02-ANIMATION-BRIEF-REPORT.md` — J04-L02-V01 — animated CAD views: build report; last date mentioned: no date stated. — hardware/joints/cad/briefs/J04-L02-ANIMATION-BRIEF-REPORT.md:1
- `hardware/joints/cad/briefs/J04-L02-ANIMATION-BRIEF.md` — J04-L02-V01 — build brief: animated views of the leg and of Mack walking (kinematic illustration); last date mentioned: no date stated. — hardware/joints/cad/briefs/J04-L02-ANIMATION-BRIEF.md:1
- `hardware/joints/cad/briefs/J04-L02-BUILD-BRIEF-REPORT.md` — J04-L02 build brief report; last date mentioned: no date stated. — hardware/joints/cad/briefs/J04-L02-BUILD-BRIEF-REPORT.md:1
- `hardware/joints/cad/briefs/J04-L02-BUILD-BRIEF.md` — J04-L02 — build brief: one complete three-axis leg and cradle interface (packaging model); last date mentioned: no date stated. — hardware/joints/cad/briefs/J04-L02-BUILD-BRIEF.md:1
- `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF-REPORT.md` — J04-L02-F01 figures build report; last date mentioned: no date stated. — hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF-REPORT.md:1
- `hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF.md` — J04-L02-F01 — build brief: three labelled still figures of the leg, drawn from the CAD model; last date mentioned: 2026-11-11. — hardware/joints/cad/briefs/J04-L02-FIGURES-BRIEF.md:1
- `hardware/joints/cad/briefs/J04-MODELS-BRIEF.md` — J04-M01 — build brief: 3D model files a visitor can spin in the browser on the repository page; last date mentioned: no date stated. — hardware/joints/cad/briefs/J04-MODELS-BRIEF.md:1
- `hardware/joints/cad/exports/geometry-check.json` — hardware/joints/cad/exports/geometry-check.json; last date mentioned: no date stated. — hardware/joints/cad/exports/geometry-check.json:1
- `hardware/joints/cad/exports/l02-A-under-direct/geometry-check.json` — hardware/joints/cad/exports/l02-A-under-direct/geometry-check.json; last date mentioned: no date stated. — hardware/joints/cad/exports/l02-A-under-direct/geometry-check.json:1
- `hardware/joints/cad/exports/l02-A-under-proximal/geometry-check.json` — hardware/joints/cad/exports/l02-A-under-proximal/geometry-check.json; last date mentioned: no date stated. — hardware/joints/cad/exports/l02-A-under-proximal/geometry-check.json:1
- `hardware/joints/cad/exports/l02-animation/gait-check.json` — hardware/joints/cad/exports/l02-animation/gait-check.json; last date mentioned: no date stated. — hardware/joints/cad/exports/l02-animation/gait-check.json:1
- `hardware/joints/cad/exports/l02-comparison.json` — hardware/joints/cad/exports/l02-comparison.json; last date mentioned: 2026-11-10. — hardware/joints/cad/exports/l02-comparison.json:1
- `hardware/joints/cad/exports/l02-sketch-direct/geometry-check.json` — hardware/joints/cad/exports/l02-sketch-direct/geometry-check.json; last date mentioned: no date stated. — hardware/joints/cad/exports/l02-sketch-direct/geometry-check.json:1
- `hardware/joints/cad/j04-c01.example.json` — hardware/joints/cad/j04-c01.example.json; last date mentioned: no date stated. — hardware/joints/cad/j04-c01.example.json:1
- `hardware/joints/cad/j04-l02.candidate-A-under.json` — hardware/joints/cad/j04-l02.candidate-A-under.json; last date mentioned: 2026-11-10. — hardware/joints/cad/j04-l02.candidate-A-under.json:1
- `hardware/joints/cad/j04-l02.candidate-C-hip-inside.json` — hardware/joints/cad/j04-l02.candidate-C-hip-inside.json; last date mentioned: 2026-11-10. — hardware/joints/cad/j04-l02.candidate-C-hip-inside.json:1
- `hardware/joints/cad/j04-l02.candidate-D-hips-inside.json` — hardware/joints/cad/j04-l02.candidate-D-hips-inside.json; last date mentioned: 2026-11-10. — hardware/joints/cad/j04-l02.candidate-D-hips-inside.json:1
- `hardware/joints/cad/j04-l02.example.json` — hardware/joints/cad/j04-l02.example.json; last date mentioned: 2026-11-10. — hardware/joints/cad/j04-l02.example.json:1
- `hardware/joints/leg-layout.md` — Mack — design the leg before the dock; last date mentioned: 2026-10-22. — hardware/joints/leg-layout.md:1
- `hardware/joints/leg-packaging.md` — Mack — one leg with its actuators in place; last date mentioned: 2026-11-10. — hardware/joints/leg-packaging.md:1
- `hardware/joints/recovery-envelope.md` — Mack R04 — recovery in every direction; last date mentioned: 2026-10-21. — hardware/joints/recovery-envelope.md:1
- `hardware/measurements.csv` — hardware/measurements.csv; last date mentioned: no date stated. — hardware/measurements.csv:1
- `hardware/parts.csv` — hardware/parts.csv; last date mentioned: no date stated. — hardware/parts.csv:1
- `hardware/printer-comparison.md` — W04 stage 2 — printer comparison; last date mentioned: 2026-11-10. — hardware/printer-comparison.md:1
- `hardware/solar-feasibility.md` — Mack S04 — optional solar charging; last date mentioned: 2026-10-21. — hardware/solar-feasibility.md:1
- `hardware/system-budget.csv` — hardware/system-budget.csv; last date mentioned: no date stated. — hardware/system-budget.csv:1
- `hardware/workshop-road.md` — W04 — workshop road: printer, bench and first parts; last date mentioned: 2026-11-11. — hardware/workshop-road.md:1
- `software/README.md` — M.A.C. Model 04 — software workspace; last date mentioned: 2026-10-20. — software/README.md:1
- `software/desktop/README.md` — Mack Local AI 0.3; last date mentioned: 2026-10-21. — software/desktop/README.md:1
- `software/mack/LISTENING.md` — Local listening and conversation archive; last date mentioned: 2026-10-21. — software/mack/LISTENING.md:1
- `software/mack/VOICE.md` — Local reference voice on Apple silicon; last date mentioned: 2026-10-21. — software/mack/VOICE.md:1
- `software/mack/identity.json` — software/mack/identity.json; last date mentioned: no date stated. — software/mack/identity.json:1
- `software/mack/persona.md` — Mack's SAL-inspired personality — revision 5; last date mentioned: 2026-10-21. — software/mack/persona.md:1
- `vendor/README.md` — Upstream snapshots and notices; last date mentioned: no date stated. — vendor/README.md:1
- `vendor/agentbridge/README.md` — AgentBridge; last date mentioned: no date stated. — vendor/agentbridge/README.md:1
- `vendor/agentbridge/SOURCE.md` — agentbridge — source record; last date mentioned: 2026-10-20. — vendor/agentbridge/SOURCE.md:1
- `vendor/continuum-hexapod/SOURCE.md` — continuum-hexapod — source record; last date mentioned: 2026-10-20. — vendor/continuum-hexapod/SOURCE.md:1
- `vendor/macintosh-mini/README.md` — vendor/macintosh-mini/README.md; last date mentioned: no date stated. — vendor/macintosh-mini/README.md:1
- `vendor/macintosh-mini/SOURCE.md` — macintosh-mini — source record; last date mentioned: 2026-10-20. — vendor/macintosh-mini/SOURCE.md:1
- `vendor/macintosh-mini/maclock-build/README.md` — Manual install; last date mentioned: no date stated. — vendor/macintosh-mini/maclock-build/README.md:1
- `vendor/macintosh-mini/maclock-pcb/README.md` — Macintosh Mini breakout PCB; last date mentioned: no date stated. — vendor/macintosh-mini/maclock-pcb/README.md:1
- `vendor/macintosh-mini/maclock-screen-bezel/README.md` — Macintosh Mini screen bezel; last date mentioned: no date stated. — vendor/macintosh-mini/maclock-screen-bezel/README.md:1
- `vendor/wondermac/README.md` — vendor/wondermac/README.md; last date mentioned: no date stated. — vendor/wondermac/README.md:1
- `vendor/wondermac/SOURCE.md` — wondermac — source record; last date mentioned: 2026-10-20. — vendor/wondermac/SOURCE.md:1

FACTS PASS DONE — 275-line digest written; browser proof unrun here; brain freshness unverified.
