#!/usr/bin/env python3
"""Build digbuild-heappatch-<ver>.jar -- a small server-only Forge 1.20.1 mod
that fixes heap behaviour the host will not let us fix from outside.

Two things only, neither tied to any particular mod:
  - HeapTuning sets MinHeapFreeRatio/MaxHeapFreeRatio and G1's periodic GC at
    runtime, because PebbleHost passes neither LOADER_STARTUPFLAGS nor
    user_jvm_args.txt through to the JVM.
  - StructureTemplateCacheMixin bounds vanilla's unbounded template cache.

Deliberately separate from digbuild-patches / digbuild-tickpatches: those are
side="BOTH" and ship to players, this one is server-only and must not.

Compile-only dependencies are pulled from the game server itself and cached in
./lib: mixin, the Forge language jars, and SRG-named Minecraft. Mixins are
compiled against the real target, never against a guess at its shape -- an
@Inject whose signature has drifted fails at boot, not at build time.

javac is the one thing that has to be a subprocess; the jar is assembled with
zipfile so no external `jar` binary is needed.

  python3 patch/build_mod.py
  python3 patch/build_mod.py --refresh   # re-pull the cached deps
"""
import argparse
import os
import pathlib
import subprocess
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
from ptero import Panel  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
LIB = HERE / "lib"
STAGE = HERE / "build" / "mod"

VERSION = "1.0.0"
OUT = HERE / f"digbuild-heappatch-{VERSION}.jar"

# The server runs Java 17. Newer bytecode aborts the whole Forge boot, so build
# with a real 17 toolchain rather than whatever happens to be on PATH.
JAVA_HOMES = (
    os.environ.get("JAVA_HOME"),
    "/opt/homebrew/opt/openjdk@17",
    "/usr/lib/jvm/java-17-openjdk",
)

# Remote path -> local cache name. All compile-only.
DEPS = {
    "/libraries/org/spongepowered/mixin/0.8.5/mixin-0.8.5.jar": "mixin-0.8.5.jar",
}

SOURCES = (
    "src/digbuild/patch/DigbuildPatchMod.java",
    "src/digbuild/patch/HeapTuning.java",
    "src/digbuild/patch/mixin/StructureTemplateCacheMixin.java",
)

RESOURCES = {
    "mods.toml": "META-INF/mods.toml",
    "pack.mcmeta": "pack.mcmeta",
    "digbuildheappatch.mixins.json": "digbuildheappatch.mixins.json",
}


def javac():
    for home in JAVA_HOMES:
        if home and (pathlib.Path(home) / "bin" / "javac").exists():
            return pathlib.Path(home) / "bin" / "javac"
    raise SystemExit(
        "no Java 17 toolchain found. brew install openjdk@17, or set JAVA_HOME."
    )


def fetch_deps(panel, refresh=False):
    """Cache the compile-time jars, pulling from the server when missing."""
    LIB.mkdir(exist_ok=True)
    paths = []

    for remote, local in DEPS.items():
        dest = LIB / local
        if refresh or not dest.exists():
            print(f"  pulling {remote}")
            panel.download(remote, dest)
        paths.append(dest)

    # SRG-named Minecraft. StructureTemplateCacheMixin shadows f_230345_ and
    # injects into m_230407_ by their runtime names, so they have to be on the
    # classpath -- and compiling against them is the point: a drifted name is a
    # javac error here instead of a missing injector at boot.
    mcsrg = LIB / "mcsrg.jar"
    if refresh or not mcsrg.exists():
        base = "/libraries/net/minecraft/server"
        vers = [e["name"] for e in panel.list_dir(base) if "-" in e["name"]]
        if not vers:
            raise SystemExit(f"no versioned Minecraft under {base}")
        vdir = f"{base}/{sorted(vers)[-1]}"
        srg = [
            e["name"] for e in panel.list_dir(vdir) if e["name"].endswith("-srg.jar")
        ]
        if not srg:
            raise SystemExit(f"no -srg.jar in {vdir}")
        print(f"  pulling {vdir}/{srg[0]}")
        panel.download(f"{vdir}/{srg[0]}", mcsrg)
    paths.append(mcsrg)

    # Forge's @Mod annotation. The agent build already caches these.
    forgelib = HERE.parent / "agent" / "forgelib"
    for jar in ("javafmllanguage.jar", "fmlcore.jar"):
        f = forgelib / jar
        if not f.exists():
            raise SystemExit(f"missing {f} -- run the agent build first")
        paths.append(f)

    return paths


def compile_sources(classpath):
    if STAGE.exists():
        for p in sorted(STAGE.rglob("*"), reverse=True):
            p.rmdir() if p.is_dir() else p.unlink()
    STAGE.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(javac()), "--release", "17",
        # Mixin's jar carries an annotation processor that generates refmaps and
        # drags in gson. The mixin here is remap=false and written in SRG names,
        # which is what the Forge runtime uses, so there is no refmap to build.
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


MIXIN_CONFIG = "digbuildheappatch.mixins.json"

# Forge registers a mod's mixin config from this manifest attribute. The
# [[mixins]] block in mods.toml alone is not enough -- without MixinConfigs the
# config is never read, no injector runs, and nothing anywhere reports an error.
# digbuild-patches carries the same attribute; that is how it works and this
# did not.
MANIFEST = f"""Manifest-Version: 1.0
MixinConfigs: {MIXIN_CONFIG}
"""


def package():
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        # First entry by convention, so a plain unzip shows it up top.
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
    classpath = fetch_deps(Panel(), a.refresh)
    print("compile:")
    compile_sources(classpath)
    print("package:")
    jar = package()
    print(f"\nbuilt {jar.name} ({jar.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
