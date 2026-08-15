<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Land Mobs

The 52 Alex's Mobs creatures that live on the Overworld surface or in Overworld
caves. Stats are read out of `bakeAttributes()` in the decompiled entity
classes, so they are exact. Spawn placement is read out of the **live server's**
`/config/alexsmobs/<id>_spawns.json`, which is edited on this server and names
Terralith and Biomes O' Plenty biomes the stock config does not.

## Inclusion boundary

This doc covers a mob when its live spawn config places it **on the Overworld
surface or in Overworld caves**. Three edge cases, called out so the parallel
docs can be reconciled without overlap:

- **Dropbear is covered here but is a Nether mob on this server.** Its live
  spawn config is `minecraft:nether_wastes` plus `biomesoplenty:crystalline_chasm`
  and nothing else — that is the mod's own default (`DefaultBiomes.DROPBEAR`),
  not a server edit. It is documented here because it is a land mob by every
  other measure; [mobs-nether-end.md](mobs-nether-end.md) owns the Nether
  spawn context.
- **Terrapin and Platypus are registered `WATER_AMBIENT` / `CREATURE` but
  spawn on warm rivers.** Both are covered here. Terrapin is bucketable and
  appears in the aquatic roster in [overview.md](overview.md).
- **Alligator Snapping Turtle, Anaconda, Crocodile, Froststalker and Shoebill**
  are `ISemiAquatic` swamp/river mobs. Covered here.

Not covered here: everything aquatic (Lobster through Cachalot Whale), the
Nether roster (Crimson Mosquito, Warped Toad, Warped Mosco, Bone Serpent,
Straddler, Stradpole, Soul Vulture, Laviathan, Spectre, Skelewag, Sea Bear),
the End and space roster (Endergrade, Enderiophage, Mimicube, Cosmaw, Cosmic
Cod, Void Worm, Farseer, Murmur, Skreecher, Underminer, Ghost Miner), Caiman
and Mudskipper (aquatic doc), and every projectile, multipart segment and
vehicle entity.

## Reading the attribute table

Blank cells mean the entity does not override that attribute and inherits the
vanilla default for its base class. Every land mob in this mod is built on
`Monster.createMonsterAttributes()` regardless of whether it is hostile — that
is the base builder, not a statement about behaviour.

