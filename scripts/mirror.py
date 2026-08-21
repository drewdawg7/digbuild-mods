#!/usr/bin/env python3
"""Recursively mirror a directory off the game server into a local tree.

The client API has no bulk read, so anything that wants to grep across many
server files ends up making one request per file. Doing that inline, twice,
is what this exists to stop: mirror once into .cache/, then work locally.

  python3 scripts/mirror.py /config .cache/config
  python3 scripts/mirror.py /config .cache/config --refresh

Re-runs skip files whose size already matches, so a second pass over /config
costs one listing per directory and nothing else. `--refresh` re-downloads
everything; use it after changing configs on the server.

Text files come back through files/contents (one request). Anything the API
refuses to serve inline -- binaries, and files over its inline size cap -- is
fetched through the signed-url download path instead.
"""
import argparse
import json
import pathlib
import sys
import urllib.error

from ptero import Panel, PteroError

# Directories that are large, binary, or irrelevant to reading configuration.
# spark dumps in particular are megabytes each and carry the JVM command line.
SKIP_DIRS = {"spark", "jei", "dynmapblockscan", "__pycache__"}


def mirror(panel, remote, local, refresh=False, skip=SKIP_DIRS, depth=0):
    """Copy `remote` into `local`. Returns (fetched, skipped, failed)."""
    local = pathlib.Path(local)
    local.mkdir(parents=True, exist_ok=True)
    fetched = skipped = failed = 0

    for entry in sorted(panel.list_dir(remote), key=lambda e: e["name"]):
        name = entry["name"]
        rpath = f"{remote.rstrip('/')}/{name}"
        lpath = local / name

        if Panel.is_dir(entry):
            if name in skip:
                continue
            sub = mirror(panel, rpath, lpath, refresh, skip, depth + 1)
            fetched, skipped, failed = (a + b for a, b in zip((fetched, skipped, failed), sub))
            continue

        # Size is the only cheap change signal -- the listing's mtime moves on
        # every server boot whether or not the bytes changed.
        if not refresh and lpath.exists() and lpath.stat().st_size == entry["size"]:
            skipped += 1
            continue

        try:
            body = panel.read_file(rpath)
            # files/contents honours content-type, so .json configs arrive
            # already parsed. Re-serialise rather than spend a second request
            # on the download path -- JSON has no comments to lose.
            if not isinstance(body, str):
                body = json.dumps(body, indent=2)
            lpath.write_text(body, encoding="utf8")
            fetched += 1
        except (PteroError, UnicodeError):
            try:
                panel.download(rpath, lpath)
                fetched += 1
            # The signed-url fetch is a plain urlopen, so its failures surface
            # as HTTPError rather than PteroError.
            except (PteroError, urllib.error.HTTPError, OSError) as e:
                print(f"  ! {rpath}: {e}", file=sys.stderr)
                failed += 1

    if depth == 0:
        print(f"{local}: {fetched} fetched, {skipped} unchanged, {failed} failed")
    return fetched, skipped, failed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("remote", help="server path, e.g. /config")
    ap.add_argument("local", help="local destination directory")
    ap.add_argument("--refresh", action="store_true", help="re-download unchanged files")
    ap.add_argument("--all", action="store_true", help="do not skip the usual noisy dirs")
    a = ap.parse_args(argv)

    _, _, failed = mirror(
        Panel(), a.remote, a.local, refresh=a.refresh, skip=set() if a.all else SKIP_DIRS
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
