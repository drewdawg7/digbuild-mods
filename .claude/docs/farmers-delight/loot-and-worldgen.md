<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Loot & Worldgen

Covers the 37 Forge global loot modifiers, the 112 loot tables (98 block, 14
chest), the 5 village structure pieces, and the config options that gate them.

Sources: `FarmersDelight-1.20.1-1.3.2.jar` version **1.3.2**,
`data/farmersdelight/loot_modifiers/` (37 files),
`data/forge/loot_modifiers/global_loot_modifiers.json`,
`data/farmersdelight/loot_tables/{blocks,chests}/`,
`data/farmersdelight/structures/village/houses/` (5 NBT templates, read with a
standalone NBT parser), and the decompiled
`common/loot/modifier/`, `common/world/VillageStructures.java` and
`common/Configuration.java` (jadx 1.5.4). Live config:
`/config/farmersdelight-common.toml`.

Vanilla data used for comparison (village template pools and farm processor
lists) comes from the 1.20.1 tag of `misode/mcmeta`, not from memory.

Every percentage below is computed from the weights in the JSON, not carried
over.

**Scope boundary.** Wild crop worldgen (the nine
`patch_wild_*` / `patch_*_mushroom_colony` features and the biome modifiers that
place them), crop growth, Rich Soil and the crops themselves are in
**farming.md**. This doc owns the loot tables, the loot modifiers and the
*village structure* worldgen. Where a crop's block loot table is listed here it
is listed as loot only; growth behaviour is cross-referenced, not repeated.

## Global loot modifiers

37 modifiers, all listed in `data/forge/loot_modifiers/global_loot_modifiers.json`
with `"replace": false`. There are only **four implementation classes**:

| Type | Class | Count | What it does |
|---|---|---:|---|
| `farmersdelight:add_loot_table` | `AddLootTableModifier` | 14 | rolls a whole extra loot table into the result |
| `farmersdelight:add_item` | `AddItemModifier` | 17 | appends a fixed item stack (`count`, default 1) |
| `farmersdelight:replace_item` | `ReplaceItemModifier` | 1 | strips one item from the result and appends another |
| `farmersdelight:pastry_slicing` | `PastrySlicingModifier` | 5 | appends slices scaled to the block's remaining bites |

### Condition semantics — AND, not OR

**All four classes extend Forge's `LootModifier`**, whose constructor builds
`LootItemConditions.andConditions(conditions)`. Every entry in a file's
`conditions` array must therefore pass. None of the four implements
`IGlobalLootModifier` directly, and no file in this mod carries two
`forge:loot_table_id` conditions — the 14 chest modifiers each name exactly one
table. Where the mod wants an OR it says so explicitly with
`minecraft:any_of` (used in `add_onion_to_illagers`, `add_onion_to_zombies`,
`scavenging_leather`, `scavenging_string` and `slicing_candle_cake`). The
AND-vs-OR trap does not bite here.

Two structural notes that do matter:

- The 14 `add_loot_table` modifiers are the only ones with a
  `forge:loot_table_id` condition. Every other modifier is scoped **purely by
  its block/entity/tool predicates**, so it fires on any loot table roll whose
  context matches — including tables added by other mods that use the vanilla
  entity or block in question.
- `AddLootTableModifier.doApply` checks `Configuration.GENERATE_FD_CHEST_LOOT`
  at runtime. The other three types have no config gate.

### Chest loot — 14 modifiers, one per vanilla chest table

Each injects an extra Farmer's Delight table on top of the vanilla contents;
nothing vanilla is removed. All 14 are switched off together by
`generateFDChestLoot = false` (this server: **true**).

