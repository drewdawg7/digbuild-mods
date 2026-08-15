<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Cooking

Everything the mod adds for turning raw ingredients into food: the five stations, the heat
system they share, and every recipe in the mod's `data/` tree.

IDs are the real registry names, read from the `register("…")` calls in `ModBlocks`,
`ModItems`, `ModRecipeTypes` and `ModRecipeSerializers`, not from the Java field names.

## The stations

`ModBlockEntityTypes` registers eight block entities. Five of them are workstations; the other
three (`cabinet`, `canvas_sign`, `hanging_canvas_sign`) are storage and decoration.

| Block | Registry ID | What it does | Needs heat |
|---|---|---|---|
| Cooking Pot | `farmersdelight:cooking_pot` | 6-input recipe crafting into meals | Yes |
| Skillet | `farmersdelight:skillet` | Single-item campfire cooking, in-world or held | Yes (in-world) |
| Stove | `farmersdelight:stove` | Six items grilled at once, and a heat source itself | It *is* the heat |
| Cutting Board | `farmersdelight:cutting_board` | Tool-driven processing of one item at a time | No |
| Basket | `farmersdelight:wooden_basket`, `farmersdelight:bamboo_basket` | 27-slot hopper that collects dropped items | No |

Two more blocks are storage rather than stations but sit in the same workflow: the eleven
**Cabinets** (`farmersdelight:<wood>_cabinet`, 27 slots each, one block entity type) and the
**feast** and **pie** blocks that finished food is served from.

## Heat

Every heated station shares one interface, `HeatableBlockEntity`, and one rule.

A station is heated when the block **directly beneath it** is in the block tag
`#farmersdelight:heat_sources`. If that block has a `lit` blockstate property, it must be lit;
if it has no such property it always counts.

`#farmersdelight:heat_sources` as shipped by the mod:

| Entry | Has `lit` state | Notes |
|---|---|---|
| `minecraft:magma_block` | no | always hot |
| `minecraft:lava_cauldron` | no | always hot |
| `farmersdelight:stove` | **yes** | must be lit |
| `#farmersdelight:tray_heat_sources` | — | nested tag, below |

`#farmersdelight:tray_heat_sources`:

| Entry | Has `lit` state | Notes |
|---|---|---|
| `minecraft:lava` | no | source or flowing |
| `#minecraft:campfires` | **yes** | Campfire and Soul Campfire; must be lit |
| `#minecraft:fire` | no | Fire and Soul Fire |

**There is no fuel anywhere in this system.** A lit campfire or stove under a pot cooks
indefinitely; nothing is consumed but the ingredients.

**Heat conducts through one block.** If the station does not require direct heat — and neither
the Cooking Pot nor the Skillet does; `requiresDirectHeat()` is never overridden in the mod — a
block from `#farmersdelight:heat_conductors` directly beneath it will pass heat up from a heat
source two blocks down. The tag holds `minecraft:hopper` and, optionally, `create:chute`
(Create is not installed on this server, so the entry is inert). This is what makes a
hopper-fed automated cooking pot possible: campfire, hopper, pot.

**Tray legs are cosmetic, and they are not the same tag.** The Cooking Pot's `support`
blockstate and the Skillet's `support` boolean are set from `#farmersdelight:tray_heat_sources`
only — the subset with an open flame. A pot on a stove or a magma block gets no tray; it is
still heated. Sneak-clicking a Cooking Pot with an empty hand toggles it between the hanging
handle and the tray/none state, which is purely visual.

**Add-ons extend the tags.** Dungeons Delight ships its own
`data/farmersdelight/tags/blocks/heat_sources.json` and `tray_heat_sources.json`, neither with
`"replace": true`, so they **merge additively** on top of the lists above. What counts as heat
on this server is therefore FD's contents plus `dungeonsdelight:dungeon_stove` (heat source) and
`dungeonsdelight:living_fire` (tray heat source). Its file also lists
`netherexp:treacherous_candle` with `"required": false`; that mod is not installed, so the entry
is skipped gracefully and is inert — nothing to chase. See `addons.md`.

## Cooking Pot

**Crafted** on a crafting table:

```
b S b     b = minecraft:brick        S = minecraft:wooden_shovel
i W i     i = #forge:ingots/iron     W = #forge:buckets/water
i i i
```

The water bucket is a container ingredient and comes back.

### Inventory layout

Nine slots in one `ItemStackHandler`:

| Index | Slot | Behaviour |
|---|---|---|
| 0–5 | ingredient grid, 2 rows × 3 columns | any items; the recipe matcher is order-independent |
| 6 | meal display, top right | **read-only in the GUI** — cannot be inserted into or taken from |
| 7 | container input, bottom middle | shows a Bowl ghost icon; accepts the current recipe's container |
| 8 | output, bottom right | finished servings; taking from here awards the stored XP |

### How it runs

1. Put up to six ingredients in the grid. Each grid slot contributes **one item per craft**
   regardless of stack size, so a stack of 64 carrots in one slot is 64 crafts' worth of that
   one ingredient — not 64 carrots in a single meal.
2. Heat the pot. `cookTime` advances one tick per game tick while heated *and* a recipe
   matches; it falls back at **two ticks per tick** whenever heat is lost or the recipe stops
   matching, so an interrupted cook loses progress twice as fast as it gained it.
3. On completion the result lands in slot 6, one item is consumed from each occupied grid slot,
   and any ingredient with a crafting remainder (bucket, bottle, bowl) is **spat out as a
   dropped item** from the pot's left side rather than returned to a slot.
4. What happens next depends on whether the meal has a container.

### Containers, and eating from the pot

A recipe's container is its explicit `"container"` field if present, otherwise the crafting
remainder of its result item. Bowl meals and bottled drinks therefore get one automatically.

- **Meal has no container** (only Dumplings and Cabbage Rolls): it moves straight from slot 6
  to the output slot on the next tick. Nothing else is needed.
- **Meal has a container**: nothing leaves slot 6 until a matching container appears. Two ways
  to supply one:
  - Put bowls (or bottles, or a Pumpkin for Stuffed Pumpkin) in slot 7. Each tick the pot
    pairs one container with one serving and moves it to the output slot.
  - Right-click the pot **holding the container item**. That hands you one serving directly and
    consumes one container. This is the "eat from the pot" path, and it only works with the
    exact container the recipe declares — `isContainerValid` compares against the stored
    container stack, so a bowl will not extract Hot Cocoa and a bottle will not extract stew.

Right-clicking with an empty hand (not sneaking) opens the GUI. Right-clicking with any item
that is not the container also just opens the GUI.

### Output stacking and capacity

Slot 6 is a plain handler slot with a limit of 64, and `canCook` accepts a new craft as long as
the stored count stays within that limit. The meals themselves stack to 16 (`bowlFoodItem` and
`drinkItem` both set `maxStackSize(16)`), so **the pot buffers up to 64 servings internally**
while the output slot only ever holds 16. The durability-style bar on a Cooking Pot item is
scaled against 64 for the same reason.

### Breaking the pot, and XP

Breaking the pot drops slots 0–5, 7 and 8 as items, but **slot 6 travels with the pot** —
the meal, the container stack and the custom name are written into the item's
`BlockEntityTag`, so a pot full of stew can be picked up and carried. A pot item with a meal in
it also works in a crafting grid: the `farmersdelight:food_serving` special recipe takes a
filled pot plus one matching container anywhere in the grid and returns one serving, leaving
the pot behind with one fewer.

XP accumulates per recipe crafted and is paid out when a player takes from the output slot, or
when the pot block is broken.

### Automation

The pot exposes two different item handlers by side:

| Side | Insert | Extract |
|---|---|---|
| Top (or no side) | slots 0–5, ingredients | slots 0–5 |
| Any other side, including bottom | slot 7, containers | slot 8, finished meals |

A comparator reads the whole nine-slot inventory.

### Recipe book

`enableCookingPotRecipeBook` is `true` on this server, so the pot's GUI carries a recipe book
with three tabs — `meals`, `drinks`, `misc` — chosen per recipe by its optional
`recipe_book_tab` field. Recipes with no tab, or an unrecognised one, still work; they log a
warning and appear untabbed. There is no server-side behaviour beyond that.

## Skillet

**Crafted** on a crafting table:

```
. # #     # = #forge:ingots/iron
. # #     / = minecraft:brick
/ . .
```

The Skillet is both a block and a weapon: 5 + iron-tier damage (7 total), −3.1 attack speed,
+1 knockback, iron durability, and it takes weapon enchantments except Sweeping Edge. Fire
Aspect on it is functional, not decorative — see below.

### Placing it

The Skillet item only places as a block when the player is **sneaking**. Right-clicking without
sneaking starts handheld cooking instead. Placing it copies the item stack, enchantments
included, into the block entity, and breaking it gives that exact item back.

### In-world cooking

The placed Skillet holds one slot and cooks **campfire recipes only** (`minecraft:campfire_cooking`).

- Right-click with a valid ingredient to add it; it accepts a whole stack into the slot but
  cooks one item at a time.
- Right-click with an empty hand to take the contents back.
- An invalid item prints *"This item cannot be cooked in a skillet."* Adding food while the
  Skillet is waterlogged prints an underwater message and refuses.
