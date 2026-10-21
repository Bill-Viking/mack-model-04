# STATUS — M.A.C. Model 04 (Mack)

## Now

2026-10-21: Bill chose **SAL 9000's voice and complete manner from 2010**, with the depth of the Agent 99 personality work. Implemented an original Mack-specific persona in software/mack/persona.md, loaded into every model-generated turn independently of model weights and memory. Runtime truth and capability limits remain authoritative. Added local voice selection, pace/pitch settings, an original audition and immediate interruption. The current sound is explicitly a **stock-voice study**, initially local Samantha; no exact SAL voice model or film audio has been installed. Asked for an existing reference clip or voice model; that input remains pending. docs/personality-and-voice.md records behavior, acoustic goals and acceptance, plus Qwen3-TTS/MLX as an unevaluated synthesis candidate. Agent 99 files were consulted read-only; private source was not copied into this public repository.

Verification for the personality/voice change: 30 Python tests and 12 JavaScript tests pass. Reviewed eight real Qwen3.6:35b probes using a disposable database. The first pass was too wordy; the revised pass kept unknown memories unknown, declined nonexistent perception/movement, corrected calmly, resisted false agreement, and distinguished Mack from SAL and the stock voice from the film voice. Two follow-up probes confirmed correction and unknown-fact handling after removing a fictional workshop example that collided with the memory regression fixture. The model still sometimes adds an unnecessary follow-up question; conversational restraint needs further tuning. These are sampled observations, not a guarantee of every model response or acoustic likeness. In-browser playback entered Speaking, Stop voice returned immediately to Ready, and a pace edit survived reload. Local Samantha selection was verified. The production database dump stayed byte-identical across restart and audition. QA transcripts, backup and stock audio study are ignored under runtime/. No microphone was used.

2026-10-21: Bill explicitly asked to let the public follow Mack from start to finish and to share its GitHub link on X. **The GitHub repository is now public.** Added a public introduction and docs/build-log.md, with concept-versus-built status clearly labeled. Reviewed tracked files and 194 unique text objects across the existing Git history for common credential patterns and private runtime files; no matches were found. Normal Git author metadata remains part of the history. Runtime memory and credentials remain excluded. Verified anonymous access to the repository page, GitHub API and updated raw README, all HTTP 200.

2026-10-21: **Mack Local AI 0.2 runs at http://127.0.0.1:9844/**. The original desktop now connects to real local Ollama inference, initially Qwen3.6:35b on Bill’s M2 Max / 64 GiB Mac. No new model download or cloud credential was required. Explicit Remember commands and the Memories editor persist facts in SQLite. Edits, recoverable Trash, bounded recent conversation, legacy-browser import, installed-model selection and digest-change checks are implemented. Facts remain independent of model weights. Model output has no tool, file, camera or motor authority.

Bill selected the deployment direction: **as self-contained as possible, no-network operation with an onboard local model, and optional cloud/frontier APIs for harder tasks**. The finished robot should keep memory and body control locally. A home inference server is optional. docs/model-strategy.md records current model research, Meta Muse Spark 1.3’s hosted availability versus future open weights, downloadable candidates, staged upgrades, and proposed Continuum/Terrarium/Exocortex service boundaries. Those projects were inspected read-only; no service bridge is enabled. Continuum semantic expansion stays off; Terrarium’s recorded outward-export boundary is preserved.

Verification: **30 Python tests and 8 legacy JavaScript tests pass**, and all 93 imported-file hashes match. Live UI/Qwen checks passed for saved-fact recall, reload, correction, switching to Qwen2.5:3b without losing memory, restoring Qwen3.6:35b, and excluding a trashed fact from the next prompt. Exact database state (facts, Trash, history, selected model/digest) survived an actual service restart. A discovered window-growth clipping issue was repaired; title bars and controls were checked at the normal viewport, 640×480 and 412×504. No browser console errors were observed during these checks.

Voice output still uses an available local browser voice. Browser dictation is newly opt-in; its gate was verified, but no microphone capture/transcription was performed. Its browser vendor may process audio online. **Fully offline speech recognition, the enforced offline/assisted mode switch, cloud adapters, automated model downloads/rollback, mock body contract, sensors, motors and bootable Linux deployment remain open.** This Mac prototype does not establish onboard performance or a fully disconnected voice experience.

