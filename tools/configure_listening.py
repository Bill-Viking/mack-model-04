#!/usr/bin/env python3
"""One-time, explicit download of Mack's pinned local speech recognizer."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software'))
from mack.listening import MODEL, REVISION


def main():
    from huggingface_hub import snapshot_download
    path = ROOT / 'runtime/listening/models/qwen3-asr-0.6b-8bit'
    snapshot_download(MODEL, revision=REVISION, local_dir=path,
                      allow_patterns=['*.json', '*.safetensors', '*.txt', 'README.md'], max_workers=4)
    config = path.parents[1] / 'config.json'
    config.write_text(json.dumps({'model_id': MODEL, 'revision': REVISION, 'model_path': str(path)}, indent=2)+'\n')
    config.chmod(0o600)
    print('Mack’s local listening is installed. No model download occurs during conversation.')


if __name__ == '__main__':
    main()
