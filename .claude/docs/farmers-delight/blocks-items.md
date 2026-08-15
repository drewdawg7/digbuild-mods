<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Blocks & Items

Everything Farmer's Delight registers that is not food, not a crop, and not a cooking station:
knives, storage, decoration, canvas signs, rope, and the loose materials. IDs are all in the
`farmersdelight:` namespace.

**What is covered elsewhere.** This doc deliberately stops at four boundaries:

| Subject | Doc |
|---|---|
| Cooking Pot, Skillet, Stove, Cutting Board, Basket, and every cooking/cutting recipe | [cooking.md](cooking.md) |
| Food items, feasts, pies, drinks, Nourishment and Comfort | [foods-and-effects.md](foods-and-effects.md) |
| Crops, seeds, Rich Soil, Organic Compost, tomato trellising, wild crops, worldgen | [farming.md](farming.md) |
| Loot tables, the global loot modifiers, chest loot injection | [loot-and-worldgen.md](loot-and-worldgen.md) |

The mod registers **185 items** (184 in the creative tab plus one hidden) and **132 blocks**. Roughly
half the block count is the canvas sign matrix — 17 colours × 4 block forms — which is why the raw
numbers are larger than the visible item list.

> **IDs are the real registry names**, read from the `register("…")` calls in `ModItems` /
> `ModBlocks`, not from the Java field names. Three cases differ: the field `WOODEN_BASKET`
> displays as **Basket** while `BAMBOO_BASKET` displays as **Bamboo Basket**; the wall variants of
> hanging signs register as `<colour>_wall_hanging_canvas_sign` (colour first, `wall` before
> `hanging`) while the standing ones are `<colour>_hanging_canvas_sign`; and `TATAMI` displays as
> "Tatami Block", not "Tatami".

## SRG mapping

