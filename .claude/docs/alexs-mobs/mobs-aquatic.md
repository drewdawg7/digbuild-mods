<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Aquatic creatures

## What this doc covers

Every Alex's Mobs creature whose live spawn configuration places it **in or at the
edge of water** — ocean, river, swamp water, and beach. Twenty-three entities:

| Included | Why |
|---|---|
| Blobfish, Cachalot Whale, Comb Jelly, Devil's Hole Pupfish, Flying Fish, Frilled Shark, Giant Squid, Hammerhead Shark, Lobster, Mantis Shrimp, Mimic Octopus, Orca, Skelewag, Triops | Fully aquatic; spawn placement `IN_WATER` |
| Catfish, Terrapin | Fully aquatic; river and swamp water |
| Alligator Snapping Turtle, Caiman, Crocodile, Mudskipper, Platypus, Seal | Semi-aquatic; live in the water body their spawn config names |
| Sea Bear | Aquatic, not naturally spawned — see [Sea Bear](#sea-bear) |

Deliberately **not** covered here, and left to the land / Nether / End docs:
Anaconda, Shoebill and Seagull (swamp and beach *biomes*, but land- or air-dwelling),
Rain Frog (desert), Cosmic Cod and Laviathan (not overworld water). Triops shares the
Rain Frog's desert biome list but spawns `IN_WATER`, so it is here.

Two lang ids in the aquatic range — `cachalot_part` and `giant_squid_part` — are
multipart hitbox segments of the Cachalot Whale and Giant Squid, not separate mobs.
They are documented under those two entries and do not appear in the tables.

## Provenance

- **Stats** are read out of `bakeAttributes()` in the decompiled entity classes
  (jadx over `alexsmobs-1.22.9.jar`, pulled from the live server's `/mods`). The SRG
  attribute field names were validated by diffing those bodies against the clean
  upstream source at [`AlexModGuy/AlexsMobs@1.20`](https://github.com/AlexModGuy/AlexsMobs/tree/1.20),
  which is the same `version = '1.22.9'` as the installed jar. `Attributes.f_22276_`
  = `MAX_HEALTH`, `f_22277_` = `FOLLOW_RANGE`, `f_22278_` = `KNOCKBACK_RESISTANCE`,
  `f_22279_` = `MOVEMENT_SPEED`, `f_22281_` = `ATTACK_DAMAGE`, `f_22284_` = `ARMOR`.
  No mob in this doc uses `FLYING_SPEED`.
- **Drops** come from `data/alexsmobs/loot_tables/entities/*.json` in the jar, plus
  the code paths that call `spawnAtLocation` directly (noted inline).
- **Spawning** combines the live server's `/config/alexsmobs/*_spawns.json` biome
  lists, the weights and rolls in `/config/alexsmobs.toml`, and the pack sizes
  hardcoded in `AMWorldRegistry`.
- **Mechanics** are read from the entity classes and their AI goals. Blank cells in
  the stat table mean the entity does not override that attribute.

`alexsmobs.fandom.com` returns HTTP 402 and was not used.

## All aquatic mobs by health

| Mob | ID | Disposition | HP | Attack | Armor | Speed | Follow | KB resist |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Sea Bear | `sea_bear` | Hostile | 200 | 8 | | 0.325 | | |
| Cachalot Whale | `cachalot_whale` | Neutral | 160 | 30 | | 1.2 | 32 | 1 |
| Orca | `orca` | Neutral | 60 | 10 | 0 | 1.35 | 64 | 0.7 |
| Giant Squid | `giant_squid` | Neutral | 38 | 8 | | 0.25 | | |
| Crocodile | `crocodile` | Hostile | 30 | 10 | 8 | 0.25 | 15 | 0.4 |
| Hammerhead Shark | `hammerhead_shark` | Hostile | 30 | 5 | 0 | 0.5 | | |
| Caiman | `caiman` | Neutral | 20 | 3 | 8 | 0.2 | | |
| Frilled Shark | `frilled_shark` | Neutral | 20 | 3 | 0 | 0.2 | | |
| Mantis Shrimp | `mantis_shrimp` | Neutral | 20 | 3 | 8 | 0.3 | 32 | 0.1 |
| Skelewag | `skelewag` | Hostile | 20 | 3 | | 0.45 | | |
| Alligator Snapping Turtle | `alligator_snapping_turtle` | Hostile | 18 | 4 | 8 | 0.2 | 16 | 0.7 |
| Mimic Octopus | `mimic_octopus` | Passive | 16 | 2 | 0 | 0.2 | | |
| Mudskipper | `mudskipper` | Neutral | 12 | 2 | | 0.2 | | |
| Catfish | `catfish` | Passive | 10 / 20 / 30 | | | 0.25 | | |
| Platypus | `platypus` | Passive | 10 | | | 0.2 | 16 | |
| Seal | `seal` | Neutral | 10 | 2 | | 0.18 | | |
| Terrapin | `terrapin` | Passive | 10 | | 10 | 0.1 | | |
| Blobfish | `blobfish` | Passive | 8 | | | 0.25 | | |
| Comb Jelly | `comb_jelly` | Passive | 6 | | | 0.2 | | |
| Flying Fish | `flying_fish` | Passive | 6 | | | 0.3 | | |
| Lobster | `lobster` | Neutral | 5 | 2 | 2 | 0.15 | | |
| Triops | `triops` | Passive | 4 | | | 0.25 | | |
| Devil's Hole Pupfish | `devils_hole_pupfish` | Passive | 2 | | | 0.34 | | |

Notes on the table:

- **Cachalot Whale and Orca speeds** look wrong but are not — both use the vanilla
  Dolphin scale (`MOVEMENT_SPEED` 1.2), which is a different unit from a land mob's
  0.25. They are not five times faster than a shark.
- **Catfish health** is overwritten on spawn from the size the fish rolls:
  10 (small), 20 (medium), 30 (large).
- **Cachalot Whale albinos** override both values: 230 health and 45 attack.
- **Disposition** is derived from the target goals. "Neutral" means it has no
  unprovoked player target but will retaliate or defends prey; "hostile" means it
  has a goal that targets players (or, for the Alligator Snapping Turtle, anything
  that enters its bite box) without provocation.

## Spawning

Biome lists are from the live `/config/alexsmobs/` files. Weight is added to the
biome's pool for that spawn category — a bigger number is a bigger share of that
pool, not an absolute rate. "Rolls" is an extra gate applied per attempt: `N` means
a 1-in-`N` chance, and `0` or `1` means no gate at all.

| Mob | Where | Weight | Rolls | Pack |
|---|---|---:|---:|---|
| Alligator Snapping Turtle | Swamps except Mangrove Swamp; Tundra Bog, Ice Marsh, Orchid Swamp | 20 | 1 | 1–2 |
| Blobfish | Deep oceans, at **y 25 or below** | 30 | — | 2 |
| Cachalot Whale | Cold oceans, Lukewarm Ocean, Deep Ocean, Deep Lukewarm Ocean, Abyssal Chasm — under open sky, within 15 blocks of sea level | 2 | — | 1–2 |
| Caiman | Mangrove Swamp, Underground Jungle; must stand on mud or muddy mangrove roots | 29 | — | 2–4 |
| Catfish | Swamps except Mangrove Swamp; non-cold rivers; Orchid Swamp, Ice Marsh, Warm River | 4 | 2 | 1–3 |
| Comb Jelly | Frozen Ocean, Deep Frozen Ocean, Abyssal Chasm — at night, light level 4 or lower | 5 | 1 | 2–3 |
| Crocodile | Swamps, Mangrove Swamp, non-cold rivers, Tropic Beach, Orchid Swamp, Red Oasis, Warm River | 20 | 1 | 1–2 |
| Devil's Hole Pupfish | **One chunk in the whole world** — see below | 23 | — | 5–12 |
| Flying Fish | Temperate oceans only (not cold, not hot, not deep) | 8 | — | 3–6 |
| Frilled Shark | Deep oceans | 11 | — | 1 |
| Giant Squid | Deep oceans | 3 | — | 1–2 |
| Hammerhead Shark | Hot oceans, between y 46 and sea level | 8 | 1 | 2–3 |
| Lobster | Beaches, Gravel Beach, Stony Shore | 7 | — | 3–5 |
| Mantis Shrimp | Hot oceans and Mangrove Swamp; must be over coral, mud or muddy mangrove roots, at or below sea level | 15 | — | 1–4 |
| Mimic Octopus | Hot oceans except Deep Warm Ocean | 9 | — | 1–2 |
| Mudskipper | Mangrove Swamp, Underground Jungle | 28 | — | 2–4 |
| Orca | Cold oceans, between y 46 and sea level | 2 | 6 | 3–4 |
| Platypus | Non-cold rivers, Tundra Bog, Warm River | 20 | — | 1–2 |
| Seal | Beaches, cold oceans, Gravel Beach, Dune Beach, Stony Shore | 20 | — | 3–8 |
| Skelewag | **Shipwrecks only** on this server — see below | 15 | — | 1–2 |
| Terrapin | Non-cold rivers, Tundra Bog, Warm River | 4 | — | 1–2 |
| Triops | Hot dry sandy biomes except badlands; Ancient Sands, Desert Canyon, Desert Oasis, Desert Spires, Sandstone Valley, Red Oasis | 8 | — | 2–6 |

Three spawn rules on this server are not biome-based at all:

- **`restrictPupfishSpawns = true`.** Pupfish spawn in exactly one chunk per world.
  At world load the server picks a random chunk within `pupfishChunkSpawnDistance`
  (**2000 blocks**) of `0, 0` whose water column tops out between y 31 and y 63, and
  logs `Found Pupfish chunk at <x> ~ <z>` to `latest.log`. If it cannot find one
  within five minutes it gives up and logs that no pupfish will spawn in the world.
  Their biome config is `minecraft:is_overworld`, which does nothing once the chunk
  restriction is on. The **Strange Fish Finder** points at that chunk.
- **`restrictSkelewagSpawns = true`.** Skelewags are added to the Shipwreck
  structure's monster spawn pool (1–2 per pack) and the deep-ocean biome entry is
  removed entirely. Each one is also tethered to a 15-block radius of where it spawned.
- **Beached cachalot whales** (`beachedCachalotWhales = true`) are their own spawner
  — see [Beached whales](#beached-whales).

## Drops

From `data/alexsmobs/loot_tables/entities/`. Ranges are before Looting unless a
Looting bonus is listed.

| Mob | Drops |
|---|---|
| Alligator Snapping Turtle | *(no loot table — shear it instead)* |
| Blobfish | `blobfish ×1`; `bone_meal ×1` at 5% |
| Cachalot Whale | *(no pools — its items come from code, see below)* |
| Caiman | *(loot table has no pools)* |
| Catfish (small) | `raw_catfish ×0–1`, +0–1 per Looting level |
| Catfish (medium) | `raw_catfish ×2–3`, +0–1 per Looting level |
| Catfish (large) | `raw_catfish ×4–6`, +0–1 per Looting level |
| Comb Jelly | `rainbow_jelly ×0–2`, +0–1 per Looting level |
| Crocodile | `crocodile_scute ×-1–2`, `crocodile_egg ×-2–1`, each +0–1 per Looting level |
| Devil's Hole Pupfish | *(loot table has no pools)* |
| Flying Fish | `flying_fish ×1`; `bone_meal ×1` at 5% |
| Frilled Shark | *(no pools — drops `serrated_shark_tooth` from code)* |
| Giant Squid | `ink_sac ×4–8` |
| Hammerhead Shark | *(no pools — drops `shark_tooth` from code)* |
| Lobster | `lobster_tail ×0–1`, +0–1 per Looting level |
| Mantis Shrimp | *(no loot table)* |
| Mimic Octopus | `ink_sac ×0–1`, +0–1 per Looting level |
| Mudskipper | `tropical_fish ×1` |
| Orca | *(loot table has no pools)* |
| Platypus | *(loot table has no pools)* |
| Sea Bear | *(loot table has no pools)* |
| Seal | *(loot table has no pools)* |
| Skelewag | `bone ×0–2` (+0–1 Looting); `fish_bones` at 30% (+20%/level); `skelewag_sword` at 10% (+5%/level); `novelty_hat` at 1% (+1.5%/level) |
| Terrapin | *(loot table has no pools)* |
| Triops | *(loot table has no pools)* |

Negative minimums in the crocodile table are the mod's way of writing "usually
nothing": a `-1 to 2` roll yields 0, 0, 1 or 2 with equal weight.

Drops handled in code rather than by loot table:

| Item | Source |
|---|---|
| `ambergris ×2–3` | A rescued beached Cachalot Whale swims up and gifts it. Once per whale. |
| `cachalot_whale_tooth ×1` | 10% chance each time a Cachalot Whale lands a charge attack. |
| `lost_tentacle ×1` | 20% chance when a Giant Squid breaks free of a whale's jaws. |
| `shark_tooth ×1` | 30% chance each time a Hammerhead Shark completes a strike. |
| `serrated_shark_tooth ×1` | 1-in-15 chance when a Frilled Shark bites a squid. |
| `spiked_scute` or `seagrass` | Shearing a mossy Alligator Snapping Turtle. |
| `fedora ×1` | Killing a Platypus that is wearing one. |
| Planks ×3, sticks ×2 | The boat a Cachalot Whale destroys. |

## The whale, the squid, and the deep ocean

### Cachalot Whale

160 health, 30 attack, full knockback immunity, and a nine-block-wide multipart
hitbox (`cachalot_part` ×6 — head, two body sections, three tail sections; damage to
any segment is forwarded to the whale). It heals 2 health every 10 seconds.

It has no player target goal. Its target tag `cachalot_whale_targets` is Mimic
Octopus, Giant Squid, vanilla Squid and Glow Squid — hit it, or attack one of those
in front of it, and it comes for you.

The attack is a **charge**. Before committing it echolocates: it fires
`cachalot_echo` projectiles at the target every half-second until one returns, then
lines up and rams. Contact deals its full attack damage and launches everything
inside the head hitbox. It skips echolocation entirely against players and against
anything not in water. Charge cooldown is 30 ticks against a player, 100 against
anything else.

- **Boats do not survive it.** A charge that connects with a boat's passenger
  destroys the boat outright and drops 3 planks and 2 sticks.
- **`cachalotDestruction = true`** on this server. While charging at a target the
  whale breaks planks, logs, wooden stairs, wooden slabs and wool, on top of the
  ice and lily pads it always breaks. Outside a charge it only breaks ice and lily
  pads, and it converts ice to water rather than dropping it.
- **`cachalotVolume = 3.0`** — three times the normal animal volume for its clicks.
  Config range is 0.0–10.0 if it becomes a complaint.
- It **sleeps vertically**, nose-up, between day-time 18000 and 22812 (late night),
  and floats to keep its blowhole clear. A sleeping whale does not despawn.
- **1 in 100 whales is albino**: 230 health, 45 attack, and it never despawns.
  Breeding an albino produces albino calves.

### Giant Squid

38 health, 8 attack, ten hitbox segments (`giant_squid_part`), heals 2 health every
5 seconds. It swims toward the deepest 60% of whatever water column it is in, so in
a deep ocean you will meet it near the floor.

- Within 7 blocks of a target with line of sight it **grabs**, dragging the victim
  along and dealing **3–7 damage per second** for up to 50 seconds.
- Hurting one has a 50% chance per hit to make it **release an ink cloud**.
- It actively **flees cachalot whales** it can see within 50 blocks, sprinting when
  the whale closes inside 20.
- Its small-prey target list (`giant_squid_targets`: blobfish, cod, salmon, tropical
  fish, catfish, flying fish, pupfish, triops) is gated on the squid *not* being in
  water, so in practice it never fires. What it does attack is anything that hurt it,
  and guardians within 20 blocks.

### The whale–squid fight

A cachalot whale that connects a charge on an adult giant squid does not damage it —
it **takes it in its jaws**. Held in the mouth the squid takes 4–7 damage per second.
Every tick of capture the squid has a 1-in-13 chance to ink and bite back for 4–7,
and each of those bites has a 30% chance to break the hold. **20% of successful
escapes drop a Lost Tentacle**, which is the only source of the item and the
ingredient for the Squid Grapple. If the squid never breaks free the whale releases
it after 15 seconds anyway. Baby whales do not grab.

### Beached whales

`beachedCachalotWhales = true`, and this is a scheduled event rather than a spawn
table entry. Every 60 seconds **during a thunderstorm** the spawner decrements a
`beachedCachalotWhaleSpawnDelay` counter (24000 ticks, one full day). When it hits
zero it rolls against an accumulating chance that starts at 25% and rises by
`beachedCachalotWhaleSpawnChance` (**5**) per failed attempt, clamped to 5–100. On a
success there is a further 1-in-5 chance to actually place the whale, on a beach
biome (`is_beach`, Gravel Beach, Dune Beach, Stony Shore) 15–84 blocks from a random
player.

The stranded whale is tethered to 16 blocks and **despawns after 47999 ticks (about
40 minutes)**. Get water over its eyes — dig a channel, place water, or push it —
and it un-beaches, clears its despawn timer, swims to the nearest player within 50
blocks and drops **2–3 Ambergris**. It will not reward the player who last hurt it,
and it only pays out once.

## Sharks and predators

### Hammerhead Shark

30 health, 5 attack, movement speed 0.5 — the fastest thing in a hot ocean. It
targets **any living entity at half health or below within 50 blocks**, including
players, plus squid, mimic octopus and schooling fish. Uninjured players are ignored.

Its combat loop is a circle: it orbits the target at 5–10 blocks for **360–440 ticks
(18–22 seconds)** before closing and striking. Each completed strike has a **30%
chance to drop a Shark Tooth** on the spot, whether or not the shark ever dies.
Six Shark Tooth Arrows are crafted from one tooth, a stick and kelp; they deal a
flat **7 extra damage** on hit and chew through shields.

It avoids Guardians at 8 blocks.

### Frilled Shark

20 health, 3 attack, deep ocean only. It does not target players — its list is squid,
mimic octopus, schooling fish, blobfish and drowned. It takes **half damage from
drowned**.

The bite applies **Exsanguination III for 3 seconds**, which deals magic damage each
second equal to the lower of (amplifier + 1) and the seconds remaining — 3, then 2,
then 1, so **6 total** on top of the bite. Biting a squid has a 1-in-15 chance to
drop a Serrated Shark Tooth.

Out of pressure — fewer than 10 blocks of water above it — it enters a
**depressurised** state and visibly bloats. It is bucketable.

### Orca

60 health, 10 attack, 70% knockback resistance, follow range 64. Its target tag
`orca_targets` is Moose, Seal, Polar Bear, Turtle, Drowned, Guardian and Elder
Guardian, plus baby cachalot whales within 25 blocks. It does **not** target players
unprovoked. Damage against Drowned and Guardians is **doubled** (20).

- Two attacks: a **bite**, and a **tail swing** that adds hard knockback plus an
  upward launch. It picks between them at random while in water.
- It **jumps out of the water** to hit targets, and breaks ice and lily pads it
  swims through — ice becomes water rather than dropping.
- **Swim near one and it grants Orca's Might** (`alexsmobs:orcas_might`), 50 seconds,
  refreshed while you keep swimming: **+3 attack speed**, which on a normal weapon
  removes the swing cooldown entirely. Attacking that orca strips the effect
  immediately.
- Four cosmetic variants, picked from which world quadrant the orca spawned in.
- Breed with **salmon**. Not tameable despite extending `TamableAnimal`.

### Skelewag

20 health, 3 attack, speed 0.45. Hostile: it targets players and dolphins on sight
and never suffocates. On this server it spawns **only inside shipwrecks**, tethered
to 15 blocks of its spawn point.

- **20% of skelewags spawn carrying a Drowned rider.**
- 30% spawn with the alternate texture variant.
- Two attacks: a **stab** (full damage plus knockback, used after charging in from
  more than 5 blocks) and a **slash** that hits everything within 2 blocks of the
  target for **half damage, once every 5 ticks across the 25-tick animation** — five
  hits if you stay in the arc.
- The **Skelewag Skull** it drops (10%, +5% per Looting level) is an iron-tier sword
  with **+3.5 attack damage and no attack-speed penalty** — it swings at the bare-hand
  rate of 4.0/s — 430 durability, and it can be raised to block like a shield.
- The **Novelty Hat** (1%, +1.5% per Looting level) is a helmet with 2 armour.

### Sea Bear

200 health, 8 attack, and it is **not obtainable through any spawn table**. The
spawner is an April Fools' hook: on **1 April** (real-world date; the
`superSecretSettings` override is `false` here), any swimming entity wearing a
**Sombrero** rolls a 1-in-245 chance per tick to have a sea bear spawn 10–32 blocks
away and charge it. Its only target predicate is "wearing a sombrero".

Standing on an **Anti-Sea Bear Circle** (`sand_circle` / `red_sand_circle`) makes you
untargetable — the bear stops, points at you, and backs off for 100–200 ticks.
Otherwise it closes to 3.5 blocks and deals **6 damage on every fifth tick of its
attack animation**.

## Tameable and rideable

Nothing in this doc is rideable. Six are tameable, by three different routes.

| Mob | How | Commands |
|---|---|---|
| Mimic Octopus | Feed **Lobster Tail** (raw or cooked) repeatedly. After 5 feedings each one has a 50% chance to tame; guaranteed at 9. Must be in its default state. | Wander / follow / stay |
| Mantis Shrimp | Feed **Tropical Fish** repeatedly. After 10 feedings each one has a 1-in-6 chance; guaranteed at 31. | Wander / follow / stay / break blocks |
| Mudskipper | Feed **Lobster Tail** — 50% per feeding. | Wander / follow / stay |
| Caiman | **Hatch a caiman egg** within 20 blocks of you. The hatchling is tame and ordered to sit. Wild caimans cannot be tamed. | Wander / follow / stay |
| Crocodile | **Hatch a crocodile egg** within 20 blocks of you. Same rule. | Wander / follow / stay |

Reptile eggs only hatch on sand (or a block in `crocodile_spawns`), and hatch through
three stages on random ticks. Crocodile eggs drop from crocodiles and are also sold
by wandering traders (`wanderingTraderOffers = true`).

Breeding, for everything that breeds:

| Mob | Breeding item |
|---|---|
| Alligator Snapping Turtle | Cod |
| Caiman | Raw or Cooked Catfish |
| Cachalot Whale | **Not documented.** It has a `BreedGoal` but no `isFood` override and no tempt goal, so the breeding item is whatever vanilla `Animal` defaults to rather than anything the mod specifies. |
| Crocodile | Rotten Flesh |
| Mantis Shrimp | Lobster Tail (raw or cooked), tamed only |
| Mimic Octopus | Tropical Fish, tamed only |
| Mudskipper | Insect items, Lobster Tail (raw or cooked) |
| Orca | Salmon |
| Platypus | Lobster Tail |
| Seal | Lobster Tail (raw or cooked) |
| Terrapin | Seagrass |
| Devil's Hole Pupfish | Not fed — see below |
| Triops | Carrot, then a mate |

## Individual mechanics

### Mimic Octopus

16 health, 2 attack, passive, and the most mechanically dense mob here. It changes
appearance to match its surroundings, taking a **90% visibility penalty** to mobs
looking for it while camouflaged against a block.

Tame it with lobster tails. Once tamed:

| Give it | Effect |
|---|---|
| Gunpowder or a Creeper Head | Mimic a **creeper** |
| Prismarine Shard or Crystals | Mimic a **guardian** |
| Pufferfish or a Pufferfish Bucket | Mimic a **pufferfish** |
| Ink Sac | Toggle mimicry off / on |
| Slime Ball | Refill its moisture to full |
| Lobster Tail | Heal 5 |
| **Mimicream** | **Permanent upgrade** — 5 feedings, or 3 with a coin flip |

A forced disguise holds for 1200 ticks (60 s) normally, 120 ticks once upgraded.

Unupgraded, disguises are pure bluff: it scares mobs off but deals no damage.
**Upgraded**, the disguise fights:

- **Pufferfish** — 4 damage plus **Poison III for 20 seconds** to anything within
  about 2 blocks.
- **Guardian** — a beam at targets within 7 blocks, 1 damage on contact.
- **Creeper** — a real explosion (power 1–2, no block damage), 300-tick cooldown.

It flees Drowned, Dolphins, Orcas, Hammerhead Sharks, Mantis Shrimp, Cachalot Whales,
Frilled Sharks, Catfish and Caimans. It can hold one item in its main hand
(shift-click) and is bucketable once tamed.

### Mantis Shrimp

20 health, 8 armour, 3 attack. Neutral — it hunts `mantis_shrimp_targets`: Mimic
Octopus, Lobster, **Shulker**, Squid, Guardian, Elder Guardian, Tropical Fish,
Catfish, Flying Fish and Triops.

Its attack is a **punch**: full attack damage, 1.7 knockback with an upward
component, and if the target is out of water it is **set on fire for 2 seconds**.

The shulker interaction is the reason to keep one:

- Damage dealt to a mantis shrimp **by a shulker or shulker bullet is reduced to
  `(amount + 1) × 0.33`** — a 4-damage bullet becomes 1.65.
- A shulker **killed by a mantis shrimp always drops a Shulker Shell**, and its normal
  loot table is voided so it drops nothing else.

Untamed shrimp that kill vanilla fish void that fish's loot table. Four colour
variants; Mangrove Swamp always produces the white one, and mangrove spawns are
additionally culled by 50%. It can hold an item, and hands over items in
`shrimp_rice_fryables` (`forge:crops/rice`) without needing a shift-click.

### Catfish

Three sizes, rolled at spawn: **35% medium**, otherwise small; then a separate 10%
roll upgrades it to **large** if the biome is a swamp. Size sets health (10 / 20 / 30),
hitbox, and which loot table it uses.

- **Small and medium catfish swallow item entities** that have been on the ground
  more than 35 ticks, into an internal inventory of **3 slots (small) or 9 slots
  (medium)**. Killing the fish drops everything it holds.
- **Large catfish swallow live mobs** — anything 1.0 blocks tall or shorter that is
  not another catfish. The mob is stored whole and released later at **25% of its max
  health**. Players are never eligible.
- **Right-click any catfish with a Sea Pickle** and it spits: an item back out for
  small and medium, the swallowed mob for large. A large catfish also spits its
  captive on death.
- They are drawn to **Sea Lanterns**, both as a placed block and as a dropped item.
- Bucketable, one bucket item per size. Raw Catfish is 2 hunger, Cooked is 5.

### Devil's Hole Pupfish

2 health, the smallest mob in this doc, and confined to a single chunk per world.

- It grazes **moss blocks, moss carpet, mossy cobblestone and mossy stone bricks**.
  Each completed feeding has a **1-in-3 chance to drop a Slime Ball** and a separate
  1-in-3 chance to make the fish ready to breed.
- Breeding is a **chase**: a ready pupfish pairs off with another ready pupfish and
  they circle each other rather than being fed an item.
- The **Strange Fish Finder** (`pupfish_locator`, 200 durability) points at the
  pupfish chunk from anywhere.

### Seal

10 health, herd animal, flees Orcas at 20 blocks. **`polarBearsAttackSeals = true`**,
so polar bears hunt them. Hurting one panics every seal within 15 blocks for 100–250
ticks.

**Throw a fish at a seal** (anything in `minecraft:fishes`) and it dives, digs into
the seabed and brings something back from its own loot table:

| Reward | Chance |
|---|---|
| Sand ×1–10 | 19.4% |
| Kelp ×2–4 | 19.4% |
| Gravel ×8–16 | 12.9% |
| Shark Tooth | 6.8% |
| Clay Ball ×5–32 | 6.5% |
| Wet Sponge ×1–2 | 6.5% |
| Ink Sac | 6.1% |
| Potion | 3.2% |
| Prismarine Crystals | 3.2% |
| Serrated Shark Tooth | 2.6% |
| Prismarine Shard ×2–5 | 2.6% |
| Fish Bones | 1.9% |
| Vanilla fishing junk | 1.3% |
| Coral (5 kinds) | 0.6% each |
| Bucket of Lobster | 0.6% |
| Music Disc "Thime" | 0.6% |
| Scute | 0.6% |
| Coral blocks (5 kinds) | 0.3% each |
| Turtle Egg | 0.6% (two entries) |
| **Nautilus Shell** | **0.3%** |

It digs in sand, gravel, grass, dirt and clay. Cold biomes produce the white variant.

### Platypus

10 health, passive, but **anything that hits it in melee takes Poison for 5 seconds**.

Right-click it with **Redstone or a Redstone Block** and it charges up and starts
digging for items:

| Fed | Result |
|---|---|
| Redstone | Clay Ball 74%, Maggot 26% |
| Redstone Block | Clay Ball ×1–2 65%, Maggot 32%, **Fedora 3.2%** |

Give a platypus the Fedora back and it wears it; killing a hatted platypus drops it.
Bucketable. Breeds on Lobster Tail. Lays eggs.

### Terrapin

10 health, 10 armour, speed 0.1 — the Koopa shell.

- **Jump on a terrapin on land** and it retreats into its shell for 2–4 seconds.
- **Jump on a retreated terrapin** and it **launches as a spinning shell** in the
  direction you are facing for **5–10 seconds**, dealing **4–8 damage** to everything
  it touches (credited to you) and ricocheting off walls.

Seven cosmetic variants including a Koopa skin, with the shell, skin and colour
inherited independently through the egg block. Breeds on Seagrass. Bucketable.
Shoebills hunt them.

### Alligator Snapping Turtle

18 health, 8 armour, 4 attack, 70% knockback resistance. An **ambush predator**: with
no target and in water it sits motionless with its mouth open, and its target search
box is **its own hitbox inflated by 0.5 horizontally and 2 vertically** — it attacks
anything, player included, that swims into its mouth, and nothing that does not. If a
chase runs more than 40 ticks and the target is more than 5 blocks away (10 for
non-players), it gives up and forgets you.

It grows moss while in water: **+1 level every 12000 ticks (10 minutes), capped at
10**. **Shear it** and you get either a **Spiked Scute** — chance equals moss level
× 5%, so 50% at full moss — or Seagrass. Shearing resets moss to zero.

It climbs walls while underwater. Breeds on Cod. No loot table at all: killing one
drops nothing.

### Crocodile and Caiman

The **Crocodile** (30 health, 10 attack, 8 armour) hunts players and everything in
`crocodile_targets` — passive land animals, villagers, kangaroos, gelada monkeys,
catfish, caimans and triops.

- Its **lunge** deals 10 damage. If the target is narrower than the crocodile, is not
  sneaking, and it has no victim already, the target is **grabbed** instead — forced
  to ride the crocodile, taking **2 damage every 2 seconds**.
- In water, a grabbed victim triggers a **death roll**: **5 damage every 10 ticks**
  for as long as the hold lasts.
- **Sneaking prevents the grab.** **Blocking with a shield** stops the bite, damages
  the shield for 10, and **stuns the crocodile for 25–44 ticks**.
- Desert crocodiles are a separate texture set on spawn, from `spawns_desert_crocodiles`.

The **Caiman** (20 health, 3 attack, 8 armour) is the small version, and is neutral.
It hunts `caiman_targets` — chickens, rabbits, frogs, parrots, crows, toucans, blue
jays, jerboas, sugar gliders, banana slugs, terrapins, triops, catfish, flying fish,
rain frogs, tropical fish, cod and salmon. Untamed caimans that kill water animals
**void that animal's loot table**. It bellows in water as a display. Tame it only by
hatching an egg; feed a tame one anything in `minecraft:fishes` to heal 5.

### Mudskipper

12 health, 2 attack, equally at home on mud and in water. Its ranged attack is a
**mud ball** at targets within 8 blocks, on a 10–20 tick cooldown, applying
**Slowness for 3 seconds**; below about 3 blocks it bites instead. Tame it with
lobster tails (50% per feeding), heal it with insect items. Bucketable.

### Lobster

5 health, 2 armour, 2 attack, pinches back when hurt. Six colours with sharply
different odds:

| Variant | Chance |
|---|---|
| Red | 75% |
| Blue | 15% |
| Yellow | 5% |
| Red and Blue | ~5% |
| **Black** | **0.001%** |
| **White** | **0.001%** |

Lobster Tail is 2 hunger raw, 6 cooked, and is the breeding or taming item for
Mimic Octopus, Mantis Shrimp, Mudskipper, Platypus and Seal. Bucketable, and the
bucket keeps the colour.

### Comb Jelly

6 health, three colours (blue, green, red), a random size between 0.8× and 1.2×, and
a night-only, dark-only spawn. Drops **0–2 Rainbow Jelly**.

**Rainbow Jelly permanently recolours any living entity** it is used on — right-click
a mob, or eat it yourself. Renaming the item selects which rainbow pattern is applied.
A **Sponge** used on a rainbow-coloured entity removes the effect. Bucketable; the
bucket preserves both colour and size.

### Blobfish

8 health, deep ocean at y 25 or below. Out of water it suffocates — **unless you
right-click it with a Slime Ball**, which "slimes" it permanently: it stops taking
suffocation damage on land and never despawns. The Blobfish item is 3 hunger but
carries **Poison for 6 seconds, guaranteed**. 5% of kills also drop Bone Meal.

### Flying Fish

6 health, temperate open ocean, in schools of 3–6 that share a colour. It glides out
of the water in bursts; hurting one makes every flying fish within 15 blocks glide
immediately. **`dolphinsAttackFlyingFish = true`** and seals hunt them at 55 blocks.

Four Flying Fish plus two String make **Flying Fish Boots**, which let you glide by
jumping out of water. The fish item is 3 hunger.

### Triops

4 health, desert water. It picks up and eats dropped food.

- Feed it a **Carrot** (or anything in `forge:crops/carrot`) and it becomes ready to
  breed.
- Two ready triops **pair off on their own** within 10 blocks and one becomes
  pregnant; she then lays a **Triops Eggs** block on the seabed. Breeding cooldown
  afterwards is **1200–4800 ticks (1–4 minutes)**.

Bucketable.

## Aquatic systems

### Fish buckets

Fourteen aquatic mobs here are `Bucketable` — right-click with a water bucket to
capture one, and the bucket item stores its full state. All use
`ItemModFishBucket` with `Fluids.WATER`, so placing one also places a water source.

| Bucket item | Preserves |
|---|---|
| `blobfish_bucket` | slimed flag, custom name |
| `comb_jelly_bucket` | colour variant, size |
| `devils_hole_pupfish_bucket` | custom name |
| `flying_fish_bucket` | colour variant |
| `frilled_shark_bucket` | depressurised flag |
| `lobster_bucket` | colour variant |
| `mimic_octopus_bucket` | tame state and owner (tamed only) |
| `mudskipper_bucket` | tame state and owner |
| `platypus_bucket` | fedora, charge state |
| `small_catfish_bucket` / `medium_catfish_bucket` / `large_catfish_bucket` | size, inventory contents |
| `terrapin_bucket` | all seven variant fields |
| `triops_bucket` | breed state |

A bucketed mob has `FromBucket` set, which makes it **persistent** — it will never
despawn once released.

### Items from aquatic mobs

| Item | Source | What it does |
|---|---|---|
| **Ambergris** | Rescued beached whale, 2–3 | Furnace fuel, **12800 ticks** — 20 smelting operations' worth of burn time from one item |
| **Cachalot Whale Tooth** | 10% per whale charge | Crafting only |
| **Echolocator** | 2 whale teeth + 1 Ambergris + 4 iron | 100 uses; pings the nearest cave air pocket within range |
| **Strange Fish Finder** | `pupfish_locator` | 200 uses; points at the world's one pupfish chunk |
| **Lost Tentacle** | 20% when a squid escapes a whale | Crafting; repairs the Squid Grapple |
| **Squid Grapple** | 3 Lost Tentacle + crossbow + 3 copper | Bow-draw grappling hook; power scales with draw time |
| **Shark Tooth** | 30% per hammerhead strike | 1 tooth + stick + kelp → **6 Shark Tooth Arrows**, +7 damage on hit, damages shields |
| **Serrated Shark Tooth** | Frilled shark biting a squid | Crafting |
| **Skelewag Skull** | 10% skelewag drop | Iron-tier sword, +3.5 damage, no swing cooldown, 430 durability, blocks like a shield |
| **Novelty Hat** | 1% skelewag drop | Helmet, 2 armour |
| **Fish Bones** | 30% skelewag drop, 1.9% seal reward | Crafts into Bone Meal |
| **Rainbow Jelly** | Comb Jelly, 0–2 | Permanently recolours a mob; removed with a Sponge |
| **Lobster Tail** | Lobster, 0–1 | 2 hunger raw / 6 cooked; the universal aquatic-taming food |
| **Raw / Cooked Catfish** | Catfish, 0–6 by size | 2 / 5 hunger |
| **Blobfish** | Blobfish, 1 | 3 hunger + guaranteed Poison 6 s |
| **Flying Fish** | Flying Fish, 1 | 3 hunger; 4 + string → Flying Fish Boots |
| **Spiked Scute** | Shearing a mossy snapping turtle | Crafting |
| **Crocodile Scute** | Crocodile | Crocodile armour |
| **Sombrero** | — | Helmet, 2 armour; **wearing it in water on 1 April summons a Sea Bear** |
| **Anti-Sea Bear Circle** | — | Standing on it makes a Sea Bear unable to target you |

### Status effects from aquatic mobs

| Effect | ID | Source | What it does |
|---|---|---|---|
| Exsanguination | `alexsmobs:exsanguination` | Frilled Shark bite (level III, 3 s) | Magic damage each second equal to min(level, seconds left) |
| Orca's Might | `alexsmobs:orcas_might` | Swimming near an Orca (50 s) | +3 attack speed |
| Poison | vanilla | Platypus retaliation (5 s); upgraded Mimic Octopus pufferfish form (III, 20 s); eating a Blobfish (6 s) | — |
| Slowness | vanilla | Mudskipper mud ball (3 s) | — |

### Config knobs that change aquatic behaviour

Values below are what the live server runs, from `/config/alexsmobs.toml`.

| Option | Value | Effect |
|---|---|---|
| `cachalotDestruction` | `true` | Angry whales break wood and wool, not just ice |
| `cachalotVolume` | `3.0` | Whale click volume, relative to other animals |
| `beachedCachalotWhales` | `true` | Beached whale event enabled |
| `beachedCachalotWhaleSpawnDelay` | `24000` | One in-game day between attempts |
| `beachedCachalotWhaleSpawnChance` | `5` | Percent added per failed attempt |
| `blobfishSpawnHeight` | `25` | Maximum y for blobfish |
| `restrictPupfishSpawns` | `true` | Pupfish confined to one chunk |
| `pupfishChunkSpawnDistance` | `2000` | Radius from 0,0 for that chunk |
| `restrictSkelewagSpawns` | `true` | Skelewags only at shipwrecks |
| `polarBearsAttackSeals` | `true` | — |
| `dolphinsAttackFlyingFish` | `true` | — |
| `superSecretSettings` | `false` | Sea Bears only spawn on the real 1 April |
