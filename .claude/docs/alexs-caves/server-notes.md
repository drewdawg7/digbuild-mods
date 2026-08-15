<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Server Notes

Server-specific findings for the digbuild PebbleHost server. Everything here was
observed on the live server, not inferred from the mod in isolation.

## Environment

| | |
|---|---|
| Platform | PebbleHost (Pterodactyl panel) |
| Server ID | see `$PTERO_SERVER` (not recorded here — public repo) |
| Loader | Forge 47.4.10 (Minecraft 1.20.1) |
| Mods installed | 148 jars |
| Difficulty | **easy** |
| PvP | enabled |
| View / simulation distance | 10 / 10 |
| Max players | 20 |
| Level type | `minecraft:normal`, no custom generator settings, empty seed |
| Online mode | true; whitelist off |

## Install state

Alex's Caves is installed cleanly:

- `alexscaves-2.0.2.jar` (71 MB), `citadel-2.6.3-1.20.1.jar`,
  `alexs_caves_spellbooks-1.1.2.jar` all present in `/mods`
- Config generated at `config/alexscaves-general.toml`,
  `config/alexscaves-client.toml`, `config/alexscaves_biome_generation/` (6 files)
- **No datapack overrides.** `/datapacks`, `/defaultconfigs` and
  `/moonlight-global-datapacks` are all empty, so nothing is overriding AC's
  data-driven content except the Spellbooks add-on's bundled override of the
  Vallumraptor loot table.
- **All config is stock** — see [config.md](config.md) for the mechanical diff.

## Log findings

From `logs/latest.log` (boot at 04:34, current session):

### 1. Structure salt collisions — benign

```
[StructureEssentials] Non-unique structure_set salt:3 ... [alexscaves:cake_cave, alexscaves:ferrocave]
[StructureEssentials] Non-unique structure_set salt:2 ... [alexscaves:ocean_trench, alexscaves:acid_pit]
```

StructureEssentials warns that two structure sets sharing a salt can overlap.
This matches the jar data exactly (`cake_cave` and `ferrocave` are both salt 3;
`ocean_trench` and `acid_pit` are both salt 2).

**Not actionable.** Each pair is restricted to a different biome — cake_cave is
Candy Cavity and ferrocave is Magnetic Caves; ocean_trench is Abyssal Chasm and
acid_pit is Toxic Caves. Two structures cannot contend for a chunk they can
never both be eligible for. This warning will appear on every boot; it should be
treated as noise.

### 2. Mixin warnings — benign

```
Mixin alexscaves.mixins.json:SwampHutPieceMixin has multiple constructors ...
defineId called for: TremorzillaEntity from class LicowitchEntity
```

The first is Mixin picking a constructor for the witch-hut chest injection
(`loot_chest_in_witch_huts`), which is expected. The second is a class-init
ordering notice from Forge's data syncher, not an error.

### 3. Citadel / AllTheLeaks interaction — worth watching

```
[AllTheLeaks] Failed to get VarHandle for class CitadelServerData with field dataMap
```

AllTheLeaks (a memory-leak patcher) tries to reach into Citadel's server data map
and cannot. The practical effect is that AllTheLeaks will not clean up Citadel's
tracked entity data — a possible slow memory creep on a long-running server, not
a crash. If you see memory growth over multi-day uptimes, this is a lead. Citadel's
own `Track Entities` option (`true`) is the relevant switch.

### 4. Unrelated, but present

`irons_spellbooks` logs a broken loot-table reference
(`irons_spellbooks:chests/citadel/citadel_tomes` is missing). This is an Iron's
Spells packaging issue, not an Alex's Caves one, though it touches a
citadel-named path.

## Worldgen coexistence

This pack stacks several worldgen mods that all touch caves and biome placement:

| Mod | Overlap risk |
|---|---|
| Terralith 2.5.4 + TerraBlender 3.0.1.10 | surface biome placement |
| Yung's Better Caves 2.0.5 | cave carving |
| Yung's Cave Biomes 2.0.5 | underground biome placement |
| Darker Depths 2.1.5 | underground biomes |

**No incompatibility warning fired.** Alex's Caves ships
`warn_generation_incompatibility` (enabled) which prints a warning at boot if it
detects an incompatible generation mod; it did not trigger. Alex's Caves places
its biomes through its own biome source rather than by injecting into the vanilla
noise router, which is why it coexists with TerraBlender-based mods.

Expect AC biomes to be **rarer in practice** than the raw config implies, because
they compete for underground volume with Yung's Cave Biomes and Darker Depths.
Cave Maps remain the reliable way to find them.

## Mod compatibility hooks in the jar

Alex's Caves ships exactly one real compat module: **JEI** (present here — a
Spelunkery Table recipe category, plus a Cave Tablet subtype interpreter so
tablets for different biomes show as distinct entries).

It also probes for two mods at runtime, **neither installed**: `distanthorizons`
and `entityculling`. Nothing to do; noted so it is not mistaken for a missing
dependency.

## Anticipated support questions

Ranked by how likely they are to reach an admin:

1. **"Something took over my screen / I'm being controlled."** The Watcher's
   camera possession (`watcher_possession = true`). Working as intended.
2. **"A nuke destroyed half my base."** 48-block blast radius, and
   `nuke_max_block_explosion_resistance = 1000` means obsidian does not survive.
   Stock behaviour.
3. **"I can't find any of these biomes."** They are hundreds of blocks apart and
   excluded near spawn. The Cave Map is the intended answer — direct players
   through [progression.md](progression.md) rather than to random digging.
4. **"My tablet broke."** Five wrong guesses destroys it. Not recoverable.
5. **"I'm not healing."** Irradiated. Blocks all natural regeneration.
6. **"Time is moving strangely near that player."** Sugar Rush
   (`sugar_rush_slows_time = true`).

## Performance notes

The two AC-specific tick costs on this server:

- `cave_creature_spawn_count_modifier = 1.75` — dinosaurs and other cave
  creatures get 1.75× the surface-animal cap, in their own mob category that does
  not compete with vanilla caps.
- `pathfinding_threads = 5` — large mobs (Atlatitan, Tremorzilla, Grottoceratops)
  path on 5 cores. **Raising** this reduces main-thread impact.

Both are defaults. With 148 mods and 20 slots, Alex's Caves is unlikely to be the
dominant cost, but the Primordial Caves are the densest mob biome in the pack and
are the first place to look if TPS drops correlate with a player's location.

## How to pull this data again

The jars and config came from the Pterodactyl client API with `PTERO_PANEL`,
`PTERO_SERVER` and `PTERO_KEY` (now exported in `~/.zshenv`). `scripts/sync_mods.py`
in this repo uses the same endpoints; note PebbleHost's panel expects
`file_path`, not stock Pterodactyl's `file`, on the download endpoint.
