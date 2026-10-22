# Mack — fitted electronics and walking body

Engineering proposal v0.1, updated 2026-10-21. Implements [P05–P13](../docs/product-spec.md). No components, dimensions, pin assignments, load limits or power topology are approved by this document.

## Package the whole robot

Treat the clock, base, legs, battery, compute, display, audio and sensors as one assembly. Preserve the accepted silhouette while maintaining structural load paths, usable cooling, and access for assembly and service.

| Zone | Proposed contents | Design evidence needed |
| --- | --- | --- |
| Screen and upper shell | Display, curved front cover, concealed camera assembly, main compute and audio. | Usable volume, camera sightline, cover distortion/transmission, display crosstalk, connectors, viewing angle, microphone isolation, cooling and service access. |
| Underside base | Structural frame, body controller, power distribution; battery as low as practical. | Mounting datums, leg load paths, center of gravity, battery removal, ground clearance and stop access. |
| Four legs | Supported joints, actuators, covers, cable paths and compliant feet. | Link geometry, joint ranges, load/current/temperature measurements, cable bend clearance and replaceable wear parts. |
| Roof, optional | Recessed solar panel and protected wiring. | Net harvested Wh, usable area after vents/guards, temperature, added CoM/inertia and full rollover clearance; see [S04](solar-feasibility.md). |

The clock's cosmetic shell cannot be presumed to carry gait loads. Design a frame that connects the body mass and leg mounts. Keep battery placement adjustable during balance trials. Do not derive scale or joint axes from the concept image.

## Clock intake and engineering budgets

Record actual measurements in [measurements.csv](measurements.csv), including model/revision and what each mass contains. Use named mounting datums and photos for dimensions. Populate [system-budget.csv](system-budget.csv) as assemblies are selected; blank means unknown.

Before selecting motors or committing CAD:

1. Inventory what remains from the clock and what is removed. Establish available internal volume and a mass breakdown without double-counting.
2. Lay out the display, compute, audio, battery and controller with their connectors and cable clearances. Reserve installation/removal paths.
3. Evaluate the [J04 joint and recovery proposal](joints/README.md): twelve leg actuators (three per leg), with additional recovery mechanism axes/count TBD. The [R04 study](joints/recovery-envelope.md) requires fore/aft, sideways, inverted and mixed-contact coverage. The original side-sweeping rear arm alone does not establish pitch recovery. Prove contact reach, usable forces and the complete protected path before selecting or dropping added mechanisms.
4. Calculate joint demands across proposed stances and steps, including support changes and dynamic loads; then validate on a restrained leg. Dividing total mass by four is not a sufficient motor-sizing method.
5. Budget electrical average and peak demand, heat and runtime for actual operating modes. A larger battery also adds mass and may increase actuator demand; iterate the complete design.

Record vendor ratings separately from measurements. Actuator stall torque is not a continuous operating rating. Do not order a full motor set from a marketing torque value alone.

## Sensing baseline to evaluate

These are proposed functions, not a shopping list. Counts, placement and interfaces follow tests.

| Function | Candidate method | Placement/integration question | Acceptance evidence |
| --- | --- | --- | --- |
| Hear and respond | Microphone, speaker and amplifier | Can Mack hear speech with playback, cooling and motors active? | Capture/playback latency and intelligibility tests in the assembled shell; clear mute/capture state. |
| Body orientation | IMU | Rigid body mount, vibration and coordinate calibration. | Known tilt tests, sample age and missing-data detection. |
| Obstacles | Short-range distance sensing and/or contact bumper | Field of view must cover the chosen direction and body/leg swept volume. | Detection and stopping tests across representative materials and approach angles. |
| Floor/edge awareness | Downward range sensing and, if needed, foot contact feedback | Coverage changes through the gait; dark/glossy surfaces and mounting height matter. | Controlled tests on the approved surfaces, invalid-reading behavior, and measured stopping margin. No table-edge operation is qualified yet. |
| Power and heat | Rail voltage/current, battery and relevant device/actuator temperature | Required channels depend on chosen parts and power architecture. | Load peaks, brownout, low-energy and heating responses recorded with the full assembly. |
| Joint state | Available actuator position/current/temperature feedback or added sensing | Feedback capability changes motor/controller selection and wiring. | Detect or explicitly bound stalled/failed movement; no fictional feedback for an open-loop servo. |
| User input and interruption | Accessible stop input; deliberate interaction/mute controls | Reachable during a fault; local path independent of UI and AI. | Stop under host/link failure; deliberate recovery and no automatic movement on restart. |
| Visual understanding | Camera assembly; count and optical route unselected | Curved cover and concealed optics per the F04 study; aperture, light loss, baffles, compute cost and capture indication. | Useful perception through the assembled face, including display-content interference and motion; retention agreed before recording. |

