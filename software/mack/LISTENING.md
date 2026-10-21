# Local listening and conversation archive

Mack Local AI 0.3 connects click-to-talk microphone capture, local transcription,
local Ollama conversation, a lasting SQLite archive and approved voice v1.
This implementation runs on an Apple silicon development Mac. It does not qualify
a Linux robot board, battery life, a distant room microphone or a humanoid body.

## Use it

1. WHERE: Mack in Chrome or Safari at http://127.0.0.1:9844/. Click **Talk to Mack**.
2. WHERE: the browser/macOS microphone prompt. Allow access for Mack.
3. WHERE: Mack. Wait for **Microphone on**, speak, then click **Finish & send**.

Mack closes the microphone before recognizing the recording. The transcript goes
to the selected local model; its completed answer is saved and read in approved
voice v1. **Escape**, **Cancel recording**, closing Mack or hiding its page stops
capture. Recording ends at 60 seconds. No microphone runs between turns.
Control Panels offers **Review transcript before sending** to correct recognition
errors before a message is submitted. This is especially useful for names.

If an embedded browser stays at **Opening microphone**, open the same local address
in Chrome or Safari. Chrome can show a microphone chooser and **Allow while visiting
the site**. The app releases capture after a 30-second permission/startup timeout;
a permission granted after cancellation cannot leave a late stream recording.
The active input name is shown while listening. If the level meter stays empty,
check Chrome's selected input. Apple silicon MacBooks physically disconnect the
built-in microphone when the lid is closed; open the lid or choose an external
microphone, such as a Studio Display's microphone.
[Apple Platform Security](https://support.apple.com/en-ie/guide/security/secbbd20b00b/web).
An unavailable recognizer leaves typing available and never falls back to online
browser dictation. This release configures English recognition.

## One-time installation

Bill's Mac already has the recognizer. A fresh machine needs the Apple silicon
Python 3.12 environment from [VOICE.md](VOICE.md). Keep the pinned MLX Audio 0.6.1
requirements; the recognizer uses that existing environment without upgrades.

1. WHERE: Terminal, repository root, with the voice environment installed. Download the recognizer while online:

```sh
.venv/bin/python tools/configure_listening.py
```

2. WHERE: Finder, repository root. Open **Start Mack.command**.

The model is [mlx-community/Qwen3-ASR-0.6B-8bit](https://huggingface.co/mlx-community/Qwen3-ASR-0.6B-8bit),
pinned at `89e96d92ba34aca20b3e29fb10cc284097d1219f` (about 1 GB of weights).
Its model card lists Apache 2.0. See [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR)
and [MLX Audio's Qwen3-ASR integration](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/stt/models/qwen3_asr/README.md)
for upstream implementation and terms. No upstream code was vendored for this feature.
Configuration and model assets stay under ignored `runtime/listening/`.
Starting conversation never downloads models.

## Local data and limits

The browser captures mono PCM with an AudioWorklet and converts it to 16 kHz PCM16
WAV. Uploads are authenticated, same-origin and limited to 60 seconds / 1,920,044
bytes. Invalid formats, very short audio and near-silence are rejected. This energy
check is not a full voice-activity detector; room noise can still produce mistaken
words. The recognizer has one worker at a time, a 90-second deadline and a bounded
512-token / 2,000-character output. Truncation is reported rather than submitted.

Each job uses a private temporary directory and a 0600 recording file, removed
when the job succeeds, fails or is cancelled. No raw microphone recording is kept
as a memory. Transcribed words and completed answers become conversation history.
Memory files and generated media remain Git-ignored. This is not encrypted storage
or secure erasure; a machine crash, backups or filesystem recovery can retain data.

All completed exchanges remain in `runtime/mack/memory.sqlite3`. The old 40-exchange
retention limit is removed; 40 is now only the visible chat limit. **New Conversation**
starts a fresh chat without erasing the archive. **Conversations** searches full
exchanges, with pages of 20, recoverable Trash and restoration. Curated facts remain
separate in **Memories**, saved with **Remember that…** or the editor.

AI recall uses up to four relevant archive excerpts, word matching with a recent
fallback, plus four recent exchanges and six curated fact excerpts. Context is
bounded; it is not exhaustive semantic recall or learning into model weights.
Historical assistant replies are labeled as dialogue, not verified facts. Changes
to curated facts exclude older dialogue from AI retrieval, conservatively preventing
old conversation from reviving a correction or removal. That older dialogue remains
visible/searchable in Conversations. Trashing an exchange excludes it from recall
but does not remove a separately saved fact. Restore is reversible; no purge is
provided. Back up the memory folder as described in the [desktop guide](../desktop/README.md).

## Offline evidence — 2026-10-21

On Bill's M2 Max / 64 GiB Mac:

- A 6.25-second voice sample transcribed locally in 1.54 seconds with all outbound
  networking denied by macOS `sandbox-exec`. It recovered the sentence, spelling
  Mack as “Mac”; this is one sample, not an accuracy benchmark.
- Under the same deny-network policy, synthesis took 5.49 seconds and reproduced
  the approved greeting byte-for-byte: SHA-256
  `6192f95cd23edf174d3451619cfc6f1647e5e6ec0e3a1f85f8f84c0b5164a1fb`.
- A separate Qwen3.6:35b Ollama process and Mack runtime ran with outbound network
  denied except loopback. The policy allowed a local connection and rejected an
  external connection with PermissionError. After a runtime restart and a new
  conversation, Mack recalled a fictional workshop name and door color from the
  archive in 10.86 seconds, then generated the spoken answer in 7.02 seconds.
- The authenticated WAV HTTP endpoint passed a real transcription and removed its
  temporary recording. The production schema migration preserved every existing
  fact, setting and exchange. Unit tests cover cancellation, timeouts, microphone
  release, malformed audio, archive retention/recovery and access boundaries.

The OS policies were scoped to test processes; the machine's network settings and
shared Ollama service were not altered. Normal speech workers also use offline
model-loading flags and a Python socket audit guard. The runtime only addresses
loopback Ollama, ignores proxies, refuses redirects and rejects known cloud models.
No cloud API is configured. A physical disconnected cold reboot, broader accents,
noisy rooms, long conversations and Linux/onboard performance remain to be tested.
