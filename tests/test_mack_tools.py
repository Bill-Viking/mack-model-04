"""Read-only tool authority, grounded replies, bounded loops and cancellation."""
import copy
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'software'))
from mack.runtime import MackError, Ollama, Runtime, Store
from mack.toolbox import Toolbox


def tool_call(name, arguments):
    return {'function': {'name': name, 'arguments': arguments}}


def response(text='', calls=None):
    return {'done': True, 'message': {'role': 'assistant', 'content': text,
                                    'tool_calls': calls or []}}


class ToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Store(self.temp.name)
        self.store.select('local', 'digest')
        self.store.save('My favourite bird is a kingfisher.')
        old = self.store.save('My old workshop is Juniper.')
        self.store.move(old, True)
        self.box = Toolbox(self.store.snapshot())

    def test_search_excludes_trash_is_bounded_and_does_not_write(self):
        before = self.store.snapshot()
        self.assertEqual(self.box.invoke('search_memories', {'query': 'Juniper'})['data']['facts'], [])
        result = self.box.invoke('search_memories', {'query': 'kingfisher'})
        self.assertEqual(len(result['data']['facts']), 1)
        self.assertEqual(before, self.store.snapshot())
        for number in range(10):
            self.store.save('Bird fact ' + str(number))
        bounded = Toolbox(self.store.snapshot()).invoke('search_memories', {'query': 'bird'})['data']
        self.assertEqual(bounded['returned_count'], 6)
        self.assertEqual(bounded['matching_count'], 11)

    def test_unknown_and_malformed_calls_do_not_gain_authority(self):
        before = self.store.snapshot()
        for name, arguments in [('shell', {'command': 'whoami'}),
                                ('walk', {'distance': 1}), ('save_memory', {'text': 'Bad'}),
                                ('local_time', {'timezone': 'arbitrary'}),
                                ('mack_status', []), ('search_memories', {'query': 2}),
                                ('search_memories', {'query': 'x' * 201}),
                                ('search_memories', {'query': '', 'include_trash': True})]:
            self.assertFalse(self.box.invoke(name, arguments)['ok'])
        self.assertEqual(before, self.store.snapshot())

    def test_identity_and_authority_survive_model_change(self):
        first = self.box.invoke('mack_status', {})['data']
        self.store.select('replacement', 'new-digest')
        second = Toolbox(self.store.snapshot()).invoke('mack_status', {})['data']
        self.assertEqual(first['identity'], second['identity'])
        self.assertEqual(second['identity']['pronouns'], 'she/her')
        self.assertEqual(first['body'], second['body'])
        self.assertEqual(second['body']['motion_actions'], [])
        self.assertFalse(second['body']['physical_connection'])
        # A caller cannot mutate the shared identity through a returned status.
        second['identity']['name'] = 'Changed'
        self.assertEqual(self.box.status()['identity']['name'], 'Mack')

    def test_clock_reports_offset_and_source(self):
        data = self.box.invoke('local_time', {})['data']
        from datetime import datetime
        stamp = datetime.fromisoformat(data['iso'])
        self.assertIsNotNone(stamp.utcoffset())
        self.assertEqual(data['weekday'], stamp.strftime('%A'))
        self.assertIn('host clock', data['source'])

    def provider(self, replies, capabilities=None):
        provider = Ollama()
        self.requests = []
        iterator = iter(replies)

        def request(path, body=None, timeout=4):
            if path == '/api/show':
                return {'capabilities': capabilities if capabilities is not None else ['completion', 'tools']}
            if path == '/api/tags':
                return {'models': [{'name': 'local', 'digest': 'digest', 'capabilities': ['completion']}]}
            self.requests.append(copy.deepcopy(body))
            return next(iterator)

        provider.request = request
        return provider

    def test_real_tool_result_enters_followup_and_receipt_has_no_memory_content(self):
        provider = self.provider([
            response(calls=[tool_call('search_memories', {'query': 'bird'})]),
            response('Your favourite bird is a kingfisher.')])
        runtime = Runtime(self.temp.name, provider)
        result = runtime.chat({'id': 'tools-1234', 'text': 'Search your memory for my favourite bird.'})
        last = self.requests[-1]['messages'][-1]
        self.assertEqual(last['role'], 'tool')
        self.assertIn('kingfisher', json.loads(last['content'])['data']['facts'][0]['text'])
        self.assertEqual(result['tools'], [{'name': 'search_memories', 'ok': True}])
        self.assertEqual(len(runtime.store.snapshot()['history']), 1)

    def test_rejected_tool_is_reported_to_model(self):
        provider = self.provider([response(calls=[tool_call('walk', {})]), response('I cannot walk yet.')])
        provider.chat('local', [], self.box)
        outcome = json.loads(self.requests[-1]['messages'][-1]['content'])
        self.assertFalse(outcome['ok'])
        self.assertEqual(self.box.receipts, [{'name': 'walk', 'ok': False}])

    def test_models_without_tools_keep_plain_conversation(self):
        provider = self.provider([response('Hello.')], ['completion'])
        self.assertEqual(provider.chat('local', [], self.box)[0], 'Hello.')
        self.assertNotIn('tools', self.requests[0])
        self.assertEqual(self.box.receipts, [])

    def test_tools_not_advertised_cannot_execute(self):
        provider = self.provider([response(calls=[tool_call('local_time', {})])], ['completion'])
        with self.assertRaises(MackError):
            provider.chat('local', [], self.box)
        self.assertEqual(self.box.receipts, [])

    def test_repeated_tools_stop_without_recording_partial_reply(self):
        provider = self.provider([response(calls=[tool_call('local_time', {})])] * 3)
        runtime = Runtime(self.temp.name, provider)
        with self.assertRaises(MackError):
            runtime.chat({'id': 'limit-1234', 'text': 'Keep calling tools forever.'})
        self.assertEqual(len(self.requests), 3)
        self.assertEqual(runtime.store.snapshot()['history'], [])

    def test_oversized_or_malformed_batch_runs_nothing(self):
        for calls in [[tool_call('local_time', {})] * 5,
                      [tool_call('local_time', {}), {'function': {'name': 'mack_status', 'arguments': 'bad'}}]]:
            provider = self.provider([response(calls=calls)])
            with self.assertRaises(MackError):
                provider.chat('local', [], self.box)
            self.assertEqual(self.box.receipts, [])

    def test_cancel_after_inference_prevents_tools_and_followup(self):
        cancelled = threading.Event()
        provider = self.provider([response(calls=[tool_call('local_time', {})])])
        original = provider.request

        def request(path, *args, **kwargs):
            result = original(path, *args, **kwargs)
            if path == '/api/chat':
                cancelled.set()
            return result

        provider.request = request
        with self.assertRaises(MackError) as error:
            provider.chat('local', [], self.box, cancelled)
        self.assertEqual(error.exception.status, 409)
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.box.receipts, [])


if __name__ == '__main__':
    unittest.main()
