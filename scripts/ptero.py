#!/usr/bin/env python3
"""Pterodactyl client-API wrapper for the digbuild server on PebbleHost.

Everything here is the *client* API (/api/client/...), which is all a normal
account key can reach. Import this rather than hand-rolling requests -- the
per-endpoint parameter quirks below are easy to get wrong.

Env:
  PTERO_PANEL   panel base url, e.g. https://panel.pebblehost.com
  PTERO_SERVER  short server id
  PTERO_KEY     client api key (ptlc_...)

CLI (handy for the "read the primary source" workflow -- pull a jar or a
config off the server and inspect it locally):

  python3 scripts/ptero.py ls /mods
  python3 scripts/ptero.py cat /server.properties
  python3 scripts/ptero.py get /mods/some.jar ./some.jar
  python3 scripts/ptero.py put ./local.jar /mods
  python3 scripts/ptero.py ports
"""
import json
import mimetypes
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

TIMEOUT = 120
USER_AGENT = "digbuild-tools"

DIRECTORY_MIME = "inode/directory"


class PteroError(RuntimeError):
    pass


def _env(name):
    try:
        return os.environ[name]
    except KeyError:
        raise PteroError(
            f"{name} is not set. The three PTERO_* vars live in ~/.zshenv "
            "locally and in Actions vars/secrets in CI."
        ) from None


