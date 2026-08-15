<!-- Generated from FarmersDelight-1.20.1-1.3.2.jar + live server config. Provenance: ../README.md -->

# Farmer's Delight — Advancements, Progression Chains and Gates

Everything below is read out of `FarmersDelight-1.20.1-1.3.2.jar` — its `data/`
and `assets/` trees for the data-driven content, the decompiled classes for
behaviour — and cross-checked against `/config/farmersdelight-common.toml` on the
live server. Where the mod registers something but never describes it, this doc
says so rather than guessing.

Tick figures are converted to seconds throughout.

## Advancement files vs. player-visible advancements

`data/farmersdelight/advancements/` holds **218 JSON files**, but
`assets/farmersdelight/lang/en_us.json` has only **42 `advancements.*` keys**.
That is not a discrepancy — it is two different things living in one directory:

| Directory | Files | What they are |
|---|---|---|
| `advancements/main/` | **21** | The player-visible tree. Each has a `display` block with a title, description, icon and frame |
| `advancements/recipes/` | **197** | Recipe-unlock plumbing. No `display` block, so they never appear in the advancement screen and never produce a toast |

**21 visible advancements × 2 lang keys each (`.title` + `.description`) = 42.**
That is the whole of the lang file's advancement section.

How the two sets were separated — a **set-diff, not a file count**. Every lang
key was split to its stem (`advancements.farmersdelight.<stem>.title` →
`<stem>`), and that set was diffed both ways against the basenames of
`main/*.json`. **Both differences are empty**: 21 stems, 21 files, exact match.
No visible advancement is missing a translation, and no lang key describes a
file that does not exist. The 197 files in `recipes/` contribute zero lang keys
because they have nothing to translate.

## Recipe-unlock advancements

**197 files in `advancements/recipes/`.** They are the standard vanilla
recipe-book mechanism, not achievements. Nothing here is worth tabling; the
shape is identical across all of them.

- **194** are plain advancements with `parent: "minecraft:recipes/root"`, no
  `display`, `sends_telemetry_event: false`, and `rewards.recipes` naming the one
  recipe they unlock. Every one carries exactly two criteria in a single OR
  group: a `minecraft:inventory_changed` check for a relevant ingredient, and a
  `minecraft:recipe_unlocked` check for the recipe itself. Picking up the
  ingredient adds the recipe to your recipe book. That is their entire effect.
- **3** — `potato_crate.json`, `carrot_crate.json`, `beetroot_crate.json` — are
  Forge *conditional* advancement files. They wrap the same structure in an
  `advancements` array behind a `farmersdelight:vanilla_crates_enabled`
  condition, which reads `enableVanillaCropCrates` from the config. That option
  is **`true`** on this server, so all three load.

197 recipe advancements against 333 recipe files in `data/farmersdelight/recipes/`
— the shortfall is the cooking-pot and cutting-board recipes, which use custom
recipe types and do not get generated recipe-book unlocks.

## The player-visible advancement tree

One root, `farmersdelight:main/root`, and 20 descendants. Frames break down as
**16 task, 2 goal, 3 challenge**. Nothing in the tree gates anything mechanically
— no advancement is a prerequisite for any recipe or block.

### Tree

```
root
├─ craft_knife
│  ├─ get_ham
│  ├─ harvest_straw
│  │  └─ place_organic_compost
│  │     └─ get_rich_soil
│  └─ use_cutting_board
│     └─ obtain_netherite_knife
├─ get_fd_seed
│  ├─ get_mushroom_colony
│  ├─ harvest_ropelogged_tomato
│  │  └─ hit_raider_with_rotten_tomato
│  └─ plant_rice
│     └─ plant_all_crops
└─ place_campfire
   ├─ place_cooking_pot
   │  └─ eat_nourishing_food
   │     └─ place_feast
   │        └─ master_chef
   └─ use_skillet
      └─ place_skillet
```

The three branches off the root are the mod's three intended lines of play:
**tools** (`craft_knife`), **farming** (`get_fd_seed`) and **cooking**
(`place_campfire`). The longest chain is 6 deep: `root → place_campfire →
place_cooking_pot → eat_nourishing_food → place_feast → master_chef`.

### Full table

All ids are under `farmersdelight:main/`. Triggers are read out of each file's
`criteria` block, not inferred from the id. Where several criteria sit in one
`requirements` OR group, any one of them completes the advancement.