- The finished item is **ejected as a dropped entity** to the Skillet's right side; there is no
  output slot. Put a hopper or a Basket under it to collect.
- Waterlogging a Skillet that has contents dumps them on the ground.
- Losing heat rewinds progress at two ticks per tick, same as the pot.

### Cooking time

`SkilletBlock.getSkilletCookingTime(recipeTicks, fireAspectLevel)`:

```
seconds   = recipeTicks / 20
reduction = 0.2 − 0.05 × fireAspectLevel
result    = floor(seconds × reduction) × 20 ticks
return clamp(result, 60 ticks, recipeTicks)
```

Every campfire recipe in Farmer's Delight and in vanilla is 600 ticks, so in practice:

| Fire Aspect | Ticks | Seconds | vs. a campfire (30 s) |
|---|---|---|---|
| none | 120 | **6 s** | 5× faster |
| I | 80 | **4 s** | 7.5× faster |
| II | 60 | **3 s** | 10× faster |

60 ticks (3 s) is the floor — `MINIMUM_COOKING_TIME` — so Fire Aspect above II buys nothing on
a 600-tick recipe.

### Cooking while held

Right-click (not sneaking) while holding the Skillet, with the food in the **other hand**, and
standing within a 3×3×3 cube of any `#farmersdelight:heat_sources` block — or while on fire.
The skillet takes one item from the off-hand, stores it in NBT under `Cooking`, and becomes a
use-item with the duration from the same formula above. Release early and the raw item is
returned to your inventory; hold to the end and the cooked item goes to your inventory (or
drops at your feet if it is full).

Details a player will trip over:

- Both hands are involved. The Skillet must be in the hand you right-click with, the food in
  the other.
- Nothing happens without a nearby heat source; you get *"Hold food in your other hand…"* if the
  off-hand item has no campfire recipe, and nothing at all if there is no heat.
- Being **underwater** (eyes submerged) aborts with an underwater message.
- The item's durability bar is repurposed as an orange cooking progress bar while `Cooking` is
  set.
- The food flips in the pan every 12 ticks; that is animation only.

## Stove

**Crafted** on a crafting table:

```
i i i     i = #forge:ingots/iron
B . B     B = minecraft:bricks
B C B     C = minecraft:campfire
```

The Stove is the mod's own heat source and its own grill. It is placed **lit** and stays lit
forever — no fuel slot, no fuel item, nothing consumed.

- **Ignite** with Flint and Steel or a Fire Charge. **Extinguish** with anything that can
  perform `shovel_dig`, or any item in `#forge:buckets/water`.
- **Six items at once**, one per slot (`getInventorySlotCount()` = 6, slot limit 1), arranged in
  two rows of three on the top face. Right-click with food to add one item to the next empty
  slot. There is no GUI and no container item — you cannot make soup on a stove.
- It cooks **campfire recipes** and uses the recipe's own time, **unmodified**: 30 s for every
  vanilla and Farmer's Delight campfire recipe. The Stove is a capacity upgrade over a
  campfire, not a speed one.
- Results are **ejected upward as dropped items**.
- Extinguishing does not cancel progress instantly; each item cools at two ticks per tick.
- Standing on a lit stove deals 1 damage per tick from `farmersdelight:stove_burn` unless the
  entity is sneaking, fire-immune, or has Frost Walker.

**The one rule that catches everyone:** if anything covers the grilling area — the 10×10 centre
of the block face, `3..13` on X and Z, `0..1` on Y of the block above — the stove **drops all
its food on the ground** and refuses to accept more. A Cooking Pot or Skillet placed on top of
a stove does exactly that. Stack a pot on a stove for heat, or grill on it; never both.

## Cutting Board

**Crafted** on a crafting table:

```
/ # #     # = #minecraft:planks
/ # #     / = minecraft:stick
```

It needs a solid face or a sturdy centre beneath it and pops off if that support is removed.
One slot, no GUI, no heat.

### Using it

1. Right-click with the item to process. The board takes the **whole stack** you are holding
   (the slot limit is 64), and each cut consumes one. It reports *"x items remaining"* after
   each cut.
2. Right-click with the tool. The matching recipe's results are flung out to the board's left
   side, the tool loses 1 durability, and one input item is consumed.
3. Right-click with an empty hand to take back whatever is left.

Order matters, and this is the single most common way to get it wrong: **the "place item" check
runs before the "use tool" check.** If the board is empty, clicking it with a knife *places the
knife on the board*. The board must already hold the food before the tool does anything.

Failure messages tell you which half is wrong: *"This item cannot be processed on a cutting
board"* (no recipe for the stored item at all) versus *"This tool cannot process this item"* (a
recipe exists but not for the tool you are holding).

### Which tool cuts what

The tool is an ingredient like any other, and every recipe in the mod writes it as a two-entry
array: a `farmersdelight:tool_action` ingredient (matches anything whose item reports that
Forge `ToolAction`, so modded tools work automatically) plus a plain tag as a fallback.

| Action | Fallback tag | Recipes | Covers |
|---|---|---|---|
| `knife_dig` | `#forge:tools/knives` | 47 | meat into cuts/slices, produce into seeds and dye, cake and pies into slices, dough into pasta |
| `axe_strip` | `#minecraft:axes` | 22 | every log and wood into its stripped form **plus a Tree Bark** |
| `axe_dig` | `#minecraft:axes` | 13 | wooden furniture back into planks (75% each), baskets back into canvas |
| `hoe_dig` | `#minecraft:hoes` | 13 | chest boats and minecarts back into their two parts |
| `pickaxe_dig` | `#minecraft:pickaxes` | 6 | bricks, quartz, amethyst, stone and deepslate back into components |
| `shears_dig` | `#forge:shears` | 3 | leather armour, horse armour and saddles back into leather |
| `shovel_dig` | `#minecraft:shovels` | 2 | clay into clay balls, gravel into flint |

`knife_dig` is a Farmer's Delight action, not a Forge one; `KnifeItem.canPerformAction` returns
true for `knife_dig`, `knife_harvest`, `SHEARS_CARVE` and `SWORD_DIG`. Only knives report it, so
in practice a knife is the only thing that satisfies those 47 recipes. The knives are Flint,
Iron, Golden, Diamond and Netherite, listed identically in `#farmersdelight:tools/knives` and
`#forge:tools/knives`. Dungeons Delight merges `dungeonsdelight:stained_knife` and
`#dungeonsdelight:cleavers` into that tag additively, so those work too — see `addons.md`.

`#farmersdelight:straw_harvesters` is a **pure alias**: its only entry is
`#farmersdelight:tools/knives`. Harvesting straw and cutting on a board therefore accept exactly
the same set of tools; they are not two separate requirements.

### Chance results and Fortune

Results carry an optional `chance`. Each output rolls **once per item in its count**, so
`Yellow Dye ×2` at 50% is two independent coin flips, not one flip for both.

`cuttingBoardFortuneBonus` (**0.1** on this server, the mod default) is added to the roll
threshold per level of Fortune on the tool. Fortune III on a knife takes a 50% output to 80%
and makes anything at 70% or better certain. It applies to every chance result, not only rare
ones.

### Carved tools

Sneak-right-click an **empty** board with any `TieredItem`, Trident or Shears and the tool is
mounted on the board as decoration. While carved, the board accepts nothing and processes
nothing; take the tool off with an empty hand first. Items in
`#farmersdelight:flat_on_cutting_board` (Trident, Spyglass, and optional entries for mods not
installed here) render lying flat instead of upright — display only.

### Dispensers

`enableCuttingBoardDispenserBehavior` is `true` on this server. A dispenser aimed at a cutting
board uses the dispensed item as the cutting tool instead of dispensing it, via a mixin on
`DispenserBlock`. The board must already hold an item; the tool takes durability damage and is
destroyed at zero. There is no player, so no advancement and no chat feedback.

A comparator reads the stored stack as a fraction of the slot limit.

## Basket

**Crafted** on a crafting table (Wooden Basket shown; the Bamboo Basket swaps sticks for bamboo):

```
/ . /     # = farmersdelight:canvas
# . #     / = minecraft:stick
/ # /
```

Not a cooking station, but the collector that sits under one. It is a 27-slot container that
also behaves like a directional hopper for **item entities only**:

- It faces any of the six directions. Its pickup volume is its own block space **plus** the
  adjacent block in the direction it faces — so a downward-facing basket also catches items in
  the block below it, an upward-facing one in the block above, and so on.
- It also grabs any item entity that touches that volume directly, not only on its own tick.
- Items dropped by a Skillet, a Stove or a Cutting Board land in it.
- Transfer cooldown is **8 ticks (0.4 s)**.
- It does **not** pull from or push into other inventories — only item entities. It never
  pushes anything out.
- Redstone power disables it (`enabled` blockstate). A comparator reads it like a chest.
- Right-click opens a 27-slot chest-style GUI.

## Serving blocks

Large meals craft into placeable blocks rather than items.

**Feasts** (`#farmersdelight:feasts`) hold servings in a blockstate:

