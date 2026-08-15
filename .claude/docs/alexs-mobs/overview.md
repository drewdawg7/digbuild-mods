<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Overview

**Alex's Mobs** adds 91 living creatures to the existing Overworld, Nether and
End, spread across the vanilla biome list rather than into new dimensions or
biomes of its own. Most of them are ambient fauna with one mechanic attached —
a drop, a taming path, a mount, a tool ingredient — and the mod's own
progression is the **Animal Dictionary**, a book carrying an entry per species.
Nothing in it is locked — every entry is readable from the start — and the 106
advancements hanging off it are a checklist rather than a gate.

## Versions on this server

| Mod | ID | Version | Jar | Role |
|---|---|---|---|---|
| Alex's Mobs | `alexsmobs` | 1.22.9 | `alexsmobs-1.22.9.jar` | the mod |
| Citadel | `citadel` | 2.6.3 | `citadel-2.6.3-1.20.1.jar` | **required** library (same author) |
| Alex's Delight | `alexsdelight` | 1.5 | `alexsdelight-1.5.jar` | add-on (Farmer's Delight bridge) |
| RAM-Compat | `ramcompat` | 0.1.4 | `ramcompat-1.20.1-0.1.4.jar` | add-on (Relics bridge) |

Authors: Alexthe668, Carro1001, Paint_Ninja. License: GNU Lesser General Public
License. Issue tracker: <https://github.com/Alex-the-666/AlexsMobs/issues>.

## Dependency graph

```
alexsmobs 1.22.9
├── citadel  >= 2.6.0   (mandatory, both sides)   ✓ 2.6.3 installed
└── forge    >= 47.1.0  (mandatory, both sides)   ✓ 47.4.10 installed

alexsdelight 1.5
├── forge      >= 47      (mandatory)             ✓
└── minecraft  [1.20.1]   (mandatory)             ✓
    (declares no hard dependency on alexsmobs or farmersdelight —
     both are present anyway: farmersdelight 1.3.2)

ramcompat 0.1.4
├── minecraft  [1.20.1, 1.21)                     ✓
├── forge      >= 47                              ✓
├── curios     >= 5.2.0+1.20.1                    ✓ 5.14.1+1.20.1 installed
├── octolib    >= 0.1                             ✓ 0.5.0.1+1.20.1 installed
└── relics     >= 0.6.5                           ✓ 0.8.0.13 installed
    (declares no hard dependency on alexsmobs)
```

All declared ranges are satisfied by what is currently installed.

`alexsmobs` declares Citadel on side `BOTH` and ships client-side rendering
code, so it is required on the client as well as the server.

## Install state on this server

| | |
|---|---|
| Main config | `/config/alexsmobs.toml` — 711 lines, 431 assignments |
| Per-mob spawn configs | `/config/alexsmobs/` — 90 JSON files |
| Add-on configs | none observed |

The 90 files in `/config/alexsmobs/` are 86 named `<mob>_spawns.json` plus four
bare ones — `farseer.json`, `murmur.json`, `skreecher.json`, `underminer.json`.
Each is a biome allow/deny list built from `BIOME_TAG` and `REGISTRY_NAME`
clauses. They are **live, edited config, not defaults**: several of them name
Terralith biomes (`terralith:amethyst_rainforest`, `terralith:rocky_jungle`,
`terralith:skylands_summer`, …), which the mod's shipped defaults do not.
See [spawning.md](spawning.md) and [config.md](config.md).

Notable in the jar rather than the config:

- **12 blocks ship unregistered.** `end_pirate_anchor`, `end_pirate_anchor_winch`,
  `end_pirate_door`, `end_pirate_trapdoor`, `end_pirate_flag`,
  `end_pirate_ship_wheel`, `phantom_sail`, `spectre_sail`, `purpur_planks` and
  its slab/stairs/wall have lang entries, blockstates, models and (for most)
  `Block…` classes in the jar, but no entry in `AMBlockRegistry`. Verified by
  reading the constant pool of `AMBlockRegistry.class` directly — none of the 12
  names appear. They do not exist in-game.
- **One item has a broken translation key.** `alexsmobs:stink_ray_empty_inventory`
  is registered, but the lang file only carries `item.alexsmobs.stink_empty_inventory`.
  That item renders as a raw key.
