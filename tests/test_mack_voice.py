"""Exercise local voice process limits and cancellation without downloading models."""
import hashlib
import json
import copy
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'software'))
from mack.voice import VoiceService
from mack.runtime import MackError


class VoiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['runtime/voice/model', '.venv/bin', 'tools', 'software/mack']:
            (self.root / name).mkdir(parents=True)
        (self.root / '.venv/bin/python').symlink_to(sys.executable)
        reference = self.root / 'reference.wav'
        reference.write_bytes(b'reference fixture')
        self.config = {'model_path': str(self.root / 'runtime/voice/model'),
                       'reference_path': str(reference), 'reference_text': 'Fixture.',
                       'reference_sha256': hashlib.sha256(reference.read_bytes()).hexdigest(),
                       'model_id': 'fixture', 'revision': 'fixed',
                       'engine': 'mlx-audio', 'engine_version': '0.6.1'}
        self.profile = json.loads((Path(__file__).resolve().parents[1] / 'software/mack/voice-profile.json').read_text())
        for key in ('model_id', 'revision', 'reference_sha256'):
            self.profile[key] = self.config[key]
        self.profile['reference_text_sha256'] = hashlib.sha256(b'Fixture.').hexdigest()
        for path, key in [('runtime/voice/model/generation_config.json', 'generation_config_sha256'),
                          ('software/mack/requirements-voice-macos.txt', 'requirements_sha256')]:
            (self.root / path).write_bytes(b'fixture')
            self.profile[key] = hashlib.sha256(b'fixture').hexdigest()
        (self.root / 'software/mack/voice-profile.json').write_text(json.dumps(self.profile))
        (self.root / 'runtime/voice/config.json').write_text(json.dumps(self.config))
        (self.root / 'tools/synthesize_voice.py').write_text('''
import argparse,json,sys,time,wave,os
p=argparse.ArgumentParser();p.add_argument('--config');p.add_argument('--output');a=p.parse_args()
request=json.load(sys.stdin);text=request['text']
if text=='expect-film': assert request['style']=='film'
if text=='expect-natural': assert request['style']=='natural'
assert os.environ['HF_HUB_OFFLINE']=='1'
if text=='wait': time.sleep(20)
if text=='fail': sys.exit(4)
if text=='invalid':
    open(a.output,'wb').write(b'not audio');sys.exit(0)
with wave.open(a.output,'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(b'\\x00\\x01'*2400)
''')
        self.voice = VoiceService(self.root, timeout=0.3)
        self.addCleanup(self.voice.close)

    def test_valid_audio_is_returned_without_retained_jobs(self):
        data, _ = self.voice.synthesize({'id': 'voice-okay', 'text': 'Hello'})
        self.assertTrue(data.startswith(b'RIFF'))
        self.assertEqual(list((self.root / 'runtime/voice/jobs').iterdir()), [])

    def test_missing_or_changed_reference_is_not_substituted(self):
        self.assertTrue(self.voice.status()['available'])
        Path(self.config['reference_path']).write_bytes(b'changed')
        self.assertFalse(self.voice.status()['available'])
        with self.assertRaises(MackError):
            self.voice.synthesize({'id': 'voice-missing', 'text': 'Hello'})

    def test_approved_default_and_explicit_alternative_reach_the_worker(self):
        self.assertEqual(self.voice.status()['profile'], 'mack-voice-v1')
        self.assertTrue(self.voice.synthesize({'id': 'voice-default', 'text': 'expect-film'})[0])
        self.assertTrue(self.voice.synthesize({'id': 'voice-natural', 'text': 'expect-natural', 'style': 'natural'})[0])

    def test_changed_config_cannot_silently_redefine_the_approved_voice(self):
        for key, value in [('reference_text', 'Other words.'), ('reference_sha256', 'other'),
                           ('model_id', 'new model'), ('revision', 'new revision'),
                           ('engine', 'other engine'), ('engine_version', 'future')]:
            config = copy.deepcopy(self.config)
            config[key] = value
            (self.root / 'runtime/voice/config.json').write_text(json.dumps(config))
            with self.subTest(key=key):
                self.assertFalse(self.voice.status()['available'])
                with self.assertRaises(MackError):
                    self.voice.synthesize({'id': 'voice-drift', 'text': 'Hello'})
                self.assertIsNone(self.voice.process)

    def test_changed_sampling_defaults_or_dependency_recipe_block_generation(self):
        for name in ['runtime/voice/model/generation_config.json', 'software/mack/requirements-voice-macos.txt']:
            path = self.root / name
            path.write_bytes(b'changed')
            with self.subTest(path=name):
                self.assertFalse(self.voice.status()['available'])
            path.write_bytes(b'fixture')
            self.assertTrue(self.voice.status()['available'])

    def test_early_cancel_prevents_generation_and_long_text_is_rejected(self):
        self.voice.cancel('voice-early')
        for payload in [{'id': 'voice-early', 'text': 'Hello'},
                        {'id': 'voice-long', 'text': 'x'*601},
                        {'id': 'voice-style', 'text': 'Hello', 'style': 'unknown'},
                        {'id': '../path', 'text': 'Hello'}]:
            with self.assertRaises(MackError):
                self.voice.synthesize(payload)

    def test_timeout_failure_and_invalid_audio_release_the_engine(self):
        for text, status in [('wait', 504), ('fail', 503), ('invalid', 502)]:
            with self.assertRaises(MackError) as error:
                self.voice.synthesize({'id': 'voice-'+text, 'text': text})
            self.assertEqual(error.exception.status, status)
        self.assertTrue(self.voice.synthesize({'id': 'voice-recovery', 'text': 'Hello'})[0])

    def test_cancellation_kills_active_process_and_concurrent_job_is_refused(self):
        self.voice.timeout = 5
        errors = []
        def run():
            try:
                self.voice.synthesize({'id': 'voice-cancel', 'text': 'wait'})
            except MackError as error:
                errors.append(error.status)
        thread = threading.Thread(target=run)
        thread.start()
        try:
            deadline = time.monotonic()+2
            while self.voice.process is None and time.monotonic()<deadline:
                time.sleep(0.01)
            self.assertIsNotNone(self.voice.process)
            with self.assertRaises(MackError) as error:
                self.voice.synthesize({'id': 'voice-conflict', 'text': 'Hello'})
            self.assertEqual(error.exception.status, 409)
            self.voice.cancel('voice-cancel')
            thread.join(2)
            self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [409])
        finally:
            self.voice.close()
            thread.join(2)


if __name__ == '__main__':
    unittest.main()
