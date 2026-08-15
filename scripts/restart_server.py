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


def announce(panel, text, dry_run=False):
    if dry_run:
        print(f"  [dry-run] say {text}")
        return
    panel.send_command(f"say {text}")
    print(f"  say {text}")


def wait_for_ready(panel, timeout=READY_TIMEOUT):
    """Poll until the server reports running AND the log says it finished boot."""
    deadline = time.monotonic() + timeout
    seen_stopped = False
    while time.monotonic() < deadline:
        try:
            state = panel.state()
        except PteroError:
            state = "unreachable"

        if state in ("stopping", "offline", "starting", "unreachable"):
            seen_stopped = True

        if state == "running" and seen_stopped:
            try:
                log = panel.read_file("/logs/latest.log")
            except PteroError:
                log = ""
            if READY_MARKER in log:
                return True

        left = int(deadline - time.monotonic())
        print(f"  {state}… ({left}s left)")
        time.sleep(POLL)
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--message", default="restarting to bring up the live map")
    ap.add_argument("--countdown", type=int, default=15,
                    help="seconds between the warning and the restart")
    ap.add_argument("--no-wait", action="store_true",
                    help="don't block waiting for the server to come back")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

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

    print(f"sending power {signal}…")
    panel.power(signal)

    if args.no_wait:
        return 0

    if wait_for_ready(panel):
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