- **Three entity ids are lang-only leftovers** — `cachalot_part`,
  `giant_squid_part` and `crocodile_egg` have `entity.alexsmobs.*` names but no
  registered entity type. (`block.alexsmobs.crocodile_egg` is a separate, real
  block.)
- **Two registered entity types have no display name** — `emu_egg` and
  `ice_shard`. Both are projectiles that are never named in a UI.
- **`data/domesticationinnovation/` tags ship in the jar** (five
  `petstore_cage_*` / `petstore_fishtank` entity tags). Domestication Innovation
  is not installed on this server, so they are inert.

## Census

Counted from the jar. Method is given per row, because the lang file and the
registries disagree in a few places and the registry is the authority.

| | Count | Counted from |
|---|---:|---|
| Entity types | **116** | `DEF_REG.register("…")` literals in `entity/AMEntityRegistry.java` |
| — of which living mobs | 91 | the above, `MobCategory` ≠ `MISC`, minus multipart segments |
| — of which projectiles | 17 | `MobCategory.MISC` extending `Entity`/`Arrow`/`ThrowableItemProjectile` |
| — of which body segments | 6 | ids ending `_part`, plus `centipede_body`/`centipede_tail`/`tendon_segment` |
| — of which vehicles | 1 | `straddleboard` (`PlayerRideableJumping`) |
| Items | **254** | 240 literal `DEF_REG.register` calls in `item/AMItemRegistry.java`, less 2 loop prefixes, plus the 5 banner patterns and 11 `dimensional_carver_shard_*` they expand to |
| Blocks | **25** | `RegistryObject<Block>` fields in `block/AMBlockRegistry.java` (37 `block.alexsmobs.*` lang keys — see the 12 unregistered above) |
| Block entities | 6 | `.register("…")` in `tileentity/AMTileEntityRegistry.java` |
| Status effects | **19** | `EFFECT_DEF_REG.register` in `effect/AMEffectRegistry.java` |
| Potions | 15 | `POTION_DEF_REG.register` in the same file |
| Enchantments | **4** | `enchantment/AMEnchantmentRegistry.java`, all four Straddleboard-only |
| Damage types | 2 | `data/alexsmobs/damage_type/` (`farseer`, `freddy`) |
| Advancements | 106 | files under `data/alexsmobs/advancements/` (212 lang keys = 106 title/description pairs) |
| Loot tables | 139 | `data/alexsmobs/loot_tables/` — 104 entity, 25 block, 10 gameplay |
| Global loot modifiers | 4 | `data/alexsmobs/loot_modifiers/` — banana, blossom, ancient dart, pigshoes |
| Recipes | 84 | `data/alexsmobs/recipes/` |
| Capsid recipes | 4 | `data/alexsmobs/capsid_recipes/` |
| Tags | 223 | `data/alexsmobs/tags/` — 125 item, 54 block, 29 entity type, 10 worldgen, 5 banner pattern |
| Worldgen features | 1 | `leafcutter_anthill` (configured + placed) |
| Paintings | 2 | `misc/AMPaintingRegistry.java` |
| Banner patterns | 5 | `misc/AMBannerRegistry.java` |
| Points of interest | 4 | `misc/AMPointOfInterestRegistry.java` |
| Sound events | 212 | `alexsmobs.sound.*` keys in `assets/alexsmobs/lang/en_us.json` |
| Creative tabs | 1 | `itemGroup.alexsmobs` |

## Content pillars

