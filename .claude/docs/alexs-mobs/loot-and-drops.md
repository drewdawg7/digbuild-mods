<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Loot & Drops

Covers the 4 global loot modifiers that rewrite vanilla loot, the 10 gameplay
loot tables, the 25 block loot tables, the 104 entity loot tables, and the
leafcutter anthill worldgen feature.

Sources: `alexsmobs.jar` version **1.22.9**, `data/alexsmobs/loot_modifiers/`,
`data/alexsmobs/loot_tables/{gameplay,blocks,entities}/`,
`data/alexsmobs/worldgen/`, `data/alexsmobs/forge/`, and
`assets/alexsmobs/lang/en_us.json`; the decompiled `misc/`, `world/`, `entity/`
and `tileentity/` packages for everything that is implemented in code rather
than in JSON; the live server's `/config/alexsmobs.toml` and
`/config/alexsmobs/leafcutter_anthill_spawns.json`.

Every percentage below is computed from the weights in the JSON, not carried
over. Where the decompiled code used SRG names the constants were cross-read
against the clean upstream source (`AlexModGuy/AlexsMobs`, branch `1.20`);
three item constants only resolved that way and are flagged inline.

## Global loot modifiers

Four Forge global loot modifiers, registered in
`misc/AMLootRegistry.java`. Each one is a JSON file in
`data/alexsmobs/loot_modifiers/` naming the vanilla loot table it attaches to,
plus a Java class holding the actual condition — the JSON alone never states
the probability.

These are the only places Alex's Mobs alters vanilla loot.

| Modifier | Vanilla loot table it injects into | Item added | Count | Chance on this server |
|---|---|---|---:|---|
| `ancient_dart` | `minecraft:chests/jungle_temple` **and** `minecraft:chests/jungle_temple_dispenser` | Ancient Dart | 1 | 100% |
| `banana_drop` | `minecraft:blocks/jungle_leaves` | Banana | 1 | 0.50% per leaf block, rising with Fortune |
| `blossom_drop` | `minecraft:blocks/acacia_leaves` | Acacia Blossom | 1 | 0.77% per leaf block, rising with Fortune |
| `pigshoes` | `minecraft:gameplay/piglin_bartering` | Pigshoes | 1 | 2.50% per barter |

**`ancient_dart`.** `AncientDartLootModifier` gates on
`AMConfig.addLootToChests` (`true` on this server) and then rolls
`random.nextInt(1) == 0`, which is always true. Every jungle temple chest and
every jungle temple dispenser therefore contains exactly one extra Ancient
Dart. There is no randomness in this modifier at all.

**`banana_drop` and `blossom_drop`.** `BananaLootModifier` and
`BlossomLootModifier` are the same code with different constants. Both return
the loot unchanged if the tool carries Silk Touch or is a pair of shears.
Otherwise:

```
step   = floor(chance * 0.1)
rarity = chance - (fortuneLevel * step)
drops if rarity < 1 or random.nextInt(rarity) == 0
```

The server runs `bananaChance = 200` and `acaciaBlossomChance = 130`, with
`bananasDropFromLeaves` and `acaciaBlossomsDropFromLeaves` both `true`.

| Fortune | Banana rarity | Banana chance | Blossom rarity | Blossom chance |
|---|---:|---:|---:|---:|
| none | 1 in 200 | 0.500% | 1 in 130 | 0.769% |
| I | 1 in 180 | 0.556% | 1 in 117 | 0.855% |
| II | 1 in 160 | 0.625% | 1 in 104 | 0.962% |
| III | 1 in 140 | 0.714% | 1 in 91 | 1.099% |

The tags `#alexsmobs:drops_bananas` and `#alexsmobs:drops_acacia_blossoms`
contain exactly `minecraft:jungle_leaves` and `minecraft:acacia_leaves`, and
the modifiers hook those two vanilla loot tables directly. No modded leaf block
drops either item.

**`pigshoes`.** `PigshoesLootModifier` gates on `AMConfig.addLootToChests`,
then rolls `random.nextFloat() <= AMConfig.tusklinShoesBarteringChance`. The
server runs `0.025`, so 2.5% of piglin barters yield a pair of Pigshoes in
addition to the normal barter result.

### Two vanilla-loot changes that are not loot modifiers

- **A Mantis Shrimp that kills a Shulker.** `EntityMantisShrimp.awardKillScore`
  overwrites the Shulker's `DeathLootTable` with the empty table and then spawns
  a Shulker Shell directly. The shell is guaranteed, and the Shulker's own drops
  are suppressed. (Resolved against upstream — the decompiled form reads
  `BuiltInLootTables.f_78712_` and `Items.f_42748_`.)
- **A Mantis Shrimp that punches a fish.** Any untamed Mantis Shrimp punching an
  `AbstractFish` target sets that fish's `DeathLootTable` to empty, so the fish
  drops nothing when it dies.

Separately, `event/ServerEvents.onEntityDrops` returns the Vine Lasso when a
lassoed mob of any kind dies — the lasso is added to that mob's drops
regardless of which mod the mob came from.

