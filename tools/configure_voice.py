#!/usr/bin/env python3
"""Configure a private WAV reference and optionally download the pinned Mac model."""
import argparse
import hashlib
import json
import shutil
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16'
REVISION = 'a6eb4f68e4b056f1215157bb696209bc82a6db48'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True, help='Mono PCM16 WAV at 24000 Hz')
    parser.add_argument('--transcript', type=Path, required=True, help='UTF-8 file with the exact reference words')
    parser.add_argument('--download', action='store_true', help='Download the pinned 4.2 GiB model')
    args = parser.parse_args()
    transcript = args.transcript.read_text().strip()
    if not 1 <= len(transcript) <= 2000:
        parser.error('Reference transcript must have 1–2000 characters.')
    with wave.open(str(args.reference)) as wav:
        if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) != (1, 2, 24000):
            parser.error('Reference must be mono PCM16 WAV at 24000 Hz.')
        if not 3 <= wav.getnframes() / wav.getframerate() <= 30:
            parser.error('This first audition supports a 3–30 second reference.')
    model_path = ROOT / 'runtime/voice/models/qwen3-tts-1.7b-base'
    if args.download:
        from huggingface_hub import snapshot_download
        snapshot_download(MODEL, revision=REVISION, local_dir=model_path, max_workers=4)
    for name in ['config.json', 'model.safetensors', 'speech_tokenizer/model.safetensors']:
        if not (model_path / name).is_file():
            parser.error('Model is incomplete. Use --download to install the pinned revision.')
    digest = hashlib.sha256(args.reference.read_bytes()).hexdigest()
    directory = ROOT / 'private-media/voice-reference'
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    reference = directory / (digest + '.wav')
    if args.reference.resolve() != reference:
        shutil.copyfile(args.reference, reference)
    reference.chmod(0o600)
    config = {'model_id': MODEL, 'revision': REVISION, 'model_path': str(model_path),
              'reference_path': str(reference), 'reference_sha256': digest,
              'reference_text': transcript, 'engine': 'mlx-audio', 'engine_version': '0.6.1'}
    destination = ROOT / 'runtime/voice/config.json'
    temporary = destination.with_suffix('.tmp')
    temporary.write_text(json.dumps(config, indent=2)+'\n')
    temporary.chmod(0o600)
    temporary.replace(destination)
    print('Local reference voice configured. Open Control Panels in Mack to audition it.')


if __name__ == '__main__':
    main()