| id | Title | Description | Parent | Frame | Trigger |
|---|---|---|---|---|---|
| `root` | Farmer's Delight | A world of flavor awaits you! | — | task | `minecraft:inventory_changed` with **empty conditions** — granted on the first change to your inventory. The criterion is named `seeds` but checks nothing |
| `craft_knife` | Hunt and Gather | Craft a Knife to scavenge extra goods from plants and animals | `root` | task | `minecraft:inventory_changed` for any of the five knives (flint, iron, diamond, golden, netherite) |
| `get_ham` | Wild Butcher | Use a Knife to extract Ham from Pigs or Hoglins | `craft_knife` | task | `minecraft:inventory_changed` for `farmersdelight:ham` or `farmersdelight:smoked_ham` |
| `harvest_straw` | Grasping at Straws | Harvest grass, wheat or rice with a Knife to collect Straw | `craft_knife` | task | `minecraft:inventory_changed` for `farmersdelight:straw` |
| `place_organic_compost` | Advanced Composting | Place down some Organic Compost. It composts better with sun, water and mushrooms! | `harvest_straw` | task | `minecraft:placed_block` — `farmersdelight:organic_compost` |
| `get_rich_soil` | Plant Food | Organic Compost slowly decays into Rich Soil, an upgrade for your farms! | `place_organic_compost` | **goal** | `minecraft:inventory_changed` for `farmersdelight:rich_soil` |
| `use_cutting_board` | Watch Your Fingers | With a tool in hand, use a Cutting Board to break down an item | `craft_knife` | task | `farmersdelight:use_cutting_board` — the mod's own trigger, fired unconditionally by `CuttingBoardBlockEntity.processStoredItemUsingTool` when a cutting recipe completes. Its `TriggerInstance.test()` returns `true` with no predicate |
| `obtain_netherite_knife` | If You Can't Take the Heat... | Spend a whole Netherite Ingot to upgrade your knife! Or get out of the kitchen. | `use_cutting_board` | **challenge** | `minecraft:inventory_changed` for `farmersdelight:netherite_knife`. Rewards **200 XP** |
| `get_fd_seed` | Crops of the Wild | Four new crops may be found in the wild, across many climates... or maybe in a chest somewhere. | `root` | task | `minecraft:inventory_changed` for any of `cabbage_seeds`, `tomato_seeds`, `onion`, `rice` |
| `get_mushroom_colony` | Fungus Among Us | Shear a fully mature Mushroom Colony. To grow them like this, you'll need a very rich soil... | `get_fd_seed` | task | `minecraft:inventory_changed` for `brown_mushroom_colony` or `red_mushroom_colony` (the block items) |
| `harvest_ropelogged_tomato` | Tall-mato | Hang some rope above a tomato crop to make it grow taller | `get_fd_seed` | task | `minecraft:item_used_on_block` — using **any** item (`match_tool` with an empty predicate) on a `farmersdelight:tomatoes_on_rope` block whose `age` is `0` |
| `hit_raider_with_rotten_tomato` | Boo! Hiss! | Throw a Rotten Tomato at one of these pesky raiders! | `harvest_ropelogged_tomato` | task | `minecraft:player_hurt_entity` — damage whose direct entity is a `farmersdelight:rotten_tomato` projectile, against an entity in `#minecraft:raiders` |
| `plant_rice` | Dipping Your Roots | Plant grains of Rice in a shallow water puddle | `get_fd_seed` | task | `minecraft:placed_block` — `farmersdelight:rice` |
| `plant_all_crops` | Crop Rotation | Cultivate every food-related plant you can find, such as vegetables, fruits, fungi or roots! | `plant_rice` | **challenge** | `minecraft:placed_block` × **19**, each its own requirement group, so all 19 are needed. Rewards **100 XP**. See the list below |
| `place_campfire` | Bonfire Lit | Place down a Campfire to cook some food | `root` | task | `minecraft:placed_block` — `minecraft:campfire` or `minecraft:soul_campfire` |
| `place_cooking_pot` | Dinner's Served! | Put down a Cooking Pot and start preparing meals! | `place_campfire` | **goal** | `minecraft:placed_block` — `farmersdelight:cooking_pot` |
| `eat_nourishing_food` | Nourishing! | A balanced and diverse meal will keep you fed and healthy for a long time! | `place_cooking_pot` | task | `minecraft:effects_changed` — gaining `farmersdelight:nourishment` |
| `place_feast` | A Glorious Feast | Some meals are big enough to be placed down and shared with friends! | `eat_nourishing_food` | task | `minecraft:placed_block` for any one of the six feast blocks: `roast_chicken_block`, `stuffed_pumpkin_block`, `honey_glazed_ham_block`, `shepherds_pie_block`, `gleaming_salad_block`, `rice_roll_medley_block` |
| `master_chef` | Master Chef | Eat a course of every meal available! | `place_feast` | **challenge** | `minecraft:consume_item` × **27**, each its own requirement group, so all 27 are needed. Rewards **200 XP**. See the list below |
| `use_skillet` | Portable Cooking | Skillets let you cook on the go. Stand near heat, then hold food in your other hand! | `place_campfire` | task | `minecraft:consume_item` for `farmersdelight:skillet` — i.e. the skillet's own use action completing |
| `place_skillet` | Sizzling Hot! | Sneak to place your Skillet down as a block | `use_skillet` | task | `minecraft:placed_block` — `farmersdelight:skillet` |