Sensor observations used for immediate body protection must be available to the local controller or another independently qualified local path. A cloud vision response cannot be the sole obstacle or edge protection.

The [F04 study](display-and-vision.md) carries Bill's curved-screen and concealed
camera intent. A camera behind a shared curved cover is distinct from one behind
active display pixels. Reserve optical volume and access in the packaging model
before closing the upper shell; no camera or optical stack is selected yet.

## Electrical work package

The [B04 power study](battery-power.md) uses a protected, serviceable lithium-ion
pack low in the cradle as the working direction. It separates stored energy from
peak-current capability and proposes regulated compute power, an independently
controlled actuator branch and local battery supervision. Select pack voltage and
capacity from measured loads and usable volume. Include returned motor energy,
full-pack braking and loss-of-power behavior in R04 recovery qualification.

Produce a reviewed schematic and harness/pin map covering battery protection and charging, regulated compute supply, actuator power, grounding/return paths, switching, protection devices, connectors and accessible isolation. Specify voltage/current ratings and connector keying from selected hardware; the reference clock PCB does not establish these.

Test actuator transient load while compute, display and audio run. Record voltage at the consumers, current peaks, temperatures and reset behavior. Check charge/run behavior as a separate mode. No battery pack, charger, wire gauge or fuse value is selected here.

Bill requested roof solar if it produces enough useful energy. The
[solar study](solar-feasibility.md) recommends evaluating it as supplemental
charging, with a compatible regulated charge/power path and low-power parked mode.
Record generation separately from consumption; panel presence does not mean net
charging. Keep the normal battery/dock baseline independent of sunlight.

## Mechanical proof sequence

The [D04 dock](charging-dock.md) adds an external support saddle, calibrated
marker, gated charging source and robot-side recessed contacts/cradle shoes.
Reserve its interface clear of the battery, leg sweep and R04 ground-contact
envelope. Qualify return-energy estimates, alignment, measured net charging and
loss-of-power/blocked-route behavior. Keep stationary dock mass out of the moving
robot budget. Lithium-ion is primary; a fuel-cell hybrid remains separate research.

The [engineering workflow](engineering-workflow.md) defines CAD ownership, the
home Dell import/analysis work and staged manufacturing. The first
[J04-C01 model](joints/cad/README.md) is example cartridge geometry; it does not
replace the measured intake or qualify the joint's missing mechanical interfaces.

Fit models → one supported joint → one restrained loaded leg → four-leg base with representative dummy mass → complete stationary Mack → restrained integrated motion → supervised floor walking. Save CAD revision, parts, firmware, calibration, measured load, surface, limit settings and results for each test.

Before each powered test, set the numerical pass limits for that configuration. Do not mark a gait qualified from animation or simulation. Confirm stability, grip, joint heating, current, cable clearance, loosened fasteners and stopping/recovery through repeated runs.

Self-righting adds protected resting contacts, an inverted reach/collision study, and
a recovery matrix with a representative dummy body before the real display and
battery assembly. See [J04 acceptance stages](joints/README.md#prototype-and-acceptance-plan).

## Release evidence

The assembled product needs editable CAD and drawings, printable part exports, purchased-part BOM, schematic/PCB/harness files, assembly order, calibration data and instructions, service access, and results linked to [the roadmap](../docs/roadmap.md). At present these are deliverables to create.
