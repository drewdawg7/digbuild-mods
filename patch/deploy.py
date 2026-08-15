#!/usr/bin/env python3
"""Upload the patch jar, restart, and confirm the server came back.

The mixin config is "required": true, so a drifted injector does not degrade
gracefully -- it aborts the boot. This deploys behind a rollback: if the server
does not report Done, or the log shows a mixin failure naming our config, the
jar is removed and the server restarted again so it is never left down.

Refuses to run while players are online.

  python3 patch/deploy.py
  python3 patch/deploy.py --no-rollback     # leave the jar on for debugging
"""
import argparse
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from ptero import Panel, PteroError  # noqa: E402
from build_mod import OUT  # noqa: E402

BOOT_MARKER = "Done ("
BOOT_TIMEOUT = 480
POLL = 10

# Anything here in the boot log means our patch is the problem.
FAILURE_MARKERS = (
    "digbuildheappatch",
    "digbuild.patch",
)

# HeapTuning logs the flag values it read back. That line is the only proof the
# jar is doing anything at all.
APPLIED_MARKER = "[digbuild] heap tuning:"
# Not just mixin failures: a bad mods.toml dependency range aborts the boot as a
# ModLoadingException long before any injector runs.
ERROR_MARKERS = (
    "MixinApplyError",
    "InvalidInjectionException",
    "mixin apply failed",
    "ModLoadingException",
    "LoadingFailedException",
    "requires",
)


def wait_for_boot(p, timeout=BOOT_TIMEOUT):
    """True once the server reports Done; False the moment it is clear it won't.

    A failed boot does not hang -- Forge exits and the container goes offline.
    Waiting out the full timeout on an already-dead server is just dead time, so
    treat a return to 'offline' after the restart as terminal. The first poll is
    skipped for that check: the container is briefly offline mid-restart, which
    is not a crash.
    """
    deadline = time.monotonic() + timeout
    started = False
    while time.monotonic() < deadline:
        try:
            state = p.state()
            if state == "running":
                started = True
                if BOOT_MARKER in p.read_file("/logs/latest.log"):
                    return True
            elif started and state in ("offline", "stopping"):
                print(f"  server went {state} after starting -- boot failed")
                return False
        except (PteroError, OSError):
            pass  # the log is briefly absent while the container recycles
        time.sleep(POLL)
    print("  timed out waiting for boot")
    return False


def patch_errors(p):
    """Boot-log lines that implicate this patch specifically."""
    try:
        lines = p.log_lines()
    except (PteroError, OSError):
        return []
    return [
        ln for ln in lines
        if any(m in ln for m in ERROR_MARKERS) and any(f in ln for f in FAILURE_MARKERS)
    ]


def rollback(p, name):
    print(f"\nrolling back: removing /mods/{name}")
    p.delete("/mods", [name])
    p.power("restart")
    print("restarting without the patch...")
    if wait_for_boot(p):
        print("server is back up, unpatched")
    else:
        print("server did NOT come back -- check the panel console", file=sys.stderr)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-rollback", action="store_true")
    # The guard is about not surprising people mid-session, not about safety.
    # An admin who knows who is online can say so.
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
        print("\npatch produced mixin errors:", file=sys.stderr)
        for ln in errs[:10]:
            print("  " + ln.strip()[:200], file=sys.stderr)
        if not a.no_rollback:
            rollback(p, OUT.name)
        return 1

    # HeapTuning runs during mod construction, so its line is already in the log
    # by the time Done prints -- but poll anyway rather than assume ordering.
    applied = []
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        applied = [ln for ln in p.log_lines() if APPLIED_MARKER in ln]
        if applied:
            break
        time.sleep(POLL)

    if not applied:
        print("\nbooted clean, but the patch never fired -- the injector missed.")
        print("The server is healthy; the optimisation just is not active.")
        return 1

    print("booted clean")
    print("  " + applied[-1].split("]: ", 1)[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