The SRG attribute field names left in the decompiled source were resolved by
diffing against the clean upstream source at
[`AlexModGuy/AlexsMobs`](https://github.com/AlexModGuy/AlexsMobs) branch `1.20`,
which is version 1.22.9 — the same build as the installed jar. Gorilla pinned
`MAX_HEALTH` / `FOLLOW_RANGE` / `ARMOR` / `ATTACK_DAMAGE` /
`KNOCKBACK_RESISTANCE` / `MOVEMENT_SPEED`; Rhinoceros additionally pinned
`ARMOR_TOUGHNESS` and `ATTACK_KNOCKBACK`.

**One field is inferred, not confirmed:** `f_22280_` is read as `FLYING_SPEED`.
It appears on three mobs in this doc — Flutter (0.8), Fly (0.8) and Hummingbird
(7.0) — and those columns should be treated as unverified.

## All land mobs by health

| Mob | ID | HP | Attack | Armor | Tough | KB resist | Atk KB | Speed | Follow | Fly speed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Elephant | `elephant` | 85 | 10 | | | 0.9 | | 0.35 | 32 | |
| Bunfungus | `bunfungus` | 80 | 8 | | | | | 0.21 | 32 | |
| Rhinoceros | `rhinoceros` | 60 | 8 | 12 | 4 | 0.9 | 2 | 0.25 | 32 | |
| Grizzly Bear | `grizzly_bear` | 55 | 8 | | | 0.6 | | 0.25 | | |
| Moose | `moose` | 55 | 7.5 | | | 0.5 | | 0.25 | | |
| Tiger | `tiger` | 50 | 12 | | | | | 0.25 | 86 | |
| Anaconda | `anaconda` | 40 | — | | | | | 0.15 | | |
| Bison | `bison` | 40 | 8 | | | | 2 | 0.25 | 32 | |
| Tusklin | `tusklin` | 40 | 9 | | | 0.9 | | 0.3 | | |
| Cave Centipede | `centipede_head` | 35 | 8 | 6 | | 0.5 | | 0.22 | 32 | |
| Crocodile | `crocodile` | 30 | 10 | 8 | | 0.4 | | 0.25 | 15 | |
| Gorilla | `gorilla` | 30 | 7 | 0 | | 0.5 | | 0.25 | 32 | |
| Komodo Dragon | `komodo_dragon` | 30 | 4 | 0 | | | | 0.23 | | |
| Snow Leopard | `snow_leopard` | 30 | 6 | | | | | 0.35 | 64 | |
| Froststalker | `froststalker` | 24 | 4.5 | 2 | | | | 0.3 | | |
| Dropbear | `dropbear` | 22 | 2 | | | 0.7 | | 0.25 | 20 | |
| Kangaroo | `kangaroo` | 22 | 4 | | | | | 0.5 | 32 | |
| Anteater | `anteater` | 20 | 6 | | | | | 0.25 | | |
| Emu | `emu` | 20 | 3 | | | | | 0.35 | | |
| Sunbird | `sunbird` | 20 | 2 | | | | | 1.0 | 64 | |
| Alligator Snapping Turtle | `alligator_snapping_turtle` | 18 | 4 | 8 | | 0.7 | | 0.2 | 16 | |
| Gelada Monkey | `gelada_monkey` | 18 | 4 | | | | | 0.25 | | |
| Tarantula Hawk | `tarantula_hawk` | 18 | 5 | 4 | | | | 0.3 | 32 | |
| Bald Eagle | `bald_eagle` | 16 | 5 | | | | | 0.3 | 32 | |
| Guster | `guster` | 16 | 1 | | | | | 0.2 | 32 | |
| Maned Wolf | `maned_wolf` | 16 | 2 | | | | | 0.3 | 32 | |
| Mungus | `mungus` | 15 | — | | | | | 0.25 | | |
| Tasmanian Devil | `tasmanian_devil` | 14 | 2 | | | | | 0.3 | 32 | |
| Blue Jay | `blue_jay` | 10 | 1 | | | | | 0.25 | | |
| Capuchin Monkey | `capuchin_monkey` | 10 | 2 | | | | | 0.4 | | |
| Platypus | `platypus` | 10 | — | | | | | 0.2 | 16 | |
| Rocky Roller | `rocky_roller` | 10 | 2 | 20 | | 0.7 | | 0.25 | 20 | |
| Shoebill | `shoebill` | 10 | 4 | | | | | 0.2 | | |
| Terrapin | `terrapin` | 10 | — | 10 | | | | 0.1 | | |
| Raccoon | `raccoon` | 9 | 2 | | | | | 0.25 | | |
| Crow | `crow` | 8 | 1 | | | | | 0.2 | | |
| Flutter | `flutter` | 8 | 1 | | | | | 0.21 | 32 | 0.8 |
| Gazelle | `gazelle` | 8 | 2 | | | | | 0.25 | | |
| Leafcutter Ant | `leafcutter_ant` | 8 | 2 | | | | | 0.25 | 32 | |
| Potoo | `potoo` | 8 | 1 | | | | | 0.2 | | |
| Rattlesnake | `rattlesnake` | 8 | 2 | 0 | | | | 0.28 | | |
| Roadrunner | `roadrunner` | 8 | 1 | | | | | 0.45 | 10 | |
| Seagull | `seagull` | 8 | 1 | | | | | 0.2 | | |
| Skunk | `skunk` | 8 | 1 | | | | | 0.25 | | |
| Sugar Glider | `sugar_glider` | 8 | 2 | | | | | 0.25 | | |
| Cockroach | `cockroach` | 6 | — | | | | | 0.35 | | |
| Rain Frog | `rain_frog` | 6 | — | | | | | 0.2 | | |
| Toucan | `toucan` | 6 | — | | | | | 0.2 | | |
| Banana Slug | `banana_slug` | 4 | 1 | | | | | 0.1 | | |
| Hummingbird | `hummingbird` | 4 | 0 | | | | | 0.45 | | 7.0 |
| Jerboa | `jerboa` | 4 | — | | | | | 0.45 | | |
| Fly | `fly` | 2 | 1 | | | | | 0.25 | | 0.8 |

An em dash in the Attack column means the entity registers no `ATTACK_DAMAGE`
attribute at all. For Cockroach, Jerboa, Mungus, Platypus, Rain Frog, Terrapin
and Toucan that is because they never attack. Anaconda is the exception: it
does damage entirely in code (see *Anaconda* below).

Cave Centipede's 35 HP is on the head segment (`centipede_head`); the body and
tail segments are separate entities with their own health that forward damage to
the head.

## Disposition

| Disposition | Mobs |
|---|---|
| **Hostile** — attacks players unprovoked | Cave Centipede, Guster, Rocky Roller, Dropbear, Crocodile (untamed adults), Komodo Dragon (untamed adults), Anaconda (adults), Froststalker (conditional), Tiger (conditional), Bison (close range), Rhinoceros (close range), Rattlesnake (close range) |
| **Neutral** — retaliates, or hostile under a stated condition | Grizzly Bear, Anteater, Leafcutter Ant, Tusklin, Alligator Snapping Turtle, Bald Eagle, Blue Jay, Capuchin Monkey, Crow, Elephant, Emu, Flutter, Gelada Monkey, Gorilla, Kangaroo, Moose, Raccoon, Roadrunner, Shoebill, Snow Leopard, Tarantula Hawk, Tasmanian Devil |
| **Passive** — no target selector that can pick a player | Banana Slug, Bunfungus, Cockroach, Fly, Gazelle, Hummingbird, Jerboa, Maned Wolf, Mungus, Platypus, Potoo, Rain Frog, Seagull, Skunk, Sugar Glider, Sunbird, Terrapin, Toucan |

The conditional hostiles are worth stating precisely, because the condition is
the whole mechanic:

- **Bison** and **Rhinoceros** run `NearestAttackableTargetGoal<Player>` with
  the target range overridden to **3 blocks**. Adults only, and not while
  breeding. A Rhinoceros that has been fed wheat by any player stops targeting
  players entirely (`trustsAny()`).
- **Rattlesnake** uses the same pattern at **2 blocks**, and rattles first.
- **Froststalker** targets any player **not wearing a Froststalker Helmet**.
- **Tiger** targets any player **without the Tiger's Blessing effect**.
- **Crocodile** and **Anaconda** stop targeting players on Peaceful; Crocodile
  also stops once tamed. Anaconda stops for 3–6 minutes after being fed chicken.

## Where they spawn

Weight and rolls are the live values in `/config/alexsmobs.toml`. Higher weight
= more likely within the biome's spawn pool; **rolls is inverted** — higher
means *less* likely, and `0` means no extra roll. Group is the min–max pack size
passed to `MobSpawnSettings.SpawnerData`.

Every entry below also carries the biome's own `minecraft:is_overworld` or
`forge:no_default_monsters` guards where the config sets them; those are omitted
for readability.

| Mob | Where | Weight | Rolls | Group |
|---|---|---:|---:|---|
| Alligator Snapping Turtle | Swamps other than mangrove swamp; BOP tundra bog; Terralith ice marsh and orchid swamp | 20 | 1 | 1–2 |
| Anaconda | All swamps including mangrove swamp; Terralith ice marsh, orchid swamp, amethyst rainforest, tropical jungle, skylands summer | 12 | 0 | 1 |
| Anteater | Jungles other than bamboo jungle; Terralith jungle variants | 7 | 0 | 1–3 |
| Bald Eagle | Coniferous hills, grove, windswept forest; Terralith blossom, highland and skylands variants; BOP jade cliffs | 15 | 0 | 2–4 |
| Banana Slug | Old-growth pine and spruce taiga, rare dense taigas; Terralith forested highlands, shield, skylands autumn, yosemite lowlands; BOP redwood forest, coniferous forest, fir clearing; Autumnity maple forest | 14 | 0 | 2–3 |
| Bison | Plains that are neither savanna nor hot; meadow; BOP field, forested field, grassland, pasture, prairie; Terralith cold shrubland, rocky shrubland, steppe, valley clearing | 9 | 0 | 6–10 |
| Blue Jay | Forests other than sparse jungle, and all taigas; Terralith blossom, highland and shield variants; cherry grove; BOP redwood forest, snowblossom grove | 16 | 0 | 2–4 |
| Bunfungus | Rare mushroom biomes; Terralith mirage isles | 3 | 0 | 1 |
| Capuchin Monkey | Jungles other than bamboo jungle; mangrove swamp; Terralith jungle variants | 28 | 0 | 9–16 |
| Cave Centipede | Underground everywhere in the Overworld except oceans, mushroom fields and the deep dark; all 13 Terralith cave biomes | 8 | 1 | 1 |
| Cockroach | Same footprint as Cave Centipede | 4 | 0 | 5 |
| Crocodile | Swamps including mangrove swamp; non-cold rivers; BOP tropic beach; Terralith orchid swamp, red oasis, warm river | 20 | 1 | 1–2 |
| Crow | Non-savanna plains, all forests, all taigas; Terralith shrubland, highland, blossom and skylands variants; cherry grove; BOP snowblossom grove | 10 | 0 | 3–5 |
| Dropbear | **Nether wastes**; BOP crystalline chasm | 19 | 1 | 1 |
| Elephant | Savannas; Terralith arid highlands, brushland, fractured savanna, savanna badlands, savanna slopes, shrubland, red oasis | 30 | 0 | 3–5 |
| Emu | Badlands and savannas; Terralith savanna and mesa variants, red oasis; BOP lush desert | 20 | 0 | 2–5 |
| Flutter | **Lush caves only** | 13 | 0 | 2–4 |
| Fly | Anywhere in the Overworld | 3 | 1 | 2–3 |
| Froststalker | Ice spikes, frozen peaks; Terralith frostfire caves, frozen cliffs, glacial chasm, snowy badlands, gravel desert | 20 | 0 | 5–7 |
| Gazelle | Savannas; Terralith savanna variants and red oasis | 40 | 0 | 7 |
| Gelada Monkey | Plains plateaus; Terralith highlands, hot shrubland, rocky shrubland, steppe, valley clearing | 5 | 0 | 9–16 |
| Gorilla | Jungles other than bamboo jungle; Terralith jungle variants | 25 | 0 | 7 |
| Grizzly Bear | Forests other than sparse jungle, and all taigas; same Terralith/BOP list as Blue Jay | 8 | 0 | 2–3 |
| Guster | Hot, dry, sandy biomes; Terralith ancient sands, desert canyon, desert spires, ashen savanna, desert caves | 35 | 0 | 1–2 |
| Hummingbird | Flower forest, sunflower plains, all jungles, meadow, cherry grove; Terralith blossom, jungle, skylands and orchid swamp variants | 19 | 1 | 7 |
| Jerboa | Hot, dry, sandy biomes that are not badlands; Terralith desert variants and red oasis | 12 | 2 | 1–3 |
| Kangaroo | Badlands and savannas; Terralith savanna and mesa variants, red oasis; BOP lush desert | 25 | 0 | 3–5 |
| Komodo Dragon | Jungles that are **not** dense; Terralith sandstone valley, red oasis, skylands summer; BOP tropics | 16 | 1 | 1–2 |
| Leafcutter Ant | Not a biome spawn — from anthills (see below) | — | — | — |
| Maned Wolf | Savannas; Terralith savanna variants (no red oasis) | 8 | 0 | 1 |
| Moose | Snowy wastelands and snowy taigas; Terralith alpine grove, snowy badlands, snowy maple forest, snowy shield, wintry forest, wintry lowlands, gravel desert, skylands winter; BOP snowy coniferous forest, snowy fir clearing, snowy maple woods, snowblossom grove | 9 | 0 | 3–4 |
| Mungus | Rare mushroom biomes; Terralith mirage isles | 4 | 1 | 3–5 |
| Platypus | Non-cold rivers; BOP tundra bog; Terralith warm river | 20 | 0 | 1–2 |
| Potoo | **Dark forest only** | 15 | 0 | 1 |
| Raccoon | All forests, non-savanna plains, all taigas; Terralith blossom, shrubland, highland and mirage variants; cherry grove; BOP redwood forest, snowblossom grove | 10 | 0 | 2–4 |
| Rain Frog | Hot, dry, sandy biomes that are not badlands; Terralith desert variants and red oasis | 10 | 0 | 1–3 |
| Rattlesnake | Badlands and all hot, dry, sandy biomes; Terralith desert and mesa variants | 12 | 0 | 1–2 |
| Rhinoceros | Savannas; Terralith savanna variants and red oasis | 24 | 0 | 3–5 |
| Roadrunner | Badlands and all hot, dry, sandy biomes; Terralith desert and mesa variants | 9 | 1 | 2 |
| Rocky Roller | Dripstone caves; Terralith andesite, diorite and granite caves | 60 | 0 | 1 |
| Seagull | Beaches and stony shores; Terralith basalt cliffs, granite cliffs, gravel beach, white cliffs, skylands autumn and spring; BOP dune beach | 21 | 0 | 3–6 |
| Shoebill | Swamps other than mangrove swamp; Terralith orchid swamp, red oasis | 10 | 0 | 1–2 |
| Skunk | Warm forests that are neither savanna, cold, nor sparse jungle; Terralith birch taiga, blossom variants, mirage isles, temperate highlands; cherry grove | 7 | 0 | 1–2 |
| Snow Leopard | All snowy biomes, snowy slopes, frozen peaks, jagged peaks; Terralith frozen cliffs, glacial chasm, emerald peaks, rocky mountains, scarlet mountains, snowy shield, skylands winter | 18 | 0 | 1–2 |
| Sugar Glider | Birch forest, old-growth birch forest; Terralith white cliffs | 15 | 0 | 2–4 |
| Sunbird | All mountain biomes, snowy slopes, frozen peaks, jagged peaks; a long list of Terralith mountain, cliff, spire and skylands biomes | 5 | 6 | 1 |
| Tarantula Hawk | Hot, dry, sandy biomes that are not badlands; Terralith desert variants and red oasis | 6 | 1 | 1 |
| Tasmanian Devil | Same footprint as Skunk, minus cherry grove | 10 | 0 | 1–2 |
| Terrapin | Non-cold rivers; BOP tundra bog; Terralith warm river | 4 | 0 | 1–2 |
| Tiger | Bamboo jungle, cherry grove; Terralith sakura grove and valley, amethyst canyon and rainforest, skylands spring; BOP bamboo grove, snowblossom grove | 30 | 0 | 1–3 |
| Toucan | Jungles other than bamboo jungle; Terralith jungle variants | 23 | 0 | 5 |
| Tusklin | Ice spikes, snowy plains; Terralith snowy badlands, gravel desert; BOP snowblossom grove | 18 | 0 | 3–5 |

Every one of these weights and rolls is the mod's own stock default. Nothing in
the spawning section of `alexsmobs.toml` is edited on this server.

### The hummingbird rolls default is an upstream bug

Worth knowing because it reads as a server edit and is not one.
`AMConfig.hummingbirdSpawnRolls` is `0`, but that static field is **not** what
generates the TOML default. `CommonConfig.java` builds the spec with a
copy-pasted argument:

```java
hummingbirdSpawnRolls = buildInt(builder, "hummingbirdSpawnRolls", "spawns",
        AMConfig.flySpawnRolls, 0, Integer.MAX_VALUE, …);
```

The default comes from **`flySpawnRolls`**, which is `1`. So the live
`hummingbirdSpawnRolls = 1` is stock, hummingbirds are **not** rarer than stock
here, and `AMConfig.hummingbirdSpawnRolls = 0` is dead code that is overwritten
on load. Every other `*SpawnRolls` entry in `CommonConfig` takes its default
from its own mob's field; hummingbird is the only one wired to a different mob.
Filed alongside the `snowy_maple_woods` and `boneSeprentSpawnRolls` bugs in
[spawning.md](spawning.md).

Comparing a live TOML value against the `AMConfig` static initialiser is the
trap here — `CommonConfig` is the only authority on what a default actually is.

### Guster spawns are weather-gated

`limitGusterSpawnsToWeather = true` in the live config. Gusters only spawn while
it is raining or thundering, on top of their biome requirements.

### Leafcutter anthills

Leafcutter Ants have no biome spawn entry. They come from **leafcutter
anthills**, a worldgen feature placed at `leafcutterAnthillSpawnChance = 0.005`
— a **0.5% chance per chunk** — in jungles other than bamboo jungle plus the
Terralith jungle variants. A colony holds at most
`leafcutterAntColonySize = 10` ants.

## Drops

From `data/alexsmobs/loot_tables/entities/`. Ranges are before Looting; the
Looting bonus, where a table has one, is `+0–1` per level unless noted.

Several tables roll a **negative minimum count**, which clamps to zero — that is
how the mod expresses a chance of no drop. Those are expanded below rather than
printed raw.

| Mob | Drops |
|---|---|
| Alligator Snapping Turtle | *(no loot table file)* — Spiked Scute or Seagrass on shearing only, see below |
| Anaconda | *(empty loot table)* |
| Anteater | *(empty loot table)* |
| Bald Eagle | `feather ×0–1` |
| Banana Slug | `banana_slug_slime ×0–2` |
| Bison | `beef ×6–8` (Looting +0–2, cooked if on fire), `bison_fur ×0–2` |
| Blue Jay | `feather ×0–1` |
| Bunfungus | `red_mushroom ×0–2` (no Looting bonus) |
| Capuchin Monkey | *(empty loot table)* |
| Cave Centipede | `centipede_leg ×0–2` (head segment only; body and tail have empty tables) |
| Cockroach | `cockroach_wing_fragment ×0–1` |
| Crocodile | `crocodile_scute` — 50% none, 25% ×1, 25% ×2; `crocodile_egg` — 75% none, 25% ×1 |
| Crow | `feather ×0–1` |
| Dropbear | `dropbear_claw ×0–2` |
| Elephant | *(empty loot table)* |
| Emu | `emu_feather ×0–2`; `feather` — 67% none, 33% ×1 |
| Flutter | `spore_blossom ×0–1` |
| Fly | `maggot ×0–2` |
| Froststalker | `froststalker_horn` — 23% chance, **player kill required**, +10% per Looting level |
| Gazelle | `mutton ×0–1` (cooked if on fire), `gazelle_horn ×0–1` |
| Gelada Monkey | *(empty loot table)* |
| Gorilla | *(empty loot table)* |
| Grizzly Bear | `bear_fur` — 50% none, 25% ×1, 25% ×2; `bear_dust` — 1% chance, +1% per Looting level |
| Guster | `guster_eye` — 20% chance, +10% per Looting level; `sand ×0–3` (glass if on fire) |
| Hummingbird | *(empty loot table)* |
| Jerboa | *(empty loot table)* |
| Kangaroo | `kangaroo_hide ×0–2`, `kangaroo_meat ×1–2` (cooked if on fire) |
| Komodo Dragon | *(empty loot table)* — drops `komodo_spit` while alive, see below |
| Leafcutter Ant | *(empty loot table)*; the **queen** drops `leafcutter_ant_pupa ×0–1` |
| Maned Wolf | *(empty loot table)* |
| Moose | `moose_ribs ×1–3` (cooked if on fire) |
| Mungus | *(empty loot table)* — Mungal Spores on shearing only |
| Platypus | *(empty loot table)* |
| Potoo | `feather ×0–1` |
| Rain Frog | *(empty loot table)* |
| Raccoon | `raccoon_tail` — 67% none, 33% ×1 (no Looting bonus) |
| Rattlesnake | `rattlesnake_rattle ×0–1` (no Looting bonus) |
| Rhinoceros | *(empty loot table)* |
| Roadrunner | `roadrunner_feather` — 75% none, 25% ×1; `feather ×0–2` |
| Rocky Roller | `rocky_shell` — 75% chance, +10% per Looting level; `tuff ×0–2`; `pointed_dripstone ×0–2` |
| Seagull | `feather ×0–2` |
| Shoebill | `feather ×0–4` |
| Skunk | *(empty loot table)* |
| Snow Leopard | *(empty loot table)* |
| Sugar Glider | *(empty loot table)* |
| Sunbird | *(empty loot table)* |
| Tarantula Hawk | `tarantula_hawk_wing_fragment ×0–1` |
| Tasmanian Devil | *(empty loot table)* |
| Terrapin | *(empty loot table)* |
| Tiger | *(empty loot table)* |
| Toucan | `feather ×0–1` |
| Tusklin | `porkchop ×3–6` (cooked if on fire), `snowball ×0–1` |

Twenty-two of the 52 have an empty loot table. That is deliberate for the ones
you are meant to keep alive — Elephant, Gorilla, Tiger, Snow Leopard, Rhinoceros
— and for the ones whose useful output comes from interaction rather than death:
Mungus, Platypus, Sugar Glider, Anteater, Komodo Dragon.

Variant tables exist for **Guster** (`guster_red` drops red sand, `guster_soul`
drops soul sand, both otherwise identical), **Froststalker**
(`froststalker_spikes` for the spiked variant: 33% horn plus `packed_ice ×0–3`
and `blue_ice ×0–2`) and **Cockroach** (`cockroach_maracas` adds a guaranteed
Maraca and a 20% Sombrero).

### Items that come from a live mob, not from death

| Mob | Item | How |
|---|---|---|
| Alligator Snapping Turtle | `spiked_scute` or `seagrass` | Shear it. Chance of the scute is `moss level × 5%`, otherwise seagrass; shearing resets moss to zero |
| Bison | `bison_fur ×2–3` | Shear an unsheared bison |
| Cockroach | — | Shearing decapitates it; a headless cockroach stays alive |
| Komodo Dragon | `komodo_spit` | Dropped on its own every 24000–36000 ticks (20–30 minutes) by any adult |
| Mungus | mushroom block | Shear it; consumes one of its stored mushrooms |
| Platypus | Piglin-barter-style loot | It digs; see below |
| Sugar Glider | forage loot | It forages leaves; see below |
| Anteater | anthill loot | It raids a leafcutter anthill; see below |

## Taming, breeding and riding

`Breed` is the `isFood()` item tag. `Tame` is the `isTameableFood()` /
`*_TAMEABLES` tag and the code path that consumes it.

| Mob | Tameable | Breedable with | Rideable |
|---|---|---|---|
| Alligator Snapping Turtle | No | Cod | No |
| Anaconda | No | — (pacified by raw or cooked chicken) | No |
| Anteater | No | Leafcutter Ant Pupa | No |
| Bald Eagle | **Yes** — Fish Oil, 50% per feed | Rotten Flesh | Perches on a Falconry Glove |
| Banana Slug | No | Brown Mushroom | No |
| Bison | No | Wheat | No |
| Blue Jay | No | insect items (Maggot, Mosquito Larva, Leafcutter Ant Pupa) | No |
| Bunfungus | No | — | No |
| Capuchin Monkey | **Yes** — bananas, 20% per feed | insect items, once tamed | Rides your shoulder (shift-interact) |
| Cave Centipede | No | — | No |
| Cockroach | No | Sugar | No |
| Crocodile | **Yes** — hatch a Crocodile Egg; the hatchling tames to the nearest player | Rotten Flesh | No |
| Crow | **Yes** — Pumpkin Seeds | Pumpkin Seeds, once tamed | No |
| Dropbear | No | — | No |
| Elephant | **Yes** — throw an Acacia Blossom for it to pick up | Acacia Blossom, once tamed | **Yes**, no saddle needed; wearable carpet and a chest |
| Emu | No | Wheat | No |
| Flutter | **Yes** — feed *distinct* flower species; 1-in-3 per feed from the 4th, guaranteed by the 7th | Bone Meal, once tamed | No |
| Fly | No | Rotten Flesh | No |
| Froststalker | No | Raw or Cooked Porkchop | No |
| Gazelle | No | Wheat, Acacia Blossom | No |
| Gelada Monkey | No | Dead Bush | No |
| Gorilla | **Yes** — bananas | bananas, once tamed | No |
| Grizzly Bear | **Yes** — Salmon | Salmon, once tamed | **Yes**, no saddle |
| Guster | No | — | No |
| Hummingbird | No | any flower | No |
| Jerboa | Befriended, not tamed — any seed | insect items | No |
| Kangaroo | **Yes** — Carrots, 10–15 feedings | Dead Bush, Grass | Pouch inventory, not a mount |
| Komodo Dragon | **No — tameable food tag is empty, see below** | Rotten Flesh, but gated behind taming so unreachable | Saddle, but gated behind taming so unreachable |
| Leafcutter Ant | No | — (Gongylidia makes the queen produce workers) | No |
| Maned Wolf | No | Rabbit, Cooked Rabbit, Chicken, Cooked Chicken | No |
| Moose | No | Dandelion | No |
| Mungus | No | Mungal Spores | No |
| Platypus | No | Lobster Tail | No — bucketable |
| Potoo | No | insect items | Perches on a Falconry Glove |
| Raccoon | **Yes** — eggs | Bread | No; wearable carpet |
| Rain Frog | No | insect items | No |
| Rattlesnake | No | — | No |
| Rhinoceros | Trust, not taming — Wheat | Dead Bush, Grass | No |
| Roadrunner | No | insect items | No |
| Rocky Roller | No | — | No |
| Seagull | No | Cod | No |
| Shoebill | No | — (fish feed it) | No |
| Skunk | No | Sweet Berries | No |
| Snow Leopard | No | Moose Ribs, Cooked Moose Ribs | No |
| Sugar Glider | **Yes** — Sweet Berries, 50% per feed | Honeycomb | Rides your shoulder (shift-interact) |
| Sunbird | No | — | No |
| Tarantula Hawk | **Yes** — Spider Eyes, 15–25 feedings | Fermented Spider Eye | No |
| Tasmanian Devil | No | — | No |
| Terrapin | No | Seagrass | No — bucketable |
| Tiger | No | Acacia Blossom | No |
| Toucan | No | eggs | No |
| Tusklin | No | Red Mushroom | **Yes** with a Saddle, untamed — it bucks |

Ten tamed species (Bald Eagle, Capuchin Monkey, Crocodile, Crow, Grizzly Bear,
Komodo Dragon, Kangaroo, Raccoon, Sugar Glider, Tarantula Hawk) cycle a
wander / follow / stay command on interaction, announced with
`entity.alexsmobs.all.command_<n>`. Crow has a fourth state, "gathering items".

### The Komodo Dragon taming gap

`EntityKomodoDragon.mobInteract` tames on a single stack of
`#alexsmobs:komodo_dragon_tameables` larger than a random `58–73` items. That
tag **ships empty** — both in the installed jar and in the upstream 1.22.9
source — so no item satisfies it.

**Confirmed in play on this server, not just in the jar.** A datapack could
populate the tag, so all three load points were listed through the Pterodactyl
client API — `/datapacks`, `/world/datapacks` and `/defaultconfigs` — and all
three are empty. Nothing overrides the tag, so it is empty at runtime and
**Komodo Dragons cannot be tamed here at all**. Everything downstream of taming
(Saddle, riding, breeding with Rotten Flesh, the sit command) is gated behind
`isTame()` and is therefore unreachable. This is a mod-side gap, not a server
config choice.

## Mob mechanics

### Anaconda

Registers no attack damage. It bites for a flat **4**, then constricts anything
up to 2 blocks wide: the target is pinned in place, and from 2 seconds into the
hold it takes **`max(4, 25% of its maximum health)` every second**. Against a
full-health player that is 5 per second and it does not stop until the anaconda
or the target dies. Feeding it raw or cooked chicken clears its target and makes
it passive for **3–6 minutes** (3600–7200 ticks).

### Anteater

Raids leafcutter anthills. It rolls the `alexsmobs:gameplay/anteater_reward`
table with `-4` to `1` rolls, so most raids yield nothing; the notable hit is
Leafcutter Ant Pupa at ~10% of any item that does drop. Feeding it any insect
item stops it being angry and heals 4.

### Bald Eagle

The falconry mob. Tamed with Fish Oil (50% per feed), it perches on a **Falconry
Glove** and can be launched at a target. Fitting it with a **Falconry Hood**
lets it strike from long range — the mod's own challenge advancement is a kill
from 100 blocks with a hooded eagle. Shears remove the hood.

### Bison

Attacks players inside 3 blocks. Wears snow if you use a Snow Block on it and
keeps it permanently until you shovel it off. Shearing an unsheared bison yields
2–3 Bison Fur and resets its feeding counter.

### Blue Jay

Feeding one Glow Berries breaks its bond with any Raccoon it is riding, sets you
as its last feeder for 60 seconds, and dismounts it. Feeding it a seed makes it
sing for 2 seconds, which is what alerts nearby mobs.

### Bunfungus

A Rabbit fed Mungal Spores transforms into a Bunfungus
(`bunfungusTransformation = true` on this server). It begs for carrots and takes
one into its hand if you offer it. On eating, it gives itself Strength and
Regeneration II for 50 seconds.

### Capuchin Monkey

Tamed with bananas at 20% per feed. Give a tamed one an **Ancient Dart** and it
throws darts at your targets; shears take the dart back. Shift-interact to have
it ride your shoulder. It drops a Banana Peel block when it eats a banana.

### Cave Centipede

Multi-segment: `centipede_head` carries the stats, with `centipede_body` and
`centipede_tail` entities trailing it. Its bite applies **Poison II**, scaled by
difficulty. It actively flees light (`AnimalAIFleeLight`) and hunts cockroaches
as well as players and villagers.

### Cockroach

Effectively unkillable by half-measures: reduced below 1 HP there is a 1-in-3
chance it goes **headless** instead of dying, and a headless cockroach stays
alive. Shears decapitate it outright. Give it a **Maraca** and it dances and
becomes `cockroach_maracas`, which drops the maraca back plus a 20% Sombrero.
Adults periodically drop a Cockroach Ootheca.

### Crocodile

Hostile to players as an untamed adult on any difficulty above Peaceful; tamed
crocodiles flip to attacking hostile mobs instead (creepers excluded). Adults
cannot be tamed — the only path is a **Crocodile Egg**, which tames the
hatchling to the nearest player at the moment it hatches
(`BlockReptileEgg.tame`). Females lay eggs on suitable ground. Feeding a tamed
one any meat heals 10.

### Crow

Steals crops off farmland (`crowsStealCrops = true`). A tamed crow has a fourth
command state, "gathering items", in which it fetches dropped items back to you.
Interacting with a crow holding an item makes it drop that item.

### Dropbear

Clings to cave ceilings upside down and drops onto whatever walks underneath,
targeting a ceiling 3–6 blocks above the victim. Its **Dropbear Claw** brews
into the **Clinging Potion** (Awkward + claw, 3 minutes; +Redstone for 8
minutes), which lets you climb walls.

### Elephant

The pack animal. Throw it an **Acacia Blossom** and it tames itself to whoever
threw it. A tamed adult is ridden bareback, wears a wool carpet for colour, and
takes a wooden **chest** for a 54-slot inventory that dumps on the ground when
you shear the chest off. Wild elephants follow each other in caravans; villagers
will ride them. Trader Elephants carry the
`alexsmobs:gameplay/trader_elephant_chest` loot table.

### Emu

`emuTargetSkeletons = true` — emus hunt skeletons and pillagers unprovoked. Emu
Leggings crafted from their feathers give a **45% chance to dodge projectiles**
(`emuPantsDodgeChance`). Adults lay Emu Eggs.

### Flutter

Lush caves only. Tamed by feeding it **four or more distinct flower species** —
repeating a flower it has already eaten does nothing but a head shake. A tamed
flutter accepts a **Flower Pot**, after which it can be shift-interacted to
produce a fish bucket. Shears remove the pot.

### Froststalker

Hunts in schools of 5–7 with a leader. It targets any player **not wearing a
Froststalker Helmet**, which is crafted from its own horn — the helmet is the
counter to the mob. Rain or water grows its ice spikes, which give it armor and
switch it to the `froststalker_spikes` loot table; a hot biome with no water
gives it **Weakness for 20 seconds** every 10 seconds instead. It freezes water
it walks over into Frosted Ice.

### Gelada Monkey

Troops of 9–16 with a dominance fight between males. Feeding wheat to one makes
3–5 of the troop clear grass around them at once.

### Gorilla

Tamed with bananas. An untamed silverback **charges anyone who looks at it**
(`GorillaAIChargeLooker`) — breaking line of sight is the counter. Wild gorillas
forage leaves and travel in caravans of 7.

### Grizzly Bear

Neutral, tamed with Salmon, and the only bear you can ride bareback once tamed.
Wild bears seek out beehives and become "honeyed", and flee bees while honeyed.
Snow Block on it makes it snowy permanently; a shovel removes it. Its rare
**Bear Dust** drop is 1% before Looting.

### Guster

A hostile sand elemental gated to rain and thunder. Fires `EntitySandShot`
projectiles. Two variants exist by biome — the red-sand and soul-sand gusters
drop their own sand type. **Guster Eye** is a 20% drop, +10% per Looting level.

### Hummingbird

Flocks of 7. It pollinates flowers and is the mob the **Hummingbird Feeder**
block is for; Sugar is its feeder sweetener. It has the highest listed flying
speed in the mod at 7.0 (field inferred, see above) and does zero attack damage.

### Jerboa

Cats, ocelots and foxes hunt jerboas (`catsAndFoxesAttackJerboas = true`), and
so do rattlesnakes. Feeding it any seed befriends it and, at **30% chance**,
gives you **Fleet-Footed** for 10 minutes — a +0.2 sprint-jump speed bonus.

### Kangaroo

Tamed by feeding **10–15 Carrots**, each with a chance to stick. Shift-interact
opens its **pouch**, a portable inventory; a joey rides in the pouch until you
open it. It boxes with a stand-up melee attack.

### Komodo Dragon

Its bite applies **Poison** scaled by difficulty. It drops a **Komodo Spit**
item on its own every 20–30 minutes, which is the practical way to farm the
ingredient without killing one. See the taming gap above.

### Leafcutter Ant

Colony mob tied to anthills. Workers cut leaves and carry them home — each
returned leaf has a `leafcutterAntFungusGrowChance = 30%` of growing fungus, and
harvesting breaks the leaf block 20% of the time
(`leafcutterAntBreakLeavesChance`). A colony below half strength regrows a
worker every `leafcutterAntRepopulateFeedings = 25` feedings. Feeding
**Gongylidia** to the queen spawns 1–2 new ants on a 20-minute cooldown and
pacifies the whole colony; feeding it to a worker just heals it and pacifies the
colony.

### Maned Wolf

Feed it an **Apple** and it eats, then shakes for 5–6.5 seconds — the mod's
stench mechanic. It also dances to music discs (`IDancingMob`).

### Moose

Bulls jostle each other with their antlers. Snow Block makes it snowy, shovel
removes it. Wolves hunt moose (`wolvesAttackMoose = true`). Moose Ribs are the
only breeding food for Snow Leopards, which links the two mobs.

### Mungus

Transforms terrain. `mungusBiomeTransformationType = 2` on this server, the
maximum — a mungus changes **both the blocks and the chunk's biome** to match
the mushroom it is carrying. Feed it up to 5 mushrooms of one kind; the mapping
is Red/Brown Mushroom → mushroom fields with mycelium, Crimson Fungus → crimson
forest, Warped Fungus → warped forest. A **Poisonous Potato** reverts it.
Shearing takes back one stored mushroom. Mungal Spores are its breeding item and
turn Rabbits into Bunfungus.

### Platypus

Digs riverbeds for the `alexsmobs:gameplay/platypus_reward` table: **74% Clay
Ball, 26% Maggot**. Feeding it **Redstone** starts it sensing; feeding a
**Redstone Block** supercharges it, which switches it to
`platypus_supercharged_reward` — 65% Clay Ball ×1–2, 32% Maggot, **3.2% Fedora**.
Its spur applies Poison for 5 seconds. It is bucketable, and it will wear a
Fedora.

### Potoo

Dark forest only, one at a time. Like the Bald Eagle it is `IFalconry` — it
perches on a **Falconry Glove**. It spends the day motionless imitating a broken
branch.

### Raccoon

Steals from chests (`raccoonStealFromChests = true`). It washes food in water
before eating (`RaccoonAIWash`) and raids turtle eggs. Tamed with eggs; it wears
a wool carpet. Feeding it **Glow Berries** bonds it with nearby Blue Jays, which
then ride on it.

### Rain Frog

Grumpy and burrowed most of the time. Hitting the ground next to it with a
**shovel** forces it out of its burrow into its standing display for 1–2.5
seconds and blocks it re-burrowing for another 7.5–13.5 seconds. It also dances
to music discs.

### Rattlesnake

Rattles before it strikes; it only targets players inside **2 blocks**. It hunts
Rabbits and Jerboas, and Roadrunners hunt it. Its **Rattle** is an Animal
Dictionary ingredient and has no Looting bonus on the drop.

### Rhinoceros

Charges, with 12 armor, 4 armor toughness and 90% knockback resistance — the
highest defensive stat line of any land mob here. Feeding it **Wheat** adds you
to its trusted list, and a rhino that trusts anybody stops targeting players
entirely and defends its trusted players instead. Applying a **potion** to its
horn makes the horn carry that potion's effect on hit, returning the glass
bottle.

### Roadrunner

The fastest land mob in the doc at 0.45 movement speed. It hunts rattlesnakes on
sight and retaliates against players who hit it.

### Rocky Roller

20 armor on 10 health — it curls into a rolling ball and is nearly immune to
chip damage while doing so. Its roll applies **Earthquake** for 1 second to
anything it hits. It drops `rocky_shell` 75% of the time plus Tuff and Pointed
Dripstone.

### Seagull

Steals food out of the player's inventory (`seagullStealing = true`, no
blacklist set on this server) and flees; interacting with a seagull holding an
item makes it drop the item and sets a 75–150 second steal cooldown. It also
reveals buried treasure (`SeagullAIRevealTreasure`).