## Gameplay loot tables

Ten tables in `data/alexsmobs/loot_tables/gameplay/`. None of them are chest
loot; each is rolled by a specific mob behaviour or block.

### `anteater_reward` — Anteater raiding an anthill

Rolled by `AnteaterAIRaidNest` when an anteater finishes eating at an ant nest.
The pool's roll count is a uniform integer from **-4 to 1**, and only the value
`1` produces a roll: **1 in 6 raids (16.7%) drops anything at all**. When it
does, one item from a pool of total weight 49:

| Item | Weight | Share of a successful roll | Per raid |
|---|---:|---:|---:|
| Dirt | 20 | 40.82% | 6.80% |
| Coarse Dirt | 10 | 20.41% | 3.40% |
| Rooted Dirt | 5 | 10.20% | 1.70% |
| Leafcutter Ant Pupa | 5 | 10.20% | 1.70% |
| Hanging Roots | 5 | 10.20% | 1.70% |
| Maggot | 2 | 4.08% | 0.68% |
| Beetroot | 1 | 2.04% | 0.34% |
| Potato | 1 | 2.04% | 0.34% |

### `platypus_reward` — Platypus digging

Rolled by `PlatypusAIDigForItems` each time a platypus finishes digging a block
tagged `#alexsmobs:platypus_digables` underwater. One item per dig, total
weight 27.

| Item | Weight | Chance |
|---|---:|---:|
| Clay Ball | 20 | 74.07% |
| Maggot | 7 | 25.93% |

### `platypus_supercharged_reward` — supercharged Platypus digging

The same goal picks this table instead when `platypus.superCharged` is set.
Total weight 31.

| Item | Count | Weight | Chance |
|---|---|---:|---:|
| Clay Ball | 1–2 | 20 | 64.52% |
| Maggot | 1 | 10 | 32.26% |
| Fedora | 1 | 1 | 3.23% |

The Fedora is the only source in this table that is not also in the ordinary
one.

### `pupfish_reward` — Devil's Hole Pupfish feeding

Rolled by the pupfish's feeding goal. After a feed completes there is a
**1 in 3** chance the table is rolled at all; the table itself holds a single
entry, so a successful roll is always one Slime Ball. Net: one Slime Ball per
three completed feeds.

### `seal_reward` — Seal diving for a player

Rolled by `SealAIDiveForItems` when a seal that has been fed by a player
completes a dive and returns. One item, total weight 310.

| Item | Count | Weight | Chance |
|---|---|---:|---:|
| Sand | 1–10 | 60 | 19.35% |
| Kelp | 2–4 | 60 | 19.35% |
| Gravel | 8–16 | 40 | 12.90% |
| Shark Tooth | 1 | 21 | 6.77% |
| Clay Ball | 5–32 | 20 | 6.45% |
| Wet Sponge | 1–2 | 20 | 6.45% |
| Ink Sac | 1 | 19 | 6.13% |
| Water Bottle | 1 | 10 | 3.23% |
| Prismarine Crystals | 1 | 10 | 3.23% |
| Prismarine Shard | 2–5 | 8 | 2.58% |
| Serrated Shark Tooth | 1 | 8 | 2.58% |
| Fish Bones | 1 | 6 | 1.94% |
| *(reroll on `minecraft:gameplay/fishing/junk`)* | — | 4 | 1.29% |
| Scute | 1 | 2 | 0.65% |
| Turtle Egg | 1 | 1+1 | 0.65% |
| Tube / Brain / Bubble / Fire / Horn Coral | 1 | 2 each | 0.65% each |
| Lobster Bucket | 1 | 2 | 0.65% |
| Music Disc — Thime | 1 | 2 | 0.65% |
| Tube / Brain / Bubble / Fire / Horn Coral Block | 1 | 1 each | 0.32% each |
| Nautilus Shell | 1 | 1 | 0.32% |

Turtle Egg appears as two separate weight-1 entries, which is why it lands at
0.65% rather than 0.32%. The junk entry carries `quality: -2`, so a higher Luck
value makes it *less* likely.

### `sugar_glider_reward` — Sugar Glider foraging leaves

`EntitySugarGlider.getForageLoot` runs after 100 ticks (5 seconds) of foraging
on a block in `#minecraft:leaves`, and checks three tiers in order:

1. **10%** — a rare item specific to that leaf species (`LEAF_TO_RARES`).
2. **next 15%** (a roll under 0.25 that was not under 0.10) — the sapling for
   that leaf species (`LEAF_TO_SAPLING`).
3. **remaining 75%** — one item from `sugar_glider_reward`, total weight 142:

