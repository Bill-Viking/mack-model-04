#!/usr/bin/env python3
"""Offline recognition, optionally keeping weights warm between local requests."""
import argparse
import contextlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software'))
from mack.offline import deny_network

os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1')
deny_network()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--audio', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--serve', action='store_true')
    args = parser.parse_args()
    if not args.serve and (not args.audio or not args.output):
        parser.error('Use --serve or provide --audio and --output.')
    from importlib.metadata import version
    if version('mlx-audio') != '0.6.1':
        raise ValueError('Use the pinned MLX Audio environment.')
    import soundfile as sf
    from mlx_audio.stt import load
    config = json.loads(args.config.read_text())
    with contextlib.redirect_stdout(sys.stderr):
        model = load(config['model_path'])

    def recognize(path):
        audio, rate = sf.read(path, dtype='float32')
        if rate != 16000 or audio.ndim != 1:
            raise ValueError('Expected mono 16 kHz audio.')
        with contextlib.redirect_stdout(sys.stderr):
            result = model.generate(audio, language='English', max_tokens=512, temperature=0.0, verbose=False)
        return {'text': result.text, 'truncated': result.generation_tokens >= 512}

    if args.serve:
        # Only the parent supplies these temporary paths. No listener or network API.
        for line in sys.stdin:
            request = json.loads(line)
            print(json.dumps(recognize(request['audio'])), flush=True)
    else:
        args.output.write_text(json.dumps(recognize(args.audio)))
        args.output.chmod(0o600)


if __name__ == '__main__':
    main()