| Pillar | One line | Covered in |
|---|---|---|
| Surface fauna | 52 `CREATURE` mobs spread across the vanilla Overworld biome list, most with a single drop or interaction hook | [mobs-land.md](mobs-land.md) |
| Aquatic fauna | 17 `WATER_CREATURE`/`WATER_AMBIENT` mobs from Lobster up to Cachalot Whale and Giant Squid, plus a beached-whale spawner | [mobs-aquatic.md](mobs-aquatic.md) |
| Ambient swarms | 7 `AMBIENT` mobs (Fly, Cockroach, Flutter, Jerboa, Rain Frog, Cosmic Cod, Underminer) that exist as background density | [mobs-land.md](mobs-land.md), [mobs-aquatic.md](mobs-aquatic.md) |
| Nether and End fauna | Warped Mosco, Warped Toad, Soul Vulture, Bone Serpent, Straddler/Stradpole, Laviathan, Mungus, Endergrade, Enderiophage, Cosmaw, Mimicube, Void Worm, Farseer | [mobs-nether-end.md](mobs-nether-end.md) |
| Multipart bosses | Void Worm, Bone Serpent, Anaconda, Cave Centipede and Murmur are each two or more entity types — a head plus `IHurtableMultipart` segments | [mobs-nether-end.md](mobs-nether-end.md), [mobs-land.md](mobs-land.md) |
| Tameable mounts and pets | Gorilla, Elephant, Grizzly Bear, Crocodile, Tiger, Capuchin Monkey, Raccoon, Snow Leopard and others take a food-and-trust or throw-a-banana path; three command states (`wandering`/`following`/`staying`) are shared across all of them | [taming-and-progression.md](taming-and-progression.md) |
| Animal Dictionary | `alexsmobs:animal_dictionary`, handed to every player on first join by default (`giveBookOnStartup = true`); the 106 advancements are the progression ladder behind it | [taming-and-progression.md](taming-and-progression.md) |
| Transmutation Table | Block + `TileEntityTransmutationTable`, spends experience to convert items, with per-item weights tracked in `TransmutationData` so repeated conversions get more expensive | [items-blocks.md](items-blocks.md) |
| Capsid | Block + `TileEntityCapsid`; four data-driven `capsid_recipes` (`cosmic_cod`, `mysterious_worm`, `music_disc_daze`, `shattered_dimensional_carver`) | [items-blocks.md](items-blocks.md) |
| Straddleboard | The mod's one vehicle, and the only thing its 4 enchantments apply to — Straddle Jump, Lavawaxed, Serpent Charmer, Returning Board | [effects-and-enchantments.md](effects-and-enchantments.md), [items-blocks.md](items-blocks.md) |
| Status effects and potions | 19 effects and 15 brewable potions, including three that overwrite vanilla potion names (`speed_iii`, and the long/strong variants) | [effects-and-enchantments.md](effects-and-enchantments.md) |
| Drops and global loot | 104 entity loot tables plus 4 global loot modifiers that inject bananas into leaves, blossoms, ancient darts and pigshoes | [loot-and-drops.md](loot-and-drops.md) |
| Spawn control | Per-mob JSON biome lists in `/config/alexsmobs/`, applied through Forge biome and structure modifiers, on top of `…SpawnRolls` gates in the TOML | [spawning.md](spawning.md), [config.md](config.md) |

## Interaction with other mods on this server

| Mod | Interaction |
|---|---|
| **Citadel** 2.6.3 | Hard dependency. Supplies the animation system (`IAnimatedEntity`, `AnimationHandler`) every animated Alex's Mobs entity uses. Shared with Alex's Caves. |
| **Alex's Delight** 1.5 | Add-on by NCP Bails. Bridges Alex's Mobs drops into Farmer's Delight cooking. See [addons.md](addons.md). |
| **RAM-Compat** 0.1.4 | Add-on by SSKirillSS. Bridges Alex's Mobs into Relics via Curios. See [addons.md](addons.md). |
| **Farmer's Delight** 1.3.2 | Alex's Delight's other parent. |
| **Relics** 0.8.0.13, **Curios** 5.14.1, **OctoLib** 0.5.0.1 | RAM-Compat's other parents. |
| **Terralith** | Not a code dependency, but this server's spawn JSONs name Terralith biomes explicitly, so Alex's Mobs spawning is tuned around it. |
| **JEI** 15.20.0.112 | The only compat class in the jar is `compat/jei`. |
| **Alex's Caves** 2.0.2 | Same author, same Citadel dependency, no direct code link. |

