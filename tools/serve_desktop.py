#!/usr/bin/env python3
"""Serve only Mack's desktop assets on loopback. No packages or network services."""
import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = ROOT / 'software' / 'desktop'
IDENTITY = hashlib.sha256(str(ROOT).encode()).hexdigest()[:16]
ASSETS = {
    '/': ('index.html', 'text/html; charset=utf-8'),
    '/index.html': ('index.html', 'text/html; charset=utf-8'),
    '/styles.css': ('styles.css', 'text/css; charset=utf-8'),
    '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
    '/model.mjs': ('model.mjs', 'text/javascript; charset=utf-8'),
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond(False)

    def do_HEAD(self):
        self.respond(True)

    def respond(self, head_only):
        path = urlsplit(self.path).path
        if path == '/__mack__':
            data = json.dumps({'app': 'mack-desktop', 'version': '0.1', 'identity': IDENTITY}).encode()
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
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def log_message(self, *_):
        pass


def running_mack(url):
    try:
        with urllib.request.urlopen(url + '__mack__', timeout=1) as response:
            payload = json.load(response)
            return payload.get('app') == 'mack-desktop' and payload.get('identity') == IDENTITY
    except (OSError, ValueError, urllib.error.URLError):
        return False


def main():
    parser = argparse.ArgumentParser(description='Open Mack’s desktop on this Mac.')
    parser.add_argument('--port', type=int, default=9844)
    parser.add_argument('--no-open', action='store_true', help='Serve without opening a browser')
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
