#!/usr/bin/env python3
"""Install and configure BlueMap on the digbuild server.

BlueMap is a server-side (side="SERVER") web map. It needs two things the
other 148 mods don't: a second port allocation for its built-in webserver, and
`accept-download: true` so it may pull vanilla client resources from Mojang.
Both are handled here.

Configs are written *before* the first boot so the mod only needs one restart:
BlueMap creates any config file that is missing but never overwrites one that
already exists. The per-dimension map configs (config/bluemap/maps/*.conf) are
deliberately left for BlueMap to generate -- it knows the modded dimension list
and we don't.

Usage (the port is the allocation from the panel -- this repo is public, so it
is passed in rather than hardcoded):

  python3 scripts/setup_bluemap.py --claim-port           # claim one, print it
  python3 scripts/setup_bluemap.py --port <port>          # jar + configs
  python3 scripts/setup_bluemap.py --port <port> --dry-run
  python3 scripts/setup_bluemap.py --configs-only --port <port>
  python3 scripts/setup_bluemap.py --status               # what's installed now

A restart is required afterwards and is NOT done here -- players may be online.
"""
import argparse
import hashlib
import pathlib
import sys
import urllib.request

from ptero import Panel, PteroError

# Pinned: 5.12 is the last BlueMap that supports 1.20.x (a backport; mainline
# moved to 1.21+). Verified against the Modrinth API, loaders=[forge].
JAR_NAME = "bluemap-5.12-mc1.20-6-forge.jar"
JAR_URL = (
    "https://cdn.modrinth.com/data/swbUV1cr/versions/kC7iYqja/"
    "bluemap-5.12-mc1.20-6-forge.jar"
)
JAR_SHA512 = (
    "e3c704792e6fc0243ecc3c7e68aab409b8475ed97b77b1cffa7feaf513e92df2"
    "b77af139e3c9a14a24eee85009bd855c7e0918d9d1d90024a98b419961054cce"
)

MODS_DIR = "/mods"
CONFIG_DIR = "/config/bluemap"

# Data and webroot are relative to the server root, matching BlueMap's defaults.
DATA_DIR = "bluemap"
WEBROOT = "bluemap/web"

# 4 cores available; leave headroom so the initial render doesn't fight the
# server thread while players are on.
RENDER_THREADS = 2


def core_conf():
    return f"""\
##  BlueMap core-config -- managed by scripts/setup_bluemap.py

# Required, or BlueMap will not render at all: this confirms you own Minecraft
# and lets BlueMap download vanilla client resources from Mojang for textures.
accept-download: true

data: "{DATA_DIR}"

render-thread-count: {RENDER_THREADS}

# This is what makes the 148 mods render properly -- BlueMap reads block models
# and textures straight out of the mod jars instead of drawing them grey.
scan-for-mod-resources: true

metrics: true
"""


def webserver_conf(port):
    return f"""\
##  BlueMap webserver-config -- managed by scripts/setup_bluemap.py

enabled: true

webroot: "{WEBROOT}"

# Must be an allocation claimed in the panel (Network -> Additional Ports);
# the default allocation is the game port and cannot be reused.
port: {port}
"""


def webapp_conf():
    return f"""\
##  BlueMap webapp-config -- managed by scripts/setup_bluemap.py

enabled: true

webroot: "{WEBROOT}"

update-settings-file: true
use-cookies: true

# Perspective (3D) by default; players can switch to flat in the map settings.
default-to-flat-view: false
"""


def plugin_conf():
    return """\
##  BlueMap plugin-config -- managed by scripts/setup_bluemap.py

# The live player dots. Requires the integrated webserver, which we run.
live-player-markers: true

hidden-game-modes: [
    "spectator"
]
hide-vanished: true
hide-invisible: true
hide-sneaking: false

skin-download: true

# Don't pause rendering when players are on -- the world is small and the
# render-thread count is already conservative.
player-render-limit: -1

full-update-interval: 1440
"""


def configs(port):
    return {
        f"{CONFIG_DIR}/core.conf": core_conf(),
        f"{CONFIG_DIR}/webserver.conf": webserver_conf(port),
        f"{CONFIG_DIR}/webapp.conf": webapp_conf(),
        f"{CONFIG_DIR}/plugin.conf": plugin_conf(),
    }


