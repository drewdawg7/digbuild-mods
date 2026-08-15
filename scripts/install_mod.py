#!/usr/bin/env python3
"""Resolve a mod from Modrinth, check it against the server's JVM, upload it.

The bytecode check is the point of this script. Forge aborts the entire boot if
any mod's class files are newer than the runtime, so a jar built for Java 21
dropped into a Java 17 server takes the whole thing down until someone deletes
it by hand. Verify before uploading, never after.

  python3 scripts/install_mod.py spark --dry-run
  python3 scripts/install_mod.py spark
  python3 scripts/install_mod.py spark --version 1.10.53
"""
import argparse
import io
import json
import pathlib
import sys
import urllib.parse
import urllib.request
import zipfile

from ptero import Panel

MODRINTH = "https://api.modrinth.com/v2"
UA = "digbuild-tools (github.com/drewdawg7/digbuild)"

LOADER = "forge"
MC = "1.20.1"

# Class-file major version -> Java release. 61 == Java 17.
CLASS_MAJOR_TO_JAVA = {52: 8, 55: 11, 60: 16, 61: 17, 62: 18, 63: 19, 64: 20, 65: 21}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def resolve(slug, version=None, loader=LOADER, mc=MC):
    """Newest published build matching loader + game version."""
    q = urllib.parse.urlencode({
        "loaders": json.dumps([loader]),
        "game_versions": json.dumps([mc]),
    })
    versions = _get(f"{MODRINTH}/project/{slug}/version?{q}")
    if not versions:
        raise SystemExit(f"no {slug} build for {loader} {mc}")
    if version:
        versions = [v for v in versions if v["version_number"] == version]
        if not versions:
            raise SystemExit(f"{slug} {version} not found for {loader} {mc}")
    v = versions[0]  # Modrinth returns newest first
    f = next(f for f in v["files"] if f["primary"])
    return {
        "name": f["filename"],
        "url": f["url"],
        "sha512": f["hashes"]["sha512"],
        "version": v["version_number"],
        "published": v["date_published"][:10],
    }


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def max_class_version(blob):
    """Highest class-file major version in the jar -- the Java release it needs."""
    top = 0
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for n in z.namelist():
            if not n.endswith(".class"):
                continue
            head = z.read(n)[:8]
            if len(head) >= 8 and head[:4] == b"\xca\xfe\xba\xbe":
                top = max(top, int.from_bytes(head[6:8], "big"))
    return top


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("slug", help="Modrinth project slug, e.g. spark")
    ap.add_argument("--version", help="pin an exact version_number")
    ap.add_argument("--loader", default=LOADER)
    ap.add_argument("--mc", default=MC)
    ap.add_argument("--dry-run", action="store_true", help="resolve and verify, do not upload")
    ap.add_argument("--out", default=None, help="also keep the jar here")
    a = ap.parse_args(argv)

    info = resolve(a.slug, a.version, a.loader, a.mc)
    print(f"resolved  {info['name']}")
    print(f"version   {info['version']}  ({info['published']})")

    blob = fetch(info["url"])
    import hashlib
    got = hashlib.sha512(blob).hexdigest()
    if got != info["sha512"]:
        raise SystemExit("sha512 mismatch -- refusing to upload")
    print(f"sha512    ok ({len(blob) / 1024:.0f} KiB)")

    p = Panel()
    needs = max_class_version(blob)
    have = p.java_major()
    needs_java = CLASS_MAJOR_TO_JAVA.get(needs, needs)
    print(f"bytecode  class major {needs} (Java {needs_java}); server runs Java {have}")
    if have and needs_java != needs and needs_java > have:
        raise SystemExit(
            f"refusing: needs Java {needs_java}, server is Java {have}. "
            "Uploading this would break the next boot."
        )

    if a.out:
        pathlib.Path(a.out).write_bytes(blob)
        print(f"saved     {a.out}")

    if a.dry_run:
        print("\ndry run -- nothing uploaded")
        return 0

    tmp = pathlib.Path(a.out) if a.out else pathlib.Path("/tmp") / info["name"]
    if not a.out:
        tmp.write_bytes(blob)
    print(f"uploading {info['name']} -> /mods")
    print("status   ", p.upload(tmp, "/mods"))
    print("\nnot live until the server restarts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
