"""The desktop must never serve the repository, private files, or write requests."""
import importlib.util
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
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_assets_load_with_right_types(self):
        for path, kind in [('/', 'text/html'), ('/app.js', 'text/javascript'), ('/model.mjs', 'text/javascript'), ('/styles.css', 'text/css')]:
            with urllib.request.urlopen(self.url + path) as response:
                self.assertEqual(response.status, 200)
                self.assertIn(kind, response.headers['Content-Type'])
                self.assertIn("connect-src 'none'", response.headers['Content-Security-Policy'])
                self.assertTrue(response.read())

    def test_repository_and_traversal_are_not_served(self):
        for path in ['/STATUS.md', '/.git/config', '/../STATUS.md', '/%2e%2e/STATUS.md', '/software/', '/sources/']:
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(self.url + path)
            self.assertEqual(error.exception.code, 404)

    def test_no_post_endpoint(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(urllib.request.Request(self.url + '/', data=b'test'))
        self.assertEqual(error.exception.code, 501)

    def test_existing_instance_identity(self):
        self.assertTrue(module.running_mack(self.url + '/'))


if __name__ == '__main__':
    unittest.main()
