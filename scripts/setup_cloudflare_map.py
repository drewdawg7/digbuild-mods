#!/usr/bin/env python3
"""Put the web map behind https://map.<zone> instead of a raw ip:port.

The map mod serves plain HTTP on a high port that Cloudflare's proxy does
not listen on, so three things are needed and none of them is just a DNS record:

  1. A proxied A record for the hostname -- proxied so the origin ip stays
     hidden and so the two rules below are allowed to apply at all.
  2. An origin rule rewriting the destination port to the map's allocation.
     Without it Cloudflare would connect to the origin on 80/443.
  3. A configuration rule setting SSL mode to "flexible" for this hostname
     only. The map mod has no TLS, and scoping it here leaves the wiki's own SSL
     mode alone.

Both rule types are on Cloudflare's free plan (10 rules each).

The origin ip and port are read from the Pterodactyl panel, so nothing about
the allocation is hardcoded in this public repo.

Usage:
  python3 scripts/setup_cloudflare_map.py --status
  python3 scripts/setup_cloudflare_map.py --dry-run
  python3 scripts/setup_cloudflare_map.py
"""
import argparse
import sys

from cloudflare import PHASE_CONFIG, PHASE_ORIGIN, CloudflareError, Zone
from ptero import Panel, PteroError

SUBDOMAIN = "map"

# Stable rule identifiers -- re-running updates these in place rather than
# stacking duplicates.
REF_ORIGIN = "digbuild-map-port"
REF_CONFIG = "digbuild-map-ssl"


def map_allocation(panel):
    """(ip, port) of the non-default allocation the map webserver listens on."""
    extra = [a for a in panel.allocations() if not a["is_default"]]
    if not extra:
        raise SystemExit(
            "no spare allocation on the server -- claim one in the panel first"
        )
    if len(extra) > 1:
        raise SystemExit(
            "more than one spare allocation; pass --port to disambiguate: "
            + ", ".join(str(a["port"]) for a in extra)
        )
    return extra[0]["ip"], extra[0]["port"]


def origin_rule(host, port):
    return {
        "ref": REF_ORIGIN,
        "description": "web map webserver port",
        "expression": f'http.host eq "{host}"',
        "action": "route",
        "action_parameters": {"origin": {"port": port}},
        "enabled": True,
    }


def config_rule(host):
    return {
        "ref": REF_CONFIG,
        "description": "map origin speaks plain HTTP",
        "expression": f'http.host eq "{host}"',
        "action": "set_config",
        "action_parameters": {"ssl": "flexible"},
        "enabled": True,
    }


def status(zone, host, port):
    print(f"zone:    {zone.name} ({zone.plan()})")

    records = [r for r in zone.dns_records(name=host) if r["type"] == "A"]
    if records:
        r = records[0]
        where = "proxied" if r["proxied"] else "DNS-ONLY (rules will not apply)"
        print(f"dns:     {host} A -> {_mask(r['content'])} [{where}]")
    else:
        print(f"dns:     {host} (no A record)")

    for phase, ref, label in (
        (PHASE_ORIGIN, REF_ORIGIN, "origin"),
        (PHASE_CONFIG, REF_CONFIG, "config"),
    ):
        found = [r for r in zone.rules(phase) if r.get("ref") == ref]
        if found:
            params = found[0].get("action_parameters", {})
            print(f"{label}:  {found[0]['expression']} -> {params}")
        else:
            print(f"{label}:  (not set)")

    print(f"expects: the map mod listening on port {port}")


def _mask(ip):
    head = ip.split(".")[0] if "." in ip else ip[:4]
    return f"{head}.x.x.x"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--zone", help="zone name (default: the token's only zone)")
    ap.add_argument("--subdomain", default=SUBDOMAIN)
    ap.add_argument("--port", type=int, help="override the map webserver's port")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    panel = Panel()
    zone = Zone(args.zone)
    host = f"{args.subdomain}.{zone.name}"

    ip, port = map_allocation(panel)
    port = args.port or port

    if args.status:
        status(zone, host, port)
        return 0

    print(f"{host} -> {_mask(ip)}:{port}")

    if args.dry_run:
        print(f"  [dry-run] A record {host} -> origin ip, proxied")
        print(f"  [dry-run] origin rule: destination port -> {port}")
        print("  [dry-run] config rule: ssl -> flexible")
        return 0

    _, verb = zone.upsert_dns_record(
        host, "A", ip, proxied=True, comment="web map (managed by digbuild-mods)"
    )
    print(f"  dns record: {verb}")

    # Rules created before the map mod was swapped carried a mod-specific ref;
    # drop them so the generic ones below don't sit alongside duplicates.
    for phase, ref in ((PHASE_ORIGIN, "digbuild-bluemap-port"),
                       (PHASE_CONFIG, "digbuild-bluemap-ssl")):
        if zone.delete_rule(phase, ref):
            print(f"  removed stale rule {ref}")

    print(f"  origin rule: {zone.upsert_rule(PHASE_ORIGIN, origin_rule(host, port))}")
    print(f"  config rule: {zone.upsert_rule(PHASE_CONFIG, config_rule(host))}")

    print()
    print(f"https://{host} is wired up.")
    print("It returns 521/522 until the server restarts and the map mod starts")
    print("listening -- that is Cloudflare reaching a port nothing is on yet.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (CloudflareError, PteroError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
