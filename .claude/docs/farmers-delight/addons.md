<!-- Generated from forge-dungeonsdelight-1.20.1-1.3.0.jar + alexsdelight-1.5.jar + FarmersDelight-1.20.1-1.3.2.jar + a content scan of all 148 jars in the live /mods + live server config. Provenance: ../README.md -->

# Farmer's Delight — Add-ons & Dependencies

Two Farmer's Delight add-ons are installed on this server: **Dungeon's Delight**
(monster cooking) and **Alex's Delight** (Alex's Mobs cooking). Neither replaces
a single file of Farmer's Delight data — every hook is either an additive tag,
a new recipe in the add-on's own namespace, or a global loot modifier. The
behaviour changes are real all the same, and they are catalogued below.

Alex's Delight is documented from the Alex's Mobs side in
[../alexs-mobs/addons.md](../alexs-mobs/addons.md); this page covers it from the
Farmer's Delight side — what it adds to the cooking chain — and does not repeat
the Alex's Mobs loot-table analysis.

Seven further jars on the server carry Farmer's Delight content or references
without being add-ons. They are in
[Other mods that touch Farmer's Delight](#other-mods-on-this-server-that-touch-farmers-delight),
along with three defects found there.

> **Read [How Farmer's Delight decides something is a tool](#how-farmers-delight-decides-something-is-a-tool)
> before concluding that any tool is excluded from anything.** Farmer's Delight
> accepts a Forge `ToolAction` as an alternative to tag membership almost
> everywhere, so an add-on tool missing from `forge:tools/knives` is usually
> still fully functional. Comparing tag membership alone gives the wrong answer.

## The parent mod

**Farmer's Delight** (`farmersdelight` 1.20.1-1.3.2) by **vectorwing**, license
**MIT**. Credits list Chloe Dawn, Grimmauld, CDAGaming, TelepathicGrunt,
ConductiveFoam, simibubi, Jozufozu, bagel, Silk, SkySom, Eutro and RaymondBlaze.
Source and issue tracker: <https://github.com/vectorwing/FarmersDelight>;
project pages <https://www.curseforge.com/minecraft/mc-mods/farmers-delight> and
<https://modrinth.com/mod/farmers-delight>. 1.3.2 (2026-05-13) is the current
1.20.1 build — the server is up to date.

| Declared | Range | Server has | In range |
|---|---|---|---|
| `forge` | `[47.1.0,)` | 47.4.10 | yes |
| `minecraft` | `[1.20,1.20.1]` | 1.20.1 | yes |
| `crafttweaker` (optional) | `[14.0.6,)` | not installed | n/a |

### How Farmer's Delight decides something is a tool

This matters for every add-on below, and the answer is **never a tag alone**.
Farmer's Delight consistently accepts a Forge **`ToolAction`** as an alternative
to tag membership, in both its code and its recipe data.

**In code**, `ItemUtils.isValidTool(stack, action, fallbackTag)` returns
`stack.canPerformAction(action) || stack.is(fallbackTag)`. `isKnife()` calls it
with `KnifeItem.KNIFE_HARVEST` and `farmersdelight:tools/knives`, and that gates
knife scavenging, pastry and cake slicing, straw harvesting and rice harvesting.

**In recipe data**, a cutting recipe's `tool` field is a **JSON array**, which
`Ingredient.fromJson` deserialises as a compound ingredient matching **any**
entry — not all of them. Every one of Farmer's Delight's 106 cutting-board
recipes but one is written as an action/tag pair:

```json
"tool": [
  { "type": "farmersdelight:tool_action", "action": "knife_dig" },
  { "tag": "forge:tools/knives" }
]
```

The same pattern covers the non-knife recipes — `axe_dig` paired with
`#minecraft:axes`, `axe_strip`, and so on. So **the general rule is that any
item performing the right `ToolAction` works in Farmer's Delight's cutting
recipes whether or not it joins the tag**, and any modded axe that performs
`axe_dig` works on the wood recipes for free. The single exception is
`recipes/integration/silentgear/cutting/netherwood.json`, which supplies a bare
`axe_strip` action and no tag at all — the reverse case, and Silent Gear is not
installed.

Farmer's Delight's own five knives are in both `farmersdelight:tools/knives` and
`forge:tools/knives`, and `KnifeItem.canPerformAction` returns true for
`knife_dig`, so they satisfy every branch.

The consequence for add-ons: **an add-on tool that subclasses `KnifeItem`
inherits the ToolAction and therefore works everywhere in Farmer's Delight,
tag membership or not.** Only third-party recipes that write `tool` as a bare
tag object, with no action alternative, can exclude it — see
[Tag-only checks and what they actually cost](#tag-only-checks-and-what-they-actually-cost).

The live `/config/farmersdelight-common.toml` is at stock defaults throughout.

## Dungeon's Delight (`dungeonsdelight` 1.3.0)

File `forge-dungeonsdelight-1.20.1-1.3.0.jar`. By **Yirmiri** (owner and
programmer) and **Betwixer** (artist), of the **Azurune** group — the two names
`mods.toml` gives as `authors="Yirmiri & Betwixer"`, with those roles confirmed
on the Modrinth team page. Description: *"Dungeon's Delight is a cooking and
farming mod in which you turn monsters into delicious delicacies."* 1,490 files
in the jar.

- CurseForge: <https://www.curseforge.com/minecraft/mc-mods/dungeons-delight>
- Modrinth: <https://modrinth.com/mod/dungeons_delight> (underscore in the slug)
- Source: <https://github.com/Yirmiri/Dungeons-Delight>

License is the **AZURUNE License**, the string `mods.toml` carries and Modrinth
records as `LicenseRef-AZURUNE-License`; CurseForge shows only "Custom License".
It is published at
<https://github.com/Yirmiri/Yirmiri/blob/main/AZURUNE-LICENSE.md> and is a
custom all-rights-reserved license (v1.0.2, © Azurune 2025), not an OSI one.
Relevant terms for a private server: use as a dependency and inclusion in a
modpack are both permitted **only if the jar was obtained from Modrinth or
CurseForge**, and the pack must comply with the Minecraft EULA.
**Redistribution is not permitted** — which matters here, because the sibling
`digbuild` repo mirrors `mods/` and publishes it as a GitHub Release. Addons may
use and modify the code and assets; modification of the mod itself is allowed
only to contribute upstream or for private use.

1.3.0 (2026-05-26) is the **newest** 1.20.1 Forge build on both platforms as of
today, not necessarily the terminal one — the project is not marked
end-of-support for 1.20.1 and also targets 1.21/1.21.1. The 1.20.1 Forge line
runs 1.0.0 → 1.2.10 → 1.3.0.

The largest add-on on the server by content: it adds a **second cooking pot**
with its own recipe type, 53 blocks, 134 items, 10 status effects, 3
enchantments, 6 entities, a structure and a crop, and it wires all of it into
Farmer's Delight's cutting board, heat sources, cabinets, meal/feast/drink tags
and knife-scavenging system.

### Declared dependencies vs. what this server runs

| Declared | Range | Server has | In range |
|---|---|---|---|
| `forge` | `[47,)` | 47.4.10 | yes |
| `minecraft` | `[1.20.1,1.21)` | 1.20.1 | yes |
| `farmersdelight` | `[1.3.0,)`, ordering `AFTER` | 1.20.1-1.3.2 | yes |
| `runiclib` | `[4.3.7,)`, ordering `AFTER` | 1.20.1-4.3.11 | yes |

All four are satisfied. Unlike Alex's Delight, this add-on declares its parent
correctly, and it declares `ordering="AFTER"` so its datapack entries load after
Farmer's Delight's.

RunicLib (`runiclib` 1.20.1-4.3.11, by **Yirmiri** with effect icons by
**BackupCup**, same AZURUNE License, <https://modrinth.com/mod/runiclib>) is a
hard dependency and not optional flavour: Dungeon's Delight
blocks extend `net.azurune.runiclib.common.publicized.*`, its effects extend
RunicLib's `PublicMobEffect`, its mod-loaded checks go through
`runiclib.core.platform.Services`, and several of its foods grant RunicLib's own
`perception` and `pyromaniac` effects. It is a MultiLoader library of registry
helpers, conditional recipes, attributes and premade status effects, formerly
published as *TipsyLib*. 4.3.11 is the newest 1.20.1 Forge build, so the
`[4.3.7,)` range is satisfied with room to spare.

### Blocks (53)

| Group | Blocks |
|---|---|
| Cooking stations | `monster_pot`, `dungeon_stove` |
| Feasts & pastries | `monster_cake`, `candle_monster_cake`, `spider_pie`, `sculk_tart`, `spider_donut`, `ossobuco_block`, `guardian_angel_block`, `silverfish_and_chips_block`, `glow_berry_gelatin_block`, `sculk_mayo_block` |
| Crops & plants | `rotbulb_crop`, `rotbulb_plant`, `rotten_crop`, `rotten_potatoes`, `rotten_tomatoes`, `wormouth`, `wormroot_tendrils`, `wormroot_stalk`, `wormroots_block` |
| Storage crates | `rotbulb_crate`, `poisonous_potato_crate`, `rotten_tomato_crate` |
| Stained scrap | `stained_scrap_block`, `cut_stained_scrap`, `cut_stained_scrap_stairs`, `cut_stained_scrap_slab`, `stained_scrap_bars`, `stained_scrap_grate`, `stained_lantern` |
| Living light | `living_fire`, `living_candle`, `living_campfire`, `living_lantern`, `living_torch`, `wall_living_torch` |
| Wormwood set | `wormwood_planks`, `wormwood_stairs`, `wormwood_slab`, `wormwood_mosaic`, `wormwood_mosaic_stairs`, `wormwood_mosaic_slab`, `wormwood_fence`, `wormwood_fence_gate`, `wormwood_door`, `wormwood_trapdoor`, `wormwood_button`, `wormwood_pressure_plate`, `wormwood_cabinet` |
| Other | `gunk`, `rotten_spawner`, `embedded_eggs`, `heap_of_ancient_eggs` |

`wormwood_cabinet` extends Farmer's Delight's `CabinetBlock`; `spider_pie` and
`sculk_tart` extend its `PieBlock`; `ossobuco_block`, `guardian_angel_block`,
`glow_berry_gelatin_block` and `silverfish_and_chips_block` extend its
`FeastBlock`; `dungeon_stove` extends its `AbstractStoveBlock` /
`AbstractStoveBlockEntity`; the Monster Pot reuses its `CookingPotItemHandler`,
`CookingPotMealSlot` and `CookingPotSupport`.

### Non-food items

| Group | Items |
|---|---|
| Cleavers | `flint_cleaver`, `iron_cleaver`, `golden_cleaver`, `diamond_cleaver`, `netherite_cleaver`, `stained_cleaver` |
| Knife | `stained_knife` |
| Materials | `stained_scrap`, `stained_scrap_fragment`, `sculk_polyp`, `rotbulb`, `ancient_egg`, `brined_flesh`, `gritty_flesh` |
| Thrown | `rancid_reduction`, `gunk_arrow` (the six cleavers are also throwable — see below) |
| Transport | `wormwood_boat`, `wormwood_chest_boat` |
| Spawn eggs | `monster_yam_spawn_egg`, `rotten_zombie_spawn_egg` |

`CleaverItem` **extends Farmer's Delight's `KnifeItem`**, so cleavers carry the
`KNIFE_HARVEST` tool action and count as knives everywhere Farmer's Delight
tests for one in code.

### Cleaver and Stained Knife stats

Seven weapons, read out of the `register("…")` calls in `DDItems` (lines
152–172), the tiers in `DDMaterials`, and the `Item.Properties` constants in
`DDProperties`. The constructor is
`CleaverItem(float range, Tier tier, float attackDamage, float attackSpeed, Properties)`
— note `range` comes **first**, before the tier.

Attack damage is displayed as `attackDamage + tier bonus + 1` (the player's own
base), the same arithmetic used for the Farmer's Delight knives in
[blocks-items.md](blocks-items.md#knife-stats), so the two tables are directly
comparable. Durability is set explicitly in `Item.Properties` rather than
inherited, and matches each tier's own use count in every case.

| Weapon | Durability | Attack damage (displayed) | Attack speed | Mining tier | Mining speed | Enchantability | `range` |
|---|---|---|---|---|---|---|---|
| `flint_cleaver` Flint Cleaver | 131 | 4.0 | 1.0/s | Stone | 4.0 | 5 | 1.25 |
| `golden_cleaver` Golden Cleaver | 32 | 3.0 | 1.0/s | Wood | 12.0 | 22 | 1.75 |
| `iron_cleaver` Iron Cleaver | 250 | 5.0 | 1.0/s | Iron | 6.0 | 14 | 1.5 |
| `diamond_cleaver` Diamond Cleaver | 1561 | 6.0 | 1.0/s | Diamond | 8.0 | 10 | 1.75 |
| `netherite_cleaver` Netherite Cleaver | 2031 | 7.0 | 1.0/s | Netherite | 9.0 | 15 | 1.75 |
| `stained_cleaver` Stained Cleaver | 1016 | 6.5 | 1.0/s | Netherite | 7.0 | 20 | 1.75 |
| `stained_knife` Stained Knife | 1016 | 5.0 | 2.0/s | Netherite | 7.0 | 20 | — |

The Netherite Cleaver is fire-resistant as an item. Both Stained tools are
Uncommon rarity and repair from `#dungeonsdelight:repairs_stained_tools`. The
custom `STAINED` tier is mining level 4, 1016 uses, speed 7.0, +2.5 attack
damage, enchantability 20 — a Netherite-level tier with roughly half the
durability, better enchantability, and the second-highest damage bonus in the
set.

**Cleavers are a separate weapon line, not a knife variant.** Every cleaver
passes **−3.0** attack speed where every Farmer's Delight knife and the Stained
Knife pass **−2.0**, so cleavers swing at **1.0/s against 2.0/s** — half the
rate, for roughly 1.5 points more damage per hit. Against an Iron Knife's 3.5
damage at 2.0/s (7.0 DPS), an Iron Cleaver is 5.0 at 1.0/s (5.0 DPS): the
cleaver is the *worse* sustained melee weapon and is balanced around burst,
reach and throwing instead.

The Stained Knife is the outlier in the other direction — it keeps the knife's
−2.0 speed and gets the Stained tier's +2.5 bonus, giving **5.0 damage at
2.0/s**, which beats the Netherite Knife's 5.5 at the same speed only on
durability and enchantability, not on damage.

### Cleavers are throwable

The `range` field is a **public float on `CleaverItem` that is used exactly
once**, and it is not a reach or attack-range value. In
`CleaverItem.releaseUsing` it is passed as the fifth argument to
`AbstractArrow.shootFromRotation(shooter, xRot, yRot, zRot, velocity, inaccuracy)`
— so **`range` is the projectile's launch velocity**, with inaccuracy fixed at
`1.0`. The field name is misleading; higher values travel faster and further
per tick, but the mod defines no reach change of any kind. For scale, a thrown
trident uses velocity 2.5 and a fully drawn bow 3.0, so cleavers at 1.25–1.75
are slow projectiles.

The throw mechanic, from `CleaverItem` and `CleaverEntity`:

- Right-click **charges** the cleaver (`UseAnim.BOW`, max use duration 72000
  ticks). Releasing before **10 ticks** (0.5 s) does nothing.
- Releasing throws a `dungeonsdelight:cleaver` entity, costs **1 durability**,
  and plays `item.cleaver.throw`. A cleaver at 1 durability from breaking
  cannot be thrown at all.
- Hitting a block sets a **50-tick (2.5 s) cooldown** on the item and plays
  `item.cleaver.hit_block`. The cleaver sticks and can be picked back up;
  thrown in creative it is not retrievable.
- Damage on hit uses a dedicated `dungeonsdelight:cleaver` damage type.
- **Ricochet** (a Dungeon's Delight enchantment) adds one bounce per level.
  Each bounce reflects the velocity at ×0.8, multiplies damage by **×1.25**,
  and plays `item.cleaver.ricochet` rising 0.25 in pitch each time.
- **Serrated Strike** (also Dungeon's Delight's) applies the `serrated` effect
  on hit; re-applying to an already-serrated target adds half the remaining
  duration.
- Damage decays ×0.8 per entity pierced.

Base thrown damage is **not** the melee number. `CleaverEntity` overrides
`setBaseDamage(d)` as `this.damage = d * 1.66`, and the item throws with
`setBaseDamage(0 + getAttackDamage())`, where `getAttackDamage()` is the tier
bonus plus the constructor's `attackDamage` and **excludes** the player's +1.
So an unenchanted throw deals `(attackDamage + tier bonus) × 1.66`:

| Weapon | Melee (displayed) | Unenchanted thrown |
|---|---|---|
| Flint Cleaver | 4.0 | 4.98 |
| Golden Cleaver | 3.0 | 3.32 |
| Iron Cleaver | 5.0 | 6.64 |
| Diamond Cleaver | 6.0 | 8.30 |
| Netherite Cleaver | 7.0 | 9.96 |
| Stained Cleaver | 6.5 | 9.13 |

Sharpness adds `level × 0.5 + 0.5` — but because `setBaseDamage` re-applies the
×1.66 multiplier to the already-multiplied stored value, the enchanted totals
compound rather than adding linearly. That looks like an author error; the
per-level enchanted figures are deliberately **not published here**.

At an enchanting table a cleaver accepts **Sharpness, Smite, Bane of
Arthropods and Looting**, and explicitly refuses **Fortune, Fire Aspect and
Knockback** — narrower than a Farmer's Delight knife, which accepts Fire Aspect
and Knockback and refuses only Fortune. Anything whose own category already
accepts the item (Unbreaking, Mending) still applies.

### Foods

Nutrition, saturation modifier, flags and effects read out of `DDProperties` and
`INProperties`. Saturation restored is `nutrition × modifier × 2`. Effect
namespaces are written out because three mods contribute them:
`farmersdelight:comfort` is the parent mod's own effect, `runiclib:*` come from
the library dependency, the rest are Dungeon's Delight's or vanilla.

| Item | ID | Nutr. | Sat. mod | Flags | Effects |
|---|---|---|---|---|---|
| Amethyst Rock Candy | `amethyst_rock_candy` | 4 | 0.5 | stacks to 16 | `minecraft:strength` 1, 90 s, 70% |
| Arcane Chili | `arcane_chili` | 7 | 0.7 |  | `dungeonsdelight:tenacity` 1, 600 s; `runiclib:pyromaniac` 1, 120 s |
| Au Rotten Potatoes | `au_rotten_potatoes` | 6 | 0.5 | stacks to 16 | `dungeonsdelight:tenacity` 1, 180 s |
| Aurora Ice Cream | `aurora_ice_cream` | 9 | 0.5 | stacks to 16 | `farmersdelight:comfort` 1, 120 s; `minecraft:night_vision` 1, 120 s; `runiclib:perception` 1, 30 s |
| Blazing Blood Sausage | `blazing_blood_sausage` | 14 | 0.9 | stacks to 16 | `dungeonsdelight:burrow_gut` 1, 240 s; `runiclib:pyromaniac` 1, 120 s |
| Bloated Baked Potato | `bloated_baked_potato` | 4 | 0.4 |  |  |
| Bloody Mary | `bloody_mary` | 0 | 0.0 | fast, stacks to 16 | `dungeonsdelight:burrow_gut` 2, 180 s |
| Bowl of Glowberry Gelatin | `glow_berry_gelatin` | 7 | 0.5 | stacks to 16 | `runiclib:perception` 1, 180 s; `farmersdelight:comfort` 1, 180 s |
| Bowl of Ossobuco | `ossobuco` | 12 | 0.9 | stacks to 16 | `dungeonsdelight:voracity` 2, 120 s |
| Bowl of Silverfish and Chips | `silverfish_and_chips` | 10 | 0.9 | stacks to 16 | `dungeonsdelight:burrow_gut` 1, 240 s; `dungeonsdelight:voracity` 1, 120 s |
| Bubblegunk | `bubblegunk` | 0 | 0.0 | fast |  |
| Bug Chops | `bug_chops` | 4 | 0.3 | meat |  |
| Candied Silverfish Sucker | `candied_silverfish_sucker` | 6 | 0.3 | stacks to 16 | `dungeonsdelight:decisive` 1, 120 s; `dungeonsdelight:burrow_gut` 1, 120 s |
| Candied Vex Sucker | `candied_vex_sucker` | 4 | 0.5 | stacks to 16 | `dungeonsdelight:decisive` 1, 120 s; `minecraft:speed` 1, 120 s |
| Chicken Jockey Sandwich | `chicken_jockey_sandwich` | 7 | 0.7 | stacks to 16 |  |
| Chloropasta | `chloropasta` | 12 | 0.8 | stacks to 16 | `farmersdelight:comfort` 1, 120 s; `minecraft:regeneration` 2, 6 s, 50% |
| Cleaved Ancient Egg | `cleaved_ancient_egg` | 2 | 0.4 |  |  |
| Cob n' Candy | `cob_n_candy` | 4 | 0.4 |  | `dungeonsdelight:decisive` 1, 20 s; `dungeonsdelight:pouncing` 1, 20 s |
| Cooked Sniffer Shank | `cooked_sniffer_shank` | 8 | 0.9 |  |  |
| Cooked Snifferwurst | `cooked_snifferwurst` | 10 | 0.7 |  | `minecraft:regeneration` 1, 8 s, 60% |
| Creeperilla | `creeperilla` | 2 | 0.3 | always edible |  |
| Creeperilla Squib | `creeperilla_squib` | 1 | 0.2 | always edible |  |
| Devilish Eggs | `devilish_eggs` | 6 | 0.7 |  |  |
| Fried Bug Chops | `fried_bug_chops` | 8 | 0.8 | meat |  |
| Fried Ghast Calamari | `fried_ghast_calamari` | 4 | 0.6 | meat, always edible |  |
| Gelled Salad | `gelled_salad` | 8 | 0.6 | stacks to 16 | `dungeonsdelight:tenacity` 1, 120 s |
| Ghast Calamari | `ghast_calamari` | 2 | 0.3 | meat, always edible |  |
| Ghast Roll | `ghast_roll` | 6 | 0.6 | always edible | `minecraft:regeneration` 1, 20 s |
| Ghast Tentacle | `ghast_tentacle` | 3 | 0.3 | meat |  |
| Ghastly Spirits | `ghastly_spirits` | 0 | 0.0 | fast, stacks to 16 | `minecraft:levitation` 1, 15 s; `minecraft:regeneration` 3, 12 s; `minecraft:slow_falling` 1, 20 s |
| Ghoulash | `ghoulash` | 8 | 0.6 | stacks to 16 | `dungeonsdelight:voracity` 1, 240 s |
| Gyudon | `gyudon` | 9 | 0.7 | stacks to 16 | `dungeonsdelight:voracity` 2, 180 s; `minecraft:fire_resistance` 1, 90 s |
| Hydra Fricassee | `hydra_fricassee` | 10 | 1.0 | stacks to 16 | `dungeonsdelight:voracity` 2, 360 s; `runiclib:pyromaniac` 1, 120 s |
| Liveroot Beer | `liveroot_beer` | 2 | 0.4 | fast, stacks to 16 | `minecraft:speed` 1, 60 s |
| Logo Item | `logo_item` | -3 | 0.0 | always edible, fast |  |
| Malicious Sandwich | `malicious_sandwich` | 9 | 0.9 | stacks to 16 |  |
| Maze Roll | `maze_roll` | 6 | 0.6 | always edible |  |
| Meef Wellington | `meef_wellington` | 10 | 0.7 |  |  |
| Monster Muffin | `monster_muffin` | 5 | 0.5 | always edible | `dungeonsdelight:exudation` 1, 120 s |
| Plate of Guardian Angel | `guardian_angel` | 8 | 1.0 | stacks to 16 | `dungeonsdelight:voracity` 1, 180 s |
| Poi | `poi` | 6 | 0.5 | stacks to 16 | `dungeonsdelight:tenacity` 1, 180 s; `dungeonsdelight:exudation` 1, 300 s |
| Poisonous Poutine | `poisonous_poutine` | 8 | 0.7 | stacks to 16 | `dungeonsdelight:voracity` 1, 120 s; `dungeonsdelight:pouncing` 1, 180 s |
| Raw Sniffer Shank | `sniffer_shank` | 4 | 0.4 |  |  |
| Raw Snifferwurst | `snifferwurst` | 6 | 0.5 |  | `minecraft:regeneration` 1, 6 s, 40% |
| Rotten Tripe | `rotten_tripe` | 2 | 0.05 | meat | `minecraft:hunger` 1, 10 s, 20% |
| Rubaboo | `rubaboo` | 5 | 0.5 | stacks to 16 | `dungeonsdelight:tenacity` 1, 60 s; `minecraft:fire_resistance` 1, 120 s |
| Salt Soaked Stew | `salt_soaked_stew` | 10 | 0.8 | stacks to 16 | `minecraft:water_breathing` 1, 60 s; `dungeonsdelight:tenacity` 1, 180 s |
| Scaly Fiddlehead Risotto | `scaly_fiddlehead_risotto` | 8 | 0.8 | stacks to 16 | `dungeonsdelight:voracity` 2, 480 s |
| Sculk Apple | `sculk_apple` | 5 | 0.5 | fast |  |
| Sculk Mayo | `sculk_mayo` | 1 | 0.2 | fast, stacks to 16 | `minecraft:weakness` 1, 120 s, 20% |
| Shiokara | `shiokara` | 7 | 0.5 | stacks to 16 | `dungeonsdelight:tenacity` 1, 180 s; `minecraft:regeneration` 2, 7 s; `dungeonsdelight:putrid_scent` 1, 7 s |
| Silverfish Abdomen | `silverfish_abdomen` | 2 | 0.4 | meat |  |
| Silverfish Fried Rice | `silverfish_fried_rice` | 12 | 0.9 | stacks to 16 | `dungeonsdelight:burrow_gut` 1, 180 s; `dungeonsdelight:tenacity` 1, 240 s |
| Sinigang | `sinigang` | 6 | 0.6 | stacks to 16 | `dungeonsdelight:tenacity` 1, 120 s; `dungeonsdelight:pouncing` 1, 180 s; `dungeonsdelight:exudation` 2, 180 s |
| Slice of Monster Cake | `monster_cake_slice` | 3 | 0.5 |  | `dungeonsdelight:exudation` 2, 120 s; `dungeonsdelight:pouncing` 2, 60 s |
| Slice of Spider Pie | `spider_pie_slice` | 3 | 0.3 | always edible |  |
| Slicorice | `slicorice` | 3 | 0.4 | always edible |  |
| Slime Noodles | `slime_noodles` | 1 | 0.2 |  |  |
| Slime Slab | `slime_bar` | 2 | 0.3 |  |  |
| Smoked Spider Meat | `smoked_spider_meat` | 5 | 0.7 | meat |  |
| Snuffledog | `snuffledog` | 14 | 1.1 | stacks to 16 | `minecraft:regeneration` 2, 6 s |
| Soaked Skewer | `soaked_skewer` | 7 | 0.6 | stacks to 16 | `minecraft:water_breathing` 1, 120 s; `dungeonsdelight:decisive` 1, 120 s |
| Soft Serve Sniffer Egg | `soft_serve_sniffer_egg` | 4 | 0.4 | stacks to 16 | `minecraft:regeneration` 1, 5 s, 75% |
| Spider Bubble Tea | `spider_bubble_tea` | 0 | 0.0 | fast, stacks to 16 |  |
| Spider Extract | `spider_extract` | 0 | 0.0 | fast, stacks to 16 | `minecraft:poison` 1, 30 s |
| Spider Meat | `spider_meat` | 2 | 0.4 | meat | `minecraft:poison` 1, 15 s, 50% |
| Spider Salmagundi | `spider_salmagundi` | 7 | 0.9 | stacks to 16 | `dungeonsdelight:tenacity` 1, 45 s; `dungeonsdelight:pouncing` 2, 45 s |
| Spider Tanghulu | `spider_tanghulu` | 5 | 0.7 | stacks to 16 | `dungeonsdelight:pouncing` 1, 300 s; `dungeonsdelight:decisive` 1, 120 s |
| Sweetbread | `sweetbread` | 6 | 0.8 | always edible | `dungeonsdelight:burrow_gut` 1, 60 s |
| Taro Milk Tea | `taro_milk_tea` | 0 | 0.0 | fast, stacks to 16 | `dungeonsdelight:exudation` 3, 300 s |
| Terrine Loaf | `terrine_loaf` | 7 | 0.9 | stacks to 16 | `dungeonsdelight:exudation` 2, 180 s; `minecraft:water_breathing` 1, 90 s |
| The Monster Burger | `monster_burger` | 20 | 1.0 | stacks to 1 | `dungeonsdelight:tenacity` 1, 1 s; `dungeonsdelight:burrow_gut` 1, 1 s; `dungeonsdelight:decisive` 1, 1 s; `dungeonsdelight:exudation` 1, 1 s; `dungeonsdelight:pouncing` 1, 1 s; `dungeonsdelight:voracity` 1, 1 s |
| Tokayaki | `tokayaki` | 9 | 0.7 | stacks to 16 | `dungeonsdelight:voracity` 1, 120 s; `dungeonsdelight:exudation` 2, 120 s |
| Torchberry Raisins | `torchberry_raisins` | 1 | 0.3 | always edible |  |
| Tower Boreito | `tower_boreito` | 12 | 1.2 | stacks to 16 | `dungeonsdelight:burrow_gut` 2, 300 s |
| Trollber Chutney | `trollber_chutney` | 5 | 0.5 | fast, stacks to 16 | `runiclib:perception` 1, 15 s |
| Wardenzola | `wardenzola` | 4 | 0.6 |  |  |
| Wardenzola Crumbles | `wardenzola_crumbles` | 2 | 0.3 | always edible |  |
| Wilderness Luncheon | `wilderness_luncheon` | 7 | 0.6 |  |  |
| sculk catblueberry | `sculk_catblueberry` | 5 | 0.5 | fast |  |
| sculk dogapple | `sculk_dogapple` | 5 | 0.5 | fast |  |

The two Appledog items are listed lowercase because that is verbatim what
`assets/dungeonsdelight/lang/en_us.json` gives for
`item.dungeonsdelight.sculk_catblueberry` and `…sculk_dogapple` — unfinished
strings in the jar, not a transcription slip. Their `FoodProperties` carry no
effect, but the jar's tooltip keys claim Instant Health; that is applied
elsewhere in code and the amount is **not documented here**.

Items whose `FoodProperties` are built without a nutrition call — Bubblegunk,
Bloody Mary, Taro Milk Tea, Spider Bubble Tea, Rancid Reduction, Spider Extract,
Ghastly Spirits — restore **0** hunger by construction; they are consumed for
their effects.

### Effects (10)

| Effect | Kind | Notes |
|---|---|---|
| `feral_bite` | beneficial | plain effect |
| `serrated` | harmful | |
| `putrid_scent` | harmful | |
| `ravenous_rush` | beneficial | +30 % movement speed, +10 % attack damage, both `MULTIPLY_TOTAL` |
| `exudation` | neutral | monster variant of `minecraft:absorption` |
| `decisive` | neutral | monster variant of `minecraft:strength` |
| `pouncing` | neutral | monster variant of `minecraft:jump_boost` |
| `burrow_gut` | neutral | monster variant of `minecraft:haste`, drains hunger |
| **`voracity`** | neutral | **monster variant of `farmersdelight:nourishment`**, drains hunger |
| **`tenacity`** | neutral | **monster variant of `farmersdelight:comfort`**, heals 1 HP on an interval |

The last two are the ones that reach into Farmer's Delight — see
[Farmer's Delight behaviour it changes](#farmers-delight-behaviour-it-changes).

Also registered: 3 enchantments (`ricochet`, `serrated_strike`, `life_grasp`),
6 entities (`monster_yam`, `rotten_zombie`, `ancient_egg`, `cleaver`,
`rancid_reduction`, `gunk_arrow`), 8 damage types, one structure
(`rotten_dungeon`, one 1-piece template pool) and two configured features
(`wormroot`, `patch_wild_rotbulb`; Rotbulb generates in `minecraft:swamp` and
`minecraft:mangrove_swamp` only).

### Recipes (140 files in `data/dungeonsdelight/recipes/`)

| Type | Count |
|---|---|
| `dungeonsdelight:monster_cooking` | 52 |
| `minecraft:crafting_shaped` | 40 |
| `minecraft:crafting_shapeless` | 17 |
| **`farmersdelight:cutting`** | **14** |
| `minecraft:smoking` | 7 |
| **`farmersdelight:cooking`** | **6** |
| `minecraft:smelting` | 2 |
| `minecraft:campfire_cooking` | 2 |

Plus 10 more in `data/twilightforest/recipes/` (see
[Integration content](#integration-content-for-mods-that-are-not-installed)).

**Monster cooking** is a new recipe type and serializer,
`dungeonsdelight:monster_cooking`, worked by the **Monster Pot** — a Cooking Pot
built on Farmer's Delight's own block-entity classes but with a separate recipe
registry, so Monster Pot recipes do not appear in the Cooking Pot and vice
versa. All 52 use Farmer's Delight's `recipe_book_tab` field (`meals`, `drinks`,
`misc`) and a 200-tick cook time. Monster Pot crafting recipe: a
`farmersdelight:cooking_pot` in the centre, five Stained Scrap around and below
it, two Spider Eyes and a Bone across the top.

The Monster Pot's heat comes from `dungeonsdelight:monster_heat_sources` —
`minecraft:spawner`, the Dungeon Stove, the Stained Lantern, and the
`monster_tray_heat_sources` tag (Living Fire, Living Campfire). It does **not**
read Farmer's Delight's `heat_sources` tag, so a vanilla Campfire or a Farmer's
Delight Stove will not run a Monster Pot.

**The 6 `farmersdelight:cooking` recipes** are new **Cooking Pot** recipes. One
loads here:

- `cooking/dog_food_from_fleshes_tag.json` — **`farmersdelight:dog_food`** from
  `#dungeonsdelight:fleshes` + Bone Meal + `#farmersdelight:wolf_prey` +
  `#forge:crops/rice`, 200 ticks, 1.0 xp, `misc` tab. A new, additional way to
  obtain a Farmer's Delight item.

The other five are Twilight Forest-gated and do not load.

**The 14 `farmersdelight:cutting` recipes** are Cutting Board recipes, all
requiring `#farmersdelight:tools/knives`: Ancient Egg, Brined Flesh, Creeperilla,
Ghast Tentacle, Gritty Flesh, Gunk, Monster Cake, Rotbulb, Rotbulb Plant, Sculk
Mayo Block, Sculk Tart, Slime Bar, Spider Pie, Wardenzola. Two of them return
Farmer's Delight items as by-products — Gunk cuts to `farmersdelight:straw`, and
Slime Bar returns the `farmersdelight:canvas` it was made with.

### Data it contributes to the `farmersdelight` namespace

Eight files under `data/farmersdelight/`. **Every one of them is a tag, and none
of them sets `"replace": true`** — so all eight merge with the parent mod's own
tag rather than replacing it. Nothing in this jar overwrites a Farmer's Delight
recipe, loot table, advancement or model. Verified by listing the jar's full
entry set: the only `farmersdelight`-namespace paths present are these eight.

| File | Adds | What changes |
|---|---|---|
| `tags/blocks/heat_sources.json` | `dungeonsdelight:dungeon_stove` (plus `netherexp:treacherous_candle`, `required: false`, not installed) | The Dungeon Stove powers a **Farmer's Delight Cooking Pot and Skillet** (`HeatableBlockEntity`, plus a held Skillet cooking beside one) |
| `tags/blocks/tray_heat_sources.json` | `dungeonsdelight:living_fire` | Living Fire heats a Skillet or Cooking Pot placed directly on top of it |
| `tags/items/cabinets/wooden.json` | `dungeonsdelight:wormwood_cabinet` | Wormwood Cabinet behaves as a wooden cabinet |
| `tags/items/tools/knives.json` | `#dungeonsdelight:cleavers`, `dungeonsdelight:stained_knife` | **7 new tools count as knives to Farmer's Delight's code** — see below |
| `tags/items/meals.json` | 19 Dungeon's Delight meals | They stack to 16 and behave as Farmer's Delight meals |
| `tags/items/feasts.json` | `ossobuco_block`, `guardian_angel_block`, `glow_berry_gelatin_block`, `silverfish_and_chips_block` | Treated as feasts |
| `tags/items/drinks.json` | `spider_bubble_tea`, `bloody_mary`, `taro_milk_tea`, `liveroot_beer` | Treated as drinks |
| `tags/blocks/mineable/knife.json` | 9 Dungeon's Delight food blocks, `embedded_eggs`, `heap_of_ancient_eggs`, `silverfish_and_chips_block`, **and 6 vanilla sculk blocks** | See below |

Two of those deserve spelling out.

**Sculk becomes knife-mineable.** `mineable/knife` gains `minecraft:sculk`,
`sculk_catalyst`, `sculk_vein`, `sculk_sensor`, `calibrated_sculk_sensor` and
`sculk_shrieker`. Farmer's Delight's own copy of that tag lists only cactus,
melon, pumpkins, cobweb, cake, wool and its own pies. After the merge, **a
Farmer's Delight knife is the correct tool for every sculk block in the Deep
Dark** on this server. That is a change to vanilla behaviour delivered through a
Farmer's Delight tag, and it is what makes the `sculk_polyp` global loot
modifiers reachable.

**Seven new knives.** The six cleavers and the Stained Knife join
`farmersdelight:tools/knives`. They therefore work for **knife scavenging**
(feather, leather, string, rabbit hide, shulker shell, ham from pigs and
hoglins), **pastry and cake slicing**, **straw harvesting**
(`straw_harvesters` includes the knives tag) and **rice harvesting**.

They also perform **all 47** of Farmer's Delight's knife cutting-board recipes,
but they get that from inheritance rather than from this tag — see below.

### Tag-only checks and what they actually cost

Dungeon's Delight adds its cleavers and the Stained Knife to
`farmersdelight:tools/knives` but **not** to `forge:tools/knives`. That is a
real inconsistency in the jar. **In practice it costs almost nothing**, and the
reason is the ToolAction alternative described in
[How Farmer's Delight decides something is a tool](#how-farmers-delight-decides-something-is-a-tool).

The inheritance chain, read out of the decompiled jars:

- `CleaverItem extends KnifeItem` — Farmer's Delight's own `KnifeItem`.
  `StainedKnifeItem extends KnifeItem`; `StainedCleaverItem extends
  CleaverItem`; the eight Twilight Forest integration tools extend
  `INKnifeItem`/`INCleaverItem`, which extend the same two.
- `KnifeItem.canPerformAction` is `return KNIFE_ACTIONS.contains(toolAction);`
  — unconditional, no stack or tag test.
- `KNIFE_ACTIONS = Set.of(SHEARS_CARVE, SWORD_DIG, KNIFE_DIG, KNIFE_HARVEST)`,
  so `knife_dig` is in the set.
- Grepping the entire decompiled Dungeon's Delight source for
  `canPerformAction` returns **nothing** — no subclass overrides it.

So every Dungeon's Delight cleaver and the Stained Knife satisfy the
`knife_dig` branch of all 47 recipes, and they satisfy `ItemUtils.isKnife()`
twice over. **They perform every Farmer's Delight cutting-board knife recipe.**

Only a check written as a bare tag object, with no action alternative, can
exclude them. Three such checks exist on this server, and all three are
third-party rather than Farmer's Delight's own data:

| Tag-only check | Written as | Effect on Dungeon's Delight tools |
|---|---|---|
| Alex's Delight's 5 cutting recipes | `"tool": {"tag": "forge:tools/knives"}` | **Genuinely excluded** — a cleaver cannot cut Raw Bison, Raw Bunfungus, kangaroo meat, moose ribs or raw catfish |
| Sophisticated Backpacks' FD compat | `{"type": "tag", "tag": "forge:tools/knives"}` in a JSON registry | Excluded from Tool Swapper auto-swap on the cutting board and on animals |
| `CuttingBoardBlockEntity.playProcessingSound` | `tool.is(CommonTags.Items.TOOLS_KNIVES)` | **Cosmetic only** — a cleaver cuts fine but plays the board's block sound instead of the knife sound |

Symmetrically, Dungeon's Delight writes its own 14 cutting recipes as
`{"tag": "farmersdelight:tools/knives"}`, also tag-only, so a third-party knife
that performs `knife_dig` without joining that tag cannot run them. Farmer's
Delight's five knives are in both tags and run everything in both directions.

A one-line datapack addition to `forge:tools/knives` would close all three
gaps. The only one a player would notice is the Alex's Delight row.

### Farmer's Delight behaviour it changes

Four mechanisms, none of them a data override.

**1. Three Farmer's Delight foods gain effects they do not have in the parent
mod.** `DDCommonEvents.handleAdditionalFoodEffects` subscribes to
`LivingEntityUseItemEvent.Finish` and applies, on the live config
(`fdStickFoodsGrantStrength = true`, `fdGlowingFoodsGrantPerception = true`):

| Farmer's Delight item | Added effect |
|---|---|
| Barbecue Stick | `minecraft:strength` I for 1,200 ticks (60 s) |
| Melon Popsicle | `minecraft:strength` I for 100 ticks (5 s) |
| Glow Berry Custard | `runiclib:perception` I for 1,200 ticks (60 s) |

Both switches are exposed in `/config/dungeonsdelight-config.toml` and both are
at their `true` defaults here.

**2. Nourishment and Comfort get overwritten while a monster variant is
active.** `MonsterEffect.applyEffectTick` scans the entity's active effects each
tick and, on finding its declared normal variant, swaps it: the old effect is
removed and the monster variant is applied for the **remaining duration of the
old effect** (`DDUtil.applyEffectSwap`), always at amplifier 0. `voracity`
declares `farmersdelight:nourishment` as its normal variant and `tenacity`
declares `farmersdelight:comfort`. So while Voracity is running, **any
Nourishment the player gains from any Farmer's Delight meal is immediately
converted into Voracity** — which drains 0.075 × (amplifier+1) exhaustion per
tick instead of suppressing hunger. Tenacity likewise consumes Comfort, healing
1 HP on an interval derived from the player's saturation
(`saturation × 3` ticks) instead. Ten Dungeon's Delight foods in the table above
grant Voracity and eleven grant Tenacity, so this is a routine occurrence rather
than an edge case. Three of its foods grant Farmer's Delight's Comfort directly
(Aurora Ice Cream, Bowl of Glowberry Gelatin, Chloropasta), which a subsequent
Tenacity will then consume.

**3. Knife scavenging is extended to 8 new mob families.** Dungeon's Delight
registers 23 global loot modifiers through `data/forge/loot_modifiers/`, all
built on **Farmer's Delight's own GLM types** (`farmersdelight:add_item`,
`farmersdelight:add_loot_table`, `farmersdelight:pastry_slicing`) and all
conditioned on `#farmersdelight:tools/knives` in the killer's main hand:

| Drop | From (entity tag) |
|---|---|
| `spider_meat` | spider, cave spider (+ 4 Twilight Forest spiders, absent) — only when not on fire |
| `smoked_spider_meat` | same, when on fire |
| `silverfish_abdomen` | silverfish |
| `rotten_tripe` | zombie, husk, drowned, `dungeonsdelight:rotten_zombie` |
| `slime_noodles` | slime (+ absent Twilight Forest and Aether slimes) |
| `ghast_tentacle` | ghast (+ 3 absent Twilight Forest ghasts) |
| `sculk_polyp` | warden |
| `gunk` | `dungeonsdelight:monster_yam` |
| `creeperilla` | **entity tag is empty in the jar — this modifier can never fire** |
| `bug_chops` | Twilight Forest beetles and `hamsters:hamster` — none installed, never fires |

Four more are plain drops with no knife requirement: `gritty_flesh` from husks
and `brined_flesh` from drowned, both at 30 % + 10 %/level of Looting and only
when killed by a player; `sniffer_shank` / `cooked_sniffer_shank` from sniffers.
Eight more add `stained_scrap` to spawner and Rotten Spawner drops and
`sculk_polyp` to all six sculk blocks. One is a
`farmersdelight:pastry_slicing` modifier giving Sculk Tart slices to any
`farmersdelight:tools/knives` tool.

**4. The Rotten Tomatoes crop drops a Farmer's Delight item.** Its block loot
uses `ModItems.ROTTEN_TOMATO` — a Farmer's Delight item — as its crop drop, and
the Rotten Tomato Crate packs and unpacks nine of them. Dungeon's Delight also
uses Farmer's Delight's Rich Soil and Rich Soil Farmland in
`rotbulb_growable_on`, and `farmersdelight:pie_crust` and
`farmersdelight:canvas` as crafting ingredients.

Damage from Dungeon's Delight's Ancient Egg, Rancid Reduction, raw creeper foods
and Bloody Mary is dealt through Farmer's Delight's
`ModDamageTypes.getSimpleDamageSource()` helper, but the damage types themselves
are Dungeon's Delight's own. That is a utility call, not a behaviour change.

### Mixins

`dungeonsdelight.mixin.json`, `"required": true`, JAVA_17, 10 common + 7 client
mixins: `AllayMixin`, `BaseFireBlockMixin`, `BlockMixin`, `BoatMixin`,
`BoatTypeMixin`, `ChestBoatMixin`, `FoodDataMixin`, `LivingEntityMixin`,
`MobEffectUtilMixin`, `PlayerMixin`. **All target vanilla classes — none targets
Farmer's Delight.** The live log carries one cosmetic complaint about the config
at boot:

```
[main/ERROR] [mixin/]: Mixin config dungeonsdelight.mixin.json does not specify
"minVersion" property
```

That is a metadata warning, not a failure; all mixins apply.

### Integration content for mods that are not installed

Dungeon's Delight ships content for seven other mods, named in
`IntegrationIds`: `arts_and_crafts`, `appledog`, `bountifulfares`, `cannibal`,
`excessive_building`, `netherexp`, `twilightforest`. **None of the seven is
installed on this server.**

- **25 items are registered anyway.** `TFItems` (23) and `ADItems` (2) register
  unconditionally on the mod event bus. Their `isEnabled()` returns true if the
  companion mod is loaded **or** `forceEnableCompatItems` is true **or**
  `disableContentIntegration` is *false*. The live config has
  `forceEnableCompatItems = false` and `disableContentIntegration = false`, so
  the third clause is satisfied and **all 25 exist and are usable here** —
  `ironwood_knife`, `ironwood_cleaver`, `steeleaf_knife`, `steeleaf_cleaver`,
  `knightmetal_knife`, `knightmetal_cleaver`, `fiery_knife`, `fiery_cleaver`,
  `bug_chops`, `fried_bug_chops`, `torchberry_raisins`, `wilderness_luncheon`,
  `maze_roll`, `meef_wellington`, `sweetbread`, `tower_boreito`,
  `aurora_ice_cream`, `blazing_blood_sausage`, `arcane_chili`,
  `hydra_fricassee`, `scaly_fiddlehead_risotto`, `liveroot_beer`,
  `trollber_chutney`, `sculk_dogapple`, `sculk_catblueberry`.
- **They are invisible in creative.** The "Dungeon's Delight Compat" tab adds
  them only inside `Services.PLATFORM.isModLoaded(...)` guards, which fail here.
- **They are uncraftable.** 25 of the 26 integration recipes carry a
  `forge:mod_loaded` condition (13 in the `dungeonsdelight` namespace, 10 in
  `data/twilightforest/recipes/`, 2 for `appledog`) and are discarded at load.
  The one exception is `recipes/integration/common/fried_bug_chops_from_smoking.json`,
  which is ungated and **does** load — but its only input, `bug_chops`, has no
  reachable source, because the loot modifier that would drop it is keyed to
  Twilight Forest beetles.

Net effect: 25 registered, enabled, hidden, unobtainable items. Four of them
(`arcane_chili`, `hydra_fricassee`, `aurora_ice_cream`,
`scaly_fiddlehead_risotto`) and one drink (`liveroot_beer`) are listed as plain
strings in Dungeon's Delight's additions to `farmersdelight:meals` and
`farmersdelight:drinks`; because the items *are* registered, those tag entries
resolve and no tag error is logged.

### Data it ships for Amendments

`data/amendments/tags/items/sets_on_fire.json` (adding `living_torch`) and
twelve files under `assets/amendments/` for a double Monster Cake model.
**Amendments is not installed** — it appears in none of the 148
`META-INF/mods.toml` files and in no filename in `/mods`. Both trees are inert.
The tag entry is written `{"id": ..., "required": false}` and the namespace has
no consumer, so nothing is logged.

### Live config

`/config/dungeonsdelight-config.toml`, all four options at their code defaults:

| Option | Value | Default | Effect |
|---|---|---|---|
| `fdStickFoodsGrantStrength` | `true` | `true` | Barbecue Stick and Melon Popsicle grant Strength |
| `fdGlowingFoodsGrantPerception` | `true` | `true` | Glow Berry Custard grants `runiclib:perception` |
| `forceEnableCompatItems` | `false` | `false` | |
| `disableContentIntegration` | `false` | `false` | Integration items stay registered and enabled |

One loot-table validation warning appears at boot and is Dungeon's Delight's
own, not a Farmer's Delight interaction:

```
[main/WARN] [LootDataManager]: Found loot table element validation problem in
{loot_tables:dungeonsdelight:entities/monster_yam}.pools[0].entries[0].functions[1]:
Parameters [<parameter minecraft:tool>] are not provided in this context
```

It repeats for `pools[1]`. The Monster Yam's drops still roll; the `tool`-gated
function inside them cannot evaluate.

## Alex's Delight (`alexsdelight` 1.5)

By **NCP Bails**. License **All Rights Reserved**. Full treatment, including its
three Alex's Mobs data overrides and the broken Barbecue on a Stick recipe, is
in [../alexs-mobs/addons.md](../alexs-mobs/addons.md). This section covers only
what it contributes to the Farmer's Delight cooking system.

**It ships zero files in the `farmersdelight` namespace** — no data, no assets.
Confirmed by full entry scan of the jar. Everything it does to Farmer's Delight
is done from its own namespace or from code.

It also **does not declare `farmersdelight` in `mods.toml`** (only `forge` and
`minecraft`), yet `AlexsDelight.addCreative()` reads
`vectorwing.farmersdelight.common.registry.ModCreativeTabs.TAB_FARMERS_DELIGHT`
and `ModFoods` references `ModEffects.NOURISHMENT`. Forge's dependency checker
cannot catch that. Farmer's Delight 1.3.2 is present, so it is latent.

What it adds to the cooking chain, from `data/alexsdelight/recipes/` (39 files):

| Type | Count | Notes |
|---|---|---|
| `farmersdelight:cutting` | 5 | Cutting Board, tool `#forge:tools/knives`, all yield 2 |
| `farmersdelight:cooking` | 4 | Cooking Pot, 200 ticks / 0.35 xp, served in a bowl |
| `minecraft:smelting` / `smoking` / `campfire_cooking` | 8 each | the same 8 ingredients in all three, 200 ticks / 1.0 xp — so the Smoker gets none of its usual speed advantage |
| `minecraft:crafting_shapeless` | 6 | one of which is broken |

- All **23 of its food items register into the Farmer's Delight creative tab**,
  not one of their own.
- Four of them (Kangaroo Stew, Acacia Blossom Soup, Lobster Pasta, Kangaroo
  Pasta) grant **`farmersdelight:nourishment`** for 5 minutes.
- Its cooking-pot recipes consume Farmer's Delight ingredients directly: Onion
  (2), Raw Pasta (3), Tomato Sauce (2), Tomato, Cabbage, Beetroot, Red Mushroom
  Colony (2), Mixed Salad.
- One recipe **produces a Farmer's Delight item**: `barbecue_on_a_stick` would
  yield 2 × `farmersdelight:barbecue_stick`. It is the broken one — it lists an
  ingredient in a nonexistent `amfd:` namespace and Forge discards it at load,
  confirmed in the live log. So Alex's Delight adds **no** working new route to
  a Farmer's Delight item.

Its five cutting recipes write `"tool": {"tag": "forge:tools/knives"}` as a
bare tag object with no ToolAction alternative — unlike Farmer's Delight's own
recipes, which always offer one. That makes these the only recipes on the server
that genuinely exclude Dungeon's Delight cleavers and the Stained Knife. See
[Tag-only checks and what they actually cost](#tag-only-checks-and-what-they-actually-cost).
Farmer's Delight's own five knives run them.

## Other mods on this server that touch Farmer's Delight

The list below was built by downloading **all 148 jars** in the live `/mods`
through the Pterodactyl client API and, for each, enumerating every entry under
`data/farmersdelight/**` and `assets/farmersdelight/**`, enumerating any other
path containing `farmersdelight`, and decompressing every file to scan for the
literal byte strings `farmersdelight` and `vectorwing` — including nested
jar-in-jar. **All 148 downloaded and scanned successfully; none failed.**

Exactly **ten** jars carry a hit: Farmer's Delight itself, the two add-ons
above, and the seven below. Nothing else on the server references Farmer's
Delight in any form.

### Supplementaries 3.1.43

The most extensive of the non-add-ons, and the only other jar that ships files
under `data/farmersdelight/`. Four tag files, all `"replace": false` or with no
`replace` key, so all additive:

| File | Adds | Status |
|---|---|---|
| `tags/blocks/mineable/knife.json` | `supplementaries:sack`, `#supplementaries:flags` | active — Farmer's Delight knives cut sacks and flags |
| `tags/blocks/ropes.json` | `supplementaries:rope` | active — tomato vines climb Supplementaries rope, since `enableTomatoVineClimbingTaggedRopes = true` in the live config |
| `tags/blocks/mushroom_colony_growable_on.json` | `supplementaries:planter_rich` | active |
| `tags/blocks/tray_heat_source.json` | `supplementaries:blaze_rod_block`, `supplementaries:fire_pit` | **dead — see below** |

> **Defect: a misspelled mod id.** `recipes/quiver_fd.json` carries
> `{"type": "forge:mod_loaded", "modid": "farmers_delight"}` — with an
> underscore. The mod id is `farmersdelight`, and the other **seven**
> `forge:mod_loaded` conditions in the same jar spell it correctly. Forge
> resolves the misspelling to "not loaded", so the condition can never pass and
> the recipe is silently dropped at load. It would have cut a Saddle into 2
> Leather with shears. The recipe also carries a `supplementaries:flag`
> condition for `quiver`, so it may have been gated anyway — but the mod id
> alone is sufficient to kill it, and the inconsistency with its seven siblings
> makes it a typo rather than an intent.

> **Defect: a misnamed tag.** Farmer's Delight's tag is
> `farmersdelight:tray_heat_sources` — **plural**. Re-verified against code
> rather than filenames: `ModTags` declares it as
> `modBlockTag("tray_heat_sources")`, it is read in exactly two places
> (`SkilletBlock` line 179 and `CookingPotBlock` line 124, both testing the
> block directly beneath), and grepping the entire Farmer's Delight jar — data,
> assets and classes — returns **12 occurrences of the plural and zero of the
> singular**. Supplementaries ships
> `tray_heat_source` (singular). The file creates a tag nothing reads, so
> **the Blaze Rod Block and the Fire Pit do not keep a Skillet hot on a tray.**
> Dungeon's Delight ships the same tag spelled correctly, which is how the
> difference was caught. Fixable with a one-file datapack override under the
> plural name.

Beyond the tags, Supplementaries carries a real code integration
(`integration/FarmersDelightCompat`, `CompatFarmersDelightTomatoMixin`, and
`TomatoRopeBlock` / `TomatoStickBlock` / `TomatoLoggedBlock`) letting Farmer's
Delight tomato vines grow on Supplementaries ropes and sticks, with eight
dedicated block models. It also ships:

- **Three cutting-board recipes** of its own (`farmersdelight:cutting`) —
  `ash_bricks_fd`, `lapis_bricks_fd` and `quiver_fd`. The third never loads;
  see below.
- Recipe variants gated on `farmersdelight` being loaded: `pancake_fd`,
  `planter`, `planter_rich` (crafted from `farmersdelight:rich_soil`), `sack_2`,
  `sack_3` (from `farmersdelight:canvas`).
- A `straw_from_flax` global loot modifier keyed to
  `#farmersdelight:straw_harvesters`, dropping `farmersdelight:straw`.
- Eleven Moonlight soft-fluid definitions covering Farmer's Delight drinks —
  apple cider, hot cocoa, tomato sauce, melon juice, berry custard, and the
  stews and soups — each tagged `"from_mod": "farmersdelight"`, so they work in
  jars, faucets and the fluid systems.
- Farmer's Delight entries in `tags/items/cookies` (honey, sweet berry, peanut
  butter), `tags/items/straw`, `tags/items/ropes`,
  `tags/items/flower_box_plantable` (both mushroom colonies),
  `tags/blocks/hang_from_ropes` (rope, tomatoes),
  `tags/blocks/rope_support` and `tags/blocks/water_holder` (basket).

### Moonlight 2.16.34

`data/moonlight/moonlight/soft_fluids/milk.json` lists
`farmersdelight:milk_bottle` among the bottle-capacity milk containers. This is
the library layer under the Supplementaries fluid entries above. One line, no
gameplay change beyond the bottle working as a milk container.

### Tinkers' Construct 3.11.2.166

Two integrations, both conditional:

- `data/tconstruct/recipes/compat/wheat_dough.json` — a **casting-table recipe**
  producing `farmersdelight:wheat_dough` from Wheat plus 250 mB of
  `#mantle:water`, 50-tick cooling, cast consumed. Gated on
  `forge:item_exists` for the item, which is satisfied here, so **this recipe is
  live** and is an additional route to a Farmer's Delight item.
- `farmersdelight:iron_knife` is listed in
  `tags/items/melting/iron/tools_costing_1.json`, so it melts down for one
  ingot's worth of iron in a Smeltery. The gold, diamond and netherite melting
  tags also name Farmer's Delight items.

### Sophisticated Backpacks 3.24.63.2049

`data/sophisticatedbackpacks/registry/compat/farmersdelight/block_tools.json`
and `entity_tools.json`. The first registers `farmersdelight:cutting_board` as
operable by the backpack's Tool Swapper upgrade with knives
(`forge:tools/knives`), axes, pickaxes, shovels and shears. The second makes the
backpack auto-swap to a knife (`forge:tools/knives`) when interacting with any
animal — which is how knife scavenging is triggered. Both are bare tag entries
keyed to the **Forge** tag with no ToolAction alternative, so Dungeon's Delight
cleavers do not trigger the auto-swap. Swapping to one by hand still cuts
normally.

### Realm RPG: Quests 0.1.1

Nine quest item tags name Farmer's Delight items as objectives or ingredients:
`cook/food_simple` (mixed salad, barbecue stick, stuffed potato, egg sandwich),
`cook/food_medium` (bacon sandwich, mutton wrap, hamburger, kelp roll, bacon and
eggs, fruit salad), `cook/food_advanced` (shepherd's pie, apple pie, sweet berry
cheesecake, chocolate pie, melon popsicle, roasted mutton chops, steak and
potatoes, grilled salmon), `cook/salad`, `cook/pot` (cooking pot),
`cook/cutting` (iron knife), `cook/soup_ingredients` (onion), `cook/old/making_cake`
and `angler/fishing_net` (`farmersdelight:rope`). All entries are written
`{"required": false}`. Farmer's Delight food is quest content here.

### Beautiful Enchanted Books 6.0.0

Ships `assets/farmersdelight/models/item/enchanted_book/backstabbing.json` and
its texture — a themed enchanted-book model for Farmer's Delight's
`backstabbing` enchantment. Cosmetic, client-side, no data.

### Sky Villages 1.0.4

`data/skyvillages/worldgen/template_pool/skyvillage_houses.json` contains three
elements pointing at `skyvillages:farmersdelight/sky_village_farmersdelight_farm_{0,1,2}`,
weight 50 each out of a 1,280 total for that pool (11.7 %).

> **Defect: missing structure templates.** The Sky Villages jar contains 66
> entries and **no path containing `farmersdelight` at all**. Its
> `data/skyvillages/structures/` directory is flat — `farm_1.nbt`, `house_1.nbt`
> and so on — with no `farmersdelight/` subdirectory. The three pool elements
> reference NBT that does not ship. Unlike every other cross-mod reference on
> this list, they carry **no `mod_loaded` condition**, so they are not
> conditionally-disabled content; they are dangling references. No error appears
> in the current `latest.log`, because pool element templates are resolved when
> a structure actually generates rather than at boot. Whether a sky village
> rolling one of those three elements fails or silently skips it was not
> observed here and is **not documented**.

### Checked and ruled out

Every one of the remaining 138 jars was scanned by full entry list plus
decompressed byte scan, including nested jar-in-jar, with **zero** occurrences
of `farmersdelight` or `vectorwing`. That includes every mod that might
plausibly have been expected to integrate:

| Mod | Result |
|---|---|
| `aquaculture` 2.5.7 | no reference — no fish are cuttable on the cutting board |
| `alexsmobs` 1.22.9 | none of its own; the entire link is `alexsdelight` |
| `apotheosis`, `ApothicAttributes` | no reference |
| `iceandfire` 2.1.13, `alexscaves` 2.0.2 | no reference |
| `irons_spellbooks` 3.16.2 and its add-ons | no reference |
| `jei` 15.20.0.112 | no reference in the jar; Farmer's Delight and Dungeon's Delight each ship their own JEI plugin instead |
| `terralith` 2.5.4, `dungeons_enhanced`, `dungeons-and-taverns` | no reference; no Farmer's Delight crops or loot injected |
| `lootintegrations` 4.7 | no reference; does not touch Farmer's Delight chest loot |
| `curios` 5.14.1, `relics`, `artifacts` | no reference |
| ~128 others | no `farmersdelight` or `vectorwing` byte anywhere |

Farmer's Delight's own chest-loot injection (`generateFDChestLoot = true`,
14 `add_loot_*` global loot modifiers) and its village integration
(`generateVillageCompostHeaps`, `generateFDCropsOnVillageFarms`, both `true`)
are the parent mod's own behaviour, not an add-on's, and are unmodified here.

The blind spot in this method is the same as always: a mod that keys off a tag
or a class hierarchy rather than the literal string — anything acting on "all
foods" or "all crops" — would affect Farmer's Delight content without naming it,
and a byte scan cannot see that.

## Add-ons that exist but are NOT installed

For reference when weighing pack additions. Farmer's Delight has the largest
add-on ecosystem of any mod on this server. The list below is what a Modrinth
and CurseForge search for 1.20.1 Forge returns, not an exhaustive census, and
**none of it is installed here**.

Availability column: **verified** means the Modrinth version endpoint was
queried with `loaders=["forge"]` *and* `game_versions=["1.20.1"]` together,
which is the only thing that proves the combination — a project's top-level
`loaders` and `game_versions` arrays are unions across all its files and will
falsely imply Forge 1.20.1. **facet** means it appeared under the Forge + 1.20.1
search facets but the individual file was not opened. **CF** means it was read
off a CurseForge project page.

### Core expansions and themed cuisines

| Add-on | Author | What it does | 1.20.1 Forge |
|---|---|---|---|
| Delightful | brnbrd | The large configurable expansion — new foods plus compat hooks into many other mods | verified |
| Nether's Delight | Umpaz | Nether cooking: hoglin meat, blackstone stove, propelplant | verified |
| My Nether's Delight | SoyTutta | A separate, larger Nether food add-on — a different mod, not a rename | verified |
| End's Delight | FoggyHillside | End dishes built on chorus fruit and the dragon egg | verified |
| Ender's Delight | ax3dgaming1 | A different, smaller End-themed add-on | verified |
| Miner's Delight | SoyTutta | Mining and underground foods and tools (CurseForge slug `miners-delight-plus`) | verified |
| Ocean's Delight | Scouter567 | Ocean-themed culinary content | verified |
| Oceanic Delight | DariusZeBaguette | Ocean foods and aquatic plants; distinct from Ocean's Delight | facet |
| Silent's Delight | Scouter567 | Deep Dark and warden-themed dishes | verified |
| Farmer's Respite | ProbablyEyes | Tea and coffee — kettles, brewing, caffeine effects | verified |
| Brewin' And Chewin' | ProbablyEyes | Keg fermenting: liquors, cheese, fudge, and coaster displays | verified |
| Cultural Delights | Baisylia | World-cuisine foods, new crops and cooking blocks | verified |
| Corn Delight | Syameimaru_Zheng | Corn crop and corn dishes | verified |
| Vintage Delight | ribss498 | Pickling, cheese and extra farming | verified |
| Rustic Delight | phantomwing | Pancakes, cotton, coffee, bell peppers, fried foods | verified |
| More Delight | Axperty | Extra meals, knives and ingredients | verified |
| Cuisine Delight | lcy0x1 | Freeform plating with nutrition bonuses on top of FD cooking | verified |
| Crabber's Delight | AlabasterLeking | Crab trapping and coastal foods | verified |
| Fright's Delight | ChefMooon | Horror dishes made from hostile mob drops | verified |
| Roll Delight | matthewrat213 | Sushi, as an actual FD add-on | verified |

### Cross-mod bridges

| Add-on | Author | What it does | 1.20.1 Forge |
|---|---|---|---|
| Create: Central Kitchen | MarbleGateKeeper | Automates FD pots and cutting boards with Create, incl. Mechanical Arm support | verified |
| Create Slice & Dice | possible_triangle | Makes FD recipes work under Create's mechanical processing | verified |
| Delightful Creators | Flomik | Bridges Create machinery to FD processing | verified |
| Compat Delight | FixerLink | Umbrella compat mod covering ~50 partner mods, config-gated | verified |
| Farmer's Delight Compat | Kanadeyoru | De-duplicates overlapping items and blocks across FD add-ons | facet |
| Abnormals Delight | TeamAbnormals | Per-wood cabinets, deer and duck cuts for the Abnormals suite | verified |
| Farmer's (Delight) Croptopia | ACCBDD | Croptopia crops usable in FD cooking | verified |
| Croptopia Delight | ropyxa | Alternative Croptopia ↔ FD recipe integration | verified |
| Aquaculture Delight | NoCube | Aquaculture 2 fish turned into FD dishes — **relevant here, `aquaculture` 2.5.7 is installed** | verified |
| Tinkers Construct Delight | NoCube | Tinkers' knives and dishes — **relevant here, `TConstruct` is installed** | verified |
| L_Ender's Cataclysm Delight | Chaolux | 50+ dishes tied to Cataclysm's dungeon bosses — **relevant here, `cataclysm` is installed** | verified |
| Ice and Fire Delight | Donne431 (Modrinth) | Ice and Fire × FD — **relevant here, `iceandfire` 2.1.13 is installed**. A same-named CurseForge project by scarlet_dragonic is a *different* mod | facet |
| Alex's Mobs Delight | bf_meow | A second, larger Alex's Mobs bridge — ~100 foods, 9 tools. **Would contend with the installed Alex's Delight over the same content** | CF |
| Twilight's Flavor & Delight | lcy0x1 | Twilight Forest foods and desserts | verified |
| Ars Nouveau's Flavors & Delight | lcy0x1 | 49+ foods from Ars Nouveau ingredients | verified |
| Aether's Delight | zjjohn121110 | The Aether × FD | verified |
| [NoCube's] Undergarden Delight | NoCube | Undergarden ingredients in FD, vanilla style | verified |
| Nature's Delight | TeamHibiscus | Nature's Spirit woods and biomes | verified |
| Compat O' Plenty | KreloX | Biomes O' Plenty × FD (plus Quark, Twigs, Abnormals) | verified |
| Every Compat (Wood Good) | MehVahdJukaar | Generates FD cabinets and cutting boards for every modded wood | verified |
| Vampire's Delight | GridExpert | Vampirism × FD, garlic-focused | verified |
| Goety's Delight | baizeli | Goety × FD | verified |
| TofuDelight | baguchi | TofuCraft Reload × FD | verified |
| Galospheric Delight | CosmoCat | Galosphere × FD | verified |
| Epicfight: Farmer's Delight Compat | teanekosan | Gives FD knives Epic Fight weapon data | verified |
| Project MMO: Farmer's Delight Compat | Silvertide | FD cooking blocks grant PMMO experience | verified |

### Tooling and presentation

| Add-on | Author | What it does | 1.20.1 Forge |
|---|---|---|---|
| Autochef's Delight | Snownee | Performance and QoL: stacked cooking, faster FD recipe matching | verified |
| EMI Farmer's Delight Reforged | Lexeef | EMI recipe-viewer support for FD cooking and cutting | verified |
| Display Delight | jkvin114 | Renders every FD food item in 3D when placed | verified |
| Storage Delight / Crate Delight | Axperty | Kitchen furniture and crates matching FD's look (two sibling mods) | verified |
| Delight Lib | Axperty | Library for authoring FD add-ons across loaders and versions | verified |
| Culinary Construct | TheIllusiveC4 | Custom sandwiches and stews from arbitrary foods; commonly paired with FD rather than a true add-on | verified |

### Name traps

- **End's Delight** (FoggyHillside) and **Ender's Delight** (ax3dgaming1) are
  different mods. So are **Nether's Delight** (Umpaz) and **My Nether's
  Delight** (SoyTutta). Neither pair is a rename.
- **Alex's Delight** (`alexsdelight`, Baisylia / NCP Bails), which *is*
  installed here, and **Alex's Mobs Delight** (bf_meow), which is not, both
  claim Alex's Mobs × Farmer's Delight compatibility. Installing both would put
  two mods in contention over the same Alex's Mobs loot tables.
- The Alex's Caves space has three competing bridges — **Cave Delight**
  (TheValiantSquidward), **Caves Delight** (sieyva) and **Alex's Caves
  Delight** (scarlet_dragonic). `alexscaves` 2.0.2 is installed here, so all
  three are candidates, and they overlap heavily with each other.
- The **"Let's Do" series** (satisfyu, with Cristelknight on the shared *Let's
  Do API*) — Vinery, Bakery, Meadow, Candlelight, Brewery, HerbalBrews — is a
  parallel food ecosystem with its own API that ships Farmer's Delight
  cross-compat rather than depending on it. Not add-ons.
- **Sushi Go Crafting** (buuz135) is standalone, not an FD add-on.

### Checked and not found

**Farmer's Knives** (ianm1647) exists for 1.20.1 but publishes Fabric, Quilt and
NeoForge only — there is no 1.20.1 Forge build. No project exists under the
names Mystical Delight, Legendary Delight, Mob's Delight, Homestead, Delightful
Farming, Sully's Mod Delight or Farmer's Delight Integrations; people saying the
last one usually mean *Compat Delight* or *Farmer's Delight Compat*. There is no
standalone FD ↔ AppleSkin bridge — nutrition tooltips live inside *Delightful*
and *Cuisine Delight*.

## Sources

- **`forge-dungeonsdelight-1.20.1-1.3.0.jar`** — pulled from the live server's
  `/mods` via the Pterodactyl client API, unzipped and decompiled with jadx.
  Registry IDs from the `register("…")` calls in `DDItems`, `DDBlocks`,
  `DDEffects`, `DDEnchantments`, `DDEntities`, `TFItems` and `ADItems`; food
  values from `DDProperties` and `INProperties`; display names from
  `assets/dungeonsdelight/lang/en_us.json`; recipes, tags, loot modifiers and
  worldgen read from the `data/` tree verbatim. Weapon stats come from `DDItems`
  lines 152–172, the custom tier in `DDMaterials`, and the durability and rarity
  constants in `DDProperties`; the throw mechanic from
  `CleaverItem.releaseUsing`/`applyEffects`, `CleaverEntity` and `DDSounds`.
  Vanilla tier constants were not taken from memory — they were cross-checked
  against the independently derived knife table in
  [blocks-items.md](blocks-items.md#knife-stats), which resolves to the same
  per-tier bonuses, speeds and enchantabilities. Enchantment SRG names were
  anchored at both ends of the consecutive field block rather than assumed:
  `f_44977_` is named `sharpness` by a preserved local in
  `CleaverItem.applyEffects`, `f_44981_` is named `fireAspectLevel` in Farmer's
  Delight's `SkilletItem`, and `f_44987_` is the argument to `ApplyBonusCount`
  in block loot, which is Fortune by definition.
- **`FarmersDelight-1.20.1-1.3.2.jar`** — same pipeline, for the parent tags the
  add-ons join, its 106 cutting-board recipes, `ModTags`, `ItemUtils`,
  `KnifeItem`, `ToolActionIngredient`, `CuttingBoardRecipe.Serializer`,
  `CuttingBoardBlockEntity` and the parent global loot modifier list.
  Tool eligibility was determined from the **deserialisation path**, not from
  tag membership: `CuttingBoardRecipe.Serializer` passes the `tool` field to
  `Ingredient.fromJson`, which treats a JSON array as match-any, and every
  recipe's `tool` array was parsed to confirm the action/tag pairing (106 of
  106, one exception noted inline). An earlier draft of this page compared tag
  membership alone and wrongly concluded that Dungeon's Delight cleavers could
  not use the cutting board; that claim is retracted and the correct rule is in
  [How Farmer's Delight decides something is a tool](#how-farmers-delight-decides-something-is-a-tool).
- **`alexsdelight-1.5.jar`** — recipe types and counts read from its `data/`
  tree; the rest of its analysis is in
  [../alexs-mobs/addons.md](../alexs-mobs/addons.md) and is not restated or
  contradicted here.
- **Jar-wide content sweep** — all 148 jars named in `manifest.json` downloaded
  from `/mods` via `files/download` (signed-URL two-step, explicit User-Agent),
  each scanned for `data/farmersdelight/**`, `assets/farmersdelight/**`, any
  path naming `farmersdelight`, and the byte strings `farmersdelight` and
  `vectorwing`, then deleted. 148/148 succeeded, 0 retries needed, 0 failures.
  Per-jar findings written to `/tmp/fd/refs/<jar>.txt` in the session
  scratchpad. `Supplementaries` and `Sky Villages` were re-fetched afterwards to
  read the individual files.
- **Live server** — `/config/dungeonsdelight-config.toml`,
  `/config/farmersdelight-common.toml`, `/config/farmersdelight-client.toml`,
  `/logs/latest.log` (mod version list, the mixin `minVersion` warning, the
  Monster Yam loot warning, the Alex's Delight recipe failure), and the full
  `/mods` listing.
- CurseForge and Modrinth project pages for provenance, licensing and the
  not-installed list.

Where a third-party wiki and the code disagreed, the code won and the difference
is called out inline.