**`plant_all_crops` (19 blocks, all required):** wheat, beetroots, carrots,
potatoes, `farmersdelight:cabbages`, `farmersdelight:budding_tomatoes`,
`farmersdelight:onions`, `farmersdelight:rice`, melon stem, pumpkin stem, sweet
berry bush, sugar cane, kelp, cocoa, nether wart, chorus flower, brown mushroom,
red mushroom, cave vines (glow berries). Note it wants the **budding** tomato
block, which is what planting a tomato seed produces — not the mature
`tomatoes` block.

**`master_chef` (27 meals, all required):** mixed salad, cooked rice, bone broth,
beef stew, vegetable soup, fish stew, chicken soup, fried rice, pumpkin soup,
baked cod stew, noodle soup, onion soup, bacon and eggs, ratatouille, steak and
potatoes, pasta with meatballs, pasta with mutton chop, mushroom rice, roasted
mutton chops, vegetable noodles, squid ink pasta, grilled salmon, roast chicken,
stuffed pumpkin, honey glazed ham, shepherd's pie, gleaming salad.

## Progression chains

### From nothing to a working kitchen

The mod's four stations are independent of each other — **no station is required
to craft another station**. What differs is the vanilla prerequisite each one
carries.

1. **Cutting Board** — `/##` over `/##`: 4 `#minecraft:planks`, 2 sticks.
   Wood only, so this is the first station reachable. It does nothing without a
   tool, so pair it with a knife (below).
2. **Campfire** — vanilla: 3 sticks, 3 logs, 1 coal or charcoal. Not a Farmer's
   Delight block, but it is the heat source everything else stands on, and it is
   what `place_campfire` fires on.
3. **Cooking Pot** — `bSb` / `iWi` / `iii`: 2 bricks, 1 wooden shovel, 1 item in
   `#forge:buckets/water`, **5 iron** (`#forge:ingots/iron`). Needs a furnace for
   the bricks and iron, and a full water bucket that is consumed.
   - It only cooks while **heated**: the block directly below must be in
     `#farmersdelight:heat_sources` — magma block, lava cauldron,
     `farmersdelight:stove`, plus `#farmersdelight:tray_heat_sources` (lava,
     `#minecraft:campfires`, `#minecraft:fire`). If that block has a `lit`
     property it must be lit.
   - A **hopper** (or a Create chute, listed as optional in the tag) may sit
     between pot and heat: `#farmersdelight:heat_conductors` lets the pot look
     one block further down. That is how a pot is automated.
   - 9 slots: 6 ingredients, 1 meal output, 1 container input, 1 container
     output. There are **28 cooking recipes**. Cook times:

     | Time | Count | Recipes |
     |---|---|---|
     | **5 s** (100 ticks) | 3 | Cabbage Rolls, Cooked Rice, Tomato Sauce (0.35 XP each) |
     | **10 s** (200 ticks) | 24 | 19 meals (18 at 1.0 XP, Bone Broth at 0.35), 2 drinks (Apple Cider, Hot Cocoa), 3 misc (Dog Food, Dumplings, Glow Berry Custard) |
     | **20 s** (400 ticks) | 1 | Stuffed Pumpkin, 2.0 XP — the only 400-tick recipe |
4. **Stove** — `iii` / `B B` / `BCB`: **3 iron**, 4 bricks blocks, 1 campfire.
   Cooks up to **6 items at once** using vanilla `minecraft:campfire_cooking`
   recipes, popping results out on top. Ignite it with flint and steel or a fire
   charge; it stays lit with no fuel. It also counts as a heat source for a
   Cooking Pot or Skillet placed on it, and it burns anything standing in its
   grilling area that is not sneaking or fire-immune.
