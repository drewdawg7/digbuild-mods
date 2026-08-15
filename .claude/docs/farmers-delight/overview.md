<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Overview

**Farmer's Delight** is a cooking and farming expansion. It adds four crops and
their wild variants, a set of workstations that replace the crafting grid for
food (Cooking Pot, Cutting Board, Skillet, Stove), around seventy foods with
their own saturation and effect profile, two status effects that change how
eating works, and a spread of decorative and storage blocks built out of the
same materials. It adds no dimensions, no biomes and one entity — a thrown
rotten tomato.

Two things make it structural rather than cosmetic for this pack. It defines two
**custom recipe types**, `farmersdelight:cooking` and `farmersdelight:cutting`,
which other mods on this server register recipes into; and it injects new loot
pools into fourteen vanilla chest tables through Forge global loot modifiers, so
its items appear in ordinary world loot without any datapack work.

## Versions on this server

| Mod | ID | Version | Jar | Role |
|---|---|---|---|---|
| Farmer's Delight | `farmersdelight` | 1.20.1-1.3.2 | `FarmersDelight-1.20.1-1.3.2.jar` | the mod |
| Dungeon's Delight | `dungeonsdelight` | 1.3.0 | `forge-dungeonsdelight-1.20.1-1.3.0.jar` | add-on, **hard** dependency on this mod |
| Alex's Delight | `alexsdelight` | 1.5 | `alexsdelight-1.5.jar` | add-on, no declared dependency |
| RunicLib | `runiclib` | 4.3.11 | `forge-runiclib-1.20.1-4.3.11.jar` | Dungeon's Delight's required library |

Author: **vectorwing**. License: **MIT License**. Issue tracker:
<https://github.com/vectorwing/FarmersDelight/issues>. Credits line in
`mods.toml` names Chloe Dawn, Grimmauld, CDAGaming, TelepathicGrunt,
ConductiveFoam, simibubi, Jozufozu, bagel, Silk, SkySom, Eutro and RaymondBlaze.

## Dependency graph

From each jar's `META-INF/mods.toml`:

```
farmersdelight 1.20.1-1.3.2
├── forge         >= 47.1.0        (mandatory, BOTH)   ✓ 47.4.10 installed
├── minecraft     [1.20,1.20.1]    (mandatory, BOTH)   ✓ 1.20.1
└── crafttweaker  >= 14.0.6        (OPTIONAL, BOTH)    ✗ not installed

dungeonsdelight 1.3.0
├── forge           >= 47          (mandatory, BOTH)   ✓
├── minecraft       [1.20.1,1.21)  (mandatory, BOTH)   ✓
├── farmersdelight  >= 1.3.0       (mandatory, AFTER)  ✓ 1.3.2 installed
└── runiclib        >= 4.3.7       (mandatory, AFTER)  ✓ 4.3.11 installed

alexsdelight 1.5
├── forge      >= 47               (mandatory, BOTH)   ✓
└── minecraft  [1.20.1]            (mandatory, BOTH)   ✓
    (declares no hard dependency on farmersdelight or alexsmobs —
     both are present anyway)
```

All declared ranges are satisfied by what is installed. `farmersdelight`
declares `side = "BOTH"` on every dependency and ships client rendering,
recipe-book and overlay code, so it is required on the client as well as the
server. The only optional dependency, CraftTweaker, is **not** installed — the
three `.zs` scripts in `data/farmersdelight/scripts/` (`cooking_pot.zs`,
`cutting_board.zs`, `replacer_testing.zs`) are the mod's own test scripts and
never load here.

## Install state on this server

| | |
|---|---|
| Common config | `/config/farmersdelight-common.toml` — 20 options, all stock |
| Client config | `/config/farmersdelight-client.toml` — 3 options, all stock |
| Add-on config | `/config/dungeonsdelight-config.toml` — see [addons.md](addons.md) |
| Datapack overrides | none observed |