| Block | Servings | Leaves a container behind |
|---|---|---|
| `farmersdelight:roast_chicken_block` | 4 | yes |
| `farmersdelight:honey_glazed_ham_block` | 4 | yes |
| `farmersdelight:shepherds_pie_block` | 4 | yes |
| `farmersdelight:gleaming_salad_block` | 4 | yes — also emits light, 3 per remaining serving |
| `farmersdelight:stuffed_pumpkin_block` | 4 | no, vanishes when emptied |
| `farmersdelight:rice_roll_medley_block` | **8** | yes |

Right-click to take one serving. The serving items are `bowlFoodItem`s, so **you must be
holding a Bowl** — the block tells you which container it wants if you are not. Clicking a
zero-serving feast that leaves a container behind breaks it and drops that container.

**Pies** (`#farmersdelight:pies`) work differently: 4 bites, eaten directly off the block with
no container, *or* cut with a knife to pop out a slice item. Apple Pie, Chocolate Pie, Sweet
Berry Cheesecake and vanilla Pumpkin Pie are all pie blocks. A knife also cuts a placed vanilla
Cake into `farmersdelight:cake_slice`, one per bite.

## Nourishment

Almost every cooking-pot meal grants **Nourishment**, the mod's own effect. It does one thing:
each tick, it resets the player's *exhaustion* to zero unless natural regeneration is actively
burning saturation. In effect it freezes the hunger bar for its duration. Durations used:

| Constant | Ticks | Seconds |
|---|---|---|
| `BRIEF_DURATION` | 600 | 30 s |
| `SHORT_DURATION` | 1200 | 60 s |
| `MEDIUM_DURATION` | 3600 | 3 min |
| `LONG_DURATION` | 6000 | 5 min |

`enableVanillaSoupExtraEffects` is `true` here, so vanilla Mushroom Stew and Beetroot Soup also
grant 3 minutes of Nourishment and Rabbit Stew grants 5 minutes.
`enableStackableSoupItems` is `true` with the default list, so Mushroom Stew, Beetroot Soup and
Rabbit Stew all stack to 16 like the mod's own meals.

The second effect, **Comfort**, heals 1 health every 80 ticks (4 s) while the player has
saturation left and no Regeneration. No cooking-pot recipe grants it directly.

## Config affecting cooking

From the live `/config/farmersdelight-common.toml`. All four are at the mod defaults.

| Option | Value | Effect |
|---|---|---|
| `enableCookingPotRecipeBook` | `true` | recipe book in the Cooking Pot GUI |
| `cuttingBoardFortuneBonus` | `0.1` | +10 percentage points per Fortune level on cutting-board chance results |
| `enableCuttingBoardDispenserBehavior` | `true` | dispensers can operate a cutting board |
| `enableVanillaSoupExtraEffects` | `true` | vanilla soups grant Nourishment |
| `enableStackableSoupItems` | `true` | vanilla soups stack to 16 |

## Recipe types

| Type | Serializer | Count in the jar | Station |
|---|---|---|---|
| `farmersdelight:cooking` | `farmersdelight:cooking` | 28 | Cooking Pot |
| `farmersdelight:cutting` | `farmersdelight:cutting` | **106** (72 `cutting/`, 33 `salvaging/`, 1 SilentGear) | Cutting Board |
| `farmersdelight:food_serving` | special crafting | 1 | crafting table |
| `farmersdelight:dough` | special crafting | 1 | crafting table |
| `minecraft:crafting_shaped` | — | 51 (+3 inside `forge:conditional`) | crafting table |
| `minecraft:crafting_shapeless` | — | 86 | crafting table |
| `minecraft:campfire_cooking` | — | 7 | campfire, Skillet, Stove |
| `minecraft:smoking` | — | 9 | smoker |
| `minecraft:smelting` | — | 10 | furnace |
| `minecraft:blasting` | — | 2 | blast furnace |
| `minecraft:smithing_transform` | — | 1 | smithing table |
| Create / Immersive Engineering / SilentGear | — | 29 | **inactive** |

333 files in total. The `integration/` tree (29 files, all wrapped in a `forge:mod_loaded`
condition) targets Create, Immersive Engineering and SilentGear — **none of which are installed
on this server**, so none of those recipes load. The one exception worth knowing is that the
SilentGear file is a `farmersdelight:cutting` recipe, which is why the cutting-recipe count is
106 files but only 105 active ones.

The `farmersdelight:cutting` type takes exactly one input ingredient and up to four results;
`farmersdelight:cooking` takes up to six and throws a parse error above that.

The two special crafting recipes have no shape:

- **`farmersdelight:food_serving`** — a Cooking Pot item holding a meal, plus one item matching
  that meal's container, anywhere in a 2×2 or larger grid. Yields one serving and returns the
  pot with one fewer.
- **`farmersdelight:dough`** — one Wheat plus one item in `#forge:buckets/water`, anywhere in a 2×2
  or larger grid. Yields one Wheat Dough and gives the bucket back. (The shaped
  `wheat_dough_from_egg` recipe, 3 Wheat + 1 egg → 3 Dough, is the bulk alternative.)

## Recipe tag reference

The cooking-pot recipes lean on Forge tags. Those the mod defines itself:

