#!/usr/bin/env python3
"""Replace Dynmap with squaremap on the digbuild server.

Why the swap: Dynmap renders 3D block models, which means converting every
mod's models into its own patch format. On this pack that conversion fails
constantly -- 16,327 "Invalid modellist patch" lines per boot, 96% of the whole
log -- because it cannot represent rotated model elements, and its chunk cache
serialised every loaded chunk to NBT and back just to read it. squaremap does
none of that: it draws top-down using each block's built-in vanilla map colour,
so modded blocks work with no scanning step to get wrong.

The cost is that squaremap is flat. There are no isometric perspectives, and
the Forge line is frozen at 1.2.0 (2023-09-15) because upstream moved to
NeoForge. 1.20.1 is frozen too, so that matters less than it reads.

squaremap ships no default config -- it writes one on first boot -- so this is
deliberately two passes:

  python3 scripts/setup_squaremap.py --status
  python3 scripts/setup_squaremap.py --install          # remove Dynmap, add squaremap
  <restart>                                             # squaremap writes its config
  python3 scripts/setup_squaremap.py --configure        # patch port + bind
  <restart>

Restarts are NOT done here -- players may be online. Use
scripts/restart_server.py, which warns them first.
"""
import argparse
import pathlib
import sys
import urllib.request
import zipfile

from ptero import Panel, PteroError

# Pinned. 1.2.0 is the last Forge build squaremap ever published; everything
# after it is NeoForge only. All its classes are Java 17 or older, which is the
# constraint that took the server down with BlueMap 5.12.
JAR = {
    "name": "squaremap-forge-mc1.20.1-1.2.0.jar",
    "url": "https://cdn.modrinth.com/data/PFb7ZqK6/versions/kuGh8mjN/"
           "squaremap-forge-mc1.20.1-1.2.0.jar",
}

# Everything Dynmap left behind. The bluemap directory is from the swap before
# this one and is equally dead.
DEAD_JAR_PREFIXES = ("Dynmap-", "DynmapBlockScan-")
DEAD_DIRS = ("/dynmap", "/bluemap")

# squaremap writes to /squaremap, not /config/squaremap, on Forge.
CONFIG = "/squaremap/config.yml"
# squaremap defaults to 8080; 8034 is the allocation map.<zone> already points
# at, so taking it over means the Cloudflare side needs no change at all.
DEFAULT_PORT = 8034
# What the web UI hands out for links. Left as localhost it produces URLs that
# only work on the container.
WEB_ADDRESS = "https://map.abcdefc.gg"

JAVA17_CLASS_MAJOR = 61


