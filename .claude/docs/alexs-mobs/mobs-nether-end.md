<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Nether, End and non-natural mobs

## What this covers

Alex's Mobs registers **116** entity types. This doc covers three slices of that
roster and deliberately leaves the rest to sibling docs:

- **In scope** — every mob whose spawn config targets the Nether or the End, every
  entity that has no natural spawn at all (summoned, transmuted, converted or
  structure-only), the three deep-underground mobs whose live config is shaped
  differently from the rest (Farseer, Murmur, Skreecher, plus the Underminer), and
  every purely technical entity (projectiles, body segments, vehicles).
- **Out of scope** — overworld land animals and overworld aquatic animals, which are
  documented in the parallel land and water docs. Where an in-scope mob interacts
  with one of those (the Crimson Mosquito with the Mungus, the Enderiophage with the
  Endermen), the interaction is described here but the other mob's stats are not.

Stats are read directly out of `bakeAttributes()` in the decompiled entity classes,
so they are exact. Blank cells mean the entity does not override that attribute and
inherits the vanilla default for its base class. Every in-scope mob extends
`Monster` except the Spectre, which extends `Animal`.

The SRG attribute field names were validated against the clean upstream source at
[AlexModGuy/AlexsMobs, branch `1.20`](https://github.com/AlexModGuy/AlexsMobs/tree/1.20):
the Warped Mosco, Farseer, Straddler, Bone Serpent, Void Worm and Laviathan stat
blocks match the decompiled constants field for field and in the same order.
`FLYING_SPEED` is the one field name that has not been directly confirmed — it
appears in this doc only on the Farseer, and is marked inferred there.

## All in-scope mobs by health

| Mob | ID | Where | HP | Attack | Armor | Speed | Follow | KB resist |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Sea Bear | `sea_bear` | Summoned | 200 | 8 | | 0.325 | | |
| Void Worm | `void_worm` | End (summoned) | 160 | 5 | 4 | 0.3 | 256 | |
| Warped Mosco | `warped_mosco` | Nether (converted) | 100 | 10 | 10 | 0.3 | 128 | 1 |
| Farseer | `farseer` | Overworld, world border | 70 | 4.5 | 6 | 0.35 | | |
| Laviathan | `laviathan` | Nether | 60 | 1 | 10 | 0.3 | | 1 |
| Spectre | `spectre` | End | 50 | 2 | | 1.0 | 64 | |
| Warped Toad | `warped_toad` | Nether | 30 | 2 | | 0.2 | 32 | 0.25 |
| Mimicube | `mimicube` | End City | 30 | 2 | | 0.45 | 32 | |
| Murmur | `murmur` | Deep underground | 30 | 3 | | 0.2 | 48 | 0.3 |
| Murmur (head) | `murmur_head` | — | 30 | 3 | | 0.2 | 48 | |
| Void Worm segment | `void_worm_part` | — | 30 | | | 0.15 | | |
| Straddler | `straddler` | Nether | 28 | 2 | 5 | 0.3 | 32 | 0.8 |
| Bone Serpent | `bone_serpent` | Nether | 25 | 5 | | 1.45 | 32 | |
| Endergrade | `endergrade` | End | 20 | 2 | 0 | 0.15 | | |
| Enderiophage | `enderiophage` | End | 20 | 2 | | 0.15 | 16 | |
| Cosmaw | `cosmaw` | End | 20 | 1 | | 0.3 | 32 | |
| Underminer | `underminer` | Mineshafts | 20 | 3 | | 0.2 | 64 | |
| Soul Vulture | `soul_vulture` | Nether Fossils | 12 | 4 | | 0.25 | 18 | |
| Crimson Mosquito | `crimson_mosquito` | Nether | 10 | 5 | 0 | 0.25 | 32 | |
| Bone Serpent segment | `bone_serpent_part` | — | 10 | | | 0.15 | | |
| Cosmic Cod | `cosmic_cod` | End | 4 | | | 0.35 | | |
| Stradpole | `stradpole` | Nether | 4 | | | 0.3 | | |
| Skreecher | `skreecher` | Deep Dark | 2 | 1 | | 0.2 | 64 | |

The Farseer also sets flying speed 0.5. The Void Worm's health is not a code
constant — it reads `voidWormMaxHealth` from config, which this server leaves at the
default **160**.

## Hostility

| Attitude | Mobs |
|---|---|
| Attacks players on sight | Bone Serpent, Crimson Mosquito, Warped Mosco, Soul Vulture, Straddler, Mimicube, Farseer, Skreecher, Murmur (via its head), Void Worm, Sea Bear |
| Retaliates only | Laviathan, Underminer, Cosmaw, Enderiophage (targets Endermen and Ender-Flu carriers, not players) |
| Passive | Warped Toad, Stradpole, Endergrade, Cosmic Cod, Spectre |

Bone Serpents are hostile because the live config sets `neutralBoneSerpents = false`;
flipping it to `true` removes their player and villager target goals entirely.

## Drops

From `data/alexsmobs/loot_tables/entities/`. Ranges are before Looting.

| Mob | Drops |
|---|---|
| Bone Serpent | `bone_serpent_tooth ×0–1`, `bone ×10–15`, `bone_block ×1–4` |
| Crimson Mosquito | `mosquito_proboscis` 10% |
| Crimson Mosquito (with blood) | `mosquito_proboscis` 10%, `blood_sac` 80% |
| Crimson Mosquito (grown from a Fly) | `mosquito_proboscis` 30%, `blood_sac` 10% |
| Crimson Mosquito (from a Fly, with blood) | `mosquito_proboscis` 50%, `blood_sac` (always) |
| Warped Mosco | `warped_muscle` 70%, `hemolymph_sac ×1–5` |
| Warped Toad | one of `shroomlight ×0–1` or `nether_wart ×0–1` (equal weight) |
| Soul Vulture | `bone ×0–2`, `coal ×0–1` |
| Soul Vulture (3+ souls) | `bone ×0–2`, `coal ×0–1`, `soul_heart ×0–1` |
| Straddler | `straddlite` 20%, `basalt ×0–3` |
| Stradpole | *(loot table has no pools)* |
| Laviathan | `magma_block ×0–3`, `blackstone ×0–3` |
| Laviathan (obsidian-crusted) | `obsidian ×0–3`, `blackstone ×0–3` |
| Skreecher | `skreecher_soul` — **only when killed by a player** |
| Murmur | `unsettling_kimono` or `red_wool ×0–1` (weights 1 and 9), plus `elastic_tendon ×0–2` |
| Spectre | *(loot table has no pools)* |
| Endergrade | *(loot table has no pools; drops its saddle if saddled)* |
| Enderiophage | `capsid ×1` |
| Cosmaw | `chorus_fruit ×0–1` |
| Cosmic Cod | `cosmic_cod ×1`, plus `bone_meal` 5% |
| Mimicube | `mimicream ×-1–1` |
| Void Worm (head) | `void_worm_eye ×1`, `void_worm_mandible ×2` |
| Void Worm (split half) | *(loot table has no pools)* |
| Farseer | `farseer_arm ×0–1` |
| Underminer | *(loot table `ghost_miner` has no pools)* |
| Sea Bear | *(loot table has no pools)* |

Looting adds `0–1` to most of the fixed-count rows, `0–3` to the Bone Serpent's
bones and `0–2` to its bone blocks; the percentage drops use a looting multiplier of
0.01–0.1 per level, so Looting moves them by one to ten points per level.

The Mimicube's `×-1–1` is the mod's own count range: roughly a two-in-three chance of
one Mimicream and a one-in-three chance of nothing.

The Underminer carries a **Ghostly Pickaxe** in its main hand. Its loot table is
empty, so the pickaxe dropping through the normal equipment-drop path is the only
thing it can leave behind, and only when a player lands the kill.

Six loot tables have no pools at all — `stradpole`, `spectre`, `endergrade`,
`void_worm_splitter`, `ghost_miner` and `sea_bear`.

## Where each one spawns

Translated from the live `/config/alexsmobs/*.json` biome files and the `[spawning]`
section of `/config/alexsmobs.toml`. **Weight** is the entry's share of the biome's
spawn pool; **rolls** is an extra `1-in-N` filter applied on top, so rolls 40 means
39 out of 40 attempts are discarded. Rolls 0 means no extra filter.

### Nether

| Mob | Biomes | Group | Weight | Rolls | Placement |
|---|---|---|---:|---:|---|
| Bone Serpent | every Nether biome that allows default monsters | 1 | 8 | 40 | in lava, with air above the lava column |
| Crimson Mosquito | Crimson Forest, plus the modded Crimson Gardens, Visceral Heap, Ash Barrens and Infernal Dunes | 4 | 15 | 0 | on solid ground, dark enough for monsters |
| Warped Toad | Warped Forest, plus Crimson Gardens, Warped Desert, Inverted Forest and Quartz Flats | 5 | 30 | 0 | on solid ground or on lava |
| Soul Vulture | **Nether Fossil structures only** | 1–3 | 30 | 0 | on soul fire base blocks or its own perch blocks |
| Straddler | Basalt Deltas, plus Withered Abyss, Volcanic Deltas and Withered Forest | 1–3 | 70 | 0 | on ground |
| Stradpole | same four biomes as the Straddler | 1 | 10 | 3 | in lava |
| Laviathan | every Nether biome | 1 | 15 | 1 | in lava |
| Warped Mosco | **none** | 1 | 1 | 1000 | see below |

`soulVultureSpawnOnFossil = true` on this server, so the Soul Vulture's biome list is
ignored entirely and it is added to the Nether Fossil structure's own spawn table
instead. Its listed biomes only take effect if that flag is turned off.

The Warped Mosco's biome list is empty and its roll filter is 1-in-1000, so it never
spawns naturally under any circumstances. It only exists by conversion.

### End

| Mob | Biomes | Group | Weight | Rolls | Placement |
|---|---|---|---:|---:|---|
| Endergrade | every End biome except the central island | 2–6 | 10 | 0 | no placement restriction |
| Enderiophage | End biomes other than the central island, End Barrens, End Highlands and Small End Islands | 2 | 4 | 2 | no placement restriction |
| Cosmaw | End biomes other than the central island and Small End Islands | 1–2 | 9 | 0 | no placement restriction |
| Cosmic Cod | every End biome, including the central island | 9–13 | 5 | 0 | ambient category |
| Spectre | every End biome except the central island | 1–2 | 10 | 5 | — |
| Mimicube | **End City structures only** | 1–3 | 40 | 0 | on ground |
| Void Worm | **none** | 1 | 0 | 0 | see below |

`mimicubeSpawnInEndCity = true`, so the Mimicube's biome list is ignored and it is
added to the End City structure spawn table instead. The Void Worm's weight is 0 and
its biome list is empty; it is summon-only.

### Deep underground and structures

| Mob | Where | Group | Weight | Rolls |
|---|---|---|---:|---:|
| Farseer | any overworld biome that allows monsters except Mushroom Fields, and only **within 100 blocks of the world border** | 1 | 30 | 0 |
| Murmur | any non-ocean, non-mushroom overworld biome except the Deep Dark, plus twelve named Terralith cave biomes; must be **below y = -30** and unable to see sky | 1 | 5 | 1 |
| Skreecher | **Deep Dark only**, standing on sculk, dark enough for monsters | 1 | 10 | 1 |
| Underminer | **abandoned mineshafts only** | 1 | 50 | 1 |

`restrictFarseerSpawns = true` with `farseerBorderSpawnDistance = 100`, so on this
server the Farseer is a world-border mob and appears nowhere else.
`restrictUnderminerSpawns = true` removes the Underminer's biome spawns entirely and
adds it to the mineshaft structure's ambient spawn table instead. Both mobs' biome
lists are still in config but are inert while those flags are on.

The Murmur's height cap comes from `murmurSpawnHeight = -30`; biomes tagged
`alexsmobs:spawns_murmurs_ignore_height` bypass it.

### No natural spawn at all

| Mob | Trigger |
|---|---|
| Warped Mosco | A Crimson Mosquito drinks from a Mungus that is ready to trigger it |
| Void Worm | A Mysterious Worm item drops into the void in the End |
| Sea Bear | Swimming while wearing a Sombrero, on April 1 only |
| Enderiophage | Also obtainable by hatching a Capsid (below) |
| Straddler | Also obtainable by feeding a Stradpole (below) |

## Nether mobs

### Bone Serpent — 25 HP, 5 attack

A segmented lava swimmer with 7–14 trailing `bone_serpent_part` segments. The
segments have 10 HP each but exist for collision and rendering; damage is dealt to
the head. It navigates lava and water, and leaps clear of the surface — it also
leaps deliberately near a ridden Straddleboard, on a 100–400 tick cooldown.

It targets players and villagers on sight, and also hunts Wither Skeletons and Soul
Vultures regardless of the neutrality setting. A player riding a **Straddleboard
enchanted with Serpent Friend** is excluded from all of those target goals, so
serpents ignore them. `straddleboardEnchants = true` on this server.

Its tooth brews with a Lava Bottle to make the **Lava Vision** potion.

### Crimson Mosquito — 10 HP, 5 attack

Latches onto its target as a rider and drinks. Every 20 ticks (1 second) attached it
deals **2 damage** and gains a blood level; above blood level 3 it detaches. It also
detaches after 81 ticks regardless. Detached, it spits `mosquito_spit` projectiles
for **4 damage**.

Its loot table depends on two flags: whether it is carrying blood, and whether it
grew from a Fly rather than spawning as a mosquito. All four combinations are listed
in the drops table.

Two things turn a mosquito into a Warped Mosco:

- Drinking from a **Mungus** that is ready to trigger the transformation. That bite
  deals **7 damage** instead of 2 and disables the mungus's explosion.
- Being fed a **Warped Mixture** by hand.

Either way the mosquito becomes "sick", stops flying, swells for 160 ticks
(8 seconds) and is then replaced by a Warped Mosco. `warpedMoscoTransformation = true`
on this server, and `warpedMoscoMobTriggers` is empty, so the Mungus is the only mob
that triggers it. No recipe, loot table or code path in the jar grants a Warped
Mixture, so how it is obtained is **not documented** in the mod's own data.

A Warped Toad's tongue kills a Crimson Mosquito outright, whatever its health.

### Warped Mosco — 100 HP, 10 attack, 10 armor, immune to knockback

Four attacks, chosen by distance and situation:

| Attack | Effect |
|---|---|
| Punch | 10 damage plus heavy knockback, within 4.7 blocks |
| Slam | 10–18 damage to everything within 5 blocks, plus knock-up |
| Suck | Grabs the target as a passenger; every 4 ticks it deals 10 damage and gives itself Regeneration II for 5 seconds |
| Spit | Fires 2–3 Hemolymph globs, **7 damage** each |

If the target is already riding something when the Mosco would grab it, the Mosco
slams instead. It hunts players and anything in `alexsmobs:crimson_mosquito_targets`
— the mod's passive and neutral land animal tags plus villagers — out to 50 blocks.

### Warped Toad — 30 HP, 2 attack

Passive toward players. It hunts Silverfish, Spiders, Cave Spiders, Flies,
Cockroaches, Leafcutter Ants, Tarantula Hawks, Crimson Mosquitoes and Warped Moscos
with a tongue attack that drags the target in and deals its 2 attack damage — except
against a Crimson Mosquito, which the tongue kills instantly.

Tame it by feeding **Mosquito Larva**, with a 1-in-3 chance per larva. A tamed toad
takes command cycles (wander / follow / stay) on empty-handed use, defends its owner,
and heals 5 when fed anything in `alexsmobs:insect_items` (Maggot, Mosquito Larva,
Leafcutter Ant Pupa). It breeds with Mosquito Larva. It is not rideable.

### Soul Vulture — 12 HP, 4 attack

Circles a perch and dive-tackles. Each successful tackle deals its 4 attack damage,
heals it by the same amount and adds a soul level, up to 5, on a 100–300 tick
cooldown. It only gains a soul if it is missing at least that much health.

At **3 or more souls** it switches to a second loot table and can drop a **Soul
Heart**, which is what a Spectre in the End is attracted to. Bone Serpents hunt Soul
Vultures.

### Straddler — 28 HP, 2 attack, 5 armor

Walks on stilts through lava, standing above the surface. Its ranged attack, on a
30-tick cycle out to 16 blocks, is to **launch a live Stradpole** at the target: 3
damage plus knockback, and the stradpole then ricochets up to 20 times or 200 ticks
before landing. A blocked hit damages the shield instead.

It drops **Straddlite**, which is the ingredient for the whole Nether-riding kit:

| Item | Recipe |
|---|---|
| Straddleboard | 4 Straddlite + 4 Netherite Ingots |
| Straddle Saddle | 2 Straddlite + 2 Saddles |
| Straddle Helmet | 4 Straddlite + 2 String |
| Straddlite Block | 9 Straddlite |

### Stradpole — 4 HP

The Straddler's larval form and its ammunition. Bucketable with a **lava bucket**.
Feeding it a **Mosquito Larva** turns it into a Straddler with a 45% chance per
larva; a failed attempt still consumes the larva.

### Laviathan — 60 HP, 1 attack, 10 armor, immune to knockback

A rideable lava whale. It is not tamed — it is tacked:

1. Give it a **Straddle Saddle** to make it rideable.
2. Give it a **Straddle Helmet** for the head gear.
3. Use on it empty-handed while it has the saddle to mount. Babies cannot be ridden.

Feed **Magma Cream** to heal 10; breed with **Mosquito Larva**. Its listed attack
damage of 1 is genuinely 1 — its size and block-breaking, not its bite, are what
matter.

Entering water crusts it in obsidian: it switches to the `laviathan_obsidian` loot
table and drops obsidian instead of magma blocks.

## End mobs

### Endergrade — 20 HP, 2 attack

Passive. Eats Chorus Fruit and Chorus Flowers off the ground (healing 5 each) and
breaks chorus flower blocks. Breeds with Chorus Fruit.

Give it a **Saddle** to make it rideable, then use empty-handed to mount; it is
steered with a **Chorus on a Stick** (Fishing Rod + Chorus Fruit). It drops the
saddle on death.

It is the natural carrier of **Ender Flu** — Enderiophages seek out Endergrades and
anything already infected. Feeding a Chorus Fruit to an infected Endergrade heals it
8 and cures the flu.

### Enderiophage — 20 HP, 2 attack

A bacteriophage that attaches to a living target rather than biting it. Attached, it
deals **6 damage** per strike, dropping to 1 if the target is below 20% health. On a
successful hit against a non-Enderman, there is a 1-in-3 chance it injects **Ender
Flu** for 12000 ticks (10 minutes), stacking one amplifier level per injection up to
level 4, heals itself 5, and loses its eye — after which it disengages and stops
targeting.

Against an **Enderman** it does something different: it takes the enderman's eye
back, heals 5, inflicts Blindness for 20 seconds, and flees for 400 ticks. Damage
dealt to a phage *by* an Enderman is reduced to `(damage + 1) × 0.35`.

Its colour follows the dimension it is in — one skin for the End, one for the
Overworld, one for the Nether.

It drops a **Capsid** every time. A Capsid placed as a block converts items over
120 ticks (6 seconds):

| Input | Output |
|---|---|
| Cod | Cosmic Cod |
| Mosquito Larva | **Mysterious Worm** |
| Any music disc | Music Disc "Daze" |
| Dimensional Carver | Shattered Dimensional Carver (200 ticks) |

A Capsid holding an **Ender Eye** and placed directly on top of a vertical End Rod
hatches a new Enderiophage after 20 ticks, destroying both blocks.

### Cosmaw — 20 HP, 1 attack

A floating claw that grabs items out of the air. Throw it a **Cosmic Cod**: it
catches it, eats it after 30 ticks, and has a **30% chance** per fish to tame to
whoever threw it. Anything else it catches is simply eaten or dropped.

A tamed Cosmaw's headline behaviour is catching its falling owner. If the owner is
falling without an elytra, or drops below y = -30, the Cosmaw closes in, picks them
up as a passenger and flies them back to the last safe ground it recorded, ejecting
them once it arrives. It teleports to the owner if they are more than 100 blocks
away or below y = -20.

Empty-handed use cycles wander / follow / stay. It breeds with Cosmic Cod, and hunts
wild Cosmic Cod out to 80 blocks.

### Cosmic Cod — 4 HP

An ambient End fish that swims through the air in schools of 9–13. Bucketable.
Drops itself, plus Bone Meal 5% of the time. It is the Cosmaw's taming item and
breeding item, and is craftable from Cod in a Capsid.

### Mimicube — 30 HP, 2 attack

Spawns only inside **End Cities**, in groups of 1–3. When something attacks it, it
copies that attacker's helmet, main-hand item and off-hand item onto itself — and
uses them: it blocks with a copied shield, and fires arrows or throws a trident if it
copied a bow or trident. Every copy is created **already at maximum damage**, so it
is one hit from breaking.

It drops **Mimicream**, which duplicates items (`mimicreamRepair = true` on this
server). The blacklist is `alexsmobs:blood_sprayer` and `alexsmobs:hemolymph_blaster`
— those two cannot be copied.

### Spectre — 50 HP, passive

A flying End whale that ignores blocks entirely — it has no gravity, no fall damage
and `noPhysics` is set every tick, so it drifts straight through terrain. It is
**invulnerable to everything except magic damage**, the void, creative-mode players,
and sources tagged as bypassing invulnerability.

It is drawn to a player holding a **Soul Heart** (from a Soul Vulture with 3+ souls)
from up to 64 blocks away. Leash it and it becomes transport: past 10 blocks the
leash drags the holder along, cancels their fall distance and damps their descent.
Sneak to let go.

It drops nothing and cannot be bred.

## Deep underground

### Murmur — 30 HP, 3 attack

Spawns below y = -30, out of sight of the sky, anywhere in the overworld except
oceans, mushroom biomes and the Deep Dark. The body is neutral and only retaliates —
but it permanently carries a second entity, the **`murmur_head`**, which is what
actually hunts. The head targets players within 10 blocks and villagers within 30,
detaches from the neck, circles for 30 ticks, then closes and bites for **5 damage**
on a 5–20 tick cooldown. Past 64 blocks from the body it snaps back.

Damage dealt to the head is passed to the body at **half value** first; the head is
destroyed when the body dies, and the body regrows a head the moment it lacks one.
Killing the body is the only way to end it.

It drops **Elastic Tendon** (crafts the Tendon Whip with Dropbear Claws) and, on a
1-in-10 weighted roll, the **Unsettling Kimono** chestplate. Wearing the kimono stops
undead mobs from targeting you unless you hit them first — with three exceptions
listed in `alexsmobs:ignores_kimono`: the Wither, the Murmur and the Murmur's head.

### Skreecher — 2 HP, 1 attack

Deep Dark only, spawning on sculk in the dark, one at a time. It clings upside-down
to ceilings and claps. Every 8 ticks of clapping it **angers every Warden within
range that can see it**, and after 100 ticks of continuous clapping it **summons a
Warden** — once per skreecher, only if there is no Warden nearby already, and only in
a biome tagged `alexsmobs:skreechers_can_spawn_wardens` (the Deep Dark). The summoned
Warden spawns angry at the skreecher, not at the player.
`skreechersSummonWarden = true` on this server.

Any damage knocks it off the ceiling and stops it clapping for 200–400 ticks. With
2 HP that is usually academic.

It drops a **Skreecher Soul** only when a player lands the kill; three of them plus
sculk and bone blocks craft a **Sculk Boomer**.

### Underminer — 20 HP, 3 attack

A ghost miner restricted to abandoned mineshafts. It floats without gravity, passes
through walls, takes no fall damage, and patrols the mineshaft's corridors.

Its behaviour is an ore detector. It looks for ore blocks within 16 blocks that a
player *cannot* see — blocked by up to 4 blocks of stone — flies to the block that is
hiding one, and mimes mining that face. The block it is pretending to mine is the
wall between you and the ore.

Throw it any item tagged `#forge:ores` and for the next 2000–3200 ticks it will hunt
only that specific ore.

It **vanishes when a player comes within 8 blocks** (`underminerDisappearDistance`),
and while fully hidden it cannot be attacked or targeted. It is neutral and only
retaliates. It carries a Ghostly Pickaxe; its loot table is empty.

## Bosses

Only one entity in scope has a boss bar.

### Void Worm — 160 HP, 5 attack, 4 armor

**Not a natural spawn.** Craft a **Mysterious Worm** by putting a Mosquito Larva in a
Capsid, then **drop the item into the void in the End**. When the dropped item falls
below y = -60 in a dimension listed in `voidWormSpawnDimensions` (this server:
`minecraft:the_end` only) it is consumed and a Void Worm rises from y = 0 with
**25–39 segments**. `voidWormSummonable = true` and `voidWormDamageModifier = 1.0`.

It shows a blue boss bar that darkens the sky. It is immune to fall, drowning,
suffocation, lava, void and all fire damage, and never despawns.

**The fight has three repeating modes:**

| Mode | Behaviour |
|---|---|
| Circle | Orbits the target and spits **four Void Crystals** at a time. Every 40 ticks at full health, every **15 ticks once damaged**. Runs 60–260 ticks. |
| Slam rise | Climbs to 20–40 blocks above the target. |
| Slam fall | Dives at double speed through the target's position. |

Anything caught inside its mouth takes **8–16 damage** and is launched. A **Void
Crystal** hit deals **4 damage** and **disables the player's shield**.

**It splits.** Killing a body segment cuts the worm in two: the tail half becomes a
new worm with **half the parent's maximum health**, 80% of its speed, and the
`void_worm_splitter` loot table, which is empty. Splitters give less experience and
drop nothing. Only the original head drops loot, so cutting the worm apart destroys
part of the reward.

It also **opens portals**. It creates one to a random destination on an idle timer
(200–1200 ticks between attempts), and if it is stuck against terrain for more than
40 ticks it opens one next to its target and comes through it.

**Head drops:** 1 Void Worm Eye and 2 Void Worm Mandibles. The drops are spawned with
no gravity, permanently glowing and with an unlimited lifetime, inside a shell of
slow-decaying Ender Residue, so they cannot fall into the void.

| Made from the drops | Recipe |
|---|---|
| Void Worm Beak | 2 Mandibles |
| Dimensional Carver | 2 Mandibles + 1 Eye + 2 Netherite Ingots |
| Void Worm Effigy | 1 Beak + 2 Ender Pearls + 4 Purpur Blocks |

### Farseer — 70 HP, 4.5 attack, 6 armor

No boss bar and no phases, but it fights unlike anything else in the mod, and on this
server it is a world-border encounter — `restrictFarseerSpawns = true` limits it to
within 100 blocks of the border.

It spawns **invisible** and stays that way until a player comes within 9 blocks, at
which point it plays an emerge animation. **It is invulnerable for the whole of that
animation.**

Two attacks:

- **Melee**, inside 4 blocks: strikes with a random one of its four arms for
  **5–9 damage**.
- **Beam**, beyond 2 blocks with line of sight: charges, then deals
  `random(0–1) + max(6, 10% of the target's maximum health)` as `alexsmobs:farseer`
  damage. It fires up to 6 beams, then goes on an 80–120 tick cooldown. It stops
  moving inside 17 blocks while beaming.

Because the beam scales off *your* maximum health, extra hearts do not reduce the
number of beams it takes to kill you.

It drops a **Farseer Arm** (0–1), which crafts the **Transmutation Table** with a
Nether Star and 3 Obsidian. Its flying speed attribute is 0.5 — the one attribute
value in this doc read through an inferred SRG field name.

## Summoned and April Fools

### Sea Bear — 200 HP, 8 attack

**April 1 only.** While a player is in water wearing a **Sombrero**, there is a
1-in-245 chance per tick that a Sea Bear spawns 10–31 blocks away already targeting
them. If a Sea Bear is already within 32 blocks, no new one spawns and the existing
ones retarget instead.

Standing on a **Sand Circle** or **Red Sand Circle** block makes a player exempt, as
does creative mode. It drops nothing.

`AlexsMobs.isAprilFools()` returns true either on April 1 by the server's clock or
whenever `superSecretSettings` is enabled. This server has
`superSecretSettings = false`, so the date is the only trigger.

## Technical entities

These are registered entity types with no natural spawn and no independent behaviour
— projectiles, body segments, vehicles and markers. They exist as targets and
carriers, not as mobs, and are listed here only so the roster is complete.

| Entity | ID | What it is |
|---|---|---|
| Bone Serpent Bones | `bone_serpent_part` | Bone Serpent tail segment, 10 HP |
| Void Worm | `void_worm_part` | Void Worm body segment, 30 HP; killing one splits the worm |
| Murmur | `murmur_head` | The Murmur's detachable head, 30 HP, bites for 5 |
| Void Crystal | `void_worm_shot` | Void Worm projectile, 4 damage, disables shields |
| Void Portal | `void_portal` | Portal the Void Worm opens and travels through |
| Mosquito Blood | `mosquito_spit` | Crimson Mosquito projectile, 4 damage |
| Hemolymph | `hemolymph` | Warped Mosco projectile, 7 damage |
| Straddleboard | `straddleboard` | Rideable lava board crafted from Straddlite and Netherite |
| Enderiophage Rocket | `enderiophage_rocket` | Firework-style rocket crafted from a Capsid |
| Anaconda | `anaconda_part` | Anaconda body segment |
| Cave Centipede Body / Tail | `centipede_body`, `centipede_tail` | Cave Centipede segments |
| Whale Echo | `cachalot_echo` | Cachalot Whale echolocation pulse |
| Cockroach Ootheca | `cockroach_egg` | Cockroach egg |
| Emu Egg | `emu_egg` | Thrown emu egg (registered with no display name) |
| Ice Shard | `ice_shard` | Froststalker projectile (registered with no display name) |
| Fart Cloud | `fart` | Area effect cloud |
| Gust | `gust` | Guster projectile |
| Mud Ball | `mud_ball` | Thrown mud |
| Pollen Ball | `pollen_ball` | Thrown pollen |
| Thrown Sand | `sand_shot` | Pocket Sand projectile |
| Shark Tooth Arrow | `shark_tooth_arrow` | Arrow variant |
| Tentacle | `squid_grapple` | Squid Grapple hook |
| Tendon | `tendon_segment` | Tendon Whip segment |
| Tossed Item | `tossed_item` | Item thrown by a mob |
| Vine Lasso | `vine_lasso` | Thrown lasso |

Three ids that appear in the language file have **no registered entity** and are only
display names reused by other entities: `cachalot_part`, `giant_squid_part` and
`crocodile_egg`.

## Damage types

Alex's Mobs adds two custom damage types, in `data/alexsmobs/damage_type/`.

| Damage type | Exhaustion | Scaling |
|---|---:|---|
| `alexsmobs:farseer` | 0.1 | `when_caused_by_living_non_player` |
| `alexsmobs:freddy` | 0.1 | `never` |

**Neither type is in any damage type tag** — not `bypasses_armor`, not
`bypasses_invulnerability`, not `bypasses_resistance`, not `is_fire` or `is_projectile`.
So both are ordinary damage as far as mitigation goes: armour, Protection,
Resistance, absorption and invulnerability frames all apply normally. What is custom
about them is the trigger and the death message.

**`alexsmobs:farseer`** is dealt only by the Farseer's beam, for
`random(0–1) + max(6, 10% of the target's maximum health)`. Its scaling is
`when_caused_by_living_non_player`, so unlike most of the mod's damage it *is*
difficulty-scaled — this server runs `difficulty=easy`, which reduces it. It picks
one of **three** death messages at random, each equally likely:

| Key | Message |
|---|---|
| `death.attack.farseer_0` | *"%s was turned to static"* |
| `death.attack.farseer_1` | *"%s had the channels changed on them"* |
| `death.attack.farseer_2` | *"%s was sent to the 4th dimension"* |

Each also has a `.player` variant used when the kill is credited to a killer.

The language file ships a **fourth** pair of keys, `death.attack.farseer_3` /
`death.attack.farseer_3.player` — *"%s was disintegrated"* — that is **unreachable**.
`DamageSourceRandomMessages` in `misc/AMDamageTypes.java` picks the index with
`attacked.m_217043_().m_188503_(3)`, i.e. `nextInt(3)`, so the index is only ever
0, 1 or 2. The message is a dead key and never appears in game.

**`alexsmobs:freddy`** is dealt only by the Grizzly Bear's April Fools jumpscare
routine, which is gated behind `AlexsMobs.isAprilFools()` — April 1 by the server's
clock, or `superSecretSettings` (false here). A grizzly picks a player within 13
blocks that does not already have the Power Down effect, applies **Power Down**,
plays a music box for 100–230 ticks, then leaps. Its damage is not a number the
player can survive by having more health:

- In a **hardcore** world it deals `maxHealth - 1` and then sets the player's health
  to 1, so the player lives.
- Otherwise it deals `maxHealth + 1000`, which is unconditionally lethal.

This server is not hardcore, so the lethal branch is the one that applies. Its
scaling is `never`, so difficulty does not change it. Death message: *"Was that the
bite of '87?"*
