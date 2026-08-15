#!/usr/bin/env python3
"""Cloudflare API v4 client for the abcdefc.gg zone.

Same shape as ptero.py: import Zone rather than hand-rolling requests. Covers
the pieces this repo needs -- DNS records and the two Rulesets phases that put
a mod's web server behind a real hostname.

Env:
  CLOUDFLARE_API_TOKEN  custom token, zone-scoped. Needs DNS:Edit,
                        Origin Rules:Edit, Config Rules:Edit, Zone:Read.

CLI:
  python3 scripts/cloudflare.py zones
  python3 scripts/cloudflare.py dns
  python3 scripts/cloudflare.py rules http_request_origin
  python3 scripts/cloudflare.py rules http_config_settings
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.cloudflare.com/client/v4"
TIMEOUT = 60

# Rulesets phases. Origin rules rewrite where Cloudflare connects; config rules
# override zone settings per-hostname.
PHASE_ORIGIN = "http_request_origin"
PHASE_CONFIG = "http_config_settings"

PHASE_NAMES = {
    PHASE_ORIGIN: "origin rules",
    PHASE_CONFIG: "configuration rules",
}


class CloudflareError(RuntimeError):
    pass


class Zone:
    """One zone, resolved by name (or the only zone the token can see)."""

    def __init__(self, name=None, token=None):
        self.token = token or os.environ.get("CLOUDFLARE_API_TOKEN")
        if not self.token:
            raise CloudflareError(
                "CLOUDFLARE_API_TOKEN is not set. It belongs in ~/.zshenv next "
                "to the PTERO_* vars -- never in this repo, which is public."
            )
        self.name, self.id = self._resolve(name)

    # --- plumbing ---------------------------------------------------------

    def request(self, path, method="GET", body=None, params=None):
        url = API + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                payload = json.load(r)
        except urllib.error.HTTPError as e:
            try:
                payload = json.loads(e.read().decode())
            except (ValueError, OSError):
                raise CloudflareError(f"{method} {path} -> {e.code}") from None
            raise CloudflareError(
                f"{method} {path} -> {e.code}: " + _messages(payload)
            ) from None
        if not payload.get("success", False):
            raise CloudflareError(f"{method} {path}: " + _messages(payload))
        return payload["result"]

    def zpath(self, suffix=""):
        return f"/zones/{self.id}{suffix}"

    def _resolve(self, name):
        zones = self.request("/zones", params={"name": name} if name else None)
        if not zones:
            raise CloudflareError(f"token cannot see zone {name!r}")
        if name is None and len(zones) > 1:
            raise CloudflareError(
                "token sees multiple zones; pass one explicitly: "
                + ", ".join(z["name"] for z in zones)
            )
        return zones[0]["name"], zones[0]["id"]

    def plan(self):
        return self.request(self.zpath())["plan"]["name"]

    # --- dns --------------------------------------------------------------

    def dns_records(self, **filters):
        return self.request(self.zpath("/dns_records"), params=filters or None)

    def upsert_dns_record(self, name, type, content, proxied=True, ttl=1, comment=None):
        """Create or update a record. Returns (record, "created"|"updated"|"unchanged")."""
        existing = [r for r in self.dns_records(name=name) if r["type"] == type]
        body = {
            "type": type,
            "name": name,
            "content": content,
            "proxied": proxied,
            # ttl must be 1 ("automatic") while proxied; Cloudflare rejects
            # anything else on a proxied record.
            "ttl": 1 if proxied else ttl,
        }
        if comment:
            body["comment"] = comment
        if not existing:
            return self.request(self.zpath("/dns_records"), "POST", body), "created"
        rec = existing[0]
        same = all(rec.get(k) == v for k, v in body.items() if k != "comment")
        if same:
            return rec, "unchanged"
        return (
            self.request(self.zpath(f"/dns_records/{rec['id']}"), "PUT", body),
            "updated",
        )

    # --- rulesets ---------------------------------------------------------

    def entrypoint(self, phase):
        """The zone's entrypoint ruleset for `phase`, or None if it has none."""
        try:
            return self.request(self.zpath(f"/rulesets/phases/{phase}/entrypoint"))
        except CloudflareError as e:
            if "404" in str(e) or "does not exist" in str(e).lower():
                return None
            raise

    def rules(self, phase):
        ruleset = self.entrypoint(phase)
        return ruleset.get("rules", []) if ruleset else []

    def upsert_rule(self, phase, rule):
        """Create or replace a rule, keyed on its `ref`. Returns the verb used.

        `ref` is Cloudflare's stable rule identifier -- matching on it means
        re-running this never stacks up duplicate rules.
        """
        ref = rule.get("ref")
        if not ref:
            raise CloudflareError("rule needs a 'ref' so it can be matched on re-run")

        ruleset = self.entrypoint(phase)
        if ruleset is None:
            self.request(
                self.zpath("/rulesets"),
                "POST",
                {
                    "name": f"digbuild {PHASE_NAMES.get(phase, phase)}",
                    "kind": "zone",
                    "phase": phase,
                    "rules": [rule],
                },
            )
            return "created"

        for existing in ruleset.get("rules", []):
            if existing.get("ref") == ref:
                if _rule_matches(existing, rule):
                    return "unchanged"
                self.request(
                    self.zpath(f"/rulesets/{ruleset['id']}/rules/{existing['id']}"),
                    "PATCH",
                    rule,
                )
                return "updated"

        self.request(self.zpath(f"/rulesets/{ruleset['id']}/rules"), "POST", rule)
        return "created"


    def delete_rule(self, phase, ref):
        """Drop a rule by ref. Returns True if one was there."""
        ruleset = self.entrypoint(phase)
        if not ruleset:
            return False
        for rule in ruleset.get("rules", []):
            if rule.get("ref") == ref:
                self.request(
                    self.zpath(f"/rulesets/{ruleset['id']}/rules/{rule['id']}"),
                    "DELETE",
                )
                return True
        return False


def _rule_matches(existing, wanted):
    return all(existing.get(k) == v for k, v in wanted.items() if k != "ref")


def _messages(payload):
    parts = []
    for e in payload.get("errors", []) or []:
        msg = e.get("message", "")
        chain = e.get("error_chain") or []
        for c in chain:
            msg += f" ({c.get('message')})"
        parts.append(msg)
    return "; ".join(parts) or json.dumps(payload)[:300]


def _main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "zones":
        # Deliberately before Zone() so it also works with a multi-zone token.
        token = os.environ.get("CLOUDFLARE_API_TOKEN")
        z = Zone.__new__(Zone)
        z.token = token
        for r in z.request("/zones"):
            print(r["name"], r["id"], r["status"], r["plan"]["name"])
        return 0

    z = Zone(args[0] if cmd == "dns" and args else None)
    if cmd == "dns":
        for r in z.dns_records():
            flag = "proxied" if r["proxied"] else "dns-only"
            print(f"{r['type']:<6} {r['name']:<28} {flag:<9} {r['content']}")
    elif cmd == "rules":
        phase = args[0] if args else PHASE_ORIGIN
        rules = z.rules(phase)
        if not rules:
            print(f"(no {PHASE_NAMES.get(phase, phase)})")
        for r in rules:
            print(f"{r.get('ref') or r['id']}: {r['expression']}")
            print(f"    {r['action']} {json.dumps(r.get('action_parameters', {}))}")
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(_main(sys.argv[1:]))
    except CloudflareError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