| Item | Weight | Share of the table | Per forage |
|---|---:|---:|---:|
| Stick | 45 | 31.69% | 23.77% |
| Hanging Roots | 10 | 7.04% | 5.28% |
| Feather | 10 | 7.04% | 5.28% |
| Sweet Berries | 10 | 7.04% | 5.28% |
| Egg | 10 | 7.04% | 5.28% |
| Cobweb | 9 | 6.34% | 4.75% |
| Wheat Seeds | 7 | 4.93% | 3.70% |
| Arrow | 7 | 4.93% | 3.70% |
| Maggot | 5 | 3.52% | 2.64% |
| Bamboo | 5 | 3.52% | 2.64% |
| Moss Carpet | 4 | 2.82% | 2.11% |
| Vine | 3 | 2.11% | 1.58% |
| Glow Berries | 3 | 2.11% | 1.58% |
| Cockroach Wing | 3 | 2.11% | 1.58% |
| Cockroach Ootheca | 3 | 2.11% | 1.58% |
| Honeycomb | 3 | 2.11% | 1.58% |
| Fern | 2 | 1.41% | 1.06% |
| Bear Fur | 2 | 1.41% | 1.06% |
| Moose Antler | 1 | 0.70% | 0.53% |

The "per forage" column assumes the leaf species has both a rare list and a
sapling mapping. On a species with neither, the table is rolled every time and
the middle column applies directly.

### `trader_elephant_chest` — Trader Elephant inventory

Filled once, at spawn, by `EntityElephant.addElephantLoot`. A trader elephant
is created in `ServerEvents.onEntityFinalizeSpawn` whenever a Wandering Trader
spawns: the elephant appears with probability `elephantTraderSpawnChance`
(**0.6**) and, because `limitElephantTraderBiomes` is `true`, only in a biome
whose base temperature is at least 1.0. Neither option is exposed in
`alexsmobs.toml` on this server, so both run at the code default.

Three pools:

| Pool | Rolls | Contents |
|---|---|---|
| `trader_elephant_chest_emerald` | 0 or 1 | Emerald ×0–1 |
| `trader_elephant_book` | 0 or 1 | Animal Dictionary ×0–1 |
| `trader_elephant_chest` | 2–13 | the weighted table below |

The first two pools each roll 0 or 1 times with equal probability, and the item
count inside is itself 0–1, so each yields its item **25%** of the time. The
main pool rolls a uniform 2–13 times (mean 7.5) over total weight 86:

| Item | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Sand | 1–2 | 20 | 23.26% |
| Maggot | 1–2 | 14 | 16.28% |
| Mosquito Larva | 1 | 11 | 12.79% |
| Banana | 1 | 5 | 5.81% |
| Acacia Blossom | 1 | 5 | 5.81% |
| Cockroach Wing Fragment | 1–2 | 5 | 5.81% |
| Shark Tooth | 1 | 5 | 5.81% |
| Tarantula Hawk Wing Fragment | 1 | 5 | 5.81% |
| Emu Egg | 1 | 4 | 4.65% |
| Stick | 1 | 3 | 3.49% |
| Centipede Leg | 1 | 3 | 3.49% |
| Cobweb | 1 | 3 | 3.49% |
| Emu Feather | 1 | 2 | 2.33% |
| Crocodile Scute | 1 | 1 | 1.16% |

### `transmutation_table_common` / `_uncommon` / `_rare`

`TileEntityTransmutationTable.rollPossiblity` fills the table's three output
slots — slot 0 always from the common table, slot 1 from the uncommon table,
slot 2 from the rare table. One item per slot. Each transmute costs
`transmutingExperienceCost` = **3 experience levels** on this server.

`limitTransmutingToLootTables` is `false` here, which enables the second path:
for a player the table has seen before, one of the three slots (index 0 or 1)
may instead be replaced by an item drawn from that player's own transmutation
history. The chance is `min(0.01875 × totalWeight, 0.20)` — capped at **20%**,
and reached at a stored weight of 10.67 or above.

**Common** (total weight 125):

| Item | Weight | Chance |
|---|---:|---:|
| Dirt | 25 | 20.00% |
| Stick | 22 | 17.60% |
| Cobblestone | 20 | 16.00% |
| Sand | 15 | 12.00% |
| Snowball | 15 | 12.00% |
| Clay Ball | 6 | 4.80% |
| Granite | 4 | 3.20% |
| Diorite | 4 | 3.20% |
| Andesite | 4 | 3.20% |
| Torch | 3 | 2.40% |
| Kelp | 3 | 2.40% |
| Red Sand | 2 | 1.60% |
| Cobbled Deepslate | 1 | 0.80% |
| Netherrack | 1 | 0.80% |

**Uncommon** (total weight 129):

| Item | Weight | Chance |
|---|---:|---:|
| Raw Copper | 25 | 19.38% |
| Flint | 22 | 17.05% |
| Raw Iron | 20 | 15.50% |
| Coal | 20 | 15.50% |
| Wheat | 9 | 6.98% |
| Gunpowder | 5 | 3.88% |
| Redstone | 5 | 3.88% |
| Glowstone Dust | 4 | 3.10% |
| Book | 4 | 3.10% |
| Slime Ball | 3 | 2.33% |
| Feather | 3 | 2.33% |
| Melon Slice | 3 | 2.33% |
| Raw Gold | 2 | 1.55% |
| Pumpkin | 2 | 1.55% |
| Capsid | 1 | 0.78% |
| Acacia Blossom | 1 | 0.78% |

