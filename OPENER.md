lane: RayCue/Research
written: 2026-10-22T08:15:55-07:00
by: ACT — RayCue/Research: Mack joint design
on: MAC
head: d30cc25 (catalog-scale checkpoint follows)
status_updated: 2026-10-22T08:15:55-07:00
where: Joints before docking; catalog scale and proposed 30 + 30 mm links recorded; actual component fit outstanding
next: machine compares actual actuator packaging for direct and proximal knee drive
depends_on: actual shell geometry, mass/center of mass and selected actuator/bearings
open_in: /Users/bill/Projects/RayCue Mac · existing RayCue/Research chat · ACT — RayCue/Research: Mack joint design
judgment: Preserve approved voice/local memory; geometric checks do not establish mechanical performance
model: Preserve the user's model choice and read the live dial
---
Read the project status/memory first. Bill has resumed and put joints and mechanical design BEFORE docking controls. Start with hardware/joints/leg-layout.md (J04-L01-D02) and catalog-scale.json. Develop one complete three-axis leg and cradle interface; the old C01 solids model only one example hip pivot. Direct knee drive is a proposed first-prototype baseline, with proximal drive retained for a measured packaging/mass comparison. Neither arrangement nor a motor is newly approved by Bill. Bill supplied a WB-8 catalog screenshot. The manufacturer confirms 80 × 91 × 112 mm and 229 g. The W/D/H mapping follows the screenshot; actual unit geometry, interior and retained mass remain unmeasured. A scaled sketch proposes 30 + 30 mm links; its 172.6 mm overall standing height is a calculated illustration, not a fitted design. XL330 is a size/mass benchmark only, not selected. Place actual component output datums and supporting hardware next. Keep the original appearance, accepted voice and private memory intact. Mack and the old preview servers remain stopped. The following dated shutdown context remains valid for restart and preservation, but it no longer sets the work priority.

## Dock appearance image

Bill requested a realistic concept of Mack resting in her dock with the original little Mac design preserved. concepts/mack-charging-dock-v1.png is the inspected 1536×1024 built-in image_gen result, made with concepts/raycue-build-target.png as the reference. Exact prompt/provenance is in concepts/mack-charging-dock-v1-prompt.txt. D04 and hardware README link it. The low foot tray is an appearance variant, not a ratified replacement for D04's clear-floor saddle; marker and contact/clearance details remain unengineered. Do not overwrite the original accepted target or claim this is a physical photograph or tested dock. Live application/voice/memory and static previews were untouched.

## Battery direction

Bill explicitly confirmed lithium-ion as primary and requested autonomous docking. D04 (hardware/charging-dock.md) proposes a supported central saddle, guided/recessed contacts and marker-led final approach after local navigation to staging. P13 and G7 now require offline return/recharge evidence; T04 adds dock and fault practice. No physical capability, circuit or executable docking service added. The stationary dock is excluded from carried robot mass; new onboard-interface row excludes shared charger/gauge mass.

Return reserve is route + approach + bounded retries + safe stop + uncertainty in Wh, with conservative measured inputs and no guessed percentage. Source defaults off; independent seating/connection checks precede charging; report net battery charging separately from contact/full/inhibited states. Qualify sudden contact loss, reverse blocking, depleted-pack wake/service, blocked/moved/unpowered dock, stale sensors, stop and reboot. Stop/help when conditions or energy are insufficient; no indefinite search or resumed movement after reboot. A future hydrogen hybrid is plausible research, not a selected system or demonstrated fit/endurance benefit.

Dock preview: http://127.0.0.1:9848/charging-dock-concept.svg on the existing hardware-only server, PID81029 when checked. IAB17 marked deliverable. Browser layout inspected and label overlaps repaired; private screenshots runtime/cad/d04-dock.png and d04-dock-lower.png (1265×712). SVG XML, CSV blank parameters, 121 local links/anchors and whitespace checks pass. First physical step remains measured geometry, then an adjustable unpowered fixture; a software-only state mock can progress separately. AprilTag/Nav2 are references only. Preserve production Mack and the existing CAD/face/recovery previews.

