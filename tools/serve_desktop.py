#!/usr/bin/env python3
"""Mack's loopback desktop and local AI/memory API. No third-party Python packages."""
import argparse
import hashlib
import json
import secrets
import sqlite3
import sys
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software'))
from mack.runtime import MackError, Runtime
from mack.voice import VoiceService
from mack.listening import ListeningService, MAX_BYTES
DESKTOP = ROOT / 'software' / 'desktop'
IDENTITY = hashlib.sha256(str(ROOT).encode()).hexdigest()[:16]
ASSETS = {
    '/': ('index.html', 'text/html; charset=utf-8'),
    '/index.html': ('index.html', 'text/html; charset=utf-8'),
    '/styles.css': ('styles.css', 'text/css; charset=utf-8'),
    '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
    '/model.mjs': ('model.mjs', 'text/javascript; charset=utf-8'),
    '/service.mjs': ('service.mjs', 'text/javascript; charset=utf-8'),
    '/voice.mjs': ('voice.mjs', 'text/javascript; charset=utf-8'),
    '/listening.mjs': ('listening.mjs', 'text/javascript; charset=utf-8'),
    '/microphone-worklet.js': ('microphone-worklet.js', 'text/javascript; charset=utf-8'),
}


class Handler(BaseHTTPRequestHandler):
    def allowed(self, token=False):
        hosts = {'127.0.0.1:' + str(self.server.server_port), 'localhost:' + str(self.server.server_port)}
        if self.headers.get('Host') not in hosts:
            return False
        if self.headers.get('Origin') not in (None, *('http://' + h for h in hosts)):
            return False
        if self.headers.get('Sec-Fetch-Site') == 'cross-site':
            # A link may open the public shell. Cross-site API and asset reads
            # remain forbidden, including bootstrap's private state and token.
            navigation = (not token and self.command == 'GET'
                          and urlsplit(self.path).path in ('/', '/index.html')
                          and self.headers.get('Sec-Fetch-Mode') == 'navigate'
                          and self.headers.get('Sec-Fetch-Dest') == 'document')
            if not navigation:
                return False
        return not token or secrets.compare_digest(self.headers.get('X-Mack-Token', ''), getattr(self.server, 'token', 'unavailable'))

    def json_response(self, payload, code=200, head=False):
        data = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        if not head:
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def do_GET(self):
        self.respond(False)

    def do_HEAD(self):
        self.respond(True)

    def respond(self, head_only):
        if not self.allowed():
            return self.json_response({'error': 'Only this local Mack desktop may connect.'}, 403, head_only)
        path = urlsplit(self.path).path
        if path.startswith('/api/'):
            if path != '/api/bootstrap' and not self.allowed(token=True):
                return self.json_response({'error': 'Reload Mack to reconnect.'}, 403, head_only)
            if not hasattr(self.server, 'runtime'):
                return self.json_response({'error': 'Runtime unavailable.'}, 503, head_only)
            try:
                if path == '/api/bootstrap':
                    return self.json_response({'token': self.server.token, 'state': self.server.runtime.store.snapshot()}, head=head_only)
                if path == '/api/state':
                    return self.json_response(self.server.runtime.store.snapshot(), head=head_only)
                if path == '/api/models':
                    return self.json_response(self.server.runtime.health(), head=head_only)
                if path == '/api/voice/status':
                    return self.json_response(self.server.voice.status(), head=head_only)
                if path == '/api/listening/status':
                    return self.json_response(self.server.listening.status(), head=head_only)
                return self.json_response({'error': 'Unknown Mack service.'}, 404, head_only)
            except (sqlite3.Error, OSError):
                return self.json_response({'error': 'Memory storage is unavailable. Existing data has been kept.'}, 503, head_only)
        if path == '/__mack__':
            data = json.dumps({'app': 'mack-desktop', 'version': '0.3', 'identity': IDENTITY}).encode()
            kind = 'application/json'
        elif path in ASSETS:
            name, kind = ASSETS[path]
            try:
                data = (DESKTOP / name).read_bytes()
            except OSError:
                self.send_error(500, 'A desktop asset could not be read')
                return
        else:
            self.send_error(404, 'Not a Mack desktop asset')
            return
        self.send_response(200)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def do_POST(self):
        if not self.allowed(token=True):
            return self.json_response({'error': 'Reload Mack to reconnect.'}, 403)
        try:
            path = urlsplit(self.path).path
            length = int(self.headers.get('Content-Length', '0'))
            if path in ('/api/listening/transcribe', '/api/listening/preview'):
                if not 44 < length <= MAX_BYTES:
                    raise MackError('Recording is empty or exceeds 60 seconds.', 413)
                if self.headers.get('Content-Type') != 'audio/wav':
                    raise MackError('Expected local WAV audio.', 415)
                audio = self.rfile.read(length)
                if len(audio) != length:
                    raise MackError('Recording upload was interrupted.')
                return self.json_response(self.server.listening.transcribe(audio, self.headers.get('X-Mack-Request-Id'),
                                                                           preview=path.endswith('/preview')))
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                return self.json_response({'error': 'JSON required.'}, 415)
            if not 0 < length <= 500_000:
                raise MackError('Request is empty or too large.', 413)
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise MackError('A JSON object is required.')
            runtime = self.server.runtime
            path = urlsplit(self.path).path
            if path == '/api/listening/cancel':
                self.server.listening.cancel(payload.get('id'))
                return self.json_response({'ok': True})
            if path == '/api/conversation/search':
                return self.json_response({'exchanges': runtime.store.conversations(payload.get('query', ''), payload.get('offset', 0), payload.get('trashed', False))})
            if path == '/api/voice/speak':
                audio, seconds = self.server.voice.synthesize(payload)
                self.send_response(200)
                self.send_header('Content-Type', 'audio/wav')
                self.send_header('Content-Length', str(len(audio)))
                self.send_header('Cache-Control', 'no-store')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('X-Mack-Voice-Seconds', str(seconds))
                self.end_headers()
                try:
                    self.wfile.write(audio)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return
            if path == '/api/voice/cancel':
                self.server.voice.cancel(payload.get('id'))
                return self.json_response({'ok': True})
            if path == '/api/chat':
                return self.json_response(runtime.chat(payload))
            if path == '/api/cancel':
                runtime.cancel(payload.get('id', ''))
                return self.json_response({'ok': True})
            if path == '/api/memory/save':
                runtime.change(runtime.store.save, payload.get('text'), payload.get('id'))
            elif path == '/api/memory/move':
                runtime.change(runtime.store.move, payload.get('id'), payload.get('trashed'))
            elif path == '/api/memory/import':
                runtime.change(runtime.store.import_browser, payload)
            elif path == '/api/model':
                runtime.select(payload.get('model'))
            elif path == '/api/conversation/new':
                runtime.change(runtime.store.new_conversation)
            elif path == '/api/conversation/move':
                runtime.change(runtime.store.move_conversation, payload.get('id'), payload.get('trashed'))
            else:
                raise MackError('Unknown Mack service.', 404)
            return self.json_response(runtime.store.snapshot())
        except MackError as error:
            self.json_response({'error': str(error)}, error.status)
        except (ValueError, TypeError, KeyError):
            self.json_response({'error': 'Invalid request.'}, 400)
        except (sqlite3.Error, OSError):
            self.json_response({'error': 'Memory storage is unavailable. Your existing data has been kept.'}, 503)

    def log_message(self, *_):
        pass