5. **Skillet** — ` ##` / ` ##` / `/  `: **4 iron**, 1 brick. Two modes:
   - **Held**: stand within reach of a `#farmersdelight:heat_sources` block and
     hold a food item in your off hand. Cooking time is
     `max(60 ticks, 20% of the campfire recipe time)`, i.e. **3 seconds minimum**;
     each level of Fire Aspect on the skillet cuts that 20% by a further 5
     percentage points.
   - **Placed** (sneak-place): cooks off the block directly below it, which must
     be in `#farmersdelight:tray_heat_sources` — lava, campfire or fire only. A
     placed skillet does **not** accept a stove or magma block.
   - It is also a weapon: Iron tier, **6 attack damage** and +1 knockback.

### Farming, from first seed to self-sustaining

Farmer's Delight adds four crops. Three of them (cabbage, tomato, rice) have no
vanilla source at all, so the first unit of each has to come from the world.

1. **Find a wild crop patch.** Nine `add_features_by_filter` biome modifiers
   place them, all in the `vegetal_decoration` step. Rarity is *one attempt per
   N chunks*:

   | Patch | Rarity | Where |
   |---|---|---|
   | Wild Cabbages | 1 in **30** | `#minecraft:is_beach` |
   | Wild Beetroots | 1 in **30** | `#minecraft:is_beach` |
   | Wild Rice | 1 in **20** | `#forge:is_wet/overworld`, excluding `#forge:is_underground` |
   | Wild Tomatoes | 1 in **100** | `#forge:is_hot/overworld`, excluding `#forge:is_wet` |
   | Wild Potatoes | 1 in **100** | Overworld, temperature 0.1–0.3, excluding `#forge:is_underground` |
   | Wild Onions | 1 in **120** | Overworld, temperature 0.4–0.9, excluding Lush Caves and Mushroom Fields |
   | Wild Carrots | 1 in **120** | Overworld, temperature 0.4–0.9, excluding Lush Caves and Mushroom Fields |
   | Brown / Red Mushroom Colony | 1 in **15** each | `#forge:is_mushroom` |

   Those are **biome tags**, not biome lists — any mod on this server that tags
   its biomes `is_beach`, `is_hot/overworld` or `is_wet/overworld` gets wild crop
   patches too. Wild rice is additionally restricted by a
   `farmersdelight:biome_tag` placement modifier to `minecraft:is_overworld`.

2. **Break the patch for seeds.** **A knife is not required.** Breaking a wild
   crop with anything gives its seed directly, with a Fortune bonus of
   0–2× level:

   | Wild block | Bare-hand / any tool | With shears |
   |---|---|---|
   | Wild Cabbages | 1 Cabbage Seeds (+Fortune), plus **20%** for 1 Cabbage | the block itself, replantable |
   | Wild Tomatoes | 1 Tomato Seeds (+Fortune), plus **20%** for 1 Tomato | the block itself |
   | Wild Onions | 1 Onion (+Fortune), plus 1–3 Allium | the block itself |
   | Wild Rice | 1 Rice per half of the two-block plant | the block itself |
   | Wild Carrots | 1 Carrot (+Fortune) | the block itself |
   | Wild Potatoes | 1 Potato (+Fortune) | the block itself |
   | Wild Beetroots | 1 Beetroot Seeds (+Fortune), plus **20%** for 1 Beetroot | the block itself |
   | Sandy Shrub | **12.5%** for Beetroot Seeds (+Fortune) | the block itself |

   Using a **knife** instead routes through the Cutting Board's recipe set and
   gives a different, generally richer result — see Gates below.

3. **Two shortcuts that skip the search entirely.**
   - **Wandering Trader.** `enableWanderingTraderFDTrades = true`. All four —
     Cabbage Seeds, Tomato Seeds, Rice, Onion — are added to the generic trade
     pool at **1 emerald for 1**, 12 trades each.
   - **Chest loot.** `generateFDChestLoot = true` adds 14 loot pools. Seeds
     appear in abandoned mineshafts, shipwreck supply, simple dungeons, and five
     village house types (plains, desert, savanna, snowy, taiga).
   - `generateFDCropsOnVillageFarms = true`, so village farm plots sometimes grow
     these crops outright.

4. **Plant them.**
   - **Onion** is an `ItemNameBlockItem` — the item you eat is the item you
     plant. Standard farmland.
   - **Cabbage** and **Tomato** plant from their seed items on farmland.
   - **Rice** must go into a **full water source block** (fluid level 8) over a
     dirt-family block, with sky light 6 or better above it. It grows into Rice
     Panicles, which mature over 4 stages.

