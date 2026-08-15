#!/usr/bin/env python3
"""Drive spark from the server console and pull its output back out of the log.

The client API has no console-response channel -- `POST /command` returns 204
and the actual output only ever lands in latest.log. So every command here is
"send, wait, diff the log". Bracketing by log length rather than by timestamp
keeps it correct when several commands run back to back.

  python3 scripts/spark_report.py
  python3 scripts/spark_report.py heapsummary
  python3 scripts/spark_report.py healthreport tps
"""
import argparse
import sys
import time

from ptero import Panel

# spark prints asynchronously, a beat after the command returns. Heap summaries
# take the longest -- they walk the whole live set.
SETTLE = {"heapsummary": 25, "healthreport": 25}
DEFAULT_SETTLE = 10

DEFAULT_COMMANDS = ("heapsummary", "healthreport")


def run_command(p, command, settle):
    """Send `command`, then return whatever the log gained afterwards."""
    before = len(p.log_lines())
    p.send_command(command)
    time.sleep(settle)
    return p.log_lines()[before:]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "commands",
        nargs="*",
        default=list(DEFAULT_COMMANDS),
        help=f"spark subcommands (default: {' '.join(DEFAULT_COMMANDS)})",
    )
    # A profiler run is the wait, not an afterthought: `profiler start` returns
    # immediately and the interesting output arrives whenever it is stopped.
    ap.add_argument("--settle", type=int, help="seconds to wait after each command")
    a = ap.parse_args(argv)

    p = Panel()
    for sub in a.commands:
        print(f"=== spark {sub} ===")
        settle = a.settle or SETTLE.get(sub.split()[0], DEFAULT_SETTLE)
        for line in run_command(p, f"spark {sub}", settle):
            # Strip the log prefix; spark's own formatting is what matters.
            print(line.split("]: ", 1)[-1] if "]: " in line else line)
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
