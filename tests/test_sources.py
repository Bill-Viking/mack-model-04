"""Check provenance failures and checkout preservation without a network."""

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("sources", Path(__file__).parents[1] / "tools/sources.py")
sources = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sources)


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.file = self.root / "vendor/example/part.txt"
        self.file.parent.mkdir(parents=True)
        self.file.write_bytes(b"original\n")
        self.repo = {"id": "example", "imports": [{
            "path": "vendor/example/part.txt", "bytes": 9,
            "sha256": hashlib.sha256(b"original\n").hexdigest(),
        }]}
        self.data = {"repositories": [self.repo]}

    def test_clean_snapshot(self):
        self.assertEqual(sources.check_imports(self.root, self.data), (1, []))

    def test_same_length_edit_detected(self):
        self.file.write_bytes(b"modified\n")
        self.assertIn("Changed:", sources.check_imports(self.root, self.data)[1][0])

    def test_missing_file_detected(self):
        self.file.unlink()
        self.assertIn("Missing:", sources.check_imports(self.root, self.data)[1][0])

    def test_unrecorded_file_detected(self):
        self.file.with_name("extra.txt").write_text("untracked import")
        self.assertIn("Unrecorded:", sources.check_imports(self.root, self.data)[1][0])

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            sources.confined(self.root, "vendor/../../outside", "vendor")

    def test_symlink_rejected(self):
        self.file.unlink()
        self.file.symlink_to(self.root / "outside")
        with self.assertRaises(ValueError):
            sources.check_imports(self.root, self.data)

    def test_dirty_or_wrong_revision_is_preserved(self):
        path = self.root / "sources/example"
        path.mkdir(parents=True)
        def git(*args):
            return subprocess.check_output(
                ["git", "-c", "core.hooksPath=/dev/null", *args],
                cwd=path, text=True, stderr=subprocess.DEVNULL,
            ).strip()
        git("init", "--quiet", "--template=")
        git("remote", "add", "origin", "https://github.com/example/example.git")
        (path / "file.txt").write_text("first")
        git("add", "file.txt")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "--quiet", "-m", "fixture")
        head = git("rev-parse", "HEAD")
        repo = {"id": "example", "fetchable": True, "directory": "sources/example",
                "url": "https://github.com/example/example.git", "revision": head}
        self.assertIn("already present", sources.fetch_checkout(self.root, repo))
        (path / "file.txt").write_text("keep my edit")
        with self.assertRaisesRegex(ValueError, "Dirty"):
            sources.fetch_checkout(self.root, repo)
        self.assertEqual((path / "file.txt").read_text(), "keep my edit")
        (path / "file.txt").write_text("first")
        repo["revision"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "Revision differs"):
            sources.fetch_checkout(self.root, repo)
        self.assertEqual(git("rev-parse", "HEAD"), head)


if __name__ == "__main__":
    unittest.main()