def fetch_jar(dest):
    if dest.exists():
        return dest
    print(f"  downloading {JAR['name']}")
    req = urllib.request.Request(JAR["url"], headers={"User-Agent": "digbuild-tools"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dest.write_bytes(r.read())
    return dest


def max_class_major(jar):
    """Highest bytecode version in the jar.

    Forge does not skip a mod it cannot load, it aborts the whole boot, so a
    jar built for a newer Java than the runtime is a dead server rather than a
    missing feature. Checked here instead of discovered at boot.
    """
    worst = 0
    with zipfile.ZipFile(jar) as z:
        for n in z.namelist():
            if n.endswith(".class"):
                worst = max(worst, int.from_bytes(z.read(n)[6:8], "big"))
    return worst


def dead_jars(p):
    return [
        e["name"] for e in p.list_dir("/mods")
        if e["name"].startswith(DEAD_JAR_PREFIXES)
    ]


def status(p):
    print("== map mods ==")
    for e in p.list_dir("/mods"):
        n = e["name"]
        if n.startswith(DEAD_JAR_PREFIXES) or n.lower().startswith("squaremap"):
            print(f"  {n:60} {e['size']:>10}")

    print("\n== leftover directories ==")
    for d in DEAD_DIRS:
        print(f"  {d}: {'present' if p.exists(d) else 'gone'}")

    print("\n== squaremap config ==")
    try:
        text = p.read_file(CONFIG)
    except PteroError:
        print(f"  {CONFIG} not written yet (needs one boot with the jar installed)")
        return
    # Only the webserver block and the public address. "enabled:" alone appears
    # a dozen times in this file and none of the others are interesting. The
    # block ends at the next line indented no deeper than its own header --
    # every key here is nested, so column zero never comes back.
    depth = None
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        indent = len(line) - len(line.lstrip())
        if s.startswith("internal-webserver:"):
            depth = indent
            print(f"  {line}")
            continue
        if depth is not None and indent <= depth:
            depth = None
        if s.startswith("web-address:") or depth is not None:
            print(f"  {line}")


def install(p, jar, dry_run):
    doomed = dead_jars(p)
    print("removing Dynmap:")
    for n in doomed or ["  (none installed)"]:
        print(f"  /mods/{n}" if doomed else n)
    if doomed and not dry_run:
        p.delete("/mods", doomed)

    for d in DEAD_DIRS:
        if not p.exists(d):
            continue
        print(f"  {d}/ (rendered tiles and config)")
        if not dry_run:
            parent, _, name = d.rpartition("/")
            p.delete(parent or "/", [name])

    print(f"\ninstalling {JAR['name']}")
    if not dry_run:
        p.upload(jar, "/mods")


def configure(p, port, dry_run):
    """Patch the generated config's webserver block, leaving the rest alone."""
    try:
        text = p.read_file(CONFIG)
    except PteroError:
        raise SystemExit(
            f"{CONFIG} does not exist yet -- boot once with the jar installed "
            "so squaremap writes its defaults, then run this again."
        )

    out, patched = [], set()
    in_webserver = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("internal-webserver:"):
            in_webserver = True
            out.append(line)
            continue
        # Only touch port/bind inside internal-webserver; both are common enough
        # words to appear elsewhere in the file.
        if in_webserver and stripped and not line[0].isspace():
            in_webserver = False
        if in_webserver and stripped.startswith("port:"):
            out.append(line.split("port:")[0] + f"port: {port}")
            patched.add("port")
        elif in_webserver and stripped.startswith("bind:"):
            # The container's public interface is not localhost; binding there
            # would make the map unreachable from Cloudflare.
            out.append(line.split("bind:")[0] + "bind: 0.0.0.0")
            patched.add("bind")
        elif stripped.startswith("web-address:"):
            out.append(line.split("web-address:")[0] + f"web-address: {WEB_ADDRESS}")
            patched.add("web-address")
        else:
            out.append(line)

    missing = {"port", "bind", "web-address"} - patched
    if missing:
        raise SystemExit(
            f"did not find {', '.join(sorted(missing))} in {CONFIG} -- the "
            "schema changed; patch it by hand rather than letting this write "
            "something wrong"
        )

    print(f"{CONFIG}: port -> {port}, bind -> 0.0.0.0, "
          f"web-address -> {WEB_ADDRESS}")
    if not dry_run:
        p.write_file(CONFIG, "\n".join(out) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--status", action="store_true")
    g.add_argument("--install", action="store_true")
    g.add_argument("--configure", action="store_true")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    p = Panel()

    if a.status:
        status(p)
        return 0

    if a.configure:
        configure(p, a.port, a.dry_run)
        print("\nrestart to pick it up: python3 scripts/restart_server.py")
        return 0

    # Repo-relative, not cwd-relative: running this from scripts/ should not
    # scatter a second cache directory in there.
    cache = pathlib.Path(__file__).resolve().parent.parent / ".cache"
    cache.mkdir(exist_ok=True)
    jar = fetch_jar(cache / JAR["name"])

    major = max_class_major(jar)
    have = p.java_major()
    print(f"bytecode: max class major {major}, server java {have}")
    if major > JAVA17_CLASS_MAJOR:
        raise SystemExit(
            f"{JAR['name']} needs a newer Java than {have}; refusing -- Forge "
            "would abort the boot rather than skip it"
        )

    install(p, jar, a.dry_run)
    print(
        "\nnext: restart so squaremap writes its config, then\n"
        f"  python3 scripts/setup_squaremap.py --configure --port {a.port}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
