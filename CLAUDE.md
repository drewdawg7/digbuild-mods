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
| `sync/` | `digbuild-sync` — the **client-side** updater: downloads the published zip at launch and extracts what the player is missing (see **Client mod sync** below) |
| `tweaks/` | `digbuild-tweaks` — a server-only Forge mod holding this pack's gameplay tweaks, each config-driven and reloadable in place (see **Gameplay tweaks** below) |
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

## Gameplay tweaks

`digbuild-tweaks` is where a gameplay change goes when the thing it changes is
**code rather than data** and no config in the pack reaches it. Server-only:
every check these override runs on the server, so players need nothing and the
jar is excluded from the published pack. Deliberately not more mixins in
`digbuild-heappatch` — that one is JVM and cache behaviour and would apply to
any pack; this is specific to ours.

Each tweak is a `Tweak` subclass owning one config file under
`/config/digbuild-tweaks/`. Adding one means: a class in
`src/digbuild/tweaks/tweak/`, an entry in `Tweaks.ALL`, and — if it needs a
mixin — the source in `build_mod.py`'s `SOURCES` and the class in
`digbuildtweaks.mixins.json`.

**Config edits do not need a restart.** `Tweaks` stats each config file every
200 ticks and re-runs that tweak when the mtime or size changes, so an edit made
through the panel is live within about ten seconds and the result — including
any id nothing registers — is logged. `apply()` must therefore be re-runnable:
it replaces what the previous call published rather than adding to it. Only
config is live; changing what a tweak *does* is a rebuild and a restart, because
mixins are applied by the class transformer when the target class is first
loaded and cannot be re-applied afterwards.

Build and deploy like the heap patch — `build_mod.py`, `verify_patch.py`, then
`deploy.py`, which restarts behind a rollback and refuses to run with players
online. A new tweak jar also needs its `EXCLUDE_PREFIXES` entry **pushed before
it is uploaded**; see **The publish pipeline** for why, and for what to do if it
went out anyway.

### enchant-applicability

Which items an enchantment may go on is code on 1.20.1. Vanilla's
`EnchantmentCategory.WEAPON` is literally `item instanceof SwordItem`, so
Looting, Fire Aspect, Knockback and every modded enchantment that reuses WEAPON
— `apotheosis:scavenger` among them — are sword-only by construction. Nothing
reaches it from outside: no datapack (enchantments only became data-driven in
1.21), and no config in this pack. Apotheosis' `enchantments.cfg` is per
enchantment but only covers levels, power, rarity and where it can be obtained.

`/config/digbuild-tweaks/enchant-applicability.properties`:

```
minecraft:looting = axe, trident
apotheosis:scavenger = axe, trident
apotheosis:knowledge = axe, trident
apotheosis:capturing = axe, trident
```

Those four are the whole default set, chosen from the 15 `WEAPON`-category
enchantments in the pack. All four were checked in the jars and read the
killer's main-hand stack, so they fire from an axe or a melee trident stab.
Majrusz's enchantments are deliberately excluded: they use a `Predicate` rather
than an `EnchantmentCategory` and `CustomEnchantment` overrides `canEnchant`, so
a rule would take at the enchanting table and not at the anvil — and their
`IS_MELEE` predicate already covers axes.

Targets are either an item-class alias (`axe`, `trident`, `sword`, `pickaxe`,
`shovel`, `hoe`), which picks up modded items of that class too, or an exact
item id. Rules only widen, so nothing there can take an enchantment away from an
item that already accepts it.

**The anvil and the enchanting table do not share a check** — this was traced
through the server's own jars, and patching only the obvious one puts an
enchantment on the anvil while leaving it off the table:

