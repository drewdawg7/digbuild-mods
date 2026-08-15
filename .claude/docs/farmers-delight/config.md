<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Configuration

## Summary: server vs. stock

**There are none.** The server runs **all 23 options across both files at their
mod defaults** — 20 in `config/farmersdelight-common.toml` and 3 in
`config/farmersdelight-client.toml`. Not one value, list entry or list order
differs.

| Deviation | Option | Stock | This server |
|---|---|---|---|
| — | *none* | — | — |

Any Farmer's Delight behaviour players report on this server is stock mod
behaviour, not a server tuning decision. The full option-by-option table follows
anyway, because "what could be changed" is the useful half of that answer.

### How this was verified

Mechanically, not by eye. Every `define` / `defineInRange` / `defineList` call
in the static initialiser of `vectorwing/farmersdelight/common/Configuration.java`
was parsed out of the decompiled jar, its literal default extracted from the
**argument passed to the builder call** — never from a static field initialiser,
which is the trap that produces phantom deviations — and the resulting 23-key
map compared against the two live TOMLs parsed the same way. Result: 23 keys on
each side, no key missing from either, no value mismatch, both list options
identical in contents and order.

Cross-checked a second way: `Configuration.java` on the upstream `1.20` branch
of [`vectorwing/FarmersDelight`](https://github.com/vectorwing/FarmersDelight)
— which carries `mod_version=1.3.2`, matching the installed jar exactly — is
character-identical to the decompiled copy in every `define*` call. The defaults
below are therefore confirmed against clean source, not only against jadx
output.

Because both files are stock, the "Server" and "Stock default" columns are
merged into one **Value** column throughout.

## Files

| Path | Scope | Options | Notes |
|---|---|---:|---|
| `/config/farmersdelight-common.toml` | server | 20 | six sections, one nested |
| `/config/farmersdelight-client.toml` | client | 3 | no sections; three bare top-level keys, which is what the code builds |
| `/config/dungeonsdelight-config.toml` | server | — | the add-on's own file, covered in [addons.md](addons.md) |

Alex's Delight ships no config file. There is no `farmersdelight-server.toml`;
this mod puts all gameplay options in the common spec.

The client file's lack of `[section]` headers is not damage — `CLIENT_BUILDER`
never calls `push()`, so the three keys are correctly at the root.

## `[settings]`

4 options.

| Option | Value | What it does | Player-facing? |
|---|---|---|---|
| `enableFarmerFDTrades` | `true` | Novice and Apprentice Farmer villagers get a chance to buy this mod's crops. | **yes** — changes villager trade pools |
| `enableWanderingTraderFDTrades` | `true` | The Wandering Trader gets a chance to sell this mod's seeds and plantables. | **yes** — the main renewable route to Cabbage, Tomato and Rice seeds without finding the wild patches |
| `enableRopeReeling` | `true` | Sneak-use with an empty hand on a rope reels it back up, bottom to top. | **yes** — a build/traversal convenience |
| `canvasSignDarkBackgroundList` | `["gray", "purple", "blue", "brown", "green", "red", "black"]` | Dye colours that default a Canvas Sign to white text when placed, because the background is too dark for black text. | cosmetic only |

## `[farming]`

3 options.

| Option | Value | What it does | Player-facing? |
|---|---|---|---|
| `richSoilBoostChance` | `0.2` | Per-tick chance that Rich Soil gives a crop planted on it a free bone-meal tick. Range `0.0`–`1.0`; `0.0` disables. | **yes** — this is the entire point of Rich Soil, and the number the farming page should quote |
| `enableTomatoVineClimbingTaggedRopes` | `true` | Tomato crops can climb any rope in the `farmersdelight:ropes` tag, not just this mod's Rope. Converts climbed blocks into `defaultTomatoVineRope`. | **yes** — matters when another mod's rope is in the tag |
| `defaultTomatoVineRope` | `"farmersdelight:rope"` | Which rope block a broken Tomato Vine leaves behind. | consequence of the above |

## `[crafting]`

3 options.

| Option | Value | What it does | Player-facing? |
|---|---|---|---|
| `enableCookingPotRecipeBook` | `true` | The Cooking Pot UI carries a recipe book, like a Crafting Table or Furnace, with the `meals` / `drinks` / `misc` tabs each `farmersdelight:cooking` recipe declares. | **yes** — client UI, but server-side config |
| `enableVanillaCropCrates` | `true` | Makes the 3×3 storage crates for vanilla crops (carrot, potato, beetroot) craftable. This is the flag behind the three `forge:conditional` recipes gated on `farmersdelight:vanilla_crates_enabled`. | **yes** — three recipes appear or vanish |
| `cuttingBoardFortuneBonus` | `0.1` | Each level of Fortune on the cutting tool adds this much to the `chance` of every rare Cutting Board result. Range `0.0`–`1.0`; `0.0` disables. | **yes** — Fortune III on a knife adds +30 percentage points to rare cutting drops |

## `[overrides]`

Vanilla item overrides. 4 options at this level plus a nested subsection.

| Option | Value | What it does | Player-facing? |
|---|---|---|---|
| `enableVanillaSoupExtraEffects` | `true` | Minecraft's own soups and stews grant Nourishment when eaten, the same as this mod's meals. | **yes** — silently changes vanilla food behaviour |
| `enableRabbitStewJumpBoost` | `true` | Rabbit Stew additionally grants Jump Boost. | **yes** — same |
| `enablePumpkinPieSneakToPlace` | `false` | **The one option shipped `false`.** When on, placing a Pumpkin Pie as a block requires sneaking. Off means a Pumpkin Pie places on a normal use-click, which can surprise players trying to eat one. | **yes** |
| `enableCuttingBoardDispenserBehavior` | `true` | A Dispenser facing a Cutting Board operates it with the tool it holds. | **yes** — the basis of automated cutting |

### `[overrides.stack_size]`

2 options.

| Option | Value | What it does | Player-facing? |
|---|---|---|---|
| `enableStackableSoupItems` | `true` | Any `BowlFoodItem` named in `soupItemList` becomes stackable to 16, matching this mod's meals. | **yes** — inventory-level change to vanilla items |
| `soupItemList` | `["minecraft:mushroom_stew", "minecraft:beetroot_soup", "minecraft:rabbit_stew"]` | The targeted items. They must extend `BowlFoodItem` in code to be affected, so adding an arbitrary modded soup here does nothing unless it does. | consequence of the above |

## `[world]`

3 options. All three take effect at chunk generation, so flipping any of them
only affects newly generated terrain.

| Option | Value | What it does | Player-facing? |
|---|---|---|---|
| `generateFDChestLoot` | `true` | Adds this mod's loot pools to chest loot across the game — ropes, crops, tools. This is the gate on the 14 `add_loot_table` global loot modifiers and their 14 `fd_*` chest tables. | **yes** — see [loot-and-worldgen.md](loot-and-worldgen.md) |
| `generateVillageCompostHeaps` | `true` | Compost Heaps (Organic Compost piles) sometimes generate in villages, from the five `*_compost_pile.nbt` structures. | **yes** — new-chunk villages only |
| `generateFDCropsOnVillageFarms` | `true` | This mod's crops sometimes replace standard crops in village farm plots. | **yes** — the earliest reliable source of Cabbage, Onion and Tomato seeds |

## `[debug]`

1 option. Labelled "Not meant for gameplay" by the mod, but it is on by default
and does affect gameplay.

| Option | Value | What it does | Player-facing? |
|---|---|---|---|
| `enableTomatoRopePermanence` | `true` | A Tomato Vine hanging on rope force-places a Rope block when broken. The mod's own comment notes this makes `/setblock` on that position fail at first, and recommends disabling only if it blocks creative or command editing. | mostly builder-facing; leave on |

## Client file

3 options, all cosmetic, all client-side. They are listed here because the file
is present on the server install; the values a given player sees come from their
own client.

| Option | Value | What it does |
|---|---|---|
| `enableNourishmentHungerOverlay` | `true` | Gilded overlay on the food meter while Nourishment is active. |
| `enableComfortHealthOverlay` | `true` | Scrolling overlay on the health meter while Comfort is active. |
| `enableFoodEffectTooltip` | `true` | Food items show a tooltip listing the effects they grant. Applies to Minecraft's foods as well as this mod's — the main reason a player can read nutrition at all without JEI. |

## Options that change player-facing behaviour

Sixteen of the twenty common options change something a player can observe. The
seven with the widest blast radius, if this server ever does tune them:

| Option | Why it matters |
|---|---|
| `enableWanderingTraderFDTrades` | the renewable seed source |
| `generateFDCropsOnVillageFarms` | the early seed source |
| `generateFDChestLoot` | 14 vanilla chest tables gain pools |
| `richSoilBoostChance` | crop growth rate on the mod's premium soil |
| `cuttingBoardFortuneBonus` | scales every rare Cutting Board drop with Fortune |
| `enableVanillaSoupExtraEffects` | changes vanilla soups' effects |
| `enableStackableSoupItems` | changes vanilla soups' stack size |

The remaining four — `canvasSignDarkBackgroundList`, `defaultTomatoVineRope`,
`soupItemList` and `enableTomatoRopePermanence` — are either cosmetic or
consequences of an option above.