**Zero deviations from stock config.** All 23 options match the defaults in
`Configuration.java` exactly; see [config.md](config.md) for the full table and
the method.

Notable in the jar rather than the config:

- **One dead lang key.** `item.farmersdelight.earthworm` ("Earthworm") is
  translated in 43 of the jar's 45 language files, but no
  `earthworm` item is registered, and the string appears nowhere in the
  decompiled source, models or textures. It does not exist in-game.
- **`data/minecraft/advancements/` and `data/minecraft/recipes/` are empty
  directory entries** in the zip. The mod's recipes for vanilla results (Beetroot
  Soup and Mushroom Stew in the Cooking Pot, etc.) are written into the
  `farmersdelight` namespace instead, via the builder's `saveToFD` path.
- **Six of the eight cross-mod data namespaces in the jar are inert here.**
  `create`, `createaddition`, `origins`, `sereneseasons`, `silentgear` and
  `immersiveengineering` are not installed, so their tag files and the 29
  `forge:mod_loaded`-gated integration recipes never load. `tconstruct` and the
  `forge` common tags do apply. See the interaction table below.
- **`data/farmersdelight/weapon_attributes/skillet.json` is a Better Combat
  datapack file** (`{"parent": "bettercombat:mace"}`). Better Combat is not
  installed, so the Skillet uses its plain item attributes.

## Census

Counted by extracting the string literals from the `register("…")` calls in the
decompiled registry classes and **set-diffing** them against the
`assets/farmersdelight/lang/en_us.json` key set — not by counting files. The
diff is what makes the numbers trustworthy: the lang file has 139
`block.farmersdelight.*` keys against 132 registered blocks, and the seven
extras turn out to be UI strings (`block.farmersdelight.cutting_board.invalid_tool`,
`…skillet.underwater`, and five siblings), not missing registrations.

| | Count | Counted from |
|---|---:|---|
| Blocks | **132** | `BLOCKS.register("…")` literals in `common/registry/ModBlocks.java`. 133 `RegistryObject<Block>` fields, but `BASKET` is an alias assignment for `BAMBOO_BASKET`, not a registration. Set-diffs cleanly against the 132 non-UI `block.farmersdelight.*` lang keys — no strays either way. |
| Items | **185** | 184 `registerWithTab("…")` + 1 `registerHidden("…")` (`debug_pumpkin_pie`) in `ModItems.java`. 91 of the 185 are `BlockItem`s whose names come from `block.*` keys; the remaining 94 match the 94 real `item.farmersdelight.*` names exactly (97 keys, less two `skillet.*` UI strings and the dead `earthworm`). |
| — creative-tab items | 184 | the same, minus `debug_pumpkin_pie`, which is registered hidden |
| Status effects | **2** | `EFFECTS.register` in `ModEffects.java` — `nourishment`, `comfort`. The 4 `effect.farmersdelight.*` lang keys are two name/description pairs, not four effects. |
| Enchantments | **1** | `ModEnchantments.java` — `backstabbing`. Same 2-keys-per-entry pattern in lang. |
| Entity types | **1** | `ModEntityTypes.java` — `rotten_tomato` |
| Block entity types | **8** | `ModBlockEntityTypes.java` — stove, cooking_pot, basket, cutting_board, skillet, cabinet, canvas_sign, hanging_canvas_sign |
| Menu types | **1** | `ModMenuTypes.java` — `cooking_pot` |
| Recipe types | **2** | `RECIPE_TYPES.register` in `ModRecipeTypes.java` — `cooking`, `cutting`. Table below. |
| Recipe serializers | **4** | `ModRecipeSerializers.java` — `cooking`, `cutting`, `food_serving`, `dough`. The last two are `CustomRecipe` subclasses that live on the vanilla crafting type. |
| Loot function types | **3** | `ModLootFunctions.java` — `copy_meal`, `copy_skillet`, `smoker_cook` |
| Loot modifier types | **4** | `ModLootModifiers.java` — `add_item`, `replace_item`, `add_loot_table`, `pastry_slicing` |
| Particle types | **3** | `ModParticleTypes.java` — `star`, `steam`, `sparkle` |
| Sound events | **20** | `SOUNDS.register` in `ModSounds.java`; matches the 20 entries in `assets/farmersdelight/sounds.json` (17 have subtitles) |
| Damage types | **1** | `ModDamageTypes.java` `ResourceKey` + `data/farmersdelight/damage_type/stove_burn.json`; 2 `death.attack.*` lang keys |
| Creative tabs | **1** | `ModCreativeTabs.java` — `itemGroup.farmersdelight` |
| Custom advancement triggers | **1** | `ModAdvancements.java` — `CuttingBoardTrigger` |
| Worldgen features | **2** | `ModBiomeFeatures.java` — `wild_crop`, `wild_rice` |
| Biome modifier types | **1** | `ModBiomeModifiers.java` — `add_features_by_filter` |
| Placement modifier types | **1** | `ModPlacementModifiers.java` — `biome_tag` |
| Mixins | **14** | `farmersdelight.mixins.json` — 12 common, 2 client |

