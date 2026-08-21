#!/usr/bin/env python3
"""Check the built jar before it goes anywhere near the server.

Same rules as the heap patch's check, one target class different: Forge does not
skip a mod it cannot load, it aborts the boot, and an injector whose target has
drifted is a silent no-op under "required": false.

The member names below are typed by hand into the mixin and resolved from
strings at runtime, so javac cannot check them -- and they live in two different
jars. canEnchant is vanilla, SRG-named; canApplyAtEnchantingTable is Forge's
addition and exists only in the patched classes.

  python3 tweaks/verify_patch.py
"""
import importlib.util
import json
import pathlib
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "patch"))
from verify_patch import check_bytecode, javap, JAVA17_CLASS_MAJOR  # noqa: E402


def _module(name, path):
    """Load by path, not by name. Both mods have a build_mod.py and a
    verify_patch.py, and ../patch is on sys.path for the shared helpers above --
    an ordinary import here silently checks the heap patch's jar instead."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_build = _module("tweaks_build", HERE / "build_mod.py")
LIB, OUT = _build.LIB, _build.OUT

ENCHANTMENT = "net.minecraft.world.item.enchantment.Enchantment"
SHAPED = "net.minecraft.world.item.crafting.ShapedRecipe"
SHAPELESS = "net.minecraft.world.item.crafting.ShapelessRecipe"

# (jar, class, signature fragment). The vanilla jar is checked for Enchantment
# too, so a Forge update that moved canApplyAtEnchantingTable off it cannot pass
# by looking like the vanilla name it never was.
#
# The recipe entries carry the parameter type on purpose: assemble is
# overloaded, the bridge takes a plain Container, and targeting the wrong one
# would run the carryover twice.
EXPECTED = (
    ("mcsrg.jar", ENCHANTMENT, "m_6081_"),
    ("forge-server.jar", ENCHANTMENT, "m_6081_"),
    ("forge-server.jar", ENCHANTMENT, "canApplyAtEnchantingTable"),
    ("mcsrg.jar", SHAPED, "m_5874_(net.minecraft.world.inventory.CraftingContainer"),
    ("mcsrg.jar", SHAPELESS, "m_5874_(net.minecraft.world.inventory.CraftingContainer"),
)


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

    print("\ninjector targets:")
    dumps = {}
    for jar, cls, member in EXPECTED:
        path = LIB / jar
        if not path.exists():
            print(f"  FAIL {jar} not cached -- cannot verify {member}")
            ok = False
            continue
        dumps.setdefault((jar, cls), javap(cls, path))
        found = any(member in line for line in dumps[(jar, cls)].splitlines())
        print(f"  {'ok  ' if found else 'FAIL'} {cls.rsplit('.', 1)[-1]}.{member}")
        ok = ok and found

    print("\nmanifest:")
    with zipfile.ZipFile(OUT) as z:
        manifest = z.read("META-INF/MANIFEST.MF").decode()
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
        present = f"{pkg}/{m}.class" in classes
        print(f"  {'ok  ' if present else 'FAIL'} {m}")
        ok = ok and present

    print("\n" + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
