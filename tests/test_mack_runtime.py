"""Persistence, corrections, provider changes, cancellation and service boundaries."""
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'software'))
from mack.runtime import MackError, Ollama, Runtime, Store


class Provider:
    def __init__(self):
        self.digest = 'digest-one'
        self.calls = []
        self.failure = False
        self.started = threading.Event()
        self.release = None

    def models(self):
        if self.failure:
            raise MackError('Offline', 503)
        return [{'name': 'first', 'digest': self.digest, 'size': 100},
                {'name': 'second', 'digest': 'digest-two', 'size': 100}]

    def chat(self, model, messages):
        self.calls.append((model, messages))
        self.started.set()
        if self.release:
            self.release.wait(5)
        if self.failure:
            raise MackError('Offline', 503)
        return 'A generated reply.', 4


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.provider = Provider()
        self.runtime = Runtime(self.temp.name, self.provider)
        self.runtime.health()
        self.number = 0

    def chat(self, text):
        self.number += 1
        return self.runtime.chat({'id': 'request-' + str(self.number), 'text': text})

    def test_explicit_memory_survives_restart_and_model_change(self):
        self.chat('Remember that my workshop is called Juniper.')
        self.assertEqual(len(self.provider.calls), 0)
        replacement = Runtime(self.temp.name, self.provider)
        replacement.select('second')
        replacement.chat({'id': 'request-new', 'text': 'What is my workshop called?'})
        model, messages = self.provider.calls[-1]
        self.assertEqual(model, 'second')
        self.assertIn('Juniper', messages[0]['content'])
        self.assertEqual(len(replacement.store.snapshot()['notes']), 1)
        self.assertEqual(self.runtime.store.path.stat().st_mode & 0o777, 0o600)

    def test_only_explicit_requests_write_memory(self):
        self.chat('I like jazz. Can you help plan my day?')
        self.assertEqual(self.runtime.store.snapshot()['notes'], [])
        self.assertEqual(len(self.runtime.store.snapshot()['history']), 1)

    def test_edit_and_trash_remove_stale_context(self):
        self.chat('Remember that my workshop is Juniper.')
        self.chat('What is my workshop?')
        note = self.runtime.store.snapshot()['notes'][0]
        self.runtime.change(self.runtime.store.save, 'My workshop is Cedar.', note['id'])
        self.chat('What is my workshop?')
        prompt = json.dumps(self.provider.calls[-1][1])
        self.assertNotIn('Juniper', prompt)
        self.assertIn('Cedar', prompt)
        self.runtime.change(self.runtime.store.move, note['id'], True)
        self.chat('What is my workshop?')
        self.assertNotIn('Cedar', json.dumps(self.provider.calls[-1][1]))
        self.assertEqual(len(self.runtime.store.snapshot()['trash']), 1)

    def test_browser_import_is_atomic_and_does_not_overwrite_corrections(self):
        payload = {'notes': [{'id': 'old', 'text': 'Original'}], 'trash': []}
        self.runtime.store.import_browser(payload)
        self.runtime.store.save('Corrected', 'browser:old')
        self.runtime.store.import_browser(payload)
        self.assertEqual(self.runtime.store.snapshot()['notes'][0]['text'], 'Corrected')
        with self.assertRaises(MackError):
            self.runtime.store.import_browser({'notes': [{'id': 'new', 'text': 'New'}, {'id': 'bad', 'text': ''}]})
        self.assertEqual(len(self.runtime.store.snapshot()['notes']), 1)
        self.runtime.store.move('browser:old', True)
        self.runtime.store.import_browser(payload)
        self.assertEqual(self.runtime.store.snapshot()['notes'], [])

    def test_changed_digest_requires_explicit_reselection(self):
        self.provider.digest = 'changed'
        self.assertFalse(self.runtime.health()['ready'])
        with self.assertRaises(MackError):
            self.chat('Hello')
        self.runtime.select('first')
        self.assertTrue(self.runtime.health()['ready'])
        self.chat('Hello')

    def test_offline_preserves_memory_and_does_not_create_fake_turn(self):
        self.chat('Remember that I like jazz.')
        before = self.runtime.store.snapshot()
        self.provider.failure = True
        self.assertFalse(self.runtime.health()['ready'])
        with self.assertRaises(MackError):
            self.chat('Hello')
        self.assertEqual(before, self.runtime.store.snapshot())
        self.chat('Remember that I also like blues.')
        self.assertEqual(len(self.runtime.store.snapshot()['notes']), 2)

    def test_retried_request_is_idempotent_and_reuse_is_rejected(self):
        payload = {'id': 'retry-1234', 'text': 'Remember that I like jazz.'}
        self.runtime.chat(payload)
        self.assertTrue(self.runtime.chat(payload)['replayed'])
        self.assertEqual(len(self.runtime.store.snapshot()['notes']), 1)
        with self.assertRaises(MackError):
            self.runtime.chat({**payload, 'text': 'A different request'})

    def test_cancel_and_concurrent_mutation(self):
        self.provider.release = threading.Event()
        failures = []
        def work():
            try:
                self.runtime.chat({'id': 'cancel-123', 'text': 'Hello'})
            except MackError as error:
                failures.append(error)
        thread = threading.Thread(target=work)
        thread.start()
        self.assertTrue(self.provider.started.wait(2))
        try:
            with self.assertRaises(MackError) as error:
                self.runtime.change(self.runtime.store.save, 'Conflicting fact')
            self.assertEqual(error.exception.status, 409)
            with self.assertRaises(MackError):
                self.runtime.select('second')
            self.runtime.cancel('cancel-123')
        finally:
            self.provider.release.set()
            thread.join(3)
        self.assertFalse(thread.is_alive())
        self.assertEqual(failures[0].status, 409)
        self.assertEqual(self.runtime.store.snapshot()['history'], [])

    def test_new_conversation_clears_history_not_facts(self):
        self.chat('Remember that I like jazz.')
        self.runtime.change(self.runtime.store.new_conversation)
        state = self.runtime.store.snapshot()
        self.assertEqual(state['history'], [])
        self.assertEqual(len(state['notes']), 1)

    def test_retrieval_is_bounded_and_prioritizes_matching_facts(self):
        for i in range(8):
            self.runtime.store.save('Workshop project ' + str(i))
        self.runtime.store.save('My favourite bird is a kingfisher.')
        self.chat('What bird do I like?')
        memories = json.loads(self.provider.calls[-1][1][0]['content'].split('Active memory data:\n')[1])
        self.assertEqual(len(memories), 6)
        self.assertIn('kingfisher', memories[0]['text'])

    def test_future_database_version_is_preserved(self):
        with self.runtime.store.connect() as db:
            db.execute('PRAGMA user_version=99')
        with self.assertRaises(MackError):
            Store(self.temp.name)
        with self.runtime.store.connect() as db:
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 99)


