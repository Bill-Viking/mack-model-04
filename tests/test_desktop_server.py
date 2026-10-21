"""The loopback API protects personal data and serves only allowlisted assets."""
import importlib.util
import http.client
import json
import secrets
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer

spec = importlib.util.spec_from_file_location('serve_desktop', Path(__file__).resolve().parents[1] / 'tools' / 'serve_desktop.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DesktopServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), module.Handler)
        cls.temp = tempfile.TemporaryDirectory()
        cls.server.runtime = module.Runtime(cls.temp.name)
        cls.server.token = secrets.token_urlsafe(32)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def test_assets_load_with_right_types(self):
        for path, kind in [('/', 'text/html'), ('/app.js', 'text/javascript'), ('/model.mjs', 'text/javascript'), ('/styles.css', 'text/css')]:
            with urllib.request.urlopen(self.url + path) as response:
                self.assertEqual(response.status, 200)
                self.assertIn(kind, response.headers['Content-Type'])
                self.assertIn("connect-src 'self'", response.headers['Content-Security-Policy'])
                self.assertTrue(response.read())

    def test_repository_and_traversal_are_not_served(self):
        for path in ['/STATUS.md', '/.git/config', '/../STATUS.md', '/%2e%2e/STATUS.md', '/software/', '/sources/']:
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(self.url + path)
            self.assertEqual(error.exception.code, 404)

    def test_writes_require_token(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(urllib.request.Request(self.url + '/', data=b'test'))
        self.assertEqual(error.exception.code, 403)

    def test_personal_state_requires_token(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(self.url + '/api/state')
        self.assertEqual(error.exception.code, 403)

    def test_cross_site_and_rebound_hosts_are_rejected(self):
        for headers in [{'Origin': 'https://example.com'}, {'Host': 'example.com'}, {'Sec-Fetch-Site': 'cross-site'}]:
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(urllib.request.Request(self.url + '/api/bootstrap', headers=headers))
            self.assertEqual(error.exception.code, 403)

    def test_bootstrap_and_memory_round_trip(self):
        with urllib.request.urlopen(self.url + '/api/bootstrap') as response:
            bootstrap = json.load(response)
        request = urllib.request.Request(self.url + '/api/memory/save',
                    data=json.dumps({'text': 'Server test memory'}).encode(),
                    headers={'Content-Type': 'application/json', 'X-Mack-Token': bootstrap['token']})
        with urllib.request.urlopen(request) as response:
            state = json.load(response)
        self.assertIn('Server test memory', [n['text'] for n in state['notes']])

    def test_invalid_payloads_fail_without_writes(self):
        for data, expected in [(b'[]', 400), (b'{', 400)]:
            request = urllib.request.Request(self.url + '/api/memory/save', data=data,
                    headers={'Content-Type': 'application/json', 'X-Mack-Token': self.server.token})
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(request)
            self.assertEqual(error.exception.code, expected)

    def test_oversized_body_is_rejected_before_upload(self):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=2)
        try:
            connection.putrequest('POST', '/api/memory/save')
            connection.putheader('Content-Type', 'application/json')
            connection.putheader('X-Mack-Token', self.server.token)
            connection.putheader('Content-Length', '500001')
            connection.endheaders()
            self.assertEqual(connection.getresponse().status, 413)
        finally:
            connection.close()

    def test_existing_instance_identity(self):
        self.assertTrue(module.running_mack(self.url + '/'))


if __name__ == '__main__':
    unittest.main()
