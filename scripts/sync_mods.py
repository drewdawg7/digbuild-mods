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

# What the list is, then what to do when it is wrong. The caveat only parses
# once the reader knows these are deletions.
#
# The caveat earns its place: the list is derived from what left the server,
# which is not the same question as what a player can safely delete. A
# client-side library the server dropped may still be holding up a mod the
# player added themselves -- deleting Searchables here took out Controlling on
# every client that followed the instruction.
#
# Kept in the writer rather than in the file, or CI regenerates the list without
# it on the next publish. Every line stays commented -- the reader below treats
# '#' as a comment and would otherwise take these for mod names.
HEADER = (
    "# Mods no longer in the pack. Delete these from your mods folder;\n"
    "# extracting the zip cannot remove them for you. Mods you added\n"
    "# yourself are not listed here and should be left alone.\n"
    "#\n"
    "# Sometimes client-side mods may end up on this list. If your game fails\n"
    "# to launch because of a missing mod, just install it normally through\n"
    "# CurseForge (or whichever launcher you use).\n"
)

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
    "digbuild-tweaks",
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


def header_is_stale():
    """True when the published list carries an older header than HEADER.

    The header is player-facing documentation that lives in this script, but
    publishes are driven by mod changes -- so a correction to the wording would
    otherwise sit unpublished until someone happened to install a mod, which
    could be weeks. Treating a stale header as a reason to publish is what makes
    editing it here actually reach anyone.

    Compares only the commented prefix; the entries are rebuilt further down.
    """
    if not REMOVED.exists():
        return False
    current = REMOVED.read_text()
    return not current.startswith(HEADER)


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

    # A stale header is a publish reason on its own. Falling through to the
    # normal path rather than short-circuiting is deliberate: that path also
    # refills the mirror on a cold cache, and the zip step would otherwise be
    # handed an empty mods/.
    stale_header = header_is_stale()

    if not (added or removed or updated or stale_header):
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
        REMOVED.write_text(HEADER + "\n".join(stale) + "\n")
    elif REMOVED.exists():
        REMOVED.unlink()

    lines = []
    for n in added:
        lines.append(f"- added `{n}`")
    for n in updated:
        lines.append(f"- updated `{n}`")
    for n in removed:
        lines.append(f"- removed `{n}`")
    if not lines:
        # Header-only run. The release notes come from this file, and
        # `gh release create --notes-file` rejects an empty one.
        lines.append("- updated the notes at the top of `remove-mods.txt`")
    pathlib.Path("CHANGES.md").write_text("\n".join(lines) + "\n")

    print(f"{len(added)} added, {len(updated)} updated, {len(removed)} removed")
    emit(changed="true", count=str(len(remote)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
