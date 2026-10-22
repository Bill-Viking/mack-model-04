lane: RayCue/Research
written: 2026-10-21T17:00:23-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: e61d7d8 (J04 concept; CAD/workflow checkpoint follows)
status_updated: 2026-10-21T17:00:23-07:00
where: Original J04-C01 draft CAD and preview ready; measured fit and Dell imports next
next: measured hardware intake and Dell tool inspection
depends_on: actual shell geometry, mass/center of mass and selected actuator/bearings
open_in: /Users/bill/Projects/RayCue Mac · existing RayCue/Research chat
judgment: Preserve approved voice/local memory; geometric checks do not establish mechanical performance
model: Preserve the user's model choice and read the live dial
---
Read STATUS.md first. This is the current handoff; dated history remains in STATUS.md and docs/build-log.md. This chat stays active until Bill ends it.

## Current mechanical work

Bill wants fully designed dexterous joints and self-righting for Mack. He has personal Creo and Ansys installations on the home Dell, versions/modules unknown, and welcomes other tools for direct help. The Mac now has build123d 0.12.0 in runtime/cad/venv with Python 3.12. Do not alter the speech .venv for CAD.

hardware/joints/cad/ contains original editable J04-C01-D01 source, example JSON, STEP assembly/parts, an offline WebGL preview and geometry evidence. Six solids represent a yoke, shaft, moving hub/link, two bearing envelopes and motor block. Dimensions are entirely synthetic. Nominal envelope 40×108×100 mm; this is not a selected cartridge size. Missing coupling, shaft/bearing retention, fitted motor mount, encoder, cable path, stops, tolerances/materials and real body interfaces are documented in the CAD guide.

Geometry checks passed: six valid solids, no unintended neutral overlap, 33 sampled link positions ±80°, minimum 10 mm clearance excluding intentional shaft contact, STEP re-import, individual STEP solids, invalid-gap/collision rejection and a resized variant. Browser motion/parts separation/view/reset/zoom checked, console clean. Not continuous clearance, strength, thermal, fatigue, walking or recovery proof.

hardware/engineering-workflow.md defines actual loads, CAD ownership, Creo/Ansys import/analysis and staged Protolabs manufacture. hardware/dell-cad-handoff.md is a complete future Dell brief. No Dell session/connection started; no native import or FEA done. Next: clock measurements/masses/CoM, actual component envelopes, complete one-joint design and restrained fixture. No upload/quote/order made. Do not order a full set from the example solids.

J04 architecture remains a proposal: three driven axes per leg (12), supported cartridges, compliant feet, protected cradle and conditional 13th recovery-arm axis. The tall body's inverted reach must be proven. Proposed ranges and test targets are not ratified component limits. No physical robot or controller is connected. Preserve original vendor files; all 93 hashes pass.

## Live pages

Mack: http://127.0.0.1:9844/ — exec74151, PID44486 when last checked.
CAD preview: http://127.0.0.1:9847/preview.html — exec42944, PID68775 when last checked; serves only hardware/joints/cad/exports. Keep it available for Bill. Offline preview.html is self-contained.

Always resolve current PIDs before process actions. Never stop shared Ollama. Previous QA servers and the old drawing preview9846 are stopped. Private CAD screenshot: runtime/cad/j04-c01-separated.png.

## Accepted interaction and voice

Bill confirmed his real words appear in Live transcript. Studio Display Microphone is the explicit persisted input; earlier built-in-microphone failures and blanket Chrome-only advice are superseded.

Two independent input panels are live: Type a message / Send text, and Speak to Mack / Live transcript. Finish speaking & reply sends the voice draft; Turn microphone off reviews it, then Reply to voice message sends. Cancel restores only the earlier voice draft. Unsent typed text survives voice use. The final layout passed 27 JS checks and isolated browser QA; production SQL was unchanged through deployment. Bill's last unsent typed draft was “hello”; do not reset it while doing CAD work.

Approved voice v1 is locked. Qwen3-TTS 1.7B Base with pinned MLX Audio 0.6.1 reproduces Bill's accepted light-echo greeting on this Mac. software/mack/voice-profile.json is the public recipe/fingerprint record. Private reference and approved recording remain outside Git. Do not retune or ask for acceptance again. Approved audition SHA256: 6192f95cd23edf174d3451619cfc6f1647e5e6ec0e3a1f85f8f84c0b5164a1fb.

Local Qwen3-ASR-0.6B-8bit handles bounded capture and live provisional transcription; completed exchanges are archived in runtime/mack/memory.sqlite3. Source provenance distinguishes typed/microphone/edited transcripts. Keep existing personal data and old conversations intact. Curated memories and Conversations support recoverable Trash. No audio reference, recording, weights, SQLite database or credentials belong in Git.

Conversation uses installed Qwen3.6:35b. Process-scoped internet-denied ASR, recall and speech tests passed; disconnected reboot, wider quality/latency and Linux/onboard qualification remain open. Everyday use and the mock-body contract remain software work. New model research is in docs/model-strategy.md; no newly researched weights were downloaded or selected.

## Product and public record

Mack is her own Linux-based personal system with a classic Mac interface, durable local memory and optional future cloud assistance. First body: little four-leg Mac. Long-term: preserve the personalized intelligence and history into a humanoid body, years away. Each body needs its own tested controller. Continuum, Terrarium and Exocortex are proposed separate services.

Public repository: https://github.com/Bill-Viking/mack-model-04. Bill controls edits; only Bill-Viking was listed as collaborator/admin, no pending invitations, when checked. No account-wide permissions/visibility change was made. Preserve all separate no-remote project rules.

Resonance already published the approved personalized-intelligence vision posts and the approved greeting video once on Facebook and X. Facebook retained Friends; X Public. Exact permalinks/proofs are in the private application receipts mack-vision-publications-20261021.context.json and mack-voice-publications-20261021.context.json. Do not duplicate those posts.

Keep the loose root PNG untracked. No iCloud writes. Update STATUS/this opener with the next verified result; do not archive or stamp off just because one turn ends.