def fetch_jar(cache):
    """Download the pinned jar, verifying the hash. Cached between runs."""
    cache = pathlib.Path(cache)
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists() and sha512(cache) == JAR_SHA512:
        return cache
    print(f"downloading {JAR_NAME}")
    with urllib.request.urlopen(JAR_URL, timeout=300) as r:
        cache.write_bytes(r.read())
    got = sha512(cache)
    if got != JAR_SHA512:
        raise SystemExit(f"hash mismatch: expected {JAR_SHA512[:16]}…, got {got[:16]}…")
    return cache


def sha512(path):
    h = hashlib.sha512()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def status(p):
    installed = [
        e["name"] for e in p.list_dir(MODS_DIR) if e["name"].startswith("bluemap")
    ]
    print(f"jar:         {installed[0] if installed else '(not installed)'}")

    try:
        present = sorted(e["name"] for e in p.list_dir(CONFIG_DIR))
        print(f"configs:     {CONFIG_DIR}/ -> {', '.join(present) or '(empty)'}")
    except PteroError:
        print(f"configs:     {CONFIG_DIR}/ (does not exist yet)")

    allocs = p.allocations()
    extra = [a for a in allocs if not a["is_default"]]
    print(f"allocations: {len(allocs)} claimed, {len(extra)} usable for the webserver")
    for a in allocs:
        print(f"             {a['port']} {'(game port)' if a['is_default'] else '(free)'}")

    online = p.online_players()
    print(f"state:       {p.state()}, online: {', '.join(online) or 'nobody'}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, help="allocation for BlueMap's webserver")
    ap.add_argument("--claim-port", action="store_true",
                    help="claim a new allocation from the host pool and print it")
    ap.add_argument("--jar-only", action="store_true")
    ap.add_argument("--configs-only", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--force-configs", action="store_true",
                    help="overwrite configs that already exist on the server")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cache", default=".cache/bluemap.jar")
    args = ap.parse_args(argv)

    p = Panel()

    if args.status:
        status(p)
        return 0

    if args.claim_port:
        free = [a for a in p.allocations() if not a["is_default"]]
        if free:
            print(f"already have a spare allocation: {free[0]['port']}")
        elif args.dry_run:
            print("[dry-run] would claim a new allocation")
        else:
            a = p.create_allocation()
            print(f"claimed port {a['port']}")
        if not args.port:
            return 0

    do_jar = not args.configs_only
    do_configs = not args.jar_only

    if do_configs and not args.port:
        ap.error("--port is required (claim one in the panel: Network -> Additional Ports)")

    if do_configs and args.port:
        claimed = {a["port"] for a in p.allocations()}
        default = next(a["port"] for a in p.allocations() if a["is_default"])
        if args.port not in claimed:
            ap.error(
                f"port {args.port} is not allocated to this server "
                f"(claimed: {sorted(claimed)}). Add it in the panel first."
            )
        if args.port == default:
            ap.error(f"port {args.port} is the game port; claim a separate one")

    if do_jar:
        jar = fetch_jar(args.cache)
        already = [e for e in p.list_dir(MODS_DIR) if e["name"] == JAR_NAME]
        if already:
            print(f"jar already present ({already[0]['size']} bytes), skipping upload")
        elif args.dry_run:
            print(f"[dry-run] would upload {jar} -> {MODS_DIR}/{JAR_NAME}")
        else:
            print(f"uploading {JAR_NAME} -> {MODS_DIR}")
            p.upload(jar, MODS_DIR, name=JAR_NAME)

    if do_configs:
        try:
            existing = {e["name"] for e in p.list_dir(CONFIG_DIR)}
        except PteroError:
            existing = set()
            if args.dry_run:
                print(f"[dry-run] would create {CONFIG_DIR}")
            else:
                print(f"creating {CONFIG_DIR}")
                p.mkdir("/config", "bluemap")

        for path, body in configs(args.port).items():
            name = path.rsplit("/", 1)[-1]
            if name in existing and not args.force_configs:
                print(f"  = {name} (exists, left alone; --force-configs to replace)")
                continue
            if args.dry_run:
                print(f"  [dry-run] would write {path} ({len(body)} bytes)")
            else:
                print(f"  + {name}")
                p.write_file(path, body)

    if not args.dry_run:
        print()
        print("Staged. BlueMap loads on the next server restart.")
        online = p.online_players()
        if online:
            print(f"NOTE: {', '.join(online)} currently online -- don't restart blind.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PteroError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
