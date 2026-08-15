#!/usr/bin/env python3
"""Install and configure Dynmap on the digbuild server.

Dynmap is server-side (side="SERVER") and runs its own webserver, so it needs
a second port allocation -- the same one map.<zone> is already pointed at by
scripts/setup_cloudflare_map.py.

The config is not written from scratch: configuration.txt is pulled out of the
jar and only the two webserver lines are patched, so every other default stays
whatever the shipped version says.

Usage:
  python3 scripts/setup_dynmap.py --status
  python3 scripts/setup_dynmap.py --port <port> --dry-run
  python3 scripts/setup_dynmap.py --port <port>

A restart is required afterwards and is NOT done here -- players may be online.
Use scripts/restart_server.py, which warns them first.
"""
import argparse
import hashlib
import pathlib
import sys
import urllib.request
import zipfile

from ptero import Panel, PteroError

# Pinned: newest Forge 1.20 build. Dynmap has no stable 1.20.1 release, only
# the 3.7 betas. Its core is Java 8 bytecode, so the Java 17 runtime here is
# not a constraint the way it was for BlueMap.
JAR_NAME = "Dynmap-3.7-beta-6-forge-1.20.jar"
JAR_URL = (
    "https://cdn.modrinth.com/data/fRQREgAc/versions/RtI5TFAi/"
    "Dynmap-3.7-beta-6-forge-1.20.jar"
)
JAR_SHA512 = (
    "e08e993976d51417737267f3478b7a8a7aa73883249dcf5308b441a9aff45868"
    "2515dc393de5d6be09aeb81ffdee26ed628a210766d9b2df3d1aee509f7206fd"
)

ENTRYPOINT_CLASS = "org/dynmap/DynmapCore.class"
CLASS_MAJOR_OFFSET = 44

MODS_DIR = "/mods"
# The modded build reads its config from /dynmap, not /config/dynmap.
CONFIG_DIR = "/dynmap"
CONFIG_NAME = "configuration.txt"


def fetch_jar(cache):
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


def check_java(p, jar):
    """Refuse to upload a jar this server's JVM cannot load.

    Forge aborts the entire boot on an unloadable mod rather than skipping it,
    so this is worth checking before the upload rather than after the crash.
    """
    with zipfile.ZipFile(jar) as z:
        needs = int.from_bytes(z.read(ENTRYPOINT_CLASS)[6:8], "big") - CLASS_MAJOR_OFFSET
    have = p.java_major()
    if have is None:
        print(f"  ! could not read the server's Java version; jar needs {needs}")
        return
    if needs > have:
        raise SystemExit(
            f"{JAR_NAME} needs Java {needs} but the server runs Java {have}."
        )
    print(f"  java: server {have}, jar needs {needs} -- ok")


def configuration(jar, port):
    """The jar's own configuration.txt with only the webserver lines changed."""
    with zipfile.ZipFile(jar) as z:
        text = z.read(CONFIG_NAME).decode("utf8")

    out, patched = [], set()
    for line in text.splitlines():
        if line.startswith("webserver-port:"):
            out.append(f"webserver-port: {port}")
            patched.add("port")
        elif line.startswith("#webserver-bindaddress:"):
            # PebbleHost routes the allocation to the container's public
            # interface, so binding to localhost would make it unreachable.
            out.append("webserver-bindaddress: 0.0.0.0")
            patched.add("bind")
        else:
            out.append(line)

    missing = {"port", "bind"} - patched
    if missing:
        raise SystemExit(
            f"could not patch {sorted(missing)} in the shipped {CONFIG_NAME} -- "
            "the format changed, check it by hand"
        )
    return "\n".join(out) + "\n"


def status(p):
    installed = [
        e["name"] for e in p.list_dir(MODS_DIR)
        if e["name"].lower().startswith("dynmap")
    ]
    print(f"jar:         {installed[0] if installed else '(not installed)'}")

    try:
        present = sorted(e["name"] for e in p.list_dir(CONFIG_DIR))
        print(f"config:      {CONFIG_DIR}/ -> {', '.join(present) or '(empty)'}")
    except PteroError:
        print(f"config:      {CONFIG_DIR}/ (does not exist yet)")

    try:
        for line in p.read_file(f"{CONFIG_DIR}/{CONFIG_NAME}").splitlines():
            if line.startswith(("webserver-port:", "webserver-bindaddress:")):
                print(f"             {line}")
    except PteroError:
        pass

    allocs = p.allocations()
    for a in allocs:
        print(f"allocation:  {a['port']} {'(game port)' if a['is_default'] else '(web)'}")
    print(f"state:       {p.state()}, online: {', '.join(p.online_players()) or 'nobody'}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, help="allocation for Dynmap's webserver")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--force-config", action="store_true",
                    help="overwrite configuration.txt if it already exists")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cache", default=".cache/dynmap.jar")
    args = ap.parse_args(argv)

    p = Panel()

    if args.status:
        status(p)
        return 0

    port = args.port
    if not port:
        extra = [a for a in p.allocations() if not a["is_default"]]
        if len(extra) != 1:
            ap.error("pass --port; could not pick an allocation unambiguously")
        port = extra[0]["port"]
        print(f"using allocation {port}")

    jar = fetch_jar(args.cache)
    check_java(p, jar)

    present = [
        e["name"] for e in p.list_dir(MODS_DIR)
        if e["name"].lower().startswith("dynmap")
    ]
    stale = [n for n in present if n != JAR_NAME]
    if stale:
        if args.dry_run:
            print(f"[dry-run] would remove {', '.join(stale)}")
        else:
            print(f"removing {', '.join(stale)}")
            p.delete(MODS_DIR, stale)

    if JAR_NAME in present:
        print("jar already present, skipping upload")
    elif args.dry_run:
        print(f"[dry-run] would upload {jar} -> {MODS_DIR}/{JAR_NAME}")
    else:
        print(f"uploading {JAR_NAME} -> {MODS_DIR}")
        p.upload(jar, MODS_DIR, name=JAR_NAME)

    conf = configuration(jar, port)
    try:
        exists = CONFIG_NAME in {e["name"] for e in p.list_dir(CONFIG_DIR)}
    except PteroError:
        exists = False
        if args.dry_run:
            print(f"[dry-run] would create {CONFIG_DIR}")
        else:
            print(f"creating {CONFIG_DIR}")
            p.mkdir("/", CONFIG_DIR.lstrip("/"))

    if exists and not args.force_config:
        print(f"{CONFIG_NAME} exists, left alone (--force-config to replace)")
    elif args.dry_run:
        print(f"[dry-run] would write {CONFIG_DIR}/{CONFIG_NAME} (port {port})")
    else:
        print(f"writing {CONFIG_DIR}/{CONFIG_NAME} (webserver-port {port})")
        p.write_file(f"{CONFIG_DIR}/{CONFIG_NAME}", conf)

    if not args.dry_run:
        print("\nStaged. Dynmap loads on the next restart:")
        print("  python3 scripts/restart_server.py")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PteroError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
