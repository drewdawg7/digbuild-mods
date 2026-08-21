#!/usr/bin/env python3
"""Remove a mod from the server, plus the libraries only it was keeping alive.

The counterpart to install_mod.py. Deleting the jar you named is the easy part;
the reason this is a script is the closure. A content mod usually drags in one
or more libraries that nothing else declares, and those are invisible unless you
read every jar's dependency block -- so they sit in the pack forever, loading on
every boot for no one.

Dependencies come from each jar's META-INF/mods.toml, which is where Forge
itself reads them. Do not try to infer them from jar names or from grepping
class files: half of every mod's constant pool matches a substring of
"tconstruct" (AbstractConstruct, DefaultConstructorMarker), and the noise buries
the signal.

The listing is cached under .cache/moddeps/ because building it costs a full
download of every jar on the server -- roughly 500MB. Pass --refresh after
installing something new.

  python3 scripts/remove_mod.py tconstruct --dry-run
  python3 scripts/remove_mod.py tconstruct searchables
  python3 scripts/remove_mod.py tconstruct --keep-config
"""
import argparse
import io
import pathlib
import re
import sys
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor

from ptero import Panel, PteroError

UA = "digbuild-tools"
CACHE = pathlib.Path(__file__).resolve().parent.parent / ".cache" / "moddeps"
WORKERS = 8

# Config files a mod leaves in /config. Forge's own naming is <modid>-common.toml
# / -client.toml / -server.toml, but plenty of mods use a bare <modid>.toml or a
# <modid>/ subdirectory instead, so match on the stem rather than the full name.
CONFIG_DIRS = ["/config", "/defaultconfigs"]


def fetch_toml(panel, jar):
    """This jar's mods.toml, cached. Returns '' for a jar that has none."""
    hit = CACHE / (jar + ".toml")
    if hit.exists():
        return hit.read_text()
    url = panel.get("files/download", {"file_path": "/mods/" + jar})["attributes"]["url"]
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r:
        blob = r.read()
    text = ""
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for name in z.namelist():
                if name.lower().endswith("meta-inf/mods.toml"):
                    text = z.read(name).decode("utf8", "replace")
                    break
    except zipfile.BadZipFile:
        pass
    hit.write_text(text)
    return text


def parse(text):
    """(modIds this jar declares, modIds it depends on) from one mods.toml.

    [[mods]] blocks declare; [[dependencies.x]] blocks require. Both use the key
    `modId`, so the section header is the only thing telling them apart -- a
    plain grep for modId conflates a mod with everything it needs.
    """
    provides, requires, section = [], [], None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("[[mods]]"):
            section = "mods"
            continue
        if s.startswith("[[dependencies."):
            section = "deps"
            continue
        if s.startswith("["):  # any other table ends the block we were in
            section = None
            continue
        m = re.match(r'modId\s*=\s*"([^"]+)"', s)
        if m and section == "mods":
            provides.append(m.group(1))
        elif m and section == "deps":
            requires.append(m.group(1))
    return provides, requires


def build_graph(panel, jars, refresh=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    if refresh:
        for f in CACHE.glob("*.toml"):
            f.unlink()

    missing = [j for j in jars if not (CACHE / (j + ".toml")).exists()]
    if missing:
        print(f"reading mods.toml from {len(missing)} jar(s) — this downloads them", flush=True)
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(lambda j: fetch_toml(panel, j), missing))

    provides, requires = {}, {}
    for jar in jars:
        p, r = parse(fetch_toml(panel, jar))
        provides[jar] = p
        # forge/minecraft are always present; they are noise in every graph
        requires[jar] = [d for d in r if d not in ("forge", "minecraft") and d not in p]
    return provides, requires


def resolve_targets(names, provides):
    """Map each command-line name (a modId or a jar filename) to its jar."""
    by_id = {mid: jar for jar, ids in provides.items() for mid in ids}
    out, unknown = [], []
    for n in names:
        if n in by_id:
            out.append(by_id[n])
        elif n in provides:
            out.append(n)
        else:
            unknown.append(n)
    if unknown:
        raise SystemExit(f"not installed: {', '.join(unknown)}")
    return out


