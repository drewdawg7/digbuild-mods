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

from ptero import Panel

MODS = pathlib.Path("mods")
MANIFEST = pathlib.Path("manifest.json")

# Mods dropped from the pack, cumulative across every release.
#
# Extracting the zip over an existing mods/ adds and overwrites but never
# deletes, so a mod removed server-side lingers in players' folders forever.
# Usually harmless; not always -- digbuild-dynmappatch and digbuild-heappatch
# both export digbuild.patch, and two modules exporting one package is a JVM
# ResolutionException before Forge even starts, so the game dies at launch with
# no mod-loading error to read.
#
# Cumulative rather than per-release: a player several releases behind has to
# see every removal since their last update, not just the newest one. Names are
# never pruned -- the file is the full history, and deleting a mod you do not
# have is a no-op.
REMOVED = pathlib.Path("remove-mods.txt")

# Server-only jars that must never reach players' packs. Listed one by one, not
# by a "digbuild-" wildcard: digbuild-patches and digbuild-tickpatches are
# side="BOTH" and carry client rendering mixins, so players need them.
# squaremap declares side="BOTH", but only because its command layer is shared;
# the map itself is a server-side webserver and it is 7.9 MB of dead weight in a
# client pack. Its displayTest is IGNORE_ALL_VERSION, so clients without it
# connect fine. spark is universal, but it is a server profiler -- players have
# no use for it and it only inflates the download.
EXCLUDE_PREFIXES = (
    "digbuild-modsync",
    "digbuild-heappatch",
    "squaremap",
    "spark",
)

panel = Panel()


def remote_listing():
    """name -> {size, modified} for every .jar in /mods."""
    out = {}
    for a in panel.list_dir("/mods"):
        name = a["name"]
        if name.lower().startswith(EXCLUDE_PREFIXES):
            continue  # server-only, not distributed
        if name.lower().endswith(".jar") and not Panel.is_dir(a):
            out[name] = {"size": a["size"], "modified": a["modified"]}
    return out


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
        panel.download(f"/mods/{name}", MODS / name)

    MANIFEST.write_text(json.dumps(remote, indent=2, sort_keys=True) + "\n")

    # Append this run's removals, minus anything already listed or since
    # re-added -- a mod that came back must not still read as "delete me".
    known = [
        line.strip()
        for line in (REMOVED.read_text().splitlines() if REMOVED.exists() else [])
        if line.strip() and not line.startswith("#")
    ]
    stale = sorted({*known, *removed} - set(remote))
    if stale:
        REMOVED.write_text(
            "# Mods no longer in the pack. Delete these from your mods folder;\n"
            "# extracting the zip cannot remove them for you. Mods you added\n"
            "# yourself are not listed here and should be left alone.\n"
            + "\n".join(stale)
            + "\n"
        )
    elif REMOVED.exists():
        REMOVED.unlink()

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
