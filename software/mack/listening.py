"""Bounded local WAV transcription. Recordings are temporary, never memories."""
import array
import io
import json
import math
import os
import select
import subprocess
import tempfile
import threading
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
        self.warm_process = None
        self.idle_timer = None
        self.closed = False

    @staticmethod
    def dispose(process):
        if process:
            if process.poll() is None:
                process.kill()
            process.wait()
            for pipe in (process.stdin, process.stdout):
                if pipe:
                    pipe.close()

    def retire(self, process):
        with self.lock:
            if self.warm_process is process and self.ident is None:
                self.dispose(process)
                self.warm_process = None

    def close(self):
        with self.lock:
            self.closed = True
            if self.idle_timer:
                self.idle_timer.cancel()
            # The active request owns its pipes until its finally block runs.
            if self.ident is not None:
                if self.process and self.process.poll() is None:
                    self.process.kill()
            else:
                self.dispose(self.warm_process)
                self.warm_process = None

    def read_result(self, process, timeout):
        deadline = time.monotonic() + timeout
        data = bytearray()
        while b'\n' not in data:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([process.stdout], [], [], remaining)[0]:
                raise MackError('Local transcription took too long. Try a shorter recording.', 504)
            block = os.read(process.stdout.fileno(), 4096)
            if not block or len(data) + len(block) > 12000:
                raise ValueError('Invalid recognizer response')
            data.extend(block)
        return json.loads(data)

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
                    'message': 'Live local transcript ready. Words update while you speak; audio is discarded after recognition.',
                    'max_seconds': 60, 'live_preview': True, 'network': 'disabled in speech worker'}
        except MackError as error:
            return {'available': False, 'message': str(error), 'max_seconds': 60}

    def transcribe(self, data, ident, preview=False):
        self.validate_id(ident)
        try:
            duration = validate_audio(data)
        except MackError as error:
            if preview and error.status == 422:
                return {'text': '', 'local': True, 'partial': True, 'seconds': 0}
            raise
        self.config()
        if not self.gate.acquire(blocking=False):
            raise MackError('Another recording is being transcribed. Stop it or wait a moment.', 409)
        process = None
        successful = False
        started = time.monotonic()
        try:
            directory = self.root / 'runtime/listening/jobs'
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            with tempfile.TemporaryDirectory(dir=directory) as job:
                audio = Path(job) / 'recording.wav'
                audio.write_bytes(data)
                audio.chmod(0o600)
                with self.lock:
                    if ident in self.cancelled or self.closed:
                        raise MackError('Listening stopped.', 409)
                    if self.idle_timer:
                        self.idle_timer.cancel()
                    if self.warm_process and self.warm_process.poll() is not None:
                        self.dispose(self.warm_process)
                        self.warm_process = None
                    if self.warm_process is None:
                        self.warm_process = subprocess.Popen(
                            [str(self.python), str(self.worker), '--config', str(self.config_path), '--serve'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            bufsize=0, cwd=self.root,
                            env=dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_HUB_DISABLE_TELEMETRY='1'))
                    process = self.warm_process
                    self.process, self.ident = process, ident
                process.stdin.write((json.dumps({'audio': str(audio)})+'\n').encode())
                process.stdin.flush()
                result = self.read_result(process, min(self.timeout, 15) if preview else self.timeout)
                with self.lock:
                    if ident in self.cancelled:
                        raise MackError('Listening stopped.', 409)
                if not isinstance(result, dict):
                    raise ValueError('Invalid transcription response')
                text = result.get('text')
                if not isinstance(text, str) or (not text.strip() and not preview) or len(text) > 2000 or result.get('truncated'):
                    raise MackError('I could not transcribe that clearly. Try a shorter sentence or type it.', 422)
                successful = True
                return {'text': text.strip(), 'audio_seconds': duration, 'seconds': round(time.monotonic()-started, 2), 'local': True, 'partial': preview}
        except (OSError, ValueError, TypeError):
            with self.lock:
                if ident in self.cancelled or self.closed:
                    raise MackError('Listening stopped.', 409) from None
            raise MackError('The local speech recognizer is unavailable. You can still type.', 503) from None
        finally:
            with self.lock:
                self.process, self.ident = None, None
                if process and (not successful or self.closed or ident in self.cancelled):
                    self.dispose(process)
                    self.warm_process = None
                elif process:
                    # Keep weights, never recorded audio, warm across live updates.
                    self.idle_timer = threading.Timer(30, self.retire, args=(process,))
                    self.idle_timer.daemon = True
                    self.idle_timer.start()
            self.gate.release()
