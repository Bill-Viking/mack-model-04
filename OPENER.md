lane: RayCue/Research
written: 2026-10-21T13:07:57-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: 44f087c (parent of local reference voice checkpoint)
status_updated: 2026-10-21T13:07:57-07:00
where: Local SAL-reference voice works; Bill requested more inflection/echo; second audition selected, likeness not yet accepted
next: machine
depends_on: onboard measurements for hardware; configured provider for optional cloud use
open_in: /Users/bill/Projects/RayCue Mac · existing RayCue/Research chat
judgment: Preserve local memory and independent control; benchmark models and qualify offline voice before onboard claims
model: Preserve the user's model choice and read the live dial
---
Read STATUS.md first, then software/mack/VOICE.md, docs/personality-and-voice.md and docs/product-spec.md.

WHERE WE ARE

Goal: Mack is a personalized intelligence with her own Linux-based system, a classic Mac desktop, local AI and lasting memory. The first body is the four-legged Mac; a humanoid body is the long-term goal, years away. She keeps her identity and memory across models, voice engines and bodies.

1. Local Qwen3.6:35b conversation, SQLite memory, editable Memories/Trash and read-only status/clock/memory-search tools work on Bill's M2 Max.
2. Qwen3-TTS 1.7B Base now generates new speech from Bill's selected SAL reference clip locally. MLX Audio 0.6.1 is isolated in .venv. The pinned model, clip, transcript and outputs are private ignored files.
3. Bill liked the first audition and requested more inflection and echo. Reference · dry preserves it. Film study · light echo is the second delivery, selected in the live browser with automatic reply reading on. Exact likeness is not yet accepted.
4. The desktop verifies Preparing voice → actual Speaking, Stop, completion and saved preferences. 47 Python + 14 JS checks pass. Production memory is unchanged across restarts and auditions.

Bill's next move: listen to the second audition and describe what should change.
Machine's next move: refine delivery from that judgment; do not claim an exact match or pretend to have heard the playback. The Base model has no instruction-controlled prosody. Its alternate sampling and short echoes are experimental choices, not measured film processing. Conversational restraint still needs tuning: Qwen sometimes adds unnecessary offers or questions.

LIVE SERVICE

http://127.0.0.1:9844/ stays running for Bill, unified-exec session 73995. Resolve the current PID before any process action. The isolated voice QA server has been stopped. Never stop the shared Ollama service.

PRIVATE LOCAL ASSETS

runtime/mack/memory.sqlite3 contains personal memory/history. runtime/voice/config.json points to a hash-checked WAV and fixed local model. runtime/voice/auditions/mack-first-hello.wav is the dry audition (6.08 seconds); mack-film-study.wav is the second (6.25 seconds, actual API generation 4.6 seconds). Original reference and provenance are in private-media/sal-reference/. A content-addressed copy is in private-media/voice-reference/. Neither media, transcripts, weights nor databases belong in Git. Generated speech jobs use temporary directories that are removed after the request.

Voice synthesis uses offline model-loading flags and no cloud fallback. Fully disconnected reboot, local microphone input, streaming, warm-model optimization and Linux/onboard qualification remain open. A private Whisper Tiny spot check hallucinated repetitions over silence; it is not an accepted evaluator or connected speech-input feature.

NEXT PRODUCT WORK

Qualify voice with Bill, then fully local speech recognition and an enforced offline/assisted routing policy. Build and verify the mock-body contract, then measured packaging/mass/power budgets. The RayCue model, actual dimensions/mass, actuators, controller, sensors and battery remain unselected. No sensors or motors are connected. Continuum, Terrarium and Exocortex remain proposed separate services; preserve their project boundaries and do not copy the private Agent 99 personality into this public repo.

PUBLIC WORK

https://github.com/Bill-Viking/mack-model-04 is public. The README, specification and architecture make personalized intelligence and eventual humanoid embodiment explicit. docs/public-introduction.md holds approved Facebook/X copy. Resonance confirmed both posts were published once and verified after reload. Facebook retained Friends audience; X is Public. Exact permalinks and proofs live in Resonance's private application report mack-vision-publications-20261021.context.json. Do not duplicate either post.

Keep the loose root PNG untracked. Keep vendor snapshots and notices unchanged. No iCloud writes. This chat remains active until Bill ends it.
