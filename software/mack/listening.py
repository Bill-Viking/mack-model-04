"""Bounded local WAV transcription. Recordings are temporary, never memories."""
import array
import io
import json
import math
import os
import subprocess
import tempfile
import time
import wave
from pathlib import Path

from .runtime import MackError
from .voice import VoiceService

MODEL = 'mlx-community/Qwen3-ASR-0.6B-8bit'
REVISION = '89e96d92ba34aca20b3e29fb10cc284097d1219f'
MAX_BYTES = 1_920_044


def validate_audio(data):
    try:
        if not 44 < len(data) <= MAX_BYTES:
            raise ValueError()
        with wave.open(io.BytesIO(data)) as wav:
            if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) != (1, 2, 16000):
                raise ValueError()
            frames = wav.getnframes()
            if not 3200 <= frames <= 960000:
                raise ValueError()
            raw = wav.readframes(frames)
            if len(raw) != frames * 2:
                raise ValueError()
        samples = array.array('h', raw)
        if __import__('sys').byteorder != 'little':
            samples.byteswap()
        rms = math.sqrt(sum(x*x for x in samples) / len(samples)) / 32768
        if rms < 0.001:
            raise MackError('I did not hear speech. Check the selected microphone or move closer and try again.', 422)
        return frames / 16000
    except (ValueError, wave.Error, EOFError):
        raise MackError('Use a 0.2–60 second mono PCM16 WAV at 16 kHz.', 400) from None


class ListeningService(VoiceService):
    def __init__(self, root, timeout=90):
        super().__init__(root, timeout)
        self.config_path = self.root / 'runtime/listening/config.json'
        self.worker = self.root / 'tools/transcribe_audio.py'

    def config(self):
        try:
            config = json.loads(self.config_path.read_text())
            model = Path(config['model_path']).resolve()
            if not model.is_relative_to(self.root) or config['model_id'] != MODEL or config['revision'] != REVISION:
                raise ValueError()
            for file in ('config.json', 'model.safetensors', 'tokenizer_config.json', 'preprocessor_config.json', 'vocab.json', 'merges.txt'):
                if not (model / file).is_file():
                    raise ValueError()
            if not self.python.is_file() or not self.worker.is_file():
                raise ValueError()
            return config
        except (OSError, ValueError, KeyError, TypeError):
            raise MackError('Local listening is not installed. Run tools/configure_listening.py once while online. You can still type.', 503) from None

    def status(self):
        try:
            config = self.config()
            return {'available': True, 'model': config['model_id'], 'revision': config['revision'],
                    'message': 'Local listening ready. Audio stays on this Mac and is discarded after transcription.',
                    'max_seconds': 60, 'network': 'disabled in speech worker'}
        except MackError as error:
            return {'available': False, 'message': str(error), 'max_seconds': 60}

    def transcribe(self, data, ident):
        self.validate_id(ident)
        duration = validate_audio(data)
        self.config()
        if not self.gate.acquire(blocking=False):
            raise MackError('Another recording is being transcribed. Stop it or wait a moment.', 409)
        process = None
        started = time.monotonic()
        try:
            directory = self.root / 'runtime/listening/jobs'
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            with tempfile.TemporaryDirectory(dir=directory) as job:
                audio, output = Path(job) / 'recording.wav', Path(job) / 'transcript.json'
                audio.write_bytes(data)
                audio.chmod(0o600)
                with self.lock:
                    if ident in self.cancelled:
                        raise MackError('Listening stopped.', 409)
                    process = subprocess.Popen([str(self.python), str(self.worker), '--config', str(self.config_path),
                                                '--audio', str(audio), '--output', str(output)],
                                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.root,
                                               env=dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_HUB_DISABLE_TELEMETRY='1'))
                    self.process, self.ident = process, ident
                try:
                    process.wait(timeout=self.timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                    raise MackError('Local transcription took too long. Try a shorter recording.', 504) from None
                with self.lock:
                    if ident in self.cancelled:
                        raise MackError('Listening stopped.', 409)
                if process.returncode or not output.is_file() or output.stat().st_size > 12000:
                    raise MackError('Local transcription could not finish. Nothing was sent to Mack. Try again or type.', 503)
                result = json.loads(output.read_text())
                if not isinstance(result, dict):
                    raise ValueError('Invalid transcription response')
                text = result.get('text')
                if not isinstance(text, str) or not text.strip() or len(text) > 2000 or result.get('truncated'):
                    raise MackError('I could not transcribe that clearly. Try a shorter sentence or type it.', 422)
                return {'text': text.strip(), 'audio_seconds': duration, 'seconds': round(time.monotonic()-started, 2), 'local': True}
        except (OSError, ValueError, TypeError):
            raise MackError('The local speech recognizer is unavailable. You can still type.', 503) from None
        finally:
            with self.lock:
                if process and process.poll() is None:
                    process.kill()
                    process.wait()
                self.process, self.ident = None, None
            self.gate.release()