Bill confirmed that powercell means hydrogen fuel cell; he otherwise requested high-efficiency lithium-ion. hardware/battery-power.md compares hydrogen and recommends protected serviceable lithium-ion mounted low. Pack voltage/capacity/topology and supplier are unselected. Molicel cell comparisons are benchmarks, not a four-cell commitment or measured fit. Four P50B cells: 72 Wh typical and 284 g summed maximum cell mass before pack hardware; with an assumed 80% usable-energy allowance and assumed 30 W battery-side load, 1.92 h. Actual consumption/runtime unknown. Historical H-12 fuel-cell example illustrates supporting-system overhead, not current market leadership.

B04 functional architecture separates regulated compute and controlled actuator loads, requires local supervision, qualification of peaks/sag, orderly low-energy rest/shutdown and braking-energy handling when the battery cannot accept energy. Tie battery retention and added inertia into R04. Solar stays optional; whole-system low-power parking must be measured. Battery-bay intake fields are empty. No power hardware selected, ordered, built or tested. Arithmetic, CSV structure/unknowns and 89 local links/anchors passed. No software/voice/memory changes. Next: measured bay/body mass and loaded-joint demand, then choose and bench-qualify the power system.

## Future virtual practice room

Bill proposed a simple virtual physical environment for learning walking, maneuvering, obstacles and steps. docs/motion-training.md (T04-D01) records the future curriculum and proposed MuJoCo/Python starting point, with Playground as a later accelerated-learning candidate. No simulator installed or training launched by this plan. Check actual accelerator/backend support before promising training throughput on either machine.

First implementation milestone: labeled approximate whole-body model, floor, block, ramp and one adjustable step, with reset/replay and bounded baseline controls. Current J04-C01 is only a synthetic joint draft, not that body. Calibrate masses/inertia, motor limits/delays, contacts and sensors from fixtures. Use unseen evaluation layouts and the R04 directional recovery matrix; physical tests still close G5/G6. No household-stair claim. The physics training world is distinct from the service-contract mock. Keep movement policies below the AI's named-skill boundary and within independent stopping/limit enforcement; do not put simulation episodes into personal conversation memory. Reuse room generators for a future humanoid, not quadruped weights without new validation.

## Optional solar direction

Bill would add a roof panel if its useful energy justifies it. hardware/solar-feasibility.md (S04-D01) recommends testing supplemental direct-sun charging plus low-power parking; a bigger external solar dock is an alternative. No solar requirement to install regardless of benefit, no selected panel/charger/battery and no measured roof fit. Optional intake/parts/budget entries stay blank.

Voltaic P124 is a size/output benchmark: 113×66×2.6 mm, 31.6 g, expected 1.14 W per August 2026 datasheet. Explicitly assumed 4 equivalent full-sun hours and 80% additional delivered-energy factor yield 3.648 Wh before parked draw, or 14.6 minutes at a hypothetical 15 W battery-side load. This is not measured Mack runtime or a local weather forecast. Indoor-specialist Epishine data gives about 2.03 mW per 100 cm² active area at its specified 500-lux LED conditions. A solar roof does not establish continuous AI/walking power. Measure net battery Wh, actual load modes and temperatures. Keep cells inside R04 guards; roof contacts go through the frame and cannot load the panel. No new server or live software change.

## Current recovery direction

Bill explicitly added front-to-back and back-to-front rolling. hardware/joints/recovery-envelope.md (R04-D01) now distinguishes pitch about body Y, side roll about X, mixed edge/corner starts, accidental tumbling and commanded rolling. Each direction needs separate evidence. Design frame-connected front/roof/rear/side/corner contacts so the curved face and camera window stay clear through the entire loaded path. A complete geometric orientation sweep is not a qualified 360-degree rolling skill.

The original X-axis rear arm was only a side-roll candidate; fore/aft recovery is unsolved. Extra mechanism count/axes are TBD, superseding the fixed conditional 13th-axis assumption. Compare leg-only reach, the original arm, Y-axis paddle(s) and a two-axis arm before choosing. R04 has seven unverified case families and the required evidence. No whole-body CAD/dynamics/impact/controller result exists. The J04-C01 draft is unchanged.