Cross-mod tags the jar ships that this server can act on: `forge:fruits/banana`
and `forge:crops/banana` (Alex's Mobs is the banana provider for the pack),
`forge:crops/rice`, `forge:eggs`, `forge:heart`, and armour/tool tags.

## Reading the decompiled source

`alexsmobs-1.22.9.jar` was decompiled with **jadx 1.5.4**, which leaves SRG
names in place. Attributes appear as `Attributes.f_22276_` rather than
`Attributes.MAX_HEALTH`. The mapping used throughout these docs was verified by
diffing two decompiled `bakeAttributes()` bodies against the same methods in the
clean upstream source (`AlexModGuy/AlexsMobs`, branch `1.20`), where the
argument order is identical and the names are readable:

| SRG field | Attribute | Verified against |
|---|---|---|
| `f_22276_` | `MAX_HEALTH` | Gorilla 30, Rhinoceros 60 |
| `f_22277_` | `FOLLOW_RANGE` | Gorilla 32, Rhinoceros 32 |
| `f_22278_` | `KNOCKBACK_RESISTANCE` | Gorilla 0.5, Rhinoceros 0.9 |
| `f_22279_` | `MOVEMENT_SPEED` | Gorilla 0.25, Rhinoceros 0.25 |
| `f_22280_` | `FLYING_SPEED` | not directly verified — inferred from position in the vanilla field order; used only by Hummingbird, Flutter and Farseer |
| `f_22281_` | `ATTACK_DAMAGE` | Gorilla 7, Rhinoceros 8 |
| `f_22282_` | `ATTACK_KNOCKBACK` | Rhinoceros 2 |
| `f_22283_` | `ATTACK_SPEED` | `EffectOrcaMight` adds +3, matching "grants increased attack speed" |
| `f_22284_` | `ARMOR` | Gorilla 0, Rhinoceros 12 |
| `f_22285_` | `ARMOR_TOUGHNESS` | Rhinoceros 4 |
| `f_22286_` | `LUCK` | never used by this mod |

The mapping given in the task brief holds. The one field this could not confirm
from a same-method diff is `f_22280_` (`FLYING_SPEED`), because no mob that uses
it also appears with a clean-source counterpart that was checked.

## Full entity roster

All 116 registered entity types. The category column is the `MobCategory` passed
to `EntityType.Builder.of(…)`, collapsed to one word:
`CREATURE` → creature, `MONSTER` → monster, `WATER_CREATURE`/`WATER_AMBIENT` →
aquatic, `AMBIENT` → ambient, and `MISC` split by superclass into projectile,
segment, vehicle or misc. Display names are `entity.alexsmobs.<id>` from
`assets/alexsmobs/lang/en_us.json`.

Note that a few display names collide by design — `anaconda` and
`anaconda_part` are both "Anaconda", `murmur` and `murmur_head` are both
"Murmur", `void_worm` and `void_worm_part` are both "Void Worm" — because the
segments are meant to read as one creature.

| ID | Display name | Category |
|---|---|---|
| `cockroach` | Cockroach | ambient |
| `cosmic_cod` | Cosmic Cod | ambient |
| `flutter` | Flutter | ambient |
| `fly` | Fly | ambient |
| `jerboa` | Jerboa | ambient |
| `rain_frog` | Rain Frog | ambient |
| `underminer` | Underminer | ambient |
| `blobfish` | Blobfish | aquatic |
| `cachalot_whale` | Cachalot Whale | aquatic |
| `catfish` | Catfish | aquatic |
| `comb_jelly` | Comb Jelly | aquatic |
| `devils_hole_pupfish` | Devil's Hole Pupfish | aquatic |
| `flying_fish` | Flying Fish | aquatic |
| `frilled_shark` | Frilled Shark | aquatic |
| `giant_squid` | Giant Squid | aquatic |
| `hammerhead_shark` | Hammerhead Shark | aquatic |
| `lobster` | Lobster | aquatic |
| `mantis_shrimp` | Mantis Shrimp | aquatic |
| `mimic_octopus` | Mimic Octopus | aquatic |
| `orca` | Orca | aquatic |
| `sea_bear` | Sea Bear | aquatic |
| `stradpole` | Stradpole | aquatic |
| `terrapin` | Terrapin | aquatic |
| `triops` | Triops | aquatic |
| `alligator_snapping_turtle` | Alligator Snapping Turtle | creature |
| `anaconda` | Anaconda | creature |
| `anteater` | Anteater | creature |
| `bald_eagle` | Bald Eagle | creature |
| `banana_slug` | Banana Slug | creature |
| `bison` | Bison | creature |
| `blue_jay` | Blue Jay | creature |
| `bunfungus` | Bunfungus | creature |
| `caiman` | Caiman | creature |
| `capuchin_monkey` | Capuchin Monkey | creature |
| `cosmaw` | Cosmaw | creature |
| `crocodile` | Crocodile | creature |
| `crow` | Crow | creature |
| `elephant` | Elephant | creature |
| `emu` | Emu | creature |
| `endergrade` | Endergrade | creature |
| `enderiophage` | Enderiophage | creature |
| `froststalker` | Froststalker | creature |
| `gazelle` | Gazelle | creature |
| `gelada_monkey` | Gelada Monkey | creature |
| `gorilla` | Gorilla | creature |
| `grizzly_bear` | Grizzly Bear | creature |
| `hummingbird` | Hummingbird | creature |
| `kangaroo` | Kangaroo | creature |
| `komodo_dragon` | Komodo Dragon | creature |
| `laviathan` | Laviathan | creature |
| `leafcutter_ant` | Leafcutter Ant | creature |
| `maned_wolf` | Maned Wolf | creature |
| `moose` | Moose | creature |
| `mudskipper` | Mudskipper | creature |
| `mungus` | Mungus | creature |
| `platypus` | Platypus | creature |
| `potoo` | Potoo | creature |
| `raccoon` | Raccoon | creature |
| `rattlesnake` | Rattlesnake | creature |
| `rhinoceros` | Rhinoceros | creature |
| `roadrunner` | Roadrunner | creature |
| `seagull` | Seagull | creature |
| `seal` | Seal | creature |
| `shoebill` | Shoebill | creature |
| `skreecher` | Skreecher | creature |
| `skunk` | Skunk | creature |
| `snow_leopard` | Snow Leopard | creature |
| `spectre` | Spectre | creature |
| `sugar_glider` | Sugar Glider | creature |
| `sunbird` | Sunbird | creature |
| `tarantula_hawk` | Tarantula Hawk | creature |
| `tasmanian_devil` | Tasmanian Devil | creature |
| `tiger` | Tiger | creature |
| `toucan` | Toucan | creature |
| `tusklin` | Tusklin | creature |
| `warped_toad` | Warped Toad | creature |
| `bone_serpent` | Bone Serpent | monster |
| `centipede_head` | Cave Centipede | monster |
| `crimson_mosquito` | Crimson Mosquito | monster |
| `dropbear` | Dropbear | monster |
| `farseer` | Farseer | monster |
| `guster` | Guster | monster |
| `mimicube` | Mimicube | monster |
| `murmur` | Murmur | monster |
| `murmur_head` | Murmur | monster |
| `rocky_roller` | Rocky Roller | monster |
| `skelewag` | Skelewag | monster |
| `soul_vulture` | Soul Vulture | monster |
| `straddler` | Straddler | monster |
| `void_worm` | Void Worm | monster |
| `warped_mosco` | Warped Mosco | monster |
| `anaconda_part` | Anaconda | segment |
| `bone_serpent_part` | Bone Serpent Bones | segment |
| `centipede_body` | Cave Centipede Body | segment |
| `centipede_tail` | Cave Centipede Tail | segment |
| `tendon_segment` | Tendon | segment |
| `void_worm_part` | Void Worm | segment |
| `cachalot_echo` | Whale Echo | projectile |
| `cockroach_egg` | Cockroach Ootheca | projectile |
| `emu_egg` | not documented | projectile |
| `enderiophage_rocket` | Enderiophage Rocket | projectile |
| `fart` | Fart Cloud | projectile |
| `gust` | Gust | projectile |
| `hemolymph` | Hemolymph | projectile |
| `ice_shard` | not documented | projectile |
| `mosquito_spit` | Mosquito Blood | projectile |
| `mud_ball` | Mud Ball | projectile |
| `pollen_ball` | Pollen Ball | projectile |
| `sand_shot` | Thrown Sand | projectile |
| `shark_tooth_arrow` | Shark Tooth Arrow | projectile |
| `squid_grapple` | Tentacle | projectile |
| `tossed_item` | Tossed Item | projectile |
| `vine_lasso` | Vine Lasso | projectile |
| `void_worm_shot` | Void Crystal | projectile |
| `straddleboard` | Straddleboard | vehicle |
| `void_portal` | Void Portal | misc |

### On the "140 entities" figure

`/tmp/am/entities.txt` and any count of `entity.alexsmobs.*` lang keys give 140,
but that number counts sub-keys as entities: variant names
(`entity.alexsmobs.comb_jelly.variant_0` = "Blue Comb Jelly"), the shared command
strings (`entity.alexsmobs.all.command_0` = "%s is wandering"), and three
leftover ids with no registered type. Collapsing to distinct ids gives 118 in
lang; the registry gives **116**, which is the real number of entity types the
mod adds.
