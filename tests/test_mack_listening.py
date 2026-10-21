"""Local audio boundaries, private jobs and cancellation without model downloads."""
import io
import json
import sys
import tempfile
import threading
import time
import unittest
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'software'))
from mack.listening import ListeningService, MODEL, REVISION, validate_audio
from mack.runtime import MackError


def wav_bytes(rate=16000, channels=1, frames=8000, silence=False):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes((b'\0\0' if silence else b'\0\x10') * frames * channels)
    return buffer.getvalue()


class ListeningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        model = self.root / 'runtime/listening/model'
        model.mkdir(parents=True)
        for name in ('config.json', 'model.safetensors', 'tokenizer_config.json', 'preprocessor_config.json', 'vocab.json', 'merges.txt'):
            (model / name).write_text('fixture')
        (self.root / '.venv/bin').mkdir(parents=True)
        (self.root / '.venv/bin/python').symlink_to(sys.executable)
        (self.root / 'tools').mkdir()
        (self.root / 'runtime/listening/config.json').write_text(json.dumps({'model_path': str(model), 'model_id': MODEL, 'revision': REVISION}))
        self.worker = self.root / 'tools/transcribe_audio.py'
        self.worker.write_text('''
import argparse,json,os,stat
p=argparse.ArgumentParser();p.add_argument('--audio');p.add_argument('--output');p.add_argument('--config');a=p.parse_args()
assert os.environ['HF_HUB_OFFLINE']=='1'
assert stat.S_IMODE(os.stat(a.audio).st_mode)==0o600
json.dump({'text':'A local transcript.'},open(a.output,'w'))
''')
        self.service = ListeningService(self.root, timeout=.5)
        self.addCleanup(self.service.close)

    def test_audio_format_duration_and_silence_boundaries(self):
        self.assertEqual(validate_audio(wav_bytes()), .5)
        for data in (b'invalid', wav_bytes(rate=24000), wav_bytes(channels=2), wav_bytes(frames=100), wav_bytes(frames=960001), wav_bytes()[:-4]):
            with self.subTest(length=len(data)), self.assertRaises(MackError) as error:
                validate_audio(data)
            self.assertEqual(error.exception.status, 400)
        with self.assertRaises(MackError) as error:
            validate_audio(wav_bytes(silence=True))
        self.assertEqual(error.exception.status, 422)

    def test_transcript_is_local_and_recording_job_is_removed(self):
        result = self.service.transcribe(wav_bytes(), 'listening-good')
        self.assertEqual(result['text'], 'A local transcript.')
        self.assertTrue(result['local'])
        self.assertEqual(list((self.root / 'runtime/listening/jobs').iterdir()), [])

    def test_missing_model_is_truthful_and_early_cancel_does_not_start_worker(self):
        self.assertTrue(self.service.status()['available'])
        self.service.cancel('listening-early')
        with self.assertRaises(MackError) as error:
            self.service.transcribe(wav_bytes(), 'listening-early')
        self.assertEqual(error.exception.status, 409)
        self.assertIsNone(self.service.process)
        (self.root / 'runtime/listening/model/model.safetensors').unlink()
        self.assertFalse(self.service.status()['available'])

    def test_timeout_and_malformed_output_release_engine_and_clean_audio(self):
        for code, status in [('import time;time.sleep(10)', 504), ('raise SystemExit(4)', 503),
                             ("import sys;open(sys.argv[-1],'w').write('{}')", 422),
                             ("import sys;open(sys.argv[-1],'w').write('not json')", 503)]:
            self.worker.write_text(code)
            with self.subTest(code=code), self.assertRaises(MackError) as error:
                self.service.transcribe(wav_bytes(), 'listening-failure')
            self.assertEqual(error.exception.status, status)
            self.assertIsNone(self.service.process)
            self.assertEqual(list((self.root / 'runtime/listening/jobs').iterdir()), [])
            self.assertTrue(self.service.gate.acquire(blocking=False))
            self.service.gate.release()

    def test_active_cancel_terminates_worker_and_busy_request_is_refused(self):
        self.service.timeout = 10
        self.worker.write_text('import time;time.sleep(20)')
        errors = []
        def run():
            try:
                self.service.transcribe(wav_bytes(), 'listening-cancel')
            except MackError as error:
                errors.append(error.status)
        thread = threading.Thread(target=run)
        thread.start()
        try:
            deadline = time.monotonic()+2
            while self.service.process is None and time.monotonic()<deadline:
                time.sleep(.01)
            self.assertIsNotNone(self.service.process)
            with self.assertRaises(MackError) as error:
                self.service.transcribe(wav_bytes(), 'listening-conflict')
            self.assertEqual(error.exception.status, 409)
            self.service.cancel('listening-cancel')
            thread.join(2)
            self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [409])
            self.assertEqual(list((self.root / 'runtime/listening/jobs').iterdir()), [])
        finally:
            self.service.close()
            thread.join(2)


if __name__ == '__main__':
    unittest.main()
