# CONTINUUM ROADMAP — Future bodies & design implications
Companion to CONTINUUM_HEXAPOD_BUILD.md (the source of truth for current work). This doc exists so code sessions understand where the project is GOING and make architectural choices that don't foreclose it. Nothing here is current work.

## Core thesis
Continuum (the user-owned SQLite memory store + Scribe) is the persistent self. The Brain (Claude API) is a stateless faculty invoked per-tick. Bodies are peripherals. Identity and learning live in the database — so a body upgrade is a reincarnation, not a replacement: the next body wakes up already knowing the apartment from the previous body's episodes.

## Platform ladder

### Tier 1 — Freenove Big Hexapod (CURRENT, purchased)
- 18 hobby servos (no feedback), camera, ultrasonic, Pi onboard
- Role: prove the nervous system (Brain/Spine/Hand/Scribe), spatial memory, episodic learning, consolidation
- Known ceilings: commanded-position-only proprioception; no manipulation; ~20–40 min sessions
- Exit criterion: final test-ladder item passes — power-cycle the robot and verify behavior changed because of Continuum contents

### Tier 2 — LeKiwi + SO-ARM101 (~$350–550) — the planned next body
- Open-source mobile manipulator (SIGRobotics UIUC / LeRobot ecosystem; kits from Seeed/WowRobo; Pi 5 compatible)
- Omnidirectional 3-wheel base + 6-axis arm; wrist/eye-in-gripper camera (Bill's claw-cam concept, realized)
- **Feetech STS3215 serial-bus servos: actual position, load, and temperature readback.** This is the qualitative jump — expected-vs-actual becomes a per-joint measurement; gripper load = crude touch. Skill log entries gain measured outcomes ("grasp succeeded at 40% load")
- Inherits LeRobot's teleoperation, dataset, and policy-training ecosystem → Continuum episode logs become training data if learned motor policies are ever wanted
- Port cost: new hand adapter + limit table only (if current code stays body-agnostic)
- Purchase trigger: Tier 1 exit criterion met. Not before.

### Tier 3 — Unitree Go2 EDU ($3,800–13,000+, quote-only; prices falling in 2026 quadruped price war)
- Only the EDU tier has the full SDK, low-level joint control, and foot-force sensors; consumer Air ($1,600) / Pro ($2,800) tiers lack SDK access and are NOT suitable for Continuum
- EDU adds 4D lidar + depth cameras → spatial memory graduates from landmark graph to metric SLAM maps; optional 6-DOF arm
- Decision horizon: 12+ months, only if this becomes a serious research program. Waiting is cheap — prices are dropping.

## Design implications for CURRENT code (the reason this doc exists)
1. **Body-agnostic hand interface.** The Spine's action primitives (walk/turn/look/posture/stop) are the contract; hand adapters implement them per body. Don't leak hexapod specifics (leg count, gait names, servo indices) above the adapter.
2. **Capabilities registry.** Continuum should store a per-body capability record (body_id, sensors, actuators, feedback available y/n) so memories can be interpreted across incarnations ("this grasp skill was learned on a body with load feedback").
3. **Memories belong to the self, not the body.** Places/objects/episodes tables carry body_id as metadata, not as schema structure. A LeKiwi must be able to recall hexapod episodes.
4. **Limit tables are per-body config files**, versioned in the repo (limits.hexapod.yaml, later limits.lekiwi.yaml).
5. **Feedback-optional design.** Anywhere the code consumes joint state, treat actual-position/load as optional fields that are null on Tier 1 and populated on Tier 2+ — so the Tier 2 upgrade lights up richer learning without schema migration.
6. **Eye-in-hand ready.** Frame-capture abstraction should support multiple named cameras (head, wrist) even though Tier 1 has one.

## Non-goals (explicitly out of scope for now)
- Learned motor policies / RL (LeRobot territory, Tier 2+, and only after retrieval-based learning is exhausted)
- Outdoor operation, multi-robot, voice/personality layer (a possible future Brain-layer skin — Doink's saner sibling — but not until the mind works)
