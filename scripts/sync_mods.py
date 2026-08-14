#!/usr/bin/env python3
"""Mirror a Pterodactyl server's /mods folder into ./mods.

Compares the remote file listing against manifest.json and downloads only what
changed. Writes GitHub Actions outputs so the workflow can skip the expensive
steps when nothing moved.

Env:
  PTERO_PANEL   panel base url, e.g. https://panel.pebblehost.com
  PTERO_SERVER  short server id, e.g. 70f78775
  PTERO_KEY     client api key (ptlc_...)
"""
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

PANEL = os.environ["PTERO_PANEL"].rstrip("/")
SERVER = os.environ["PTERO_SERVER"]
KEY = os.environ["PTERO_KEY"]

MODS = pathlib.Path("mods")
MANIFEST = pathlib.Path("manifest.json")
TIMEOUT = 120


def api(path, params=None):
    url = f"{PANEL}/api/client/servers/{SERVER}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {KEY}",
            "Accept": "application/json",
            "User-Agent": "digbuild-mods-sync",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def remote_listing():
    """name -> {size, modified} for every .jar in /mods."""
    out = {}
    for item in api("files/list", {"directory": "/mods"})["data"]:
        a = item["attributes"]
        if a["name"].lower().endswith(".jar") and a["mime"] != "inode/directory":
            out[a["name"]] = {"size": a["size"], "modified": a["modified"]}
    return out


def download(name, dest):
    signed = api("files/download", {"file": f"/mods/{name}"})
    url = signed["attributes"]["url"]
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=TIMEOUT) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    tmp.replace(dest)


def emit(**kv):
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def main():
    remote = remote_listing()
    if not remote:
        print("refusing to continue: remote listing is empty", file=sys.stderr)
        return 1

    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}

    added = sorted(set(remote) - set(old))
    removed = sorted(set(old) - set(remote))
    updated = sorted(
        n for n in set(remote) & set(old) if remote[n] != old[n]
    )

    if not (added or removed or updated):
        print(f"no changes ({len(remote)} jars)")
        emit(changed="false")
        return 0

    MODS.mkdir(exist_ok=True)

    # Drop anything the server no longer has, plus stale local extras.
    for f in MODS.glob("*.jar"):
        if f.name not in remote:
            print(f"  - {f.name}")
            f.unlink()

    # Pull new and changed jars. Anything missing locally (cold cache) too.
    want = set(added) | set(updated)
    want |= {n for n in remote if not (MODS / n).exists()}
    for name in sorted(want):
        print(f"  + {name}")
        download(name, MODS / name)

    MANIFEST.write_text(json.dumps(remote, indent=2, sort_keys=True) + "\n")

    lines = []
    for n in added:
        lines.append(f"- added `{n}`")
    for n in updated:
        lines.append(f"- updated `{n}`")
    for n in removed:
        lines.append(f"- removed `{n}`")
    pathlib.Path("CHANGES.md").write_text("\n".join(lines) + "\n")

    print(f"{len(added)} added, {len(updated)} updated, {len(removed)} removed")
    emit(changed="true", count=str(len(remote)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