### Shoebill

Fishes by rolling the **vanilla fishing loot table** with a luck bonus of
`0.5 × luck level`. Feeding it a **Terrapin Egg** raises its luck level by 1, up
to 10; feeding it a **Crocodile Egg** raises its lure level by 1 (up to 10) and
cuts 10 seconds off its fishing cooldown each time. A maxed shoebill fishes at
effective Luck of Sea 5.

### Skunk

Sprays up to **5 blocks** in the direction it is facing. Everything caught in
the cone gets **Nausea for 15 seconds**, plus a copy of every status effect the
skunk itself currently has — a skunk that has been hit with a harmful potion
sprays that too. The spray also places **Skunk Spray** blocks on whatever
surface it hits.

### Snow Leopard

Ambush predator with a 64-block follow range that stalks and pounces. Bred with
Moose Ribs. It targets whatever is in `#alexsmobs:snow_leopard_targets` within
10 blocks and picks up dropped items.

### Sugar Glider

Tamed with Sweet Berries at 50% per feed, then rides your shoulder. Wild ones
forage leaves for the `alexsmobs:gameplay/sugar_glider_reward` table — mostly
Sticks at 32%, with Feathers, Sweet Berries and Eggs at 7% each, Cobweb at 6%,
and a 0.7% Moose Antler. It glides rather than flies.

