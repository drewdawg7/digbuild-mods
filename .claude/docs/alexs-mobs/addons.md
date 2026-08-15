<!-- Generated from alexsdelight-1.5.jar + ramcompat-1.20.1-0.1.4.jar + alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Add-ons & Dependencies

Two Alex's Mobs add-ons are installed on this server: **Alex's Delight** (Farmer's
Delight cooking) and **RAM-Compat** (Relics curios). Neither adds a mob. Both
reach into parent-mod content — Alex's Delight silently rewrites two Alex's Mobs
loot tables and one Alex's Mobs recipe, and RAM-Compat mixins three Alex's Mobs
entity classes. A further ten mods on the server interact with Alex's Mobs
without being add-ons; they are catalogued further down, along with the
candidates that were checked and ruled out.

One Alex's Delight recipe is broken on this server and fails to load. See
[Known defect: Barbecue on a Stick](#known-defect-barbecue-on-a-stick).

## Alex's Delight (`alexsdelight` 1.5)

By **NCP Bails** (the CurseForge project owner displays as *Baisylia*; the 1.5
file uploader as *NCP_Bails* — same person). License **All Rights Reserved**.
Built 2024-01-13, 54.1 KB, 100 files. Description from `mods.toml`: *"Adds
compatibility between Alex's Mobs and Farmer's Delight"*.

- CurseForge: <https://www.curseforge.com/minecraft/mc-mods/alexs-delight>
- 1.5 file: <https://www.curseforge.com/minecraft/mc-mods/alexs-delight/files/5028450>
- Not published on Modrinth (checked against the Modrinth search API).

1.5 is the terminal 1.20.1 build — the project has since moved to 1.21.1/NeoForge.

Turns Alex's Mobs animal drops into Farmer's Delight cooking-chain ingredients:
5 cutting-board cuts, 4 cooking-pot meals, 24 furnace/smoker/campfire recipes and
5 shapeless crafts (a sixth is broken). Adds 23 food items, no blocks and no
entities.

### Declared dependencies vs. what this server runs

| Declared | Range | Server has | In range |
|---|---|---|---|
| `forge` | `[47,)` | 47.4.10 | yes |
| `minecraft` | `[1.20.1]` | 1.20.1 | yes |

**It declares neither `alexsmobs` nor `farmersdelight`**, but hard-references both
at class-init: `AlexsDelight.addCreative()` reads
`vectorwing.farmersdelight.common.registry.ModCreativeTabs.TAB_FARMERS_DELIGHT`
and four of its food definitions call `ModEffects.NOURISHMENT`. The CurseForge
relations page lists Alex's Mobs, Farmer's Delight **and** Citadel as required
dependencies, so the omission is a packaging oversight, not a design choice —
Forge's dependency checker will not catch a missing Farmer's Delight. All three
are present here (`alexsmobs` 1.22.9, `FarmersDelight` 1.3.2, `citadel` 2.6.3),
so the gap is latent, not active.

### Items

All 23 register into the Farmer's Delight creative tab, not a tab of their own.
Nutrition and saturation modifier are read out of `ModFoods`; saturation restored
is `nutrition × modifier × 2`.

| Item | ID | Nutrition | Sat. mod | Notes |
|---|---|---|---|---|
| Raw Bison | `raw_bison` | 4 | 0.5 | meat |
| Cooked Bison | `cooked_bison` | 10 | 1.0 | meat |
| Raw Bunfungus | `raw_bunfungus` | 4 | 0.4 | meat |
| Cooked Bunfungus | `cooked_bunfungus` | 7 | 0.7 | meat |
| Cooked Centipede Leg | `cooked_centipede_leg` | 6 | 0.7 | meat |
| Kangaroo Shank | `kangaroo_shank` | 2 | 0.2 | meat, fast to eat |
| Cooked Kangaroo Shank | `cooked_kangaroo_shank` | 4 | 0.4 | meat, fast to eat |
| Loose Moose Rib | `loose_moose_rib` | 2 | 0.2 | meat, fast to eat |
| Cooked Loose Moose Rib | `cooked_loose_moose_rib` | 4 | 0.4 | meat, fast to eat |
| Bison Mince | `bison_mince` | 2 | 0.2 | meat, fast to eat |
| Bison Patty | `bison_patty` | 5 | 0.7 | meat, fast to eat |
| Raw Bunfungus Drumstick | `raw_bunfungus_drumstick` | 2 | 0.2 | meat, fast to eat |
| Cooked Bunfungus Drumstick | `cooked_bunfungus_drumstick` | 3 | 0.4 | meat, fast to eat |
| Raw Catfish Slice | `raw_catfish_slice` | 1 | 0.2 | meat, fast to eat |
| Cooked Catfish Slice | `cooked_catfish_slice` | 3 | 0.3 | meat, fast to eat |
| Gongylidia Bruschetta | `gongylidia_bruschetta` | 10 | 1.0 | |
| Maggot Salad | `maggot_salad` | 6 | 0.6 | bowl, stacks to 16; Nausea 60 s, always |
| Kangaroo Stew | `kangaroo_stew` | 10 | 0.8 | bowl, stacks to 16; Nourishment 5 min |
| Acacia Blossom Soup | `acacia_blossom_soup` | 12 | 0.8 | bowl, stacks to 16; Nourishment 5 min |
| Lobster Pasta | `lobster_pasta` | 10 | 0.8 | bowl, stacks to 16; Nourishment 5 min |
| Bison Burger | `bison_burger` | 12 | 1.1 | |
| Bunfungus Sandwich | `bunfungus_sandwich` | 10 | 1.0 | |
| Kangaroo Pasta | `kangaroo_pasta` | 10 | 0.8 | bowl, stacks to 16; Nourishment 5 min |

Nourishment is Farmer's Delight's own effect (`farmersdelight:nourishment`), not a
new one. Maggot Salad's Nausea is applied at probability 1.0 — every time.

> Third-party item lists for this mod circulate with two errors. They describe
> Maggot Salad as granting **Jump Boost**; `ModFoods.MAGGOT_SALAD` applies
> `MobEffects.CONFUSION` (Nausea) for 1200 ticks at probability 1.0. They also
> omit Bison Patty, Bison Mince and the Barbecue on a Stick recipe. The jar's
> `ModFoods`/`ModItems` and `data/alexsdelight/recipes/` are authoritative and
> are what the tables above are built from.

### Cutting board

Each takes any knife (`forge:tools/knives`) and yields 2.

| Input | Output |
|---|---|
| `alexsdelight:raw_bison` | 2 × `bison_mince` |
| `alexsdelight:raw_bunfungus` | 2 × `raw_bunfungus_drumstick` |
| `alexsmobs:kangaroo_meat` | 2 × `kangaroo_shank` |
| `alexsmobs:moose_ribs` | 2 × `loose_moose_rib` |
| `alexsmobs:raw_catfish` | 2 × `raw_catfish_slice` |

### Cooking pot

All four cook in 200 ticks (10 seconds) for 0.35 experience and serve in a bowl.

| Meal | Ingredients |
|---|---|
| Acacia Blossom Soup | Onion + Raw Pasta + `alexsmobs:acacia_blossom` |
| Kangaroo Pasta | cooked kangaroo (tag) + Raw Pasta + Tomato Sauce |
| Kangaroo Stew | cooked kangaroo (tag) + Carrot + Beetroot |
| Lobster Pasta | `alexsmobs:lobster_tail` + Raw Pasta + Tomato Sauce |

### Furnace, smoker and campfire

Eight ingredients each get all three recipe types (smelting, smoking,
campfire_cooking) — 24 recipes, all at 200 ticks and 1.0 experience. Because
every variant carries the same `cookingtime`, the smoker gets none of its usual
speed advantage over the furnace for these items.

`raw_bison` → `cooked_bison`; `bison_mince` → `bison_patty`; `raw_bunfungus` →
`cooked_bunfungus`; `raw_bunfungus_drumstick` → `cooked_bunfungus_drumstick`;
`raw_catfish_slice` → `cooked_catfish_slice`; `alexsmobs:centipede_leg` →
`cooked_centipede_leg`; `kangaroo_shank` → `cooked_kangaroo_shank`;
`loose_moose_rib` → `cooked_loose_moose_rib`.

### Crafting table

| Result | Ingredients (shapeless) |
|---|---|
| 2 × Gongylidia Bruschetta | salad ingredient + tomato + `alexsmobs:gongylidia` + bread + `alexsmobs:fish_oil` |
| 1 × Bison Burger | salad ingredient + tomato + Bison Patty + Beetroot + bread |
| 1 × Bunfungus Sandwich | cooked bunfungus (tag) + 2 × Red Mushroom Colony + bread |
| 1 × Maggot Salad | `alexsmobs:maggot` + Cabbage + Tomato + Onion + Beetroot + Bowl |
| 1 × Maggot Salad (alt) | `alexsmobs:maggot` + Farmer's Delight Mixed Salad |
| 2 × Barbecue on a Stick | **broken — see below** |

### Item tags it defines

- `alexsdelight:cooked_kangaroo` — `alexsdelight:cooked_kangaroo_shank`,
  `alexsmobs:cooked_kangaroo_meat`
- `alexsdelight:cooked_bunfungus` — `alexsdelight:cooked_bunfungus_drumstick`,
  `alexsdelight:cooked_bunfungus`

### Data it overrides

This is the part that matters for debugging, because it silently changes
Alex's Mobs behaviour. Three files in the `alexsmobs` namespace, all winning
over the parent jar by load order.

**`data/alexsmobs/loot_tables/entities/bison.json`** — Alex's Mobs' own table
drops **6–8 `minecraft:beef`** plus 0–2 Bison Fur, and both pools carry a
`furnace_smelt` function so a Bison killed while on fire drops cooked meat. The
override replaces beef with **2–5 `alexsdelight:raw_bison`** and **removes the
`furnace_smelt` function from both pools**. Two consequences: Bison no longer
drop vanilla beef at all, and burning a Bison to death no longer auto-cooks the
drop. Looting is unchanged (0–2 extra meat, 0–1 extra fur).

**`data/alexsmobs/loot_tables/entities/bunfungus.json`** — Alex's Mobs' own table
drops only 0–2 Red Mushroom with no looting bonus. The override adds a second
pool of 0–2 `alexsdelight:raw_bunfungus` and adds a 0–2 looting bonus to the
mushroom pool. (The pools are named `bison_meat` and `bison` in the JSON — a
copy-paste artefact in the addon, harmless.)

**`data/alexsmobs/recipes/kangaroo_burger.json`** — Alex's Mobs' own recipe is
**shaped**: bread / cooked kangaroo meat / bread. The override replaces it with a
**shapeless five-ingredient** recipe: bread + 2 × cooked kangaroo (tag) + a salad
ingredient + a carrot. The Kangaroo Burger is strictly more expensive on this
server than the Alex's Mobs wiki describes.

### Known defect: Barbecue on a Stick

`data/alexsdelight/recipes/barbecue_on_a_stick.json` lists an ingredient
`amfd:singular_cooked_moose_rib`. There is no `amfd` namespace — the mod id is
`alexsdelight` — so the item does not resolve and Forge discards the recipe at
load. Confirmed on the live server:

```
[main/ERROR] [net.minecraft.world.item.crafting.RecipeManager/]: Parsing error loading
recipe alexsdelight:barbecue_on_a_stick: com.google.gson.JsonSyntaxException:
Unknown item 'amfd:singular_cooked_moose_rib'
```

The recipe would have produced 2 × `farmersdelight:barbecue_stick` from Tomato +
Onion + Cooked Loose Moose Rib + Cooked Chicken + 2 × Stick. It cannot be crafted
here. Nothing else in the pack references `amfd`; the error is cosmetic beyond
that one lost recipe. Fixable with a one-line datapack override that corrects the
namespace to `alexsdelight`.

## RAM-Compat (`ramcompat` 1.20.1-0.1.4)

By **SSKirillSS** (the Relics author). License **All Rights Reserved**. Built
2024-08-01. 36 files. Display name on the project pages is *"Relics: Alex's Mobs
Compat"*; `mods.toml` gives the shorter *"RAM-Compat"* and the description
*"Compat addon between Relics and Alex's mobs"*.

- CurseForge: <https://www.curseforge.com/minecraft/mc-mods/ram-compat>
- Modrinth: <https://modrinth.com/mod/ram-compat>
- Source (public): <https://github.com/SSKirillSS/ram-compat> (branch `1.20.1`)
- Issue tracker: the Discord invite in `mods.toml`

Adds three Relics-style levelling curios whose abilities fire **Alex's Mobs
projectile entities** — Ice Shard, Fart and Tendon Segment — rather than
inventing new ones. No mobs, no blocks, no recipes.

### Declared dependencies vs. what this server runs

| Declared | Range | Server has | In range |
|---|---|---|---|
| `minecraft` | `[1.20.1,1.21)` | 1.20.1 | yes |
| `forge` | `[47,)` | 47.4.10 | yes |
| `curios` | `[5.2.0+1.20.1,)` | 5.14.1+1.20.1 | yes |
| `octolib` | `[0.1,)` | 0.5.0.1+1.20.1 | yes |
| `relics` | `[0.6.5,)` | 0.8.0.13 | yes |

**It does not declare `alexsmobs`**, despite compiling against
`com.github.alexthe666.alexsmobs.entity.*` and mixin-targeting three of its
classes with `"required": true`. Without Alex's Mobs the mixin config would fail
the game at load rather than degrade. Alex's Mobs 1.22.9 is present, so this is
latent.

The jar targets Relics 0.6.5+ and predates Relics 0.8.x. The range is open-ended
so the loader accepts it, and the live log shows the mod loading and all four
mixins applying with no errors, but the pairing is untested by the author against
0.8.0.13.

### What a Relics relic is

Context for the three tables below, since none of it originates in this add-on.
Relics (SSKirillSS, requires Curios API and OctoLib) adds artifacts worn in
**Curios accessory slots** rather than armour slots. Relics are found in chest
loot, injected only into the loot tables matching each relic's themed collection,
so where you search determines what you find. Each relic **rolls its stats
randomly between a minimum and a maximum** at generation and shows a quality
rating for how close that roll landed to the maximum — which is why every stat
below is a range, not a number. A relic earns its own experience from one
specific action named in its tooltip (a hit landed, a second of an aura running,
a cast), and each relic level grants a point spendable on upgrading an individual
ability's stats. Some abilities stay locked until a required relic level. There
is no research or crafting step — experience plus upgrade points is the whole
progression.

### Curios slots

| Item | Slot |
|---|---|
| `ramcompat:tendon_lump` | `charm` |
| `ramcompat:stink_gland` | `charm` |
| `ramcompat:frost_robe` | `back` |

### Tendon Lump

Curio, charm slot. Ability `tendon`, toggleable, max level 10.

Every *cooldown* seconds while toggled on, picks a random living, attackable,
line-of-sight, non-allied target within *distance* blocks and spawns an
Alex's Mobs `tendon_segment` from the wearer to it. The segment bounces between
nearby targets exactly as the Tendon Whip's does — the item reuses
`TendonWhipUtil.setLastTendon`, so a Tendon Whip in hand applies its own attack
modifiers on top.

| Stat | Initial value (rolled) | Per-level operation |
|---|---|---|
| Target search distance | 3.0 – 5.0 blocks | `MULTIPLY_BASE` +0.25 |
| Cooldown | 15.0 – 7.5 s | `MULTIPLY_BASE` −0.075 |
| Damage | 3.0 – 5.0 points | `MULTIPLY_BASE` +0.075 |

Experience: +1 per target the segment hits (`getTargetsHit() + 1`).
Loot collection: `ANTHROPOGENIC`.

Damage is injected via a mixin on `EntityTendonSegment.getBaseDamage()` reading a
`relics_damage` float off the segment's persistent NBT, so a relic-fired tendon
does the relic's damage rather than the whip's.

### Frost Robe

Curio, back slot. Three abilities.

**Warming Up** — passive, max level 0 (never upgrades). Sets the wearer's freeze
ticks to 0 every tick, forces `canFreeze()` to return false via a
`LivingEntity` mixin, and enables walking on powder snow.

**Frost Spikes** (`icicle`) — active, instantaneous cast, max level 10. Scatters
Alex's Mobs `ice_shard` projectiles around the wearer. The first icicle always
spawns; each subsequent one rolls against *chance*.

| Stat | Initial value (rolled) | Per-level operation |
|---|---|---|
| Chance of icicle spawn | 0.40 – 0.75 (40 – 75 %) | `MULTIPLY_BASE` −0.035 † |
| Max amount | 3 – 7 icicles | `MULTIPLY_BASE` +0.5 |
| Cooldown | 7.5 – 5.0 s | `MULTIPLY_BASE` −0.05 |

† The modifier on *chance* is negative, so upgrading Frost Spikes lowers the
per-icicle spawn chance while raising the maximum count. Every other stat in this
mod signs its modifier in the player's favour. This is what the code does; it
reads as an author sign error and is not called out in any published changelog.

**Frost Shield** (`freeze`) — passive, unlocks at relic level 5, max level 10. On
taking damage, rolls *chance*; on success adds *duration* seconds of freeze ticks
to the attacker and triggers Frost Spikes.

| Stat | Initial value (rolled) | Per-level operation |
|---|---|---|
| Trigger chance | 0.05 – 0.15 (5 – 15 % per hit) | `MULTIPLY_BASE` +0.1 |
| Frostbite duration | 0.75 – 1.0 s per hit | `MULTIPLY_BASE` +0.075 |

Experience: +1 per Frost Spikes activation, +1 per icicle that hits.
Loot collection: `COLD`.

A mixin on `EntityIceShard.onEntityHit` cancels the hit when the target is allied
to the shooter, so relic icicles do not friendly-fire.

### Stink Gland

Curio, charm slot. Two abilities.

**Biological Protection** (`defense`) — passive, max level 10. When the wearer
drops to **20 % health or below**, arms for *duration* seconds. While active it
clears the aggro of every mob within *radius* blocks that was targeting the
wearer, applies Nausea (100 ticks / 5 s, refreshed) to non-allied mobs in radius,
and re-targets every mob within 16 blocks of each affected mob onto that mob —
turning the crowd on itself. Plays the Alex's Mobs skunk-spray sound every 3
ticks and emits Alex's Mobs `smelly` particles. When the duration ends the
cooldown starts.

| Stat | Initial value (rolled) | Per-level operation |
|---|---|---|
| Duration | 2.0 – 5.0 s | `MULTIPLY_BASE` +0.1 |
| Radius | 1.5 – 3.0 blocks | `MULTIPLY_BASE` +0.1 |
| Cooldown | 20.0 – 15.0 s | `MULTIPLY_BASE` −0.05 |

**Foul Dash** (`dash`) — active, instantaneous cast, max level 10. Launches the
wearer along the look vector at *power*, starts a trident-style auto-spin attack
for `ceil(power × 5)` ticks, zeroes fall distance, and fires five Alex's Mobs
`fart` projectiles backwards.

| Stat | Initial value (rolled) | Per-level operation |
|---|---|---|
| Dash power | 0.75 – 1.75 | `MULTIPLY_BASE` +0.075 |
| Cooldown | 10.0 – 7.0 s | `MULTIPLY_BASE` −0.075 |

Experience: +1 per second Biological Protection is active, +1 per Foul Dash, +1
per fart projectile hit.
Loot collection: `JUNGLE`.

A mixin on `EntityFart.onEntityHit` cancels the hit on allied targets.

### How the relics are obtained

**No Alex's Mobs mob drops any of them.** The theming is Alex's Mobs-flavoured —
each relic borrows a projectile entity from elsewhere in the mod, verified
against the Alex's Mobs source: `ice_shard` is otherwise fired only by the
**Froststalker** (`EntityFroststalker`), `fart` only by the **Stink Ray** item
(`ItemStinkRay`), and `tendon_segment` only by the **Tendon Whip**
(`ItemTendonWhip` / `TendonWhipUtil`). But the drop source for the relics
themselves is vanilla chests. Nothing in the RAM-Compat jar adds a loot table, a
drop event, a recipe or a structure.

Each relic is declared with `LootData.builder().entry(LootCollections.…)`, which
is **Relics' chest-loot injection**: a collection is a set of regexes over chest
loot-table ids, and Relics rolls the relic into every matching table. Reading
`LootCollections` out of `relics-1.20.1-0.8.0.1.jar` (the build bundled in
RAM-Compat's own `libs/`, so the one it was written against):

| Relic | Collection | Matching chests |
|---|---|---|
| Tendon Lump | `ANTHROPOGENIC` | `chests/*` matching `mineshaft`, `city` or `stronghold` — mineshaft, ancient city, stronghold |
| Frost Robe | `COLD` | `chests/*` matching `fros[t/z]`, `taiga`, `cold`, `winter`, `snow`, `ice`, `glac`, plus `minecraft:chests/igloo_chest` and `minecraft:chests/village/village_fletcher` |
| Stink Gland | `JUNGLE` | `chests/*` matching `jungle` or `temple` — jungle temple, and by regex anything else with `temple` in its id |

`LootCollections` holds a single float constant `0.025`, referenced once per
entry (18 times), which indicates a uniform **2.5 % injection chance per matching
chest**. That reading is from the constant's usage pattern, not from any
published figure — treat it as strongly indicated rather than documented.

### Levelling

All three call `new LevelingData(100, 10, 200)`. The three constructor arguments
are not named in the decompiled addon, and `LevelingData` itself was not
decompiled, so **the exact XP curve is not documented here** — plausible readings
(base XP per level, max level, step or cap) were not verified and are deliberately
not published. What is verifiable from this jar: each ability caps at level 10,
Warming Up caps at 0 and is therefore permanently on and non-upgradeable, and
Frost Shield requires relic level 5 to unlock.

### Mixins

`ramcompat.mixins.json`, `"required": true`, compatibility level JAVA_8.

| Mixin | Target | Effect |
|---|---|---|
| `EntityFartMixin` | `alexsmobs:EntityFart.onEntityHit` | Cancel on allies; award Stink Gland XP |
| `EntityIceShardMixin` | `alexsmobs:EntityIceShard.onEntityHit` | Cancel on allies |
| `EntityTendonSegmentMixin` | `alexsmobs:EntityTendonSegment.getBaseDamage` | Return `relics_damage` NBT when present |
| `LivingEntityMixin` | `net.minecraft.world.entity.LivingEntity.canFreeze` | Return false while Frost Robe's Warming Up is active |

### Data it overrides

None. RAM-Compat ships no file in the `alexsmobs` namespace and no file in the
`relics` namespace beyond textures. Its only data files add its own three items
to the Curios `charm` and `back` slot tags, both with `"replace": false`.

### Live config note

`/config/relics.yaml` on this server is the stock four-line stub with
`enabledExtendedConfigs: false`, and there is no `/config/relics/` directory.
Relics' extended configuration — the layer that could retune relic stats, ability
values or loot placement — has never been generated, so **every value in the
tables above is the shipped code default**. RAM-Compat contributes no config file
of its own.

## Other mods on this server that interact with Alex's Mobs

Beyond the two add-ons above, ten of the other 145 jars touch Alex's Mobs. The
list was built by scanning every jar pulled from the live `/mods` — including
nested jar-in-jar — for the byte strings `alexsmobs` and `alexthe666`, then
reading each hit. Exactly nine jars other than the add-ons contain either string;
nothing else on the server does.

### Dependencies and Alex's Mobs' own compat code

**`citadel` 2.6.3** — hard required dependency, `versionRange="[2.6.0,)"`,
`ordering="AFTER"`. Alexthe668's shared library: animation system, entity
property tracking, datapack helpers. Alex's Mobs' data tree references
`citadel:` nine times. **Shared with Alex's Caves and Ice and Fire**, both also
on this server, so its version has to satisfy all three.

**`jei` 15.20.0.112** — the *only* `compat/` package in the Alex's Mobs source is
`compat/jei/`, holding `AlexMobsJEIPlugin`, `CapsidRecipeCategory` and
`CapsidDrawable`. It registers a **Capsid** recipe category backed by the
`alexsmobs:capsid` recipe type, feeds it
`getCapsidRecipeManager().getCapsidRecipes()`, and sets the Capsid block as the
category catalyst. Class-loaded only under `@JeiPlugin`, so Capsid recipes are
browsable here because JEI is installed. Alex's Mobs has no other compat package
and contains **zero** `ModList.get().isLoaded(...)` calls anywhere.

### Spawn-biome integration

**`terralith` 2.5.4** — `config/DefaultBiomes.java` names Terralith biomes by
registry ID **371 times** across roughly 50 mob entries (crow 31, sunbird 25,
all-forest 23, raccoon 19, hummingbird 18, bald eagle 15, cave centipede /
murmur / cockroach 12 each). Confirmed live: `/config/alexsmobs/*_spawns.json` on
this server carries entries such as `terralith:forested_highlands` and
`terralith:shield`. This is an active spawn interaction, not a stub — a large
fraction of Alex's Mobs spawning on this server happens in Terralith biomes.

**`alexscaves` 2.0.2** — Alex's Mobs spawns the **cachalot whale** and the
**comb jelly** in `alexscaves:abyssal_chasm` (`DefaultBiomes.java`; verified in
the live `cachalot_whale_spawns.json` and `comb_jelly_spawns.json`). This is the
only genuine Alex's Caves ↔ Alex's Mobs link.

> A decompiled Alex's Caves class, `AbyssalAltarBlockEntity`, contains the
> literal translation key `block.alexsmobs.capsid` in `getDisplayName`. That is a
> copy-paste leftover from Alex's Mobs' own Capsid block entity — same author —
> and it resolves against the Alex's Mobs lang file at runtime. It is not an
> integration.

### Integrations shipped by the other mod

**`supplementaries` 3.1.43** — the most extensive of these, all data-driven from
inside the Supplementaries jar:

- Cage capture: `cage_catchable.json` lists **27** Alex's Mobs entities (raccoon,
  mungus, tasmanian devil, enderiophage, platypus, crow, mimicube, roadrunner,
  rattlesnake, lobster, capuchin monkey, seagull, toucan, jerboa, potoo, flutter,
  rain frog, sugar glider, bald eagle, …). `cage_baby_catchable.json` adds
  crocodile, endergrade, gazelle, gorilla, komodo dragon, raccoon, seal, warped
  toad, bald eagle and gelada monkey as babies only.
- Jar capture: `jar_catchable.json` — enderiophage, fly, hummingbird, cockroach,
  leafcutter ant.
- `capture_blacklist.json` — centipede, bone serpent, void worm, anaconda, murmur
  cannot be captured at all.
- `tickable_when_captured.json` — mimicube. `urn_spawn.json` — fly, cockroach,
  flutter. `eats_fodder.json` — raccoon, elephant.
- Bucket-style render data: `catchable_mobs_properties/alexsmobs_{blobfish,
  stradpole,stradlepole}.json` (stradlepole forced into lava).
- Soft fluids so Alex's Mobs liquids work in jars and faucets: `fish_oil`,
  `komodo_spit`, `mimicream`, `sopa_de_macaco`, `poison`, each tagged
  `"from_mod": "alexsmobs"`.
- Six Alex's Mobs-themed banner flag textures.

**`moonlight` 2.16.34** — `soft_fluids/lava.json` registers
`alexsmobs:lava_bottle` as a valid bottle-capacity lava container. This is the
library underneath the Supplementaries fluid handling above.

**`BEB` 6.0.0** (Beautiful Enchanted Books) — ships enchanted-book models and
textures under `assets/alexsmobs/` for four Alex's Mobs enchantments:
**board_return, lavawax, serpentfriend, straddle_jump**. Cosmetic only.

**`YungsBetterJungleTemples` 2.0.5** — its `floor_2_pit` template pool contains
`betterjungletemples:mod_integration/alexsmobs_floor_2_pit_crocodiles`, gated by
`"type": "yungsapi:mod_loaded", "modid": "alexsmobs"`. Jungle temple floor-2 pits
can generate stocked with Alex's Mobs crocodiles. The NBT ships in the jar and
the gate is satisfied here.

**`betterarcheology` 1.2.1** — `SoaringWindsEnchantment.canEnchant` calls
`ModList.get().isLoaded("alexsmobs")` and additionally accepts
`ItemTarantulaHawkElytra`, so **Soaring Winds can be applied to the Tarantula
Hawk Elytra**, not just a vanilla elytra. This is the only literal
`isLoaded("alexsmobs")` check anywhere on the server.

**`alltheleaks` 1.1.1** — carries a targeted patch class annotated
`@Issue(modId="alexsmobs", issueId="#2165", versionRange="[1.22.5,)")`. On
`LevelEvent.Unload` it clears the unloaded level out of Alex's Mobs'
`ServerEvents#BEACHED_CACHALOT_WHALE_SPAWNER_MAP` and `AMWorldData#dataMap`. The
version range covers 1.22.9, so the patch is active. Memory-leak fix, no gameplay
effect.

### Checked and ruled out

Each of these was checked by full-jar entry scan (names plus decompressed bytes,
including nested jars) with **zero** occurrences of `alexsmobs` or `alexthe666`,
and, where the mod is config-driven, by grepping the live `/config` tree.

| Mod | Why it is not an integration |
|---|---|
| `moremobvariants` 1.3.0.1 | Its only "alex" hits are the vanilla `zombie/alex.png` skin variant |
| `artifacts` 9.5.19 | No Alex's Mobs references |
| `relics` 0.8.0.13 (core) | No references of its own — the entire link is `ramcompat` |
| `allthewizardgear` 1.1.12 | No references in jar; no `alexs*` entries in its server config |
| `irons_spellbooks` 3.16.2 and all its addons | None reference Alex's Mobs |
| `mowziesmobs` 1.8.2, `mowzies_cataclysm` | No references; no `alexs*` in the 816-line common config |
| `unusualfishmod` 1.1.10 | No references |
| `lootintegrations` 4.7 (+ `lootintegrations_yungs`) | No references; no `alexs*` in the live `lootintegrations.json`. Does not touch Alex's Mobs loot or structures |
| `trimeffects` 2.1.2 | No references; operates on armour trims generically |
| `dummmmmmy` 2.0.12 | No references; reacts to any damage source, not Alex's Mobs specifically |
| `farmersdelight` 1.3.2 | No references of its own — the entire link is `alexsdelight` |
| `curios` 5.14.1 | Alex's Mobs registers no curio slots or items; the only path is `ramcompat` |
| `iceandfire` 2.1.13, `apotheosis`, `aquaculture`, `cataclysm`, and ~130 others | No `alexsmobs`/`alexthe666` string anywhere |

**`domesticationinnovation`** deserves a separate note. Alex's Mobs *ships* data
for it — `data/domesticationinnovation/tags/entity_types/petstore_cage_{0..3}.json`
and `petstore_fishtank.json` are inside the Alex's Mobs jar — but that mod is not
installed on digbuild, so those tags are inert. Likewise Alex's Mobs' default
spawn data names `biomesoplenty`, `incendium`, `byg`, `autumnity` and
`creeperoverhaul` biomes; of that set only Terralith and Alex's Caves are actually
present.

The one blind spot in this method: a mod that keys off a *tag* or an entity class
hierarchy rather than the literal string — something that buffs "all animals" or
"all bosses" — would sweep up Alex's Mobs entities without naming them. A byte
scan cannot see that, and it would not be an integration in any useful sense.

## Sibling mods that are *not* Alex's Mobs add-ons

Easy to conflate, all present on this server, none of them extend Alex's Mobs:

| Mod | What it actually is |
|---|---|
| `alexscaves` 2.0.2 | Alex's Caves — same author, separate mod, deep cave biomes |
| `alexs_caves_spellbooks` 1.1.2 | Iron's Spells bridge for **Alex's Caves**, not Alex's Mobs |
| `raccompat` 0.1.3 | Relics × Alex's **Caves** compat — one letter from `ramcompat` |
| `rarcompat` 0.5 | Relics × **Artifacts** compat, no Alex's-anything involvement |

`raccompat` and `rarcompat` were checked by unzipping each jar: neither declares
`alexsmobs` and neither references a `com.github.alexthe666.alexsmobs` class.
`ramcompat` is the only Relics addon on this server that touches Alex's Mobs.

## Add-ons that exist but are NOT installed

For reference when weighing pack additions. Alex's Mobs has a much larger add-on
ecosystem than Alex's Caves — the list below is what a CurseForge search for
1.20.1 Forge returns, not an exhaustive census, and none of it is on this server.
Versions and 1.20.1 availability were not individually verified; check each
project page before adding one.

| Add-on | Author | What it does |
|---|---|---|
| Alex's Mobs Interaction | CrimsonCrips | The largest add-on — new interactions between Alex's Mobs creatures, the world, and the mod's own tools |
| Alex's Tamables | JayZX535 | Makes more Alex's Mobs creatures tamable |
| Alex's Mobs Extra Music | — | Boss-fight music for Alex's Mobs bosses |
| Alex's Mobs — Naturalist Compat | Kanadeyoru | Merges Alex's Mobs and Naturalist into one system, removing duplicate mobs and items |
| Alex's Mobs — Neapolitan Compat | Kanadeyoru | Removes items duplicated between Alex's Mobs and Neapolitan |
| Mobs of Sins: Alex's Mobs Integration | vortzplays | Integrates Alex's Mobs with Sons of Sins |
| Butchery: Alex's Mobs Addon | jmods | Butchery compatibility (marked WIP) |
| Create: Alex's Mobs | — | Brings Alex's Mobs into Create's automation systems |
| Animal Pens Expansion — Alex's Mobs | — | Animal Pens support for Alex's Mobs creatures |

> **Name collision worth knowing.** There is a second, unrelated Farmer's Delight
> bridge called **"Alex's Mobs Delight"** by *bf_meow*, distinct from the
> **"Alex's Delight"** (`alexsdelight`, NCP Bails) installed here. Both claim to
> add Alex's Mobs × Farmer's Delight compatibility. Installing both would put two
> mods in contention over the same Alex's Mobs loot tables.

## Sources

- `alexsdelight-1.5.jar` and `ramcompat-1.20.1-0.1.4.jar`, pulled from the live
  server's `/mods` via the Pterodactyl client API, unzipped and decompiled. Item
  stats from `ModFoods`/`ModItems`; relic stats from `constructDefaultRelicData()`
  in each item class; display names from each jar's
  `assets/<modid>/lang/en_us.json`; recipes, loot tables and tags read from the
  `data/` trees verbatim.
- `alexsmobs-1.22.9.jar` for the parent-mod loot tables and recipe the add-on
  overrides, its `compat/jei/` package, and `config/DefaultBiomes.java`.
- `relics-1.20.1-0.8.0.1.jar` (bundled in RAM-Compat's `libs/`) for
  `LootCollections`. The server runs Relics 0.8.0.13.
- Live server: `/logs/latest.log` for the Barbecue on a Stick failure,
  `/config/relics.yaml`, `/config/alexsmobs/*_spawns.json`, and a full scan of
  every jar in `/mods`.
- CurseForge and Modrinth project pages for provenance, licensing and the
  not-installed list.

Where a third-party wiki and the code disagreed, the code won and the difference
is called out inline.