5. **Harvest without losing the crop.**
   - Cabbages at `age 7` drop 1 Cabbage plus Cabbage Seeds (binomial, +3 with
     Fortune); immature cabbages drop only seeds.
   - Onions always drop 1 Onion, plus a second Fortune-scaled roll at `age 7`.
   - Tomatoes at `age 3` drop **1–2 Tomatoes** (+1 per Fortune level), a Tomato
     Seeds only if not ropelogged, and **5%** for a Rotten Tomato.
   - Rice Panicles at `age 3` drop **1 Rice with a knife**, or 1 Rice Panicle
     without one. A Rice Panicle crafts back into 1 Rice, so the knife is a
     convenience, not a gate. `#farmersdelight:straw_harvesters` (which is just
     `#farmersdelight:tools/knives`) also adds 1 Straw off mature rice.

6. **Upgrade the soil.** This is the self-sustaining step and it needs the tool
   chain first — see Gates.
   - **Straw** → **Organic Compost** (shapeless, 1 dirt + 2 straw + 2 bone meal +
     4 tree bark, or 1 dirt + 2 rotten flesh + 2 straw + 4 bone meal).
   - Organic Compost ticks up through **8 composting stages** and then becomes
     **Rich Soil**. Per random tick the chance is
     `0.02 × (blocks in the surrounding 3×3×3 that are in #farmersdelight:compost_activators)`
     `+ 0.10 if sky light above any neighbour exceeds 12, else 0.05`
     `+ 0.10 if any neighbour is water`. Activators are brown and red mushrooms,
     podzol, mycelium, Organic Compost itself, Rich Soil, Rich Soil Farmland and
     any mushroom colony. Surrounding a pile with mushrooms and water in the open
     is the fast path.
   - **Rich Soil** rolls a bone-meal tick on the plant above (or below, for
     `#farmersdelight:planted_from_below` plants like cave vines) at
     `richSoilBoostChance = 0.2` — **20%** per random tick, the mod default.
     Blocks in `#farmersdelight:unaffected_by_rich_soil` are skipped, which
     includes grass, moss, nylium, wild crops and the mushroom colonies
     themselves.
   - Rich Soil also **converts a plain brown or red mushroom placed on it into a
     Mushroom Colony** on the next random tick. Colonies then grow one stage at a
     time — 1 in 4 per random tick, up to age 3, and **only while standing on
     Rich Soil**.
   - Harvest a colony by right-clicking with **shears** (one mushroom, age drops
     by 1) or with a **knife** (all of them at once, age resets to 0). Breaking a
     mature age-3 colony with shears gives the **colony block item** — that, and
     only that, is what `get_mushroom_colony` wants.

### Tomatoes on rope

`harvest_ropelogged_tomato` is its own short chain and needs Straw, so it sits
behind the tool line in practice even though the advancement tree hangs it off
`get_fd_seed`.

1. Knife → Straw (see Gates).
2. **Rope**: 2 straw stacked vertically → **4 Rope**.
3. Hang rope so it occupies the block **above** a tomato crop. With
   `enableTomatoVineClimbingTaggedRopes = true` (the server value) the crop
   accepts anything in `#farmersdelight:ropes`, not just this mod's rope; broken
   vines leave behind `defaultTomatoVineRope = "farmersdelight:rope"`.
4. The crop climbs, converting the rope into a Tomato Vine and then producing a
   `tomatoes_on_rope` block. Using any item on one at `age 0` fires the
   advancement.
5. **Rotten Tomato** — 5% per mature tomato harvest — is throwable, and hitting
   anything in `#minecraft:raiders` with one gives `hit_raider_with_rotten_tomato`.
   Rotten Tomatoes also craft into Tomato Seeds, same as a good one.

### The knife tiers

All five knives are `KnifeItem extends DiggerItem`, all with the same
**+0.5 attack damage** and **−2.0 attack speed** modifiers on top of their tier.
Only durability and mining tier differ.

1. **Flint Knife** — `m` over `s`: 1 flint + 1 stick. Custom `ModMaterials.FLINT`
   tier: **131 durability**, mining level 1, speed 4.0, +1.0 tier attack damage,
   enchantability 5, repaired with flint.
2. **Iron Knife** — 1 `#forge:ingots/iron` + 1 stick. `Tiers.IRON`.
3. **Golden Knife** — 1 gold ingot + 1 stick. `Tiers.GOLD` — high
   enchantability, low durability.
