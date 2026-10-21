# Mack Local AI 0.3

A Platinum-inspired desktop connected to real local inference and a durable memory service. Original HTML/CSS/JavaScript/SVG; Python standard library backend. No emulator, Apple system software or frontend package installation.

![Mack Local AI](../../docs/images/mack-local-ai.jpg)

## Open on the Mac

1. WHERE: Finder, this repository. Double-click **Start Mack.command**.
2. WHERE: the browser at **http://127.0.0.1:9844/**. Type a message and press **Send**.
3. WHERE: Mack’s message field. Try **Remember that I like jazz**, then ask **What music do I like?** Use a true preference you want saved.

Keep the launcher’s Terminal window open. Python 3 and a running local Ollama with a downloaded conversational model are required. Bill’s Mac already has both; `qwen3.6:35b` is the initial model. This repository does not install Ollama or download weights automatically. Starting the launcher twice reopens the existing instance. Control-C stops the desktop service without erasing memories.

## Conversation and voice

Ordinary messages go to the selected local Ollama model. The desktop shows the selected model, real waiting state and connection failures. Explicit **Remember that…** / **Save note…** requests save directly through the memory service. Completed exchanges are archived automatically. The model cannot edit curated facts. Tool-capable models can request four read-only tools: current status, local clock, active-memory search and past-conversation search. Try **Check your status** or **Check the clock and tell me the time**. Calls are bounded and unknown tools are refused. Models without tool support retain ordinary text conversation.

Click **Talk to Mack**, allow microphone access, and watch **Live transcript** update while speaking. Provisional words may correct themselves; the meter and sound indicator show whether audio is arriving. Updates are requested about once per second using the local recognizer. **Finish & send** closes the microphone and checks the complete transcript before sending it to the local conversational model. Mack saves the completed exchange and answers in **approved voice v1**. Maximum recording length is 60 seconds. Escape or **Cancel recording** discards an unfinished recording/transcription. Closing Mack or hiding the page stops capture. There is no wake word or continuous listening. Live drafts are not saved in the conversation archive.

Control Panels has **Review transcript before sending** for names or recognition errors. This leaves the transcript in the message field to edit before **Send**. Silence and near-silence are rejected; background noise can still be misrecognized. [Local listening setup and evidence](../mack/LISTENING.md) documents the pinned model and offline tests. Browser microphone permission is required; use Chrome or Safari if the embedded browser does not grant access. The former browser dictation service has been removed.

Escape dismisses the pending reply, cancels local speech, and requests that the service discard an unfinished generated reply. The Ollama request may keep computing until it finishes or times out; a new conversation or memory change can be refused briefly while that request completes. Explicit saves already completed are retained. No always-on microphone is implemented.

Completed replies show which tools were checked or failed. These receipts appear
for the current browser conversation; they are not yet retained in saved history
after a reload. Tool search returns at most six matching active notes and never
reads Trash. It uses word overlap rather than semantic search.

## SAL-inspired personality and approved voice

Mack now has a persistent [SAL-inspired personality](../mack/persona.md) loaded
for every model-generated reply. It shapes conversation while keeping runtime
capabilities and memory rules explicit. The [voice design and acceptance plan](../../docs/personality-and-voice.md)
records Bill’s acceptance of the light-echo voice v1 and the remaining product checks.

Control Panels defaults to **Mack · approved voice v1** with **Approved v1 · light
echo** for new preferences. **Reference · dry (alternative)** and **Stock Mac voice**
remain available, and saved explicit choices survive reload. Edit the audition text and click
**Hear voice preview**. It works without automatic reading and writes no memory.
**Stop voice** or Escape stops preparation/playback. **Read aloud** beneath a reply
plays it on demand. Preferences survive reload; failure never substitutes another
voice. Pace and Pitch apply only to the stock browser engine.

Bill accepted voice v1 on 2026-10-21. Its recipe and the accepted private recording
are preserved. A full disconnected reboot, long-form speech quality and
Linux/onboard performance remain open.
See [voice setup and boundaries](../mack/VOICE.md) for installation and local files.

## Lasting memory

