# M.A.C. Model 04 — product definition

Owner: Bill. Intent confirmed 2026-10-20. Engineering baseline: proposed v0.1.

## The product

**Mack is an original, integrated personal robot in the accepted compact Mac form.** Its operating environment, personality, memory, sensing, electronics, and four-leg mechanism are developed as one product. The Mac OS 9-inspired screen is its face and everyday interface. Walking and sensing are core parts of the finished product.

Bill confirmed **Mack's own system on Linux** on 2026-10-20. Linux supplies the kernel and hardware foundation. Mack supplies the experience, services, behavior, body integration, and device configuration. “Mack system” is a working description, not another ratified product name. A new kernel is outside this baseline.

The current browser desktop connects to real local AI, durable memory and read-only tools on the development Mac. A bootable robot system and physical body remain to be built. A finished personal prototype and a production-ready commercial product are separate release gates below; no sales, manufacturing volume, certification, or budget has been agreed.

## Decisions already made

- Formal name: **M.A.C. Model 04**, Mobile Autonomous Computer. Everyday name: **Mack**.
- Identity: **she/her**, with SAL-inspired plain, calm conversation. Identity and memory persist independently of models and bodies.
- Long-term direction: grow a personalized intelligence through a continuing history with her person, then carry her into a humanoid body for fuller everyday interaction, years from now. The first physical release remains the accepted four-legged Mac. A later body requires separate engineering and qualification.
- Appearance: [Bill's accepted image](../concepts/raycue-build-target.png), a dominant beige compact Mac body, compact underside base, four short articulated legs, and rounded dark feet.
- Face and vision intent, added 2026-10-21: a convex CRT-like screen appearance, with camera hardware visually concealed and ideally behind the screen. Evaluate a common curved cover, hidden optical windows and true under-display alternatives; the final optical route remains open.
- Motion intent, added 2026-10-21: dexterous foot/body placement and self-righting after a fall. Qualify the recoverable poses and surfaces explicitly; do not promise recovery from every fall.
- Development intent, added 2026-10-21: a modest [virtual physical practice room](motion-training.md) for walking, maneuvering, obstacles and steps. Train and test before staged hardware transfer; no current learned locomotion or stair-climbing capability is claimed.
- Optional energy feature, added 2026-10-21: a roof solar panel if measured energy benefit justifies it. [S04](../hardware/solar-feasibility.md) evaluates supplemental charging and a larger solar dock alternative; no solar-autonomy promise or selected hardware.
- Starting enclosure: Bill's RayCue clock. Preserve its character while engineering the internal structure and base around measured loads.
- Everyday experience: an original classic Mac-style interface over modern intelligence and robotics. Authentic vintage applications are a minor, optional mode.
- System foundation: Linux with Mack's own interface, AI integration, memory, and robot software.
- Development starts on Bill's Mac and progresses into the physical robot. The final target carries its own compute, controller, sensors, and battery.

## Long-term purpose: a personalized intelligence

Bill clarified on 2026-10-21 that the lasting product is Mack's personalized
intelligence. Through conversation, shared activities and deliberately retained
memories, she should come to know his preferences, projects and ways of working.
Corrections should matter, useful routines should develop, and her familiar
personality should continue as models and tools improve.

The eventual humanoid body is intended to support a fuller interaction experience:
conversation, perception, expressive gestures, movement and practical assistance
in shared physical surroundings. This is a long-term goal beyond the first Mac
robot's release gates. Identity and memory continuity are design requirements;
humanoid mechanisms and autonomous physical skills remain future engineering.

Personalization must remain inspectable and correctable by the person. The current
runtime implements explicit saved facts, recent conversation and a stable persona.
Learning routines, richer experience memory and adaptation over time remain work
to build and evaluate; storing notes does not retrain the foundation model.

SAL-inspired voice and manner are central to Bill's conception of Mack. Voice
acceptance requires his audition of newly synthesized conversation, alongside
reliable interruption and clear delivery. Bill accepted the second reference-conditioned, light-echo audition on 2026-10-21; its sound is preserved as voice v1. The stock Mac voice remains an optional alternative. This acceptance does not close long-form speech, disconnected operation or onboard performance checks.

## What “complete” must demonstrate

These acceptance requirements define the complete embodied product. Host-side conversation, memory and tools have been verified, but no complete embodied requirement has passed yet.

| ID | Requirement | Evidence required |
| --- | --- | --- |
| P01 | One coherent device | Power-on reaches Mack's interface without a development terminal or a separate host UI. Hardware and software revisions are recorded. |
| P02 | Recognizable character | Bill accepts screen, voice, proportions, stance, and interactions in the actual assembled enclosure. |
| P03 | Conversation | A microphone request produces a response with truthful listening/thinking/speaking/error state; interruption works. Measure latency and audibility with the motors operating. |
| P04 | Durable memory | Mack recalls an explicitly saved fact after reboot. The user can inspect, correct, remove, export, and recover memory; retention behavior is documented. Browser notes alone do not satisfy this. |
| P05 | Sensing | Selected sensors report timestamped observations and health. Test obstacle, floor/edge, tilt, and power conditions in the agreed operating environment; missing/stale readings remain distinguishable from clear readings. |
| P06 | Four-leg movement | The assembled robot stands, steps, turns, and stops within a measured load, surface, speed, and stability envelope. The accepted appearance survives the packaging changes. |
| P07 | Independent body control | Stop input, expired commands, link loss, controller restart, overload, and invalid sensor data have demonstrated responses independent of the UI and AI. Restart cannot replay a previous movement. |
| P08 | Self-contained operation | Battery powers the assembled robot; no development Mac is required. Basic state, local memory, stopping, and bounded control remain available without network access. Onboard versus optional remote AI inference is a separate decision. |
| P09 | Fitted electrical and mechanical design | Shell closes; cables clear every joint; mounts carry load; service access works. Record mass/center of gravity, rail voltage/current, heat, and sound with the complete assembly. |
| P10 | Repeatable ownership | A clean installation, calibration, backup/restore, failed-update recovery, and routine charging/service procedure work from the project instructions. |
| P11 | Dexterity and self-righting | Demonstrate controlled three-dimensional foot placement and recovery from qualified front-guard, rear, left/right side, inverted and mixed edge/corner poses. Assess front-to-back and back-to-front paths independently, plus sideways paths. Qualify controlled rolls separately from accidental-tumble protection. Keep curved cover and camera window clear throughout each qualified path. Record surface, mass/CoM, direction, attempts, time, contacts, current/temperature and stopping/failure. Unsupported cases stop and request help. [R04 matrix](../hardware/joints/recovery-envelope.md). |
| P12 | Curved face and concealed vision | Bill accepts the curved compact-Mac appearance and camera concealment on the actual assembly under agreed lighting/viewing conditions. Demonstrate useful vision through the chosen cover/display stack with real desktop content, motion and dim/bright scenes. Record optical route, field of view, image quality/latency, capture state and disable control. Behind-cover placement is not claimed as behind-pixel imaging. [Optical study](../hardware/display-and-vision.md). |

## First embodied release

Proposed first physical release: one fully assembled personal prototype that converses, remembers, senses its immediate surroundings, and walks under supervision on an agreed level indoor surface. Its body and electronics travel with it. Final performance targets must be set before hardware selection; the picture supplies no dimensions or load ratings.

An initial acceptance demonstration is: power on → greet Bill → save and recall a fact → observe an obstacle → perform a requested short walk/turn → stop on command → interrupt a connection → show the resulting state → restart and retain the memory. Each movement requires its own qualified physical envelope. A successful scripted demo is insufficient evidence for unattended roaming or operation on a table edge.

The engineering record must name test conditions and quantitative pass limits **before** each physical test. Open targets include overall dimensions and mass, speed, runtime, response latency, audible noise, permitted surfaces, stop latency/distance, temperature limits, and budget. None has a fabricated target value here.

## Productization after the personal prototype

A reproducible build requires versioned CAD, drawings, schematic/PCB and harness, a sourced BOM, assembly instructions, calibration fixtures, software images, and logged acceptance results. Repair access, replaceable feet/joints, battery service, update recovery, and repeated-use testing belong in that release.

Commercial production would add a separately scoped manufacturing, support, and applicable product-compliance program. The current repository does not establish production readiness.

## Original work and reference material

Mack's product design and integration are ours to develop. The desktop code and assets are original. Linux, libraries, models, and any adapted upstream work remain attributed dependencies; “original” does not imply that their authorship changes. Training a new foundation model is not assumed.

Pinned `vendor/` snapshots are a reference library. Importing them does not install them or select them as Mack's runtime. Any adoption must be deliberate, tested, and recorded with its notices. Existing Continuum hexapod geometry, limits, and wiring never become Mack settings by copying them.

## Immediate engineering handoff

The local service now connects the desktop to durable memory, local inference and read-only tools. The next software work is qualified offline voice, reasoning evaluation and an explicitly simulated body. The next physical input is the clock's model, exterior/internal clearances, and masses. Those two tracks meet at a stationary fitted prototype before loaded walking tests.

See the [system architecture](architecture.md), [hardware integration plan](../hardware/integration-plan.md), and [release gates](roadmap.md).

## Intelligence deployment decision — 2026-10-21

Bill wants Mack as self-contained as possible, with a no-network mode using an onboard local model and optional cloud APIs/frontier reasoning when useful. Preserve memory, identity and body control locally. Ordinary interaction must not require a home inference server. Model updates must preserve remembered facts and must not grant new physical capabilities.

The target offline acceptance test is a cold boot with external networking unavailable, followed by local spoken interaction, saved-fact recall after restart and qualified body interruption/stop behavior. Assisted mode must visibly identify cloud use, send scoped context under the user’s selected policy and handle failure while preserving local operation. These are requirements for the finished system; Local AI 0.3 runs local recognition, inference, archive recall and approved speech output on the development Mac, with process-scoped offline checks passed. Disconnected cold boot and onboard performance remain unqualified. See [model strategy](model-strategy.md).
