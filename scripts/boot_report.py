#!/usr/bin/env python3
"""Did the last boot come up clean, and is anything in it new?

server_health.py answers "why is memory like that". This answers "did I just
break something", which is the question after every mod change.

Two things make the raw log useless for that. Removing a mod makes Forge print
one line per registry entry it can no longer resolve -- 2,300 of them for a
mod like Tinkers' Construct -- which buries everything else. And a 150-mod pack
logs the same dozen harmless errors on every single boot, so a fresh eye cannot
tell a real breakage from the usual noise. So: registry casualties are collapsed
to one line per namespace, and errors are diffed against the previous boot's
rotated log and marked NEW.

Exits non-zero if the server is not up or a new error appeared.

  python3 scripts/boot_report.py
  python3 scripts/boot_report.py --errors        # full text of new errors
  python3 scripts/boot_report.py --no-diff       # skip the previous-boot fetch
"""
import argparse
import collections
import gzip
import pathlib
import re
import sys
import tempfile

from ptero import Panel, PteroError

LOG = "/logs/latest.log"

# `[15Aug2026 20:23:04.187] [main/ERROR] [some.logger/TAG]: message`
LINE = re.compile(r"^\[[^\]]+\]\s*\[([^\]]+)\]\s*(?:\[([^\]]+)\])?:?\s*(.*)$")
LEVEL = re.compile(r"/(WARN|ERROR|FATAL)$")

# A registry entry Forge could not resolve, e.g. "\ttconstruct:blazewood: 2318".
CASUALTY = re.compile(r"^\s+([a-z0-9_.-]+):([a-z0-9_./-]+):\s*\d+\s*$")
MISSING_MOD = re.compile(r"^\s*([a-z0-9_.-]+) \(version (\S+) -> MISSING\)\s*$")

READY = re.compile(r'Done \(([0-9.]+)s\)')
FACTS = (
    ("java", r"java version (\d+)"),
    ("forge", r"Forge version[: ]+([0-9.]+)"),
    ("mods", r"Loading (\d+) mods"),
)

# Volatile bits that would otherwise make every occurrence look unique.
NOISE = [
    (re.compile(r"\b0x[0-9a-f]+\b", re.I), "0xX"),
    (re.compile(r"\b\d+\b"), "N"),
    (re.compile(r"%23\d+"), "%23N"),
]


def fingerprint(logger, msg):
    """Collapse a message to something stable across boots, so the same error
    twice is one entry rather than two."""
    for rx, sub in NOISE:
        msg = rx.sub(sub, msg)
    return logger, msg[:200]


def parse(text):
    """(facts, errors, casualties, missing_mods) from one log."""
    facts, errors = {}, collections.Counter()
    casualties = collections.Counter()
    missing = []
    samples = {}

    for key, rx in FACTS:
        if m := re.search(rx, text):
            facts[key] = m.group(1)
    if m := READY.search(text):
        facts["ready"] = f"{m.group(1)}s"

    for line in text.splitlines():
        if m := CASUALTY.match(line):
            casualties[m.group(1)] += 1
            continue
        if m := MISSING_MOD.match(line):
            missing.append((m.group(1), m.group(2)))
            continue
        m = LINE.match(line)
        if not m:
            continue
        thread, logger, msg = m.group(1), m.group(2) or "", m.group(3)
        if not LEVEL.search(thread):
            continue
        key = fingerprint(logger, msg)
        errors[key] += 1
        samples.setdefault(key, line)

    return facts, errors, casualties, missing, samples


def previous_boot(panel):
    """Text of the boot before this one. Minecraft rotates latest.log to
    <date>-<n>.log.gz on every start, so the newest of those is the last boot.
    debug logs are a parallel series and are not comparable."""
    try:
        entries = panel.list_dir("/logs")
    except PteroError:
        return None
    rotated = [
        e for e in entries
        if e["name"].endswith(".log.gz") and not e["name"].startswith("debug")
    ]
    if not rotated:
        return None
    newest = max(rotated, key=lambda e: e["modified"])["name"]
    with tempfile.TemporaryDirectory() as tmp:
        dest = pathlib.Path(tmp) / newest
        panel.download(f"/logs/{newest}", dest)
        with gzip.open(dest, "rt", errors="replace") as f:
            return newest, f.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--errors", action="store_true", help="print full text of new errors")
    ap.add_argument("--all-errors", action="store_true", help="print repeat errors too")
    ap.add_argument("--no-diff", action="store_true", help="don't fetch the previous boot")
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(line_buffering=True)

    p = Panel()
    state = p.state()
    text = p.read_text(LOG)
    facts, errors, casualties, missing, samples = parse(text)

    print("== boot ==")
    print(f"state    {state}")
    for k in ("java", "forge", "mods", "ready"):
        if k in facts:
            print(f"{k:8} {facts[k]}")
    if "ready" not in facts:
        print("ready    NOT YET — no 'Done (…)' line in this log")
    who = p.online_players()
    print(f"players  {', '.join(who) if who else '(nobody)'}")

    if missing:
        print("\n== mods gone from the world ==")
        for mid, ver in missing:
            n = casualties.get(mid, 0)
            print(f"  {mid} {ver} — {n} registry entr{'y' if n == 1 else 'ies'} dropped")
    orphan_ns = {ns: n for ns, n in casualties.items()
                 if ns not in {m for m, _ in missing}}
    if orphan_ns:
        print("\n== dropped entries from mods that are still installed ==")
        print("   (these are unexpected — a mod that is present should resolve)")
        for ns, n in sorted(orphan_ns.items(), key=lambda kv: -kv[1]):
            print(f"  {ns}: {n}")

    prev = None if a.no_diff else previous_boot(p)
    new, repeat = errors, collections.Counter()
    if prev:
        prev_name, prev_text = prev
        _, prev_errors, _, _, _ = parse(prev_text)
        new = collections.Counter({k: v for k, v in errors.items() if k not in prev_errors})
        repeat = collections.Counter({k: v for k, v in errors.items() if k in prev_errors})
        print(f"\n== errors (vs {prev_name}) ==")
        print(f"  {sum(repeat.values())} carried over from the previous boot")
        print(f"  {sum(new.values())} new")
    else:
        print(f"\n== errors ==\n  {sum(errors.values())} total (no previous boot to diff against)")

    def dump(title, counter, verbose):
        if not counter:
            return
        print(f"\n-- {title} --")
        for (logger, msg), n in counter.most_common():
            times = f" x{n}" if n > 1 else ""
            print(f"  [{logger}]{times} {samples[(logger, msg)] if verbose else msg[:140]}")

    dump("NEW", new, a.errors)
    if a.all_errors:
        dump("carried over", repeat, a.errors)
    elif repeat:
        print(f"\n  (--all-errors to see the {len(repeat)} carried-over kinds)")

    ok = state == "running" and "ready" in facts and not new
    print(f"\n{'clean' if ok else 'NEEDS A LOOK'}")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PteroError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
