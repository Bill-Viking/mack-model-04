#!/usr/bin/env python3
"""Verify vendored snapshots or restore pinned public reference checkouts.

Standard library + Git only. Never runs upstream installers or runtime code.
Existing checkouts are inspected, never reset or updated automatically.
"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def confined(root, relative, prefix):
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or path.parts[:1] != (prefix,):
        raise ValueError(f"Invalid {prefix} path: {relative}")
    target = root / relative
    if not target.resolve().is_relative_to(root.resolve() / prefix):
        raise ValueError(f"Path escapes {prefix}: {relative}")
    if any(p.is_symlink() for p in [target, *target.parents] if p != root.parent):
        raise ValueError(f"Symlink not permitted: {relative}")
    return target


def read_manifest(root):
    data = json.loads((root / "SOURCES.json").read_text())
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported source manifest version")
    ids, paths = set(), set()
    for repo in data["repositories"]:
        if repo["id"] in ids or not re.fullmatch(r"[a-z0-9-]+", repo["id"]):
            raise ValueError("Duplicate or invalid source ID")
        ids.add(repo["id"])
        if not re.fullmatch(r"[0-9a-f]{40}", repo["revision"]):
            raise ValueError(f"Full Git revision required: {repo['id']}")
        if repo["fetchable"]:
            confined(root, repo["directory"], "sources")
            if not re.fullmatch(r"https://github\.com/[\w.-]+/[\w.-]+\.git", repo["url"]):
                raise ValueError(f"Unexpected fetch URL: {repo['id']}")
        for item in repo["imports"]:
            confined(root, item["path"], "vendor")
            if item["path"] in paths:
                raise ValueError(f"Duplicate import: {item['path']}")
            paths.add(item["path"])
            if not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
                raise ValueError(f"Invalid SHA-256: {item['path']}")
    return data


def check_imports(root, data):
    errors, expected, count = [], set(), 0
    for repo in data["repositories"]:
        for item in repo["imports"]:
            path = confined(root, item["path"], "vendor")
            expected.add(path)
            count += 1
            if not path.is_file():
                errors.append(f"Missing: {item['path']}")
                continue
            content = path.read_bytes()
            if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
                errors.append(f"Changed: {item['path']}")
    # SOURCE.md and the vendor index are our annotations, not upstream copies.
    annotations = {root / "vendor/README.md"}
    annotations.update(root / "vendor" / r["id"] / "SOURCE.md" for r in data["repositories"])
    for path in (root / "vendor").rglob("*"):
        if path.is_symlink() or (path.is_file() and path not in expected | annotations):
            errors.append(f"Unrecorded: {path.relative_to(root)}")
    return count, errors


def git(*args, cwd):
    return subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", *args], cwd=cwd,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=True, timeout=120,
    ).stdout.strip()


def inspect_checkout(path, repo):
    if not (path / ".git").exists():
        raise ValueError(f"Not a standalone checkout; left untouched: {path}")
    if Path(git("rev-parse", "--show-toplevel", cwd=path)).resolve() != path.resolve():
        raise ValueError(f"Unexpected repository root: {path}")
    if git("remote", "get-url", "origin", cwd=path) != repo["url"]:
        raise ValueError(f"Origin differs; left untouched: {path}")
    if git("status", "--porcelain", cwd=path):
        raise ValueError(f"Dirty checkout; left untouched: {path}")
    if git("rev-parse", "HEAD", cwd=path) != repo["revision"]:
        raise ValueError(f"Revision differs; left untouched: {path}")


def fetch_checkout(root, repo):
    if not repo["fetchable"]:
        return f"{repo['id']}: local-only reference; tracked snapshot already included"
    target = confined(root, repo["directory"], "sources")
    if target.exists():
        inspect_checkout(target, repo)
        return f"{repo['id']}: pinned checkout already present"
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{repo['id']}-", dir=target.parent) as temp:
        stage = Path(temp) / "checkout"
        stage.mkdir()
        git("init", "--quiet", "--template=", cwd=stage)
        git("remote", "add", "origin", repo["url"], cwd=stage)
        git("fetch", "--quiet", "--no-tags", "--depth=1", "origin", repo["revision"], cwd=stage)
        git("checkout", "--quiet", "--detach", repo["revision"], cwd=stage)
        inspect_checkout(stage, repo)
        # rename refuses a non-empty destination; do not erase an existing checkout.
        if target.exists():
            raise ValueError(f"Destination appeared; left untouched: {target}")
        stage.rename(target)
    return f"{repo['id']}: restored {repo['revision']}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "fetch"), nargs="?", default="check")
    parser.add_argument("--only", help="Restore just this source ID (fetch only)")
    args = parser.parse_args()
    try:
        data = read_manifest(ROOT)
        if args.only and args.action != "fetch":
            parser.error("--only applies to fetch")
        if args.action == "check":
            count, errors = check_imports(ROOT, data)
            for error in errors:
                print(error)
            print(f"{count} imported files checked; {len(errors)} problems")
            return int(bool(errors))
        chosen = [r for r in data["repositories"] if not args.only or r["id"] == args.only]
        if not chosen:
            parser.error("Unknown source ID")
        for repo in chosen:
            print(fetch_checkout(ROOT, repo))
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(f"Source operation failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