| Vanilla table injected into | FD table rolled | Headline result |
|---|---|---|
| `minecraft:chests/abandoned_mineshaft` | `fd_abandoned_mineshaft` | Cooking Pot / Skillet, seeds, rope |
| `minecraft:chests/simple_dungeon` | `fd_simple_dungeon` | seeds, rope |
| `minecraft:chests/shipwreck_supply` | `fd_shipwreck_supply` | seeds, onions, rice, rope |
| `minecraft:chests/pillager_outpost` | `fd_pillager_outpost` | onions and onion crates |
| `minecraft:chests/ruined_portal` | `fd_ruined_portal` | Golden Knife |
| `minecraft:chests/bastion_hoglin_stable` | `fd_bastion_hoglin_stable` | Golden/Diamond Knife, ham |
| `minecraft:chests/bastion_treasure` | `fd_bastion_treasure` | Diamond Knife |
| `minecraft:chests/end_city_treasure` | `fd_end_city_treasure` | treasure-enchanted knife |
| `minecraft:chests/village/village_butcher` | `fd_village_butcher` | Flint/Iron Knife, meats |
| `minecraft:chests/village/village_plains_house` | `fd_village_plains_house` | onion / tomato seeds |
| `minecraft:chests/village/village_savanna_house` | `fd_village_savanna_house` | tomato / cabbage seeds |
| `minecraft:chests/village/village_snowy_house` | `fd_village_snowy_house` | onion / cabbage seeds |
| `minecraft:chests/village/village_taiga_house` | `fd_village_taiga_house` | cabbage seeds / rice |
| `minecraft:chests/village/village_desert_house` | `fd_village_desert_house` | tomato seeds / rice |