- Facts live in `runtime/mack/memory.sqlite3`, independently of browser settings and model weights. Runtime data is ignored by Git and never included in the repository push.
- Memories supports inspection, edits, recoverable Trash and restoration. There are limits of 100 active notes and 100 trashed notes, with 2,000 characters per fact.
- Each response receives up to six note excerpts (800 characters each), ranked by word overlap. This is a small deterministic retrieval baseline; it can miss relevant facts. It is not an integrated Continuum service.
- All completed exchanges remain in the local archive; the visible chat shows the latest 40 from the current conversation. New Conversation starts a fresh visible chat while preserving the archive and facts.
- **Conversations** searches full exchanges, pages through history and moves individual exchanges to recoverable Trash. Restoring brings them back into recall. Trashing an exchange does not remove a separately saved fact; edit Memories for that.
- Each reply receives up to four recent exchanges (600 characters per side) and four matching archived excerpts (400 per side), using word matching with a recent fallback. Full originals stay in the archive. This is bounded retrieval, not perfect recall or model training.
- Any curated fact change sets a conservative recall boundary: dialogue before that change remains searchable in the archive UI but is excluded from AI retrieval to avoid reviving corrected or removed information. Conversation Trash is excluded from inference. Trash and backups are not secure erasure.
- Old `mack.desktop.v1` browser notes import idempotently. Corrections and Trash moves in the database are preserved on subsequent imports. The original browser data is left intact, including when malformed or an import exceeds capacity.
- Appearance/voice/transcript-review preferences stay in browser localStorage under `mack.desktop.preferences.v2`. They are separate from personal memory.

Back up the **runtime/mack/** folder with Mack’s server stopped. Test a restored copy using `--data-dir /absolute/path/to/copied-memory`. This build provides owner-only database permissions, but no database encryption or automatic backup. Unsupported database schema versions are refused without overwrite.

## Model changes

Control Panels lists installed conversational models. **Use model** saves the model name and digest; facts remain unchanged. If that artifact changes, Mack requires explicit reselection. Embedding-only and known cloud-backed models are excluded; a cloud-backed `/api/show` response is also rejected before inference. This version has no hosted provider fallback, model downloader, automatic promotion or rollback UI. See the [research and upgrade plan](../../docs/model-strategy.md).

## Service and development

From the repository root:

```sh
python3 tools/serve_desktop.py --no-open
```

The service binds only to `127.0.0.1`, with a fixed asset allowlist, strict Host/Origin checks and a per-process token for state access and mutations. It does not expose the repository or arbitrary files. The desktop CSP permits only same-origin service requests. Ollama requests ignore environment proxies and reject redirects. There is no shell, web, camera, motion, Continuum, Terrarium or Exocortex capability. The server is a local development service; it is not configured for another device to connect over a network.

A different `--port` uses the same database unless `--data-dir` changes. Browser preferences and legacy migration remain tied to the browser address. Do not share one data directory between multiple server processes; request serialization is per process.

| Code | Purpose |
| --- | --- |
| app.js / styles.css / index.html | Classic desktop, memory editor, real service states and voice and local microphone capture. |
| service.mjs | Same-origin API requests and bootstrap token. |
| listening.mjs / microphone-worklet.js | Click-to-talk capture, live draft scheduling, WAV encoding, levels and microphone release. |
| ../mack/listening.py / ../../tools/transcribe_audio.py | Bounded local recognition, temporary audio and a warm worker with idle release. |
| voice.mjs | Local-only voice selection and validated delivery preferences. |
| ../mack/persona.md | Model-independent SAL-inspired personality, read by the runtime. |
| ../mack/identity.json / toolbox.py | Persistent she/her identity and bounded read-only status, clock and memory tools. |
| model.mjs | Legacy browser-state validation and retained 0.1 demo helpers/tests; no longer the live conversation engine. |
| ../mack/runtime.py | SQLite persistence, explicit memory commands, bounded retrieval, local Ollama adapter and request serialization. |
| ../../tools/serve_desktop.py | Loopback HTTP service and launcher. |

## Verification

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.mjs
python3 tools/sources.py check
```

Automated checks exercise persistence across runtime instances/model changes, correction and Trash context, atomic/idempotent legacy migration, explicit-only writes, provider outages, digest changes, duplicate request handling, cancellation/concurrent mutation, unknown database versions, model filtering, endpoint restrictions, request validation and static asset boundaries. The JavaScript tests retain legacy migration and demo coverage.

Live model/UI checks and outstanding limitations are recorded in the project STATUS. Audio validation, microphone release/cancellation, archive migration and retention are covered. Live microphone accuracy and physical hardware need separate trials. Expression buttons remain labeled previews.
