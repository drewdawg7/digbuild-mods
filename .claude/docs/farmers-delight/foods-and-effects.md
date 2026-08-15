<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Foods, Feasts, Effects and Damage

Covers all **77 edible items** and 3 non-food drinks, the 6 feast blocks and 4
pie blocks, the mod's 2 status effects, its 1 custom damage type, its 1
`weapon_attributes` file, and the config options on this server that change any
of it.

Sources: `FarmersDelight-1.20.1-1.3.2.jar`, pulled from the live server's
`/mods` and decompiled with [jadx 1.5.4](https://github.com/skylot/jadx).
Nutrition and saturation come from `common/FoodValues.java`; container items and
stack sizes from the `Item.Properties` in `common/registry/ModItems.java`;
effect behaviour from `common/effect/*.java`; recipes, loot modifiers, tags, the
damage type and the weapon-attribute file from the jar's `data/` tree; display
names from `assets/farmersdelight/lang/en_us.json`. Config values are the live
`/config/farmersdelight-common.toml`.

## SRG mapping — verified, it held

jadx leaves SRG names on the vanilla food builder. Every mapping used here was
confirmed line-by-line against the clean upstream source
([`vectorwing/FarmersDelight`](https://github.com/vectorwing/FarmersDelight),
branch `1.20`, whose `gradle.properties` carries `mod_version=1.3.2` — the exact
jar on this server), where `FoodValues.java` has the same declaration order:

| SRG | Method | Confirmed by |
|---|---|---|
| `m_38760_(int)` | `nutrition` | `CABBAGE` = `nutrition(2).saturationMod(0.4f)` |
| `m_38758_(float)` | `saturationMod` | same |
| `m_38757_()` | `meat` | `MINCED_BEEF` = `.meat().fast()` |
| `m_38766_()` | `fast` | same |
| `m_38765_()` | `alwaysEat` | `APPLE_CIDER` = `.alwaysEat()` |
| `m_38767_()` | `build` | every entry |
| `m_41489_(FoodProperties)` | `Item.Properties.food` | `foodItem()` helper |
| `m_41495_(Item)` | `Item.Properties.craftRemainder` | `bowlFoodItem()` = `craftRemainder(Items.BOWL).stacksTo(16)` |
| `m_41487_(int)` | `Item.Properties.stacksTo` | same |

**Every nutrition and saturation figure in the decompiled file matches upstream
exactly** — all 73 `FoodProperties` constants, checked as a set, not by spot
check. The vanilla effect constants resolved the same way: `f_19617_`
ABSORPTION, `f_19612_` HUNGER, `f_19596_` MOVEMENT_SPEED, `f_19605_`
REGENERATION, `f_19619_` GLOWING, `f_19604_` CONFUSION (Nausea), `f_19603_`
JUMP, `f_19600_` DAMAGE_BOOST, `f_19606_` DAMAGE_RESISTANCE — the last three
pinned by `DogFoodItem`/`HorseFeedItem`, which upstream declare
`MOVEMENT_SPEED, DAMAGE_BOOST, DAMAGE_RESISTANCE` and `MOVEMENT_SPEED, JUMP` in
that order. Nothing below rests on an inferred name.

## How the numbers work

- **Saturation restored = nutrition × saturation modifier × 2.** The
  "saturation modifier" in the table is the builder value, not the number of
  saturation points; the third column is the points. Vanilla clamps the result:
  `FoodData` stores `min(saturation + restored, foodLevel)`, so a meal eaten on
  a nearly-full hunger bar cannot bank more saturation than the food level it
  leaves you at (20 max).
- **Nutrition** is in half-shanks: 14 nutrition fills seven of the ten hunger
  icons.
- **Meat** matters for wolves (and for any mod that filters on `FoodProperties.isMeat`).
- **Duration** is converted from ticks; the four shared constants are
  `BRIEF 600t = 30 s`, `SHORT 1200t = 60 s`, `MEDIUM 3600t = 3:00`,
  `LONG 6000t = 5:00`.
- **Container** is the item handed back when you finish eating
  (`craftRemainder`). Bowl meals also stack to 16 instead of 64.
- **Fast** foods (marked in notes) take 16 ticks to eat instead of 32.

## Every food item

Effect chances are the per-eat roll from the `FoodProperties` builder. Where a
row says Nourishment, that is this mod's own effect — see
[Status effects](#status-effects).

### Crops

| Item | Registry id | Nutr. | Sat. mod | Saturation | Meat | Effect | Stack | Container |
|---|---|---|---|---|---|---|---|---|
| Cabbage | `farmersdelight:cabbage` | 2 | 0.4 | 1.6 | no | — | 64 | — |
| Tomato | `farmersdelight:tomato` | 1 | 0.3 | 0.6 | no | — | 64 | — |
| Onion | `farmersdelight:onion` | 2 | 0.4 | 1.6 | no | — | 64 | — |

Rice and Rice Panicle are not edible. Onion doubles as its own seed
(`ItemNameBlockItem`).

### Cut on a cutting board

Every row here comes from a `farmersdelight:cutting` recipe with a knife
(`forge:tools/knives`), except Ham, which is a kill drop.

| Item | Registry id | Nutr. | Sat. mod | Saturation | Meat | Effect | Stack | Container |
|---|---|---|---|---|---|---|---|---|
| Cabbage Leaf | `farmersdelight:cabbage_leaf` | 1 | 0.4 | 0.8 | no | — | 64 | — |
| Minced Beef | `farmersdelight:minced_beef` | 2 | 0.3 | 1.2 | **yes** | — | 64 | — |
| Raw Chicken Cuts | `farmersdelight:chicken_cuts` | 1 | 0.3 | 0.6 | **yes** | Hunger 30 s, **30%** | 64 | — |
| Raw Bacon | `farmersdelight:bacon` | 2 | 0.3 | 1.2 | **yes** | — | 64 | — |
| Raw Cod Slice | `farmersdelight:cod_slice` | 1 | 0.1 | 0.2 | no | — | 64 | — |
| Raw Salmon Slice | `farmersdelight:salmon_slice` | 1 | 0.1 | 0.2 | no | — | 64 | — |
| Raw Mutton Chops | `farmersdelight:mutton_chops` | 1 | 0.3 | 0.6 | **yes** | — | 64 | — |
| Pumpkin Slice | `farmersdelight:pumpkin_slice` | 3 | 0.3 | 1.8 | no | — | 64 | — |
| Raw Pasta | `farmersdelight:raw_pasta` | 2 | 0.3 | 1.2 | no | Hunger 30 s, **30%** | 64 | — |
| Kelp Roll Slice | `farmersdelight:kelp_roll_slice` | 6 | 0.5 | 6 | no | — | 64 | — |
| Ham | `farmersdelight:ham` | 5 | 0.3 | 3 | **yes** | — | 64 | — |
| Slice of Cake | `farmersdelight:cake_slice` | 2 | 0.1 | 0.4 | no | Speed 20 s, 100% | 64 | — |
| Slice of Apple Pie | `farmersdelight:apple_pie_slice` | 3 | 0.3 | 1.8 | no | Speed 30 s, 100% | 64 | — |
| Slice of Sweet Berry Cheesecake | `farmersdelight:sweet_berry_cheesecake_slice` | 3 | 0.3 | 1.8 | no | Speed 30 s, 100% | 64 | — |
| Slice of Chocolate Pie | `farmersdelight:chocolate_pie_slice` | 3 | 0.3 | 1.8 | no | Speed 30 s, 100% | 64 | — |
| Slice of Pumpkin Pie | `farmersdelight:pumpkin_pie_slice` | 3 | 0.3 | 1.8 | no | Speed 30 s, 100% | 64 | — |

Yields and sources:

- 2 cuts per raw item for beef → Minced Beef, chicken → Raw Chicken Cuts (+1
  bone meal), porkchop → Raw Bacon, cod and salmon → slices (+1 bone meal),
  mutton → Raw Mutton Chops. Cutting the **cooked** vanilla item gives 2 of the
  cooked cut directly.
- Cabbage → 2 Cabbage Leaf; Pumpkin → 4 Pumpkin Slice; any `forge:dough` → 1 Raw
  Pasta; Kelp Roll → 3 slices.
- Pies cut into **4** slices, Cake into **7** (`slicing_cake` loot modifier
  applies the same to a placed Cake or Candle Cake struck with a knife).
- **Ham** is a kill drop, not a recipe: killing a **Hoglin** with a knife in the
  main hand while the hoglin is *not* on fire drops Ham at 100%; a **Pig** under
  the same conditions drops it at **50%, +10 percentage points per Looting
  level**. Kill either while it *is* on fire and you get Smoked Ham instead.
- Every row in this table except Pumpkin Slice, Raw Pasta and Ham is a `fast`
  food (16 ticks to eat instead of 32).
- The four pie/cake slices apply Speed with `showParticles = false` and
  `showIcon = false` — the buff is real but invisible.

### Cooked over heat (furnace, smoker, campfire, skillet)

The Skillet cooks `minecraft:campfire_cooking` recipes, so anything in this
group can be made in a skillet as well as on a campfire.

| Item | Registry id | Nutr. | Sat. mod | Saturation | Meat | Effect | Stack | Container |
|---|---|---|---|---|---|---|---|---|
| Fried Egg | `farmersdelight:fried_egg` | 4 | 0.4 | 3.2 | no | — | 64 | — |
| Beef Patty | `farmersdelight:beef_patty` | 4 | 0.8 | 6.4 | **yes** | — | 64 | — |
| Cooked Chicken Cuts | `farmersdelight:cooked_chicken_cuts` | 3 | 0.6 | 3.6 | **yes** | — | 64 | — |
| Cooked Bacon | `farmersdelight:cooked_bacon` | 4 | 0.8 | 6.4 | **yes** | — | 64 | — |
| Cooked Cod Slice | `farmersdelight:cooked_cod_slice` | 3 | 0.5 | 3 | no | — | 64 | — |
| Cooked Salmon Slice | `farmersdelight:cooked_salmon_slice` | 3 | 0.8 | 4.8 | no | — | 64 | — |
| Cooked Mutton Chops | `farmersdelight:cooked_mutton_chops` | 3 | 0.8 | 4.8 | **yes** | — | 64 | — |
| Smoked Ham | `farmersdelight:smoked_ham` | 10 | 0.8 | 16 | **yes** | — | 64 | — |

Every row here is `fast` except **Fried Egg** and Smoked Ham. At 10 nutrition
/ 16 saturation it is the densest single food in the mod that is not a meal.
Smoked Ham has a **smoking-only** recipe (Ham → Smoked Ham); it has no furnace
or campfire variant, though the burning-hoglin drop above also produces it.

### Cooked in a cooking pot

| Item | Registry id | Nutr. | Sat. mod | Saturation | Meat | Effect | Stack | Container |
|---|---|---|---|---|---|---|---|---|
| Apple Cider | `farmersdelight:apple_cider` | 0 | 0.0 | 0 | no | Absorption 60 s, 100% | 16 | Glass Bottle |
| Tomato Sauce | `farmersdelight:tomato_sauce` | 4 | 0.4 | 3.2 | no | — | 64 | Bowl |
| Glow Berry Custard | `farmersdelight:glow_berry_custard` | 7 | 0.6 | 8.4 | no | Glowing 5 s, 100% | 16 | Glass Bottle |
| Cooked Rice | `farmersdelight:cooked_rice` | 6 | 0.4 | 4.8 | no | Nourishment 30 s, 100% | 16 | Bowl |
| Bone Broth | `farmersdelight:bone_broth` | 8 | 0.7 | 11.2 | no | Nourishment 60 s, 100% | 16 | Bowl |
| Beef Stew | `farmersdelight:beef_stew` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Vegetable Soup | `farmersdelight:vegetable_soup` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Fish Stew | `farmersdelight:fish_stew` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Onion Soup | `farmersdelight:onion_soup` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Chicken Soup | `farmersdelight:chicken_soup` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Fried Rice | `farmersdelight:fried_rice` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Mushroom Rice | `farmersdelight:mushroom_rice` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Pasta with Meatballs | `farmersdelight:pasta_with_meatballs` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Pasta with Mutton Chop | `farmersdelight:pasta_with_mutton_chop` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Ratatouille | `farmersdelight:ratatouille` | 10 | 0.6 | 12 | no | Nourishment 60 s, 100% | 16 | Bowl |
| Pumpkin Soup | `farmersdelight:pumpkin_soup` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Baked Cod Stew | `farmersdelight:baked_cod_stew` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Noodle Soup | `farmersdelight:noodle_soup` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Vegetable Noodles | `farmersdelight:vegetable_noodles` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Squid Ink Pasta | `farmersdelight:squid_ink_pasta` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Cabbage Rolls | `farmersdelight:cabbage_rolls` | 5 | 0.5 | 5 | no | — | 64 | — |
| Dumplings | `farmersdelight:dumplings` | 8 | 0.8 | 12.8 | no | — | 64 | — |
| Dog Food | `farmersdelight:dog_food` | 4 | 0.2 | 1.6 | **yes** | — | 16 | Bowl |

Notes:

- **Apple Cider has no nutrition at all.** It is `alwaysEat` — drinkable on a
  full hunger bar — and exists purely for 60 s of Absorption.
- **Dog Food** is edible by players for 4 nutrition, but its purpose is
  right-clicking a **tamed** entity in `#farmersdelight:dog_food_users`: that
  sets the animal to full health and applies **Speed I, Strength I and
  Resistance I for 5:00 each**. The bowl is returned to the feeder.
- **Horse Feed** (`farmersdelight:horse_feed`, crafted, stacks to 16) is the
  same pattern but is **not edible at all** — no `FoodProperties`. Used on a
  tamed entity in `#farmersdelight:horse_feed_users` it heals it to full and
  applies **Speed II and Jump Boost I for 5:00**. It is consumed with no
  container returned, and entities in `#farmersdelight:horse_feed_tempted` get a
  tempt goal for it.
- Cabbage Rolls and Dumplings are pot recipes with no bowl container (they are
  plain items, stack 64).
- The Stuffed Pumpkin **block** is also a cooking-pot output; its servings are
  listed under [Feasts](#feasts).

### Assembled at a crafting table

| Item | Registry id | Nutr. | Sat. mod | Saturation | Meat | Effect | Stack | Container |
|---|---|---|---|---|---|---|---|---|
| Wheat Dough | `farmersdelight:wheat_dough` | 2 | 0.3 | 1.2 | no | Hunger 30 s, **30%** | 64 | — |
| Pie Crust | `farmersdelight:pie_crust` | 2 | 0.2 | 0.8 | no | — | 64 | — |
| Sweet Berry Cookie | `farmersdelight:sweet_berry_cookie` | 2 | 0.1 | 0.4 | no | — | 64 | — |
| Honey Cookie | `farmersdelight:honey_cookie` | 2 | 0.1 | 0.4 | no | — | 64 | — |
| Melon Popsicle | `farmersdelight:melon_popsicle` | 3 | 0.2 | 1.2 | no | — | 64 | — |
| Fruit Salad | `farmersdelight:fruit_salad` | 6 | 0.6 | 7.2 | no | Regeneration 5 s, 100% | 16 | Bowl |
| Mixed Salad | `farmersdelight:mixed_salad` | 6 | 0.6 | 7.2 | no | Regeneration 5 s, 100% | 16 | Bowl |
| Nether Salad | `farmersdelight:nether_salad` | 5 | 0.4 | 4 | no | Nausea 12 s, **30%** | 16 | Bowl |
| Barbecue on a Stick | `farmersdelight:barbecue_stick` | 8 | 0.9 | 14.4 | no | — | 64 | — |
| Egg Sandwich | `farmersdelight:egg_sandwich` | 8 | 0.8 | 12.8 | no | — | 64 | — |
| Chicken Sandwich | `farmersdelight:chicken_sandwich` | 10 | 0.8 | 16 | no | — | 64 | — |
| Hamburger | `farmersdelight:hamburger` | 11 | 0.8 | 17.6 | no | — | 64 | — |
| Bacon Sandwich | `farmersdelight:bacon_sandwich` | 10 | 0.8 | 16 | no | — | 64 | — |
| Mutton Wrap | `farmersdelight:mutton_wrap` | 10 | 0.8 | 16 | no | — | 64 | — |
| Stuffed Potato | `farmersdelight:stuffed_potato` | 10 | 0.7 | 14 | no | — | 64 | — |
| Salmon Roll | `farmersdelight:salmon_roll` | 7 | 0.6 | 8.4 | no | — | 64 | — |
| Cod Roll | `farmersdelight:cod_roll` | 7 | 0.6 | 8.4 | no | — | 64 | — |
| Kelp Roll | `farmersdelight:kelp_roll` | 12 | 0.6 | 14.4 | no | — | 64 | — |
| Bacon and Eggs | `farmersdelight:bacon_and_eggs` | 10 | 0.6 | 12 | no | Nourishment 60 s, 100% | 16 | Bowl |
| Steak and Potatoes | `farmersdelight:steak_and_potatoes` | 12 | 0.8 | 19.2 | no | Nourishment 3:00, 100% | 16 | Bowl |
| Grilled Salmon | `farmersdelight:grilled_salmon` | 14 | 0.75 | 21 | no | Nourishment **3:00**, 100% | 16 | Bowl |
| Roasted Mutton Chops | `farmersdelight:roasted_mutton_chops` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |

Notes:

- **None of the sandwiches, wraps, rolls or the Barbecue Stick counts as meat**,
  even the meat-filled ones — `meat()` is only set on the raw/cooked cuts, Ham,
  Smoked Ham and Dog Food.
- **Grilled Salmon is the odd one out**: 14 nutrition like the 5:00 plates, but
  its Nourishment is MEDIUM (3:00). That is the value in both the jar and
  upstream, not a transcription slip.
- **Melon Popsicle** extinguishes the eater (`clearFire()`) on top of its food
  value, and is `fast` + `alwaysEat`. Both cookies are `fast` as well; nothing
  else in this table is.
- **Kelp Roll takes 64 ticks (3.2 s) to eat**, double a normal food; its slices
  are `fast` at 16 ticks.
- The 4 uncut pies (Apple Pie, Sweet Berry Cheesecake, Chocolate Pie, plus
  vanilla Pumpkin Pie) and the 5 feast blocks are crafted here too but are
  blocks, not foods — see below.

### Feast servings

Only obtainable by taking a serving from the matching feast block.

| Item | Registry id | Nutr. | Sat. mod | Saturation | Meat | Effect | Stack | Container |
|---|---|---|---|---|---|---|---|---|
| Plate of Roast Chicken | `farmersdelight:roast_chicken` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Bowl of Stuffed Pumpkin | `farmersdelight:stuffed_pumpkin` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Plate of Honey Glazed Ham | `farmersdelight:honey_glazed_ham` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Plate of Shepherd's Pie | `farmersdelight:shepherds_pie` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |
| Bowl of Gleaming Salad | `farmersdelight:gleaming_salad` | 14 | 0.75 | 21 | no | Nourishment 5:00, 100% | 16 | Bowl |

The Rice Roll Medley serves Cod Roll, Salmon Roll and Kelp Roll Slice, which are
listed in the crafting-table and cutting-board groups above.

### Drinks that are not food

These three have **no `FoodProperties` at all** — no nutrition, no saturation,
and they can be drunk at any hunger level because the game never checks. They
stack to 16 and return a Glass Bottle.

| Item | Registry id | Effect on drinking |
|---|---|---|
| Milk Bottle | `farmersdelight:milk_bottle` | Removes **one** effect, picked at random from the drinker's active effects that milk can cure. Not all of them — one. |
| Hot Cocoa | `farmersdelight:hot_cocoa` | Same, but the candidate list is filtered to `MobEffectCategory.HARMFUL` only. Cooking-pot recipe. |
| Melon Juice | `farmersdelight:melon_juice` | Heals **2 HP** (1 heart) immediately. |

Both bottles respect Forge's `MobEffectEvent.Remove`, and both use each effect's
own `isCurativeItem(milk_bucket)` check, so a modded effect that declares itself
uncurable by milk is skipped.

## Feasts

Six blocks are tagged `#farmersdelight:feasts`. All are placed from an item,
carry a `servings` blockstate, and are eaten by right-clicking the block, which
hands you a serving item — you then eat that item normally.

| Block | Servings | Serving item | Container needed | Empty block | Light |
|---|---|---|---|---|---|
| `farmersdelight:roast_chicken_block` | 4 | Plate of Roast Chicken | **Bowl** | stays as an empty tray | — |
| `farmersdelight:stuffed_pumpkin_block` | 4 | Bowl of Stuffed Pumpkin | **Bowl** | **breaks immediately** | — |
| `farmersdelight:honey_glazed_ham_block` | 4 | Plate of Honey Glazed Ham | **Bowl** | stays as an empty tray | — |
| `farmersdelight:shepherds_pie_block` | 4 | Plate of Shepherd's Pie | **Bowl** | stays as an empty tray | — |
| `farmersdelight:gleaming_salad_block` | 4 | Bowl of Gleaming Salad | **Bowl** | stays as an empty tray | servings × 3 |
| `farmersdelight:rice_roll_medley_block` | **8** | see below | none | stays as an empty tray | — |

Mechanics, from `FeastBlock.takeServing`:

- **The container is mandatory and consumed.** If the serving item has a
  crafting remainder (a Bowl, for every feast except the Rice Roll Medley), you
  must be holding that exact item; one is taken from your hand and the serving
  is given back. Holding anything else prints *"You need a Bowl to eat this."*
  and nothing happens. Creative players are exempt from the consumption.
- **Last serving.** `hasLeftovers` decides what happens at 0 servings. Stuffed
  Pumpkin has `hasLeftovers = false`: taking the fourth serving destroys the
  block on the spot. The other five leave a `servings=0` block behind; the
  *next* right-click on it destroys it with drops.
- **Breaking a partly-eaten feast gives you a single Bowl**, not the feast item.
  The block loot table only returns the feast block itself when `servings` is at
  its maximum, and otherwise drops `minecraft:bowl` — except Stuffed Pumpkin,
  whose table has no second pool, so **a partly eaten Stuffed Pumpkin that is
  broken drops nothing at all**.
- **Direction is cosmetic.** `FACING` is set on placement to the opposite of the
  player's facing and is only read for the collision/render shape (and for the
  Rice Roll Medley's two axis-aligned shapes). It never affects servings or who
  can eat.
- Comparators read the block: output = servings remaining.
- Serving particles fire for every feast except the Rice Roll Medley. The
  Gleaming Salad additionally emits sparkles at `0.05 × servings` chance per
  client tick and emits **light level = servings × 3** (12 when full, 0 when
  empty).

**Rice Roll Medley** is the exception on every axis: 8 servings, no container
needed, and the serving item depends on how far down the platter you are. The
list is indexed by `servings − 1`, so servings come off in this order:

| Serving taken | State before | Item given |
|---|---|---|
| 1st–3rd | 8, 7, 6 | Kelp Roll Slice |
| 4th–6th | 5, 4, 3 | Salmon Roll |
| 7th–8th | 2, 1 | Cod Roll |

### Pies are a different mechanic

Apple Pie, Sweet Berry Cheesecake, Chocolate Pie and (via FD's override)
Pumpkin Pie are `PieBlock`s, not feasts. They have **4 bites**, no `servings`
property, and two distinct interactions:

- **Bare hand / anything that is not a knife:** you eat a bite in place. The
  slice's nutrition, saturation and effects are applied directly to you and *no
  item is produced*. This bypasses the normal eating animation entirely.
- **With a knife:** a slice item is cut off and drops in front of you, and you
  eat nothing.

Either way the block advances one bite and is removed after the fourth.
Comparator output = bites remaining. Facing is set to the placing player's
horizontal direction, and only affects which quadrant renders as eaten.

## Status effects

The mod registers **2 effects** and the lang file has **4 `effect.*` keys** —
that is a name plus a `.description` for each, not a mismatch. Set-diffed
`EFFECTS.register("…")` literals in `ModEffects` against the lang keys:

| Check | Result |
|---|---|
| `EFFECTS.register()` literals | 2 — `nourishment`, `comfort` |
| `effect.farmersdelight.<id>` name keys | 2 |
| `effect.farmersdelight.<id>.description` keys | 2 |
| Registered effects missing either key | **none** |
| Keys with no registered effect | **none** |

Unlike Alex's Mobs, neither class overrides `getDescriptionId`, so
`effect.farmersdelight.<id>` really is the in-game display name.

| ID | Display name | Category | Colour |
|---|---|---|---|
| `farmersdelight:nourishment` | Nourishment | **buff** (BENEFICIAL) | `#F3B300` |
| `farmersdelight:comfort` | Comfort | **buff** (BENEFICIAL) | `#A6EBFF` |

Both categories are read straight from the `MobEffectCategory` argument to the
`MobEffect` constructor. **Neither is NEUTRAL and neither is HARMFUL.** Neither
effect registers an attribute modifier, and neither reads its amplifier — there
is no level II of either, and a higher amplifier changes nothing.

### Nourishment — what it actually does

**It does not feed you and it does not add saturation.** Its tick handler
(`isDurationEffectTick` returns true, so it runs every tick, server-side, on
players only) sets the player's **exhaustion to 0** each tick. Exhaustion is the
counter that drains saturation and then hunger, so zeroing it freezes the hunger
bar where it is.

The one exception is written into the same tick:

```
isPlayerHealingWithSaturation =
    gamerule naturalRegeneration is on
    AND the player is hurt
    AND saturation > 0
```

When that is true the effect **pauses** and lets exhaustion accumulate normally,
so fast saturation-healing still works and still costs you. When it is false —
at full health, or once saturation has run out — exhaustion is pinned at 0.

Consequences worth stating plainly:

- With Nourishment up and no saturation left, **slow natural regeneration heals
  you for free**: it costs exhaustion, and exhaustion is being zeroed.
- A separate mixin (`NourishmentAlwaysEatMixin`, injected at the head of
  `Player.canEat`) makes **every food edible at a full hunger bar while
  Nourishment is active**. That is how you top a meal up mid-effect.
- The gilded overlay on the hunger bar is client config
  `enableNourishmentHungerOverlay`.

Sources: every bowl meal, plate and feast serving in the tables above, at 100%
chance, for 30 s / 60 s / 3:00 / 5:00 depending on the dish. Plus, gated on
`enableVanillaSoupExtraEffects` (**true** here), three vanilla foods:

| Vanilla food | Nourishment |
|---|---|
| Mushroom Stew | 3:00 |
| Beetroot Soup | 3:00 |
| Rabbit Stew | 5:00 |

Rabbit Stew separately gets **Jump Boost II for 10 s** from
`enableRabbitStewJumpBoost` (**true** here). Both are applied in a
`LivingEntityUseItemEvent.Finish` handler, so they land on any living entity
that finishes eating the item, not just players.

### Comfort — what it actually does

Comfort heals **1 HP every 80 ticks (4 s)** — `isDurationEffectTick` returns
`duration % 80 == 0` — but only when all of these hold:

- the entity does **not** have vanilla Regeneration;
- if it is a player, its **saturation is 0**;
- its health is below maximum.

So it is a floor, not a boost: it keeps slow healing running when you have
nothing left to burn, and does nothing while you are already regenerating by any
other means. It ignores its amplifier entirely.

**Farmer's Delight 1.3.2 never applies Comfort.** The class constructor is
`@Deprecated` ("no longer used in Farmer's Delight, and will be removed in the
next minor release. Use Nourishment instead"), and a full grep of the jar finds
no `ModEffects.COMFORT` reference outside the registry and the client-side
health overlay. No FD food, block or event grants it.

It is still obtainable on this server, from **Dungeons Delight**
(`forge-dungeonsdelight-1.20.1-1.3.0.jar`, installed), which references FD's
effect directly: **Chloropasta** grants Comfort 2:00 and **Glowberry Gelatin**
grants Comfort 3:00, both at 100%, and its **Monster Burger** converts an active
Comfort into its own Tenacity effect for the remaining duration. Full Dungeons
Delight coverage is out of scope for this document; those three call sites were
read to establish that Comfort is reachable at all.

### Interactions with the rest of the pack

- Neither effect adds an `AttributeModifier`, so **Apotheosis / Apothic
  Attributes' attribute system does not interact with them** in either
  direction. Nothing in the FD jar reads an Apotheosis or Iron's Spells class.
- Both are BENEFICIAL, so anything on this server that strips effects by
  category will treat them as buffs to be removed, not as debuffs to be cleansed.
- FD's own Hot Cocoa filters on HARMFUL, so **drinking Hot Cocoa will never
  clear your own Nourishment or Comfort**; a Milk Bottle can, since it does not
  filter by category.
- No potion, brewing recipe, tipped arrow or `#minecraft:` tag entry exists for
  either effect. The mod registers no potions at all.

## Custom damage type

One, defined as data at `data/farmersdelight/damage_type/stove_burn.json`.

| Field | Value |
|---|---|
| ID | `farmersdelight:stove_burn` |
| `message_id` | `farmersdelight.stove` |
| `exhaustion` | `0.1` |
| `scaling` | `when_caused_by_living_non_player` |
| `effects` | `burning` |

**Trigger.** Walking onto the grill surface of a **lit Stove**
(`AbstractStoveBlock.stepOn` → `burnEntitySteppingOnStove`), for **1.0 damage**
(half a heart) per step-on tick. All five of these must hold or nothing happens:
the stove is `lit`; your bounding box intersects the grilling area one block
above the stove; you are **not sneaking** (`isSteppingCarefully`, which also
covers Soul Speed-style careful movement); you are not fire-immune; and you do
**not** have Frost Walker on your boots. Frost Walker is a hard exemption —
`EnchantmentHelper.hasFrostWalker` returns before the damage call.

**What it bypasses: nothing.** The jar ships no `data/*/tags/damage_type/`
directory at all, so `farmersdelight:stove_burn` is in no damage type tag — not
`bypasses_armor`, `bypasses_shield`, `bypasses_invulnerability`,
`bypasses_effects`, `bypasses_resistance`, `bypasses_enchantments`, `is_fire`,
`is_explosion` or `no_knockback`.

Tag membership cuts both ways here, so the two halves need stating separately:

- **Armour, generic Protection, Resistance and the normal half-second
  invulnerability window all apply.** Each of those is skipped only for damage
  that *is* tagged (`bypasses_armor`, `bypasses_enchantments`,
  `bypasses_effects`, `bypasses_invulnerability`), and this type is in none of
  them, so it is ordinary attack damage and reduces normally.
- **Fire Protection and Fire Resistance do not apply.** Both are gated the other
  way, on the type *being* in `#minecraft:is_fire` —
  `ProtectionEnchantment`'s FIRE type tests `damageSource.is(IS_FIRE)`, and so
  does the Fire Resistance check — and this type is not in that tag. Worth
  calling out because `"effects": "burning"` gives it the burning hurt sound and
  death presentation, so players will reasonably assume fire gear helps. It does
  not. The only fire-shaped exemption is `fireImmune()` entities, skipped by the
  code check above.

`effects: burning` only selects the burning hurt sound and death animation; it
carries no mechanical meaning.

`scaling: when_caused_by_living_non_player` is inert here. The source is built
by `new DamageSource(type)` with **no attacking entity**, so there is never a
living non-player cause and the damage never scales with difficulty.

Death messages:

| Key | Text |
|---|---|
| `death.attack.farmersdelight.stove` | `%1$s` was grilled to perfection |
| `death.attack.farmersdelight.stove.player` | `%1$s` was thrown on the grill by Chef `%2$s` |

The `.player` variant needs a credited killer, which for a block-sourced damage
type means the last player to have damaged the victim within the credit window.

## `weapon_attributes/skillet.json`

The jar ships exactly one file under `data/farmersdelight/weapon_attributes/`:

```json
{ "parent": "bettercombat:mace" }
```

That is a **Better Combat** data registry, not a vanilla or Forge one. It tells
Better Combat to give `farmersdelight:skillet` the same swing pattern, attack
range and animation set as Better Combat's built-in mace profile. It configures
no damage or speed numbers itself — those are inherited from the parent entry
inside Better Combat's own data.

**Better Combat is not installed on this server.** The live `/mods` listing
(153 jars) contains no `bettercombat` jar, so nothing loads this registry and
the file has no effect here. The Skillet's combat stats therefore come entirely
from `SkilletItem`'s hard-coded attribute modifiers, which are unaffected by it:

| Attribute | Modifier | Result |
|---|---|---|
| `generic.attack_damage` | `+7.0` ADDITION (`5.0 + Tiers.IRON` bonus of `2.0`) | 8 attack damage |
| `generic.attack_speed` | `−3.1` ADDITION | 0.9 attack speed |
| `generic.attack_knockback` | `+1.0` ADDITION | +1 knockback |

Durability is `Tiers.IRON` (250), and the item takes 1 damage per hit.

## Config gates on this server

Read from the live `/config/farmersdelight-common.toml`. **Every option in the
file is at the mod default**, verified against the `define(...)` defaults in
`Configuration.java` (not against static field initialisers). These are the ones
that touch food or effects:

| Option | Live value | What it gates |
|---|---|---|
| `enableVanillaSoupExtraEffects` | `true` | Mushroom Stew / Beetroot Soup grant Nourishment 3:00, Rabbit Stew 5:00 |
| `enableRabbitStewJumpBoost` | `true` | Rabbit Stew additionally grants Jump Boost II for 10 s |
| `enableStackableSoupItems` | `true` | The listed vanilla soups stack to 16 and return their bowl through FD's `BowlFoodItem` mixin |
| `soupItemList` | `["minecraft:mushroom_stew", "minecraft:beetroot_soup", "minecraft:rabbit_stew"]` | Which items the above applies to; each must extend `BowlFoodItem` |
| `enablePumpkinPieSneakToPlace` | `false` | Pumpkin Pie places as a 4-bite pie block on a normal right-click, without sneaking — so **right-clicking Pumpkin Pie against a block places it instead of eating it** |
| `cuttingBoardFortuneBonus` | `0.1` | Each Fortune level adds 10 percentage points to chance-gated cutting board results (no FD *food* result is chance-gated; this is for the dye/bonus outputs) |

Nothing in the common config changes a nutrition, saturation or effect duration
value — those are all hard-coded.

Three more options live in the **client** config (`farmersdelight-client.toml`),
which is per-player and not authoritative from the server: the Nourishment
hunger overlay, the Comfort health overlay, and `enableFoodEffectTooltip`, which
draws the "when eaten" effect lines on FD food tooltips. All three default to
`true`.

## Not documented / not verified

- Whether any datapack on this server adds `farmersdelight:stove_burn` to a
  damage type tag was not checked; the statement above is about the jar only.
- The Alex's Delight and Dungeons Delight add-ons add their own foods and (in
  Dungeons Delight's case) their own effects that reference FD's. Only the three
  Comfort call sites named above were read; neither add-on's food table is
  covered here.
- Nutrition/saturation values are the item's registered defaults. Nothing was
  checked for a server-side datapack or CraftTweaker script overriding them
  (FD ships a CraftTweaker integration package, unused unless scripts exist).
- Whether Apotheosis affixes or Iron's Spells effects alter healing or hunger in
  a way that changes how Nourishment or Comfort behave in practice was not
  tested in-game; the code-level statement — no attribute modifiers, no
  cross-references — is all that is claimed.