### Sunbird

Perches on **beacons**. Any player inside its scorch area who has neither of its
effects gets **Sunbird's Blessing** for 30 seconds — fall damage is cancelled,
falling is slowed to 60% and pitching up while elytra-flying adds lift. Hitting
the sunbird strips the blessing and replaces it with **Sunbird's Curse** for 30
seconds, which cancels elytra flight outright and pulls you down. It also curses
phantoms.

### Tarantula Hawk

Tamed by feeding **15–25 Spider Eyes**. Its sting applies **Debilitating Sting**
— movement speed reduced by 100% and 1 magic damage per tick — for **30 seconds**
against anything, or **2 minutes** (`STING_DURATION = 2400`) against arthropods.
A hawk that has buried paralysed prey to breed stings at amplifier II until it
next lays. Fed flowers to heal.
`fireproofTarantulaHawk = false` on this server, so they are not fireproof.

### Tasmanian Devil

Scavenges carrion — it targets dying and dead animals rather than healthy ones,
and drops a Bone when it finishes eating one. Feeding it **Rotten Flesh** makes
it howl.

### Terrapin

Seven colour variants (`black`, `brown`, `green`, `painted`, `red_eared`, plus a
`koopa` and a unique overlay). Bucketable. Feeding it Seagrass makes it
persistent so it will not despawn. Its egg is the Shoebill's luck food.

