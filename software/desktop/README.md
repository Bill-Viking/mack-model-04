# Mack Local AI 0.2

A Platinum-inspired desktop connected to real local inference and a durable memory service. Original HTML/CSS/JavaScript/SVG; Python standard library backend. No emulator, Apple system software or frontend package installation.

![Mack Local AI](../../docs/images/mack-local-ai.jpg)

## Open on the Mac

1. WHERE: Finder, this repository. Double-click **Start Mack.command**.
2. WHERE: the browser at **http://127.0.0.1:9844/**. Type a message and press **Send**.
3. WHERE: Mack’s message field. Try **Remember that I like jazz**, then ask **What music do I like?** Use a true preference you want saved.

Keep the launcher’s Terminal window open. Python 3 and a running local Ollama with a downloaded conversational model are required. Bill’s Mac already has both; `qwen3.6:35b` is the initial model. This repository does not install Ollama or download weights automatically. Starting the launcher twice reopens the existing instance. Control-C stops the desktop service without erasing memories.

## Conversation and voice

Ordinary messages go to the selected local Ollama model. The desktop shows the selected model, real waiting state and connection failures. Explicit **Remember that…** / **Save note…** requests save directly through the memory service. The model cannot write memories or invoke tools on its own.

Enable **Read Mack’s replies aloud** in Control Panels for a browser-supplied local voice. Optional **Allow browser dictation** enables the Dictate button when the browser supports speech recognition. It starts only after a click, asks for microphone permission, and places a transcript in the composer for review before Send. The browser vendor may process dictation online. Mac keyboard dictation is another input option. The in-app browser exposed a speech-recognition API and the opt-in gate worked; no microphone capture was started, so transcription has not been tested end to end.

Escape dismisses the pending reply, cancels local speech, and requests that the service discard an unfinished generated reply. The Ollama request may keep computing until it finishes or times out; a new conversation or memory change can be refused briefly while that request completes. Explicit saves already completed are retained. No always-on microphone is implemented.

## SAL-inspired personality and voice study

Mack now has a persistent [SAL-inspired personality](../mack/persona.md) loaded
for every model-generated reply. It shapes conversation while keeping runtime
capabilities and memory rules explicit. The [voice design and acceptance plan](../../docs/personality-and-voice.md)
distinguishes the implemented personality from the unfinished film-voice target.

In Control Panels, choose a **Local voice**, adjust **Pace** and **Pitch**, and
click **Hear voice preview**. The preview works without enabling automatic reply
reading and does not add a conversation or memory. **Stop voice** or Escape stops
it. Preferences survive reload. If a saved voice becomes unavailable, choose
another; Mack does not silently substitute an online voice.

The current sound is a stock local voice study, initially Samantha when available.
It is not an exact reproduction of SAL's film voice. A neural voice model, approved
reference, acoustic comparison and offline/onboard qualification remain open.

## Lasting memory

- Facts live in `runtime/mack/memory.sqlite3`, independently of browser settings and model weights. Runtime data is ignored by Git and never included in the repository push.
- Memories supports inspection, edits, recoverable Trash and restoration. There are limits of 100 active notes and 100 trashed notes, with 2,000 characters per fact.
- Each response receives up to six notes ranked by word overlap. This is a small deterministic retrieval baseline; it can miss relevant facts. It is not an integrated Continuum service.
- The last 40 completed exchanges persist. Only the latest four since a memory change enter model context. Editing/trashing a fact excludes earlier conversation context from the next prompt. The visible old conversation remains historical text until New Conversation clears it.
- New Conversation clears recent exchanges and keeps saved facts. Trash is excluded from inference but remains recoverable; it is not secure erasure. Original browser notes and backups may retain prior values.
- Old `mack.desktop.v1` browser notes import idempotently. Corrections and Trash moves in the database are preserved on subsequent imports. The original browser data is left intact, including when malformed or an import exceeds capacity.
- Appearance/voice/dictation preferences stay in browser localStorage under `mack.desktop.preferences.v2`. They are separate from personal memory.

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
| app.js / styles.css / index.html | Classic desktop, memory editor, real service states and browser voice/dictation. |
| service.mjs | Same-origin API requests and bootstrap token. |
| voice.mjs | Local-only voice selection and validated delivery preferences. |
| ../mack/persona.md | Model-independent SAL-inspired personality, read by the runtime. |
| model.mjs | Legacy browser-state validation and retained 0.1 demo helpers/tests; no longer the live conversation engine. |
| ../mack/runtime.py | SQLite persistence, explicit memory commands, bounded retrieval, local Ollama adapter and request serialization. |
| ../../tools/serve_desktop.py | Loopback HTTP service and launcher. |

## Verification

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/desktop.test.mjs tests/voice.test.mjs
python3 tools/sources.py check
```

Automated checks exercise persistence across runtime instances/model changes, correction and Trash context, atomic/idempotent legacy migration, explicit-only writes, provider outages, digest changes, duplicate request handling, cancellation/concurrent mutation, unknown database versions, model filtering, endpoint restrictions, request validation and static asset boundaries. The JavaScript tests retain legacy migration and demo coverage.

Live model/UI checks and outstanding limitations are recorded in the project STATUS. Hardware and microphone transcription are not covered by these tests. Expression buttons remain labeled previews.