class ProviderTests(unittest.TestCase):
    def test_nonlocal_endpoint_is_rejected(self):
        for url in ['https://example.com', 'http://example.com', 'http://127.0.0.1:11434/other', 'http://user:pass@localhost:11434']:
            with self.assertRaises(MackError):
                Ollama(url)

    def test_cloud_and_embedding_models_are_excluded(self):
        provider = Ollama()
        provider.request = lambda *args, **kwargs: {'models': [
            {'name': 'local', 'digest': 'a', 'capabilities': ['completion']},
            {'name': 'embed', 'digest': 'b', 'capabilities': ['embedding']},
            {'name': 'remote:cloud', 'digest': 'c'},
            {'name': 'remote-alias', 'digest': 'd', 'remote_host': 'https://example.com'}]}
        self.assertEqual([m['name'] for m in provider.models()], ['local'])
        provider.request = lambda *args, **kwargs: {'remote_host': 'https://example.com'}
        with self.assertRaises(MackError):
            provider.chat('remote-alias', [])

    def test_malformed_reply_is_a_service_error(self):
        provider = Ollama()
        provider.request = lambda path, *args, **kwargs: {} if path.endswith('show') else {'message': None, 'done': True}
        with self.assertRaises(MackError) as error:
            provider.chat('local', [])
        self.assertEqual(error.exception.status, 502)


if __name__ == '__main__':
    unittest.main()
