# Local reference voice on Apple silicon

Mack can generate new speech using a private reference recording and a pinned
Qwen3-TTS Base model. This is a first audition implementation. Voice likeness is
judged by listening; installation and successful synthesis do not establish a match.

Bill's Mac is already configured. In Mack's Control Panels, select **Mack · SAL
reference study**. **Reference · dry** keeps the original delivery. **Film study ·
light echo** uses an alternate sampling preset with quiet early reflections and
an 85 ms echo. The Base model does not offer instruction-controlled inflection.
The second preset is a listening experiment, not a measured copy of film processing.

Edit **Audition text**, then choose **Hear voice preview**. This generates new
speech without saving a conversation or memory. **Read aloud** plays any existing
reply. **Stop voice**, Escape or a new message interrupts speech. A selected engine
that fails is reported; another voice is never substituted automatically.

## Reproduce the installation

This path requires an Apple silicon Mac and Python 3.12. The desktop server itself
still uses only Python's standard library. Voice packages live in this repository's
ignored `.venv`; model files use roughly 4.2 GiB in ignored `runtime/voice/models/`.
The model is pinned to revision `a6eb4f68e4b056f1215157bb696209bc82a6db48`.

WHERE: Mac Terminal, repository root. Install the isolated voice dependencies:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r software/mack/requirements-voice-macos.txt
```

Prepare a user-chosen, clean reference as mono PCM16 WAV at 24 kHz. This first
setup accepts 3–30 seconds. Put its exact transcript in a private UTF-8 text file.
Paths below are placeholders for those two local files.

WHERE: Mac Terminal, repository root. Download the pinned model and configure it:

```sh
.venv/bin/python tools/configure_voice.py --download \
  --reference "/path/to/private/reference.wav" \
  --transcript "/path/to/private/transcript.txt"
```

The tool keeps a reference copy under ignored `private-media/voice-reference/`,
and configuration under ignored `runtime/voice/config.json`. It records a SHA-256
of the WAV. A changed or missing reference blocks synthesis until reconfigured.
Reference recordings, transcripts, generated audio and model weights are not in Git.
Original model/engine terms are documented by
[Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) and
[MLX Audio](https://github.com/Blaizzy/mlx-audio); reference-media permissions are
separate from those software licenses.

## Runtime behavior and limits

- The existing loopback API and token protect voice status, synthesis and cancellation.
- The browser sends text, a request ID and a supported delivery preset. It cannot
  choose model URLs, files, shell arguments or reference recordings through the API.
- One isolated process synthesizes at a time, with a 180-second timeout. Text is
  passed through stdin. Cancelling kills that job; temporary output is removed.
- Text segments are limited to 600 characters. Longer replies are split and spoken
  sequentially. There is a pause while the next segment is prepared.
- The worker loads fixed local paths with Hugging Face/Transformers offline mode
  and telemetry disabled. There is no cloud speech endpoint or download fallback.
- **Preparing voice** describes synthesis. **Speaking** follows the media player's
  playing event. Stop cancels playback and pending synthesis. Audio output is mono
  24 kHz PCM16, with peak limiting to prevent clipping.
- The first dry greeting produced 6.08 seconds of audio in 5.73 seconds on an M2 Max.
  The light-echo audition is 6.25 seconds. These are sample observations; streaming,
  a warm resident model, physical network-disconnection tests, and Linux/onboard
  qualification remain open.
- Browser dictation is a separate, opt-in input path and may use the browser
  vendor's online service. Local speech output does not make that input offline.

The Mac runtime and its dependencies are an initial implementation. A future Linux
voice backend should retain the same interface, identity and memory boundaries.