The private memory folder is runtime/mack/ and is Git-ignored. Two starting facts were saved from this conversation: Bill’s name and his self-contained/optional-cloud preference. A disposable QA fact and the old preview’s QA note remain in recoverable Trash; test exchange history was cleared before these two real facts were saved. Memory retrieval is a six-note lexical baseline; recent history keeps at most 40 completed exchanges and supplies at most four after the most recent memory edit. Backup instructions and limitations are in software/desktop/README.md. No personal database or credentials are committed.

Start Mack.command launches the loopback service. The session leaves it running for Bill’s trial (unified-exec session 43311; discover the current PID before any process action). No login item or automation was added. The browser tab remains a deliverable. Qwen’s first cold introduction took 10.77 s including 9.63 s model loading; broader latency/quality tests remain to be done.

The governing goal remains a complete original OS/AI/robotics product fitted into the accepted compact Mac form. Bill explicitly chose Mack’s own system on Linux on 2026-10-20. docs/product-spec.md defines P01–P10, docs/roadmap.md defines G0–G8, and hardware/integration-plan.md plus system-budget.csv hold the engineering intake. G2/G3 remain open for their unfinished mock-body and spoken-interaction requirements. Clock model/dimensions/mass are still the next physical input. No new kernel, foundation-model training, fitted hardware or validated leg mechanism is implied.

Name ratified by Bill on 2026-10-20: **M.A.C. Model 04** (Mobile Autonomous Computer), everyday name **Mack**. Use the formal name for project titles and the industrial designation; use Mack in conversation and the robot personality. RayCue identifies the donor clock. The existing working folder and RayCue/Research coordination lane remain in place.

On 2026-10-20 Bill asked to create a repository for Mack. Created **Bill-Viking/mack-model-04** on GitHub as a private repository and connected this local repository as its source. Canonical URL: https://github.com/Bill-Viking/mack-model-04. This request supersedes the earlier drive-only transport selection for this project. The committed introduction, concept images, documentation and pinned source library are the initial upload; ignored source checkouts and the loose duplicate PNG remain local.

Bill's target is an intelligent walking companion made from his RayCue Macintosh-shaped alarm clock. It should look and feel like a little Mac with a Mac OS 9-style shell over modern voice, memory and robotics. Real vintage application use is minor and optional. Bill accepted the compact four-leg visual concept on 2026-10-19; the image is a target, not an engineered mechanism.

On 2026-10-20 Bill reattached the exact image and said “this is what I want to build.” Saved that attachment unchanged as concepts/raycue-build-target.png and made it the README hero and visual baseline. Preserve the dominant beige Mac body, compact underside base, four short articulated legs, rounded dark feet, and classic desktop/dialog personality. The original generated image remains separately preserved. This confirms appearance; it does not supply measured dimensions or a validated leg mechanism.

On 2026-10-20, Bill asked to start the repo with an introduction, references and useful material from the other Git repos. The existing local Git repository now has a project introduction and concept image in README, architecture and milestone documents, hardware measurement and parts sheets, a software workspace guide, and a reference index. Earlier research is preserved in docs/research-notes.md. The hub's mechanical handoff capture is preserved in commit d3058f6; this current record replaces its transcript dump with plain project state.

Imported 93 unmodified files (2,360,495 bytes) into vendor/ from four pinned sources: WonderMac guides, Macintosh Mini bezel CAD/exports and KiCad board plus clock controls, AgentBridge's optional modern server/protocol, and Bill's Continuum robot code/tests. SOURCES.json records full revisions, source paths, file hashes, sizes and original modes. Each snapshot retains its notices and has a SOURCE.md. Public remote HEADs matched the existing three source checkouts when checked; no upstream update was required. Other project checkouts were read only and remain clean.

Validation: all 93 hashes match; seven source-tool tests pass, including modified/missing imports and refusal to overwrite dirty or mismatched checkouts; a fresh WonderMac restore and repeat invocation passed in a temporary folder. Owned documentation links and CSV structure checked. These are repository-tool checks, not tests of the imported runtime. No upstream installer, vendor test suite, emulator, AI service or motor code was executed.

The host desktop, local AI and durable-memory runtime are implemented; no body runtime, leg CAD or verified electrical design exists yet. The exact clock model, mass, internals, actuators, compute board and power design remain unknown. The initial printer recommendation remains an A1-class filament printer, PLA fit checks, PETG candidate structure and TPU feet; no printer or hardware purchase has been selected.

## To do

