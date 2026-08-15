# digbuild-mods

Auto-published mod pack for the **digbuild** Minecraft server (Forge 1.20.1,
Forge 47.4.10, 148 mods). The game server runs on PebbleHost behind a
Pterodactyl panel; this repo mirrors its `mods/` folder and publishes a
password-protected zip as a GitHub Release whenever the mod set changes.

Players connect at **`minecraft.abcdefc.gg`**; the server wiki is at
**`wiki.abcdefc.gg`**.

> **This repository is public.** Never commit API keys, the Pterodactyl server
> ID, the raw allocation IP/port, or the zip password. They belong in
> environment variables (locally) and GitHub Actions secrets/variables (in CI).
> The two hostnames above are public by design and fine to include.

## Layout

| Path | What it is |
|---|---|
| `scripts/sync_mods.py` | Mirrors the server's `/mods` into `./mods`, diffing against `manifest.json` |
| `manifest.json` | `name -> {size, modified}` for every published jar. Source of truth for "what changed" |
| `agent/` | `digbuild-modsync` — a small Forge mod that runs on the game server and fires a `repository_dispatch` when `mods/` changes |
| `.github/workflows/publish-mods.yml` | Sync → zip → release → prune |
| `patch/` | `digbuild-heappatch` — a server-only Forge mod carrying fixes that can only be applied from inside the JVM (see **Heap sizing** below) |
| `scripts/setup_squaremap.py` | Installs/configures the web map |
| `.claude/docs/` | Mod reference documentation (see below) |

`mods/`, `mods-latest.zip` and `CHANGES.md` are gitignored — the 466 MB mirror
lives in the Actions cache, never in git.

## Connecting to the game server

The server is administered through the **Pterodactyl client API** on PebbleHost.
Everything below is the client API (`/api/client/...`), which is what a normal
account API key can reach — not the application/admin API.

### Credentials

Three environment variables, exported in `~/.zshenv` locally:

| Variable | Value | Notes |
|---|---|---|
| `PTERO_PANEL` | `https://panel.pebblehost.com` | panel base URL |
| `PTERO_SERVER` | short server id (8 hex chars) | the identifier in the panel URL |
| `PTERO_KEY` | `ptlc_…` | **client** API key, created under Account → API Credentials |

They live in `~/.zshenv` rather than `~/.zshrc` deliberately: non-interactive
shells and scripts do not source `.zshrc`, so `sync_mods.py` would not see them
there.

In CI the same three come from `vars.PTERO_PANEL`, `vars.PTERO_SERVER` and
`secrets.PTERO_KEY`.

### Request shape

```
GET {PTERO_PANEL}/api/client/servers/{PTERO_SERVER}/{endpoint}
Authorization: Bearer {PTERO_KEY}
Accept: application/json
```

### Endpoints that are known to work

Verified against this server:

| Endpoint | Query param | Returns |
|---|---|---|
| `GET /api/client` | — | all servers on the account |
| `` (server root) | — | server details, limits, allocations |
| `resources` | — | live state, CPU, memory, disk, network |
| `files/list` | `directory=/path` | directory listing |
| `files/contents` | **`file`**`=/path` | raw file contents inline |
| `files/download` | **`file_path`**`=/path` | JSON containing a signed one-shot URL |
| `websocket` | — | JWT + socket URL for the live console |

> **PebbleHost quirk — the parameter name differs per endpoint.**
> `files/contents` takes `file=`, but `files/download` rejects `file=`
> (`422 The file path field is required`) and requires **`file_path=`**.
> Stock Pterodactyl uses `file` for both. `scripts/sync_mods.py` already
> accounts for this; anything new that downloads files must too.

`files/download` returns a *signed URL*, not the bytes — fetch the URL from
`attributes.url` in the response, unauthenticated, as a second request.

### Example

```python
import json, os, urllib.parse, urllib.request

P, S, K = os.environ["PTERO_PANEL"].rstrip("/"), os.environ["PTERO_SERVER"], os.environ["PTERO_KEY"]
H = {"Authorization": f"Bearer {K}", "Accept": "application/json"}

def api(path, params=None):
    url = f"{P}/api/client/servers/{S}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120))

# list the mods folder
for item in api("files/list", {"directory": "/mods"})["data"]:
    print(item["attributes"]["name"])

# download a file (two steps: signed url, then fetch it)
signed = api("files/download", {"file_path": "/config/alexscaves-general.toml"})
data = urllib.request.urlopen(signed["attributes"]["url"], timeout=120).read()
```

### Useful paths on the server

```
/mods                              installed jars
/config                            per-mod configs
/config/<mod>/                     some mods use a subdirectory
/logs/latest.log                   current session log
/logs/*.log.gz                     rotated logs
/world                             world data
/server.properties                 difficulty, view distance, seed, etc.
/datapacks  /defaultconfigs        currently empty
/modsync.properties                the in-server agent's config (holds a token — do not print)
```

### State-changing endpoints

`POST .../power` (start/stop/restart/kill) and `POST .../command` exist and the
key can reach them. **Do not call them without asking** — players may be online.
Check `resources` for `state` and player activity first.

## Heap sizing

**You cannot pass JVM flags to this server from outside.** Both routes were
tried and both are dead:

- the panel's `LOADER_STARTUPFLAGS` variable is accepted by the UI and silently
  dropped;
- Forge's `user_jvm_args.txt` is not read either.

