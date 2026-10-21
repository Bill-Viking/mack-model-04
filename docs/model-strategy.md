# Mack’s intelligence and model strategy

Research checked 2026-10-21. This is a role-based shortlist, not a claim that one model is universally the smartest. Publisher evaluations suggest candidates; Mack-specific trials decide deployment. Only the local Ollama adapter described below is connected today.

## Decision for this build

Keep Mack’s identity, remembered facts, permissions and body controller outside the model. Use a replaceable inference adapter. Begin with **Qwen3.6:35b already downloaded on Bill’s Mac**, so the first useful conversation needs neither a purchase nor a cloud account. The host is an M2 Max with 64 GiB of unified memory. Its capacity is not an onboard hardware specification.

The first live Ollama introduction took 10.77 seconds, including 9.63 seconds loading the model, and generated 20 tokens. That is one cold-start smoke test, not a sustained latency benchmark. Runtime replies are bounded to 400 generated tokens with an 8,192-token context setting; thinking is disabled for this conversational trial when supported. Reasoning, voice latency, memory accuracy and thermal behavior still need a representative evaluation.

Selected local artifact: `qwen3.6:35b`, digest `07d35212591fc27746f0a317c975a6d68754fb38e9053d82e25f06057af28522`, approximately 23.94 GB on disk, Q4_K_M. Ollama reported vision, completion, tools and thinking capabilities. This build uses text completion only. No new weights were downloaded. [Ollama’s Qwen3.6 library](https://ollama.com/library/qwen3.6).

## Models to evaluate

| Candidate | Access and useful role | Boundary / next evidence |
| --- | --- | --- |
| Meta Muse Spark 1.3 | Released September 2, 2026 through Meta Model API and Muse Code; a candidate for difficult planning and long tasks. | The announcement describes open weights as future work. API access is verified as offered; a downloadable 1.3 artifact has not been verified. No account or Mack adapter configured. [Meta release](https://research.meta.ai/blog/introducing-muse-spark-1-3). |
| Qwen3.6:35b | Installed local conversation baseline; no provider account needed. | Benchmark grounded memory, instruction following and warm response latency before treating it as the final choice. The Mac may serve a smaller onboard system later. [Runtime library](https://ollama.com/library/qwen3.6). |
| Google Gemma 4 | Downloadable Apache 2.0 models. E2B/E4B are candidates for compact compute; larger variants can be compared on a host. | Effective parameters are not total storage: E2B is 5.1B total and E4B is 8B total including embeddings. These variants accept audio/image input and produce text; this does not establish a speech-output pipeline. No variant installed here. [Google model card](https://ai.google.dev/gemma/docs/core/model_card_4). |
| OpenAI gpt-oss-20b | Downloadable Apache 2.0 reasoning candidate: 21B total / 3.6B active parameters; text input/output and structured/tool output. | Compare against Qwen on actual tasks. No installation or onboard memory/performance claim. [Official model page](https://developers.openai.com/api/docs/models/gpt-oss-20b). |
| OpenAI GPT-6 Astra / GPT-6.1 Sol | Hosted candidates for difficult reasoning and general work respectively. | Optional adapter, account access, per-request data scope and budget required. No credentials configured in Mack. [Current catalog](https://developers.openai.com/api/docs/models). |
| Anthropic Fable 5.1 / Opus 5.5 / Sonnet 5.5 | Hosted candidates spanning demanding reasoning, broad work and faster response. | Compare the least expensive capable option for routine work; reserve expensive deliberation for tasks that benefit. [Official overview](https://platform.claude.com/docs/en/models/overview). |
| Google Gemini 4 Argon / Gemini 3.8 Flash | Hosted reasoning and faster-response candidates. | Compare actual memory accuracy and latency before selection. No credentials or integration configured. [Official catalog](https://ai.google.dev/gemini-api/docs/models). |

Availability, model identifiers, pricing and terms must be checked again when an adapter is implemented. A downloadable language model alone does not establish a robot’s physical competence. Greater autonomy requires validated tools, feedback and control, alongside better reasoning.

## Meta’s robotics-related work

**SAM 3.1** is relevant to perception: detecting, segmenting and tracking objects in images/video from prompts. The official repository records the March 27, 2026 update. Its documented setup requires a CUDA GPU stack and checkpoint access; it is not an installed macOS component. Evaluate recorded, consented scenes on suitable hardware before choosing an onboard substitute. [Official SAM repository](https://github.com/facebookresearch/sam3).

**V-JEPA 2** is relevant to learned physical prediction and planning research. Released in June 2025, it is older than the recent Muse release. Demonstrated robot-arm manipulation does not validate the gait, balance or safety of Mack’s four-leg body. Consider it as a separate experimental service after the mechanical and simulation foundations exist. [Official V-JEPA 2 repository](https://github.com/facebookresearch/vjepa2), [Meta research explanation](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/).

## Three possible deployment arrangements

1. **Onboard:** fast local interaction, memory, sensor processing and bounded behavior; the independent controller always owns time-critical movement and stopping.
2. **Home-assisted:** Mack asks the Mac or Dell for heavier inference through a deliberately configured authenticated service. Memory selections travel only within the approved home boundary. The current loopback server is not exposed on the LAN.
3. **Optional cloud assistance:** a hosted model receives only the context needed for an approved task. Memory stays locally owned. Provider retention settings, costs and failure behavior are part of implementation, not assumptions.

Bill selected the direction on 2026-10-21: as self-contained as possible, a no-network mode that uses a local model, and optional cloud APIs/frontier models when useful. The recommendation is **onboard operation by default, optional cloud assistance**. A home inference server can be an additional accelerator; it must not become a requirement for ordinary operation.

Define the future modes explicitly:

- **Offline:** no non-loopback requests from Mack’s services, no remote fallback, local speech recognition and synthesis, downloaded local inference, persistent memory, and locally enforced body behavior. A network-disconnect boot/conversation/recall/stop test must pass before the device earns this claim.
- **Assisted:** local remains available; an approved task can use a configured cloud provider with scoped context, visible routing, budget limits and an understandable failure path. Failed cloud inference may offer a local retry without changing memories or expanding permissions. Never silently upload a full memory database.

This release uses local Mac inference, Qwen3-ASR speech input and approved local speech output. Speech workers load cached models with networking disabled; the desktop has no browser dictation or cloud fallback. Process-scoped OS-denied-network tests passed for recognition, Qwen3.6:35b recall after a runtime restart, and approved synthesis. A physical disconnected reboot remains untested. See [listening evidence](../software/mack/LISTENING.md). Optional assisted routing remains future work.

## Downloading better models without losing Mack

Implemented now: select an installed conversational model in Control Panels; save its exact name and digest separately from memories; refuse inference when that digest changes until explicitly reselected. Embedding and known cloud-backed entries are excluded. A model switch never grants new tools or permissions. The original browser notes migrate idempotently into the local database; changing models does not move or rewrite them.

Planned update pipeline:

1. Fetch a model into a staging slot from a verified publisher/runtime source. Record model family, revision, hash, quantization, tokenizer, license reference, runtime minimum, modalities and measured resource budget.
2. Run fixed tests for personal-fact recall, correction/forgetting, unknown facts, misleading input, structured action proposals, model errors, interruption, resource use and cold/warm latency.
3. Compare against the current version with the same prompts and context. Keep durable memory schema and retrieval settings constant for a fair comparison.
4. Select the candidate explicitly only after it passes; keep the previous artifact and configuration available for rollback. Do not automatically accept a tag update.
5. Treat embedding changes as a separate index migration. Preserve source records and provenance; rebuild and validate the index without rewriting personal facts.

Automatic download, evaluation-driven promotion, signed manifests and one-click rollback are **not implemented** in 0.3. Installed-model switching and digest checks are implemented.

## Continuum, Terrarium and Exocortex

These are proposed services with distinct ownership. No existing project or private database was changed to build Mack.

| Service | What Mack could use | First adapter boundary |
| --- | --- | --- |
| Continuum research project | Evidence, candidate memories, explicit governance, trusted-memory retrieval and outcome attribution. | Read a deliberately scoped export of active trusted memories with IDs/provenance. Offer new experiences for review through a separate opt-in path. Preserve its frozen experiments and keep `retrieval.semantic_expansion` off under the existing ruling. |
| Terrarium (`LLM Arcade Game`) | An inhabited simulated world, resident behavior and experiments in learning/social interaction. | Import explicit outward exports only while its recorded observation-window restrictions remain unresolved. Keep simulated experiences labeled and separate from real memories. It is not a qualified physics simulator for Mack’s legs. |
| Exocortex | Selected personal facts, project state and user-authorized work context. | Read/export allowlisted records with source, timestamp and scope. Do not ingest the entire dossier, share credentials, or give a model unrestricted filesystem/shell access. |
| Continuum hexapod reference | Brain/spine separation, bounded requests, mock adapters and outcome records. | Test and adapt abstractions for a mock four-leg body. Retain upstream provenance; do not adopt hexapod geometry or limits as Mack settings. |

A shared future envelope should carry `source`, `record_id`, `revision`, `observed_at`, `scope`, `kind` (real/simulated), `provenance`, and deletion/correction status. A service adapter must report unavailable/stale data honestly. All outward actions remain independently governed. The API shapes and adapters still need implementation and tests.

## What lasting memory means in 0.3

Memories are explicit user-saved facts in SQLite, independent of model weights. The model does not autonomously decide what becomes permanent. The user can inspect, correct, trash and restore them. The most relevant six notes are selected by deterministic word overlap; this is a limited baseline, not Continuum’s governed retrieval or semantic recall. Corrections and removals exclude older conversation context from the next prompt to prevent the obvious stale-fact path.

All completed exchanges persist in a searchable local archive. The current chat displays up to 40; New Conversation starts a fresh visible session without deleting history. AI context includes up to four recent exchanges and four retrieved archived excerpts, plus six fact excerpts. Retrieval uses word matching with a recent fallback, not a semantic memory engine. A curated fact change conservatively excludes earlier dialogue from AI retrieval; the archive UI still shows it. Conversation Trash is recoverable and excluded from recall, independently of curated facts. Backups and original browser records may retain previous values. The database has owner-only file permissions and is ignored by Git; encryption and automated backups are not supplied.

Keep `runtime/mack/` backed up with Mack’s server stopped. Restore into a separate `--data-dir` first and verify before replacing a working copy. Unknown database schema versions are refused without migration or overwrite. Model downtime does not prevent inspecting or explicitly saving facts.