Data-driven content, counted from the `data/` tree by parsing each JSON's
top-level `type` rather than by filename:

| | Count | Notes |
|---|---:|---|
| Recipes (total) | **333** | `data/farmersdelight/recipes/**` |
| — `farmersdelight:cutting` | 106 | the Cutting Board |
| — `minecraft:crafting_shapeless` | 86 | |
| — `minecraft:crafting_shaped` | 51 | plus 3 more wrapped in `forge:conditional` |
| — `farmersdelight:cooking` | 28 | the Cooking Pot |
| — `minecraft:smelting` / `smoking` / `campfire_cooking` / `blasting` | 10 / 9 / 7 / 2 | |
| — `forge:conditional` | 3 | crate recipes gated on `farmersdelight:vanilla_crates_enabled` |
| — `farmersdelight:food_serving` | 1 | |
| — `farmersdelight:dough` | 1 | |
| — `minecraft:smithing_transform` | 1 | Netherite Knife |
| — integration recipes | 29 | 12 Create, 16 Immersive Engineering, 1 Silent Gear, each behind a `forge:mod_loaded` condition; **none of those three mods is installed**, so all 29 are inert |
| Advancements | **218** | 21 real advancements under `advancements/main/` (42 lang keys = 21 title/description pairs) plus 197 recipe-unlock advancements under `advancements/recipes/`, which carry no lang keys by design |
| Loot tables | **112** | 98 block, 14 chest (`fd_*`, one per injected vanilla chest) |
| Global loot modifiers | **37** | `loot_modifiers/` — 17 `add_item`, 14 `add_loot_table`, 5 `pastry_slicing`, 1 `replace_item`. All 37 are listed in `data/forge/loot_modifiers/global_loot_modifiers.json` with `"replace": false`. The 14 `add_loot_table` entries are the 14 `fd_*` chest tables. |
| Tags | **162** | across all namespaces: 38 `farmersdelight`, 80 `forge`, 28 `minecraft`, 9 `sereneseasons`, 4 `create`, 2 `createaddition`, 1 `origins`, 1 `tconstruct` |
| Worldgen JSONs | **19** | 10 configured features, 9 placed features (`patch_sandy_shrub` is configured-only) |
| Biome modifiers | **9** | `data/farmersdelight/forge/biome_modifier/` — the nine placed features that get injected |
| Structure NBTs | **5** | `structures/village/houses/{plains,desert,savanna,snowy,taiga}_compost_pile.nbt` |
| Damage type JSON | **1** | `stove_burn` |
| Weapon attributes | **1** | `skillet.json`, a Better Combat file; that mod is not installed |
| CraftTweaker scripts | **3** | shipped test scripts; CraftTweaker is not installed |
| `FoodProperties` constants | **73** | `common/FoodValues.java` — the nutrition/saturation source for [foods-and-effects.md](foods-and-effects.md) |

