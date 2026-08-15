<!-- Generated from alexscaves-2.0.2.jar + alexsmobs-1.22.9.jar + FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: README.md -->

# `.claude/docs`

Reference documentation for the mods running on the digbuild PebbleHost server
(Forge 47.4.10, Minecraft 1.20.1). Written for two audiences:
code that needs exact registry IDs, and the player-facing server wiki.

| | |
|---|---|
| Game server | `minecraft.abcdefc.gg` |
| Wiki | `wiki.abcdefc.gg` |

Content here is the source material for the wiki — the tables are meant to be
lifted onto wiki pages, and the prose is written to be read by players.

## Contents

| Doc | Covers |
|---|---|
| [alexs-caves/overview.md](alexs-caves/overview.md) | What the mod is, versions, dependency graph, install state |
| [alexs-caves/biomes.md](alexs-caves/biomes.md) | The six cave biomes: placement, climate params, ambience, spawn tables |
| [alexs-caves/progression.md](alexs-caves/progression.md) | Cave Tablet → Spelunkery Table → Cave Codex → Cave Map loop |
| [alexs-caves/mobs.md](alexs-caves/mobs.md) | All 44 mobs with stats from code, drops, and summon mechanics |
| [alexs-caves/blocks-items.md](alexs-caves/blocks-items.md) | Full block/item catalog grouped by biome |
| [alexs-caves/structures-loot.md](alexs-caves/structures-loot.md) | 14 structures, placement rules, chest loot |
| [alexs-caves/config.md](alexs-caves/config.md) | Every config option, default vs. what this server runs |
| [alexs-caves/addons.md](alexs-caves/addons.md) | Alex's Caves Spellbooks, Citadel |
| [alexs-caves/server-notes.md](alexs-caves/server-notes.md) | Server-specific findings, pack interactions, log warnings |
| [alexs-mobs/overview.md](alexs-mobs/overview.md) | What the mod is, versions, dependency graph, install state, full 116-entity roster |
| [alexs-mobs/mobs-land.md](alexs-mobs/mobs-land.md) | 52 land and ambient overworld creatures: stats from code, drops, behaviour |
| [alexs-mobs/mobs-aquatic.md](alexs-mobs/mobs-aquatic.md) | 23 water creatures, the beached-whale event, and the whale/squid encounter |
| [alexs-mobs/mobs-nether-end.md](alexs-mobs/mobs-nether-end.md) | Nether, End, boss, summoned and technical entities: stats, spawns, drops, mechanics |
| [alexs-mobs/spawning.md](alexs-mobs/spawning.md) | All 90 spawn configs: biomes in plain English, weights, group sizes, placement rules |
| [alexs-mobs/config.md](alexs-mobs/config.md) | Every `alexsmobs.toml` option, default vs. what this server runs |
| [alexs-mobs/items-blocks.md](alexs-mobs/items-blocks.md) | Items and blocks by function, incl. the Transmutation Table, Capsid and Straddleboard |
| [alexs-mobs/loot-and-drops.md](alexs-mobs/loot-and-drops.md) | 104 entity loot tables, the 4 global loot modifiers, and code-only drops |
| [alexs-mobs/taming-and-progression.md](alexs-mobs/taming-and-progression.md) | Animal Dictionary, every tameable/breedable/rideable creature, progression chains, all 106 advancements |
| [alexs-mobs/effects-and-enchantments.md](alexs-mobs/effects-and-enchantments.md) | 19 status effects, 4 Straddleboard enchantments, 2 custom damage types |
| [alexs-mobs/addons.md](alexs-mobs/addons.md) | Alex's Delight, RAM-Compat, and every other mod on the server that touches Alex's Mobs |
| [farmers-delight/overview.md](farmers-delight/overview.md) | What the mod is, versions, dependency graph, install state, census, the two custom recipe types |
| [farmers-delight/cooking.md](farmers-delight/cooking.md) | The stations, the heat rules, the cutting-board tool matrix, and all 333 recipes |
| [farmers-delight/foods-and-effects.md](farmers-delight/foods-and-effects.md) | All 77 foods with nutrition and saturation, the 6 feasts, Nourishment and Comfort, the stove damage type |
| [farmers-delight/farming.md](farmers-delight/farming.md) | Crops, Rich Soil and Organic Compost, knives and rope, wild-crop worldgen, village compost heaps, config, composter values |
| [farmers-delight/blocks-items.md](farmers-delight/blocks-items.md) | Knives and Backstabbing, storage, decoration, canvas signs, rope — everything the sibling docs do not claim |
| [farmers-delight/loot-and-worldgen.md](farmers-delight/loot-and-worldgen.md) | The 37 global loot modifiers, the 14 vanilla chest tables they change, knife-kill drops, village compost heaps |
| [farmers-delight/progression.md](farmers-delight/progression.md) | The 21-advancement tree vs. 197 recipe unlocks, kitchen/farming/knife chains, gates, vanilla prerequisites |
| [farmers-delight/config.md](farmers-delight/config.md) | Every `farmersdelight-common.toml` and `-client.toml` option, default vs. what this server runs |
| [farmers-delight/addons.md](farmers-delight/addons.md) | Dungeon's Delight, Alex's Delight, and every other mod on the server that touches Farmer's Delight |

## Provenance

Everything in these docs is derived from primary sources, not from memory:

