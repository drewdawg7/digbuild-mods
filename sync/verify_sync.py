#!/usr/bin/env python3
"""Exercise digbuild-sync against a throwaway game directory.

There is no way to unit-test "Forge picks up the jar we just downloaded", but
everything before that point -- the manifest, the hash diff, what gets deleted
and what is left alone -- is ordinary file work, and that is what this covers.
SyncCore has a main() for exactly this reason.

The jars served here are real zips with a real META-INF/mods.toml, because the
collision rule reads mod ids out of them; a stub file would pass a test the
release could not.

  python3 sync/build_mod.py && python3 sync/verify_sync.py
"""
import functools
import hashlib
import http.server
import pathlib
import shutil
import subprocess
import sys
import tempfile
import threading
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "patch"))
import build_mod as heappatch  # noqa: E402  (for the Java 17 toolchain)

CLASSES = HERE / "build" / "mod"
LIB = HERE / "lib"

failures = []


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f" -- {detail}" if detail and not ok else ""))
    if not ok:
        failures.append(label)


def java():
    javac = heappatch.javac()
    return javac.parent / "java"


def make_jar(path, mod_id, marker=""):
    """A minimal but genuine Forge mod jar."""
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("META-INF/mods.toml", f'modLoader="javafml"\n\n[[mods]]\nmodId="{mod_id}"\n')
        z.writestr("marker.txt", marker)
    return path


def sha1(path):
    h = hashlib.sha1()
    h.update(path.read_bytes())
    return h.hexdigest()


def serve(directory):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass  # the request log is noise next to the check results

    handler = functools.partial(Quiet, directory=str(directory))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}"


def write_manifest(path, base_url, jars):
    rows = ["#digbuild-sync 1"]
    for jar in jars:
        rows.append(f"{sha1(jar)}\t{jar.stat().st_size}\t{jar.name}\t{base_url}/{jar.name}")
    path.write_text("\n".join(rows) + "\n")


def write_config(game, manifest_url, enabled=True, remove_dropped=True):
    (game / "config").mkdir(parents=True, exist_ok=True)
    (game / "config" / "digbuild-sync.properties").write_text(
        f"enabled = {str(enabled).lower()}\n"
        f"manifest = {manifest_url}\n"
        f"remove_dropped = {str(remove_dropped).lower()}\n"
        "timeout_seconds = 10\n"
        # Off, or every run of this opens a window on a developer's desktop.
        "progress_window = false\n"
    )


def run(game):
    cp = [str(CLASSES)] + [str(p) for p in sorted(LIB.glob("*.jar"))]
    r = subprocess.run(
        [str(java()), "-cp", ":".join(cp), "digbuild.sync.SyncCore", str(game)],
        capture_output=True, text=True,
    )
    if r.returncode:
        print(r.stdout + r.stderr, file=sys.stderr)
        raise SystemExit("SyncCore exited non-zero")
    return r.stdout