**Rare** (total weight 124):

| Item | Weight | Chance |
|---|---:|---:|
| Gilded Blackstone | 20 | 16.13% |
| Raw Copper | 12 | 9.68% |
| Quartz | 12 | 9.68% |
| Blaze Rod | 12 | 9.68% |
| Prismarine Crystals | 12 | 9.68% |
| Prismarine Shard | 12 | 9.68% |
| Amethyst Shard | 10 | 8.06% |
| Lapis Lazuli | 10 | 8.06% |
| Ender Pearl | 9 | 7.26% |
| Ghast Tear | 5 | 4.03% |
| End Rod | 4 | 3.23% |
| Emerald | 2 | 1.61% |
| Diamond | 1 | 0.81% |
| Mimicream | 1 | 0.81% |
| Shulker Shell | 1 | 0.81% |
| Nautilus Shell | 1 | 0.81% |

The rare table is the only renewable source of Mimicream, Shulker Shell and
Nautilus Shell in this table, each at 0.81% of the third slot.

## Block drops

25 block loot tables. Fourteen of them are plain "drops itself" tables and are
omitted. What follows is everything that is not.

| Block | Without Silk Touch | With Silk Touch |
|---|---|---|
| `sand_circle` | Sand | Sand |
| `red_sand_circle` | Red Sand | Red Sand |
| `caiman_egg` | nothing | the egg |
| `crocodile_egg` | nothing | the egg |
| `platypus_egg` | nothing | the egg |
| `crystalized_banana_slug_mucus` | nothing | the block |
| `rainbow_glass` | nothing | the block |
| `leafcutter_anthill` | nothing | the anthill, with its `Ants` NBT copied into the item |
| `transmutation_table` | **a Nether Star** | the table |
| `leafcutter_ant_chamber` | see below | the chamber block |
| `ender_residue` | nothing | nothing |
| `skunk_spray` | nothing | nothing |
| `terrapin_egg` | nothing | nothing |

**`leafcutter_ant_chamber`** is the only block with a Fortune interaction.
Without Silk Touch, a `table_bonus` roll on Fortune decides between a
Leafcutter Ant Pupa and the chamber block itself:

| Fortune | Chance of a Pupa | Otherwise |
|---|---:|---|
| none | 10% | Leafcutter Ant Chamber |
| I | 14.29% | Leafcutter Ant Chamber |
| II | 25% | Leafcutter Ant Chamber |
| III or higher | 100% | — |

**`transmutation_table`** returns its Nether Star crafting component when
broken without Silk Touch, so the block is never destroyed outright — but the
table's stored per-player transmutation history is lost, since only the Silk
Touch branch returns the block.

**`leafcutter_anthill`** breaks to nothing without Silk Touch. A Silk Touch pick
carries the colony (the `Ants` tag) into the item, so the ants survive the move.

`ender_residue`, `skunk_spray` and `terrapin_egg` have empty pool lists and
never drop anything by any means.

`sand_circle` and `red_sand_circle` are decorative variants that break into
ordinary Sand and Red Sand — the circle block itself is never returned, with or
without Silk Touch.

## Entity drops

104 loot tables in `data/alexsmobs/loot_tables/entities/`.

Reading the table:

- **Count** is a uniform integer over the stated range. Ranges whose minimum is
  at or below zero include rolls that produce nothing — for `0–2`, each of 0, 1
  and 2 is equally likely, so a third of kills drop none. Negative minimums work
  the same way: `-1–2` is four equally likely outcomes of which two yield
  nothing (50%), and `-2–1` yields nothing 75% of the time.
- **Chance** is a whole-pool condition. `23% +10%/L` means a base 23% that rises
  by 10 percentage points per level of Looting.
- **Looting** in the count column, written `+0–1/L`, adds a uniform 0 to N per
  Looting level to the item count.
- **Cooked** marks a `furnace_smelt` function conditioned on the mob being on
  fire when it dies.

