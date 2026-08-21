#!/usr/bin/env python3
"""Upload the tweaks jar, restart, and confirm the server came back.

Same shape as the heap patch's deploy and it reuses that boot watcher: upload,
restart, and roll the jar back off the server if the boot fails or the log names
this mod. Refuses to run while players are online.

The success check is the summary each tweak logs when its config is applied at
setup. A boot that comes up clean with no such line means every config was empty
or unreadable -- the server is fine and the jar is doing nothing, which is
exactly the failure that is invisible otherwise.

Only needed for code changes. Config edits are picked up by the running server
within about ten seconds; see Tweaks.java.

  python3 tweaks/deploy.py
  python3 tweaks/deploy.py --no-rollback     # leave the jar on for debugging
"""
import argparse
import importlib.util
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "patch"))
from ptero import Panel, PteroError  # noqa: E402
from deploy import ERROR_MARKERS, rollback, wait_for_boot  # noqa: E402


def _module(name, path):
    """See verify_patch.py: ../patch is on sys.path and has a build_mod too."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


OUT = _module("tweaks_build", HERE / "build_mod.py").OUT

# Anything here in the boot log means this patch is the problem.
FAILURE_MARKERS = (
    "digbuildtweaks",
    "digbuild.tweaks",
)

APPLIED_MARKER = "[digbuild] tweaks:"


def patch_errors(p):
    try:
        lines = p.log_lines()
    except (PteroError, OSError):
        return []
    return [
        ln for ln in lines
        if any(m in ln for m in ERROR_MARKERS) and any(f in ln for f in FAILURE_MARKERS)
    ]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-rollback", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="restart even with players online")
    a = ap.parse_args(argv)

    if not OUT.exists():
        raise SystemExit(f"{OUT.name} not built -- run build_mod.py")

    p = Panel()
    who = p.online_players()
    if who and not a.force:
        print(f"players online: {', '.join(who)} -- refusing", file=sys.stderr)
        return 1
    if who:
        print(f"players online: {', '.join(who)} -- restarting anyway (--force)")

    print(f"uploading {OUT.name} -> /mods")
    p.upload(OUT, "/mods")

    print("restarting...")
    p.power("restart")
    time.sleep(20)

    if not wait_for_boot(p):
        print("server did not report Done in time", file=sys.stderr)
        if not a.no_rollback:
            rollback(p, OUT.name)
        return 1

    errs = patch_errors(p)
    if errs:
        print("\npatch produced errors:", file=sys.stderr)
        for ln in errs[:10]:
            print("  " + ln.strip()[:200], file=sys.stderr)
        if not a.no_rollback:
            rollback(p, OUT.name)
        return 1

    applied = []
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        applied = [ln for ln in p.log_lines() if APPLIED_MARKER in ln]
        if applied:
            break
        time.sleep(10)

    if not applied:
        print("\nbooted clean, but no tweak applied anything -- check "
              "/config/digbuild-tweaks/ and the boot log.")
        return 1

    print("booted clean")
    for ln in applied[-6:]:
        print("  " + ln.split("]: ", 1)[-1].strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
