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
DESKTOP = ROOT / 'software' / 'desktop'
IDENTITY = hashlib.sha256(str(ROOT).encode()).hexdigest()[:16]
ASSETS = {
    '/': ('index.html', 'text/html; charset=utf-8'),
    '/index.html': ('index.html', 'text/html; charset=utf-8'),
    '/styles.css': ('styles.css', 'text/css; charset=utf-8'),
    '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
    '/model.mjs': ('model.mjs', 'text/javascript; charset=utf-8'),
    '/service.mjs': ('service.mjs', 'text/javascript; charset=utf-8'),
}


class Handler(BaseHTTPRequestHandler):
    def allowed(self, token=False):
        hosts = {'127.0.0.1:' + str(self.server.server_port), 'localhost:' + str(self.server.server_port)}
        if self.headers.get('Host') not in hosts:
            return False
        if self.headers.get('Origin') not in (None, *('http://' + h for h in hosts)):
            return False
        if self.headers.get('Sec-Fetch-Site') == 'cross-site':
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
                return self.json_response({'error': 'Unknown Mack service.'}, 404, head_only)
            except (sqlite3.Error, OSError):
                return self.json_response({'error': 'Memory storage is unavailable. Existing data has been kept.'}, 503, head_only)
        if path == '/__mack__':
            data = json.dumps({'app': 'mack-desktop', 'version': '0.2', 'identity': IDENTITY}).encode()
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
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def do_POST(self):
        if not self.allowed(token=True):
            return self.json_response({'error': 'Reload Mack to reconnect.'}, 403)
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.json_response({'error': 'JSON required.'}, 415)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 500_000:
                raise MackError('Request is empty or too large.', 413)
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise MackError('A JSON object is required.')
            runtime = self.server.runtime
            path = urlsplit(self.path).path
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
            return payload.get('app') == 'mack-desktop' and payload.get('identity') == IDENTITY and payload.get('version') == '0.2'
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
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
