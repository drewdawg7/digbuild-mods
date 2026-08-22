#!/usr/bin/env python3
"""Build digbuild-sync-<ver>.jar -- the client-side updater.

A ModLauncher service, not a Forge mod. ModDirTransformerDiscoverer hoists jars
in mods/ that declare cpw.mods.modlauncher.api.ITransformationService onto the
boot layer before mod discovery, so this one can drop new jars into mods/ and
have Forge find them on the same launch. ModsFolderLocator then skips it
(allExcluded), which is why there is no mods.toml here and why Forge does not
complain about its absence.

It downloads the published pack zip and extracts what the player is missing, so
nothing about how the pack is published had to change. Ships inside that zip,
which is why it is *not* in sync_mods.py's EXCLUDE_PREFIXES -- the opposite of
every other digbuild jar. It sits in the game server's mods/ purely so the
existing pipeline carries it; DigbuildSyncService checks LAUNCHTARGET and does
nothing server-side.

Compile-only deps come from the game server's own libraries, cached in ./lib.
joptsimple and securejarhandler are there for javac's benefit only: they appear
in ITransformationService's default-method signatures, so the interface will not
resolve without them even though nothing here calls those methods.

  python3 sync/build_mod.py
  python3 sync/build_mod.py --refresh   # re-pull the cached deps
"""
import argparse
import pathlib
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "patch"))
from ptero import Panel  # noqa: E402
import build_mod as heappatch  # noqa: E402  (for javac/compile, shared)

LIB = HERE / "lib"
STAGE = HERE / "build" / "mod"

VERSION = "1.0.0"
OUT = HERE / f"digbuild-sync-{VERSION}.jar"

# Newest version directory under each is taken, matching how the server itself
# resolves them.
MAVEN = (
    "/libraries/cpw/mods/modlauncher",
    "/libraries/cpw/mods/securejarhandler",
    "/libraries/net/sf/jopt-simple/jopt-simple",
)

SOURCES = (
    "src/digbuild/sync/DigbuildSyncService.java",
    "src/digbuild/sync/SyncCore.java",
    "src/digbuild/sync/SyncConfig.java",
    "src/digbuild/sync/SyncLog.java",
    "src/digbuild/sync/EncryptedZip.java",
    "src/digbuild/sync/Progress.java",
)

SERVICE = "cpw.mods.modlauncher.api.ITransformationService"

# The whole hook. Without this entry the jar is an ordinary file in mods/ that
# Forge rejects for having no mods.toml; with it, ModDirTransformerDiscoverer
# loads it before anything else and Forge leaves it alone.
RESOURCES = {
    f"services/{SERVICE}": f"META-INF/services/{SERVICE}",
}

MANIFEST = "Manifest-Version: 1.0\n"


def maven_jars(panel, refresh=False):
    LIB.mkdir(exist_ok=True)
    out = []
    for base in MAVEN:
        vers = [e["name"] for e in panel.list_dir(base) if Panel.is_dir(e)]
        if not vers:
            raise SystemExit(f"nothing under {base}")
        vdir = f"{base}/{sorted(vers)[-1]}"
        jars = [
            e["name"] for e in panel.list_dir(vdir)
            if e["name"].endswith(".jar") and "-sources" not in e["name"]
        ]
        if not jars:
            raise SystemExit(f"no jar in {vdir}")
        dest = LIB / jars[0]
        if refresh or not dest.exists():
            print(f"  pulling {vdir}/{jars[0]}")
            panel.download(f"{vdir}/{jars[0]}", dest)
        out.append(dest)
    return out


def compile_sources(classpath):
    heappatch.STAGE = STAGE
    heappatch.SOURCES = SOURCES
    heappatch.HERE = HERE
    heappatch.compile_sources(classpath)


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

    print("deps:")
    classpath = maven_jars(Panel(), a.refresh)
    print("compile:")
    compile_sources(classpath)
    print("package:")
    jar = package()
    print(f"\nbuilt {jar.name} ({jar.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