| Tag | Contents |
|---|---|
| `#forge:crops/cabbage`, `#forge:salad_ingredients` | Cabbage, Cabbage Leaf |
| `#forge:crops/onion`, `#forge:vegetables/onion` | Onion |
| `#forge:crops/tomato`, `#forge:vegetables/tomato` | Tomato |
| `#forge:crops/rice`, `#forge:grain/rice`, `#forge:seeds/rice` | Rice |
| `#forge:vegetables` | Beetroot, Carrot, Onion, Potato, Tomato |
| `#forge:raw_meat` | Rabbit + raw beef, chicken, pork, mutton (each including the mod's cut versions) |
| `#forge:raw_beef` | Beef, Minced Beef |
| `#forge:raw_chicken` | Chicken, Raw Chicken Cuts |
| `#forge:raw_pork` | Porkchop, Raw Bacon |
| `#forge:raw_mutton` | Mutton, Raw Mutton Chops |
| `#forge:raw_fishes` | Cod, Raw Cod Slice, Salmon, Raw Salmon Slice, Tropical Fish |
| `#forge:milk` | Milk Bucket, Milk Bottle |
| `#forge:eggs` | Egg |
| `#forge:dough` | Wheat Dough |
| `#forge:pasta` | Raw Pasta |
| `#forge:bread` | Bread |
| `#forge:berries` | Sweet Berries, Glow Berries |
| `#forge:serving_containers` (`farmersdelight:serving_containers`) | Bowl, Glass Bottle, Bucket |

`#forge:crops/beetroot`, `#forge:crops/carrot`, `#forge:crops/potato`, `#forge:crops/wheat`,
`#forge:mushrooms` and `#forge:bones` are used by cooking-pot recipes but are **not** defined in
this jar; they come from Forge itself or from other mods on the server. Their exact contents are
not documented here.


### Inactive integration recipes

All 29 files under `data/farmersdelight/recipes/integration/` carry a `forge:mod_loaded`
condition for a mod that is **not on this server**, so none of them load. Listed for
completeness in case one of those mods is ever added:

| Folder | Type | Count | Target mod |
|---|---|---|---|
| `create/milling` | `create:milling` | 8 | Create |
| `create/mixing` | `create:mixing` | 3 | Create |
| `create/filling` | `create:filling` | 1 | Create |
| `immersiveengineering/crusher` | `immersiveengineering:crusher` | 8 | Immersive Engineering |
| `immersiveengineering/cloche` | `immersiveengineering:cloche` | 4 | Immersive Engineering |
| `immersiveengineering/squeezer` | `immersiveengineering:squeezer` | 2 | Immersive Engineering |
| `immersiveengineering/fermenter` | `immersiveengineering:fermenter` | 1 | Immersive Engineering |
| `immersiveengineering/metalpress` | `immersiveengineering:metal_press` | 1 | Immersive Engineering |
| `silentgear/cutting` | `farmersdelight:cutting` | 1 | SilentGear |

Counted by grepping `"modid"` out of every recipe file: 12 `create`, 16 `immersiveengineering`,
1 `silentgear`, and no other modid appears in a recipe condition. Farmer's Delight does also
ship `data/` trees for `create`, `createaddition`, `origins`, `sereneseasons` and `tconstruct`,
but those are **tags**, not recipes, and are likewise inert with their mods absent.

The three crate recipes (`potato_crate`, `carrot_crate`, `beetroot_crate`) are also conditional,
but on the mod's own `enableVanillaCropCrates` config option, which is `true` here — they load.

## Add-on overlap

Two Farmer's Delight add-ons are installed. Neither **overrides** a `farmersdelight:` recipe
file; both add to `farmersdelight:` **tags**, which is what changes behaviour documented above.
Full treatment belongs in `addons.md` — flagged here only:

- **`forge-dungeonsdelight-1.20.1-1.3.0.jar`** ships a `data/farmersdelight/` tree of 15 tag
  files (no recipes). It adds `dungeonsdelight:dungeon_stove` to
  `#farmersdelight:heat_sources`, `dungeonsdelight:living_fire` to
  `#farmersdelight:tray_heat_sources`, `#dungeonsdelight:cleavers` and
  `dungeonsdelight:stained_knife` to `#farmersdelight:tools/knives`, plus entries in
  `mineable/knife`, `cabinets/wooden`, `drinks`, `feasts` and `meals`. Its own 275 recipe files
  live in the `dungeonsdelight:` namespace and include `farmersdelight:cooking` and
  `farmersdelight:cutting` entries that appear on the same stations.
- **`alexsdelight-1.5.jar`** ships **no** `data/farmersdelight/` tree at all. Its cooking-pot
  and cutting-board recipes live entirely under `data/alexsdelight/recipes/`.

## Notes and open items

- The `#minecraft:campfires`, `#minecraft:fire`, `#forge:crops/beetroot`, `#forge:crops/carrot`,
  `#forge:crops/potato`, `#forge:crops/wheat`, `#forge:mushrooms` and `#forge:bones` tags are
  not defined in this jar. Their contents on this server, after every mod's tag file merges,
  were **not verified** — the entries listed here are Farmer's Delight's own contributions only.
- Only the Farmer's Delight, Dungeons Delight and Alex's Delight jars were checked for
  additions to `#farmersdelight:heat_sources` and `#farmersdelight:tools/knives`. The other 150
  jars on the server were **not** scanned; another mod could add a heat source or a knife.
- Cooking-pot recipes that output a vanilla item (Beetroot Soup, Mushroom Stew, Rabbit Stew)
  show `—` for hunger and saturation in the table below because those values are vanilla's, not
  the mod's. Farmer's Delight does add Nourishment to all three via `VANILLA_SOUP_EFFECTS`
  (3 min, 3 min and 5 min respectively) when `enableVanillaSoupExtraEffects` is on.
- Hot Cocoa has no `FoodProperties` at all. It is a `DrinkableItem` whose only effect is to
  remove one randomly chosen harmful, milk-curable status effect.
- Stuffed Pumpkin is listed by its block ID `farmersdelight:stuffed_pumpkin_block`; eating it
  means placing it and taking the four `farmersdelight:stuffed_pumpkin` servings (14 hunger,
  0.75 saturation, 5 min Nourishment each).
- The Skillet cooking-time table assumes a 600-tick campfire recipe, which is every campfire
  recipe in vanilla and in this mod. A modded campfire recipe with a different time gets a
  different result from the same formula.

## Recipe lists

### Cooking Pot — all 28 recipes

| Result | Registry ID | Ingredients | Container | Time | XP | Book tab | Hunger | Sat. | Nourishment |
|---|---|---|---|---|---|---|---|---|---|
| Apple Cider | `farmersdelight:apple_cider` | Apple + Apple + Sugar | Glass Bottle | 10 s | 1 | drinks | 0 | 0 | — |
| Baked Cod Stew | `farmersdelight:baked_cod_stew` | `#forge:raw_fishes/cod` + `#forge:crops/potato` + `#forge:eggs` + `#forge:crops/tomato` | Bowl | 10 s | 1 | meals | 14 | 0.75 | 5 min |
| Beef Stew | `farmersdelight:beef_stew` | `#forge:raw_beef` + `#forge:crops/carrot` + `#forge:crops/potato` | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Beetroot Soup | `minecraft:beetroot_soup` | `#forge:crops/beetroot` + `#forge:crops/beetroot` + `#forge:crops/beetroot` | Bowl | 10 s | 1 | meals | — | — | — |
| Bone Broth | `farmersdelight:bone_broth` | `#forge:bones` + Glow Berries / `#forge:mushrooms` / Hanging Roots / Glow Lichen | Bowl | 10 s | 0.35 | meals | 8 | 0.7 | 60 s |
| Cabbage Rolls | `farmersdelight:cabbage_rolls` | `#forge:crops/cabbage` + `#forge:raw_meat` / `#forge:raw_fishes` / `#forge:vegetables` / `#forge:mushrooms` | none | 5 s | 0.35 | misc | 5 | 0.5 | — |
| Chicken Soup | `farmersdelight:chicken_soup` | `#forge:raw_chicken` + `#forge:crops/carrot` + `#forge:salad_ingredients` + `#forge:vegetables` | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Cooked Rice | `farmersdelight:cooked_rice` | `#forge:crops/rice` | Bowl | 5 s | 0.35 | misc | 6 | 0.4 | 30 s |
| Dog Food | `farmersdelight:dog_food` | Rotten Flesh + Bone Meal + `#forge:raw_meat` + `#forge:crops/rice` | Bowl | 10 s | 1 | misc | 4 | 0.2 | — |
| Dumplings ×2 | `farmersdelight:dumplings` | `#forge:dough` + `#forge:crops/cabbage` + `#forge:crops/onion` + `#forge:raw_chicken` / `#forge:raw_pork` / `#forge:raw_beef` / Brown Mushroom | none | 10 s | 1 | misc | 8 | 0.8 | — |
| Fish Stew | `farmersdelight:fish_stew` | `#forge:raw_fishes` + Tomato Sauce + `#forge:crops/onion` | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Fried Rice | `farmersdelight:fried_rice` | `#forge:crops/rice` + `#forge:eggs` + `#forge:crops/carrot` + `#forge:crops/onion` | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Glow Berry Custard | `farmersdelight:glow_berry_custard` | Glow Berries + `#forge:milk` + `#forge:eggs` + Sugar | Glass Bottle | 10 s | 1 | misc | 7 | 0.6 | — |
| Hot Cocoa | `farmersdelight:hot_cocoa` | `#forge:milk` + Sugar + Cocoa Beans + Cocoa Beans | Glass Bottle | 10 s | 1 | drinks | — | — | — |
| Mushroom Rice | `farmersdelight:mushroom_rice` | Brown Mushroom + Red Mushroom + `#forge:crops/rice` + Carrot / Potato | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Mushroom Stew | `minecraft:mushroom_stew` | Brown Mushroom + Red Mushroom | Bowl | 10 s | 1 | meals | — | — | — |
| Noodle Soup | `farmersdelight:noodle_soup` | `#forge:pasta` + `#forge:eggs` + Dried Kelp + `#forge:raw_pork` | Bowl | 10 s | 1 | meals | 14 | 0.75 | 5 min |
| Onion Soup | `farmersdelight:onion_soup` | `#forge:crops/onion` + `#forge:crops/onion` + `#forge:bread` + `#forge:milk` | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Pasta with Meatballs | `farmersdelight:pasta_with_meatballs` | Minced Beef + `#forge:pasta` + Tomato Sauce | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Pasta with Mutton Chop | `farmersdelight:pasta_with_mutton_chop` | `#forge:raw_mutton` + `#forge:pasta` + Tomato Sauce | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |
| Pumpkin Soup | `farmersdelight:pumpkin_soup` | Pumpkin Slice + `#forge:salad_ingredients` + `#forge:raw_pork` + `#forge:milk` | Bowl | 10 s | 1 | meals | 14 | 0.75 | 5 min |
| Rabbit Stew | `minecraft:rabbit_stew` | `#forge:crops/potato` + Rabbit + `#forge:crops/carrot` + Brown Mushroom / Red Mushroom | Bowl | 10 s | 1 | meals | — | — | — |
| Ratatouille | `farmersdelight:ratatouille` | `#forge:crops/tomato` + `#forge:crops/onion` + `#forge:crops/beetroot` + `#forge:vegetables` | Bowl | 10 s | 1 | meals | 10 | 0.6 | 60 s |
| Squid Ink Pasta | `farmersdelight:squid_ink_pasta` | `#forge:raw_fishes` + `#forge:pasta` + `#forge:crops/tomato` + Ink Sac | Bowl | 10 s | 1 | meals | 14 | 0.75 | 5 min |
| Stuffed Pumpkin | `farmersdelight:stuffed_pumpkin_block` | `#forge:crops/rice` + `#forge:crops/onion` + Brown Mushroom + `#forge:crops/potato` + `#forge:berries` + `#forge:vegetables` | Pumpkin | 20 s | 2 | meals | — | — | — |
| Tomato Sauce | `farmersdelight:tomato_sauce` | `#forge:crops/tomato` + `#forge:crops/tomato` | Bowl | 5 s | 0.35 | misc | 4 | 0.4 | — |
| Vegetable Noodles | `farmersdelight:vegetable_noodles` | `#forge:crops/carrot` + `#forge:mushrooms` + `#forge:pasta` + `#forge:salad_ingredients` + `#forge:vegetables` | Bowl | 10 s | 1 | meals | 14 | 0.75 | 5 min |
| Vegetable Soup | `farmersdelight:vegetable_soup` | `#forge:crops/carrot` + `#forge:crops/potato` + `#forge:crops/beetroot` + `#forge:salad_ingredients` | Bowl | 10 s | 1 | meals | 12 | 0.8 | 3 min |

### Cutting Board — all 106 recipes, by tool

Grouped by the `farmersdelight:tool_action` each recipe declares. Percentages are per-result
chances before Fortune; a result with a count and a chance rolls once per item.

#### Knife — `knife_dig` (47)

| Input | Output | Recipe ID |
|---|---|---|
| Allium | Magenta Dye ×2 | `farmersdelight:cutting/allium` |
| Apple Pie | Slice of Apple Pie ×4 | `farmersdelight:cutting/apple_pie` |
| Azure Bluet | Light Gray Dye ×2 | `farmersdelight:cutting/azure_bluet` |
| Beef | Minced Beef ×2 | `farmersdelight:cutting/beef` |
| Blue Orchid | Light Blue Dye ×2 | `farmersdelight:cutting/blue_orchid` |
| Brown Mushroom Colony | Brown Mushroom ×5 | `farmersdelight:cutting/brown_mushroom_colony` |
| Cabbage | Cabbage Leaf ×2 | `farmersdelight:cutting/cabbage` |
| Cake | Slice of Cake ×7 | `farmersdelight:cutting/cake` |
| Chicken | Raw Chicken Cuts ×2, Bone Meal | `farmersdelight:cutting/chicken` |
| Chocolate Pie | Slice of Chocolate Pie ×4 | `farmersdelight:cutting/chocolate_pie` |
| Cod | Raw Cod Slice ×2, Bone Meal | `farmersdelight:cutting/cod` |
| Cooked Chicken | Cooked Chicken Cuts ×2, Bone Meal | `farmersdelight:cutting/cooked_chicken` |
| Cooked Cod | Cooked Cod Slice ×2, Bone Meal | `farmersdelight:cutting/cooked_cod` |
| Cooked Mutton | Cooked Mutton Chops ×2 | `farmersdelight:cutting/cooked_mutton` |
| Cooked Salmon | Cooked Salmon Slice ×2, Bone Meal | `farmersdelight:cutting/cooked_salmon` |
| Cornflower | Blue Dye ×2 | `farmersdelight:cutting/cornflower` |
| Dandelion | Yellow Dye ×2 | `farmersdelight:cutting/dandelion` |
| Ham | Porkchop ×2, Bone | `farmersdelight:cutting/ham` |
| Ink Sac | Black Dye ×2 | `farmersdelight:cutting/ink_sac` |
| Kelp Roll | Kelp Roll Slice ×3 | `farmersdelight:cutting/kelp_roll` |
| Lily Of The Valley | White Dye ×2 | `farmersdelight:cutting/lily_of_the_valley` |
| Melon | Melon Slice ×9 | `farmersdelight:cutting/melon` |
| Mutton | Raw Mutton Chops ×2 | `farmersdelight:cutting/mutton` |
| Orange Tulip | Orange Dye ×2 | `farmersdelight:cutting/orange_tulip` |
| Oxeye Daisy | Light Gray Dye ×2 | `farmersdelight:cutting/oxeye_daisy` |
| Pink Tulip | Pink Dye ×2 | `farmersdelight:cutting/pink_tulip` |
| Poppy | Red Dye ×2 | `farmersdelight:cutting/poppy` |
| Porkchop | Raw Bacon ×2 | `farmersdelight:cutting/porkchop` |
| Pumpkin | Pumpkin Slice ×4 | `farmersdelight:cutting/pumpkin` |
| Pumpkin Pie | Slice of Pumpkin Pie ×4 | `farmersdelight:cutting/pumpkin_pie` |
| Red Mushroom Colony | Red Mushroom ×5 | `farmersdelight:cutting/red_mushroom_colony` |
| Red Tulip | Red Dye ×2 | `farmersdelight:cutting/red_tulip` |
| Rice Panicle | Rice, Straw | `farmersdelight:cutting/rice_panicle` |
| Salmon | Raw Salmon Slice ×2, Bone Meal | `farmersdelight:cutting/salmon` |
| Sea Beet | Beetroot Seeds, Red Dye | `farmersdelight:cutting/wild_beetroots` |
| Smoked Ham | Cooked Porkchop ×2, Bone | `farmersdelight:cutting/smoked_ham` |
| Sweet Berry Cheesecake | Slice of Sweet Berry Cheesecake ×4 | `farmersdelight:cutting/sweet_berry_cheesecake` |
| Tomato Shrub | Tomato Seeds, Tomato — 20%, Green Dye — 10% | `farmersdelight:cutting/wild_tomatoes` |
| Torchflower | Orange Dye ×2 | `farmersdelight:cutting/torchflower` |
| White Tulip | Light Gray Dye ×2 | `farmersdelight:cutting/white_tulip` |
| Wild Cabbage | Cabbage Seeds, Yellow Dye ×2 — 50% | `farmersdelight:cutting/wild_cabbages` |
| Wild Carrot | Carrot, Light Gray Dye ×2 — 50% | `farmersdelight:cutting/wild_carrots` |
| Wild Onion | Onion, Magenta Dye ×2, Lime Dye — 10% | `farmersdelight:cutting/wild_onions` |
| Wild Potato | Potato, Purple Dye ×2 — 50% | `farmersdelight:cutting/wild_potatoes` |
| Wild Rice | Rice, Straw — 50% | `farmersdelight:cutting/wild_rice` |
| Wither Rose | Black Dye ×2 | `farmersdelight:cutting/wither_rose` |
| `#forge:dough` | Raw Pasta | `farmersdelight:cutting/tag_dough` |

#### Axe (strip) — `axe_strip` (22)

| Input | Output | Recipe ID |
|---|---|---|
| Acacia Log | Stripped Acacia Log, Tree Bark | `farmersdelight:cutting/acacia_log` |
| Acacia Wood | Stripped Acacia Wood, Tree Bark | `farmersdelight:cutting/acacia_wood` |
| Bamboo Block | Stripped Bamboo Block, Straw | `farmersdelight:cutting/bamboo_block` |
| Birch Log | Stripped Birch Log, Tree Bark | `farmersdelight:cutting/birch_log` |
| Birch Wood | Stripped Birch Wood, Tree Bark | `farmersdelight:cutting/birch_wood` |
| Cherry Log | Stripped Cherry Log, Tree Bark | `farmersdelight:cutting/cherry_log` |
| Cherry Wood | Stripped Cherry Wood, Tree Bark | `farmersdelight:cutting/cherry_wood` |
| Crimson Hyphae | Stripped Crimson Hyphae, Tree Bark | `farmersdelight:cutting/crimson_hyphae` |
| Crimson Stem | Stripped Crimson Stem, Tree Bark | `farmersdelight:cutting/crimson_stem` |
| Dark Oak Log | Stripped Dark Oak Log, Tree Bark | `farmersdelight:cutting/dark_oak_log` |
| Dark Oak Wood | Stripped Dark Oak Wood, Tree Bark | `farmersdelight:cutting/dark_oak_wood` |
| Jungle Log | Stripped Jungle Log, Tree Bark | `farmersdelight:cutting/jungle_log` |
| Jungle Wood | Stripped Jungle Wood, Tree Bark | `farmersdelight:cutting/jungle_wood` |
| Mangrove Log | Stripped Mangrove Log, Tree Bark | `farmersdelight:cutting/mangrove_log` |
| Mangrove Wood | Stripped Mangrove Wood, Tree Bark | `farmersdelight:cutting/mangrove_wood` |
| Netherwood Log | Stripped Netherwood Log, Tree Bark | `farmersdelight:integration/silentgear/cutting/netherwood` |
| Oak Log | Stripped Oak Log, Tree Bark | `farmersdelight:cutting/oak_log` |
| Oak Wood | Stripped Oak Wood, Tree Bark | `farmersdelight:cutting/oak_wood` |
| Spruce Log | Stripped Spruce Log, Tree Bark | `farmersdelight:cutting/spruce_log` |
| Spruce Wood | Stripped Spruce Wood, Tree Bark | `farmersdelight:cutting/spruce_wood` |
| Warped Hyphae | Stripped Warped Hyphae, Tree Bark | `farmersdelight:cutting/warped_hyphae` |
| Warped Stem | Stripped Warped Stem, Tree Bark | `farmersdelight:cutting/warped_stem` |

#### Axe — `axe_dig` (13)

| Input | Output | Recipe ID |
|---|---|---|
| Acacia Door / Acacia Trapdoor / Acacia Sign / Acacia Hanging Sign / Acacia Fence / Acacia Fence Gate / Acacia Pressure Plate / Acacia Button / Acacia Boat / Acacia Cabinet | Acacia Planks — 75% | `farmersdelight:salvaging/acacia_furniture` |
| Bamboo Basket | Canvas, Bamboo | `farmersdelight:cutting/bamboo_basket` |
| Bamboo Door / Bamboo Trapdoor / Bamboo Sign / Bamboo Hanging Sign / Bamboo Fence / Bamboo Fence Gate / Bamboo Pressure Plate / Bamboo Button / Bamboo Raft / Bamboo Cabinet | Bamboo Planks — 75% | `farmersdelight:salvaging/bamboo_furniture` |
| Basket | Canvas, Stick | `farmersdelight:cutting/wooden_basket` |
| Birch Door / Birch Trapdoor / Birch Sign / Birch Hanging Sign / Birch Fence / Birch Fence Gate / Birch Pressure Plate / Birch Button / Birch Boat / Birch Cabinet | Birch Planks — 75% | `farmersdelight:salvaging/birch_furniture` |
| Cherry Door / Cherry Trapdoor / Cherry Sign / Cherry Hanging Sign / Cherry Fence / Cherry Fence Gate / Cherry Pressure Plate / Cherry Button / Cherry Boat / Cherry Cabinet | Cherry Planks — 75% | `farmersdelight:salvaging/cherry_furniture` |
| Crimson Door / Crimson Trapdoor / Crimson Sign / Crimson Hanging Sign / Crimson Fence / Crimson Fence Gate / Crimson Pressure Plate / Crimson Button / Crimson Cabinet | Crimson Planks — 75% | `farmersdelight:salvaging/crimson_furniture` |
| Dark Oak Door / Dark Oak Trapdoor / Dark Oak Sign / Dark Oak Hanging Sign / Dark Oak Fence / Dark Oak Fence Gate / Dark Oak Pressure Plate / Dark Oak Button / Dark Oak Boat / Dark Oak Cabinet | Dark Oak Planks — 75% | `farmersdelight:salvaging/dark_oak_furniture` |
| Jungle Door / Jungle Trapdoor / Jungle Sign / Jungle Hanging Sign / Jungle Fence / Jungle Fence Gate / Jungle Pressure Plate / Jungle Button / Jungle Boat / Jungle Cabinet | Jungle Planks — 75% | `farmersdelight:salvaging/jungle_furniture` |
| Mangrove Door / Mangrove Trapdoor / Mangrove Sign / Mangrove Hanging Sign / Mangrove Fence / Mangrove Fence Gate / Mangrove Pressure Plate / Mangrove Button / Mangrove Boat / Mangrove Cabinet | Mangrove Planks — 75% | `farmersdelight:salvaging/mangrove_furniture` |
| Oak Door / Oak Trapdoor / Oak Sign / Oak Hanging Sign / Oak Fence / Oak Fence Gate / Oak Pressure Plate / Oak Button / Oak Boat / Oak Cabinet | Oak Planks — 75% | `farmersdelight:salvaging/oak_furniture` |
| Spruce Door / Spruce Trapdoor / Spruce Sign / Spruce Hanging Sign / Spruce Fence / Spruce Fence Gate / Spruce Pressure Plate / Spruce Button / Spruce Boat / Spruce Cabinet | Spruce Planks — 75% | `farmersdelight:salvaging/spruce_furniture` |
| Warped Door / Warped Trapdoor / Warped Sign / Warped Hanging Sign / Warped Fence / Warped Fence Gate / Warped Pressure Plate / Warped Button / Warped Cabinet | Warped Planks — 75% | `farmersdelight:salvaging/warped_furniture` |

#### Hoe — `hoe_dig` (13)

| Input | Output | Recipe ID |
|---|---|---|
| Acacia Chest Boat | Acacia Boat, Chest | `farmersdelight:salvaging/acacia_chest_boat` |
| Bamboo Chest Raft | Bamboo Raft, Chest | `farmersdelight:salvaging/bamboo_chest_raft` |
| Birch Chest Boat | Birch Boat, Chest | `farmersdelight:salvaging/birch_chest_boat` |
| Cherry Chest Boat | Cherry Boat, Chest | `farmersdelight:salvaging/cherry_chest_boat` |
| Chest Minecart | Minecart, Chest | `farmersdelight:salvaging/chest_minecart` |
| Dark Oak Chest Boat | Dark Oak Boat, Chest | `farmersdelight:salvaging/dark_oak_chest_boat` |
| Furnace Minecart | Minecart, Furnace | `farmersdelight:salvaging/furnace_minecart` |
| Hopper Minecart | Minecart, Hopper | `farmersdelight:salvaging/hopper_minecart` |
| Jungle Chest Boat | Jungle Boat, Chest | `farmersdelight:salvaging/jungle_chest_boat` |
| Mangrove Chest Boat | Mangrove Boat, Chest | `farmersdelight:salvaging/mangrove_chest_boat` |
| Oak Chest Boat | Oak Boat, Chest | `farmersdelight:salvaging/oak_chest_boat` |
| Spruce Chest Boat | Spruce Boat, Chest | `farmersdelight:salvaging/spruce_chest_boat` |
| Tnt Minecart | Minecart, Tnt | `farmersdelight:salvaging/tnt_minecart` |

#### Pickaxe — `pickaxe_dig` (6)

| Input | Output | Recipe ID |
|---|---|---|
| Amethyst Block | Amethyst Shard ×4 | `farmersdelight:salvaging/amethyst_block` |
| Bricks | Brick ×4 | `farmersdelight:salvaging/bricks` |
| Deepslate | Cobbled Deepslate | `farmersdelight:salvaging/deepslate` |
| Nether Bricks | Nether Brick ×4 | `farmersdelight:salvaging/nether_bricks` |
| Quartz Block | Quartz ×4 | `farmersdelight:salvaging/quartz_block` |
| Stone | Cobblestone | `farmersdelight:salvaging/stone` |

#### Shears — `shears_dig` (3)

| Input | Output | Recipe ID |
|---|---|---|
| Leather Helmet / Leather Chestplate / Leather Leggings / Leather Boots | Leather | `farmersdelight:salvaging/leather_armor` |
| Leather Horse Armor | Leather ×2 | `farmersdelight:salvaging/leather_horse_armor` |
| Saddle | Leather ×2, Iron Nugget ×2 — 50% | `farmersdelight:salvaging/saddle` |

#### Shovel — `shovel_dig` (2)

| Input | Output | Recipe ID |
|---|---|---|
| Clay | Clay Ball ×4 | `farmersdelight:cutting/clay` |
| Gravel | Gravel, Flint — 10% | `farmersdelight:cutting/gravel` |

### Campfire, smoker and furnace recipes added by the mod

| Input | Output | Type | Time | XP |
|---|---|---|---|---|
| Egg | Fried Egg | Campfire | 30 s | 0.35 |
| Egg | Fried Egg | Furnace | 10 s | 0.35 |
| Egg | Fried Egg | Smoker | 5 s | 0.35 |
| Golden Knife | Gold Nugget | Blast furnace | 5 s | 0.1 |
| Golden Knife | Gold Nugget | Furnace | 10 s | 0.1 |
| Ham | Smoked Ham | Smoker | 10 s | 0.35 |
| Iron Knife | Iron Nugget | Blast furnace | 5 s | 0.1 |
| Iron Knife | Iron Nugget | Furnace | 10 s | 0.1 |
| Minced Beef | Beef Patty | Campfire | 30 s | 0.35 |
| Minced Beef | Beef Patty | Furnace | 10 s | 0.35 |
| Minced Beef | Beef Patty | Smoker | 5 s | 0.35 |
| Raw Bacon | Cooked Bacon | Campfire | 30 s | 0.35 |
| Raw Bacon | Cooked Bacon | Furnace | 10 s | 0.35 |
| Raw Bacon | Cooked Bacon | Smoker | 5 s | 0.35 |
| Raw Chicken Cuts | Cooked Chicken Cuts | Campfire | 30 s | 0.35 |
| Raw Chicken Cuts | Cooked Chicken Cuts | Furnace | 10 s | 0.35 |
| Raw Chicken Cuts | Cooked Chicken Cuts | Smoker | 5 s | 0.35 |
| Raw Cod Slice | Cooked Cod Slice | Campfire | 30 s | 0.35 |
| Raw Cod Slice | Cooked Cod Slice | Furnace | 10 s | 0.35 |
| Raw Cod Slice | Cooked Cod Slice | Smoker | 5 s | 0.35 |
| Raw Mutton Chops | Cooked Mutton Chops | Campfire | 30 s | 0.35 |
| Raw Mutton Chops | Cooked Mutton Chops | Furnace | 10 s | 0.35 |
| Raw Mutton Chops | Cooked Mutton Chops | Smoker | 5 s | 0.35 |
| Raw Salmon Slice | Cooked Salmon Slice | Campfire | 30 s | 0.35 |
| Raw Salmon Slice | Cooked Salmon Slice | Furnace | 10 s | 0.35 |
| Raw Salmon Slice | Cooked Salmon Slice | Smoker | 5 s | 0.35 |
| Wheat Dough | Bread | Furnace | 10 s | 0.35 |
| Wheat Dough | Bread | Smoker | 5 s | 0.35 |

### Crafting table recipes

| Result | Shape | Ingredients | Recipe ID |
|---|---|---|---|
| Acacia Cabinet | `___` / `D·D` / `___` | `D` = Acacia Trapdoor; `_` = Acacia Slab | `farmersdelight:acacia_cabinet` |
| Apple Pie | `###` / `aaa` / `xOx` | `#` = `#forge:crops/wheat`; `O` = Pie Crust; `a` = Apple; `x` = Sugar | `farmersdelight:apple_pie` |
| Apple Pie | `##` / `##` | `#` = Slice of Apple Pie | `farmersdelight:apple_pie_from_slices` |
| Bacon Sandwich | shapeless | `#forge:bread`, `#forge:cooked_bacon`, `#forge:salad_ingredients`, `#forge:crops/tomato` | `farmersdelight:bacon_sandwich` |
| Bacon and Eggs | shapeless | Cooked Bacon ×2, Bowl, `#forge:cooked_eggs` ×2 | `farmersdelight:bacon_and_eggs` |
| Bag of Rice | `###` / `###` / `###` | `#` = Rice | `farmersdelight:rice_bag` |
| Bamboo Basket | `/·/` / `#·#` / `/#/` | `#` = Canvas; `/` = Bamboo | `farmersdelight:bamboo_basket` |
| Bamboo Cabinet | `___` / `D·D` / `___` | `D` = Bamboo Trapdoor; `_` = Bamboo Slab | `farmersdelight:bamboo_cabinet` |
| Barbecue on a Stick | shapeless | `#forge:crops/tomato`, `#forge:crops/onion`, `#forge:cooked_beef` / `#forge:cooked_pork` / `#forge:cooked_chicken` / `#forge:cooked_mutton` / `#forge:cooked_fishes` / Cooked Rabbit, Stick | `farmersdelight:barbecue_stick` |
| Basket | `/·/` / `#·#` / `/#/` | `#` = Canvas; `/` = Stick | `farmersdelight:wooden_basket` |
| Beetroot Crate | `###` / `###` / `###` | `#` = Beetroot | `farmersdelight:beetroot_crate` |
| Beetroot ×9 | shapeless | Beetroot Crate | `farmersdelight:beetroot_from_crate` |
| Birch Cabinet | `___` / `D·D` / `___` | `D` = Birch Trapdoor; `_` = Birch Slab | `farmersdelight:birch_cabinet` |
| Black Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/black` | `farmersdelight:black_canvas_sign` |
| Black Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/black` | `farmersdelight:black_hanging_canvas_sign` |
| Blue Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/blue` | `farmersdelight:blue_canvas_sign` |
| Blue Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/blue` | `farmersdelight:blue_hanging_canvas_sign` |
| Book | shapeless | Paper ×3, Canvas | `farmersdelight:book_from_canvas` |
| Brown Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/brown` | `farmersdelight:brown_canvas_sign` |
| Brown Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/brown` | `farmersdelight:brown_hanging_canvas_sign` |
| Cabbage | shapeless | Cabbage Leaf ×2 | `farmersdelight:cabbage_from_leaves` |
| Cabbage Crate | `###` / `###` / `###` | `#` = Cabbage | `farmersdelight:cabbage_crate` |
| Cabbage ×9 | shapeless | Cabbage Crate | `farmersdelight:cabbage` |
| Cake | `mmm` / `ses` / `www` | `e` = `#forge:eggs`; `m` = `#forge:milk`; `s` = Sugar; `w` = `#forge:crops/wheat` | `farmersdelight:cake_from_milk_bottle` |
| Cake | shapeless | Slice of Cake ×7 | `farmersdelight:cake_from_slices` |
| Canvas | `##` / `##` | `#` = Straw | `farmersdelight:canvas` |
| Canvas | shapeless | Canvas Rug ×2 | `farmersdelight:canvas_from_canvas_rug` |
| Canvas Rug ×2 | shapeless | Canvas | `farmersdelight:canvas_rug` |
| Canvas Sign ×3 | `w#w` / `w#w` / `·/·` | `#` = Canvas; `/` = Stick; `w` = `#minecraft:planks` | `farmersdelight:canvas_sign` |
| Carrot Crate | `###` / `###` / `###` | `#` = Carrot | `farmersdelight:carrot_crate` |
| Carrot ×9 | shapeless | Carrot Crate | `farmersdelight:carrot_from_crate` |
| Cherry Cabinet | `___` / `D·D` / `___` | `D` = Cherry Trapdoor; `_` = Cherry Slab | `farmersdelight:cherry_cabinet` |
| Chicken Sandwich | shapeless | `#forge:bread`, `#forge:cooked_chicken`, `#forge:salad_ingredients`, `#forge:crops/carrot` | `farmersdelight:chicken_sandwich` |
| Chocolate Pie | `##` / `##` | `#` = Slice of Chocolate Pie | `farmersdelight:chocolate_pie_from_slices` |
| Chocolate Pie | `ccc` / `mmm` / `xOx` | `O` = Pie Crust; `c` = Cocoa Beans; `m` = `#forge:milk`; `x` = Sugar | `farmersdelight:chocolate_pie` |
| Cod Roll ×2 | shapeless | Raw Cod Slice ×2, Cooked Rice | `farmersdelight:cod_roll` |
| Cooking Pot | `bSb` / `iWi` / `iii` | `S` = Wooden Shovel; `W` = `#forge:buckets/water`; `b` = Brick; `i` = `#forge:ingots/iron` | `farmersdelight:cooking_pot` |
| Crimson Cabinet | `___` / `D·D` / `___` | `D` = Crimson Trapdoor; `_` = Crimson Slab | `farmersdelight:crimson_cabinet` |
| Cutting Board | `/##` / `/##` | `#` = `#minecraft:planks`; `/` = Stick | `farmersdelight:cutting_board` |
| Cyan Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/cyan` | `farmersdelight:cyan_canvas_sign` |
| Cyan Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/cyan` | `farmersdelight:cyan_hanging_canvas_sign` |
| Dark Oak Cabinet | `___` / `D·D` / `___` | `D` = Dark Oak Trapdoor; `_` = Dark Oak Slab | `farmersdelight:dark_oak_cabinet` |
| Diamond Knife | `m` / `s` | `m` = Diamond; `s` = Stick | `farmersdelight:diamond_knife` |
| Egg Sandwich | shapeless | `#forge:bread`, `#forge:cooked_eggs` ×2 | `farmersdelight:egg_sandwich` |
| Flint Knife | `m` / `s` | `m` = Flint; `s` = Stick | `farmersdelight:flint_knife` |
| Fruit Salad | shapeless | Apple, Melon Slice ×2, `#forge:berries` ×2, Pumpkin Slice, Bowl | `farmersdelight:fruit_salad` |
| Full Tatami Mat | shapeless | Half Tatami Mat ×2 | `farmersdelight:full_tatami_mat_from_halves` |
| Full Tatami Mat ×2 | shapeless | Tatami Block | `farmersdelight:full_tatami_mat` |
| Gleaming Salad | shapeless | Glow Berries ×2, Honey Bottle, `#forge:crops/tomato`, Golden Carrot, `#forge:crops/beetroot`, Cabbage ×2, Bowl | `farmersdelight:gleaming_salad_block` |
| Golden Knife | `m` / `s` | `m` = Gold Ingot; `s` = Stick | `farmersdelight:golden_knife` |
| Gray Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/gray` | `farmersdelight:gray_canvas_sign` |
| Gray Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/gray` | `farmersdelight:gray_hanging_canvas_sign` |
| Green Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/green` | `farmersdelight:green_canvas_sign` |
| Green Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/green` | `farmersdelight:green_hanging_canvas_sign` |
| Grilled Salmon | shapeless | `#forge:cooked_fishes/salmon`, Sweet Berries, Bowl, `#forge:crops/cabbage`, `#forge:crops/onion` | `farmersdelight:grilled_salmon` |
| Half Tatami Mat ×2 | shapeless | Full Tatami Mat | `farmersdelight:half_tatami_mat` |
| Hamburger | shapeless | `#forge:bread`, Beef Patty, `#forge:salad_ingredients`, `#forge:crops/tomato`, `#forge:crops/onion` | `farmersdelight:hamburger` |
| Hanging Canvas Sign ×6 | `X·X` / `w#w` / `w#w` | `#` = Canvas; `X` = Chain; `w` = `#minecraft:logs` | `farmersdelight:hanging_canvas_sign` |
| Honey Cookie ×8 | shapeless | Honey Bottle, `#forge:crops/wheat` ×2 | `farmersdelight:honey_cookie` |
| Honey Glazed Ham | shapeless | Sweet Berries ×4, Honey Bottle, Smoked Ham, Cooked Rice ×2, Bowl | `farmersdelight:honey_glazed_ham_block` |
| Horse Feed | shapeless | Hay Block / Rice Bale, Apple ×2, Golden Carrot | `farmersdelight:horse_feed` |
| Iron Knife | `m` / `s` | `m` = `#forge:ingots/iron`; `s` = Stick | `farmersdelight:iron_knife` |
| Jungle Cabinet | `___` / `D·D` / `___` | `D` = Jungle Trapdoor; `_` = Jungle Slab | `farmersdelight:jungle_cabinet` |
| Kelp Roll | `RXR` / `###` | `#` = Dried Kelp; `R` = Cooked Rice; `X` = `#forge:vegetables` | `farmersdelight:kelp_roll` |
| Lead | `ss·` / `ss·` / `··s` | `s` = Straw | `farmersdelight:lead_from_straw` |
| Light Blue Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/light_blue` | `farmersdelight:light_blue_canvas_sign` |
| Light Blue Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/light_blue` | `farmersdelight:light_blue_hanging_canvas_sign` |
| Light Gray Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/light_gray` | `farmersdelight:light_gray_canvas_sign` |
| Light Gray Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/light_gray` | `farmersdelight:light_gray_hanging_canvas_sign` |
| Lime Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/lime` | `farmersdelight:lime_canvas_sign` |
| Lime Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/lime` | `farmersdelight:lime_hanging_canvas_sign` |
| Magenta Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/magenta` | `farmersdelight:magenta_canvas_sign` |
| Magenta Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/magenta` | `farmersdelight:magenta_hanging_canvas_sign` |
| Mangrove Cabinet | `___` / `D·D` / `___` | `D` = Mangrove Trapdoor; `_` = Mangrove Slab | `farmersdelight:mangrove_cabinet` |
| Melon Juice | shapeless | Melon Slice ×4, Sugar, Glass Bottle | `farmersdelight:melon_juice` |
| Melon Popsicle | `·mm` / `imm` / `-i·` | `-` = Stick; `i` = Ice; `m` = Melon Slice | `farmersdelight:melon_popsicle` |
| Milk Bottle ×4 | shapeless | Milk Bucket, Glass Bottle ×4 | `farmersdelight:milk_bottle` |
| Milk Bucket | shapeless | Bucket, Milk Bottle ×4 | `farmersdelight:milk_bucket_from_bottles` |
| Mixed Salad | shapeless | `#forge:salad_ingredients`, `#forge:crops/tomato`, `#forge:crops/beetroot`, Bowl | `farmersdelight:mixed_salad` |
| Mutton Wrap | shapeless | `#forge:bread`, `#forge:cooked_mutton`, `#forge:salad_ingredients`, `#forge:crops/onion` | `farmersdelight:mutton_wrap` |
| Nether Salad | shapeless | Crimson Fungus, Warped Fungus, Bowl | `farmersdelight:nether_salad` |
| Oak Cabinet | `___` / `D·D` / `___` | `D` = Oak Trapdoor; `_` = Oak Slab | `farmersdelight:oak_cabinet` |
| Onion Crate | `###` / `###` / `###` | `#` = Onion | `farmersdelight:onion_crate` |
| Onion ×9 | shapeless | Onion Crate | `farmersdelight:onion` |
| Orange Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/orange` | `farmersdelight:orange_canvas_sign` |
| Orange Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/orange` | `farmersdelight:orange_hanging_canvas_sign` |
| Organic Compost | shapeless | Dirt, Rotten Flesh ×2, Straw ×2, Bone Meal ×4 | `farmersdelight:organic_compost_from_rotten_flesh` |
| Organic Compost | shapeless | Dirt, Straw ×2, Bone Meal ×2, Tree Bark ×4 | `farmersdelight:organic_compost_from_tree_bark` |
| Packed Mud ×2 | shapeless | Straw, Mud ×2 | `farmersdelight:packed_mud_from_straw` |
| Painting | `sss` / `scs` / `sss` | `c` = Canvas; `s` = Stick | `farmersdelight:painting_from_canvas` |
| Paper | shapeless | Tree Bark ×3 | `farmersdelight:paper_from_tree_bark` |
| Pie Crust | `wMw` / `·w·` | `M` = `#forge:milk`; `w` = `#forge:crops/wheat` | `farmersdelight:pie_crust` |
| Pink Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/pink` | `farmersdelight:pink_canvas_sign` |
| Pink Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/pink` | `farmersdelight:pink_hanging_canvas_sign` |
| Potato Crate | `###` / `###` / `###` | `#` = Potato | `farmersdelight:potato_crate` |
| Potato ×9 | shapeless | Potato Crate | `farmersdelight:potato_from_crate` |
| Pumpkin | `##` / `##` | `#` = Pumpkin Slice | `farmersdelight:pumpkin_from_slices` |
| Pumpkin Pie | `##` / `##` | `#` = Slice of Pumpkin Pie | `farmersdelight:pumpkin_pie_from_slices` |
| Pumpkin Pie ×2 | `cec` / `csc` / `·O·` | `O` = Pie Crust; `c` = Pumpkin Slice; `e` = `#forge:eggs`; `s` = Sugar | `farmersdelight:pumpkin_pie_from_pie_crust` |
| Pumpkin Seeds | shapeless | Pumpkin Slice | `farmersdelight:pumpkin_seeds_from_slice` |
| Purple Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/purple` | `farmersdelight:purple_canvas_sign` |
| Purple Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/purple` | `farmersdelight:purple_hanging_canvas_sign` |
| Red Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/red` | `farmersdelight:red_canvas_sign` |
| Red Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/red` | `farmersdelight:red_hanging_canvas_sign` |
| Rice | shapeless | Rice Panicle | `farmersdelight:rice` |
| Rice Bale | `###` / `###` / `###` | `#` = Rice Panicle | `farmersdelight:rice_bale` |
| Rice Panicle ×9 | shapeless | Rice Bale | `farmersdelight:rice_panicle` |
| Rice Roll Medley | shapeless | Kelp Roll Slice ×3, Salmon Roll ×3, Cod Roll ×2, Bowl | `farmersdelight:rice_roll_medley_block` |
| Rice ×9 | shapeless | Bag of Rice | `farmersdelight:rice_from_bag` |
| Roast Chicken | shapeless | `#forge:crops/onion`, `#forge:eggs`, Bread, `#forge:crops/carrot` ×2, Cooked Chicken, Baked Potato ×2, Bowl | `farmersdelight:roast_chicken_block` |
| Roasted Mutton Chops | shapeless | Cooked Mutton Chops, `#forge:crops/beetroot`, Bowl, Cooked Rice, `#forge:crops/tomato` | `farmersdelight:roasted_mutton_chops` |
| Rope Fence Gate | `/r/` / `/r/` | `/` = Stick; `r` = Rope | `farmersdelight:rope_fence_gate` |
| Rope Fence ×3 | `r/r` / `r/r` | `/` = Stick; `r` = Rope | `farmersdelight:rope_fence` |
| Rope ×4 | `s` / `s` | `s` = Straw | `farmersdelight:rope` |
| Rope ×4 | shapeless | Safety Net | `farmersdelight:rope_from_safety_net` |
| Safety Net | `rr` / `rr` | `r` = Rope | `farmersdelight:safety_net` |
| Salmon Roll ×2 | shapeless | Raw Salmon Slice ×2, Cooked Rice | `farmersdelight:salmon_roll` |
| Scaffolding ×6 | `b#b` / `b·b` / `b·b` | `#` = Canvas; `b` = Bamboo | `farmersdelight:scaffolding_from_canvas` |
| Shepherd's Pie | shapeless | Baked Potato ×2, `#forge:milk`, `#forge:cooked_mutton` ×3, `#forge:crops/onion` ×2, Bowl | `farmersdelight:shepherds_pie_block` |
| Skillet | `·##` / `·##` / `/··` | `#` = `#forge:ingots/iron`; `/` = Brick | `farmersdelight:skillet` |
| Spruce Cabinet | `___` / `D·D` / `___` | `D` = Spruce Trapdoor; `_` = Spruce Slab | `farmersdelight:spruce_cabinet` |
| Steak and Potatoes | shapeless | Baked Potato, Cooked Beef, Bowl, `#forge:crops/onion`, Cooked Rice | `farmersdelight:steak_and_potatoes` |
| Stove | `iii` / `B·B` / `BCB` | `B` = Bricks; `C` = Campfire; `i` = `#forge:ingots/iron` | `farmersdelight:stove` |
| Straw Bale | `###` / `###` / `###` | `#` = Straw | `farmersdelight:straw_bale` |
| Straw ×9 | shapeless | Straw Bale | `farmersdelight:straw` |
| Stuffed Potato | shapeless | Baked Potato, `#forge:cooked_beef`, `#forge:milk` | `farmersdelight:stuffed_potato` |
| Sweet Berry Cheesecake | `##` / `##` | `#` = Slice of Sweet Berry Cheesecake | `farmersdelight:sweet_berry_cheesecake_from_slices` |
| Sweet Berry Cheesecake | `sss` / `sss` / `mOm` | `O` = Pie Crust; `m` = `#forge:milk`; `s` = Sweet Berries | `farmersdelight:sweet_berry_cheesecake` |
| Sweet Berry Cookie ×8 | shapeless | Sweet Berries, `#forge:crops/wheat` ×2 | `farmersdelight:sweet_berry_cookie` |
| Tatami Block | shapeless | Full Tatami Mat ×2 | `farmersdelight:tatami_block_from_full` |
| Tatami Block ×2 | `cs` / `sc` | `c` = Canvas; `s` = Straw | `farmersdelight:tatami` |
| Tomato Crate | `###` / `###` / `###` | `#` = Tomato | `farmersdelight:tomato_crate` |
| Tomato Seeds | shapeless | Tomato / Rotten Tomato | `farmersdelight:tomato_seeds` |
| Tomato ×9 | shapeless | Tomato Crate | `farmersdelight:tomato` |
| Warped Cabinet | `___` / `D·D` / `___` | `D` = Warped Trapdoor; `_` = Warped Slab | `farmersdelight:warped_cabinet` |
| Wheat Dough ×3 | shapeless | `#forge:crops/wheat` ×3, `#forge:eggs` | `farmersdelight:wheat_dough_from_egg` |
| White Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/white` | `farmersdelight:white_canvas_sign` |
| White Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/white` | `farmersdelight:white_hanging_canvas_sign` |
| Yellow Canvas Sign | shapeless | `#farmersdelight:canvas_signs`, `#forge:dyes/yellow` | `farmersdelight:yellow_canvas_sign` |
| Yellow Hanging Canvas Sign | shapeless | `#farmersdelight:hanging_canvas_signs`, `#forge:dyes/yellow` | `farmersdelight:yellow_hanging_canvas_sign` |
