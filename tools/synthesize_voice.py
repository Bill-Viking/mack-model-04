#!/usr/bin/env python3
"""One isolated local synthesis job. Text arrives on stdin, never in process arguments."""
import argparse
import json
import os
import sys
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software'))
from mack.voice_profile import load_profile, validate_profile

# No model downloads, telemetry or online fallback during speech generation.
os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                  HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    profile = load_profile(ROOT)
    validate_profile(ROOT, config, profile)
    if version('mlx-audio') != profile['engine_version']:
        raise ValueError('Installed speech engine differs from the approved version.')
    request = json.loads(sys.stdin.read(10000))
    text = request['text']
    style = request.get('style', profile['default_style'])
    if style not in ('natural', 'film'):
        raise ValueError('Unknown voice delivery.')
    if not isinstance(text, str) or not 1 <= len(text.strip()) <= 600:
        raise ValueError('Voice text must be between 1 and 600 characters.')

    import mlx.core as mx
    import numpy as np
    import soundfile as sf
    from mlx_audio.tts.utils import load_model

    # Preserve Bill's approved recipe. The Base model has no prosody instruction API.
    delivery = profile['styles'][style]
    mx.random.seed(delivery['seed'])
    model = load_model(config['model_path'])
    chunks = []
    samples = 0
    for result in model.generate(text=text.strip(), lang_code=profile['language'],
                                 ref_audio=config['reference_path'],
                                 ref_text=config['reference_text'],
                                 temperature=delivery['temperature'],
                                 max_tokens=profile['max_tokens']):
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
    reflections = delivery['reflections']
    if reflections:
        # Quiet early reflections and a short echo preserve intelligibility.
        source = audio
        audio = np.pad(source, (0, round(max(delay for delay, _ in reflections) * model.sample_rate)))
        for delay, gain in reflections:
            offset = round(delay * model.sample_rate)
            audio[offset:offset + len(source)] += source * gain
    peak = float(np.max(np.abs(audio)))
    if peak < 0.0001:
        raise ValueError('Voice produced only silence.')
    # Only prevent clipping; do not pitch-shift or remove the reference's texture.
    if peak > profile['peak_limit']:
        audio *= profile['peak_limit'] / peak
    sf.write(str(args.output), audio, model.sample_rate, subtype='PCM_16')
    print(json.dumps({'seconds': len(audio) / model.sample_rate,
                      'sample_rate': model.sample_rate, 'peak': peak, 'style': style}))


if __name__ == '__main__':
    main()