> **Two rows in this table do not describe what this server does.** The
> `alexsdelight` add-on ships its own
> `data/alexsmobs/loot_tables/entities/{bison,bunfungus}.json`, which win over
> the Alex's Mobs jar by load order. In play:
>
> - **Bison** drop **2–5 Raw Bison** (`alexsdelight:raw_bison`) instead of 6–8
>   Beef, plus 0–2 Bison Fur, and **neither pool is cooked any more** — burning a
>   Bison to death no longer auto-smelts the drop. Looting is unchanged.
> - **Bunfungus** additionally drop **0–2 Raw Bunfungus**
>   (`alexsdelight:raw_bunfungus`, +0–2/L), and the Red Mushroom pool **gains a
>   0–2 Looting bonus** it does not have in the base jar.
>
> Full diff and the third override (the Kangaroo Burger recipe) in
> [addons.md](addons.md#data-it-overrides).

| Entity | Item | Count | Chance | Notes |
|---|---|---|---|---|
| `anaconda` | — | — | — | **empty table** |
| `anteater` | — | — | — | **empty table** |
| `bald_eagle` | Feather | 0–1, +0–1/L | always | |
| `banana_slug` | Banana Slug Slime | 0–2, +0–1/L | always | |
| `bison` | Beef | 6–8, +0–2/L | always | cooked — **overridden, see the note above this table** |
| `bison` | Bison Fur | 0–2, +0–1/L | always | cooked — **overridden, see the note above this table** |
| `blobfish` | Blobfish | 1 | always | |
| `blobfish` | Bone Meal | 1 | 5% | |
| `blue_jay` | Feather | 0–1, +0–1/L | always | |
| `bone_serpent` | Bone Serpent Tooth | 0–1, +0–1/L | always | |
| `bone_serpent` | Bone | 10–15, +0–3/L | always | |
| `bone_serpent` | Bone Block | 1–4, +0–2/L | always | |
| `bunfungus` | Red Mushroom | 0–2 | always | no Looting bonus — **overridden, see the note above this table** |
| `cachalot_whale` | — | — | — | **empty table**; see code-driven drops |
| `caiman` | — | — | — | **empty table** |
| `capuchin_monkey` | — | — | — | **empty table**; see code-driven drops |
| `catfish` | Raw Catfish | 0–1, +0–1/L | always | cooked; small size |
| `catfish_medium` | Raw Catfish | 2–3, +0–1/L | always | cooked; size 1 |
| `catfish_large` | Raw Catfish | 4–6, +0–1/L | always | cooked; size 2 |
| `centipede_body` | — | — | — | **empty table** |
| `centipede_head` | Centipede Leg | 0–2, +0–1/L | always | |
| `centipede_tail` | — | — | — | **empty table** |
| `cockroach` | Cockroach Wing Fragment | 0–1, +0–1/L | always | |
| `cockroach_maracas` | Cockroach Wing Fragment | 0–1, +0–1/L | always | roach holding maracas |
| `cockroach_maracas` | Sombrero | 1 | 20% +1%/L | |
| `cockroach_maracas` | Maraca | 1 | always | |
| `cockroach_maracas_headless` | Cockroach Wing Fragment | 0–1, +0–1/L | always | headless roach with maracas |
| `cockroach_maracas_headless` | Maraca | 1 | always | no Sombrero |
| `comb_jelly` | Rainbow Jelly | 0–2, +0–1/L | always | |
| `cosmaw` | Chorus Fruit | 0–1, +0–1/L | always | |
| `cosmic_cod` | Cosmic Cod | 1 | always | |
| `cosmic_cod` | Bone Meal | 1 | 5% | |
| `crimson_mosquito` | Mosquito Proboscis | 1 | 10% +1%/L | no blood |
| `crimson_mosquito_full` | Mosquito Proboscis | 1 | 10% +1%/L | blood level > 0 |
| `crimson_mosquito_full` | Blood Sac | 1 | 80% +1%/L | |
| `crimson_mosquito_fly` | Mosquito Proboscis | 1 | 30% +3%/L | grown from a Fly |
| `crimson_mosquito_fly` | Blood Sac | 1 | 10% +1%/L | |
| `crimson_mosquito_fly_full` | Mosquito Proboscis | 1 | 50% +3%/L | from a Fly, blood level > 0 |
| `crimson_mosquito_fly_full` | Blood Sac | 1 | always | |
| `crocodile` | Crocodile Scute | -1–2, +0–1/L | always | 50% nothing |
| `crocodile` | Crocodile Egg | -2–1, +0–1/L | always | 75% nothing |
| `crow` | Feather | 0–1, +0–1/L | always | |
| `devils_hole_pupfish` | — | — | — | **empty table** |
| `dropbear` | Dropbear Claw | 0–2, +0–1/L | always | |
| `elephant` | — | — | — | **empty table**; see code-driven drops |
| `emu` | Emu Feather | 0–2, +0–1/L | always | |
| `emu` | Feather | -1–1, +0–1/L | always | 67% nothing |
| `endergrade` | — | — | — | **empty table**; see code-driven drops |
| `enderiophage` | Capsid | 1 | always | |
| `farseer` | Farseer Arm | 0–1, +0–1/L | always | |
| `flutter` | Spore Blossom | 0–1, +0–1/L | always | |
| `fly` | Maggot | 0–2, +0–1/L | always | |
| `flying_fish` | Flying Fish | 1 | always | |
| `flying_fish` | Bone Meal | 1 | 5% | |
| `frilled_shark` | — | — | — | **empty table**; see code-driven drops |
| `froststalker` | Froststalker Horn | 1 | 23% +10%/L | **player kill only** |
| `froststalker_spikes` | Froststalker Horn | 1 | 33% +10%/L | spiked variant; no player-kill requirement |
| `froststalker_spikes` | Packed Ice | 0–3, +0–1/L | always | |
| `froststalker_spikes` | Blue Ice | 0–2, +0–1/L | always | |
| `gazelle` | Mutton | 0–1, +0–1/L | always | cooked |
| `gazelle` | Gazelle Horn | 0–1, +0–1/L | always | |
| `gelada_monkey` | — | — | — | **empty table** |
| `ghost_miner` | — | — | — | **empty table**; orphaned, see below |
| `giant_squid` | Ink Sac | 4–8 | always | no Looting bonus |
| `gorilla` | — | — | — | **empty table** |
| `grizzly_bear` | Bear Fur | -1–2, +0–1/L | always | 50% nothing |
| `grizzly_bear` | Bear Dust | 1 | 1% +1%/L | |
| `guster` | Guster Eye | 1 | 20% +10%/L | |
| `guster` | Sand | 0–3, +0–1/L | always | cooked (to glass) |
| `guster_red` | Guster Eye | 1 | 20% +10%/L | variant 1 |
| `guster_red` | Red Sand | 0–3, +0–1/L | always | cooked |
| `guster_soul` | Guster Eye | 1 | 20% +10%/L | variant 2 |
| `guster_soul` | Soul Sand | 0–3, +0–1/L | always | cooked |
| `hammerhead_shark` | — | — | — | **empty table** |
| `hummingbird` | — | — | — | **empty table** |
| `jerboa` | — | — | — | **empty table** |
| `kangaroo` | Kangaroo Hide | 0–2, +0–1/L | always | |
| `kangaroo` | Kangaroo Meat | 1–2, +0–1/L | always | cooked |
| `komodo_dragon` | — | — | — | **empty table**; see code-driven drops |
| `laviathan` | Magma Block | 0–3, +0–1/L | always | |
| `laviathan` | Blackstone | 0–3, +0–1/L | always | |
| `laviathan_obsidian` | Obsidian | 0–3, +0–1/L | always | obsidian variant |
| `laviathan_obsidian` | Blackstone | 0–3, +0–1/L | always | |
| `leafcutter_ant` | — | — | — | **empty table** |
| `leafcutter_ant_queen` | Leafcutter Ant Pupa | 0–1, +0–1/L | always | queen variant |
| `lobster` | Lobster Tail | 0–1, +0–1/L | always | cooked |
| `maned_wolf` | — | — | — | **empty table** |
| `mimic_octopus` | Ink Sac | 0–1, +0–1/L | always | |
| `mimicube` | Mimicream | -1–1 | always | 67% nothing, no Looting bonus |
| `moose` | Moose Ribs | 1–3, +0–1/L | always | cooked |
| `mudskipper` | Tropical Fish | 1 | always | |
| `mungus` | — | — | — | **empty table**; see code-driven drops |
| `murmur` | Unsettling Kimono | 1 | 10% of pool | one pool, two entries |
| `murmur` | Red Wool | 0–1, +0–1/L | 90% of pool | |
| `murmur` | Elastic Tendon | 0–2, +0–1/L | always | |
| `orca` | — | — | — | **empty table** |
| `platypus` | — | — | — | **empty table**; see code-driven drops |
| `potoo` | Feather | 0–1, +0–1/L | always | |
| `raccoon` | Raccoon Tail | -1–1 | always | 67% nothing, no Looting bonus |
| `rain_frog` | — | — | — | **empty table** |
| `rattlesnake` | Rattlesnake Rattle | 0–1 | always | no Looting bonus |
| `rhinoceros` | — | — | — | **empty table** |
| `roadrunner` | Roadrunner Feather | -2–1, +0–1/L | always | 75% nothing |
| `roadrunner` | Feather | 0–2, +0–1/L | always | |
| `rocky_roller` | Rocky Shell | 1 | 75% +10%/L | |
| `rocky_roller` | Tuff | 0–2, +0–1/L | always | |
| `rocky_roller` | Pointed Dripstone | 0–2, +0–1/L | always | |
| `sea_bear` | — | — | — | **empty table** |
| `seagull` | Feather | 0–2, +0–1/L | always | |
| `seal` | — | — | — | **empty table** |
| `shoebill` | Feather | 0–4, +0–1/L | always | |
| `skelewag` | Skelewag Sword | 1 | 10% +5%/L | |
| `skelewag` | Novelty Hat | 1 | 1% +1.5%/L | |
| `skelewag` | Fish Bones | 1 | 30% +20%/L | |
| `skelewag` | Bone | 0–2, +0–1/L | always | |
| `skreecher` | Skreecher Soul | 1 | always | **player kill only** |
| `skunk` | — | — | — | **empty table** |
| `snow_leopard` | — | — | — | **empty table** |
| `soul_vulture` | Bone | 0–2, +0–1/L | always | |
| `soul_vulture` | Coal | 0–1, +0–1/L | always | |
| `soul_vulture_heart` | Bone | 0–2, +0–1/L | always | carrying a soul heart |
| `soul_vulture_heart` | Coal | 0–1, +0–1/L | always | |
| `soul_vulture_heart` | Soul Heart | 0–1 | always | 50% nothing, no Looting bonus |
| `spectre` | — | — | — | **empty table** |
| `straddler` | Straddlite | 1 | 20% +5%/L | |
| `straddler` | Basalt | 0–3, +0–1/L | always | |
| `stradpole` | — | — | — | **empty table** |
| `sugar_glider` | — | — | — | **empty table** |
| `sunbird` | — | — | — | **empty table** |
| `tarantula_hawk` | Tarantula Hawk Wing Fragment | 0–1, +0–1/L | always | |
| `tasmanian_devil` | — | — | — | **empty table** |
| `terrapin` | — | — | — | **empty table** |
| `tiger` | — | — | — | **empty table** |
| `toucan` | Feather | 0–1, +0–1/L | always | |
| `triops` | — | — | — | **empty table** |
| `tusklin` | Porkchop | 3–6, +0–1/L | always | cooked |
| `tusklin` | Snowball | 0–1, +0–1/L | always | |
| `void_worm` | Void Worm Eye | 1 | always | |
| `void_worm` | Void Worm Mandible | 2 | always | |
| `void_worm_splitter` | — | — | — | **empty table**; split segments drop nothing |
| `warped_mosco` | Warped Muscle | 1 | 70% +10%/L | |
| `warped_mosco` | Hemolymph Sac | 1–5, +0–1/L | always | |
| `warped_toad` | Shroomlight | 0–1, +0–1/L | 50% of pool | one pool, two entries |
| `warped_toad` | Nether Wart | 0–1, +0–1/L | 50% of pool | |

### Entities with an empty loot table

38 tables have no pools at all and drop nothing from JSON: `anaconda`,
`anteater`, `cachalot_whale`, `caiman`, `capuchin_monkey`, `centipede_body`,
`centipede_tail`, `devils_hole_pupfish`, `elephant`, `endergrade`,
`frilled_shark`, `gelada_monkey`, `ghost_miner`, `gorilla`,
`hammerhead_shark`, `hummingbird`, `jerboa`, `komodo_dragon`,
`leafcutter_ant`, `maned_wolf`, `mungus`, `orca`, `platypus`, `rain_frog`,
`rhinoceros`, `sea_bear`, `seal`, `skunk`, `snow_leopard`, `spectre`,
`stradpole`, `sugar_glider`, `sunbird`, `tasmanian_devil`, `terrapin`,
`tiger`, `triops`, `void_worm_splitter`.

### Entities with no loot table file at all

Three registered mobs have no file in `loot_tables/entities/` and so fall back
to a missing table, which is empty:

- `alligator_snapping_turtle` — drops nothing on death; its scute comes from
  shearing (below).
- `mantis_shrimp` — drops nothing on death.
- `underminer` — the loot table is empty, but the mob's held item is not; see
  below.

`ghost_miner.json` is the mirror case: a loot table with no matching entity
registration. Nothing rolls it.

### Variant tables and how the game picks them

Nine entities override `getDefaultLootTable` to swap to a variant table:

| Entity | Condition | Table used instead |
|---|---|---|
| Catfish | size 1 / size 2 | `catfish_medium` / `catfish_large` |
| Cockroach | holding maracas / headless with maracas | `cockroach_maracas` / `cockroach_maracas_headless` |
| Crimson Mosquito | blood level > 0, and whether it grew from a Fly | `crimson_mosquito_full`, `crimson_mosquito_fly`, `crimson_mosquito_fly_full` |
| Froststalker | has spikes | `froststalker_spikes` |
| Guster | variant 1 / variant 2 | `guster_red` / `guster_soul` |
| Laviathan | obsidian form | `laviathan_obsidian` |
| Leafcutter Ant | is queen | `leafcutter_ant_queen` |
| Soul Vulture | carrying a soul heart | `soul_vulture_heart` |
| Void Worm | is a splitter segment | `void_worm_splitter` |

### Drops that come from code, not JSON

None of these appear anywhere in the loot table tree.

**On death, via `dropEquipment`** — worn or carried gear returned when the mob
dies:

| Entity | Item returned | Condition |
|---|---|---|
| Capuchin Monkey | Ancient Dart | it is carrying a dart |
| Catfish | everything in its stomach inventory | always; a size-2 catfish also spits |
| Elephant | Chest, plus the full contents of its inventory | it is chested |
| Elephant | the dyed carpet it is wearing | it has a carpet and is not a trader elephant |
| Endergrade | Saddle | saddled |
| Flutter | Flower Pot | potted |
| Kangaroo | everything in its pouch inventory | always |
| Komodo Dragon | Saddle | saddled |
| Laviathan | Straddle Saddle, Straddle Helmet | whichever gear it wears |
| Platypus | Fedora | wearing one |
| Raccoon | the dyed carpet it is wearing | it has a carpet |
| Tusklin | Saddle, and the Pigshoes in its feet slot | saddled / shod |

**Underminer's pickaxe.** `EntityUnderminer` spawns holding a Ghostly Pickaxe
and overrides `getEquipmentDropChance` for the main hand to **0.5**. On a
player kill that is a 50% chance to drop the pickaxe, +1 percentage point per
Looting level. This is the mob's only drop.

**Combat and interaction drops:**

| Trigger | Result |
|---|---|
| Cachalot Whale rams a player riding a boat | 3 planks of the boat's wood type and 2 Sticks, plus a **1 in 10** chance of a Cachalot Whale Tooth; the boat is destroyed |
| Frilled Shark's bite lands on a Squid | **1 in 15** chance of a Serrated Shark Tooth |
| Giant Squid grappling a Cachalot Whale breaks free (30% per attempt) | **20%** of those escapes drop a Lost Tentacle |
| Capuchin Monkey eats an item tagged `#alexsmobs:bananas` | **1 in 4** chance of a Banana Peel |
| Mantis Shrimp kills a Shulker | guaranteed Shulker Shell (see the global-loot section) |

**Timed drops from living mobs** — these tick down while the mob is alive and
adult, and produce an item on the ground with no kill involved:

| Entity | Item | Interval |
|---|---|---|
| Banana Slug | Banana Slug Slime | 24 000–36 000 ticks (20–30 min) |
| Cockroach | Cockroach Ootheca | 24 000–48 000 ticks (20–40 min) |
| Emu | Emu Egg | 6 000–12 000 ticks (5–10 min) |
| Grizzly Bear (tamed) | Bear Fur | 24 000–48 000 ticks (20–40 min) |
| Komodo Dragon | Komodo Spit | 24 000–36 000 ticks (20–30 min) |
| Mungus | Mungal Spores | 24 000–48 000 ticks (20–40 min) |
| Roadrunner | Roadrunner Feather | 24 000–48 000 ticks (20–40 min) |

**Growth and shearing:**

| Trigger | Result |
|---|---|
| A Crocodile grows from baby to adult (needs `doMobLoot`) | 1 Crocodile Scute |
| Shearing a Bison | 2–3 Bison Fur, and the bison stays sheared until it has been fed again |
| Shearing an Alligator Snapping Turtle | a Spiked Scute with probability `moss × 5%`, otherwise Seagrass; the moss level resets to zero |
| Shearing an Elephant or Raccoon wearing a carpet | the carpet back |
| Shearing a chested Elephant | a Chest plus everything inside |
| Shearing a saddled Komodo Dragon | the Saddle |
| Shearing a potted Flutter | a Flower Pot |

## Worldgen — leafcutter anthills

One configured feature and one placed feature, both
`alexsmobs:leafcutter_anthill`. This is the mod's only worldgen feature.

**Where.** The biome modifier `alexsmobs:am_leafcutter_ant_spawns` adds the
placed feature to the `SURFACE_STRUCTURES` decoration step of every biome that
passes `/config/alexsmobs/leafcutter_anthill_spawns.json`. That file on this
server matches the mod default: any overworld biome tagged
`#minecraft:is_jungle` **except** Bamboo Jungle, plus six Terralith biomes —
Amethyst Canyon, Amethyst Rainforest, Jungle Mountains, Rocky Jungle, Tropical
Jungle and Skylands Summer. Terralith 2.5.4 is installed, so those six are live.

**How often.** The placed feature carries only an `in_square` placement
modifier — no count, no rarity filter — so it is attempted once in every chunk
of an eligible biome. The rate is set inside the feature code, which rejects the
attempt when `random.nextFloat() > 0.0175`. **About 1 chunk in 57 (1.75%) of
jungle gets an anthill**, or roughly one every 7–8 chunks in each direction.

> **The config option does not do what it says.** `alexsmobs.toml` has
> `leafcutterAnthillSpawnChance = 0.005` described as the "percent chance for
> leafcutter anthills to spawn as world gen in each chunk". The value is never
> read as a rate — `AMWorldRegistry.addLeafcutterAntSpawns` only checks that it
> is greater than zero before adding the feature to the biome. The actual rate
> is the hard-coded `0.0175` in `FeatureLeafcutterAnthill`. Setting the option
> to zero switches anthills off; any other value produces the same 1.75%.

**What generates.** The feature also aborts if the block below the surface
point is a fluid, so anthills never generate over water.

- A mound of **Coarse Dirt**, with 20% of its blocks replaced by plain Dirt,
  2–3 layers tall and a few blocks across.
- One **Leafcutter Anthill** block set into the mound, with 2 blocks of air
  above it. Each of the four sides has an independent 50% chance of a 3-block
  Coarse Dirt buttress.
- **3–5 Leafcutter Ants inside the anthill, the first of which is the queen.**
  They emerge on their own timers.
- A shaft of **Leafcutter Ant Chamber** running 1–2 blocks below the anthill,
  opening into a small spherical chamber 2–3 blocks down.

The chamber blocks are the payoff: each one broken without Silk Touch has a
10% chance (rising to 100% at Fortune III) of a Leafcutter Ant Pupa.

## Unverified

- The `LEAF_TO_RARES` and `LEAF_TO_SAPLING` maps behind the Sugar Glider's 10%
  and 15% foraging tiers were not enumerated per leaf species. The percentages
  above are exact; which rare item each leaf yields is not recorded here.
- `elephantTraderSpawnChance` (0.6) and `limitElephantTraderBiomes` (true) are
  read from `AMConfig` defaults. Neither key is present in the server's
  `alexsmobs.toml`, so they are not player-adjustable on this server, but they
  were not confirmed against a running world.