| Path | Calls |
|---|---|
| anvil, `/enchant` | `Enchantment.canEnchant` (`m_6081_`), whose default is `this.category.canEnchant(item)` |
| enchanting table | `Enchantment.canApplyAtEnchantingTable` (Forge's own), which bounces through `ItemStack` to `IForgeItem`'s default — and that reads `enchantment.category` **directly**, never `canEnchant` |

So the mixin injects into both, at HEAD, cancelling only with `true`.

Two things it deliberately does not do:

- **It cannot reach an enchantment that overrides those methods.** Vanilla's
  `DamageEnchantment` is the stock example: it overrides `canEnchant` so axes
  take Sharpness without any category change. Nothing on the default allowlist
  overrides either method, and a note is logged if one starts to — otherwise the
  rule is accepted, logged as active, and silently does nothing.
- **It only moves the applicability check.** Whether the enchantment then does
  anything is up to the enchantment. The defaults all read the killer's
  main-hand stack, so they work from an axe or a melee trident stab, but a
  thrown trident is not in the hand when the mob dies and no main-hand
  enchantment applies to the throw. `minecraft:sweeping` is left out for the
  same reason: its effect is gated on the sweep attack, which Forge grants only
  to items answering `ToolActions.SWORD_SWEEP`.

The boot log lists every sword-only enchantment on the server, which is where to
look for more to add rather than unzipping jars.

### craft-carryover

Vanilla builds a crafted item from the recipe alone — `assemble()` is literally
`this.result.copy()` — and ingredients are matched by item id, NBT ignored. So
every "consume a vanilla piece to make a modded one" recipe in this pack eats
whatever the piece was carrying. `armoroftheages:raijin_armor_head` is the case
that surfaced it: gold + a `minecraft:netherite_helmet`, and an affixed,
socketed helmet goes in while a plain Raijin helmet comes out.

This tweak copies chosen root NBT keys from an ingredient onto the result.
Apotheosis keeps affixes, rarity, name, category, socket count and gems in one
compound, `affix_data`, so that single key is the whole fix and is the default.
Adding `Enchantments` to `tags` carries those too.

The rolled name comes across with it, which is what you want:
`affix_data.name` is a *translatable template*, and Apotheosis'
`ItemStackMixin.apoth_affixItemName` substitutes the stack's own hover name into
it at render time — so the result reads "Spellshielded **Raijin Helmet** of
Darkness", not the netherite helmet's name.

Four rules, three of them fixed because each closes a hole:

- the result must be a single item, or one affixed input pays for a whole stack
- exactly one ingredient may carry the tags; two is ambiguous, so none is copied
- a tag the result already has is never overwritten
- `same_slot_only` (configurable, default true) requires source and result to be
  worn in the same slot. Affix modifiers are rolled for the slot the item was
  found in, so turning it off is how a sword ends up granting armour. Non-armour
  all reports as main hand, so weapon-to-weapon still works.

**The injection point is the recipe, not the menu.** FastWorkbench `@Overwrite`s
`CraftingMenu.slotsChanged` and routes the grid through its own
`FastBenchUtil.slotChangedCraftingGrid`, so an injector on vanilla's
`CraftingMenu.slotChangedCraftingGrid` never fires for a crafting table here.
`ShapedRecipe`/`ShapelessRecipe.assemble` is upstream of all of it — vanilla
menus, FastWorkbench, JEI transfer, automation — and the result slot previews
what it returns, so the affixes are visible before the craft rather than
appearing on take. Both types return `this.result.copy()`, so mutating the
returned stack cannot touch the recipe's own template. The bridge overload
taking a plain `Container` is deliberately not targeted; hooking both would
apply the carryover twice.

Note this is a balance decision, not just a fix: it makes every such recipe an
upgrade path rather than a sink, pack-wide.

## Client mod sync

`digbuild-sync` saves players re-downloading the zip by hand. At launch it
fetches the published pack, extracts the jars the player does not already have,
and lets the game carry on booting.

**It reads the same zip the wiki hands out**, at
`/releases/latest/download/mods-latest.zip`, with the password that is printed
on the install page. Nothing about publishing changed to accommodate it — no
manifest, no second artifact, no extra workflow step. If the pipeline publishes
a release, this picks it up.

**It is a ModLauncher service, not a Forge mod**, because a mod cannot add mods
— Forge builds its mod list during boot and opens every jar, and nothing may
join that list afterwards. `ModDirTransformerDiscoverer` scans `mods/` for jars
declaring `META-INF/services/cpw.mods.modlauncher.api.ITransformationService`
and hoists them onto the boot layer *before* `ModsFolderLocator` lists the
directory, so a jar extracted there loads on the same launch. No restart, and no
fighting Windows over a jar the game already holds open — nothing has opened
`mods/` yet.

Three ordering facts, all read out of Forge 47.4.10 and modlauncher 10.0.9
rather than assumed, because the whole design rests on them:

| Fact | Where |
|---|---|
| Service jars in `mods/` are loaded before mod discovery | `ModDirTransformerDiscoverer.scan` |
| …and are then skipped by mod discovery, so they need no `mods.toml` | `ModsFolderLocator` vs `ModDirTransformerDiscoverer.allExcluded()` |
| `GAMEDIR`/`LAUNCHTARGET` are set after every `onLoad` and before every `initialize`; `beginScanning` is after both | `TransformationServicesHandler.initializeTransformationServices` |

That last one is why the work happens in `initialize` and not `onLoad` — the
game directory is not in the environment yet during `onLoad`.

Consequences worth knowing before changing any of it:

- **No in-game UI.** One jar cannot be both a service and a mod, so there is no
  main-menu button; the switch is `enabled` in
  `config/digbuild-sync.properties`, written with defaults on first launch.
- **Nothing here may touch a Minecraft or Forge class.** The game's class loader
  does not exist yet. Stdlib only, and that is a constraint rather than taste.
- **It does not update itself.** Its own jar is open on the boot layer by the
  time its code runs, so it skips its own entry in the zip. A new
  `digbuild-sync` reaches players in the zip, downloaded by hand once.
- **It ships inside the pack**, so it also sits in the game server's `/mods`.
  `DigbuildSyncService` checks `LAUNCHTARGET` and does nothing server-side.

### Reading the zip

`java.util.zip` cannot open the pack: the workflow builds it with
`7z -mem=ZipCrypto`, and `ZipFile` refuses an encrypted entry. So `EncryptedZip`
walks the central directory by hand — that part is plain — and implements
PKWARE's original stream cipher for the entry data. Weak encryption, and
irrelevantly so: the password is published on the wiki, and the point is
packaging rather than secrecy.

Every entry carries a CRC, which does double duty: it is checked after
inflating, and it is what decides whether a jar already on disk is the same file
(size first, then CRC). No state of our own is needed for that comparison.

### What it deletes

Only what `remove-mods.txt` names — the list the pipeline already maintains and
the wiki already tells players to action by hand. Extracting a zip adds and
overwrites but never removes, and a leftover jar is sometimes a boot failure
rather than dead weight. A mod the player added is not on that list and is never
touched.

That inherits the caveat already on `remove-mods.txt`: a client-side library the
server dropped may still be holding up a mod the player added, and this removes
it without asking.

### Rebuilding

```bash
python3 sync/build_mod.py     # -> sync/digbuild-sync-1.0.0.jar
```

Deploying is unlike the other digbuild jars: it goes into the server's `/mods`
like an ordinary mod and the existing pipeline publishes it. There is no
exclusion to push first, because it is meant to ship.

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

`EXCLUDE_PREFIXES` in `sync_mods.py` keeps server-only jars out of the
player-facing pack — currently `digbuild-modsync`, `digbuild-heappatch`,
`digbuild-tweaks`, `squaremap` and `spark`. **`digbuild-sync` is deliberately
not on that list**: it is the one digbuild jar players need, and it lives in the
server's `/mods` only so this pipeline carries it into the zip.

> **Push the exclusion before the jar reaches `/mods`.** CI checks out `origin`
> and runs *that* copy of `sync_mods.py`, never the one on your laptop, and the
> agent fires on the first boot after any change to `/mods`. So a server-only
> jar uploaded while its `EXCLUDE_PREFIXES` entry is still an uncommitted local
> edit gets picked up by a workflow that has never heard of it, zipped, and
> released to every player. That is exactly how `digbuild-tweaks-1.0.0.jar`
> ended up in release `mods-20260821-230123`.
>
> Order is: commit and push the exclusion, *then* upload the jar. This is the
> one part of a server-only mod's deploy that is not local — the build, the
> verify and the upload all are, which is what makes it easy to forget.
>
> To recover once it has shipped: push the exclusion, then
> `gh workflow run publish-mods.yml`. The next sync sees the jar as removed,
> drops it from `manifest.json` and publishes a corrected pack. Doing nothing
> also works eventually — any later mod change republishes without it — but the
> bad release stays downloadable until the 5-release prune ages it out.

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