### Tiger

Attacks any player who does not have **Tiger's Blessing**, and its roar applies
**Fear** — a 100% movement speed reduction that also zeroes horizontal velocity
— for 5 seconds. The blessing lasts 10 minutes and is the practical way to move
through bamboo jungle. Acacia Blossom is its breeding item.

### Toucan

Hand it a **Golden Apple** and it holds it for 10 minutes; hand it an
**Enchanted Golden Apple** and the effect is permanent and it turns enchanted.
While holding golden fruit it produces the sapling matched to the fruit. It
takes no fall damage and gets a boost climbing vines.

### Tusklin

The only mob here that is ridden **without being tamed**: put a Saddle on an
adult and mount it, and it will buck you off. **Pigshoes** — a 2.5% Piglin
bartering drop (`tusklinShoesBarteringChance`) — fit a tusklin and stop the
bucking. Feeding it a Brown Mushroom heals 6 and pacifies it for another 60
seconds.

## Status effects these mobs apply

| Effect | ID | Source | What it does |
|---|---|---|---|
| Clinging | `clinging` | Dropbear Claw potion | Climb walls; 3 min, 8 min extended |
| Debilitating Sting | `debilitating_sting` | Tarantula Hawk | −100% movement speed, 1 magic damage per tick |
| Earthquake | `earthquake` | Rocky Roller | Marker effect, 1 s per hit |
| Fear | `fear` | Tiger roar | −100% movement speed, horizontal velocity zeroed; 5 s |
| Fleet-Footed | `fleet_footed` | Feeding a Jerboa a seed | +0.2 sprint-jump speed; 10 min, 30% chance |
| Nausea | vanilla | Skunk spray | 15 s |
| Poison | vanilla | Komodo Dragon bite, Platypus spur | Difficulty-scaled; Platypus is a flat 5 s |
| Poison II | vanilla | Cave Centipede bite | Difficulty-scaled |
| Sunbird's Blessing | `sunbird_blessing` | Standing near a Sunbird | No fall damage, slowed falling, elytra lift; 30 s |
| Sunbird's Curse | `sunbird_curse` | Hitting a Sunbird | Cancels elytra flight, pulls you down; 30 s |
| Tiger's Blessing | `tigers_blessing` | Tiger | Marker effect; tigers ignore you. 10 min |
| Weakness | vanilla | Froststalker self-buff cost | 20 s, on the froststalker itself |

