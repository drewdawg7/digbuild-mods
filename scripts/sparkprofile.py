#!/usr/bin/env python3
"""Parse a spark .sparkprofile and report who allocates.

In an --alloc profile the per-node "time" field carries bytes allocated rather
than nanoseconds. What matters is *self* allocation -- a frame's own total minus
its children's -- otherwise every result is just "Thread.run" holding 100%.

Wire format (spark's sampler proto):
  SamplerData    { 1: metadata, 2: repeated ThreadNode }
  ThreadNode     { 1: name, 2: time(double), 3: repeated StackTraceNode }
  StackTraceNode { 1: time(double), 2: repeated StackTraceNode,
                   3: class_name, 4: method_name }

  python3 scripts/sparkprofile.py --latest
  python3 scripts/sparkprofile.py --latest --top 30 --filter squaremap
"""
import argparse
import collections
import gzip
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ptero import Panel  # noqa: E402

SPARK_DIR = "/config/spark"
MIB = 1 << 20


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
            val, i = struct.unpack("<f", buf[i:i + 4])[0], i + 4
        elif wtype == 1:
            val, i = struct.unpack("<d", buf[i:i + 8])[0], i + 8
        else:
            raise ValueError(f"unsupported wire type {wtype}")
        yield fnum, wtype, val


def _node(buf, is_thread=False):
    """-> (label, total, [children]). Thread and stack nodes differ only in
    which field numbers carry the name and the children."""
    name = cls = meth = None
    total = 0.0
    children = []
    for fnum, wtype, val in _fields(buf):
        if is_thread:
            if fnum == 1 and wtype == 2:
                name = val.decode("utf8", "replace")
            elif fnum == 2 and wtype in (0, 1, 5):
                total = float(val)
            elif fnum == 3 and wtype == 2:
                children.append(val)
        else:
            # Allocation counts come across as varints; wall-clock profiles use
            # doubles. Accept either rather than silently reading every total
            # as zero.
            if fnum == 1 and wtype in (0, 1, 5):
                total = float(val)
            elif fnum == 2 and wtype == 2:
                children.append(val)
            elif fnum == 3 and wtype == 2:
                cls = val.decode("utf8", "replace")
            elif fnum == 4 and wtype == 2:
                meth = val.decode("utf8", "replace")
    if not is_thread:
        name = f"{cls}.{meth}" if cls else (meth or "?")
    return name, total, children


def walk(buf, self_by_frame, is_thread=False, depth=0):
    """Accumulate self-allocation per frame. Returns this node's total."""
    name, total, kids = _node(buf, is_thread)
    child_total = 0.0
    for k in kids:
        child_total += walk(k, self_by_frame, False, depth + 1)
    # A parent's total already includes its children; only the remainder was
    # allocated by this frame itself.
    self_by_frame[name] += max(0.0, total - child_total)
    return total if total else child_total


def _packed_doubles(buf):
    """Field 8 is a packed double array of allocated bytes per time window."""
    return [struct.unpack("<d", buf[i:i + 8])[0]
            for i in range(0, len(buf) - 7, 8)]


def parse(blob):
    """Aggregate allocated bytes per frame.

    spark writes the call tree flattened -- every frame is a direct child of the
    thread node, with the tree shape carried separately -- so this sums each
    frame's own recorded bytes rather than walking a nesting that is not there.
    """
    if blob[:2] == b"\x1f\x8b":
        blob = gzip.decompress(blob)
    by_frame = collections.Counter()
    threads = 0
    for fnum, wtype, val in _fields(blob):
        if fnum != 2 or wtype != 2:
            continue
        threads += 1
        for sf, swt, sv in _fields(val):
            if sf != 3 or swt != 2:
                continue
            cls = meth = None
            amount = 0.0
            for gf, gwt, gv in _fields(sv):
                if gf == 3 and gwt == 2:
                    cls = gv.decode("utf8", "replace")
                elif gf == 4 and gwt == 2:
                    meth = gv.decode("utf8", "replace")
                elif gf == 8 and gwt == 2:
                    vals = _packed_doubles(gv)
                    if vals:
                        amount = vals[0]
            if cls:
                by_frame[f"{cls}.{meth}"] += amount
    return by_frame, threads


def latest_file(p):
    files = [e["name"] for e in p.list_dir(SPARK_DIR) if e["name"].endswith(".sparkprofile")]
    if not files:
        raise SystemExit(f"no .sparkprofile in {SPARK_DIR}")
    return f"{SPARK_DIR}/{sorted(files)[-1]}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?")
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--filter", help="only frames containing this substring")
    ap.add_argument("--dump", action="store_true",
                    help="print the raw field layout instead of parsing")
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

    if a.dump:
        raw = gzip.decompress(blob) if blob[:2] == b"\x1f\x8b" else blob
        print(f"\ntop level ({len(raw):,} bytes):")
        for fnum, wtype, val in _fields(raw):
            size = len(val) if isinstance(val, (bytes, bytearray)) else val
            print(f"  field {fnum} wt{wtype} -> {size}")
            # Descend one level into each candidate message to see its shape.
            if wtype == 2 and len(val) > 16:
                shown = 0
                for sf, swt, sv in _fields(val):
                    d = sv[:50] if isinstance(sv, (bytes, bytearray)) else sv
                    print(f"      sub {sf} wt{swt} -> {d!r:.60}")
                    # One more level: the actual stack node fields.
                    if fnum == 2 and sf == 3 and swt == 2 and shown < 3:
                        shown += 1
                        for gf, gwt, gv in _fields(sv):
                            g = gv[:40] if isinstance(gv, (bytes, bytearray)) else gv
                            print(f"          leaf {gf} wt{gwt} -> {g!r:.50}")
        return 0

    frames, threads = parse(blob)
    total = sum(frames.values())
    print(f"\n{threads} threads, {total / MIB:,.0f} MiB sampled\n")

    rows = frames.most_common()
    if a.filter:
        rows = [(k, v) for k, v in rows if a.filter.lower() in k.lower()]

    print(f"{'MiB':>10}  {'%':>5}  frame")
    for name, amount in rows[: a.top]:
        print(f"{amount / MIB:10,.1f}  {amount / total * 100:5.1f}  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