class Panel:
    """A single server on the panel."""

    def __init__(self, panel=None, server=None, key=None):
        self.panel = (panel or _env("PTERO_PANEL")).rstrip("/")
        self.server = server or _env("PTERO_SERVER")
        self.key = key or _env("PTERO_KEY")

    # --- plumbing ---------------------------------------------------------

    def _url(self, path, params=None):
        url = f"{self.panel}/api/client/servers/{self.server}/{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return url

    def _headers(self, extra=None):
        h = {
            "Authorization": f"Bearer {self.key}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if extra:
            h.update(extra)
        return h

    def request(self, path, params=None, method="GET", body=None, headers=None):
        """Raw request. Returns decoded JSON, or None for empty 204 bodies."""
        data = None
        extra = dict(headers or {})
        if body is not None:
            if isinstance(body, (bytes, bytearray)):
                data = bytes(body)
            else:
                data = json.dumps(body).encode()
                extra.setdefault("Content-Type", "application/json")
        req = urllib.request.Request(
            self._url(path, params),
            data=data,
            method=method,
            headers=self._headers(extra),
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf8", "replace")[:400]
            raise PteroError(f"{method} {path} -> {e.code}: {detail}") from None
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    def get(self, path, params=None):
        return self.request(path, params)

    # --- server state -----------------------------------------------------

    def details(self):
        return self.get("")["attributes"]

    def resources(self):
        return self.get("resources")["attributes"]

    def state(self):
        return self.resources()["state"]

    def is_running(self):
        return self.state() == "running"

    # --- files ------------------------------------------------------------

    def list_dir(self, directory):
        """[attributes] for every entry in `directory`."""
        items = self.get("files/list", {"directory": directory})["data"]
        return [i["attributes"] for i in items]

    @staticmethod
    def is_dir(entry):
        # `is_file` is not always present in PebbleHost's responses; `mime` is.
        return entry.get("mime") == DIRECTORY_MIME

    def exists(self, path):
        parent, _, name = path.rstrip("/").rpartition("/")
        try:
            return any(e["name"] == name for e in self.list_dir(parent or "/"))
        except PteroError:
            return False

    def read_file(self, path):
        """File contents as text. This endpoint takes `file`."""
        raw = self.request("files/contents", {"file": path})
        return raw.decode("utf8", "replace") if isinstance(raw, bytes) else raw

    def write_file(self, path, content):
        """Overwrite (or create) a text file."""
        if isinstance(content, str):
            content = content.encode()
        # Stock Pterodactyl takes `file`; PebbleHost renames it on some
        # endpoints, so fall back rather than guess.
        try:
            return self.request(
                "files/write",
                {"file": path},
                method="POST",
                body=content,
                headers={"Content-Type": "text/plain"},
            )
        except PteroError as e:
            if "422" not in str(e):
                raise
            return self.request(
                "files/write",
                {"file_path": path},
                method="POST",
                body=content,
                headers={"Content-Type": "text/plain"},
            )

    def download(self, path, dest):
        """Download to `dest`. Two steps: signed url, then an unauthed fetch.

        PebbleHost's panel expects `file_path` here, not stock Pterodactyl's
        `file` -- `file` returns 422.
        """
        dest = pathlib.Path(dest)
        signed = self.get("files/download", {"file_path": path})["attributes"]["url"]
        tmp = dest.with_suffix(dest.suffix + ".part")
        with urllib.request.urlopen(signed, timeout=TIMEOUT) as r, open(tmp, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
        tmp.replace(dest)
        return dest

    def upload(self, local, directory, name=None):
        """Upload a local file into `directory`. Also two steps, like download."""
        local = pathlib.Path(local)
        name = name or local.name
        signed = self.get("files/upload", {"directory": directory})["attributes"]["url"]
        # The signed url does not carry the target directory; it must be re-sent.
        sep = "&" if "?" in signed else "?"
        url = signed + sep + urllib.parse.urlencode({"directory": directory})

        boundary = uuid.uuid4().hex
        ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
        body = b"".join([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="files"; filename="{name}"\r\n'.encode(),
            f"Content-Type: {ctype}\r\n\r\n".encode(),
            local.read_bytes(),
            f"\r\n--{boundary}--\r\n".encode(),
        ])
        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": USER_AGENT,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=max(TIMEOUT, 300)) as r:
                return r.status
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf8", "replace")[:400]
            raise PteroError(f"upload {name} -> {e.code}: {detail}") from None

    def delete(self, root, names):
        return self.request(
            "files/delete", method="POST", body={"root": root, "files": list(names)}
        )

    def mkdir(self, root, name):
        return self.request(
            "files/create-folder", method="POST", body={"root": root, "name": name}
        )

    # --- network ----------------------------------------------------------

    def allocations(self):
        return [a["attributes"] for a in self.get("network/allocations")["data"]]

    def create_allocation(self):
        """Claim another port from the host's pool (PebbleHost 'Additional Ports')."""
        return self.request("network/allocations", method="POST")["attributes"]

    # --- state-changing ---------------------------------------------------
    # Players may be online. Callers must ask a human first; see CLAUDE.md.

    def power(self, signal):
        if signal not in ("start", "stop", "restart", "kill"):
            raise PteroError(f"bad power signal: {signal}")
        return self.request("power", method="POST", body={"signal": signal})

    def send_command(self, command):
        return self.request("command", method="POST", body={"command": command})

    def java_major(self):
        """Major Java version of the server JVM, from the boot log.

        Worth checking before uploading any jar: Forge aborts the whole boot if
        a mod's class files are newer than the runtime, taking the server down.
        """
        m = re.search(r"java version (\d+)", self.read_file("/logs/latest.log"))
        return int(m.group(1)) if m else None

    def online_players(self):
        """Best-effort roster from latest.log -- the panel API does not expose it."""
        online = []
        for line in self.read_file("/logs/latest.log").splitlines():
            if " joined the game" in line:
                online.append(line.rsplit(": ", 1)[-1].replace(" joined the game", ""))
            elif " left the game" in line:
                who = line.rsplit(": ", 1)[-1].replace(" left the game", "")
                if who in online:
                    online.remove(who)
        return online


def _main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    cmd, args = argv[0], argv[1:]
    p = Panel()
    if cmd == "ls":
        for e in sorted(p.list_dir(args[0] if args else "/"), key=lambda e: e["name"]):
            kind = "d" if Panel.is_dir(e) else "-"
            print(f"{kind} {e['size']:>12} {e['modified']}  {e['name']}")
    elif cmd == "cat":
        print(p.read_file(args[0]), end="")
    elif cmd == "get":
        dest = args[1] if len(args) > 1 else pathlib.Path(args[0]).name
        print(p.download(args[0], dest))
    elif cmd == "put":
        print(p.upload(args[0], args[1]))
    elif cmd == "ports":
        for a in p.allocations():
            print(a["port"], "default" if a["is_default"] else "extra", a.get("notes") or "")
    elif cmd == "who":
        print("\n".join(p.online_players()) or "(nobody)")
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
