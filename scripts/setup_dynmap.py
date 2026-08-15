#!/usr/bin/env python3
"""Install and configure Dynmap (+ BlockScan) on the digbuild server.

Both mods are server-side (side="SERVER"). Dynmap runs its own webserver, so
it needs a second port allocation -- the same one map.<zone> is already
pointed at by scripts/setup_cloudflare_map.py.

BlockScan is what makes a 148-mod pack render as something other than flat
grey: it walks the installed mods' blockstate/model files and generates the
render definitions Dynmap needs for blocks it doesn't ship knowledge of. It is
only published as a dev snapshot for 1.20.1; there is no stable build.

The config is not written from scratch: configuration.txt is pulled out of the
Dynmap jar and only the two webserver lines are patched, so every other
default stays whatever the shipped version says.

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

# Pinned. Dynmap has no stable 1.20.1 release, only the 3.7 betas, and
# BlockScan only a snapshot. Both are Java 8/17 bytecode, so the Java 17
# runtime here is not the constraint it was for BlueMap.
JARS = [
    {
        "name": "Dynmap-3.7-beta-6-forge-1.20.jar",
        "url": "https://cdn.modrinth.com/data/fRQREgAc/versions/RtI5TFAi/"
               "Dynmap-3.7-beta-6-forge-1.20.jar",
        "sha512": "e08e993976d51417737267f3478b7a8a7aa73883249dcf5308b441a9aff45868"
                  "2515dc393de5d6be09aeb81ffdee26ed628a210766d9b2df3d1aee509f7206fd",
        "entrypoint": "org/dynmap/DynmapCore.class",
        "cache": ".cache/dynmap.jar",
    },
    {
        "name": "DynmapBlockScan-3.7-SNAPSHOT-forge-1.20.jar",
        "url": "https://cdn.modrinth.com/data/L3wHhk2p/versions/8swZ7iRQ/"
               "DynmapBlockScan-3.7-SNAPSHOT-forge-1.20.jar",
        "sha512": "d3c4c760910816547bb4c46c6b88119be2454df52136c737c863aea31b2832c3"
                  "cb382f09bff60f3245d6f65d568786a212a797e2586c97ecd992e920c6ce9552",
        "entrypoint": "org/dynmapblockscan/core/AbstractBlockScanBase.class",
        "cache": ".cache/dynmapblockscan.jar",
    },
]

CLASS_MAJOR_OFFSET = 44  # class file major 61 == Java 17

MODS_DIR = "/mods"
# The modded build reads its config from /dynmap, not /config/dynmap.
CONFIG_DIR = "/dynmap"
CONFIG_NAME = "configuration.txt"

# BlockScan re-scans every mod's models on every single boot -- its work sits in
# Forge's serverStarting() hook with no cache check anywhere in the path, and it
# nulls its assetmap on the way out. Each model whose parent it cannot resolve
# logs a line, which came to 681 lines (~20s) on this pack.
#
# Excluding a module skips it during that scan. The cost is that it is per
# module, not per model: blocks from these mods that DID resolve lose their
# definitions too and fall back to flat colour on the map. So this list is only
# the mods where the noise is high and the blocks are storage/decor that read
# fine flat. alexscaves (13 lines), tconstruct (2) and darkerdepths (1) are
# deliberately left in -- too little noise to be worth flattening them.
BLOCKSCAN_CONFIG = "/config/dynmapblockscan/settings.toml"
BLOCKSCAN_EXCLUDE = [
    "minecraft",               # the mod's own default, keep it
    "sophisticatedstorage",    # 612 of the 681 lines -- limited_*_barrel variants
    "dungeonsdelight",         # 33
    "sophisticatedbackpacks",  # 20
]

# Both jars, and only these, are matched when clearing out old versions.
JAR_PREFIX = "dynmap"


def fetch_jar(spec):
    cache = pathlib.Path(spec["cache"])
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists() and sha512(cache) == spec["sha512"]:
        return cache
    print(f"downloading {spec['name']}")
    with urllib.request.urlopen(spec["url"], timeout=300) as r:
        cache.write_bytes(r.read())
    got = sha512(cache)
    if got != spec["sha512"]:
        raise SystemExit(
            f"hash mismatch for {spec['name']}: "
            f"expected {spec['sha512'][:16]}…, got {got[:16]}…"
        )
    return cache


def sha512(path):
    h = hashlib.sha512()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def check_java(p, jar, entrypoint, have):
    """Refuse to upload a jar this server's JVM cannot load.

    Forge aborts the entire boot on an unloadable mod rather than skipping it,
    so this is worth checking before the upload rather than after the crash.
    """
    with zipfile.ZipFile(jar) as z:
        needs = int.from_bytes(z.read(entrypoint)[6:8], "big") - CLASS_MAJOR_OFFSET
    if have is None:
        print(f"  ! could not read the server's Java version; jar needs {needs}")
        return
    if needs > have:
        raise SystemExit(
            f"{jar.name} needs Java {needs} but the server runs Java {have}."
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


def blockscan_settings():
    """settings.toml in the shape the mod writes it, with our exclude list."""
    modules = ", ".join(f'"{m}"' for m in BLOCKSCAN_EXCLUDE)
    return (
        "#DynmapBlockScan settings\n"
        "#Managed by scripts/setup_dynmap.py\n"
        "[settings]\n"
        "\t#Which modules to exclude\n"
        f"\texclude_modules = [{modules}]\n"
        "\t#Which block names to exclude\n"
        "\texclude_blocknames = []\n"
    )


def installed_jars(p):
    return [
        e["name"] for e in p.list_dir(MODS_DIR)
        if e["name"].lower().startswith(JAR_PREFIX)
    ]


def status(p):
    jars = installed_jars(p)
    print(f"jars:        {', '.join(jars) if jars else '(none installed)'}")

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

    for a in p.allocations():
        print(f"allocation:  {a['port']} {'(game port)' if a['is_default'] else '(web)'}")
    print(f"state:       {p.state()}, online: {', '.join(p.online_players()) or 'nobody'}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, help="allocation for Dynmap's webserver")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--force-config", action="store_true",
                    help="overwrite configuration.txt if it already exists")
    ap.add_argument("--dry-run", action="store_true")
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

    have_java = p.java_major()
    jars = {spec["name"]: fetch_jar(spec) for spec in JARS}
    for spec in JARS:
        check_java(p, jars[spec["name"]], spec["entrypoint"], have_java)

    present = installed_jars(p)
    stale = [n for n in present if n not in jars]
    if stale:
        if args.dry_run:
            print(f"[dry-run] would remove {', '.join(stale)}")
        else:
            print(f"removing {', '.join(stale)}")
            p.delete(MODS_DIR, stale)

    for name, path in jars.items():
        if name in present:
            print(f"{name} already present, skipping upload")
        elif args.dry_run:
            print(f"[dry-run] would upload {name}")
        else:
            print(f"uploading {name} -> {MODS_DIR}")
            p.upload(path, MODS_DIR, name=name)

    conf = configuration(jars[JARS[0]["name"]], port)
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

    # Unlike configuration.txt this one is ours to own -- the mod recreates it
    # with defaults, so it is rewritten every run rather than left alone.
    if args.dry_run:
        print(f"[dry-run] would write {BLOCKSCAN_CONFIG} "
              f"(exclude {len(BLOCKSCAN_EXCLUDE)} modules)")
    else:
        print(f"writing {BLOCKSCAN_CONFIG} (exclude: {', '.join(BLOCKSCAN_EXCLUDE)})")
        p.write_file(BLOCKSCAN_CONFIG, blockscan_settings())

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
