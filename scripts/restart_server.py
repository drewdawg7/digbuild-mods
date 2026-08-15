#!/usr/bin/env python3
"""Warn whoever is online, restart the server, then wait for it to come back.

The panel API has no player list, so the roster comes from latest.log. The
in-game warning is a plain `say` through the console endpoint.

Usage:
  python3 scripts/restart_server.py --message "back in a minute" --countdown 15
  python3 scripts/restart_server.py --dry-run
  python3 scripts/restart_server.py --no-wait
"""
import argparse
import sys
import time

from ptero import Panel, PteroError

# Forge with ~150 mods is not quick to boot; give it room before giving up.
READY_TIMEOUT = 480
POLL = 10

# The line Minecraft prints once the server is accepting connections.
READY_MARKER = 'Done ('

LOG = "/logs/latest.log"


def announce(panel, text, dry_run=False):
    if dry_run:
        print(f"  [dry-run] say {text}")
        return
    panel.send_command(f"say {text}")
    print(f"  say {text}")


def boot_id(panel):
    """First line of latest.log -- the boot's ModLauncher banner, which carries
    its timestamp. Minecraft rotates latest.log on every start, so this changing
    is positive proof a *new* boot began. Returns None if the log is unreadable."""
    try:
        log = panel.read_file(LOG)
    except PteroError:
        return None
    return log.split("\n", 1)[0].strip() or None


def wait_for_ready(panel, was=None, timeout=READY_TIMEOUT):
    """Wait for a new boot to appear and finish.

    Two gates, in order: latest.log must rotate away from `was` (the pre-restart
    first line), then the new log must contain the ready marker.

    Do not gate this on observing a non-running state instead. A restart's
    stopping/offline/starting window can be shorter than one poll interval, so
    polling steps straight over it and the gate never opens -- which stranded
    this script for four minutes on a server that booted in twenty-five seconds.
    """
    deadline = time.monotonic() + timeout
    rotated = was is None  # nothing to compare against -> take the log as-is
    while True:
        try:
            state = panel.state()
        except PteroError:
            state = "unreachable"

        try:
            log = panel.read_file(LOG)
        except PteroError:
            log = ""

        first = log.split("\n", 1)[0].strip()
        if not rotated and first and first != was:
            rotated = True

        if rotated and READY_MARKER in log:
            return True

        left = int(deadline - time.monotonic())
        if left <= 0:
            return False
        note = "booting" if rotated else "waiting for restart"
        print(f"  {state} / {note}… ({left}s left)", flush=True)
        time.sleep(min(POLL, left))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--message", default="restarting to bring up the live map")
    ap.add_argument("--countdown", type=int, default=15,
                    help="seconds between the warning and the restart")
    ap.add_argument("--no-wait", action="store_true",
                    help="don't block waiting for the server to come back")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    # Progress is the whole point of the wait loop; block buffering hides it
    # completely when stdout is a pipe rather than a terminal.
    sys.stdout.reconfigure(line_buffering=True)

    panel = Panel()

    state = panel.state()
    online = panel.online_players() if state == "running" else []
    print(f"state: {state}, online: {', '.join(online) or 'nobody'}")

    # Nothing to warn if it's already down -- and `say` would just error.
    warn = state == "running"
    signal = "restart" if warn else "start"

    if warn:
        announce(panel, f"{args.message} (restarting in {args.countdown}s)", args.dry_run)

    if args.dry_run:
        if warn:
            print(f"  [dry-run] wait {args.countdown}s, then power {signal}")
        else:
            print(f"  [dry-run] power {signal}")
        return 0

    if warn:
        time.sleep(args.countdown)
        announce(panel, "restarting now")

    # Grab this *before* the power signal, or the rotation check races the boot.
    was = boot_id(panel)

    print(f"sending power {signal}…", flush=True)
    panel.power(signal)

    if args.no_wait:
        return 0

    if wait_for_ready(panel, was):
        print("server is back up")
        return 0
    print("server did not report ready in time — check the console", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PteroError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