PebbleHost's `/opt/start.sh` builds the java command itself, and `/opt` is
outside the container so it cannot be inspected. The JVM actually runs with:

```
-Xmx<box>M -Xms128M -XX:MaxDirectMemorySize=256M -XX:MaxMetaspaceSize=1024M
-XX:MaxRAMPercentage=90.0 -Djava.awt.headless=true
```

Do not trust the panel here — check what the JVM really got. spark records the
full command line in its dump metadata, so any `.sparkheap` or `.sparkprofile`
answers it:

```
python3 scripts/ptero.py get /config/spark/<newest>.sparkheap ./x.sparkheap
# then grep the decompressed bytes for -Xmx
```

This matters because G1's stock `MaxHeapFreeRatio` is 70, which pins committed
heap at roughly `live / 0.30` and never returns it — measured at 2,736 MB
committed against 812 MB live, unmoved by a full GC. That gap is JVM sizing
policy; nothing inside the game reaches it.

So `digbuild-heappatch` sets the flags at runtime instead, via
`HotSpotDiagnosticMXBean`. `MinHeapFreeRatio`, `MaxHeapFreeRatio` and
`G1PeriodicGCInterval` are all *manageable* HotSpot flags, which is the category
that may be written while running — a supported API, not a trick. It logs the
value it reads back after each write, so a flag that silently refuses is visible
rather than assumed. Setting the ratio to 25 took the container from ~5.4 GB to
~2.1 GB with no other change.

## Public addresses

| | |
|---|---|
| Game server | `minecraft.abcdefc.gg` |
| Wiki | `wiki.abcdefc.gg` |
| Web map | `map.abcdefc.gg` |

All three are public-facing and safe to share with players. The raw allocation
IP/port behind `minecraft.abcdefc.gg` is in the PebbleHost panel and is
deliberately not recorded here — always hand out the hostname, so the
underlying allocation can change without breaking anyone.

`scripts/setup_cloudflare_map.py` authenticates with `CLOUDFLARE_API_TOKEN`
from `~/.zshenv`. That token is **DNS-scoped and 403s on every Workers
endpoint**; the wiki repo deploys with `CLOUDFLARE_WORKERS_TOKEN`, a second
token in the same file. Keep them separate rather than widening one.

The map is **squaremap** on the second allocation (port 8034), fronted by
Cloudflare via that script. It replaced Dynmap, which
replaced BlueMap. Both predecessors failed on this pack for rendering reasons,
not performance ones: BlueMap smeared meshes, and Dynmap could not convert
rotated block models — 16,327 `Invalid modellist patch` lines per boot, 96% of
the entire log, and one line per box *per face*. squaremap draws top-down from
each block's built-in map colour, so there is no model conversion to fail and
modded blocks need no scanning step. The trade is that it is flat: no isometric
views, and the Forge line is frozen at 1.2.0 (2023-09-15) because upstream moved
to NeoForge.

The wiki is the player-facing destination for the mod documentation in
`.claude/docs/`.

## The publish pipeline

1. `digbuild-modsync` (in `agent/`) runs inside the game server JVM and
   fingerprints `mods/` once at boot.
2. On change it fires a `repository_dispatch` (`mods-changed`) at this repo,
   using a GitHub PAT stored in `/modsync.properties` on the server.
3. `publish-mods.yml` restores the cached mirror, runs `scripts/sync_mods.py`,
   and exits early if nothing changed.
4. If something changed: builds a password-protected zip (`ZIP_PASSWORD`
   secret), publishes a release, re-saves the cache, commits `manifest.json`,
   and prunes to the 5 most recent releases.

`sync_mods.py` refuses to continue if the remote listing comes back empty —
that guard exists so an API hiccup cannot wipe the mirror and publish an empty
pack. Keep it.

`EXCLUDE_PREFIXES` in `sync_mods.py` keeps server-only jars (currently
`digbuild-modsync`) out of the player-facing pack.

## Mod documentation

`.claude/docs/` holds reference docs for mods on the server, generated from the
actual jars and live config rather than from memory. Currently covers **Alex's
Caves 2.0.2**, **Alex's Mobs 1.22.9** and **Farmer's Delight 1.3.2**, plus their
add-ons — see
`.claude/docs/README.md` for the index and provenance notes.

When documenting a mod, the house rule is: read the primary source. Pull the jar
off the server, unzip it for the data-driven content (`data/`, `assets/`), and
decompile it for anything behavioural. Registry IDs come from the
`register("…")` calls, not from Java field names — those differ more often than
you would expect.

Two habits that caught real errors while writing the Alex's Mobs docs, both
worth repeating:

- **Set-diff `register()` literals against lang keys; never count files.** A
  count says "19 effects but 20 files" and sends you hunting a missing
  translation that does not exist. The diff says the 20th file is a
  `BrewingRecipe`. Related trap: these mods override `getDescriptionId()`, so an
  effect's display name lives under `alexsmobs.potion.*` and a grep for
  `effect.alexsmobs.*` will never find it.
- **A config default is what `CommonConfig` passes to `buildInt`, not the
  `AMConfig` static field.** The static initialisers are dead and overwritten on
  load. Diffing live values against them reports deviations that are not real.

## Conventions

- Python 3, standard library only. `sync_mods.py` deliberately has no
  dependencies so the workflow needs no install step.
- Comments explain *why*, not *what*. Match the existing terse style.
- Don't commit jars or the mirror.