Full effect list including the ones no land mob applies is in
[effects-and-enchantments.md](effects-and-enchantments.md).

## Config that changes these mobs

Every value below is the live setting in `/config/alexsmobs.toml`.

| Setting | Live value | Effect |
|---|---|---|
| `limitGusterSpawnsToWeather` | `true` | Gusters only spawn in rain or thunder |
| `mungusBiomeTransformationType` | `2` | Mungus changes blocks **and** chunk biome |
| `bunfungusTransformation` | `true` | Rabbits fed Mungal Spores become Bunfungus |
| `emuTargetSkeletons` | `true` | Emus hunt skeletons |
| `emuPantsDodgeChance` | `0.45` | Emu Leggings dodge 45% of projectiles |
| `wolvesAttackMoose` | `true` | Wolves hunt moose |
| `catsAndFoxesAttackJerboas` | `true` | Cats, ocelots and foxes hunt jerboas |
| `spidersAttackFlies` | `true` | Spiders hunt flies |
| `seagullStealing` | `true` | Seagulls take food from the hotbar; blacklist is empty |
| `raccoonStealFromChests` | `true` | Wild raccoons loot chests |
| `crowsStealCrops` | `true` | Wild crows take crops off farmland |
| `bananasDropFromLeaves` / `bananaChance` | `true` / `200` | 1-in-200 leaf blocks drop a Banana — the Gorilla and Capuchin taming item |
| `acaciaBlossomsDropFromLeaves` / `acaciaBlossomChance` | `true` / `130` | 1-in-130 acacia leaves drop an Acacia Blossom — the Elephant and Tiger item |
| `leafcutterAnthillSpawnChance` | `0.005` | 0.5% of jungle chunks get an anthill |
| `leafcutterAntColonySize` | `10` | Max ants per anthill |
| `leafcutterAntBreakLeavesChance` | `0.2` | Ants destroy 20% of the leaves they harvest |
| `leafcutterAntFungusGrowChance` | `0.3` | Fungus growth per returned leaf |
| `leafcutterAntRepopulateFeedings` | `25` | Feedings needed to regrow a worker |
| `tusklinShoesBarteringChance` | `0.025` | Pigshoes from Piglin bartering |
| `fireproofTarantulaHawk` | `false` | Tarantula hawks burn |
| `falconryTeleportsBack` | `false` | Eagles do not teleport home when stuck |
| `wanderingTraderOffers` | `true` | Traders sell Acacia Blossom, Mosquito Larva, Crocodile Egg |

Full option list in [config.md](config.md).

## Unverified

- `f_22280_` → `FLYING_SPEED`. Affects the Flutter, Fly and Hummingbird flying
  speed column only. Every other attribute mapping in this doc is confirmed
  against upstream.
- Seagull buried-treasure reveal: `SeagullAIRevealTreasure` exists and is
  registered, but the trigger conditions and what it produces were not read out
  of the goal.