4. **Diamond Knife** — 1 diamond + 1 stick. `Tiers.DIAMOND`.
5. **Netherite Knife** — **smithing table only**: Netherite Upgrade Smithing
   Template + Diamond Knife + 1 netherite ingot. `Tiers.NETHERITE`, fire
   resistant. This is the `obtain_netherite_knife` challenge.

Knives are found in chests as well as crafted: Flint and Iron in village butcher
chests, Golden in ruined portals and bastion hoglin stables, Diamond in bastion
treasure, bastion hoglin stables and End city treasure.

Every knife declares the tool actions `shears_carve`, `sword_dig`,
`farmersdelight:knife_dig` and `farmersdelight:knife_harvest`, and mines
`#farmersdelight:mineable/knife` — cactus, melon, pumpkins and jack o'lanterns,
cobweb, cake and candle cakes, wool and wool carpets, the mod's pies and
cheesecake, rice bag, `#farmersdelight:straw_blocks`, and whatever sits in
`#forge:mineable/knife` (which the jar ships **empty**, as the cross-mod hook).

## Gates and prerequisites

Concrete blockers, in the order they bite.

**A knife gates the whole tool branch.** `craft_knife` is the parent of
`get_ham`, `harvest_straw` and `use_cutting_board`, and that is not decorative:

- **Straw** exists only through knife-tagged tools. All five straw loot modifiers
  require `#farmersdelight:straw_harvesters`. Rates: **100%** off mature wheat
  (`age 7`) and mature rice panicles (`age 3`), **20%** off grass and tall grass,
  **30%** off a Sandy Shrub. No straw, no Rope, no Canvas, no Organic Compost,
  and therefore no Rich Soil, no Mushroom Colonies and no tomatoes on rope.
  **Straw is the single widest chokepoint in the mod, and the first knife is the
  real unlock.** What counts as a knife is wider than the mod's own five — see
  below.
- **Ham** exists only through a knife. `scavenging_ham_from_pig` requires the
  killer's **mainhand** to be in `#farmersdelight:tools/knives`; **50% + 10% per
  Looting level** on a pig, **guaranteed** on a hoglin. If the animal is on fire
  when it dies you get Smoked Ham instead, at the same rates. Ham is a hard
  requirement for Honey Glazed Ham, which is one of the 27 `master_chef` meals.
- **The same knife-in-mainhand condition** also adds feather from chickens,
  string from spiders and cave spiders, leather from cows/mooshrooms/horses/
  donkeys/mules/llamas, rabbit hide from rabbits and a shulker shell from
  shulkers — all guaranteed, all mainhand-knife-gated.
- **Pumpkins** break into **4 Pumpkin Slices** instead of a pumpkin when cut with
  a knife without Silk Touch.
- **Cake, Apple Pie, Chocolate Pie, Pumpkin Pie and Sweet Berry Cheesecake** only
  yield slices to a knife.

### What counts as a knife

Straw harvesting and Cutting Board recipes read like two different tool
requirements. **On this server they resolve to the same set of items, reached by
two routes** — and that set is wider than the five knives Farmer's Delight ships.

- `#farmersdelight:straw_harvesters` is a **pure alias**. Its only member is
  `#farmersdelight:tools/knives`; it has no entries of its own. Anything in the
  knives tag harvests Straw transitively.
- `#farmersdelight:tools/knives` is what the straw and scavenging loot modifiers
  and the rice-panicle loot table check directly. The Farmer's Delight jar
  populates it with its five knives.
- **Cutting Board recipes** take `matchesTool(KnifeItem.KNIFE_DIG, forge:tools/knives)`
  — either the **`knife_dig` tool action** or the **`#forge:tools/knives`** tag.
  Farmer's Delight fills `#forge:tools/knives` with the same five knives and
  `KnifeItem` declares `knife_dig`, so for FD's own knives the two routes
  coincide.
- **Dungeons Delight widens both.** It ships its own
  `data/farmersdelight/tags/items/tools/knives.json` holding
  `["#dungeonsdelight:cleavers", "dungeonsdelight:stained_knife"]`, and it
  carries **no `"replace": true`**, so it merges additively instead of
  overriding. `#dungeonsdelight:cleavers` resolves to the flint, iron, golden,
  diamond, netherite and stained cleavers. All seven items join
  `#farmersdelight:tools/knives`, and through the alias they harvest Straw,
  extract Ham, and satisfy every other knife-tagged loot modifier exactly as an
  FD knife does.

So the Straw gate on this server is **"an FD knife *or* a Dungeons Delight
cleaver / stained knife"** — twelve items, not five. Cutting-board cutting and
straw harvesting do **not** have different tool requirements here.

