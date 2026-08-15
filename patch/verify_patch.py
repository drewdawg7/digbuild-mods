#!/usr/bin/env python3
"""Check the built jar before it goes anywhere near the server.

Forge does not skip a mod it cannot load, it aborts the boot, and a mixin whose
target has drifted is a silent no-op under "required": false. Everything
asserted here is cheap on a laptop and expensive to discover at boot.

  python3 patch/verify_patch.py
"""
import pathlib
import json
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from build_mod import OUT, javac  # noqa: E402

MCSRG = HERE / "lib" / "mcsrg.jar"

# SRG names are typed by hand in the mixin, so check them against the runtime
# jar. javac cannot: @Shadow and method= are resolved from strings at runtime.
EXPECTED_MC = (
    ("net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager", "f_230345_"),
    ("net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager", "m_230407_"),
)

JAVA17_CLASS_MAJOR = 61


def javap(cls, jar):
    tool = javac().parent / "javap"
    r = subprocess.run(
        [str(tool), "-p", "-cp", str(jar), cls], capture_output=True, text=True
    )
    if r.returncode:
        raise SystemExit(f"javap failed for {cls}:\n{r.stderr}")
    return r.stdout


def check_bytecode(jar):
    """Every class must be Java 17 or older, or Forge aborts the boot."""
    bad = []
    with zipfile.ZipFile(jar) as z:
        for n in z.namelist():
            if not n.endswith(".class"):
                continue
            major = int.from_bytes(z.read(n)[6:8], "big")
            if major > JAVA17_CLASS_MAJOR:
                bad.append((n, major))
    return bad


def main():
    if not OUT.exists():
        raise SystemExit(f"{OUT.name} not built -- run build_mod.py")

    ok = True

    print("bytecode:")
    bad = check_bytecode(OUT)
    for name, major in bad:
        print(f"  FAIL {name}: class major {major} > {JAVA17_CLASS_MAJOR}")
        ok = False
    if not bad:
        print(f"  all classes <= Java 17 (major {JAVA17_CLASS_MAJOR})")

    print("\nSRG targets in mcsrg.jar:")
    if MCSRG.exists():
        dumps = {}
        for cls, member in EXPECTED_MC:
            dumps.setdefault(cls, javap(cls, MCSRG))
            found = any(member in line for line in dumps[cls].splitlines())
            print(f"  {'ok  ' if found else 'FAIL'} {cls.rsplit('.', 1)[-1]}: {member}")
            ok = ok and found
    else:
        print("  mcsrg.jar not cached -- cannot verify SRG names")
        ok = False

    print("\nmanifest:")
    with zipfile.ZipFile(OUT) as z:
        try:
            manifest = z.read("META-INF/MANIFEST.MF").decode()
        except KeyError:
            manifest = ""
    # Without this attribute Forge never reads the mixin config and every
    # injector silently does nothing -- no error, no log line, no effect.
    if "MixinConfigs:" in manifest:
        print("  ok   MixinConfigs present")
    else:
        print("  FAIL no MixinConfigs attribute -- mixins would never load")
        ok = False

    print("\nmixin config:")
    with zipfile.ZipFile(OUT) as z:
        cfgs = [n for n in z.namelist() if n.endswith(".mixins.json")]
        if not cfgs:
            raise SystemExit("no mixin config in the jar")
        cfg = json.loads(z.read(cfgs[0]))
        classes = {n for n in z.namelist() if n.endswith(".class")}
    pkg = cfg["package"].replace(".", "/")
    for m in cfg["mixins"]:
        path = f"{pkg}/{m}.class"
        present = path in classes
        print(f"  {'ok  ' if present else 'FAIL'} {m}")
        ok = ok and present

    print("\n" + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