def main():
    if not CLASSES.exists():
        raise SystemExit("run: python3 sync/build_mod.py")

    root = pathlib.Path(tempfile.mkdtemp(prefix="digbuild-sync-"))
    try:
        published = root / "published"
        published.mkdir()
        game = root / "game"
        mods = game / "mods"
        mods.mkdir(parents=True)

        # What the pack publishes.
        keep = make_jar(published / "keep-1.0.jar", "keep")
        newer = make_jar(published / "bumped-2.0.jar", "bumped", "v2")
        added = make_jar(published / "added-1.0.jar", "added")

        # What the player has: the matching jar, the *old* version of the
        # bumped one, and a mod of their own that the pack knows nothing about.
        shutil.copy(keep, mods / keep.name)
        make_jar(mods / "bumped-1.0.jar", "bumped", "v1")
        mine = make_jar(mods / "sodium-alike.jar", "playersown")
        mine_hash = sha1(mine)

        httpd, base = serve(published)
        manifest = published / "mods-manifest.tsv"
        write_manifest(manifest, base, [keep, newer, added])
        url = f"{base}/mods-manifest.tsv"

        print("first run (adopt, download, replace):")
        write_config(game, url)
        run(game)
        check("new mod downloaded", (mods / "added-1.0.jar").exists())
        check("bumped mod downloaded", (mods / "bumped-2.0.jar").exists())
        check("superseded jar moved out of mods/", not (mods / "bumped-1.0.jar").exists())
        check("superseded jar set aside, not destroyed",
              (mods / ".digbuild-sync-disabled" / "bumped-1.0.jar").exists())
        check("unchanged jar left alone", (mods / "keep-1.0.jar").exists())
        check("player's own mod untouched",
              (mods / "sodium-alike.jar").exists() and sha1(mods / "sodium-alike.jar") == mine_hash)
        check("downloaded content is correct", sha1(mods / "added-1.0.jar") == sha1(added))
        check("staging directory cleaned up", not (mods / ".digbuild-sync").exists())

        print("second run (nothing to do):")
        out = run(game)
        check("reports already in sync", "already matches the manifest" in out, out)

        print("second bump (this one is ours, so it is deleted):"  )
        # bumped-2.0 was installed by the sync, so bumped-3.0 replacing it is
        # housekeeping on our own file rather than a player's.
        newer3 = make_jar(published / "bumped-3.0.jar", "bumped", "v3")
        write_manifest(manifest, base, [keep, newer3, added])
        run(game)
        check("managed predecessor deleted outright",
              not (mods / "bumped-2.0.jar").exists()
              and not (mods / ".digbuild-sync-disabled" / "bumped-2.0.jar").exists())
        check("replacement installed", (mods / "bumped-3.0.jar").exists())

        print("mod dropped from the pack:")
        write_manifest(manifest, base, [keep, newer3])
        run(game)
        check("dropped mod removed", not (mods / "added-1.0.jar").exists())
        check("player's own mod still untouched", (mods / "sodium-alike.jar").exists())

        print("corrupt download:")
        # Same row, wrong hash: the jar must not land in mods/.
        rows = manifest.read_text().splitlines()
        rows.append("%s\t%d\t%s\t%s/%s" % ("0" * 40, added.stat().st_size, added.name, base, added.name))
        manifest.write_text("\n".join(rows) + "\n")
        run(game)
        check("sha1 mismatch is not installed", not (mods / "added-1.0.jar").exists())
        check("staging left no .part behind",
              not list(mods.glob(".digbuild-sync/*")) )

        print("this jar does not update itself:")
        # A newer digbuild-sync in the manifest, an older one on disk. Neither
        # the download nor the mod-id collision may fire: replacing the running
        # service jar is impossible on Windows, and a second one would mean two
        # services doing this work.
        make_jar(mods / "digbuild-sync-1.0.0.jar", "digbuildsync")
        newer_self = make_jar(published / "digbuild-sync-9.9.9.jar", "digbuildsync")
        write_manifest(manifest, base, [keep, newer3, newer_self])
        run(game)
        check("newer copy of itself not downloaded", not (mods / "digbuild-sync-9.9.9.jar").exists())
        check("running copy of itself not removed", (mods / "digbuild-sync-1.0.0.jar").exists())

        print("disabled:")
        write_manifest(manifest, base, [keep, newer3, added])
        write_config(game, url, enabled=False)
        out = run(game)
        check("does nothing when disabled",
              not (mods / "added-1.0.jar").exists() and "disabled in config" in out, out)

        print("unreachable host:")
        httpd.shutdown()
        write_config(game, url)
        before = sorted(p.name for p in mods.glob("*.jar"))
        out = run(game)
        check("offline leaves mods/ alone", sorted(p.name for p in mods.glob("*.jar")) == before)
        check("offline is a warning, not a crash", "leaving mods/ alone" in out, out)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print()
    if failures:
        print(f"{len(failures)} failed: " + ", ".join(failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
