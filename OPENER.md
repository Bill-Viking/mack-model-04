lane: RayCue/Research
written: 2026-10-21T14:16:17-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: 52eeed7 (local listening and conversation archive; pushed and remote verified)
status_updated: 2026-10-21T14:16:17-07:00
where: Local listening and archive implemented; Chrome switched from Bose to built-in microphone for Bill’s live test
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
3. Bill approved the second light-echo audition: “that’s it, lock that voice in.” Mack voice v1 is now the default. The versioned software/mack/voice-profile.json drives synthesis and guards the reference, transcript and installation recipe. The accepted recording is preserved privately. The live browser selects Approved v1 · light echo with automatic reading on. Do not continue tuning or request approval again for this voice.
4. The desktop verifies Preparing voice → actual Speaking, Stop, completion and saved preferences. 50 Python + 15 JS checks pass. A default API request reproduced the accepted WAV byte-for-byte on this Mac after locking. Production memory is unchanged across restarts and auditions.

Bill has accepted the sound. Preserve voice v1 while progressing toward full offline speech and the wider product. Future voice changes should use a separate version and compare against the preserved audition. Acceptance records Bill’s listening judgment, not an independently measured exact film match. Conversational restraint still needs tuning: Qwen sometimes adds unnecessary offers or questions.

LIVE SERVICE

http://127.0.0.1:9844/ stays running for Bill, unified-exec session 69302. Resolve the current PID before any process action. The isolated voice QA server has been stopped. Never stop the shared Ollama service.

PRIVATE LOCAL ASSETS

runtime/mack/memory.sqlite3 contains personal memory/history. runtime/voice/config.json points to a hash-checked WAV and fixed local model. runtime/voice/auditions/mack-first-hello.wav is the dry audition (6.08 seconds); mack-film-study.wav is the second (6.25 seconds, actual API generation 4.6 seconds). Original reference and provenance are in private-media/sal-reference/. A content-addressed copy is in private-media/voice-reference/. The accepted baseline is runtime/voice/approved/mack-voice-v1/audition.wav (SHA256 6192f95cd23edf174d3451619cfc6f1647e5e6ec0e3a1f85f8f84c0b5164a1fb), alongside reference/transcript/configuration copies. verification.wav is a later identical test output; the original accepted sample was not replaced. Neither media, transcripts, weights nor databases belong in Git. Generated speech jobs use temporary directories that are removed after the request.

Voice synthesis uses offline model-loading flags and no cloud fallback. Local input is implemented and OS-scoped offline tests pass. Bill’s live microphone acceptance, disconnected reboot, streaming, warm-model optimization and Linux/onboard qualification remain open. A private Whisper Tiny spot check hallucinated repetitions over silence; it is not an accepted evaluator or connected speech-input feature.

LOCAL LISTENING — CURRENT TURN

Local Qwen3-ASR-0.6B-8bit is installed under runtime/listening/ and connected to Talk to Mack → Finish & send → local model → approved voice. The old online browser dictation path is removed. Recordings are temporary, at most 60 seconds; cancellation/timeout releases tracks/processes. Conversation archive is durable, searchable and recoverable, with schema-2 migration preserving old records. New Conversation no longer deletes history. AI recall is bounded word matching with the existing fact-edit boundary.

63 Python + 21 JS checks pass. OS-scoped offline tests passed for transcription, exact approved synthesis, and isolated Qwen3.6 archive recall after restart. See software/mack/LISTENING.md for model revision, setup, timings and limits. The shared Ollama service was untouched.

Bill says his microphone did not work. Chrome permission is allowed; changed its input from Bose NC 700 UC backup to MacBook Pro Microphone (Built-in), explicitly requested by Bill. Chrome spoken replies are now on. Await Bill's real result; typed messages and a model saying it heard him are not microphone evidence. IAB microphone startup timed out. Production Chrome tab 1005073246 at port9844 is the trial; preserve it. Final input-device-name/status and honest-input instructions are now live after idle restart/reload. QA server port9845 is stopped and temporary QA tab9 is closed. The actual input blocker is now identified: AppleClamshellState=Yes, so the MacBook built-in microphone is physically disconnected by the closed lid. Studio Display Microphone is available. Await Bill’s choice to switch to it or open the lid, then verify real spoken input and audible reply.

NEXT PRODUCT WORK

Keep the accepted voice v1. Qualify disconnected speech, then fully local speech recognition and an enforced offline/assisted routing policy. Build and verify the mock-body contract, then measured packaging/mass/power budgets. The RayCue model, actual dimensions/mass, actuators, controller, sensors and battery remain unselected. No sensors or motors are connected. Continuum, Terrarium and Exocortex remain proposed separate services; preserve their project boundaries and do not copy the private Agent 99 personality into this public repo.

PUBLIC WORK

https://github.com/Bill-Viking/mack-model-04 is public. The README, specification and architecture make personalized intelligence and eventual humanoid embodiment explicit. docs/public-introduction.md holds approved Facebook/X copy. Resonance confirmed both posts were published once and verified after reload. Facebook retained Friends audience; X is Public. Exact permalinks and proofs live in Resonance's private application report mack-vision-publications-20261021.context.json. Do not duplicate either post.

Bill subsequently authorized the approved voice clip on Facebook and X. Resonance published one playable title-card video on each, retaining Facebook Friends / X Public, with AI labels and the project link. Both were reloaded and playback-checked. Exact links and screenshots are in the private receipt mack-voice-publications-20261021.context.json. Original baseline WAV is unchanged. Do not repeat these voice posts.

Keep the loose root PNG untracked. Keep vendor snapshots and notices unchanged. No iCloud writes. This chat remains active until Bill ends it.
