#!/usr/bin/env python3
"""Build digbuild-tweaks-<ver>.jar -- a server-only Forge 1.20.1 mod carrying
this pack's gameplay tweaks, each one config-driven and reloadable in place.

A tweak lives here when the thing it changes is code rather than data and no
config anywhere in the pack reaches it. The first one widens which items an
enchantment may be applied to: EnchantmentCategory.WEAPON is
`item instanceof SwordItem`, and nothing -- not Apotheosis' enchantments.cfg,
not a datapack -- exposes that. Adding another means a class under
src/digbuild/tweaks/tweak/, an entry in Tweaks.ALL, and its mixin (if it needs
one) in SOURCES and digbuildtweaks.mixins.json.

Server-only: every check these override runs on the server, so players need
nothing. Deliberately not more mixins in digbuild-heappatch -- that one is JVM
and cache behaviour and would apply to any pack, this is gameplay and is
specific to ours.

Compile-only deps are shared with the heap patch's ./lib cache, plus the two
Forge jars. Order matters: forge-<ver>-server.jar carries the *patched*
Minecraft classes, and Enchantment.canApplyAtEnchantingTable -- which one of the
injectors targets -- exists only there, not in vanilla's -srg.jar.

  python3 tweaks/build_mod.py
  python3 tweaks/build_mod.py --refresh   # re-pull the cached deps
"""
import argparse
import os
import pathlib
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "patch"))
from ptero import Panel  # noqa: E402
import build_mod as heappatch  # noqa: E402  (the heap patch's build, for javac/deps)

LIB = heappatch.LIB
STAGE = HERE / "build" / "mod"

VERSION = "1.0.0"
OUT = HERE / f"digbuild-tweaks-{VERSION}.jar"

FORGE_BASE = "/libraries/net/minecraftforge/forge"

# Also compile-only, and not in the heap patch's cache because that mod touches
# neither the event bus nor anything Mojang-serialized: the mod and Forge event
# buses, and DFU, which Registry's supertypes reference and javac therefore has
# to see.
MAVEN = ("/libraries/net/minecraftforge/eventbus", "/libraries/com/mojang/datafixerupper")

SOURCES = (
    "src/digbuild/tweaks/DigbuildTweaks.java",
    "src/digbuild/tweaks/Tweak.java",
    "src/digbuild/tweaks/Tweaks.java",
    "src/digbuild/tweaks/tweak/CraftCarryover.java",
    "src/digbuild/tweaks/tweak/EnchantApplicability.java",
    "src/digbuild/tweaks/mixin/CraftingCarryoverMixin.java",
    "src/digbuild/tweaks/mixin/EnchantmentApplicabilityMixin.java",
)

MIXIN_CONFIG = "digbuildtweaks.mixins.json"

RESOURCES = {
    "mods.toml": "META-INF/mods.toml",
    "pack.mcmeta": "pack.mcmeta",
    MIXIN_CONFIG: MIXIN_CONFIG,
}

# Forge registers a mod's mixin config from this manifest attribute. The
# [[mixins]] block in mods.toml alone is not enough -- without it the config is
# never read, no injector runs, and nothing anywhere reports an error.
MANIFEST = f"""Manifest-Version: 1.0
MixinConfigs: {MIXIN_CONFIG}
"""


def forge_jars(panel, refresh=False):
    """The patched Minecraft (-server) and the Forge API (-universal)."""
    vers = [e["name"] for e in panel.list_dir(FORGE_BASE) if Panel.is_dir(e)]
    if not vers:
        raise SystemExit(f"no versioned Forge under {FORGE_BASE}")
    vdir = f"{FORGE_BASE}/{sorted(vers)[-1]}"
    names = {e["name"] for e in panel.list_dir(vdir)}

    out = []
    for kind in ("server", "universal"):
        remote = next((n for n in sorted(names) if n.endswith(f"-{kind}.jar")), None)
        if not remote:
            raise SystemExit(f"no -{kind}.jar in {vdir}")
        dest = LIB / f"forge-{kind}.jar"
        if refresh or not dest.exists():
            print(f"  pulling {vdir}/{remote}")
            panel.download(f"{vdir}/{remote}", dest)
        out.append(dest)
    return out


def maven_jars(panel, refresh=False):
    """Newest version directory of each, and the jar in it."""
    out = []
    for base in MAVEN:
        vers = [e["name"] for e in panel.list_dir(base) if Panel.is_dir(e)]
        if not vers:
            raise SystemExit(f"nothing under {base}")
        vdir = f"{base}/{sorted(vers)[-1]}"
        jars = [e["name"] for e in panel.list_dir(vdir) if e["name"].endswith(".jar")]
        if not jars:
            raise SystemExit(f"no jar in {vdir}")
        dest = LIB / jars[0]
        if refresh or not dest.exists():
            print(f"  pulling {vdir}/{jars[0]}")
            panel.download(f"{vdir}/{jars[0]}", dest)
        out.append(dest)
    return out


def compile_sources(classpath):
    if STAGE.exists():
        for p in sorted(STAGE.rglob("*"), reverse=True):
            p.rmdir() if p.is_dir() else p.unlink()
    STAGE.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(heappatch.javac()), "--release", "17",
        # No refmap to generate: the mixin is remap=false and written in the
        # SRG names the Forge runtime actually uses.
        "-proc:none",
        "-cp", os.pathsep.join(str(p) for p in classpath),
        "-d", str(STAGE),
        *[str(HERE / s) for s in SOURCES],
    ]
    print("  javac --release 17")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout + r.stderr, file=sys.stderr)
        raise SystemExit("compile failed")
    if r.stderr.strip():
        print("  " + r.stderr.strip().replace("\n", "\n  "))


def package():
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("META-INF/MANIFEST.MF", MANIFEST)
        for cls in sorted(STAGE.rglob("*.class")):
            z.write(cls, cls.relative_to(STAGE).as_posix())
        for src, arc in RESOURCES.items():
            z.write(HERE / src, arc)
    return OUT


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--refresh", action="store_true", help="re-pull cached deps")
    a = ap.parse_args(argv)

    panel = Panel()
    print("deps:")
    forge = forge_jars(panel, a.refresh)
    shared = heappatch.fetch_deps(panel, a.refresh)
    # forge-server first: its Enchantment is the patched one, and the vanilla
    # copy in mcsrg.jar would shadow it the other way round.
    classpath = forge + maven_jars(panel, a.refresh) + shared

    print("compile:")
    compile_sources(classpath)
    print("package:")
    jar = package()
    print(f"\nbuilt {jar.name} ({jar.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