- **`alexscaves-2.0.2.jar`** — pulled from the live server's `/mods` via the
  Pterodactyl client API, then decompiled with [CFR 0.152](https://www.benf.org/other/cfr/).
  Data-driven content (biomes, structures, loot, recipes, tags) comes from the
  jar's `data/` tree; display names from `assets/alexscaves/lang/en_us.json`.
- **Live server config** — `/config/alexscaves-general.toml`,
  `/config/alexscaves-client.toml`, `/config/alexscaves_biome_generation/*.json`,
  `/config/citadel-common.toml`, pulled from the same server.
- **Mob stats** — read out of `createAttributes()` in the decompiled entity
  classes. The SRG attribute field names were validated against the
  [official wiki's](https://alexscaves.wiki.gg/wiki/Tremorzilla) published
  Tremorzilla stat block (health 500, armor 10, attack 30, knockback resist
  100%), which matches the code constants exactly.
- **`alexsmobs-1.22.9.jar`** — pulled from the same `/mods` directory and decompiled with
  [jadx 1.5.4](https://github.com/skylot/jadx). Data-driven content (loot tables, recipes, tags,
  advancements, capsid recipes) comes from the jar's `data/` tree; display names from
  `assets/alexsmobs/lang/en_us.json`. Spawn weights, group sizes, mob categories and placement
  predicates come from `AMWorldRegistry`, `AMEntityRegistry` and the entity classes.
- **Live Alex's Mobs config** — `/config/alexsmobs.toml` and the 90 per-mob spawn JSONs in
  `/config/alexsmobs/`. **All 249 TOML options and all 90 spawn JSONs are byte-identical to the mod
  defaults.** That was verified mechanically, by parsing every `define*` call out of `CommonConfig`
  and reconstructing `DefaultBiomes` into JSON for a direct diff — not by eye. The Terralith biome
  names in those files are part of the stock defaults and are not a local edit.
  Note the trap that finding depends on: a config option's default is the value passed to
  `buildInt`/`buildBool` in `CommonConfig`, **not** the `AMConfig` static field initialiser, which
  is dead and overwritten on load. The two disagree for `hummingbirdSpawnRolls`, whose default is
  copy-pasted from `flySpawnRolls` — the only such case in the file.
- **Alex's Mobs stats** — read out of `bakeAttributes()` in the decompiled entity classes. jadx
  leaves SRG field names in place (`Attributes.f_22276_`), so the mapping was resolved by diffing
  decompiled method bodies against the same methods in the clean upstream source
  ([`AlexModGuy/AlexsMobs`](https://github.com/AlexModGuy/AlexsMobs), branch `1.20`, which carries
  `version = 1.22.9`), where the argument order is identical. Gorilla and Rhinoceros between them
  pinned ten of the eleven vanilla attribute fields; `f_22280_` (FLYING_SPEED) remains inferred and
  is flagged as such wherever it is used. The mapping table is in
  [alexs-mobs/overview.md](alexs-mobs/overview.md).
  `alexsmobs.fandom.com` returns HTTP 402 and was never used.
- **Alex's Mobs add-on jars** (`alexsdelight-1.5.jar`, `ramcompat-1.20.1-0.1.4.jar`) — same
  pipeline. Food and relic stats come from the decompiled item classes; recipes, loot tables and
  tags from the `data/` trees verbatim. Cross-mod interactions were established by scanning every
  jar in `/mods`, including nested jar-in-jar, for `alexsmobs`/`alexthe666`.
- **`FarmersDelight-1.20.1-1.3.2.jar`** — same pipeline (jadx 1.5.4). Food
  values come from `common/FoodValues.java`, verified constant-for-constant
  against the clean upstream source
  ([`vectorwing/FarmersDelight`](https://github.com/vectorwing/FarmersDelight),
  branch `1.20`, `mod_version=1.3.2`), which also resolved the SRG food-builder
  and `MobEffects` names. Recipes, loot modifiers, tags, the damage type and the
  Better Combat `weapon_attributes` entry come from the jar's `data/` tree; the
  config gates from the live `/config/farmersdelight-common.toml`, which is
  byte-for-byte the mod defaults.
- **Farmer's Delight add-on jars** (`forge-dungeonsdelight-1.20.1-1.3.0.jar`,
  `alexsdelight-1.5.jar`) — same pipeline. Registry IDs from the `register("…")`
  calls in `DDItems`/`DDBlocks`/`DDEffects`/`TFItems`/`ADItems`, food values from
  `DDProperties` and `INProperties`, recipes/tags/loot modifiers from the `data/`
  trees verbatim, plus the live `/config/dungeonsdelight-config.toml`. Cross-mod
  reach was established by downloading **all 148 jars** in the live `/mods` and
  scanning each for entries under `data/farmersdelight/**` and
  `assets/farmersdelight/**`, any other path naming `farmersdelight`, and the
  byte strings `farmersdelight` and `vectorwing`, including nested jar-in-jar.
  All 148 downloaded and scanned; none failed. Exactly ten carry a hit.
- **Mechanics prose** — the mod's own in-game guidebook text
  (`assets/alexscaves/books/en_us/**.txt`), cross-checked against the code paths
  that implement each mechanic.

Where the official wiki and the code disagreed, the code won and the difference
is called out inline.

## Regenerating

The extraction and generation scripts live in the session scratchpad, not in
this repo. To rebuild from scratch you need `PTERO_PANEL`, `PTERO_SERVER` and
`PTERO_KEY` in the environment (see `scripts/sync_mods.py` for the same API
usage), plus a JDK and a decompiler — CFR 0.152 for the Alex's Caves docs,
jadx 1.5.4 for the Alex's Mobs ones (`brew install openjdk jadx`).
