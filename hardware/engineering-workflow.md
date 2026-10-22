# Mack — from joint concept to manufactured hardware

2026-10-21. Bill has personal Creo and Ansys installations on the **home Dell** and
is open to other tools that allow direct design help. Their versions, modules and
automation interfaces have not been inspected. The Mac now has a separate
build123d 0.12.0 environment and the [J04-C01 draft cartridge](joints/cad/README.md).

We can develop the complete mechanisms, drawings and analysis models, then have
parts made as each prototype passes its review. The present deliverable is the
first parametric packaging model. A reliable self-righting robot still requires
measured inputs, selected components, analysis and physical trials.

## Tool roles and model ownership

| Tool | Work it owns | Evidence before relying on it |
| --- | --- | --- |
| build123d on the Mac | Scripted dimensions, solid geometry, variants, STEP exports and geometry checks. | The D01 example generates and re-imports on Mac arm64/Python 3.12. New variants must be checked separately. |
| Creo on the home Dell | Detailed native parts, assembly datums, mechanisms, drawings and tolerances if selected as the next design master. | Exact version, installed capabilities, import units/solids and regeneration recorded locally. |
| Ansys on the home Dell | Structural/contact models and other analyses available in the installed modules. | Exact solver/modules, material data, boundary conditions, mesh convergence and correlation recorded. |
| Later multibody simulator | Leg workspace, ground contact, whole-body balance and candidate recovery trajectories. | Model identity, mass/inertia, actuator dynamics and friction matched to bench data; no simulator selected yet. |
| Protolabs or another reviewed fabricator | Process review, quotes and manufactured prototype parts. | Revision-specific quote, material/process/critical dimensions accepted before an order. |

The assistant can edit and run the scripted CAD here. Direct native Creo/Ansys
control depends on the Dell's available tools; it is not currently connected from
this Mac. Native STEP import is an exchange check, not proof that source features
or constraints transferred. Select one master per revision and name it in the
release record. Keep neutral exports beside their source, with unit and revision.

