lane: RayCue/Research
written: 2026-10-21T10:56:33-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: 06ab142 (base before the Local AI 0.2 implementation; resolve the latest commit)
status_updated: 2026-10-21T10:56:33-07:00
where: Local AI 0.2 connected; memory persists; offline-first product direction selected
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

USER DIRECTION

Mack is the complete Linux-based personal robot, not just its browser interface. Bill wants it as self-contained as possible, with offline local intelligence and optional cloud/frontier assistance. Do not re-ask this. No hosted account/key was configured. Model intelligence does not grant physical authority. Memory and local motion control remain independent of cloud availability and model upgrades.

NEXT

Implement/qualify fully local speech recognition and the explicit offline/assisted mode policy. Evaluate models on fixed Mack tasks, response latency, correction/unknown-fact behavior and resource use. Build the mock-body contract so requests/results, cancellation, expiry and recovery are real, labeled simulation. Cloud assistance needs a scoped provider adapter and credentials, without wholesale memory upload. Model downloader/evaluation/rollback remains planned.

Continuum research, Terrarium (LLM Arcade Game) and Exocortex are proposed separate services. Only read-only inspection occurred. Preserve Continuum’s frozen experiments and semantic-expansion-off ruling. Preserve Terrarium’s recorded export-only observation boundary until its owner closes it. Do not ingest the whole Exocortex dossier or write into other projects. No live bridge exists.

NEXT PHYSICAL INPUT

Actual RayCue model/revision, dimensions, mass, clearances and retained component masses. Use hardware/measurements.csv and system-budget.csv. Four-leg CAD, actuators, electronics, battery, sensors and Linux compute must fit measured budgets. No motion/hardware test or purchase occurred.

LIVE SERVICE AND REPOSITORY

http://127.0.0.1:9844/ is intentionally left running for Bill, unified-exec session 94987. Resolve the current PID before stopping anything. Start Mack.command reopens it; no login automation exists. Keep the browser deliverable. Never stop the shared Ollama service as part of Mack cleanup.

Private origin: https://github.com/Bill-Viking/mack-model-04.git. Vendor imports stay unchanged and attributed. The loose root PNG stays untracked and untouched. No iCloud writes. This chat remains active; do not perform the close ritual until Bill ends the session.
