<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Crops, Soil and Wild Crops

Everything on this page is read from `FarmersDelight-1.20.1-1.3.2.jar` (decompiled with
[jadx 1.5.4](https://github.com/skylot/jadx), plus the jar's own `data/` tree) and from
`/config/farmersdelight-common.toml` on the live server. Registry IDs are the strings passed to
`BLOCKS.register("…")` / `ITEMS.register("…")` in `ModBlocks` / `ModItems`, not the Java field
names — the two differ for every crop (`CABBAGE_CROP` registers as `cabbages`, `TOMATO_CROP` as
`tomatoes`, `RICE_CROP_PANICLES` as `rice_panicles`).

jadx leaves SRG names in place, so anything that turned on an obfuscated vanilla constant
(`BiomeTags.f_207604_`, `MobEffects.f_19600_`) was resolved by diffing the decompiled method
against the same method in the clean upstream source
([`vectorwing/FarmersDelight`](https://github.com/vectorwing/FarmersDelight), branch `1.20`, which
carries `1.3.2`). Config defaults are the value passed to the `define`/`defineInRange` call in
`Configuration`, never a static field initialiser.

## Crops

Seven plantable crops, of which three (tomato, rice, mushroom colony) do not behave like vanilla
wheat.

| Crop | Block ID | Seed item | Stages | Where it grows | Harvest | Bone meal |
|---|---|---|---|---|---|---|
| Cabbage | `cabbages` | `cabbage_seeds` | 8 (age 0–7) | Farmland, light ≥ 9 | Break | Yes, vanilla rate |
| Onion | `onions` | `onion` (the vegetable itself) | 8 (age 0–7) | Farmland, light ≥ 9 | Break | Yes, vanilla rate |
| Budding Tomato Vine | `budding_tomatoes` | `tomato_seeds` | 4 (age 0–3), then becomes a Tomato Vine | Farmland, light ≥ 9 | Break (returns seeds only) | Yes, +1–4 stages |
| Tomato Vine | `tomatoes` | — (grown from the above) | 4 (vine age 0–3) | Farmland or on another vine, light ≥ 9 | **Right-click** at age 3 | Yes, +1–2 stages |
| Tomato Vine on Rope | `tomatoes_on_rope` | — | 4 (vine age 0–3) | Hanging under rope | **Right-click** at age 3 | Yes |
| Rice (lower) | `rice` | `rice` | 4 (age 0–3), then grows Rice Panicles above | Dirt-type block under a **full source block** of water | Break | Yes, +1–4 stages |
| Rice Panicles (upper) | `rice_panicles` | — | 4 (age 0–3) | On top of a mature Rice block, light ≥ 8 | Break | Yes, +0–1 stages |
| Brown/Red Mushroom Colony | `brown_mushroom_colony`, `red_mushroom_colony` | Mushroom placed on Rich Soil | 4 (age 0–3) | **Rich Soil only**, light < 13 | Right-click with shears or knife, or break | Yes, +1–2 stages |

### Cabbage and Onion

Plain `CropBlock` subclasses. Vanilla growth: a random tick with light level ≥ 9 advances a stage
with probability `1 / (floor(25 / growthSpeed) + 1)`, where `growthSpeed` is the vanilla farmland
bonus (hydrated farmland, row layout, etc.).

- Cabbage drops one Cabbage at age 7, plus a second pool of Cabbage Seeds with the vanilla
  binomial-with-bonus Fortune roll (`extra: 3`, `probability: 0.5714286`). Below age 7 it drops one
  Cabbage Seed and nothing else.
- Onion has no separate seed item — it is planted from the Onion. It always drops one Onion, and at
  age 7 rolls a second Onion pool with the same binomial Fortune formula. Rabbits treat anything in
  `forge:crops/cabbage` as food (`RabbitsEatCabbageMixin`).
- Cutting a Cabbage on a Cutting Board yields 2 Cabbage Leaves; cutting a Wild Cabbage yields 1
  Cabbage Seed and, at 50%, 2 Yellow Dye.

### Tomatoes and the rope climb

This is the crop that behaves least like vanilla, and Farmer's Delight does **not** add a trellis
in this version — there is no trellis block, item or recipe anywhere in the jar. The vertical
support is Rope.

Planting Tomato Seeds gives a **Budding Tomato Vine** (`budding_tomatoes`, age 0–4 with max age 3).
On reaching max age it replaces itself with a **Tomato Vine** (`tomatoes`). The Tomato Vine:

- Grows a stage on a random tick at light ≥ 9 with a flat **1-in-6** chance. The formula in
  `TomatoBlock` is `random.nextInt((int)(25.0f / 5.0f) + 1) == 0` — the growth speed is hard-coded
  to 5, so farmland hydration and row layout do **not** speed a tomato vine up.
- At vine age 3, **right-clicking** it drops 1–2 Tomatoes plus a 5% chance of a Rotten Tomato, and
  resets the vine to age 0. Breaking it instead drops 1–2 Tomatoes (Fortune: uniform bonus,
  multiplier 1), one Tomato Seed if it is not ropelogged, and the same 5% Rotten Tomato.
- After each growth tick it calls `climbRopeAbove`: if the block above is rope, and the vine column
  is fewer than 3 blocks tall, a **Tomato Vine on Rope** is placed into that rope block. Stacks are
  capped at 3 vines.
- Bone-mealing a vine adds 1–2 stages (`CropBlock`'s 2–4 halved), with a 30% chance of also
  triggering a rope climb. Bone-mealing a Budding Tomato Vine adds 1–4 stages and overflows
  straight into a Tomato Vine at the leftover age.
- Breaking a ropelogged vine puts the rope back. Which rope is controlled by
  `defaultTomatoVineRope` (`farmersdelight:rope` here); `enableTomatoVineClimbingTaggedRopes` (true
  here) lets the vine climb anything in `farmersdelight:ropes`, which on this server means
  Farmer's Delight rope only — Quark and Supplementaries are both absent, and their entries in that
  tag are `required: false`.
- Tomato Seeds are crafted from one Tomato **or** one Rotten Tomato.

### Rice

Two blocks. The lower `rice` block is a `BushBlock`, not a `CropBlock`, and needs a **full-height
water source block at its own position** — placing it anywhere else is refused with the in-game
message "This seed must be planted in shallow water." It plants on any block in `minecraft:dirt`.

- Growth checks the light level **of the block above** (≥ 6), and uses a flat 1-in-3 chance per
  random tick (`25 / 10`, again hard-coded). At age 3 it grows `rice_panicles` into the air block
  above instead of advancing further.
- Rice Panicles are an ordinary `CropBlock` (light ≥ 8) whose bone-meal increase is divided by 3,
  so a bone meal is worth 0 or 1 stage.
- The lower block always drops one Rice. The panicles drop **Rice** if broken at age 3 with an item
  in `farmersdelight:tools/knives`, and a **Rice Panicle** if broken at age 3 with anything else.
  Below age 3 they drop nothing. Cutting mature panicles with a knife also adds one Straw through
  the `straw_from_mature_rice` global loot modifier.

### Mushroom colonies

Brown and Red Mushroom Colony are the only blocks in `farmersdelight:mushroom_colony_growable_on`'s
world: that tag contains **only `farmersdelight:rich_soil`**. A mushroom placed on Rich Soil is
converted to a colony by the Rich Soil block itself (see below); once it exists it advances one age
per random tick with a 1-in-4 chance, but only while the block underneath is still Rich Soil.

- Shears: right-click removes one mushroom and drops one age.
- Knife: right-click harvests all of them at once (count = current age) and resets to age 0.
- Breaking: 2/3/4/5 mushrooms at age 0/1/2/3. At age 3 with shears you get the colony block itself
  instead, which is the only way to pick one up.
- It survives at light < 13, or on any block in the vanilla mushroom-grow-block tag at any light.

## Soil and fertiliser

### Organic Compost

`organic_compost`, a block with a `composting` state 0–7. It is **crafted**, in two shapeless
recipes that both yield one block:

| Recipe | Ingredients |
|---|---|
| From rotten flesh | 1 Dirt + 2 Rotten Flesh + 2 Straw + 4 Bone Meal |
| From tree bark | 1 Dirt + 4 Tree Bark + 2 Straw + 2 Bone Meal |

Placed down, it random-ticks toward Rich Soil. On each random tick the block computes one
probability and rolls it once:

```
chance = 0.02 × (blocks tagged farmersdelight:compost_activators in the 3×3×3 around it)
       + (0.10 if any position in that 3×3×3 has sky light > 12 above it, else 0.05)
       + (0.10 if any water is in that 3×3×3)
```

On success it advances one `composting` stage; from stage 7 it becomes **Rich Soil**. Eight
successful rolls therefore convert one block.

`farmersdelight:compost_activators` is Brown Mushroom, Red Mushroom, Podzol, Mycelium, Organic
Compost, Rich Soil, Rich Soil Farmland and any mushroom colony. The block counts itself (it is in
the tag), so the floor is 0.02. The 3×3×3 is 27 positions, giving a ceiling of
`0.54 + 0.10 + 0.10 = 0.74` per random tick — a fully packed, sunlit, watered stack. A bare block
in a dark room with no neighbours sits at `0.02 + 0.05 = 0.07`.

A comparator reads `8 − composting`, so a comparator on a fresh pile outputs 8 and on a
nearly-finished one outputs 1.

### Rich Soil

`rich_soil`. Not craftable and not obtainable from any recipe — the only source is Organic Compost
finishing, plus the village Compost Heap structures below. It is a `Block` with `randomTicks()`
enabled, and on each random tick it does exactly one of two things:

1. **Mushroom conversion.** If the block above is a Brown or Red Mushroom, it is replaced with the
   matching Mushroom Colony. This is unconditional — no probability roll — and it returns early, so
   no growth boost happens that tick.
2. **Growth boost.** Otherwise, with probability `richSoilBoostChance` (**0.2** on this server,
   which is also the stock default), it applies a full bone-meal tick to the plant above — the same
   `performBonemeal` call a bone meal makes, including the green particle effect (event 2005). If
   the plant above is in `farmersdelight:planted_from_below` (cave vines) it looks *below* instead.

The boost is skipped entirely for anything in `farmersdelight:unaffected_by_rich_soil`: Grass
Block, Moss Block, both nyliums, Grass, Fern, Twisting Vines, Big Dripleaf, Pink Petals, Sandy
Shrub, both mushroom colonies, every wild crop, and `#minecraft:tall_flowers`. Plants that are not
`BonemealableBlock` are unaffected by construction.

**Rich Soil does not revert.** There is no code path anywhere in the jar that turns `rich_soil`
back into dirt, and two mixins actively protect it: `KeepRichSoilTreeMixin` cancels the
`setDirtAt` call that tree trunk placers make, so growing a tree on Rich Soil leaves the Rich Soil
intact. `KeepRichSoilGiantTreeMixin` makes `Feature.isGrassOrDirt` return false for it, which is
the check 2×2 giant trees use to validate their base.

Rich Soil can sustain any plant type **except** `CROP`, `NETHER` and `WATER` — for crops you till
it.

### Rich Soil Farmland

`rich_soil_farmland`, produced by using a hoe on Rich Soil with air above. It is a `FarmBlock`
subclass and differs from vanilla farmland in four ways:

- **Never trampled.** `KeepRichSoilUntrampledMixin` cancels `FarmBlock.turnToDirt` for it, and the
  block's own `fallOn` just applies normal fall damage. Jumping on it is free.
- **Reverts to Rich Soil, not dirt**, when it loses its crop support (`turnToRichSoil`). Placing
  the block where farmland cannot survive also gives Rich Soil.
- **Boosts the same way.** Its random tick first handles moisture (hydrated from water within a
  4-block radius or from rain, drying one level at a time otherwise); only at **moisture 7** does
  it call the same 20% `tryBoostingPlantsAboveAndBelow`. Partly-dried Rich Soil Farmland gives no
  boost at all.
- **Counts as fertile** at any moisture above 0, and supports melon/pumpkin stems even when the
  usual farmland survival check fails.

`VillagersTargetRichSoilMixin` teaches Farmer villagers to recognise any `FarmBlock` as their
secondary point of interest, so they will work a Rich Soil Farmland field.

## Farming tools and blocks

### Knives

Five knives, all `KnifeItem extends DiggerItem` mining the `farmersdelight:mineable/knife` tag,
all registered with attack-damage modifier `+0.5` and attack-speed modifier `−2.0`.

| Knife | Tier | Durability | Attack damage | Attack speed |
|---|---|---|---|---|
| Flint Knife | `ModMaterials.FLINT` (custom) | 131 | 2.5 | 2.0 |
| Golden Knife | vanilla Gold | 32 | 1.5 | 2.0 |
| Iron Knife | vanilla Iron | 250 | 3.5 | 2.0 |
| Diamond Knife | vanilla Diamond | 1561 | 4.5 | 2.0 |
| Netherite Knife | vanilla Netherite | 2031 | 5.5 | 2.0 |

The custom Flint tier is: 131 uses, mining speed 4.0, attack-damage bonus 1.0, harvest level 1,
enchantability 5, repaired with Flint. Attack damage in the table is the displayed value
(1.0 base + 0.5 + the tier bonus); attack speed is `4.0 − 2.0`. The Netherite Knife is
fire-resistant. Knives also reduce their own knockback by 0.1 on hit.

At an enchanting table a knife accepts Sharpness, Smite, Bane of Arthropods, Knockback, Fire Aspect
and Looting; Fortune is explicitly denied; anything else falls through to the enchantment's own
category check.

Farming-relevant knife behaviour:

- **Straw.** Four global loot modifiers gated on `farmersdelight:straw_harvesters` (which contains
  exactly `#farmersdelight:tools/knives`): Grass 20%, Tall Grass 20%, Sandy Shrub 30%, mature Wheat
  100%, mature Rice Panicles 100%.
- **Mushroom colonies** — clears the whole colony in one right-click (above).
- **Cutting Board** recipes accept the `knife_dig` tool action or `#forge:tools/knives`.

### Rope

`rope`, an `IronBarsBlock` subclass, 4 per 2 Straw stacked vertically (or 4 from one Safety Net).
Straw comes from a Straw Bale (9 per bale) or from knife-harvesting grass and grain.

- It is the tomato vine's vertical support (above).
- **Reeling** (`enableRopeReeling`, true here): sneak + right-click with an empty hand removes the
  **bottom** rope of the column and gives it to you, so a hanging line can be shortened from the
  top. Without the config, or without sneaking, right-clicking a rope column instead searches up to
  24 blocks upward for a Bell and rings it.
- Rope has no collision box but does have a 2×1×2-pixel support shape at its base, and does not
  block mob pathing.
- Rope Fence and Rope Fence Gate are separate blocks, tagged into `forge:fences` and
  `forge:fence_gates`.

### Sandy Shrub

`sandy_shrub` — a shearable bush that only survives on `minecraft:sand`. Breaking it gives Beetroot
Seeds at 12.5% (Fortune: uniform bonus, multiplier 2), or the shrub itself with shears, or Straw at
30% with a knife. **Bone-mealing it re-runs the `patch_sandy_shrub` feature** at the block above,
spreading a fresh patch of shrubs — it is the only renewable source of the block.

### Soil variants — what does not exist

There is no "sandy soil" or "organic soil" block in 1.3.2. The complete soil set the mod adds is
`organic_compost`, `rich_soil` and `rich_soil_farmland`. `farmersdelight:terrain` is a block tag
(`#minecraft:dirt` + `#minecraft:sand`) used by worldgen, not a block.

## Wild crops and worldgen

### The 19 files

`data/farmersdelight/worldgen/` holds 10 configured features and 9 placed features. The mismatch is
`patch_sandy_shrub`: it has a configured feature but **no** placed feature and no biome modifier,
because it is only ever invoked as the companion plant inside the cabbage and beet patches, or by
bone-mealing an existing shrub.

Each wild-crop patch places a primary plant and a companion, both only where the block directly
below matches, 64 tries in a 13×7×13 box (rice: 96 tries in a 15×7×15 box). Wild Carrots
additionally lay Coarse Dirt under themselves.

| Feature | Plants | Companion | Needs below | Attempts per chunk |
|---|---|---|---|---|
| `patch_wild_cabbages` | Wild Cabbage | Sandy Shrub | Sand | 1 chunk in 30 |
| `patch_wild_beetroots` | Sea Beet | Sandy Shrub | Sand | 1 chunk in 30 |
| `patch_wild_carrots` | Wild Carrot | Grass (+ Coarse Dirt floor) | Dirt | 1 chunk in 120 |
| `patch_wild_onions` | Wild Onion | Allium | Dirt | 1 chunk in 120 |
| `patch_wild_potatoes` | Wild Potato | Fern | Dirt | 1 chunk in 100 |
| `patch_wild_tomatoes` | Tomato Shrub | Dead Bush | Dirt or sand | 1 chunk in 100 |
| `patch_wild_rice` | Wild Rice | — | Dirt, in a full water source | 1 chunk in 20 |
| `patch_brown_mushroom_colony` | Brown Mushroom Colony (random age 0–3) | Brown Mushroom | Mycelium | 1 chunk in 15 |
| `patch_red_mushroom_colony` | Red Mushroom Colony (random age 0–3) | Red Mushroom | Mycelium | 1 chunk in 15 |

Every placed feature also carries a `farmersdelight:biome_tag` filter for `minecraft:is_overworld`
and a heightmap placement at the world surface, so a rule that fires in a biome outside that tag
produces nothing, and features are only ever placed on the surface column.

### Which biome each rule targets

Placement is decided by nine `AddFeaturesByFilterBiomeModifier` entries registered in code
(`ModBiomeModifiers`), each with an allowed biome **tag**, an optional denied set and an optional
base-temperature window. Nothing is hard-coded to a biome ID except two denials.

| Wild crop | Allowed | Denied | Temperature |
|---|---|---|---|
| Wild Cabbage, Sea Beet | `minecraft:is_beach` | — | — |
| Wild Carrot, Wild Onion | `minecraft:is_overworld` | Lush Caves, Mushroom Fields | 0.4 – 0.9 |
| Wild Potato | `minecraft:is_overworld` | `forge:is_underground` | 0.1 – 0.3 |
| Tomato Shrub | `forge:is_hot/overworld` | `forge:is_wet` | — |
| Wild Rice | `forge:is_wet/overworld` | `forge:is_underground` | — |
| Mushroom colonies | `forge:is_mushroom` | — | — |

Because the targets are tags rather than biome IDs, they pick up modded biomes automatically **iff
the mod that added them contributes to those tags**. That is the opposite of the failure mode the
Alex's Mobs spawn configs have, where biome IDs are named literally.

### What that means on this server

Six mods on digbuild touch overworld biomes. Every relevant biome tag in every mod jar was read
directly out of the jars pulled from the live `/mods`:

| Mod | Biomes added | In `is_overworld`? | Effect on wild crops |
|---|---|---|---|
| **Terralith 2.5.4** | 99 (35 vanilla biomes also overridden) | Yes — the whole `#terralith:all_terralith_biomes` tag | **Fully covered.** Terralith also contributes to `forge:is_hot/overworld` (36 biomes), `forge:is_wet/overworld` (19), `forge:is_underground` (14), `forge:is_mushroom` (Mirage Isles, Fungal Caves) and `minecraft:is_beach` (Gravel Beach). |
| **Darker Depths** | 3 cave biomes | Yes, and all 3 are in `forge:is_underground` | Rules fire but are inert in practice (see below). |
| **Yung's Cave Biomes** | 2 cave biomes | Yes, via `#yungscavebiomes:cave_biomes`, also in `forge:is_underground` | Same — inert in practice. |
| **Alex's Caves** | 6 cave biomes | **No** | No wild crops. The mod contributes to `forge:is_magical`, `is_spooky`, `is_wasteland` and `is_sparse/overworld`, none of which Farmer's Delight reads. Every one of the nine rules is inert here. |
| **Aquamirae** | none — it only overrides `minecraft:deep_frozen_ocean` | n/a | No change. |
| **TerraBlender** | one placeholder biome | n/a | No change. |

The cave-biome case deserves the caveat: Darker Depths' three caverns (base temperature 0.5) fall
inside the 0.4–0.9 window and are in `minecraft:is_overworld`, so the Wild Carrot and Wild Onion
modifiers do attach their features to those biomes. Both placed features still run at the
`MOTION_BLOCKING` heightmap — the world surface — and then pass through a `minecraft:biome` filter
that re-checks the biome at the final position. At the surface that resolves to the surface biome,
not the cave biome, so the feature is discarded. The same reasoning covers Yung's Frosted Caves
(temperature 0) and Lost Caves (2.0), which fall outside the window anyway. **No wild crop
generates inside any cave biome on this server.**

Terralith biomes that satisfy the two temperature-gated rules, computed from the `temperature`
field of each of the 99 Terralith biome JSONs:

- **Wild Carrot / Wild Onion (0.4–0.9), surface only:** 32 biomes, including Alpine Highlands,
  Blooming Valley, Highlands, Lavender Forest, Moonlight Grove, Sakura Grove, Shield, Steppe,
  Stony Spires, Temperate Highlands, Warm River and the four Skylands variants. The five Terralith
  cave biomes also inside the window are excluded in practice for the reason above.
- **Wild Potato (0.1–0.3), non-underground:** 19 biomes, including Birch Taiga, Cloud Forest, Cold
  Shrubland, Emerald Peaks, Gravel Desert, Ice Marsh, Rocky Mountains, Scarlet Mountains, Siberian
  Taiga, Snowy Cherry Grove, Snowy Maple Forest, Windswept Spires, Yellowstone and Yosemite
  Lowlands.

Terralith's 35 vanilla-biome overrides keep vanilla temperatures unchanged (Plains 0.8, Forest 0.7,
Taiga 0.25, Swamp 0.8, Jungle 0.95, and so on), so every vanilla placement still behaves exactly as
in an unmodded world. Mushroom colonies are the narrowest rule on the server: `forge:is_mushroom`
resolves to vanilla Mushroom Fields plus Terralith's Mirage Isles and Fungal Caves — and Fungal
Caves is underground, so in practice it is the two surface biomes.

**Not verified:** no wild-crop patch was confirmed by generating or inspecting a chunk of the live
world. Everything above is what the data and code say should happen.

## The five structure files

`data/farmersdelight/structures/village/houses/` holds five NBT templates —
`plains_compost_pile`, `snowy_compost_pile`, `savanna_compost_pile`, `desert_compost_pile`,
`taiga_compost_pile`. They are the "Compost Heap": a small lot containing Organic Compost blocks,
which will finish composting into Rich Soil after the village generates.

They are not registered as structures. `VillageStructures.addNewVillageBuilding` runs on
`ServerAboutToStartEvent` and injects each template into the matching vanilla village house pool
with a fixed weight:

| Pool | Template | Weight |
|---|---|---|
| `minecraft:village/plains/houses` | `plains_compost_pile` | 5 |
| `minecraft:village/savanna/houses` | `savanna_compost_pile` | 4 |
| `minecraft:village/taiga/houses` | `taiga_compost_pile` | 4 |
| `minecraft:village/snowy/houses` | `snowy_compost_pile` | 3 |
| `minecraft:village/desert/houses` | `desert_compost_pile` | 3 |

The same method, under a separate config flag, adds rule processors to the five vanilla village
farm processor lists so that Farmer's Delight crops replace some vanilla ones:

| Farm | Replacements |
|---|---|
| `farm_plains`, `farm_taiga` | 30% of Wheat → Cabbage, 30% → Tomato, 30% → Onion (applied in order) |
| `farm_snowy` | 30% of Wheat → Cabbage, 30% → Onion; 20% of Beetroot → Cabbage, 20% → Onion |
| `farm_savanna`, `farm_desert` | 30% of Wheat → Cabbage, 30% → Tomato |

Weights are added on top of the vanilla pool, so they raise the chance of a compost lot without
removing any vanilla building.

## Config gates

`/config/farmersdelight-common.toml`. **Every option on the live server is byte-identical to the
mod default**, verified by parsing each `define*` call out of `Configuration` and comparing the
value passed there against the file — not by eye. The options that touch crops, soil or worldgen:

| Option | Section | This server | Stock default | What it gates |
|---|---|---|---|---|
| `richSoilBoostChance` | `farming` | `0.2` | `0.2` | Probability that a Rich Soil / Rich Soil Farmland random tick bone-meals the plant on it. `0.0` disables the boost entirely; Rich Soil still converts mushrooms. |
| `enableTomatoVineClimbingTaggedRopes` | `farming` | `true` | `true` | Tomato vines climb anything in `farmersdelight:ropes` rather than only `farmersdelight:rope`. |
| `defaultTomatoVineRope` | `farming` | `farmersdelight:rope` | `farmersdelight:rope` | Which rope a broken ropelogged vine leaves behind. |
| `enableTomatoRopePermanence` | `debug` | `true` | `true` | A ropelogged vine force-places its rope back when removed, including by `/setblock`. |
| `generateFDChestLoot` | `world` | `true` | `true` | Adds Farmer's Delight pools (ropes, crops, tools) to 14 vanilla chest tables — village houses (plains/desert/savanna/snowy/taiga), village butcher, simple dungeon, abandoned mineshaft, shipwreck supply, pillager outpost, ruined portal, both bastion tables and End City treasure. |
| `generateVillageCompostHeaps` | `world` | `true` | `true` | Injects the five Compost Heap templates above. |
| `generateFDCropsOnVillageFarms` | `world` | `true` | `true` | Injects the five farm-plot rule processors above. |
| `enableRopeReeling` | `settings` | `true` | `true` | Sneak-use with an empty hand reels rope from the bottom. Disabling it restores bell-ringing on that interaction. |
| `enableFarmerFDTrades` | `settings` | `true` | `true` | Novice/Apprentice Farmers buy this mod's crops. |
| `enableWanderingTraderFDTrades` | `settings` | `true` | `true` | Wandering Trader sells this mod's seeds and plantables. |
| `cuttingBoardFortuneBonus` | `crafting` | `0.1` | `0.1` | Per-level Fortune bonus to rare Cutting Board results — this is how Fortune reaches wild-crop cutting recipes. |

There is no config option that disables individual wild crops, changes their rarity, or changes the
biomes they use. Doing any of that requires a datapack overriding
`data/farmersdelight/worldgen/placed_feature/*.json` or the biome modifiers. **The server has no
datapacks installed** (`/world/datapacks` is empty), and no other jar in `/mods` ships a
`data/farmersdelight/worldgen/` or `data/farmersdelight/tags/worldgen/` file, so all nine rules run
exactly as shipped.

## Composting

`CommonSetup.registerCompostables` adds 38 entries to the vanilla composter, all at
`FMLCommonSetupEvent`. The value is the per-item chance of raising the composter one level.

| Chance | Items |
|---|---|
| 30% | Tree Bark, Straw, Cabbage Seeds, Tomato Seeds, Rice, Rice Panicle, Sandy Shrub |
| 50% | Pumpkin Slice, Cabbage Leaf, Kelp Roll Slice |
| 65% | Cabbage, Onion, Tomato, Wild Cabbage, Wild Onion, Tomato Shrub, Wild Carrot, Wild Potato, Sea Beet, Wild Rice, Pie Crust |
| 85% | Rice Bale, Sweet Berry Cookie, Honey Cookie, Cake Slice, Apple Pie Slice, Sweet Berry Cheesecake Slice, Chocolate Pie Slice, Raw Pasta, Rotten Tomato, Kelp Roll |
| 100% | Apple Pie, Sweet Berry Cheesecake, Chocolate Pie, Dumplings, Stuffed Pumpkin, Brown Mushroom Colony, Red Mushroom Colony |

This is the vanilla composter, which produces Bone Meal — it is unrelated to Organic Compost, which
is crafted and never enters a composter.

The same setup method also feeds animals: Chickens and Parrots accept Cabbage Seeds, Tomato Seeds
and Rice; Pigs accept Cabbage and Tomato; Cats accept Cod Slice and Salmon Slice. Villagers pick up
Cabbage, Tomato, Onion, Rice, both seeds and Rice Panicle, and count Cabbage/Tomato/Onion as 1 food
point each and Rice as 2.
