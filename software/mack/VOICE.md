# Local reference voice on Apple silicon

Mack can generate new speech using a private reference recording and a pinned
Qwen3-TTS Base model. Bill approved the second, light-echo audition on 2026-10-21:
“that's it, lock that voice in.” It is now **Mack · approved voice v1**.

Bill's Mac is configured with **Approved v1 · light echo**, using the same sampling
and reflections he accepted. No sound settings were changed during the lock.
The dry delivery and stock Mac voice remain explicit alternatives. New preferences
and API requests without a style default to the approved reference voice; an
existing explicit choice is preserved. Automatic playback remains a separate toggle.

Edit **Audition text**, then choose **Hear voice preview**. This generates new
speech without saving a conversation or memory. **Read aloud** plays any existing
reply. **Stop voice**, Escape or a new message interrupts speech. A selected engine
that fails is reported; another voice is never substituted automatically.

## Preserved baseline

[voice-profile.json](voice-profile.json) is the public recipe. It records the pinned
model revision, MLX Audio version, reference/transcript checksums, seed 29,
temperature 0.85, English, 1800-token limit, clipping ceiling 0.98, and reflections
at 19/37/85/170 ms with gains 0.035/0.025/0.09/0.025. Other generation defaults come
from the pinned model and engine. The worker reads this profile directly.

The accepted 6.25-second mono PCM16 24 kHz WAV is preserved byte-for-byte at
`runtime/voice/approved/mack-voice-v1/audition.wav`, with private copies of the
reference, transcript, configuration and install recipe. Its SHA-256 is in the
public profile. These private assets remain ignored by Git. Preserve voice v1 when
trying a new engine or delivery; create and audition a separate version first.
Model weights are pinned by download revision, not rehashed on every utterance.
A seed and pinned recipe do not guarantee identical output across different hardware.
Acceptance of the sound does not finish offline, long-form or onboard qualification.

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

Restore the approved private mono PCM16 WAV at 24 kHz and its exact transcript.
Setup accepts 3–30 seconds and verifies both against the versioned profile.
The approved recording is not distributed by this repository.
Paths below are placeholders for those two local files.

WHERE: Mac Terminal, repository root. Download the pinned model and configure it:

```sh
.venv/bin/python tools/configure_voice.py --download \
  --reference "/path/to/private/reference.wav" \
  --transcript "/path/to/private/transcript.txt"
```

The tool keeps a reference copy under ignored `private-media/voice-reference/`,
and configuration under ignored `runtime/voice/config.json`. It records a SHA-256
of the WAV. A changed or missing reference, transcript, declared model revision,
model generation defaults or dependency recipe blocks synthesis. Configuration
refuses a different reference before downloading or replacing the installed setup.
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
  and telemetry disabled. A Python audit hook blocks network socket access in speech workers. There is no cloud speech endpoint or download fallback.
- **Preparing voice** describes synthesis. **Speaking** follows the media player's
  playing event. Stop cancels playback and pending synthesis. Audio output is mono
  24 kHz PCM16, with peak limiting to prevent clipping.
- The first dry greeting produced 6.08 seconds of audio in 5.73 seconds on an M2 Max.
  The light-echo audition is 6.25 seconds. These are sample observations; streaming,
  a warm resident model, physical network-disconnection tests, and Linux/onboard
  qualification remain open.
- Local click-to-talk input uses Qwen3-ASR. Its [setup and verification](LISTENING.md) includes OS-denied-network speech and recall tests. The approved greeting reproduced byte-for-byte under that policy; no acoustic setting changed.

The Mac runtime and its dependencies are an initial implementation. A future Linux
voice backend should retain the same interface, identity and memory boundaries.