## Content pillars

| Pillar | One line | Covered in |
|---|---|---|
| Cooking stations | Stove, Cooking Pot, Skillet and Cutting Board, plus the Cooking Pot's own recipe book with three tabs | [cooking.md](cooking.md) |
| Crops and farming | Cabbage, Onion, Tomato and Rice, their seven wild variants, Rich Soil, Organic Compost and the rope-climbing tomato vine | [farming.md](farming.md) |
| Food and nutrition | 73 `FoodProperties` entries, the Nourishment and Comfort effects, and the overrides that push Nourishment onto vanilla soups | [foods-and-effects.md](foods-and-effects.md) |
| Storage and decoration | Six crop Crates plus Rice Bag, Rice Bale and Straw Bale, two Baskets, Cabinets in every wood, Canvas Signs in 17 colours (standing and hanging), Tatami, Safety Net, Rope | [blocks-items.md](blocks-items.md) |
| Tools | Flint/Iron/Golden/Diamond/Netherite Knives on a custom `FLINT` tier, the Skillet as a weapon-and-cooker, and the Backstabbing enchantment | [blocks-items.md](blocks-items.md) |
| Worldgen and loot | Nine wild-crop and mushroom-colony patches placed by biome tag, five village Compost Pile structures, and 37 global loot modifiers touching 14 vanilla chest tables | [loot-and-worldgen.md](loot-and-worldgen.md) |
| Progression | 21 advancements under `advancements/main/`, from first crop to full feast, plus the villager and wandering-trader trades | [progression.md](progression.md) |
| Configuration | 23 options across two files, all stock on this server | [config.md](config.md) |
| Add-ons | Dungeon's Delight and Alex's Delight, both of which register into the recipe types below | [addons.md](addons.md) |

## Custom recipe types

Two registered recipe types. Everything the mod's stations do, and everything
the add-ons add to them, is data-driven through these two schemas — which is why
a new food from another mod needs no code, only a JSON.

| Type ID | Station | Registered in | Recipes shipped | Serializer class |
|---|---|---|---|---|
| `farmersdelight:cooking` | Cooking Pot | `ModRecipeTypes.COOKING` | 28 | `CookingPotRecipe$Serializer` |
| `farmersdelight:cutting` | Cutting Board | `ModRecipeTypes.CUTTING` | 106 | `CuttingBoardRecipe$Serializer` |

Two further serializers exist without a recipe type of their own, because they
are `CustomRecipe` subclasses that sit on the vanilla crafting grid:

| Type ID | Behaviour | Recipes shipped |
|---|---|---|
| `farmersdelight:food_serving` | Grid recipe that transfers a meal from a filled container onto an empty bowl/plate, preserving the meal NBT | 1 |
| `farmersdelight:dough` | Grid recipe producing Wheat Dough from grain plus a water source, consuming the water container correctly | 1 |

### `farmersdelight:cooking` schema

Read out of `CookingPotRecipe$Serializer.fromJson`:

| Field | Required | Default | Meaning |
|---|---|---|---|
| `ingredients` | yes | — | Array of up to 6 ingredients |
| `result` | yes | — | Item stack produced |
| `container` | no | none | Item the meal must be served into (bowl, plate, bottle). Absent means the result item is self-contained. |
| `cookingtime` | no | `200` | Ticks. The mod's own three tiers are `FAST_COOKING = 100`, `NORMAL_COOKING = 200`, `SLOW_COOKING = 400` — 5, 10 and 20 seconds. |
| `experience` | no | `0.0` | XP granted on collecting the meal |
| `recipe_book_tab` | no | none | `meals`, `drinks` or `misc`; controls which tab of the Cooking Pot recipe book the entry appears under |
| `group` | no | `""` | Recipe-book grouping |