Alex's Delight ships no knife tag. For the authoritative sweep of every installed
jar for `data/farmersdelight/` content — including any other mod that merges into
this tag — see [addons.md](addons.md).

**A Cutting Board needs a tool, and which tool decides the output.** The board
holds one item; you then use it with a tool in your main hand. Recipes specify
their tool as either a tag or a tool action — knives for most food, but also
`axe_strip` for logs (which is how you get **Tree Bark**, one of the two Organic
Compost routes), plus shovels and pickaxes for the salvaging recipes.
`cuttingBoardFortuneBonus = 0.1` on this server, so each Fortune level on the
tool adds **10 percentage points** to the odds of the chance-gated results.
`enableCuttingBoardDispenserBehavior = true` means a dispenser aimed at a board
will operate it with a stored tool — the automation path.

**Cutting wild crops is the better route, once you have a knife.** Breaking a
wild crop gives you the seed; cutting it on a board gives seed *and* dye:

| Cut on a board | Yields |
|---|---|
| Wild Onions | 1 Onion, 2 Magenta Dye, 10% Lime Dye |
| Wild Cabbages | 1 Cabbage Seeds, 50% for 2 Yellow Dye |
| Wild Tomatoes | 1 Tomato Seeds, 20% Tomato, 10% Green Dye |
| Wild Rice | 1 Rice, 50% Straw |
| Wild Carrots | 1 Carrot, 50% for 2 Light Gray Dye |
| Wild Potatoes | 1 Potato, 50% for 2 Purple Dye |
| Wild Beetroots | 1 Beetroot Seeds, 1 Red Dye |

**Rich Soil gates Mushroom Colonies.** `#farmersdelight:mushroom_colony_growable_on`
contains exactly one block: `farmersdelight:rich_soil`. A colony placed on
anything else will survive but never advance past the age it was placed at, so
`get_mushroom_colony` cannot be completed without the full
straw → compost → rich soil chain, unless you find a naturally generated colony
in a Mushroom Fields biome and shear it at age 3.

**Rice gates itself on water.** `RiceBlock.canSurvive` requires the fluid at its
own position to be water at **level 8** — a full source block, not flowing water
and not a waterlogged edge. Growth additionally needs sky light **≥ 6** on the
block above.

**Feasts gate on a bowl and on cooked vanilla food.** All six feast blocks are
9-slot shapeless recipes that consume a **`minecraft:bowl`** in the centre, and
five of the six require already-cooked vanilla items (cooked chicken and baked
potato for Roast Chicken; cooked mutton and baked potato for Shepherd's Pie;
honey bottle and Smoked Ham for Honey Glazed Ham; golden carrot and honey bottle
for Gleaming Salad). Stuffed Pumpkin is the exception: it is a **Cooking Pot**
recipe that uses a whole `minecraft:pumpkin` as its container, takes **20
seconds**, and awards 2.0 XP.

**`master_chef` is gated on the Nether and a squid.** Of the 27 meals, Bone Broth
needs `#forge:bones` plus glow berries / mushrooms / hanging roots / glow lichen,
Squid Ink Pasta needs an ink sac, Grilled Salmon and Baked Cod Stew need fishing,
and Honey Glazed Ham needs Smoked Ham (knife + burning pig or hoglin). None of
the 27 requires Nether travel directly, but `plant_all_crops` does — **nether
wart** forces a Nether trip and **chorus flower** forces the End.

**Nothing gates on a structure exclusively.** Every chest-loot item — knives,
cooking pot, skillet, seeds, rope — is also craftable or obtainable from wild
generation. `generateVillageCompostHeaps = true` puts Organic Compost piles in
villages, which is the one way to reach Rich Soil without a knife.

**Nourishment is not a food buff in the usual sense.** `NourishmentEffect`
zeroes your **exhaustion** every tick (unless natural regeneration is actively
healing you off saturation), so hunger stops draining for the duration. A mixin
also lets you eat while already full whenever you have it. It comes in four
durations, applied at 100% chance by the food's `FoodProperties`:

| Constant | Ticks | Seconds |
|---|---|---|
| `BRIEF_DURATION` | 600 | **30 s** |
| `SHORT_DURATION` | 1200 | **1 min** |
| `MEDIUM_DURATION` | 3600 | **3 min** |
| `LONG_DURATION` | 6000 | **5 min** |