- [x] Find original clock conversion, expanded hardware, emulator and robotics references.
- [x] Show and save the walking Mac concept; record Bill's acceptance.
- [x] Adopt M.A.C. Model 04 / Mack and update the introduction and project documentation.
- [x] Create the private Bill-Viking/mack-model-04 GitHub repository and connect origin.
- [x] Build the project introduction, architecture, roadmap and reference index.
- [x] Import selected CAD, PCB, control, bridge and robot source with provenance and notices.
- [x] Add and verify source-integrity and pinned-checkout restore tools.
- [x] Record the complete product scope and Bill's selection of Mack's own system on Linux; define acceptance gates and hardware integration work.
- [ ] Identify and measure the actual clock; populate hardware/measurements.csv.
- [x] Build and verify the host desktop, screen-state previews, saved notes, and a typed response with local speech output.
- [x] Connect the desktop to a local runtime, durable editable memory and live Ollama inference; verify persistence, model changes, correction, failure and cancellation paths.
- [x] Research current models and record the self-contained/offline plus optional-cloud direction and proposed project-service boundaries.
- [ ] Implement the simulated body contract and prove expiry, rejection, interruption and recovery.
- [x] Implement the SAL-inspired conversation profile and local voice audition controls; verify sampled behavior and preference persistence.
- [ ] Match the requested SAL sound using the chosen reference/model; audition new sentences and qualify local synthesis. Stock Samantha is only a study.
- [ ] Verify spoken input; qualify fully local speech recognition and the offline/assisted routing policy.
- [ ] Evaluate model quality, cold/warm latency and resources; implement a scoped cloud adapter and staged model upgrade/rollback flow.
- [ ] Evaluate imported Continuum mock tests and select reusable memory/control pieces.
- [ ] Develop packaging and mass/power budgets before choosing fitted hardware.
- [ ] Design and test one restrained leg with representative load.
- [ ] Build the four-leg base with dummy mass, then integrate the stationary Mac.
- [ ] Integrate sensing and independent body control; qualify the complete battery-powered robot against P01–P09.
- [ ] Produce repeatable installation, assembly/calibration, update recovery, and service evidence for P10.
- [ ] Optional after core experience: prove OS 9.0.4 and selected legacy apps.

## Important

- Origin is https://github.com/Bill-Viking/mack-model-04.git; Bill authorized public visibility on 2026-10-21 so development can be followed from start to finish. The hub confirmed its carrier registry now uses GitHub in mail pm-356c0eafa137 on 2026-10-20. Its prior RAY-TX-001 snapshot is historical and predates the foundation. No new transfer payload is claimed here.
- Where things live: software/desktop/ is the UI; software/mack/runtime.py is the local AI/memory service; tools/serve_desktop.py and Start Mack.command launch it. runtime/mack/memory.sqlite3 stores personal facts and history outside Git. Browser preferences use mack.desktop.preferences.v2; legacy mack.desktop.v1 notes are imported without overwriting originals. docs/images/mack-local-ai.jpg is the new UI screenshot; the older preview image remains historical.
- Full reference clones in sources/ remain ignored separate repositories. The tracked vendor/ subsets travel with the parent. Never push to vendor upstreams.
- Original M.A.C. Model 04 work has no public license selected. Imports retain their individual licenses. Continuum is Bill-owned local source with no upstream LICENSE at the snapshot; no public redistribution license is asserted. The differently licensed AgentBridge classic client implementation is omitted.
- Apple ROMs, OS images, chimes and emulator binaries are not in the tracked imports. Keep media, credentials, recordings and memory databases in ignored local storage.
- The existing loose file ChatGPT Image Oct 19, 2026, 11_03_05 AM.png is untracked and untouched; it is byte-identical to the committed concepts/raycue-walking-mac-v1.png.
- Imported GPIO button code can shut down Linux or launch emulator/setup commands. Do not run it on this Mac. Imported Freenove geometry/limits are not four-leg Mack settings.
- SheepShaver supports through 9.0.4; Basilisk II through 8.1. AgentBridge PowerPC is marked builds, untested. Source discrepancies and wiring/power concerns are documented in docs/references.md.
- Motor limits, timeout behavior and stopping must work independently of desktop and AI. The safe response must be validated for the actual body.
- No writes to iCloud. Public repository publication was completed and verified on 2026-10-21. No purchase, hardware modification or live robot operation occurred.
