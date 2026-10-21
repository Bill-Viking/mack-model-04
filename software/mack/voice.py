"""Optional local neural speech. The desktop and memory work without MLX installed."""
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import threading
import time
import wave
from collections import OrderedDict
from pathlib import Path

from .runtime import MackError, clean_text


class VoiceService:
    def __init__(self, root, timeout=180):
        self.root = Path(root).resolve()
        self.config_path = self.root / 'runtime/voice/config.json'
        self.python = self.root / '.venv/bin/python'
        self.worker = self.root / 'tools/synthesize_voice.py'
        self.timeout = timeout
        self.gate = threading.Lock()
        self.lock = threading.Lock()
        self.process = None
        self.ident = None
        self.cancelled = OrderedDict()

    def config(self):
        try:
            config = json.loads(self.config_path.read_text())
            for key in ('model_path', 'reference_path'):
                path = Path(config[key]).resolve()
                if not path.is_relative_to(self.root) or not path.exists():
                    raise ValueError('Missing local asset')
            if not self.python.is_file() or not self.worker.is_file():
                raise ValueError('Voice runtime is missing')
            if hashlib.sha256(Path(config['reference_path']).read_bytes()).hexdigest() != config['reference_sha256']:
                raise ValueError('Reference changed')
            if not isinstance(config['reference_text'], str) or not 1 <= len(config['reference_text']) <= 2000:
                raise ValueError('Reference transcript is missing')
            if not all(isinstance(config[key], str) and config[key] for key in ('model_id', 'revision')):
                raise ValueError('Model provenance is missing')
            return config
        except (OSError, ValueError, KeyError, TypeError):
            raise MackError('The local reference voice is not ready. Check its installation; no other voice was substituted.', 503) from None

    def status(self):
        try:
            config = self.config()
            return {'available': True, 'label': 'Mack · SAL reference study',
                    'engine': 'Qwen3-TTS 1.7B Base · MLX',
                    'model': config['model_id'], 'revision': config['revision'],
                    'message': 'Local reference voice installed. Voice likeness awaits your audition.',
                    'styles': ['natural', 'film'],
                    'max_text': 600}
        except MackError as error:
            return {'available': False, 'label': 'Mack · SAL reference study',
                    'message': str(error), 'max_text': 600}

    @staticmethod
    def validate_id(ident):
        if not isinstance(ident, str) or not re.fullmatch(r'[a-zA-Z0-9-]{8,80}', ident):
            raise MackError('Invalid voice request identity.')

    def cancel(self, ident):
        self.validate_id(ident)
        with self.lock:
            # Remember cancellation even when it arrives before the speech request.
            self.cancelled[ident] = True
            while len(self.cancelled) > 256:
                self.cancelled.popitem(last=False)
            if self.ident == ident and self.process and self.process.poll() is None:
                self.process.kill()

    def close(self):
        with self.lock:
            if self.process and self.process.poll() is None:
                self.process.kill()

    def synthesize(self, payload):
        text = clean_text(payload.get('text'), 600)
        ident = payload.get('id')
        self.validate_id(ident)
        style = payload.get('style', 'natural')
        if style not in ('natural', 'film'):
            raise MackError('Choose a supported voice delivery.')
        self.config()
        if not self.gate.acquire(blocking=False):
            raise MackError('Mack is preparing another spoken reply. Stop it or wait a moment.', 409)
        start = time.monotonic()
        process = None
        try:
            directory = self.root / 'runtime/voice/jobs'
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            with tempfile.TemporaryDirectory(dir=directory) as job:
                output = Path(job) / 'speech.wav'
                with self.lock:
                    if ident in self.cancelled:
                        raise MackError('Voice stopped.', 409)
                    environment = dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                                       HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1')
                    process = subprocess.Popen(
                        [str(self.python), str(self.worker), '--config', str(self.config_path), '--output', str(output)],
                        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        cwd=self.root, env=environment)
                    self.process, self.ident = process, ident
                try:
                    process.communicate(json.dumps({'text': text, 'style': style}).encode(), timeout=self.timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate()
                    raise MackError('Local voice took too long and was stopped. The reply is still here to read.', 504) from None
                with self.lock:
                    if ident in self.cancelled:
                        raise MackError('Voice stopped.', 409)
                if process.returncode != 0 or not output.is_file():
                    raise MackError('Local voice could not finish. The reply is still here to read; no other voice was substituted.', 503)
                if output.stat().st_size > 12_000_000:
                    raise MackError('Local voice returned too much audio.', 502)
                data = output.read_bytes()
                try:
                    with wave.open(io.BytesIO(data)) as wav:
                        if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getframerate() != 24000 or not 0 < wav.getnframes() <= 24000 * 120:
                            raise ValueError('Invalid audio')
                except (wave.Error, EOFError, ValueError):
                    raise MackError('Local voice returned invalid audio.', 502) from None
                return data, round(time.monotonic() - start, 2)
        except OSError:
            raise MackError('The local voice process could not start or read its audio. Conversation and memory are still available.', 503) from None
        finally:
            with self.lock:
                if process and process.poll() is None:
                    process.kill()
                    process.wait()
                self.process, self.ident = None, None
            self.gate.release()
