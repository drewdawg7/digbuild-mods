#!/usr/bin/env python3
"""Publish what digbuild-sync reads: a per-jar manifest, and the jars themselves.

The pack zip cannot serve this. A client three mods behind should fetch three
jars, not 466 MB, so every jar needs its own stable URL. Both live on GitHub
Releases -- the same host the wiki's install page already points at, so there is
nothing new to run and no second place for a player's download to break.

Two pieces:

  mod-store       one long-lived release holding every jar, named by content
                  (<sha1>.jar). Content-addressed so an upload is idempotent:
                  a publish only transfers the jars that actually changed, and
                  two mods that happen to share a filename cannot collide.
  mods-manifest.tsv  attached to each new release, so /latest/download/ resolves
                  it with no API call and no version pinned in the client jar.

The store is never pruned. It grows by the size of each changed jar, which is
small next to a release a run, and pruning risks 404ing a client that fetched
the manifest moments before.

Needs `gh` authenticated -- GH_TOKEN in CI.

  python3 scripts/publish_manifest.py            # upload, then write the tsv
  python3 scripts/publish_manifest.py --dry-run  # write the tsv, upload nothing
"""
import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sync_mods import EXCLUDE_PREFIXES  # noqa: E402  (one list, one place)

MODS = pathlib.Path("mods")
OUT = pathlib.Path("mods-manifest.tsv")

STORE_TAG = "mod-store"
STORE_TITLE = "Mod store"
STORE_NOTES = (
    "Individual mod jars, named by SHA-1, for the in-game updater to fetch.\n"
    "Not a release to download -- players want the zip on the newest release.\n"
)

# Bumped only when the format changes in a way older clients cannot read. They
# refuse the manifest and leave mods/ alone, which is why this is not silent.
FORMAT_VERSION = 1


def repo():
    """owner/name, from the CI environment or from the checkout's origin.

    Read rather than hardcoded so a fork publishes against itself -- a manifest
    is a list of URLs, and one pointing at someone else's repo is a fork that
    silently updates its players from upstream.
    """
    slug = os.environ.get("GITHUB_REPOSITORY")
    if slug:
        return slug
    url = subprocess.run(["git", "remote", "get-url", "origin"],
                         capture_output=True, text=True, check=True).stdout.strip()
    # Both remote spellings end in owner/name: git@host:owner/name.git and
    # https://host/owner/name.git.
    return "/".join(url.removesuffix(".git").replace(":", "/").split("/")[-2:])


def gh(*args, check=True):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def sha1(path):
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def published_jars():
    """The jars a player gets -- the same set the zip carries."""
    return sorted(
        p for p in MODS.glob("*.jar")
        if not p.name.lower().startswith(EXCLUDE_PREFIXES)
    )


def ensure_store():
    if gh("release", "view", STORE_TAG, check=False).returncode == 0:
        return
    print(f"creating the {STORE_TAG} release")
    gh("release", "create", STORE_TAG, "--title", STORE_TITLE, "--notes", STORE_NOTES)


def store_assets():
    r = gh("release", "view", STORE_TAG, "--json", "assets")
    return {a["name"] for a in json.loads(r.stdout)["assets"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="write the tsv, upload nothing")
    a = ap.parse_args(argv)

    jars = published_jars()
    if not jars:
        # Same guard sync_mods.py carries: an empty set here would publish a
        # manifest that tells every client its whole mods folder was dropped.
        print("refusing to continue: no jars to publish", file=sys.stderr)
        return 1

    slug = repo()
    base = f"https://github.com/{slug}/releases/download/{STORE_TAG}"

    digests = {jar: sha1(jar) for jar in jars}

    if not a.dry_run:
        ensure_store()
        have = store_assets()
        missing = [(jar, d) for jar, d in digests.items() if f"{d}.jar" not in have]
        print(f"{len(jars)} jars, {len(missing)} to upload")

        # Uploaded under the content name, so the asset a manifest row points at
        # can never be quietly replaced by a different build.
        with tempfile.TemporaryDirectory() as tmp:
            for jar, digest in missing:
                staged = pathlib.Path(tmp) / f"{digest}.jar"
                shutil.copy(jar, staged)
                print(f"  + {jar.name} -> {digest}.jar")
                gh("release", "upload", STORE_TAG, str(staged), "--clobber")
    else:
        print(f"{len(jars)} jars (dry run, nothing uploaded)")

    rows = [f"#digbuild-sync {FORMAT_VERSION}"]
    for jar in jars:
        digest = digests[jar]
        rows.append("\t".join([digest, str(jar.stat().st_size), jar.name, f"{base}/{digest}.jar"]))
    OUT.write_text("\n".join(rows) + "\n")
    print(f"wrote {OUT} ({len(jars)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
