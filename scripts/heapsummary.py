#!/usr/bin/env python3
"""Parse a spark .sparkheap file and print what is actually holding the heap.

spark's web viewer is the usual way to read these, but the file is just a
protobuf and the interesting part is a flat list of (class, instances, bytes).
Decoding it here means the answer to "what is using the memory" is a table in
the terminal instead of a link someone has to open.

Wire format (spark's HeapData):
  HeapData  { 1: metadata, 2: repeated HeapEntry }
  HeapEntry { 1: order, 2: instances, 3: size, 4: class name }

  python3 scripts/heapsummary.py --latest
  python3 scripts/heapsummary.py --latest --top 40
  python3 scripts/heapsummary.py ./local.sparkheap
"""
import argparse
import collections
import gzip
import pathlib
import re
import sys

from ptero import Panel

SPARK_DIR = "/config/spark"
MIB = 1 << 20

# Rough attribution of a class name to the thing that shipped it.
OWNERS = (
    ("squaremap", re.compile(r"squaremap", re.I)),
    ("minecraft/forge", re.compile(r"^(net\.minecraft|net\.minecraftforge|com\.mojang)")),
    # Primitive/object arrays and JDK collections carry no ownership of their
    # own -- they are whatever allocated them. Keep them in one bucket rather
    # than letting them masquerade as a mod.
    ("unattributable (arrays/collections/String)", re.compile(
        r"^(byte|char|short|int|long|float|double|boolean|java\.lang\.Object)\[\]$"
        r"|^java\.lang\.(String|Integer|Long|Double|Boolean)(\[\])?$"
        r"|^java\.util\."
    )),
    ("jdk", re.compile(r"^(java|jdk|sun|\[)")),
    ("it.unimi/fastutil", re.compile(r"^it\.unimi")),
)


def _varint(buf, i):
    val = shift = 0
    while True:
        b = buf[i]
        i += 1
        val |= (b & 0x7F) << shift
        if not b & 0x80:
            return val, i
        shift += 7


def _fields(buf):
    """Yield (field_number, wire_type, value) for a protobuf message."""
    i, n = 0, len(buf)
    while i < n:
        key, i = _varint(buf, i)
        fnum, wtype = key >> 3, key & 7
        if wtype == 0:
            val, i = _varint(buf, i)
        elif wtype == 2:
            ln, i = _varint(buf, i)
            val, i = buf[i:i + ln], i + ln
        elif wtype == 5:
            val, i = buf[i:i + 4], i + 4
        elif wtype == 1:
            val, i = buf[i:i + 8], i + 8
        else:
            raise ValueError(f"unsupported wire type {wtype}")
        yield fnum, wtype, val


def parse(blob):
    if blob[:2] == b"\x1f\x8b":
        blob = gzip.decompress(blob)
    entries = []
    for fnum, wtype, val in _fields(blob):
        if fnum != 2 or wtype != 2:
            continue  # 1 is metadata; we only want the entries
        e = {"order": 0, "instances": 0, "size": 0, "type": "?"}
        for sf, swt, sv in _fields(val):
            if sf == 1:
                e["order"] = sv
            elif sf == 2:
                e["instances"] = sv
            elif sf == 3:
                e["size"] = sv
            elif sf == 4 and swt == 2:
                e["type"] = sv.decode("utf8", "replace")
        entries.append(e)
    return entries


def owner(cls):
    for name, rx in OWNERS:
        if rx.search(cls):
            return name
    return cls.split(".")[0] if "." in cls else "other"


def latest_file(p):
    files = [
        e["name"] for e in p.list_dir(SPARK_DIR)
        if e["name"].endswith(".sparkheap")
    ]
    if not files:
        raise SystemExit(f"no .sparkheap in {SPARK_DIR}")
    return f"{SPARK_DIR}/{sorted(files)[-1]}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="local .sparkheap file")
    ap.add_argument("--latest", action="store_true", help="pull newest from the server")
    ap.add_argument("--top", type=int, default=30)
    a = ap.parse_args(argv)

    if a.latest:
        p = Panel()
        remote = latest_file(p)
        local = pathlib.Path(remote).name
        print(f"fetching {remote}")
        p.download(remote, local)
        blob = pathlib.Path(local).read_bytes()
    elif a.path:
        blob = pathlib.Path(a.path).read_bytes()
    else:
        ap.error("give a path or --latest")

    entries = parse(blob)
    total = sum(e["size"] for e in entries)
    print(f"\n{len(entries)} classes, {total / MIB:,.0f} MiB retained\n")

    print(f"{'MiB':>9}  {'%':>5}  {'instances':>12}  class")
    for e in sorted(entries, key=lambda e: -e["size"])[: a.top]:
        pct = e["size"] / total * 100 if total else 0
        print(f"{e['size'] / MIB:9,.1f}  {pct:5.1f}  {e['instances']:12,}  {e['type']}")

    print(f"\n{'MiB':>9}  {'%':>5}  owner")
    by_owner = collections.Counter()
    for e in entries:
        by_owner[owner(e["type"])] += e["size"]
    for name, size in by_owner.most_common(15):
        print(f"{size / MIB:9,.1f}  {size / total * 100:5.1f}  {name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