def close_over_orphans(targets, provides, requires):
    """Grow `targets` by the libraries nothing else keeps alive.

    A jar joins the removal set when every jar that declared a dependency on it
    is itself being removed, and at least one did. The "at least one" clause is
    what stops this from swallowing the pack: most content mods have no
    dependents at all, and without it every one of them would look orphaned.
    """
    removing = list(targets)
    added = []
    while True:
        for jar in provides:
            if jar in removing:
                continue
            dependents = [
                other for other in provides
                if other != jar and set(provides[jar]) & set(requires[other])
            ]
            if dependents and all(d in removing for d in dependents):
                removing.append(jar)
                added.append(jar)
                break
        else:
            return removing, added


def blocked_by(removing, provides, requires):
    """Mods that stay but still require something we are about to delete."""
    going = {mid for jar in removing for mid in provides[jar]}
    out = []
    for jar in provides:
        if jar in removing:
            continue
        for mid in requires[jar]:
            if mid in going:
                out.append((jar, mid))
    return out


def find_configs(panel, modids):
    """Config files and directories belonging to any of `modids`."""
    hits = []
    for d in CONFIG_DIRS:
        try:
            entries = panel.list_dir(d)
        except PteroError:
            continue
        for e in entries:
            stem = e["name"].split(".")[0]
            # tconstruct-common.toml -> tconstruct; mantle-client.toml -> mantle
            base = stem.rsplit("-", 1)[0] if "-" in stem else stem
            if stem in modids or base in modids:
                hits.append((d, e["name"], Panel.is_dir(e)))
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("names", nargs="+", help="modId or jar filename to remove")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, delete nothing")
    ap.add_argument("--keep-config", action="store_true", help="leave /config files alone")
    ap.add_argument("--refresh", action="store_true", help="rebuild the mods.toml cache")
    ap.add_argument("--force", action="store_true",
                    help="delete even if a remaining mod still depends on the target")
    a = ap.parse_args(argv)

    sys.stdout.reconfigure(line_buffering=True)
    panel = Panel()

    jars = sorted(e["name"] for e in panel.list_dir("/mods") if e["name"].endswith(".jar"))
    # Same guard as sync_mods.py: an API hiccup that returns nothing must not be
    # read as "the server has no mods" and go on to delete against an empty graph.
    if not jars:
        raise SystemExit("/mods came back empty — refusing to act on that")

    provides, requires = build_graph(panel, jars, a.refresh)
    targets = resolve_targets(a.names, provides)
    removing, orphans = close_over_orphans(targets, provides, requires)

    print(f"\nremoving ({len(removing)} jar(s)):")
    for jar in targets:
        print(f"  {jar}  [named]")
    for jar in orphans:
        needed = [o for o in provides if set(provides[jar]) & set(requires.get(o, []))]
        print(f"  {jar}  [orphaned — was only required by {', '.join(needed)}]")

    stuck = blocked_by(removing, provides, requires)
    if stuck:
        print("\nstill required by mods that are staying:")
        for jar, mid in stuck:
            print(f"  {jar} requires {mid}")
        if not a.force:
            raise SystemExit("refusing — pass --force to remove anyway")

    modids = {mid for jar in removing for mid in provides[jar]}
    configs = [] if a.keep_config else find_configs(panel, modids)
    if configs:
        print("\nconfig:")
        for d, name, isdir in configs:
            print(f"  {d}/{name}{'/' if isdir else ''}")

    if a.dry_run:
        print("\ndry run — nothing deleted")
        return 0

    panel.delete("/mods", removing)
    print(f"\ndeleted {len(removing)} jar(s) from /mods")
    for d in {d for d, _, _ in configs}:
        names = [n for dd, n, _ in configs if dd == d]
        panel.delete(d, names)
        print(f"deleted {len(names)} file(s) from {d}")

    for jar in removing:
        (CACHE / (jar + ".toml")).unlink(missing_ok=True)

    print("\nstill loaded until the server restarts:")
    print("  python3 scripts/restart_server.py --message '...'")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PteroError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
