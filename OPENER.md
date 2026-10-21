lane: RayCue/Research
written: 2026-10-21T16:24:00-07:00
by: ACT — RayCue/Research: Mac OS 9 and walking robot
on: MAC
head: f768412 (on/off controls; single-message layout and input provenance follow)
status_updated: 2026-10-21T16:24:00-07:00
where: Bill confirmed live speech works; one message box and Ask Mack to reply are live
next: bill
depends_on: further conversational/voice qualification and onboard measurements
open_in: /Users/bill/Projects/RayCue Mac · existing RayCue/Research chat
judgment: Preserve local memory and independent control; benchmark models and qualify offline voice before onboard claims
model: Preserve the user's model choice and read the live dial
---
Read STATUS.md first, then software/mack/VOICE.md, docs/personality-and-voice.md and docs/product-spec.md.

Latest acceptance and layout: Bill confirmed “Yes, my words appear” and supplied a scan showing recognized speech. Real microphone/transcript acceptance is met. One Your message textarea now holds typed or live spoken words; Ask Mack to reply submits it. Microphone settings are folded below it. Off reviews; cancel restores the prior draft. Input provenance accompanies new requests so the model can distinguish speech transcripts from typing; old incorrect replies remain in history. 68 Python + 27 JS checks pass and browser QA verified the flow. Production reloaded, Studio Display selected, Bill's unsent “hello” preserved. Production exec74151; resolve PID before actions. No memory or approved-voice change. Older notes calling speech acceptance pending or using Send to Mack are superseded.

Latest interaction: Turn microphone on → speak and see Live transcript → Turn microphone off to review → Send to Mack for her answer. At 60 seconds capture stops for review without sending. A separate Send can also finish an active recording. The live transcript box is visible even when off. Browser QA with labeled prerecorded speech verified live words, off retaining an editable transcript and no SQL change until explicit Send; production memory unchanged. 27 JS checks pass. Production reloaded, Studio Display still selected, microphone off. Ask for Bill's actual spoken result without treating the QA sample as proof of his speech. Earlier Talk to Mack / Finish & send instructions are superseded.

Latest interface fix: added Microphone chooser with exact device selection and browser-local persistence. Studio Display Microphone is explicitly selected in the production in-app browser, verified across reload and actual capture. Missing devices are refused without fallback; refresh enumerates without opening a mic. 27 JS checks pass, including new exact-selection and unavailable-device checks. Browser console clean. Capture cancelled; no diagnostic transcript submitted. Bill should click Talk to Mack and speak; full speech/reply acceptance remains pending. No backend or approved-voice changes.

Latest microphone fix: MacBook lid remained closed, so changed the macOS default input from its disconnected built-in microphone to Studio Display Microphone. Verified System Settings, hardware inventory, Mack's active device label and a changing nonzero meter in the existing in-app browser. “Sound detected” appeared; intelligible speech from Bill is not yet confirmed. Cancelled the 48-second diagnostic capture without sending it. Microphone is off between turns. Bill should click Talk to Mack and speak toward the display. IAB is working for capture now; the earlier Chrome-only workaround is no longer required. Preserve his memory and voice.

Latest interface change: Talk to Mack shows a live local transcript during recording, with one preview request about every second, a sound indicator and a final full transcription before submission. Warm recognition is measured at 0.14–0.23 seconds on short test samples; first startup took 1.87 seconds. Prerecorded browser QA showed words at the two-second mark and verified final review/cancellation; this is not Bill's physical mic acceptance. 66 Python + 25 JS checks pass. The built-in mic remains selected and the lid was still closed at 14:42. Bill has a pending trial prompt to open the lid and test the live words. Preserve his memory and accepted voice.

Latest research: docs/model-strategy.md now covers downloadable Muse Glimmer 30B, Qwen3.8-27B, Gemma 4 and EmbeddingGemma 2. Glimmer/Qwen are the recommended first Mac comparison; no new weights are installed or selected. Muse Spark Open is now downloadable but far too large here. NVIDIA Bolt E4B is only announced for October 23. Preserve the approved voice and existing memory while evaluating candidates in isolated data.

WHERE WE ARE

Goal: Mack is a personalized intelligence with her own Linux-based system, a classic Mac desktop, local AI and lasting memory. The first body is the four-legged Mac; a humanoid body is the long-term goal, years away. She keeps her identity and memory across models, voice engines and bodies.

1. Local Qwen3.6:35b conversation, SQLite memory, editable Memories/Trash and read-only status/clock/memory-search tools work on Bill's M2 Max.
2. Qwen3-TTS 1.7B Base now generates new speech from Bill's selected SAL reference clip locally. MLX Audio 0.6.1 is isolated in .venv. The pinned model, clip, transcript and outputs are private ignored files.
3. Bill approved the second light-echo audition: “that’s it, lock that voice in.” Mack voice v1 is now the default. The versioned software/mack/voice-profile.json drives synthesis and guards the reference, transcript and installation recipe. The accepted recording is preserved privately. The live browser selects Approved v1 · light echo with automatic reading on. Do not continue tuning or request approval again for this voice.
4. The desktop verifies Preparing voice → actual Speaking, Stop, completion and saved preferences. 50 Python + 15 JS checks pass. A default API request reproduced the accepted WAV byte-for-byte on this Mac after locking. Production memory is unchanged across restarts and auditions.

Bill has accepted the sound. Preserve voice v1 while progressing toward full offline speech and the wider product. Future voice changes should use a separate version and compare against the preserved audition. Acceptance records Bill’s listening judgment, not an independently measured exact film match. Conversational restraint still needs tuning: Qwen sometimes adds unnecessary offers or questions.

LIVE SERVICE

http://127.0.0.1:9844/ stays running for Bill, unified-exec session 1868, PID 94662 at deployment. Resolve the current PID before any process action. The isolated transcript QA server/tab have been stopped. Both production views were reloaded. Never stop the shared Ollama service.

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

Bill's repository rule is public viewing with editing under his control. For Mack, GitHub lists only Bill-Viking as a collaborator (admin), with no pending invitations, verified 2026-10-21. Do not grant others write access. Assistants act on Bill's behalf within authorized work. Preserve the separate private/local-only rules for other projects; this was not a bulk visibility change or an account-wide permissions audit.

Bill subsequently authorized the approved voice clip on Facebook and X. Resonance published one playable title-card video on each, retaining Facebook Friends / X Public, with AI labels and the project link. Both were reloaded and playback-checked. Exact links and screenshots are in the private receipt mack-voice-publications-20261021.context.json. Original baseline WAV is unchanged. Do not repeat these voice posts.

Keep the loose root PNG untracked. Keep vendor snapshots and notices unchanged. No iCloud writes. This chat remains active until Bill ends it.
