#!/usr/bin/env python3
"""Read /world/level.dat off the server and print the settings that shape play.

Gamerules are not in any .toml -- they live in level.dat as NBT, which means
neither the panel nor a config grep will show you keepInventory or
naturalRegeneration. Difficulty is doubly confusing: server.properties carries
one value and level.dat carries another, and for a dedicated server the
server.properties value is the one that wins on every boot. Printing both is
the point of this script.

  python3 scripts/leveldat.py              # gamerules + world settings
  python3 scripts/leveldat.py --all        # the whole Data compound, minus bulk
  python3 scripts/leveldat.py --file x.dat # parse a local copy instead

Only a reader. Changing a gamerule is a /gamerule console command, not an edit
to this file -- level.dat is rewritten by the server on save and any hand-edit
races that write.
"""
import argparse
import gzip
import io
import struct
import sys

from ptero import Panel

# TAG ids, in spec order. TAG_End=0 terminates a compound.
(END, BYTE, SHORT, INT, LONG, FLOAT, DOUBLE, BYTE_ARRAY, STRING, LIST,
 COMPOUND, INT_ARRAY, LONG_ARRAY) = range(13)

_FIXED = {
    BYTE: (">b", 1), SHORT: (">h", 2), INT: (">i", 4), LONG: (">q", 8),
    FLOAT: (">f", 4), DOUBLE: (">d", 8),
}

# Difficulty is stored as an ordinal; server.properties uses the name.
DIFFICULTIES = ["peaceful", "easy", "normal", "hard"]

# The world settings worth seeing next to the gamerules.
WORLD_KEYS = ["Difficulty", "DifficultyLocked", "hardcore", "allowCommands",
              "GameType", "SpawnX", "SpawnY", "SpawnZ", "Time", "DayTime"]

# Arrays and the datapack/dimension blobs are megabytes of noise in --all.
BULK_KEYS = {"Player", "DimensionData", "DataPacks", "ServerBrands",
             "removed_features", "enabled_features", "WorldGenSettings"}


def _read(f, n):
    b = f.read(n)
    if len(b) != n:
        raise EOFError("truncated NBT")
    return b


def _string(f):
    (n,) = struct.unpack(">H", _read(f, 2))
    return _read(f, n).decode("utf8", "replace")


def _payload(f, tag, path="Data"):
    if tag in _FIXED:
        fmt, n = _FIXED[tag]
        return struct.unpack(fmt, _read(f, n))[0]
    if tag == STRING:
        return _string(f)
    if tag == BYTE_ARRAY:
        (n,) = struct.unpack(">i", _read(f, 4))
        return _read(f, n)
    if tag in (INT_ARRAY, LONG_ARRAY):
        width = 4 if tag == INT_ARRAY else 8
        code = ">i" if tag == INT_ARRAY else ">q"
        (n,) = struct.unpack(">i", _read(f, 4))
        return [struct.unpack(code, _read(f, width))[0] for _ in range(n)]
    if tag == LIST:
        (inner,) = struct.unpack(">b", _read(f, 1))
        (n,) = struct.unpack(">i", _read(f, 4))
        # An empty list is written with inner=TAG_End; recursing on that would
        # be a parse error rather than the empty list it actually means.
        if inner == END or n <= 0:
            return []
        return [_payload(f, inner, f"{path}[{i}]") for i in range(n)]
    if tag == COMPOUND:
        out = {}
        while True:
            (t,) = struct.unpack(">b", _read(f, 1))
            if t == END:
                return out
            name = _string(f)
            out[name] = _payload(f, t, f"{path}.{name}")
    raise ValueError(f"unknown NBT tag {tag} at {path} (offset {f.tell()})")


def parse(raw):
    """Root compound of a (gzipped or raw) NBT document."""
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    f = io.BytesIO(raw)
    (tag,) = struct.unpack(">b", _read(f, 1))
    if tag != COMPOUND:
        raise ValueError("level.dat does not start with a compound")
    _string(f)  # root name, conventionally empty
    return _payload(f, COMPOUND)


def _fmt(v):
    return v.decode("utf8", "replace") if isinstance(v, bytes) else v


def report(data, show_all=False):
    rules = data.get("GameRules", {})
    print(f"gamerules ({len(rules)}):")
    for k in sorted(rules):
        print(f"  {k} = {_fmt(rules[k])}")

    print("\nworld settings:")
    for k in WORLD_KEYS:
        if k not in data:
            continue
        v = _fmt(data[k])
        if k == "Difficulty" and isinstance(v, int) and v < len(DIFFICULTIES):
            v = f"{v} ({DIFFICULTIES[v]})"
        print(f"  {k} = {v}")
    print("\n  note: for a dedicated server, server.properties `difficulty`")
    print("  overwrites level.dat's Difficulty on every boot -- compare both.")

    if show_all:
        print("\nother keys in Data:")
        for k in sorted(data):
            if k in BULK_KEYS or k in WORLD_KEYS or k == "GameRules":
                continue
            v = data[k]
            if isinstance(v, (dict, list)) and len(v) > 12:
                print(f"  {k} = <{type(v).__name__} of {len(v)}>")
            else:
                print(f"  {k} = {_fmt(v)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", help="parse a local level.dat instead of fetching")
    ap.add_argument("--all", action="store_true", help="also dump the rest of Data")
    a = ap.parse_args(argv)

    if a.file:
        raw = open(a.file, "rb").read()
    else:
        # level.dat is binary, so files/contents will not serve it -- the
        # signed-url download path is the only way to get the bytes.
        dest = "/tmp/digbuild-level.dat"
        Panel().download("/world/level.dat", dest)
        raw = open(dest, "rb").read()

    root = parse(raw)
    report(root.get("Data", root), show_all=a.all)
    return 0


if __name__ == "__main__":
    sys.exit(main())