PTC offers Creo Ansys Simulation and a separate Advanced extension; available
analysis types depend on the licensed installation. Owning Creo and standalone
Ansys does not establish that those integrated extensions are installed.
[PTC product description](https://www.ptc.com/en/products/creo/ansys-simulation).

## Engineering sequence

| Stage | Design work | Exit evidence |
| --- | --- | --- |
| A — Physical intake | Measure RayCue exterior, internal keep-outs, mounting datums, retained masses and center of mass. Set intended payload, speed, surfaces, runtime and maximum size. | Filled [measurements](measurements.csv) and [system budget](system-budget.csv), with methods, photos and uncertainty. Unmeasured values stay blank. |
| B — Architecture and component envelopes | Package the cradle, battery, compute, sensors, three-axis legs and candidate recovery mechanisms. Compare actuator choices against torque/speed/thermal requirements. | Actual supplier models/datasheets, calculated joint demands and directed R04 recovery-contact paths. Prove pitch as well as roll coverage before fixing extra axis count. Preserve the accepted appearance where feasible. |
| C — One complete joint | Design shaft/hub coupling, bearing fits/retention, supports, fasteners, encoder, stops, cable routing and covers. Design its restrained test fixture. | Assembly/disassembly sequence, tolerance stack and tool access; real actuator interfaces; collision checks across travel. |
| D — One leg | Connect three qualified joint designs and a compliant foot. Include foot sensing and harness motion. | Workspace and singularities, load cases, analysis and restrained loaded-leg evidence. |
| E — Dummy four-leg body | Install representative mass/inertia, battery surrogate and protected contact geometry. | Standing/stepping, interruption and selected self-righting trials under the [J04 test plan](joints/README.md#prototype-and-acceptance-plan). |
| F — Integrated Mack | Install final display, electronics, power, cooling and harness. Repeat the demanding cases. | Actual assembly passes the relevant [product requirements](../docs/product-spec.md); software or network failure cannot defeat local stopping. |

The first quote should cover a **reviewed one-joint fixture**, then one leg.
Do not order twelve identical cartridges from a geometry-only example. Different
joint locations may need different ratios, bearings, supports or thermal designs.

## Loads and analysis definition

Build load cases from the measured body, selected actuators and intended motions.
For each joint, use foot-force/moment equilibrium and the kinematic Jacobian
(`tau = J^T F`, with joint/link gravity and inertial contributions added) rather
than dividing body weight by four. Evaluate bearing reactions, shaft bending and
torsion, hub coupling, yoke deflection and fastener loads along the complete path.
Record speed, acceleration, duty cycle and actuator limits alongside the torque.

| Case | Boundary conditions to establish | Main result |
| --- | --- | --- |
| Standing and crouching | Actual support polygon, full carried mass, plausible unequal foot loads and friction. | Joint torque, bearing reactions, link/yoke deflection and frame load distribution. |
| Stepping and body lean | Support transitions, foot lever arms, acceleration and off-axis forces. | Combined bending/torsion, joint travel and actuator torque/speed margins. |
| Recovery push/roll | Measured CoM/inertia, changing body contacts, foot/arm reach and friction; both pitch senses, both roll senses and mixed contacts in R04. | Required force/torque, optical clearance, usable contacts, slip risk, energy barrier and descent/braking; whole-body dynamics treated separately. |
| Stalled or interrupted motion | Selected actuator current/torque limit, stop geometry and actual power-loss response. | Local overload and stop/fastener demand without assuming a powered holding torque after power loss. |
| Tip-over/impact | Defined forward/backward/sideways/diagonal fall configuration, impact velocity, compliance, damping and successive contacts. | Transient demand, frame/optics and battery retention, or a justified conservative bound; no arbitrary universal impact multiplier. |
| Repeated use and heat | Actual load history, dwell, ambient/motor heat, assembly preload and material process. | Fatigue/creep/loosening and temperature effects where credible material data and tools exist. |

For an Ansys study, preserve the CAD revision/hash, solver/version, units, material
source and process, contacts/friction, fastener or bearing representations,
constraints, loads, mesh settings, convergence and result extraction method.
Report displacement and reactions as well as stress. Check force/moment balance
and simple beam/shaft calculations; refine the mesh around load-bearing features
and distinguish singular stress peaks from meaningful design values. Select the
allowable and margin before declaring a result acceptable.

Avoid accidentally bonding moving interfaces. Creo's automatic contact detection
uses bonded contacts by default; review every joint/bearing/contact explicitly.
[PTC contact documentation](https://support.ptc.com/help/creo/creo_pma/r12/usascii/simulate/ansys_simulation/contacts_ansys_sim.html).
Sliding, separation and friction are nonlinear contact issues; use only the
available, verified analysis capabilities.
[Ansys contact topics](https://www.ansys.com/training-center/course-catalog/structures/fundamental-topics-in-nonlinear-contact).

A successful stress calculation does not establish walking stability or
self-righting. Ground contact, reach, actuator dynamics, sensing and a recovery
controller need simulation and restrained physical correlation. The tall body may
require an additional recovery mechanism even when the legs are strong enough.
The [R04 matrix](joints/recovery-envelope.md#qualification-matrix-to-populate)
separates fore/aft pitch, sideways roll, mixed contacts and accidental tumbling.
Model and qualify each direction independently, including contact handovers and
stopping near the center-of-mass height maximum. Keep the convex face and cameras
inside the loaded, tolerance-adjusted protective envelope throughout each path.

## Materials and fabrication route

Use a hybrid structure. Purchased bearings, actuators and fasteners supply defined
interfaces. Metal shafts and candidate machined bearing carriers handle demanding
fits. Printed covers, fit models and selected brackets can reduce cost and simplify
iteration. A structural printed part still needs process-specific properties,
orientation/condition controls, creep assessment and representative tests.

Protolabs offers MJF nylon parts and SLS services. MJF is a candidate for nylon
covers and reviewed housings; it is not evidence that this yoke is strong enough.
Finish, material, colour and process availability must be confirmed for the selected
service and region. [MJF service](https://www.protolabs.com/services/3d-printing/multi-jet-fusion/)
and [printing services](https://www.protolabs.com/services/3d-printing/).

Critical bearing seats and shaft fits need explicit dimensions, datums, finish and
inspection requirements. A vendor's general machining tolerance is not a designed
bearing fit. Choose fits from the actual bearing, load, temperature and process;
check whether post-machining, split carriers or replaceable metal inserts are
appropriate. [Protolabs machining tolerance guidance](https://www.protolabs.com/resources/design-tips/fine-tuning-tolerances-for-cnc-machined-parts/).

## Release package for the first manufactured joint

The release record should contain the part/assembly numbers and revision, owning
CAD source, STEP solids in mm, dimensioned drawings for critical features,
material/process/finish, quantities, purchased-component BOM and datasheets,
assembly/retention instructions and inspection criteria. Include cable/encoder
interfaces and the matching restrained test plan. Check all exports against the
master model before upload. Mesh files may accompany printing quotes where
required, but they do not carry the complete tolerance specification.

Obtain DFM feedback and a revision-specific quote, then resolve changes in the
master and analysis together. Bill approves expenditure against the concrete
quote before an order. No account, CAD upload, quote or order has been submitted
as part of this initial tool setup.

## Current handoff

The [Dell engineering brief](dell-cad-handoff.md) starts by inspecting the actual
Creo/Ansys versions and importing D01. It does not assume a Dell path, installed
module or working automation connection. The D01 model's open interfaces are
listed in its [CAD guide](joints/cad/README.md#open-mechanical-interfaces).
