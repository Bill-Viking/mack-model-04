"""Mack's read-only tools. No file paths, SQL, network or actuator handles."""
import copy
import json
import re
from datetime import datetime
from pathlib import Path


IDENTITY = json.loads(Path(__file__).with_name('identity.json').read_text(encoding='utf-8'))


def function(name, description, properties=None, required=None):
    return {'type': 'function', 'function': {
        'name': name, 'description': description,
        'parameters': {'type': 'object', 'properties': properties or {},
                       'required': required or [], 'additionalProperties': False}}}


DEFINITIONS = [
    function('mack_status', 'Read Mack\'s current identity, body and connected capabilities. Future plans are not current abilities.'),
    function('local_time', 'Read the host computer\'s current local date, time and UTC offset. Use for current-time questions.'),
    function('search_memories', 'Search active saved facts by word overlap. Use short keywords; empty query lists up to six recent facts. This cannot save or edit memories.',
             {'query': {'type': 'string', 'maxLength': 200}}, ['query']),
]


class Toolbox:
    """One turn's immutable view of facts, with bounded results and receipts."""
    def __init__(self, state, voice_status=None):
        self.notes = copy.deepcopy(state['notes'])
        self.model = state['model']
        self.receipts = []
        self.voice_status = copy.deepcopy(voice_status or {'available': False})

    def status(self):
        return {
            'identity': copy.deepcopy(IDENTITY),
            'body': {'id': 'desktop', 'kind': 'development desktop',
                     'physical_connection': False, 'motion_actions': [], 'sensors': []},
            'inference': {'model': self.model, 'routing': 'local Ollama only'},
            'memory': {'storage': 'local SQLite', 'active_facts': len(self.notes),
                       'writes': 'explicit Remember command or Memories editor only'},
            'voice': {'synthesis': 'browser selects stock local voice or the installed reference engine',
                      'local_reference_synthesis': self.voice_status,
                      'playback_enabled': 'unknown to backend',
                      'offline_speech_input': 'not qualified'},
            'read_only_tools': [item['function']['name'] for item in DEFINITIONS],
            'service_bridges': [],
        }

    def invoke(self, name, arguments):
        if not isinstance(name, str) or name not in {d['function']['name'] for d in DEFINITIONS}:
            result = {'ok': False, 'error': 'Unknown or unavailable tool.'}
        elif not isinstance(arguments, dict):
            result = {'ok': False, 'error': 'Tool arguments must be an object.'}
        elif name == 'search_memories':
            query = arguments.get('query')
            if set(arguments) != {'query'} or not isinstance(query, str) or len(query) > 200:
                result = {'ok': False, 'error': 'Provide only query, a string of at most 200 characters.'}
            else:
                tokens = set(re.findall(r'\w+', query.lower()))
                ranked = [(len(tokens & set(re.findall(r'\w+', note['text'].lower()))), note)
                          for note in self.notes]
                matches = [note for score, note in sorted(ranked, key=lambda pair: pair[0], reverse=True)
                           if score or not tokens]
                result = {'ok': True, 'data': {
                    'facts': [{'id': note['id'], 'text': note['text']} for note in matches[:6]],
                    'matching_count': len(matches), 'returned_count': min(6, len(matches)),
                    'method': 'word overlap; no match does not prove no relevant fact exists'}}
        elif arguments:
            result = {'ok': False, 'error': 'This tool takes no arguments.'}
        elif name == 'mack_status':
            result = {'ok': True, 'data': self.status()}
        else:
            current = datetime.now().astimezone()
            result = {'ok': True, 'data': {'iso': current.isoformat(),
                       'weekday': current.strftime('%A'), 'zone': current.tzname(),
                       'source': 'host clock; clock accuracy is not independently verified'}}
        # No argument text or memory content in the user-facing receipt.
        self.receipts.append({'name': name if isinstance(name, str) else 'invalid', 'ok': result['ok']})
        return result
