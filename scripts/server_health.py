#!/usr/bin/env python3
"""Why is the server using that much memory? Snapshot, or watch it over time.

Container memory on a modded server is mostly *reserved* heap, not live data --
the JVM takes -Xmx up front and G1 hands very little of it back once it has
grown. So the panel number only means something next to the heap ceiling, the
mod count, and whether it is still climbing while idle.

  python3 scripts/server_health.py              # one snapshot
  python3 scripts/server_health.py --watch 10   # 10 samples, 30s apart
  python3 scripts/server_health.py --watch 10 --every 60
"""
import argparse
import re
import sys
import time

from ptero import Panel

GIB = 1 << 30
MIB = 1 << 20

# Knobs that drive resident memory more than anything players do.
WORLD_KEYS = ("view-distance", "simulation-distance", "max-players", "level-name")

# Mods that exist specifically to cut (or that notoriously add) heap pressure.
MEMORY_MODS = re.compile(
    r"spark|alltheleaks|ferritecore|modernfix|clumps|squaremap|journeymap"
    r"|chunkypregen|chunky",
    re.I,
)


def gib(n):
    return f"{n / GIB:.2f} GiB"


def boot_facts(log):
    out = {}
    for key, rx in (
        ("java", r"java version (\d+)"),
        ("forge", r"Forge version[: ]+([0-9.]+)"),
        ("mods", r"Loading (\d+) mods"),
    ):
        if m := re.search(rx, log):
            out[key] = m.group(1)
    return out


def snapshot(p):
    r = p.resources()["resources"]
    limit_mb = p.details().get("limits", {}).get("memory") or 0
    return {
        "mem": r["memory_bytes"],
        "cpu": r["cpu_absolute"],
        "disk": r["disk_bytes"],
        "uptime_h": r["uptime"] / 3_600_000,
        "limit": limit_mb * MIB,
    }


def report(p):
    s = snapshot(p)
    print("== resources ==")
    pct = f" ({s['mem'] / s['limit'] * 100:.0f}% of limit)" if s["limit"] else ""
    print(f"memory   {gib(s['mem'])}{pct}")
    if s["limit"]:
        print(f"limit    {gib(s['limit'])}")
    print(f"cpu      {s['cpu']:.1f}%")
    print(f"uptime   {s['uptime_h']:.1f} h")
    print(f"disk     {gib(s['disk'])}")

    print("\n== heap ceiling ==")
    st = p.startup()
    heap = [v for k, v in st["vars"].items() if "HEAP" in k.upper() and v]
    print(f"command  {st['command']}")
    if heap:
        print(f"heap     {heap}")
    else:
        # PebbleHost's /opt/start.sh derives -Xmx from the plan's memory limit;
        # LOADER_HEAPLIMITER empty means "use the whole allocation".
        print("heap     no explicit -Xmx -- the egg gives the JVM the full "
              f"{gib(s['limit']) if s['limit'] else 'plan'} allocation")

    log = p.read_file("/logs/latest.log")
    print("\n== boot ==")
    for k, v in boot_facts(log).items():
        print(f"{k:8} {v}")

    print("\n== world knobs ==")
    props = dict(
        line.split("=", 1)
        for line in p.read_file("/server.properties").splitlines()
        if "=" in line and not line.startswith("#")
    )
    for k in WORLD_KEYS:
        if k in props:
            print(f"{k:20} {props[k]}")

    print("\n== memory-relevant mods ==")
    for name in sorted(e["name"] for e in p.list_dir("/mods")):
        if MEMORY_MODS.search(name):
            print(f"  {name}")

    who = p.online_players()
    print(f"\n== players ==\n{', '.join(who) if who else '(nobody online)'}")


def watch(p, count, every):
    """Idle memory that climbs and never falls back is a leak; a sawtooth that
    drops after a GC is just the heap doing its job."""
    print(f"{'sample':>6}  {'memory':>10}  {'delta':>9}  {'cpu':>6}")
    prev = None
    for i in range(count):
        s = snapshot(p)
        d = "" if prev is None else f"{(s['mem'] - prev) / MIB:+.0f} MiB"
        print(f"{i + 1:>6}  {gib(s['mem']):>10}  {d:>9}  {s['cpu']:>5.1f}%")
        prev = s["mem"]
        if i + 1 < count:
            time.sleep(every)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--watch", type=int, metavar="N", help="take N samples instead")
    ap.add_argument("--every", type=int, default=30, help="seconds between samples")
    a = ap.parse_args(argv)

    p = Panel()
    if a.watch:
        watch(p, a.watch, a.every)
    else:
        report(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