def running_mack(url):
    try:
        with urllib.request.urlopen(url + '__mack__', timeout=1) as response:
            payload = json.load(response)
            return payload.get('app') == 'mack-desktop' and payload.get('identity') == IDENTITY and payload.get('version') == '0.3'
    except (OSError, ValueError, urllib.error.URLError):
        return False


def main():
    parser = argparse.ArgumentParser(description='Open Mack’s desktop on this Mac.')
    parser.add_argument('--port', type=int, default=9844)
    parser.add_argument('--no-open', action='store_true', help='Serve without opening a browser')
    parser.add_argument('--data-dir', type=Path, default=ROOT / 'runtime' / 'mack', help='Private memory directory; back up this folder')
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port must be between 0 and 65535')
    url = 'http://127.0.0.1:' + str(args.port) + '/'
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as error:
        if running_mack(url):
            print('Mack is already running at ' + url, flush=True)
            if not args.no_open:
                webbrowser.open(url)
            return 0
        print('Could not start Mack on port ' + str(args.port) + ': ' + str(error), file=sys.stderr)
        print('Choose a free port with --port. Keep the same address to access your saved browser notes.', file=sys.stderr)
        return 1
    url = 'http://127.0.0.1:' + str(server.server_port) + '/'
    server.runtime = Runtime(args.data_dir)
    server.voice = VoiceService(ROOT)
    server.listening = ListeningService(ROOT)
    server.runtime.voice_status = server.voice.status
    server.runtime.listening_status = server.listening.status
    server.token = secrets.token_urlsafe(32)
    print('Mack is ready: ' + url, flush=True)
    print('Keep this window open. Control-C stops the desktop server.', flush=True)
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nMack’s desktop server stopped.', flush=True)
    finally:
        server.voice.close()
        server.listening.close()
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
