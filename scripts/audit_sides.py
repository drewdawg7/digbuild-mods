#!/usr/bin/env python3
"""Which jars in /mods do their authors say have no server-side role?

A client-only mod on a dedicated server is dead weight in the JVM, and worse,
it is invisible in a dependency graph: nothing server-side declares it, so it
reads as orphaned and gets deleted -- which is how Searchables went missing and
took Controlling down with it on every client that trusted the pack.

Do not try to infer this from the jar. mods.toml has no client-only flag (`side`
appears only inside dependency blocks, where a client library declares "BOTH"
like everything else), and every bytecode proxy for it is wrong in a way that is
not obvious until it is checked:

  - "mostly net.minecraft.client references" exonerates Searchables, which is
    41 classes of generic search API and only 7.3% client.
  - "no data/ and no registry calls" flags ferritecore, alltheleaks, Clumps,
    FastFurnace and our own tickpatches, because optimisation mods work purely
    by mixin and have neither.

The authors already publish the answer. Modrinth carries per-project environment
metadata -- client_side/server_side, superseded by `environment` -- and jars map
to projects exactly by SHA1, so there is no name matching to get wrong.

Jars not on Modrinth (CurseForge-only releases) cannot be resolved this way and
are reported as undetermined rather than guessed at.

  python3 scripts/audit_sides.py
  python3 scripts/audit_sides.py --all       # every jar, including both-sided
"""
import argparse
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from ptero import Panel, PteroError

MODRINTH = "https://api.modrinth.com/v2"
UA = "digbuild-tools (github.com/drewdawg7/digbuild)"
CACHE = pathlib.Path(__file__).resolve().parent.parent / ".cache" / "sides"
WORKERS = 6

# Server-only by design and already excluded from the player pack.
SERVER_ONLY = ("digbuild-modsync", "digbuild-heappatch", "squaremap", "spark")

# server_side values that mean the dedicated server gains nothing.
NO_SERVER_ROLE = ("unsupported",)


def post(path, payload):
    req = urllib.request.Request(
        f"{MODRINTH}{path}",
        data=json.dumps(payload).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def get(path):
    req = urllib.request.Request(f"{MODRINTH}{path}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def sha1_of(panel, jar):
    """SHA1 of a jar on the server, cached -- Modrinth keys files by content."""
    hit = CACHE / (jar + ".sha1")
    if hit.exists():
        return hit.read_text().strip()
    url = panel.get("files/download", {"file_path": "/mods/" + jar})["attributes"]["url"]
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    h = hashlib.sha1()
    with urllib.request.urlopen(req, timeout=300) as r:
        while chunk := r.read(1 << 20):
            h.update(chunk)
    digest = h.hexdigest()
    hit.write_text(digest)
    return digest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--all", action="store_true", help="print every resolved jar")
    ap.add_argument("--refresh", action="store_true", help="rebuild the hash cache")
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(line_buffering=True)

    CACHE.mkdir(parents=True, exist_ok=True)
    if a.refresh:
        for f in CACHE.glob("*"):
            f.unlink()

    p = Panel()
    jars = sorted(e["name"] for e in p.list_dir("/mods") if e["name"].endswith(".jar"))
    if not jars:
        raise SystemExit("/mods came back empty — refusing to act on that")
    jars = [j for j in jars if not j.lower().startswith(SERVER_ONLY)]

    todo = [j for j in jars if not (CACHE / (j + ".sha1")).exists()]
    if todo:
        print(f"hashing {len(todo)} jar(s) — this downloads them", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        hashes = dict(zip(jars, ex.map(lambda j: sha1_of(p, j), jars)))

    print(f"resolving {len(jars)} jar(s) against Modrinth", flush=True)
    try:
        found = post("/version_files", {"hashes": list(hashes.values()), "algorithm": "sha1"})
    except urllib.error.HTTPError as e:
        raise SystemExit(f"modrinth lookup failed: {e.code} {e.read()[:200]!r}")

    by_hash = {h: v for h, v in found.items()}
    project_ids = sorted({v["project_id"] for v in by_hash.values()})
    projects = {}
    # ids= takes a JSON array; chunked so the query string stays sane.
    for i in range(0, len(project_ids), 60):
        chunk = json.dumps(project_ids[i:i + 60])
        for proj in get(f"/projects?ids={urllib.parse.quote(chunk)}"):
            projects[proj["id"]] = proj

    rows, unknown = [], []
    for jar in jars:
        ver = by_hash.get(hashes[jar])
        if not ver:
            unknown.append(jar)
            continue
        proj = projects.get(ver["project_id"], {})
        rows.append({
            "jar": jar,
            "slug": proj.get("slug", "?"),
            "client": proj.get("client_side", "unknown"),
            "server": proj.get("server_side", "unknown"),
            "env": proj.get("environment"),
        })

    flagged = [r for r in rows if r["server"] in NO_SERVER_ROLE]
    show = rows if a.all else flagged
    show.sort(key=lambda r: r["jar"])

    if show:
        print(f"\n{'jar':<52} {'slug':<26} {'client':<10} server")
        for r in show:
            print(f"{r['jar']:<52} {r['slug']:<26} {r['client']:<10} {r['server']}")

    print(f"\n{len(flagged)} of {len(rows)} resolved jars declare server_side=unsupported")

    if unknown:
        print(f"\n{len(unknown)} jar(s) not on Modrinth — undetermined, check by hand:")
        for jar in unknown:
            print(f"  {jar}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PteroError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
