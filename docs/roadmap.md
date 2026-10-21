# M.A.C. Model 04 — build roadmap

The goal is the complete [Mack product](product-spec.md): its own system on Linux, intelligence, memory, sensing, fitted electronics and four-leg body. The accepted image sets the appearance. These are evidence gates, not a calendar estimate; a gate stays open until its tests pass.

| Gate | Build or learn | Done when |
| --- | --- | --- |
| G0 — Foundation; built | Repository, provenance, accepted concept, and host desktop preview. | Imported hashes verify; desktop interactions and truthful demo labels pass. The physical screen and live intelligence remain open. |
| G1 — Product envelope; open | Clock intake, operating environment, requirements, mass/space/power budgets and sensing plan. | Measured unit geometry and retained-component masses; numerical targets and budget recorded before part selection. |
| G2 — Integrated host system; open | Local runtime, durable memory, provider boundary, service states, and mock body. | Desktop request reaches the service and returns a truthful result; memory survives restart; simulated commands exercise rejection, expiry and recovery. |
| G3 — Live intelligence; open | Selected inference, microphone and speech output, interruptible dialogue, retention controls. | Spoken request/response and memory work; latency measured; disconnect/cancellation and offline behavior demonstrated. |
| G4 — Stationary embodied Mack; open | Selected Linux compute, boot-to-Mack, fitted display/audio/sensors, controller link and reviewed power. | Shell closes and is serviceable; sensor health is real; measured voltage, heat, sound and performance satisfy G1 limits. |
| G5 — Qualified leg; open | Selected actuator arrangement, supported joints, firmware, calibration and restrained loaded-leg fixture. | Representative load/range/current/temperature and stop/fault cases pass recorded numerical limits. |
| G6 — Qualified base; open | Four legs, representative dummy body/battery mass, gait and local protection. | Stands, steps, turns and stops on defined surfaces; stability, edge/obstacle response and link-loss behavior pass. |
| G7 — Integrated personal robot; open | Complete Mack, onboard battery, voice/personality/memory/perception and bounded movement. | P01–P09 pass on the actual assembly, including simultaneous voice/motion, network loss, reboot and no automatic movement after recovery. |
| G8 — Reproducible product build; open | Versioned CAD/BOM/harness, installation image, assembly/calibration, backup/update recovery and service instructions. | Another clean build can be installed/calibrated from the record; P10 and repeated-use tests pass. Commercial production is a separate scope. |
| Optional — Vintage apps | Separate emulator and possibly AgentBridge. | Selected apps work independently of the companion's control system. |

## Dependencies and next work

G1 physical intake and G2 host software can progress independently. G3 follows the host service boundary. G4 needs the packaging/power evidence and selected board. G5 needs the mass/load budget and actuator choice; it can proceed alongside stationary electronics. G6 uses representative mass, and G7 requires both G4 and G6. Reassess the mass and power budgets when any part changes.

Local AI 0.2 now covers the desktop/runtime boundary, persistent memories, installed-model switching and local inference. G2 stays open for the simulated body contract; G3 stays open for verified spoken input, broader latency/quality evaluation and interruption qualification. Immediate software work: the simulated body path and model/voice evaluation. Immediate physical input: clock model, exterior dimensions and total mass, followed by internal clearances and retained-part masses. See [measurements](../hardware/measurements.csv), [system budget](../hardware/system-budget.csv), and [integration plan](../hardware/integration-plan.md).

The existing bezel is printable reference material. The robot picture does not contain printable leg geometry. Imported Continuum tests and abstractions can be evaluated before adopting code; no upstream geometry or limits are accepted without Mack-specific validation.

No purchase-ready BOM, leg CAD, bootable device image, or live Mack motor driver exists yet. Each gate will carry its own revision, test conditions, results and remaining limits.
