lane: RayCue/Research
written: 2026-10-21T12:20:00-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: 71c4d29 (parent of identity and read-only tools checkpoint)
status_updated: 2026-10-21T12:20:00-07:00
where: She/her identity and local reasoning tools verified; chosen SAL clip recorded; audio analysis open
next: machine
depends_on: onboard measurements for hardware; configured provider for optional cloud use
open_in: /Users/bill/Projects/RayCue Mac · existing RayCue/Research chat
judgment: Preserve local memory and independent control; benchmark models and qualify offline voice before onboard claims
model: Preserve the user's model choice and read the live dial
---
Read STATUS.md, docs/model-strategy.md and software/desktop/README.md, then docs/product-spec.md and docs/architecture.md.

BUILT

Mack now uses real local Ollama inference (Qwen3.6:35b on Bill’s 64 GiB M2 Max), explicit SQLite facts, editable Memories/Trash, bounded persistent history and installed-model selection with digest checks. The database is ignored at runtime/mack/memory.sqlite3. Never stage it. Browser notes import idempotently; originals remain untouched. Local speech output remains available. Browser dictation is opt-in and may process audio online; it was not exercised with a microphone.

Verified 30 Python tests, 8 legacy JavaScript tests and 93 vendor hashes. Live Qwen/UI recall, correction, model switch and exclusion of trashed facts passed. Exact memory/history/model state survived a real server restart. The window-growth clipping fix was checked at normal, 640×480 and 412×504 sizes. Two true starting memories record Bill’s name and his deployment preference. Disposable QA notes remain only in recoverable Trash.

LATEST VERIFIED CHECKPOINT

Mack uses she/her. Bill wants her identity, personality and memory to carry from the compact four-legged Mac into a possible humanoid body years from now. The four-leg prototype remains first. identity.json is separate from model weights and body capabilities. toolbox.py exposes only read-only status, local clock and active-memory search through native Ollama tools. Three model requests/four calls/120 seconds per reply, cancellation checks, strict argument validation and no arbitrary file/network/motor authority. Tool receipts show in the current browser conversation, not persisted history. Models without tool support retain text conversation.

41 Python + 12 JavaScript checks pass. Four live Qwen probes verified each tool and truthful she/her/body continuity. Browser status receipt verified with disposable memory; corrected its grid layout. Production database dump remained identical across restart. Evidence stays private under runtime/body-continuity-checks/. The only new public image is docs/images/mack-identity-tools.png from the isolated test UI.

USER DIRECTION

Mack is the complete Linux-based personal robot, not just its browser interface. Bill wants it as self-contained as possible, with offline local intelligence and optional cloud/frontier assistance. Do not re-ask this. No hosted account/key was configured. Model intelligence does not grant physical authority. Memory and local motion control remain independent of cloud availability and model upgrades.

NEXT

Bill selected SAL 9000’s complete voice and manner from 2010, as with Agent 99. The original Mack persona is implemented in software/mack/persona.md and loaded on each runtime startup, independent of model and memory. Local voice selection, pace/pitch, preview and stop controls work. Stock Samantha is a temporary study, not the exact film voice. Bill supplied https://www.youtube.com/watch?v=T2E7sxGAmuo. The Chandra/SAL page and 2:44 duration were verified; captions were unavailable. Audio has not been heard or analyzed through this session’s tools. Do not ask for the link again. Do not claim acoustic completion. Read docs/personality-and-voice.md. The Mac/Linux neural synthesis path remains to be installed and evaluated.

Verified 30 Python and 12 JavaScript tests, eight sampled live Qwen persona probes, browser Speaking/Stop behavior and preference persistence. QA used disposable memory; the production database dump stayed identical across restart/audition. The stock audio preview and QA evidence stay ignored under runtime/. Do not publish them or copy private Agent 99 files into the public repository.

Implement/qualify fully local speech recognition and the explicit offline/assisted mode policy. Evaluate models on fixed Mack tasks, response latency, correction/unknown-fact behavior and resource use. Build the mock-body contract so requests/results, cancellation, expiry and recovery are real, labeled simulation. Cloud assistance needs a scoped provider adapter and credentials, without wholesale memory upload. Model downloader/evaluation/rollback remains planned.

Continuum research, Terrarium (LLM Arcade Game) and Exocortex are proposed separate services. Only read-only inspection occurred. Preserve Continuum’s frozen experiments and semantic-expansion-off ruling. Preserve Terrarium’s recorded export-only observation boundary until its owner closes it. Do not ingest the whole Exocortex dossier or write into other projects. No live bridge exists.

NEXT PHYSICAL INPUT

Actual RayCue model/revision, dimensions, mass, clearances and retained component masses. Use hardware/measurements.csv and system-budget.csv. Four-leg CAD, actuators, electronics, battery, sensors and Linux compute must fit measured budgets. No motion/hardware test or purchase occurred.

LIVE SERVICE AND REPOSITORY

http://127.0.0.1:9844/ is intentionally left running for Bill, unified-exec session 3403. Resolve the current PID before stopping anything. Start Mack.command reopens it; no login automation exists. Keep the browser deliverable. Never stop the shared Ollama service as part of Mack cleanup.

Public origin (visibility and anonymous access verified on 2026-10-21): https://github.com/Bill-Viking/mack-model-04.git. Vendor imports stay unchanged and attributed. The loose root PNG stays untracked and untouched. No iCloud writes. This chat remains active; do not perform the close ritual until Bill ends the session.

PUBLIC DEVELOPMENT

Bill asked for a public GitHub link to share on X. The repository is now PUBLIC; unauthenticated API, repository page and raw README access all returned HTTP 200. README and docs/build-log.md now introduce the public build and distinguish the visual concept from working software and unbuilt hardware. Keep actual memory databases, credentials and recordings out of every commit. Existing Git history is retained. No X post is authorized or sent by this task.