### `farmersdelight:cutting` schema

Read out of `CuttingBoardRecipe$Serializer.fromJson`:

| Field | Required | Default | Meaning |
|---|---|---|---|
| `ingredients` | yes | — | Array; the serializer throws if empty and throws if it holds more than one entry — a cutting recipe takes exactly one input |
| `tool` | yes | — | An ingredient, or a `farmersdelight:tool_action` ingredient naming a `ToolAction` (`pickaxe_dig`, `axe_strip`, …) so any modded tool with that action qualifies. All 106 shipped cutting recipes use the tool-action form. |
| `result` | yes | — | Array of at most 4 `ChanceResult`s; the serializer throws above 4 |
| `result[].chance` | no | `1.0` | Per-result probability. `cuttingBoardFortuneBonus` (default `0.1`) adds that much per level of Fortune on the tool. |
| `result[].count` | no | `1` | |
| `result[].nbt` | no | none | |
| `sound` | no | `""` | Sound event ID played on cutting |
| `group` | no | `""` | |

## Interaction with other mods on this server

| Mod | Interaction |
|---|---|
| **Dungeon's Delight** 1.3.0 | Hard dependency on this mod, loads `AFTER` it. Adds monster-derived foods through the same two recipe types. See [addons.md](addons.md). |
| **Alex's Delight** 1.5 | Bridges Alex's Mobs drops into Farmer's Delight cooking. Declares no dependency on either parent but needs both. See [addons.md](addons.md) and [alexs-mobs/addons.md](../alexs-mobs/addons.md). |
| **RunicLib** 4.3.11 | Pulled in only as Dungeon's Delight's required library. |
| **Tinkers' Construct** 3.11.2.166 | The one third-party namespace in the jar that is actually installed: `data/tconstruct/tags/items/seeds.json` adds this mod's seeds to Tinkers' seed tag. |
| **JEI** 15.20.0.112 | `integration/jei` in the jar registers both recipe types as JEI categories, plus the Cooking Pot's own recipe book. |
| **Forge common tags** | The mod both defines and populates a large slice of `forge:` food tags — `vegetables/*`, `crops/*`, `raw_*`/`cooked_*` meat and fish, `milk`, `dough`, `pasta`, `grain`, `bread`, `berries`, `eggs`, `seeds`, `tools/knives`. 80 tag files. Anything else on this server reading those tags sees Farmer's Delight's entries. |
| **Create, Create Crafts & Additions, Immersive Engineering, Silent Gear, Serene Seasons, Origins, EMI, CraftTweaker, Better Combat** | Shipped integration in the jar (recipes, tags, `data/*` files, `integration/emi`, `integration/crafttweaker`). **None of these is installed on this server**, so every one of those files is inert. |
| **Vanilla loot** | Independently of any mod, 37 global loot modifiers inject into vanilla chests, mob drops and block drops. Gated by `generateFDChestLoot` (on). See [loot-and-worldgen.md](loot-and-worldgen.md). |

## Reading the decompiled source

`FarmersDelight-1.20.1-1.3.2.jar` was decompiled with **jadx 1.5.4**, which
leaves SRG names in place — `GsonHelper.m_13851_` rather than
`GsonHelper.getAsString`, `ItemStack.f_41583_` rather than `ItemStack.EMPTY`.
Unlike the Alex's Mobs docs, no SRG mapping table was needed here: the clean
upstream source resolves everything directly.

The upstream repository is [`vectorwing/FarmersDelight`](https://github.com/vectorwing/FarmersDelight).
Branch **`1.20`** carries `mod_version=1.3.2`, `mc_version=1.20.1` in
`gradle.properties` — the exact version of the installed jar — so its files are a
line-for-line match for the decompiled ones and were used to read method and
field names throughout. `Configuration.java` on that branch was diffed against
the decompiled copy and is character-identical in every `define*` call.