Twenty-six Farmer's Delight foods in `FoodValues` grant it. With
`enableVanillaSoupExtraEffects = true` on this server, three vanilla items are
patched to grant it as well — **Mushroom Stew** and **Beetroot Soup** at 3
minutes, **Rabbit Stew** at 5 — which means `eat_nourishing_food` is reachable
from a vanilla soup, before any Farmer's Delight station exists.

## What this mod expects you to already have

Vanilla prerequisites, step by step. Nothing here is supplied by Farmer's Delight
itself.

| Step | Vanilla prerequisite |
|---|---|
| Cutting Board | Planks and sticks. Wood only |
| Flint Knife | 1 flint (gravel) + 1 stick. Reachable in the first few minutes |
| Straw | A knife, plus grass, mature wheat or mature rice to cut |
| Rope, Canvas, Safety Net | Straw only, no vanilla input |
| Organic Compost | **Bone meal** ×2–4 (skeletons or a vanilla composter), plus either 2 rotten flesh or 4 Tree Bark (an axe and logs, via the Cutting Board) |
| Campfire | 3 sticks, 3 logs, 1 coal or charcoal |
| Cooking Pot | A **furnace** for bricks, **5 iron ingots**, a **wooden shovel**, and a **filled water bucket** (itself 3 iron) — so roughly 8 iron and a smelting setup |
| Stove | **3 iron ingots**, 4 **bricks blocks** (16 bricks → 4 blocks), 1 campfire, plus **flint and steel or a fire charge** to light it |
| Skillet | **4 iron ingots** + 1 brick, and a heat source to stand near |
| Iron Knife | 1 iron ingot |
| Golden Knife | 1 gold ingot |
| Diamond Knife | 1 diamond |
| Netherite Knife | Nether travel, ancient debris, a **netherite ingot**, a **Netherite Upgrade Smithing Template** (bastion remnant), and a **smithing table** |
| Meals generally | A **bowl** or **glass bottle** or **bucket** — the Cooking Pot's container slot only accepts `#farmersdelight:serving_containers`, which is exactly those three |
| Feasts | A bowl, plus a furnace or smoker for the cooked vanilla components; Honey Glazed Ham additionally needs a **honey bottle** (bees) |
| `plant_all_crops` | The **Nether** (nether wart), the **End** (chorus flower), a **lush cave** or a trader (glow berries), cocoa beans (jungle), and kelp |
| Rice | A shallow water source and sky access |
| Rich Soil | Nothing beyond Organic Compost — but the compost decays faster with **sky light above 12**, **water adjacent**, and **mushrooms** in the surrounding 3×3×3 |

### Ingredient tags other mods can fill

Cooking Pot recipes key off Forge tags rather than concrete items in most slots,
so ingredient availability on this server is wider than the vanilla + Farmer's
Delight item list implies. The tags in use include `#forge:crops/carrot`,
`#forge:crops/potato`, `#forge:crops/beetroot`, `#forge:crops/onion`,
`#forge:crops/tomato`, `#forge:crops/rice`, `#forge:crops/wheat`,
`#forge:vegetables`, `#forge:salad_ingredients`, `#forge:berries`,
`#forge:mushrooms`, `#forge:bones`, `#forge:eggs`, `#forge:milk`, `#forge:dough`,
`#forge:pasta`, `#forge:grain`, `#forge:raw_meat` and the per-species
raw/cooked meat tags. Any mod on this server that tags its own produce into these
can substitute into the recipe. Which mods actually do so is covered by the
jar-wide sweep in [addons.md](addons.md); only the Dungeons Delight knife tag
above was verified here.

Villager trades add another route: `enableFarmerFDTrades = true`, so Novice
Farmers buy **26 Onion** or **26 Tomato** for 1 emerald and Apprentice Farmers
buy **16 Cabbage** or **20 Rice**, 16 trades each. These are sinks, not sources —
the only trade *source* is the Wandering Trader's four seed listings.

## Not documented

- The exact biome list each `#forge:is_hot/overworld`, `#forge:is_wet/overworld`
  and `#forge:is_beach` tag resolves to on this server. That depends on every
  worldgen mod in the pack and was not enumerated.
- Alex's Delight and Dungeons Delight content. Both ship Farmer's Delight cutting
  and cooking recipes (11 and 21 files respectively) and so extend these chains,
  but neither was read for this doc — see [addons.md](addons.md).

Whether any mod beyond Dungeons Delight merges into `#farmersdelight:tools/knives`
or `#forge:tools/knives` is settled by the jar-wide `data/farmersdelight/` sweep
in [addons.md](addons.md), not left open here.