jadx leaves SRG names in the decompiled jar. The mapping used here was checked against the clean
upstream source ([`vectorwing/FarmersDelight`](https://github.com/vectorwing/FarmersDelight), branch
`1.20`), file for file:

| SRG | Real name | Verified against |
|---|---|---|
| `m_6609_()` | `Tier.getUses()` | `ModMaterials.FLINT` returns 131 in both |
| `m_6624_()` | `Tier.getSpeed()` | 4.0F in both |
| `m_6631_()` | `Tier.getAttackDamageBonus()` | 1.0F in both |
| `m_6604_()` | `Tier.getLevel()` | 1 in both |
| `m_6601_()` | `Tier.getEnchantmentValue()` | 5 in both |
| `m_41503_(n)` | `Item.Properties.durability(n)` | not used by this mod — knives take durability from their `Tier` |
| `m_41487_(n)` | `Item.Properties.stacksTo(n)` | matches every upstream `stacksTo` call, e.g. `rotten_tomato` = 16 |
| `m_41486_()` | `Item.Properties.fireResistant()` | Netherite Knife only, matches upstream |

**The mapping held.** `ModMaterials.java` and `KnifeItem.java` are byte-for-byte equivalent to
upstream once names are substituted, including the `KnifeItem(tier, attackDamage, attackSpeed,
properties)` argument order that the knife stat table below depends on.

## Tools and weapons

Five knives, one enchantment. Nothing else in the mod is a tool.

### Knife stats

Every knife is built as `KnifeItem(tier, 0.5F, -2.0F, …)`. The `0.5` is added to the tier's attack
damage bonus, and the `-2.0` is added to the base attack speed of 4.0 — so **every knife swings at
2.0 attacks per second (a 0.5 s cooldown) regardless of material**, and the only thing the material
changes is damage, durability, mining tier and mining speed.

| Knife | Durability | Attack damage (displayed) | Attack speed | Mining tier | Mining speed | Enchantability |
|---|---|---|---|---|---|---|
| `flint_knife` Flint Knife | 131 | 2.5 | 2.0/s | Stone | 4.0 | 5 |
| `golden_knife` Golden Knife | 32 | 1.5 | 2.0/s | Wood | 12.0 | 22 |
| `iron_knife` Iron Knife | 250 | 3.5 | 2.0/s | Iron | 6.0 | 14 |
| `diamond_knife` Diamond Knife | 1561 | 4.5 | 2.0/s | Diamond | 8.0 | 10 |
| `netherite_knife` Netherite Knife | 2031 | 5.5 | 2.0/s | Netherite | 9.0 | 15 |

Flint's tier is defined by the mod (`ModMaterials.FLINT`, repaired with flint). The other four use
the vanilla `Tiers` enum, so their durability, mining tier, mining speed and enchantability are
vanilla values and their repair materials are the vanilla ones. Displayed attack damage is
`1 + 0.5 + tier bonus`; the tier bonuses are 1.0 flint, 0.0 gold, 2.0 iron, 3.0 diamond, 4.0
netherite.

The Netherite Knife is fire-resistant as an item. Attacking with any knife costs 1 durability, and
knife hits deal **0.1 less knockback** than the same hit with another weapon.

### Enchanting

Knives accept Sharpness, Smite, Bane of Arthropods, Knockback, Fire Aspect and Looting at an
enchanting table, plus anything whose own category already accepts the item (Unbreaking, Mending).
Fortune is explicitly refused — a knife is a `DiggerItem`, so it would otherwise qualify.

`backstabbing` **Backstabbing** is a knife-only enchantment, up to level III, Uncommon rarity, main
hand only. It triggers when the victim is facing away from the attacker (the dot product of the
target's look vector and the direction to the attacker is below −0.5, i.e. roughly the rear 120°
arc) and multiplies the hit by `1.2 + 0.2 × level`:

| Level | Damage multiplier | Min enchanting power |
|---|---|---|
| I | ×1.4 | 15 |
| II | ×1.6 | 24 |
| III | ×1.8 | 33 |

A successful backstab plays the anvil-land sound.

### What a knife can cut

A knife carries four tool actions: `knife_dig`, `knife_harvest`, `shears_carve` and `sword_dig`.
The `farmersdelight:mineable/knife` block tag is what it mines quickly:

- Cactus, melon, pumpkin, carved pumpkin, jack o'lantern, cobweb, cake
- All wool and all wool carpets
- All candle cakes
- `rice_bag`, and the four pie blocks (`apple_pie`, `sweet_berry_cheesecake`, `chocolate_pie`,
  `pumpkin_pie`)
- The `farmersdelight:straw_blocks` tag — despite the name this contains no straw at all, only
  `rope`, `safety_net`, `canvas_rug`, `tatami`, `full_tatami_mat` and `half_tatami_mat`. Its sole
  use in the mod is being folded into this tag.
- `forge:mineable/knife`, so other mods can add to it

Right-clicking a cake with a knife takes one bite and drops a **Cake Slice** item instead of eating
it; a candle cake does the same and drops its candle. This works with any item in
`farmersdelight:tools/knives`, not only this mod's five.

Knives are also the tool for a large set of Cutting Board recipes — see [cooking.md](cooking.md).

### Knife recipes

| Result | Station | Ingredients |
|---|---|---|
| Flint Knife | Crafting table | Flint above a Stick (vertical pair) |
| Iron Knife | Crafting table | Any `forge:ingots/iron` above a Stick |
| Golden Knife | Crafting table | Gold Ingot above a Stick |
| Diamond Knife | Crafting table | Diamond above a Stick |
| Netherite Knife | Smithing table | Netherite Upgrade template + Diamond Knife + Netherite Ingot |

Melting them down: an Iron Knife smelts to an Iron Nugget and a Golden Knife to a Gold Nugget, in a
furnace or blast furnace, 0.1 XP.

## Storage

### Cabinets

Eleven cabinets, one per wood type: `oak_cabinet`, `spruce_cabinet`, `birch_cabinet`,
`jungle_cabinet`, `acacia_cabinet`, `dark_oak_cabinet`, `mangrove_cabinet`, `cherry_cabinet`,
`bamboo_cabinet`, `crimson_cabinet`, `warped_cabinet`.

- **27 slots**, a single chest's worth, using the chest interface.
- **Opens against a wall.** Unlike a chest there is no obstruction check above or in front, so a
  cabinet works flush under a shelf or behind a torch. It also has no double-block form.
- **Contents drop when broken.** There is no shulker-box-style item retention.
- **Emits a comparator signal** proportional to how full it is, on the standard container scale.
- Faces the player when placed, has an `open` state that swings the doors and plays its own
  open/close sound, and keeps a custom name given on an anvil.
- Horizontal facing only, so a cabinet cannot be placed in the ceiling or floor.

Recipe (crafting table), per wood: a ring of **6 matching slabs** around **2 matching trapdoors** —
`___ / D D / ___`, slabs on the top and bottom rows, trapdoors left and right of the centre.

Salvaging a cabinet on a Cutting Board with an axe returns its planks at 75% chance, alongside all
the other furniture of that wood — see [cooking.md](cooking.md).

Tags: `farmersdelight:cabinets` (block and item) currently resolves entirely to
`farmersdelight:cabinets/wooden`.

### Crop crates

Six 3×3 compaction blocks. They are plain blocks — no inventory, no comparator output, nothing
special on break.

| Crate | Packs from | Unpacks to |
|---|---|---|
| `carrot_crate` Carrot Crate | 9 Carrot | 9 Carrot |
| `potato_crate` Potato Crate | 9 Potato | 9 Potato |
| `beetroot_crate` Beetroot Crate | 9 Beetroot | 9 Beetroot |
| `cabbage_crate` Cabbage Crate | 9 Cabbage | *no unpack recipe* |
| `tomato_crate` Tomato Crate | 9 Tomato | *no unpack recipe* |
| `onion_crate` Onion Crate | 9 Onion | *no unpack recipe* |

All six pack in a filled 3×3 crafting grid; the three vanilla-crop unpack recipes are shapeless. The
three vanilla crates (carrot, potato, beetroot) are behind the `enableVanillaCropCrates` config flag
and are **enabled on this server**. Cabbage, tomato and onion crates are unconditional but are
one-way: once packed, the only way back is the Cutting Board, covered in
[cooking.md](cooking.md).

### Sacks and bales

| Block | Packs from | Unpacks to | Notes |
|---|---|---|---|
| `rice_bag` Bag of Rice | 9 Rice | 9 Rice | Mineable with a knife |
| `rice_bale` Rice Bale | 9 Rice Panicle | 9 Rice Panicle | Placeable on any axis; fall damage on it is 20% of normal |
| `straw_bale` Straw Bale | 9 Straw | 9 Straw | Hay-block behaviour; burns readily (fire spread 60, flammability 20) |

Rice Bale takes a full facing property, so it can be laid on any of six axes rather than the three a
hay bale allows, and it dampens fall damage the same way hay does. Straw Bale is a `HayBlock`
subclass and keeps hay's fall damage reduction.

### Baskets

`wooden_basket` (displayed **Basket**) and `bamboo_basket` (**Bamboo Basket**) are 27-slot
hopper-variants: they push items in whatever direction they face, on the same 8-tick cooldown as a
vanilla hopper, are disabled by a redstone signal, are waterloggable, drop their contents when
broken and emit a comparator signal. Their recipes and their role as a cooking-station output are in
[cooking.md](cooking.md).

## Decoration and building blocks

### Materials

| Item | Source | Furnace burn time |
|---|---|---|
| `straw` Straw | Loot modifiers on tall grass and mature rice — see [loot-and-worldgen.md](loot-and-worldgen.md) | 5 s |
| `canvas` Canvas | 4 Straw in a 2×2 | 20 s |
| `tree_bark` Tree Bark | Stripping any log or wood on a Cutting Board with an axe | 10 s |

Non-obvious things these three make:

| Result | Station | Ingredients |
|---|---|---|
| Lead | Crafting table | 5 Straw, in the vanilla lead pattern |
| 2 Packed Mud | Crafting table | 1 Straw + 2 Mud, shapeless |
| Book | Crafting table | 3 Paper + 1 Canvas, shapeless |
| Painting | Crafting table | 8 Sticks around 1 Canvas |
| 6 Scaffolding | Crafting table | 6 Bamboo + 1 Canvas (`b#b / b·b / b·b`) |
| Paper | Crafting table | 3 Tree Bark, shapeless |
| Organic Compost | Crafting table | Dirt + 2 Straw + 2 Bone Meal + 4 Tree Bark, shapeless |
| Organic Compost | Crafting table | Dirt + 2 Rotten Flesh + 2 Straw + 4 Bone Meal, shapeless |

Organic Compost and the Rich Soil it becomes are covered in [farming.md](farming.md).

### Floor coverings

| Block | Recipe | Notes |
|---|---|---|
| `canvas_rug` Canvas Rug | 1 Canvas → 2 Rugs, shapeless; 2 Rugs → 1 Canvas reverses it | 1 pixel tall, does not block light, wool sounds |
| `tatami` Tatami Block | 2 Canvas + 2 Straw in a checker (`cs / sc`) → 2 blocks; also 2 Full Mats, shapeless | Full-height block with a `paired` state that merges the texture with a neighbour |
| `full_tatami_mat` Full Tatami Mat | 1 Tatami Block → 2 Mats; also 2 Half Mats, shapeless | Two-block bed-style block (`head`/`foot` parts), 2 pixels tall |
| `half_tatami_mat` Half Tatami Mat | 1 Full Mat → 2 Half Mats, shapeless | Single block, 2 pixels tall, destroyed by pistons |

Both mat forms break if the block beneath them is removed. All four are in the
`farmersdelight:straw_blocks` tag and so are quick to remove with a knife.

### Safety net

`safety_net` Safety Net — 4 Rope in a 2×2. Crafting one back yields 4 Rope.

A 2-pixel-thick platform at mid-block height. Anything that lands on it **takes no fall damage and
bounces**, keeping 60% of its downward velocity if it is a living entity and 80% if it is not.
Sneaking cancels both effects: a sneaking entity lands on it normally and takes normal fall damage.
Waterloggable.

### Rope fences

| Block | Recipe |
|---|---|
| `rope_fence` Rope Fence | 4 Rope + 2 Sticks (`r/r` twice) → 3 |
| `rope_fence_gate` Rope Fence Gate | 2 Rope + 4 Sticks (`/r/` twice) → 1 |

Standard fence and fence gate behaviour on a 1.0 hardness.

### Fuel values

Anything below that is not otherwise noted burns in a furnace for the listed time. This is a
property of the *item*, so it applies to the block form in a furnace slot.

| Item | Burn time |
|---|---|
| Straw Bale | 50 s |
| Canvas, Tatami Block | 20 s |
| Basket, Bamboo Basket, the nine wooden cabinets | 15 s |
| Tree Bark, Cutting Board, Safety Net, Canvas Rug, Rope, Rope Fence, Rope Fence Gate, Full Tatami Mat | 10 s |
| Straw, Half Tatami Mat | 5 s |

Crimson and Warped cabinets are plain block items and are **not** furnace fuel, matching their
nether-wood ingredients.

## Canvas signs, and how dyeing works

Canvas signs come in 17 colours — undyed plus the 16 dyes — and each colour exists in four block
forms:

| Form | Registry pattern | Example |
|---|---|---|
| Standing | `canvas_sign`, `<colour>_canvas_sign` | `red_canvas_sign` |
| Wall | `canvas_wall_sign`, `<colour>_canvas_wall_sign` | `red_canvas_wall_sign` |
| Hanging | `hanging_canvas_sign`, `<colour>_hanging_canvas_sign` | `red_hanging_canvas_sign` |
| Wall hanging | `wall_hanging_canvas_sign`, `<colour>_wall_hanging_canvas_sign` | `red_wall_hanging_canvas_sign` |

Only two of the four are items: the standing form and the hanging form. The wall forms are placement
states of the same item and inherit their drops from the standing/hanging block, which is why they
have no loot table of their own.

**Dyeing is a crafting recipe, not an in-world interaction.** There is no dye-on-placed-sign path
anywhere in the code. To recolour, combine any sign in `farmersdelight:canvas_signs` (or
`farmersdelight:hanging_canvas_signs`) with one dye of the target colour, shapeless — so a sign can
be recoloured repeatedly, and the undyed sign is only the starting point, not a required input.

Base recipes:

| Result | Station | Ingredients |
|---|---|---|
| 3 Canvas Sign | Crafting table | 4 planks (any, `#minecraft:planks`) + 2 Canvas + 1 Stick (`w#w / w#w / ·/·`) |
| 6 Hanging Canvas Sign | Crafting table | 4 logs (any, `#minecraft:logs`) + 2 Canvas + 2 Chain (`X·X / w#w / w#w`) |
| 1 coloured sign | Crafting table | 1 canvas sign of any colour + 1 matching dye, shapeless |

**Text colour on dark backgrounds.** When a canvas sign whose background dye is in the
`canvasSignDarkBackgroundList` config is placed, its text defaults to white instead of black. The
server runs the stock list: gray, purple, blue, brown, green, red, black. The other nine dyes and
the undyed sign get black text.

Canvas signs otherwise behave as vanilla signs — waxable, editable on both faces, glow ink works.

## Rope and its interactions

`rope` Rope — 2 Straw stacked vertically yields 4. Breaking a Safety Net returns 4 Rope.

Rope is an `IronBarsBlock` variant with **no collision box at all**, so entities and players fall
straight through a rope column; it is not a ladder and does not let you climb. Its only solid part
is a 2×1×2 pixel nub used as a support surface.

**Placement chains downward.** Placing a rope onto an existing rope walks down the column and places
the new rope at the bottom of it, so a rope line is extended from the top by clicking the block you
can already reach. Placing against a side face walks in that direction instead. The walk stops at
the first block that is not rope, and fails outright if that block is neither air nor water-filled
and placeable.

**Connecting.** Rope connects sideways to other rope, to iron bars and glass panes, and to anything
in `minecraft:walls`; when placed against a horizontal face it will also tie to any solid face. It
is waterloggable.

**Bells.** A rope hanging beneath a bell gets a `tied_to_bell` state. Right-clicking anywhere on
that rope column with an empty hand, up to 24 rope blocks below the bell, rings it.

**Reeling.** With `enableRopeReeling` on (the server default), sneak-right-clicking a rope with an
empty hand removes the **bottom-most** rope of the column and returns it, so a line can be shortened
from the top. It requires inventory space, or creative mode. Ringing the bell and reeling are
mutually exclusive on the same click: sneak reels, a plain click rings.

**Tomato vines climb rope.** With `enableTomatoVineClimbingTaggedRopes` on (server default), a
tomato crop will climb any block in the `farmersdelight:ropes` tag — this mod's rope plus Quark's
and Supplementaries' if present — and converts it to `farmersdelight:rope` in the process. See
[farming.md](farming.md) for the trellis mechanic itself.

The `farmersdelight:ropes` tag: `farmersdelight:rope`, plus optional entries for `quark:rope` and
`supplementaries:rope`. Neither of those two mods is on this server, so the tag resolves to one
block.

## Everything else registered

| Entry | What it is |
|---|---|
| `rotten_tomato` Rotten Tomato | Not food. A throwable projectile, stacks to 16. Right-click throws it at velocity 1.5; on hit it deals **0 damage** (the damage call is made with an amount of 0.0, so the target registers the thrower as an attacker but loses no health), plays a splat and bursts into item particles. |
| `horse_feed` Horse Feed | Stacks to 16. Fed to any tamed mount in `farmersdelight:horse_feed_users`: fully heals it and applies Speed II and Jump Boost I for 5 minutes each. Mobs in `farmersdelight:horse_feed_tempted` will follow a player holding it. Recipe: Hay Block **or** Rice Bale + 2 Apples + 1 Golden Carrot, shapeless. |
| `pumpkin_pie` (block) | The mod replaces vanilla Pumpkin Pie's block form. Its pick-block returns the vanilla `minecraft:pumpkin_pie` item, so the block is invisible to players. `enablePumpkinPieSneakToPlace` is **false** on this server, meaning a plain right-click places the pie as a block. |
| `sandy_shrub` Sandy Shrub | Decorative desert plant, no recipe; obtained from worldgen — see [farming.md](farming.md). |
| `organic_compost`, `rich_soil`, `rich_soil_farmland` | Soil chain; recipes above, mechanics in [farming.md](farming.md). |
| `brown_mushroom_colony`, `red_mushroom_colony` | Multi-mushroom growth blocks — [farming.md](farming.md). |
| `nourishment`, `comfort` | The two mob effects — [foods-and-effects.md](foods-and-effects.md). |
| `farmersdelight:stove_burn` | Damage type used by the Stove — [cooking.md](cooking.md). |
| `rotten_tomato` (entity) | The projectile entity behind the item above. Size 0.25³, tracking range 4, update interval 10. |

Rabbits are given a tempt goal for Cabbage and Cabbage Leaf on spawn, alongside the Horse Feed
tempt goal — the only two AI injections the mod makes.

## Registered but unreachable

The set-diff of every `register("…")` literal against `en_us.json` and the mod's recipe and loot
trees turns up exactly one item and one orphan string.

**`debug_pumpkin_pie`** — registered through `registerHidden`, so it is absent from the creative
tab. It has **no lang key** (it renders as the raw translation key
`item.farmersdelight.debug_pumpkin_pie`), **no recipe**, and **no loot table entry**. It is a
`BlockItem` for the mod's `pumpkin_pie` block whose tooltip reads "Debug item - Not meant for
gameplay". The only way to obtain it is `/give … farmersdelight:debug_pumpkin_pie`. It exists so a
developer can place the pie block without the vanilla item's pick-block override in the way; it has
no gameplay function and should be treated as not present.

**`item.farmersdelight.earthworm` = "Earthworm"** — a translation string with no item, block,
entity or recipe behind it anywhere in the jar. Nothing in the mod ever displays it. It is either a
leftover from a removed item or a placeholder for an unreleased one; either way there is no Earthworm
in this version.

Everything else that has no recipe of its own has an obvious reachable path: the 34 wall-sign blocks
are placement states that draw their drops from the standing forms via `lootFrom(…)`; the feast
serving items (`roast_chicken`, `honey_glazed_ham`, `shepherds_pie`, `stuffed_pumpkin`,
`gleaming_salad`) come from eating their block forms; `budding_tomatoes` and `tomatoes_on_rope` are
crop growth stages; `sandy_shrub` and `rich_soil` come from worldgen and composting respectively.

## Config affecting this doc

Every option below is **byte-identical to the mod default** in the live
`/config/farmersdelight-common.toml`.

| Option | Value | Effect here |
|---|---|---|
| `enableRopeReeling` | `true` | Sneak-use with an empty hand reels rope back |
| `canvasSignDarkBackgroundList` | `["gray","purple","blue","brown","green","red","black"]` | These seven dyes default new signs to white text |
| `enableTomatoVineClimbingTaggedRopes` | `true` | Tomatoes climb any `farmersdelight:ropes` block |
| `defaultTomatoVineRope` | `"farmersdelight:rope"` | What a broken tomato vine leaves behind |
| `enableVanillaCropCrates` | `true` | Carrot, Potato and Beetroot crates are craftable |
| `enablePumpkinPieSneakToPlace` | `false` | A plain right-click places Pumpkin Pie as a block |
| `enableTomatoRopePermanence` | `true` | Tomato-on-rope force-places a Rope block when broken; this is the documented cause of `/setblock` failing on those positions on the first attempt |
