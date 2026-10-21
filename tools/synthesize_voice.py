#!/usr/bin/env python3
"""One isolated local synthesis job. Text arrives on stdin, never in process arguments."""
import argparse
import json
import os
from pathlib import Path

# No model downloads, telemetry or online fallback during speech generation.
os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                  HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    import sys
    request = json.loads(sys.stdin.read(10000))
    text = request['text']
    style = request.get('style', 'natural')
    if style not in ('natural', 'film'):
        raise ValueError('Unknown voice delivery.')
    if not isinstance(text, str) or not 1 <= len(text.strip()) <= 600:
        raise ValueError('Voice text must be between 1 and 600 characters.')

    import mlx.core as mx
    import numpy as np
    import soundfile as sf
    from mlx_audio.tts.utils import load_model

    # The Base model has no instruction-style prosody control. This second
    # sampling preset is an audition, not a claim to reproduce film acoustics.
    mx.random.seed(29 if style == 'film' else 17)
    model = load_model(config['model_path'])
    chunks = []
    samples = 0
    for result in model.generate(text=text.strip(), lang_code='english',
                                 ref_audio=config['reference_path'],
                                 ref_text=config['reference_text'],
                                 temperature=0.85 if style == 'film' else 0.7,
                                 max_tokens=1800):
        chunk = np.asarray(result.audio, dtype=np.float32).reshape(-1)
        if not np.isfinite(chunk).all():
            raise ValueError('Voice produced invalid samples.')
        chunks.append(chunk)
        samples += len(chunk)
        if samples > model.sample_rate * 120:
            raise ValueError('Voice exceeded its duration limit.')
    if not chunks or not samples:
        raise ValueError('Voice produced no audio.')
    audio = np.concatenate(chunks)
    if style == 'film':
        # Quiet early reflections and a short echo preserve intelligibility.
        source = audio
        reflections = [(0.019, 0.035), (0.037, 0.025), (0.085, 0.09), (0.17, 0.025)]
        audio = np.pad(source, (0, round(0.17 * model.sample_rate)))
        for delay, gain in reflections:
            offset = round(delay * model.sample_rate)
            audio[offset:offset + len(source)] += source * gain
    peak = float(np.max(np.abs(audio)))
    if peak < 0.0001:
        raise ValueError('Voice produced only silence.')
    # Only prevent clipping; do not pitch-shift or remove the reference's texture.
    if peak > 0.98:
        audio *= 0.98 / peak
    sf.write(str(args.output), audio, model.sample_rate, subtype='PCM_16')
    print(json.dumps({'seconds': len(audio) / model.sample_rate,
                      'sample_rate': model.sample_rate, 'peak': peak, 'style': style}))


if __name__ == '__main__':
    main()