Preview: http://127.0.0.1:9848/joints/recovery-envelope.svg, same hardware-only server exec29126. Original SVG visually inspected; private proof runtime/cad/r04-recovery.png, 1159×1029. XML/references, CSV columns and local document links checked. These preview servers are stopped at close; the files remain available.

## Current face and camera direction

Bill wants a convex original-Mac screen appearance and concealed camera hardware, ideally behind the screen. P12 and hardware/display-and-vision.md record the goal. The proposed first fixture is a flat colour display under a curved clear front with a camera behind a transmissive dark border. This is behind the shared cover, not through LCD pixels. Final optical route remains open. Compare a folded beamsplitter for camera alignment behind the apparent image; true under-display OLED needs a specialised compatible panel/driver/camera and correction pipeline. No suitable small turnkey combination was established in this search.

Primary references and catalogued candidates are in the study; no purchase, supplier contact, optical test or camera installation. The transparent 1.51-inch OLED is only an experiment lead, unsuitable for the full colour desktop. Measure face aperture, surround space and depth, then test cover/tint/baffles against bare-camera images with display off/black/white/patterns and changing light/motion. Independent floor/body sensing remains required.

Schematic: hardware/face-optics-concept.svg. Browser preview http://127.0.0.1:9848/face-optics-concept.svg, exec29126, serves only hardware/. Private proof runtime/cad/f04-optics.png. The preview server is stopped at close. No live software, voice or memory change.

## Current mechanical work

Bill wants fully designed dexterous joints and self-righting for Mack. He has personal Creo and Ansys installations on the home Dell, versions/modules unknown, and welcomes other tools for direct help. The Mac now has build123d 0.12.0 in runtime/cad/venv with Python 3.12. Do not alter the speech .venv for CAD.

hardware/joints/cad/ contains original editable J04-C01-D01 source, example JSON, STEP assembly/parts, an offline WebGL preview and geometry evidence. Six solids represent a yoke, shaft, moving hub/link, two bearing envelopes and motor block. Dimensions are entirely synthetic. Nominal envelope 40×108×100 mm; this is not a selected cartridge size. Missing coupling, shaft/bearing retention, fitted motor mount, encoder, cable path, stops, tolerances/materials and real body interfaces are documented in the CAD guide.

Geometry checks passed: six valid solids, no unintended neutral overlap, 33 sampled link positions ±80°, minimum 10 mm clearance excluding intentional shaft contact, STEP re-import, individual STEP solids, invalid-gap/collision rejection and a resized variant. Browser motion/parts separation/view/reset/zoom checked, console clean. Not continuous clearance, strength, thermal, fatigue, walking or recovery proof.

hardware/engineering-workflow.md defines actual loads, CAD ownership, Creo/Ansys import/analysis and staged Protolabs manufacture. hardware/dell-cad-handoff.md is a complete future Dell brief. No Dell session/connection started; no native import or FEA done. Next: clock measurements/masses/CoM, actual component envelopes, complete one-joint design and restrained fixture. No upload/quote/order made. Do not order a full set from the example solids.

J04 architecture remains a proposal: three driven axes per leg (12), supported cartridges, compliant feet, protected cradle and additional recovery mechanism axes TBD under R04. The tall body's inverted reach and fore/aft contacts must be proven. Proposed ranges and test targets are not ratified component limits. No physical robot or controller is connected. Preserve original vendor files; all 93 hashes passed at the CAD checkpoint.

## Stopped services and restart

At close, no listeners on 9844–9848 and no matching project application/speech/preview worker were found. They had already exited, so no kill was required. Old exec IDs and PIDs elsewhere in this record are historical and must not be reused. Browser pages may be cached.

For the resuming home session: inspect ports/processes first. Start Mack.command is the existing launcher for tools/serve_desktop.py at http://127.0.0.1:9844/. Do not reinstall models or reset memory/voice. Start a loopback-only static server on 9847 from hardware/joints/cad/exports for preview.html, and on 9848 from hardware/ for face-optics-concept.svg, joints/recovery-envelope.svg and charging-dock-concept.svg, only when needed. Never serve the whole project root. Shared Ollama belongs to the machine, not this chat. Private CAD screenshot: runtime/cad/j04-c01-separated.png.

