"""Versioned voice recipe. Personal reference audio and transcripts stay private."""
import hashlib
import json
from pathlib import Path


def load_profile(root):
    return json.loads((Path(root) / 'software/mack/voice-profile.json').read_text())


def validate_profile(root, config, profile):
    """Refuse silent reference, transcript, model revision or recipe drift."""
    for key in ('model_id', 'revision', 'engine', 'engine_version', 'reference_sha256'):
        if config[key] != profile[key]:
            raise ValueError('Voice installation differs from the approved profile: ' + key)
    if hashlib.sha256(config['reference_text'].encode()).hexdigest() != profile['reference_text_sha256']:
        raise ValueError('Reference transcript differs from the approved profile')
    files = [(Path(config['reference_path']), 'reference_sha256'),
             (Path(config['model_path']) / 'generation_config.json', 'generation_config_sha256'),
             (Path(root) / 'software/mack/requirements-voice-macos.txt', 'requirements_sha256')]
    for path, key in files:
        if hashlib.sha256(path.read_bytes()).hexdigest() != profile[key]:
            raise ValueError('Voice asset differs from the approved profile: ' + key)