Full contents are in [Chest loot tables](#chest-loot-tables) below.

### Mob drops — onion from illagers and zombies

Two `add_item` modifiers, identical apart from the entity list.

| Modifier | Fires on | Conditions | Result |
|---|---|---|---|
| `add_onion_to_illagers` | Pillager, Evoker, Vindicator | killed by a player | 1 Onion, **2% + 1 percentage point per Looting level** |
| `add_onion_to_zombies` | Zombie, Husk, Zombie Villager | killed by a player | 1 Onion, **2% + 1 pp per Looting level** |

`random_chance_with_looting` with `chance: 0.02, looting_multiplier: 0.01`:

| Looting | Chance |
|---|---:|
| none | 2% |
| I | 3% |
| II | 4% |
| III | 5% |

Drowned, zombified piglins and zombie horses are not in either list.

### Knife scavenging — 10 modifiers

All require the **killer's main hand** to hold an item tagged
`farmersdelight:tools/knives` (see [Cross-mod loot](#cross-mod-loot) for what is
in that tag on this server). None of them requires a player kill: a mob or a
dispenser-held knife satisfies the same predicate.

| Modifier | Mob | Extra drop | Chance |
|---|---|---|---|
| `scavenging_feather` | Chicken | 1 Feather | **100%** |
| `scavenging_leather` | Cow, Mooshroom, Horse, Donkey, Mule, Llama, Trader Llama | 1 Leather | **100%** |
| `scavenging_rabbit_hide` | Rabbit | 1 Rabbit Hide | **100%** |
| `scavenging_string` | Spider, Cave Spider | 1 String | **100%** |
| `scavenging_shulker_shell` | Shulker | 1 Shulker Shell | **100%** |
| `scavenging_ham_from_pig` | Pig, not on fire | 1 Ham | 50% +10 pp/Looting |
| `scavenging_smoked_ham_from_pig` | Pig, on fire | 1 Smoked Ham | 50% +10 pp/Looting |
| `scavenging_ham_from_hoglin` | Hoglin, not on fire | 1 Ham | **100%** |
| `scavenging_smoked_ham_from_hoglin` | Hoglin, on fire | 1 Smoked Ham | **100%** |
| `scavenging_pumpkin` | *(block)* Pumpkin | see below | — |

The pig pair and the hoglin pair are mutually exclusive on the `is_on_fire`
flag, so a burning pig can only ever yield Smoked Ham, never both.

Pig ham chance by Looting (`chance: 0.5, looting_multiplier: 0.1`):

| Looting | Chance |
|---|---:|
| none | 50% |
| I | 60% |
| II | 70% |
| III | 80% |

**`scavenging_pumpkin`** is the only `replace_item` modifier in the mod. Breaking
a `minecraft:pumpkin` with a knife that does **not** carry Silk Touch removes the
Pumpkin from the drops and substitutes **4 Pumpkin Slices**. A Silk Touch knife,
or any non-knife tool, gets the ordinary Pumpkin. This is the only place in the
mod where Silk Touch changes a result.

### Pastry slicing — 6 modifiers

Five `pastry_slicing` modifiers plus one `add_item`. All require a knife
(`minecraft:match_tool` against the knives tag) and a matching block.

`PastrySlicingModifier` reads the block's bite counter and emits
`7 − bites` slices for a `CakeBlock` and `4 − bites` for a Farmer's Delight
`PieBlock`.

| Modifier | Block | Slice item | Count |
|---|---|---|---|
| `slicing_cake` | `minecraft:cake` | Slice of Cake | 7 − bites (7 on an untouched cake) |
| `slicing_apple_pie` | `farmersdelight:apple_pie` | Slice of Apple Pie | 4 − bites |
| `slicing_chocolate_pie` | `farmersdelight:chocolate_pie` | Slice of Chocolate Pie | 4 − bites |
| `slicing_pumpkin_pie` | `farmersdelight:pumpkin_pie` | Slice of Pumpkin Pie | 4 − bites |
| `slicing_sweet_berry_cheesecake` | `farmersdelight:sweet_berry_cheesecake` | Slice of Sweet Berry Cheesecake | 4 − bites |
| `slicing_candle_cake` | all 17 candle cake blocks | Slice of Cake | **7**, fixed |

This is load-bearing rather than cosmetic: the four Farmer's Delight pie blocks
and vanilla `minecraft:cake` all have loot tables with **no pools at all**.
Broken with anything other than a knife they drop nothing, and the modifier is
the only way to recover them. Candle cakes are the exception — the vanilla table
still returns the candle, and the modifier adds 7 slices on top; because a
candle cake cannot be bitten, the count is hard-coded rather than computed.

### Straw — 5 modifiers

All five require a tool tagged `farmersdelight:straw_harvesters`, which in this
jar contains exactly `#farmersdelight:tools/knives`.

| Modifier | Block | Condition | Straw | Chance |
|---|---|---|---:|---:|
| `straw_from_mature_wheat` | `minecraft:wheat` | `age = 7` | 1 | **100%** |
| `straw_from_mature_rice` | `farmersdelight:rice_panicles` | `age = 3` | 1 | **100%** |
| `straw_from_grass` | `minecraft:grass` (short grass) | — | 1 | 20% |
| `straw_from_tall_grass` | `minecraft:tall_grass` | — | 1 | 20% |
| `straw_from_sandy_shrub` | `farmersdelight:sandy_shrub` | — | 1 | 30% |

No Fortune or Looting scaling on any of them, and no Silk Touch exclusion — a
Silk Touch knife still produces straw.

## Chest loot tables

14 tables in `data/farmersdelight/loot_tables/chests/`. Each is rolled *in
addition to* the vanilla table it is attached to. "Nothing" rows are
`minecraft:empty` entries and are shown because they set the real odds.

### `fd_abandoned_mineshaft`

Three pools.

Pool 1 — 1 roll, total weight 8:

| Entry | Weight | Chance |
|---|---:|---:|
| Cooking Pot | 1 | 12.50% |
| Skillet (15–80% damaged) | 1 | 12.50% |
| nothing | 6 | 75.00% |

Pool 2 — 1–4 rolls (mean 2.5), total weight 5:

| Entry | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Tomato Seeds | 2–4 | 1 | 20.00% |
| Cabbage Seeds | 2–4 | 1 | 20.00% |
| Rice | 2–4 | 1 | 20.00% |
| nothing | — | 2 | 40.00% |

Pool 3 — 3 rolls, total weight 3:

| Entry | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Rope | 2–12 | 1 | 33.33% |
| nothing | — | 2 | 66.67% |

Three rolls at 1 in 3 means **70.4% of mineshaft chests contain rope**, averaging
7 rope across the chest.

### `fd_simple_dungeon`

Pool 1 — 1–4 rolls (mean 2.5), total weight 4:

| Entry | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Tomato Seeds | 2–4 | 1 | 25.00% |
| Cabbage Seeds | 2–4 | 1 | 25.00% |
| nothing | — | 2 | 50.00% |

Pool 2 — 3 rolls, total weight 3: Rope ×2–12 at 33.33% per roll, nothing at
66.67%. Same arithmetic as the mineshaft pool: 70.4% of dungeon chests hold rope.

### `fd_shipwreck_supply`

Pool 1 — 1–2 rolls (mean 1.5), total weight 24, **no empty entry**, so every
roll produces something:

| Entry | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Tomato Seeds | 2–4 | 6 | 25.00% |
| Cabbage Seeds | 2–4 | 6 | 25.00% |
| Onion | 2–4 | 6 | 25.00% |
| Rice | 2–4 | 6 | 25.00% |

Pool 2 — 1–3 rolls (mean 2), total weight 3: Rope ×4–12 at **66.67%** per roll,
nothing at 33.33%. Expected rope per supply chest is about 10.7 — the richest
rope source of the 14 tables.

### `fd_pillager_outpost`

1–2 rolls (mean 1.5), total weight 9:

| Entry | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Onion | 4–12 | 5 | 55.56% |
| Onion Crate | 1–3 | 2 | 22.22% |
| nothing | — | 2 | 22.22% |

### `fd_ruined_portal`

1 roll, total weight 4:

| Entry | Weight | Chance |
|---|---:|---:|
| Golden Knife, `enchant_randomly` | 1 | 25.00% |
| nothing | 3 | 75.00% |

### `fd_bastion_hoglin_stable`

Pool 1 — 1 roll, total weight 5:

| Entry | Weight | Chance |
|---|---:|---:|
| Diamond Knife, 15–80% damaged, `enchant_randomly` | 1 | 20.00% |
| Golden Knife, `enchant_randomly` | 2 | 40.00% |
| nothing | 2 | 40.00% |

Pool 2 — 1–2 rolls (mean 1.5), total weight 8:

| Entry | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Ham | 2–5 | 4 | 50.00% |
| Smoked Ham | 2–5 | 2 | 25.00% |
| nothing | — | 2 | 25.00% |

### `fd_bastion_treasure`

1 roll, total weight 8:

| Entry | Weight | Chance |
|---|---:|---:|
| Diamond Knife, **80–100% damaged**, `enchant_randomly` | 1 | 12.50% |
| Diamond Knife, undamaged, unenchanted | 1 | 12.50% |
| nothing | 6 | 75.00% |

25% of bastion treasure chests hold a Diamond Knife; half of those are nearly
broken.

### `fd_end_city_treasure`

1 roll, total weight 8:

| Entry | Weight | Chance |
|---|---:|---:|
| Diamond Knife, `enchant_with_levels` 20–39, treasure allowed | 1 | 12.50% |
| Iron Knife, `enchant_with_levels` 20–39, treasure allowed | 1 | 12.50% |
| nothing | 6 | 75.00% |

The only table in the mod that can produce a treasure enchantment.

### `fd_village_butcher`

Pool 1 — 1 roll, total weight 3:

| Entry | Weight | Chance |
|---|---:|---:|
| Flint Knife | 1 | 33.33% |
| Iron Knife | 1 | 33.33% |
| nothing | 1 | 33.33% |

Pool 2 — 1–2 rolls (mean 1.5), total weight 11:

| Entry | Count | Weight | Chance per roll |
|---|---|---:|---:|
| Ham | 1 | 1 | 9.09% |
| Minced Beef | 2–6 | 3 | 27.27% |
| Raw Bacon | 2–6 | 3 | 27.27% |
| Raw Mutton Chops | 2–6 | 3 | 27.27% |
| nothing | — | 1 | 9.09% |

### The five village house tables

`fd_village_plains_house`, `fd_village_savanna_house`, `fd_village_snowy_house`,
`fd_village_taiga_house` and `fd_village_desert_house` share one shape: a single
pool, **1–3 rolls** (mean 2), two entries of equal weight, **no empty entry**,
each stacking **1–3**.

| Table | 50% | 50% |
|---|---|---|
| plains | Onion | Tomato Seeds |
| savanna | Tomato Seeds | Cabbage Seeds |
| snowy | Onion | Cabbage Seeds |
| taiga | Cabbage Seeds | Rice |
| desert | Tomato Seeds | Rice |

Every village house chest of these five types gains 1–3 stacks of Farmer's
Delight seeds or produce.

## Block loot tables

98 tables in `data/farmersdelight/loot_tables/blocks/`. 56 are plain "drops
itself, subject to `survives_explosion`" and are omitted: the 6 crates, the 34
canvas signs and hanging canvas signs, `canvas_rug`, `cutting_board`,
`full_tatami_mat`, `half_tatami_mat`, `tatami`, `organic_compost`, `rice`,
`rice_bag`, `rice_bale`, `rich_soil`, `rope`, `rope_fence`, `rope_fence_gate`,
`safety_net`, `stove` and `straw_bale`.

**No block loot table in this mod references Silk Touch.** The only Silk Touch
interaction the mod has is the `scavenging_pumpkin` loot modifier above. Shears
appear instead, through `forge:can_tool_perform_action` with
`shears_harvest` — which any shears-capable tool satisfies, not only vanilla
shears.

### Tables that drop nothing at all

| Block | Note |
|---|---|
| `apple_pie` | no pools — knife slicing is the only recovery |
| `chocolate_pie` | no pools |
| `pumpkin_pie` | no pools |
| `sweet_berry_cheesecake` | no pools |

### Storage blocks that preserve state

| Block | Function | Effect |
|---|---|---|
| 11 cabinets (oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, bamboo, crimson, warped) | `copy_name` | a renamed cabinet keeps its name |
| `wooden_basket`, `bamboo_basket` | `copy_name` | same |
| `cooking_pot` | `copy_name` + `farmersdelight:copy_meal` | the pot keeps the meal it was cooking |
| `skillet` | `farmersdelight:copy_skillet` | the skillet keeps its contents |
| `rich_soil_farmland` | — | reverts to `farmersdelight:rich_soil` |

### Feast blocks

Six feast blocks drop the block back only while untouched, and a container once
any serving has been taken.

| Block | Full | Partly eaten |
|---|---|---|
| `roast_chicken_block` (4 servings) | the block | Bowl **+** Bone Meal |
| `honey_glazed_ham_block` (4) | the block | Bowl **+** Bone |
| `shepherds_pie_block` (4) | the block | Bowl |
| `gleaming_salad_block` (4) | the block | Bowl |
| `rice_roll_medley_block` (8) | the block | Bowl |
| `stuffed_pumpkin_block` (4) | the block | **nothing** |

`stuffed_pumpkin_block` is the odd one out: its table has no second pool, so a
partly eaten stuffed pumpkin is destroyed with no drop.

### Mushroom colonies

`brown_mushroom_colony` and `red_mushroom_colony` are identical apart from the
mushroom. One alternatives pool, resolved top-down:

| Age | Tool | Drop |
|---|---|---|
| 0 | any | 2 mushrooms |
| 1 | any | 3 mushrooms |
| 2 | any | 4 mushrooms |
| 3 | not shears | 5 mushrooms |
| 3 | shears | the **colony block** itself |

Only a fully grown colony can be picked up, and only with shears. No Fortune or
Silk Touch interaction.

### Crops and wild crops

Listed here as loot only — growth, ropelogging and worldgen are in farming.md.

| Block | Drop |
|---|---|
| `cabbages` | age 7: 1 Cabbage **+** Cabbage Seeds ×Binomial(3 + Fortune, 0.5714286); otherwise 1 Cabbage Seeds |
| `onions` | 1 Onion at any age, **+** a second Onion ×Binomial(3 + Fortune, 0.5714286) at age 7 |
| `tomatoes` | age 3: 1–2 Tomato +uniform(0…Fortune); Tomato Seeds unless ropelogged; 5% Rotten Tomato |
| `tomatoes_on_rope` | age 3: 1–2 Tomato +uniform(0…Fortune); 5% Rotten Tomato; no seeds |
| `budding_tomatoes` | 1 Tomato Seeds |
| `rice_panicles` | age 3 with a knife: Rice. age 3 without: Rice Panicle. Immature: nothing |
| `sandy_shrub` | shears: the shrub. Otherwise **12.5%** Beetroot Seeds, +uniform(0…2×Fortune) |
| `wild_cabbages` | shears: the wild block. Otherwise Cabbage Seeds +uniform(0…2×Fortune), **plus 20%** for 1 Cabbage |
| `wild_tomatoes` | shears: the wild block. Otherwise Tomato Seeds +uniform(0…2×Fortune), **plus 20%** for 1 Tomato |
| `wild_beetroots` | shears: the wild block. Otherwise Beetroot Seeds +uniform(0…2×Fortune), **plus 20%** for 1 Beetroot |
| `wild_onions` | shears: the wild block. Otherwise 1 Onion +uniform(0…2×Fortune), **plus 1–3 Allium** |
| `wild_carrots` | shears: the wild block. Otherwise 1 Carrot +uniform(0…2×Fortune) |
| `wild_potatoes` | shears: the wild block. Otherwise 1 Potato +uniform(0…2×Fortune) |
| `wild_rice` | two halves, each half drops the wild block with shears or 1 Rice without; each pool checks that the other half is present |

The 20% food pools on wild cabbages, tomatoes and beetroots are additionally
gated on **not** using shears, so shearing gives the transplantable block and
nothing else. Wild onions are the only wild crop that also yields a vanilla
flower.

`uniform(0…2×Fortune)` is `apply_bonus` with `uniform_bonus_count` and
`bonusMultiplier: 2`; `Binomial(3 + Fortune, 0.5714286)` is
`binomial_with_bonus_count`, the same formula vanilla wheat uses for its seeds.

### Entity loot tables

**There are none.** Farmer's Delight ships no `loot_tables/entities/` directory.
Every mob-facing change it makes goes through the 11 entity-scoped loot
modifiers above (2 onion, 9 knife scavenging — `scavenging_pumpkin` is the tenth
scavenging file but targets a block).

## Structures

Five structure templates, all in
`data/farmersdelight/structures/village/houses/`. They are not a standalone
structure — there is no structure set, no spacing and no salt. They are village
*house pieces*, added to the vanilla village pools at server start by
`VillageStructures.addNewVillageBuilding`, and gated on
`generateVillageCompostHeaps` (this server: **true**).

### Where and how often

| Piece | Added to | Weight added | Vanilla pool weight | Share of a house slot |
|---|---|---:|---:|---:|
| `plains_compost_pile` | `minecraft:village/plains/houses` | 5 | 87 | **5.4%** |
| `savanna_compost_pile` | `minecraft:village/savanna/houses` | 4 | 81 | **4.7%** |
| `taiga_compost_pile` | `minecraft:village/taiga/houses` | 4 | 76 | **5.0%** |
| `snowy_compost_pile` | `minecraft:village/snowy/houses` | 3 | 68 | **4.2%** |
| `desert_compost_pile` | `minecraft:village/desert/houses` | 3 | 72 | **4.0%** |

Roughly **1 house plot in 20**. A village places many house plots, so most
villages of these five types get at least one compost heap; a small village can
easily get none. There is no jungle or swamp variant, and no piece is added to
the zombie village pools.

Each template carries a single jigsaw block targeting `building_entrance` on
that village's `streets` pool, so the heap attaches to a road like any other
house.

### What is inside

**No compost heap contains a chest.** The loot is the blocks themselves.

| Piece | Footprint | Farmer's Delight blocks | Other notable contents |
|---|---|---|---|
| `plains_compost_pile` | 11×7×7 | 6 Organic Compost, 3 Rich Soil | oak shack with a door and glass pane, fenced yard, 2 Red Mushrooms, water |
| `savanna_compost_pile` | 9×6×5 | 3+1+1 Organic Compost (at composting stages 1, 2 and 0), 2 Rich Soil, 1 Rich Soil Farmland, 4 Cabbage crops, 4 Tomato crops | acacia lean-to, 7 farmland, 2 brown wall banners |
| `taiga_compost_pile` | 5×6×9 | 5 Organic Compost, 2 Rich Soil, **1 fully grown Brown Mushroom Colony** | cobblestone and spruce pit, open trapdoors, 3 Brown + 1 Red Mushroom |
| `snowy_compost_pile` | 7×5×9 | 8 Organic Compost, 3 Rich Soil Farmland, 7 Onion crops | spruce frame, 7 Potato crops, 11 farmland, 6 lanterns, 3 Brown Mushrooms |
| `desert_compost_pile` | 7×6×7 | 7 Organic Compost, 1 at composting stage 3, 2 Rich Soil | sandstone walls and slabs, torches, water |

The taiga heap is the only guaranteed source of a Mushroom Colony block outside
mushroom-field worldgen, and shears are needed to take it (see
[Mushroom colonies](#mushroom-colonies)).

### Crops on village farm plots

A second, separate worldgen change, gated on `generateFDCropsOnVillageFarms`
(this server: **true**). `VillageStructures` **appends** a `RuleProcessor` to
five vanilla processor lists. Rules are evaluated in order and the first match
wins, and the appended processor sees the blocks the vanilla processor already
produced.

Raw rules added:

| Processor list | Rule chain added |
|---|---|
| `minecraft:farm_plains`, `minecraft:farm_taiga` | wheat→Cabbage 30%, then wheat→Tomato 30%, then wheat→Onion 30% |
| `minecraft:farm_savanna`, `minecraft:farm_desert` | wheat→Cabbage 30%, then wheat→Tomato 30% |
| `minecraft:farm_snowy` | wheat→Cabbage 30%, wheat→Onion 30%, potato→Cabbage 20%, potato→Onion 20% |

Composed with the vanilla replacements that run first, the final make-up of a
farm plot's crop squares is:

| Village | Cabbage | Tomato | Onion | Wheat left | Vanilla crops |
|---|---:|---:|---:|---:|---|
| plains | 15.1% | 10.6% | 7.4% | 17.3% | carrots 30%, potatoes 14%, beetroots 5.6% |
| taiga | 16.8% | 11.8% | 8.2% | 19.2% | pumpkin stems 30%, potatoes 14% |
| savanna | 27.0% | 18.9% | — | 44.1% | melon stems 10% |
| desert | 21.6% | 15.1% | — | 35.3% | beetroots 20%, melon stems 8% |
| snowy | 19.8% | — | 15.3% | 8.8% | potatoes 46.1%, carrots 10% |

Snowy villages are the most heavily converted because vanilla turns 72% of their
wheat into potatoes and the cold rule chain then converts potatoes as well.

## Config gates

Every option in `/config/farmersdelight-common.toml` that switches any of the
above on or off. Nothing else in the file touches loot or worldgen.

| Option | Section | This server | Default | What it gates |
|---|---|---|---|---|
| `generateFDChestLoot` | `[world]` | **true** | true | all 14 `add_loot_table` modifiers. `false` makes them no-ops; the other 23 modifiers are unaffected |
| `generateVillageCompostHeaps` | `[world]` | **true** | true | all 5 compost pile structure pieces |
| `generateFDCropsOnVillageFarms` | `[world]` | **true** | true | the five village-farm processor rule chains |
| `cuttingBoardFortuneBonus` | `[crafting]` | **0.1** | 0.1 | Cutting Board recipe results only — not a loot table, listed here because it is the mod's other Fortune interaction |

**Every value in `farmersdelight-common.toml` on this server matches the mod
default.** That was checked by reading each `define`/`defineInRange`/`defineList`
call in `Configuration.java` and comparing the second argument against the live
file, option by option — including `enablePumpkinPieSneakToPlace`, whose default
really is `false`. No live option disables any modifier on this server.

There is **no** config option that turns off knife scavenging, straw, pastry
slicing, the pumpkin-slice replacement or the onion mob drops. Those 23
modifiers are always active.

## Cross-mod loot

**None of the 37 modifiers targets a loot table belonging to another mod.** All
14 `add_loot_table` conditions name `minecraft:` chest tables, and the other 23
are scoped by vanilla entity types, vanilla or Farmer's Delight blocks, and
tags. No rule is inert for want of a missing mod.

The interactions that do exist run the other way — other installed mods feeding
into Farmer's Delight's tags, or claiming the same vanilla tables:

- **Dungeons Delight** (`forge-dungeonsdelight-1.20.1-1.3.0.jar`) adds
  `#dungeonsdelight:cleavers` and `dungeonsdelight:stained_knife` to
  `farmersdelight:tools/knives`. The cleavers tag holds Flint, Iron, Golden,
  Diamond, Netherite and Stained Cleavers. On this server the knife tag is
  therefore **12 items**, not 5, and every scavenging, slicing, straw and
  pumpkin-slice modifier fires for all of them. Dungeons Delight also registers
  its own 21 global loot modifiers, several of which stack with these on the
  same mobs.
- **Tinkers' Construct** is installed, so the compat file
  `data/tconstruct/tags/items/seeds.json` that Farmer's Delight ships is live.
- Farmer's Delight also ships compat tags for **Create**, **Create
  Crafts & Additions**, **Origins** and **Serene Seasons**
  (`data/{create,createaddition,origins,sereneseasons}/`). **None of those four
  is installed on this server**, so those nine tag files are inert.
- The 14 chest injections attach to vanilla table *IDs*, not to vanilla
  structures. The Yung's structure mods installed here (Better Mineshafts,
  Better Dungeons, Better Strongholds and the rest) reuse the same vanilla table
  IDs, so their chests receive the Farmer's Delight pools too.
- **Loot Integrations** (`lootintegrations-1.20.1-4.7.jar`, plus
  `lootintegrations_yungs-1.6.jar`) rewrites vanilla chest tables wholesale. It
  operates on the loot table itself rather than through a Forge global loot
  modifier, so the two systems should compose — but the ordering was not
  verified in a running world. See [Unverified](#unverified).
- **Alex's Delight** (`alexsdelight-1.5.jar`) is a Farmer's Delight add-on but
  overrides only two Alex's Mobs entity tables; it touches nothing documented
  here. See `../alexs-mobs/addons.md`.

## Unverified

- **The village pool shares are computed against vanilla pool weights only.**
  Towns and Towers, Explorify and Dungeons and Taverns are all installed and all
  add entries to the same `village/*/houses` pools, which raises the denominator
  and lowers the real compost-heap share below the 4–5.4% quoted. The vanilla
  totals (87/81/76/68/72, empty entries included) come from `misode/mcmeta` at
  the 1.20.1 tag, not from a jar on this server.
- **The village farm percentages assume the appended Farmer's Delight processor
  runs after the vanilla one and sees its output**, which is how
  `StructureTemplate.processBlockInfos` chains processors, and that
  `RuleProcessor` returns on the first matching rule. Both are vanilla
  semantics read from the call site in `VillageStructures`, not observed in a
  generated village. The raw per-rule probabilities are given above so the
  composition can be rechecked.
- **Loot Integrations' interaction with the 14 chest injections was not tested.**
  If it replaces a vanilla table wholesale the `forge:loot_table_id` condition
  still matches on ID, so the Farmer's Delight pool should still be added — but
  ordering against other chest-loot mods is not established here.
- **The knives tag was verified against three jars only** (Farmer's Delight,
  Dungeons Delight, Alex's Delight). The remaining 145 jars were not scanned for
  additions to `farmersdelight:tools/knives` or
  `farmersdelight:straw_harvesters`, so the 12-item figure is a floor, not a
  ceiling.
- `ReplaceItemModifier.doApply` removes matching stacks with
  `generatedLoot.forEach(... generatedLoot.remove(item))` — mutating the list it
  is iterating. With the single Pumpkin stack it is applied to this is
  harmless; behaviour if another mod injected a second Pumpkin stack into the
  same table was not established.
