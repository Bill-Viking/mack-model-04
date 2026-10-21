# M.A.C. Model 04 — product definition

Owner: Bill. Intent confirmed 2026-10-20. Engineering baseline: proposed v0.1.

## The product

**Mack is an original, integrated personal robot in the accepted compact Mac form.** Its operating environment, personality, memory, sensing, electronics, and four-leg mechanism are developed as one product. The Mac OS 9-inspired screen is its face and everyday interface. Walking and sensing are core parts of the finished product.

Bill confirmed **Mack's own system on Linux** on 2026-10-20. Linux supplies the kernel and hardware foundation. Mack supplies the experience, services, behavior, body integration, and device configuration. “Mack system” is a working description, not another ratified product name. A new kernel is outside this baseline.

The current browser desktop is one working component. It is not a bootable robot operating system or a live AI. A finished personal prototype and a production-ready commercial product are separate release gates below; no sales, manufacturing volume, certification, or budget has been agreed.

## Decisions already made

- Formal name: **M.A.C. Model 04**, Mobile Autonomous Computer. Everyday name: **Mack**.
- Appearance: [Bill's accepted image](../concepts/raycue-build-target.png), a dominant beige compact Mac body, compact underside base, four short articulated legs, and rounded dark feet.
- Starting enclosure: Bill's RayCue clock. Preserve its character while engineering the internal structure and base around measured loads.
- Everyday experience: an original classic Mac-style interface over modern intelligence and robotics. Authentic vintage applications are a minor, optional mode.
- System foundation: Linux with Mack's own interface, AI integration, memory, and robot software.
- Development starts on Bill's Mac and progresses into the physical robot. The final target carries its own compute, controller, sensors, and battery.

## What “complete” must demonstrate

These acceptance requirements define proposed engineering work. Except for the limited desktop preview, they have not passed.

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

The next software build is a local Mack service connecting the existing desktop to durable memory, a replaceable conversation adapter, and an explicitly simulated body. The next physical input is the clock's model, exterior/internal clearances, and masses. Those two tracks meet at a stationary fitted prototype before loaded walking tests.

See the [system architecture](architecture.md), [hardware integration plan](../hardware/integration-plan.md), and [release gates](roadmap.md).

## Intelligence deployment decision — 2026-10-21

Bill wants Mack as self-contained as possible, with a no-network mode using an onboard local model and optional cloud APIs/frontier reasoning when useful. Preserve memory, identity and body control locally. Ordinary interaction must not require a home inference server. Model updates must preserve remembered facts and must not grant new physical capabilities.

The target offline acceptance test is a cold boot with external networking unavailable, followed by local spoken interaction, saved-fact recall after restart and qualified body interruption/stop behavior. Assisted mode must visibly identify cloud use, send scoped context under the user’s selected policy and handle failure while preserving local operation. These are requirements for the finished system; Local AI 0.2 runs inference on the development Mac, and fully local speech recognition/onboard performance remain unqualified. See [model strategy](model-strategy.md).