## Accepted interaction and voice

Bill confirmed his real words appear in Live transcript. Studio Display Microphone is the explicit persisted input; earlier built-in-microphone failures and blanket Chrome-only advice are superseded.

Two independent input panels are implemented: Type a message / Send text, and Speak to Mack / Live transcript. Finish speaking & reply sends the voice draft; Turn microphone off reviews it, then Reply to voice message sends. Cancel restores only the earlier voice draft. Unsent typed text survives voice use. The final layout passed 27 JS checks and isolated browser QA; production SQL was unchanged through deployment. Bill's last unsent typed draft was “hello”; do not reset it while doing CAD work.

Approved voice v1 is locked. Qwen3-TTS 1.7B Base with pinned MLX Audio 0.6.1 reproduces Bill's accepted light-echo greeting on this Mac. software/mack/voice-profile.json is the public recipe/fingerprint record. Private reference and approved recording remain outside Git. Do not retune or ask for acceptance again. Approved audition SHA256: 6192f95cd23edf174d3451619cfc6f1647e5e6ec0e3a1f85f8f84c0b5164a1fb.

Local Qwen3-ASR-0.6B-8bit handles bounded capture and live provisional transcription; completed exchanges are archived in runtime/mack/memory.sqlite3. Source provenance distinguishes typed/microphone/edited transcripts. Keep existing personal data and old conversations intact. Curated memories and Conversations support recoverable Trash. No audio reference, recording, weights, SQLite database or credentials belong in Git.

Conversation uses installed Qwen3.6:35b. Process-scoped internet-denied ASR, recall and speech tests passed; disconnected reboot, wider quality/latency and Linux/onboard qualification remain open. Everyday use and the mock-body contract remain software work. New model research is in docs/model-strategy.md; no newly researched weights were downloaded or selected.

## Product and public record

Mack is her own Linux-based personal system with a classic Mac interface, durable local memory and optional future cloud assistance. First body: little four-leg Mac. Long-term: preserve the personalized intelligence and history into a humanoid body, years away. Each body needs its own tested controller. Continuum, Terrarium and Exocortex are proposed separate services.

Public repository: https://github.com/Bill-Viking/mack-model-04. Bill controls edits; only Bill-Viking was listed as collaborator/admin, no pending invitations, when checked. No account-wide permissions/visibility change was made. Preserve all separate no-remote project rules.

Resonance already published the approved personalized-intelligence vision posts and the approved greeting video once on Facebook and X. Facebook retained Friends; X Public. Exact permalinks/proofs are in the private application receipts mack-vision-publications-20261021.context.json and mack-voice-publications-20261021.context.json. Do not duplicate those posts.

Keep the loose root PNG untracked. No iCloud writes. Bill explicitly ended this sitting; retitle ARCH and release only this chat’s claim/stamp after saving. Do not hide the chat.


## WHERE WE ARE — for the next home session

Goal: build Mack as a personal intelligence in the original little Mac body, with lithium-ion power, dexterous legs and autonomous charging.

1. ✅ Local conversation, approved voice, listening and memory are implemented on the development Mac.
2. ✅ Original joint CAD study and optical, recovery, power, training and dock plans are saved.
3. ✅ The realistic dock image and its prompt are saved; Bill said he loves it.
4. ✅ Project services are stopped; private memory passed its integrity check.

Right now: no physical body or dock has been built. The GitHub record carries the public design work; private runtime stays on the home Mac. This is not a work-machine transfer package.

Bill supplied catalog dimensions and mass. Later physical intake: confirm model/axis order, inspect usable underside mounting space and weigh retained components. Continue design from the catalog scale without asking for the same catalog facts again.
Machine’s next move: develop the complete joint/leg packaging and its mechanical interfaces. Docking controls wait. Restart Mack only when requested or needed; preserve voice and memory.

Close receipt: clock and process checks completed; Mack data verified; STATUS and this opener saved for commit/push. The final home-brain push follows this chat’s stamp/claim release.
