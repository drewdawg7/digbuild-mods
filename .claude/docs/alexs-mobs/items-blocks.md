<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Items & Blocks

The full catalog, grouped by what a thing does rather than by which mob dropped it.
IDs are all in the `alexsmobs:` namespace and are the real registry names, read from
the `register("…")` calls in `AMItemRegistry` / `AMBlockRegistry` — not guessed from the
Java field names, which sometimes differ (the field `ROADDRUNNER_BOOTS` registers as
`roadrunner_boots`, `SMALL_CATFISH_BUCKET` as `small_catfish_bucket`).

Registry totals:

| | Count |
|---|---|
| Standalone items | 151 |
| Spawn eggs | 89 |
| Banner pattern items | 5 |
| Dimensional Carver shard render items | 11 |
| Block items | 24 |
| Blocks | 25 (one has no item) |

Of the 151 standalone items, 11 are internal render-only stand-ins that never enter a
player inventory (see [Internal items](#internal-items)).

> **Numbers come from code, not from a wiki.** Durability, armour points, toughness,
> enchantability, food nutrition and saturation are read out of the item registry and
> `AMArmorMaterial`. The decompiled jar uses SRG method names (`m_41503_` durability,
> `m_41489_` food, `m_38760_` nutrition, `m_38758_` saturation modifier); every reading
> was cross-checked against the clean upstream source for the same version
> ([AlexModGuy/AlexsMobs](https://github.com/AlexModGuy/AlexsMobs), branch `1.20`,
> `gradle.properties` mod version 1.22.9 — the same version as the jar on the server),
> and the two agree line for line.

## Weapons and tools

Only one mining tool ships in the mod. Everything else is a melee weapon, a shield, or a
projectile launcher.

| Item | ID | Durability | Damage | Attack speed | Repairs with |
|---|---|---|---|---|---|
| Skelewag Skull | `skelewag_sword` | 430 | +3.5 (4.5 total) | 4.0/s (no penalty) | Bone |
| Tendon Whip | `tendon_whip` | 450 | +4 (5 total) | 1.0/s | Elastic Tendon |
| Ghostly Pickaxe | `ghostly_pickaxe` | 700 | +1 (2 total) | 1.2/s | Phantom Membrane |
| Shield Of The Deep | `shield_of_the_deep` | 400 | — | — | Serrated Shark Tooth |
| Shark Tooth Arrow | `shark_tooth_arrow` | — | vanilla arrow | — | — |
| Ancient Dart | `ancient_dart` | — | thrown, stack size 1 | — | — |

**Skelewag Skull** is a sword that also blocks: it accepts every shield tool action, uses
the block animation, and can be held up indefinitely. Dropped by the Skelewag.

**Tendon Whip** does not sweep. On a left click it fires a tendon at the nearest hostile
mob within 12 blocks that the player can see, costing 1 durability; the same tendon
launches on any successful hit. Crafted from Dropbear Claws, Elastic Tendons and a
wooden rod.

**Ghostly Pickaxe** is iron tier and mines pickaxe-mineable blocks at speed 20 (an iron
pickaxe is 6). When the player's inventory is completely full it keeps mining and stores
the drops in nine internal slots, pushing them back into the inventory as space appears;
the contents are listed in the tooltip and drop on the ground if the pickaxe breaks or is
destroyed as an item. Dropped by the Skreecher's soul route — see the Skreecher entry
under materials.

**Shield Of The Deep** behaves exactly like a vanilla shield. Crafted from 3 Serrated
Shark Teeth, 3 Prismarine Bricks, a Heart of the Sea and 2 Shark Teeth.

**Ancient Dart** appears in every Jungle Temple chest and Jungle Temple dispenser
(guaranteed, gated on `addLootToChests`, which is `true` on this server), and is also
dropped by a Capuchin Monkey holding one. Throwing it is the Capuchin Monkey's own
attack; a dispenser will throw it too.

### Ranged and spray weapons

| Item | ID | Durability | Ammunition | Effect on hit |
|---|---|---|---|---|
| Blood Sprayer | `blood_sprayer` | 100 | Blood Sac | 4 damage per shot |
| Hemolymph Blaster | `hemolymph_blaster` | 150 | Hemolymph Sac | 7 damage per shot |
| Pocket of Sand | `pocket_sand` | 220 | any `#minecraft:sand` | 2.5 damage + Blindness 5s |
| Stink Ray | `stink_ray` | 5 | Stink in a Bottle | Nausea 15s |

All four draw ammunition from anywhere in the player's inventory, cost 1 durability per
shot, and go on a short cooldown when they run dry. The Stink Ray is charged: release
time scales the projectile's speed.

- **Blood Sprayer** — Nether Bricks, 2 Blood Sacs and a Crimson Mosquito Proboscis.
- **Hemolymph Blaster** — 3 Hemolymph Sacs, a Blood Sprayer, Mimicream, a Warped Muscle
  and a Crimson Mosquito Proboscis.
- **Pocket of Sand** — 3 sand, 5 leather, a Guster Eye.
- **Stink Ray** — 2 Stink in a Bottle, 3 iron ingots, a hopper.

## Armour

Alex's Mobs armour is single pieces, not sets — no material covers all four slots and
there are no set bonuses. Armour points, toughness, durability and enchantability are
per-material values from `AMArmorMaterial`; durability is the material's multiplier times
13 (helmet), 15 (chestplate), 16 (leggings) or 11 (boots).

| Piece | ID | Slot | Armour | Toughness | Durability | Ench. | Repairs with |
|---|---|---|---|---|---|---|---|
| Spiked Turtle Shell | `spiked_turtle_shell` | Head | 3 | 1.0 | 455 | 30 | Spiked Scute |
| Antler Headdress | `moose_headgear` | Head | 3 | 0.5 | 247 | 21 | Moose Antler |
| Frontiersman's Cap | `frontier_cap` | Head | 3 | 2.5 | 221 | 21 | Raccoon Tail |
| Sombrero | `sombrero` | Head | 2 | 0.5 | 182 | 30 | Hay Block |
| Fedora | `fedora` | Head | 2 | 0.5 | 130 | 30 | Leather |
| Novelty Hat | `novelty_hat` | Head | 2 | 0.0 | 130 | 30 | Bone |
| Froststalker Helmet | `froststalker_helmet` | Head | 3 | 0.5 | 117 | 15 | not repairable |
| Crocodile Chestplate | `crocodile_chestplate` | Chest | 5 | 1.0 | 330 | 25 | Crocodile Scute |
| Rock Shell Chestplate | `rocky_chestplate` | Chest | 5 | 0.5 | 300 | 10 | Rocky Shell |
| Unsettling Kimono | `unsettling_kimono` | Chest | 3 | 0.0 | 120 | 15 | any wool |
| Tarantula Hawk Elytra | `tarantula_hawk_elytra` | Chest | 3 | 0.0 | 800 | 5 | Tattered Tarantula Hawk Wing |
| Cave Centipede Leggings | `centipede_leggings` | Legs | 6 | 0.5 | 320 | 22 | Cave Centipede Leg |
| Outback Leggings | `emu_leggings` | Legs | 4 | 0.5 | 144 | 20 | Emu Feather |
| Roadrunner Boots | `roadrunner_boots` | Feet | 3 | 0.0 | 198 | 20 | Roadrunner Feather |
| Flying Fish Boots | `flying_fish_boots` | Feet | 1 | 0.0 | 99 | 8 | Flying Fish |

Extra attributes and behaviours, all read from the code:

- **Spiked Turtle Shell** — 0.2 knockback resistance. Grants Water Breathing while worn
  out of water. Any attacker within roughly half a block of the wearer's hitbox takes 1
  thorns damage and is knocked back. Crafted from 5 Spiked Scutes around a Turtle Shell.
- **Antler Headdress** — +2 Attack Knockback while worn, and every melee swing knocks the
  target back an extra full unit. Crafted from 2 Moose Antlers, an iron ingot and 2 string.
- **Frontiersman's Cap** — +0.1 Movement Speed while sneaking. Crafted from 5 Hair of Bear,
  a leather helmet and a Raccoon Tail.
- **Crocodile Chestplate** — +1 Swim Speed. Crafted from 8 Crocodile Scutes.
- **Rock Shell Chestplate** — lets the wearer roll by sprinting. Crafted from 8 Rocky Shells.
- **Unsettling Kimono** — +2 Block Reach and +2 Entity Reach. Undead mobs will not target
  the wearer unless the wearer hits them first (mobs in `#alexsmobs:ignores_kimono` are
  exempt). Dropped by the Murmur.
- **Tarantula Hawk Elytra** — a chestplate that flies like an Elytra, losing 1 durability
  per second of flight. Crafted by combining a vanilla Elytra with 2 Tarantula Hawk Wings.
- **Cave Centipede Leggings** — wall climbing: while pressed against a wall out of water,
  the wearer climbs at 0.1 blocks/tick and takes no fall damage. Sneaking holds position.
  Crafted from 7 Cave Centipede Legs.
- **Outback Leggings** — 45% chance to cancel incoming projectile damage entirely
  (`emuPantsDodgeChance` on this server, the default). Crafted from Emu Feathers and
  Kangaroo Hide.
- **Roadrunner Boots** — +0.1 Movement Speed while standing on any block in `#minecraft:sand`.
  Crafted from 4 Roadrunner Feathers, leather boots and 2 Chiseled Sandstone.
- **Flying Fish Boots** — +0.5 Swim Speed, and jumping out of water starts a glide.
  Crafted from 2 string and 2 Flying Fish.
- **Froststalker Helmet** — wild Froststalkers follow the wearer instead of attacking, and
  treat them as the herd leader. Crafted from a Froststalker Horn and 5 Packed Ice.
- **Sombrero** — cosmetic. On 1 April it makes the wearer a Sea Bear target in water;
  standing on an Anti-Sea Bear Circle is the counter. Sold by wandering traders (20
  emeralds) and dropped by the maraca-playing Cockroach variant.
- **Novelty Hat** and **Fedora** — cosmetic. The Novelty Hat drops from Skelewags; the
  Fedora comes off a supercharged Platypus barter (1 in 31 weight) and can be put onto a
  Platypus.

### Bison fur insulation

Bison Fur is not armour itself but an upgrade applied to boots. Crafting any boots with a
single Block of Bison Fur stamps `BisonFur` on them and adds the tooltip "Insulated from
Snow". Insulated boots let the wearer walk on top of Powder Snow, clear freezing, and
push upward out of Powder Snow they are already in. The recipe is code-driven
(`alexsmobs:bison_upgrade`), so any boots from any mod qualify as long as they are not
already insulated.

## Wearables and curios

**Alex's Mobs has no Curios integration.** The mod ships no `curios` data directory, no
Curios code path, and none of the pack's Curios compat mods (`raccompat`, `ramcompat`,
`rarcompat`) list an `alexsmobs:` item in their slot tags. Everything wearable in this
mod goes in a vanilla armour slot, listed in the armour table above. The only two items
that behave like accessories are held, not worn:

| Item | ID | Stack | How it is used |
|---|---|---|---|
| Falconry Glove | `falconry_glove` | 1 | Held. Left click launches a perched bird of prey at a target; the bird returns to the glove. Crafted from 4 leather and Hair of Bear. |
| Vine Lasso | `vine_lasso` | 1 | Held. Charge and release to throw a lasso that captures and carries a mob. Crafted from a lead, 4 vines and a Shed Snake Skin. |

The **Falconry Hood** (`falconry_hood`, 2 leather + a Roadrunner Feather) is placed on the
bird, not on the player.

## Food and drink

Saturation restored is 2 × nutrition × the saturation modifier, the vanilla formula.

| Item | ID | Nutrition | Saturation mod. | Notes |
|---|---|---|---|---|
| Shrimp-Fried Rice | `shrimp_fried_rice` | 12 | 1.0 | Made in a Shoebill's nest area from items in `#alexsmobs:shrimp_rice_fryables` |
| Kangaroo Burger | `kangaroo_burger` | 12 | 1.0 | 2 bread + Cooked Kangaroo Meat |
| Cooked Kangaroo Meat | `cooked_kangaroo_meat` | 8 | 0.85 | Smelt/smoke/campfire Kangaroo Meat |
| Cooked Moose Ribs | `cooked_moose_ribs` | 7 | 0.85 | Smelt/smoke/campfire Raw Moose Ribs |
| Cooked Lobster Tail | `cooked_lobster_tail` | 6 | 0.65 | Smelt/smoke/campfire Lobster Tail |
| Cosmic Cod | `cosmic_cod` | 6 | 0.3 | 15% chance of Ender Flu for 10 minutes |
| Sopa De Macaco | `sopa_de_macaco` | 5 | 0.4 | Bowl + Banana Peel + brown mushroom + bone; stack size 1 |
| Cooked Catfish | `cooked_catfish` | 5 | 0.5 | Smelt/smoke/campfire Raw Catfish |
| Banana | `banana` | 4 | 0.3 | 1 in 200 from jungle leaves (Fortune improves it); also from Capuchin Monkeys |
| Boiled Emu Egg | `boiled_emu_egg` | 4 | 1.0 | Smelt/smoke/campfire an Emu Egg |
| Kangaroo Meat | `kangaroo_meat` | 4 | 0.6 | Kangaroo drop |
| Mosquito Repellent Stew | `mosquito_repellent_stew` | 4 | 0.3 | Always edible; Mosquito Repellent for 20 minutes; stack size 1 |
| Raw Moose Ribs | `moose_ribs` | 3 | 0.6 | Moose drop |
| Blobfish | `blobfish` | 3 | 0.4 | Always inflicts Poison for 6 seconds |
| Flying Fish | `flying_fish` | 3 | 0.4 | Flying Fish drop |
| Gongylidia | `gongylidia` | 3 | 1.2 | Grown in a Leafcutter Ant Chamber |
| Lobster Tail | `lobster_tail` | 2 | 0.4 | Lobster drop |
| Raw Catfish | `raw_catfish` | 2 | 0.3 | Catfish drop, all three sizes |
| Maggot | `maggot` | 1 | 0.2 | Fly drop; Platypus and Sugar Glider barters |
| Rainbow Jelly | `rainbow_jelly` | 1 | 0.2 | Comb Jelly drop |
| Fish Oil | `fish_oil` | 0 | 0.2 | Drink, 2 seconds, returns the glass bottle |

- **Mosquito Repellent Stew** is made shapelessly from a bowl, 2 Triops Eggs and a Stink
  in a Bottle. The Mosquito Repellent effect lasts 24000 ticks (20 minutes) and applies
  every time, and the stew is edible on a full hunger bar.
- **Fish Oil** is 4 Blobfish plus a glass bottle. With `fishOilMeme` enabled — it is `true`
  on this server, the default — drinking it also applies Oiled for 60 seconds.
- **Rainbow Jelly** doubles as a dye for living creatures: right-clicking a mob with it
  sets that mob's rainbow pattern (rainbow, trans, non-binary, bi, ace, weezer or brazil,
  chosen by the stack's custom name) and consumes the jelly.
- **Gongylidia** is the fungus a Leafcutter Ant colony grows. It is also compostable at 0.9,
  the highest of any Alex's Mobs item; Banana Peel is 1.0, Banana and Acacia Blossom 0.65.
- **Lava Bottle** (`lava_bottle`) is not food. Right-clicking lava with a glass bottle fills
  one and sets the player on fire for 6 seconds (`lavaBottleEnabled`, `true` here). It is
  the base for Lava Vision potions.

### Brewing ingredients

Five Alex's Mobs drops are brewing ingredients, and one item exists only as a brewing
intermediate.

| Base | Ingredient | Result |
|---|---|---|
| Potion of Strength | Hair of Bear | Knockback Resistance (redstone/glowstone extend it) |
| Lava Bottle | Bone Serpent Tooth | Lava Vision (redstone extends it) |
| Potion of Poison | Rattlesnake Rattle | **Poisonous Essence** (`poison_bottle`) |
| Poisonous Essence *or* Komodo Dragon Spit Bottle | Cave Centipede Leg | Poison Resistance |
| Poison Resistance | Komodo Dragon Spit | Long Poison Resistance |
| Potion of Swiftness II | Gazelle Horn | Speed III |
| Awkward Potion | Cockroach Wing | Bug Pheromones (redstone extends it) |
| Awkward Potion | Soul Heart | Soulsteal (redstone/glowstone extend it) |
| Awkward Potion | Dropbear Claw | Clinging (redstone extends it) |

**Komodo Dragon Spit Bottle** (`komodo_spit_bottle`) is 4 Komodo Dragon Spit plus a glass
bottle. Three Komodo Dragon Spit also craft shapelessly into a vanilla Slime Ball.

## Mob-derived materials

Every entry names the mob it comes from.

| Material | ID | Source |
|---|---|---|
| Hair of Bear | `bear_fur` | Grizzly Bear |
| Bear Dust | `bear_dust` | Grizzly Bear (Epic rarity; a joke item, see below) |
| Roadrunner Feather | `roadrunner_feather` | Roadrunner |
| Bone Serpent Tooth | `bone_serpent_tooth` | Bone Serpent; fireproof |
| Gazelle Horn | `gazelle_horn` | Gazelle; fireproof |
| Crocodile Scute | `crocodile_scute` | Crocodile, 1–2 when it sheds |
| Blood Sac | `blood_sac` | Crimson Mosquito, only when it is full of blood |
| Crimson Mosquito Proboscis | `mosquito_proboscis` | Crimson Mosquito |
| Crimson Mosquito Larva | `mosquito_larva` | Maggot + Crimson Mosquito Proboscis |
| Rattlesnake Rattle | `rattlesnake_rattle` | Rattlesnake |
| Shark Tooth | `shark_tooth` | Hammerhead Shark, shed when it bites; also a Seal barter |
| Serrated Shark Tooth | `serrated_shark_tooth` | Frilled Shark |
| Komodo Dragon Spit | `komodo_spit` | Komodo Dragon |
| Cave Centipede Leg | `centipede_leg` | Cave Centipede |
| Moose Antler | `moose_antler` | Moose |
| Mimicream | `mimicream` | Mimicube |
| Raccoon Tail | `raccoon_tail` | Raccoon |
| Cockroach Wing Fragment | `cockroach_wing_fragment` | Cockroach |
| Cockroach Wing | `cockroach_wing` | 9 fragments |
| Acacia Blossom | `acacia_blossom` | 1 in 130 from acacia leaves; Sugar Gliders and Elephants forage it |
| Soul Heart | `soul_heart` | Soul Vulture, when it is carrying a heart |
| Spiked Scute | `spiked_scute` | Alligator Snapping Turtle, shed |
| Guster Eye | `guster_eye` | Guster (all three colours) |
| Warped Muscle | `warped_muscle` | Warped Mosco |
| Hemolymph Sac | `hemolymph_sac` | Warped Mosco |
| Warped Mixture | `warped_mixture` | Rare rarity, stack size 1; feeding it to a Crimson Mosquito is what turns it into a Warped Mosco |
| Straddlite | `straddlite` | Straddler; fireproof |
| Emu Feather | `emu_feather` | Emu; fireproof |
| Dropbear Claw | `dropbear_claw` | Dropbear |
| Kangaroo Hide | `kangaroo_hide` | Kangaroo; 2 hides craft into 1 leather |
| Ambergris | `ambergris` | Cachalot Whale; burns for 12800 ticks (640 seconds) as furnace fuel |
| Cachalot Whale Tooth | `cachalot_whale_tooth` | Cachalot Whale |
| Leafcutter Ant Pupa | `leafcutter_ant_pupa` | Leafcutter Ant Queen, or an Ant Chamber broken without Silk Touch |
| Tattered Tarantula Hawk Wing | `tarantula_hawk_wing_fragment` | Tarantula Hawk |
| Tarantula Hawk Wing | `tarantula_hawk_wing` | 9 fragments |
| Void Worm Mandible | `void_worm_mandible` | Void Worm |
| Void Worm Eye | `void_worm_eye` | Void Worm; Rare rarity |
| Froststalker Horn | `froststalker_horn` | Froststalker |
| Shed Snake Skin | `shed_snake_skin` | Anaconda, shed |
| Rocky Shell | `rocky_shell` | Rocky Roller |
| Mungal Spores | `mungal_spores` | Mungus |
| Bison Fur | `bison_fur` | Bison |
| Lost Tentacle | `lost_tentacle` | Giant Squid |
| Fish Bones | `fish_bones` | Skelewag; 1 bone crafts into 2 bone meal |
| Farseer Arm | `farseer_arm` | Farseer; Rare rarity |
| Skreecher Soul | `skreecher_soul` | Skreecher |
| Elastic Tendon | `elastic_tendon` | Murmur |
| Banana Slug Slime | `banana_slug_slime` | Banana Slug |
| Banana Peel | `banana_peel` | Eating a Banana leaves one; also a placeable block |
| Straddlite Tack | `straddle_helmet` | 2 Straddlite + 2 string; fireproof |
| Straddlite Saddle | `straddle_saddle` | Saddle + 2 Straddlite; fireproof |
| Ancient Hogshoes | `pigshoes` | 2.5% of Piglin barters; fitted to a Tusklin |

**Ancient Hogshoes** are the only barter-only item. Fitted to a Tusklin they cut its
movement penalty (0.4 instead of 0.9) and raise its charge duration to 160 ticks from 60.
They accept boot enchantments but not Unbreaking or Mending.

**Mimicream** duplicates gear. Placing 8 Mimicream and any one damageable item in a
crafting grid returns a second copy of that item (`mimicreamRepair` is `true` here).
The server's blacklist is `alexsmobs:blood_sprayer` and `alexsmobs:hemolymph_blaster`,
the mod defaults.

## Utility and transport

### Buckets

Fifteen mob buckets. All are placeable by dispenser and return an empty bucket.

`lobster_bucket`, `blobfish_bucket`, `stradpole_bucket` (lava), `platypus_bucket`,
`frilled_shark_bucket`, `mimic_octopus_bucket`, `terrapin_bucket`, `comb_jelly_bucket`,
`devils_hole_pupfish_bucket`, `small_catfish_bucket`, `medium_catfish_bucket`,
`large_catfish_bucket`, `flying_fish_bucket`, `mudskipper_bucket`, `triops_bucket`.

Two are not water buckets: **Bucket of Stradpole** holds lava, and **Bucket of Cosmic Cod**
(`cosmic_cod_bucket`) holds no fluid at all — it releases the fish into open air. The three
catfish buckets are separate items but all release the same entity at the matching size.

**Potted Flutter** (`potted_flutter`) works the same way for a Flutter and stores the
creature's data in the item.

### Locators

| Item | ID | Durability | Points at |
|---|---|---|---|
| Echolocator | `echolocator` | 100 | Nearest dark cave air within its search range; remembers the position on the stack |
| Endolocator | `endolocator` | 25 | Nearest End Portal Frame within 128 blocks, falling back to the nearest structure in `#minecraft:eye_of_ender_located` within 100 chunks |
| Strange Fish Finder | `pupfish_locator` | 200 | The world's single Devil's Hole Pupfish chunk |

All three fire a visible whale-click pulse toward the target, cost 1 durability and set a
5-tick cooldown. The Echolocator is 2 Cachalot Whale Teeth, Ambergris and 4 iron ingots;
the Endolocator is an Echolocator surrounded by 4 ender pearls; the Strange Fish Finder is
an Echolocator with 4 Fish Bones and 4 slime balls.

### Transport and traversal

| Item | ID | Durability | Behaviour |
|---|---|---|---|
| Straddleboard | `straddleboard` | 220 | Placed on lava like a boat; fireproof; dyeable. Enchantable at value 1, but not with Unbreaking or Mending. 4 Straddlite + 3 netherite ingots |
| Grappling Squok | `squid_grapple` | 450 | Charge and release to fire a tentacle hook that pulls the player; sneak to detach. 3 Lost Tentacles, a crossbow, 3 copper ingots |
| Enderiophage Rocket | `enderiophage_rocket` | — | A firework rocket that flies as an Enderiophage. Usable for Elytra boosting. Crafts 3 from a Capsid, 2 End Stone and 2 iron nuggets |
| Chorus Fruit on a Stick | `chorus_on_a_stick` | — | Steers a ridden Endergrade. Fishing rod + chorus fruit |
| Vine Lasso | `vine_lasso` | — | Captures and carries a mob |
| Falconry Glove | `falconry_glove` | — | Perch and launch a bird of prey |

### Dimensional Carver

| Item | ID | Durability | Rarity |
|---|---|---|---|
| Dimensional Carver | `dimensional_carver` | 20 | Epic |
| Shattered Dimensional Carver | `shattered_dimensional_carver` | 4 | Rare |

Holding right click for 200 ticks (10 seconds) carves a portal at the point aimed at. A
successful carve costs 1 durability and sets a 200-tick cooldown; releasing early gives a
40-tick cooldown. Both repair from experience at an unusually high ratio (100 durability
per experience point). The **Shattered** version, made in a Capsid, opens a portal that
lasts 2000 ticks and lands the player 1,000,000 blocks away in the direction opposite the
one they were facing — or at world bottom/top if aimed straight down or up — inside the
same dimension.

The Dimensional Carver is crafted from 2 Void Worm Mandibles, a Void Worm Eye and 2
netherite ingots.

### Summoning and eggs

| Item | ID | Effect |
|---|---|---|
| Mysterious Worm | `mysterious_worm` | Dropped below Y −60 in a dimension listed in `voidWormSpawnDimensions` (this server: The End only), it summons the Void Worm boss with 25–39 segments and 160 max health |
| Emu Egg | `emu_egg` | Throwable, stacks to 8; hatches an Emu |
| Cockroach Ootheca | `cockroach_ootheca` | Throwable; hatches Cockroaches |
| Leafcutter Ant Pupa | `leafcutter_ant_pupa` | Used on two stacked blocks in `#alexsmobs:leafcutter_pupa_usable_on`, converts them into an Anthill over an Ant Chamber and seeds up to 3 ants including a queen |
| Stink in a Bottle | `stink_bottle` | Places a Skunk Spray block and returns the glass bottle; stacks to 16 |

Void Worm summoning is enabled on this server (`voidWormSummonable = true`).

### Animal Dictionary

`animal_dictionary`, stack size 1. Right-clicking any Alex's Mobs creature opens that
creature's page; right-clicking the air opens the book. It can be placed on a lectern.
Crafted from a book, any item in `#alexsmobs:animal_dictionary_ingredient` (Crocodile
Scute, Hair of Bear, Roadrunner Feather, Gazelle Horn, Rattlesnake Rattle, Komodo Dragon
Spit, Cave Centipede Leg, Moose Antler, Raccoon Tail, Cockroach Wing, Spiked Scute,
Straddlite, Emu Feather, Dropbear Claw, Cachalot Whale Tooth, Capsid or Rocky Shell) and
any green dye. It is also in the Trader Elephant's chest loot.

**Every player gets one on first join** — `giveBookOnStartup` is `true` on this server.

### Banner patterns

Five, all crafted from paper plus one mob material, all stack size 1.

| Pattern | ID | Recipe |
|---|---|---|
| Bear | `banner_pattern_bear` | Paper + Hair of Bear |
| Star Cross | `banner_pattern_australia_0` | Paper + Kangaroo Hide |
| Union Jack Ensign | `banner_pattern_australia_1` | Paper + Emu Feather |
| Sun Symbol | `banner_pattern_new_mexico` | Paper + Tattered Tarantula Hawk Wing |
| Caption Band | `banner_pattern_brazil` | Paper + Shed Snake Skin |

## Blocks

25 blocks. 24 have block items; Skunk Spray is placed by the Stink in a Bottle item and
has no item of its own.

### Functional blocks

**Capsid** (`capsid`) — hardness 1.5, needs a correct tool, emits light level 5. The mod's
transmutation device; see [The Capsid](#the-capsid) below. Dropped by Enderiophages.

**Transmutation Table** (`transmutation_table`) — hardness 1.0, light level 2, Epic rarity
item, fireproof. Opens a GUI with one input slot and three rolled results. Putting in a
stack of anything that stacks past 1 (except items on the blacklist — `minecraft:beacon`
on this server) and paying **3 experience levels** turns the whole stack into one of the
three offered items. Each transmutation rerolls the three offers from the mod's common,
uncommon and rare tables, and unless `limitTransmutingToLootTables` is set the table also
learns what players feed it and starts offering those items back, at up to a 20% chance
per roll. **Breaking it explodes** — power 3, block-damaging — because
`transmutingTableExplodes` is `true` here, and it only drops itself with Silk Touch;
without Silk Touch it drops a Nether Star. Crafted from a Nether Star, 2 Farseer Arms and
3 obsidian.

**Gustmaker** (`gustmaker`) — hardness 1.5, needs a correct tool. A redstone-triggered wind
cannon: on a rising redstone edge it spawns a Gust travelling in the direction it faces,
then rearms after 20 ticks. Facing up or down produces a vertical gust. Crafted from 8 Cut
Sandstone, a Guster Eye and redstone.

**Hummingbird Feeder** (`hummingbird_feeder`) — hardness 0.5, hangs from a block above or
stands on one below, waterloggable. Right-click with a Water Bottle and with any item in
`#alexsmobs:hummingbird_feeder_sweeteners` to fill both halves; Hummingbirds feed from a
full feeder. Crafted from 5 copper ingots, a glass bottle and 2 sunflowers.

**Sculk Boomer** (`sculk_boomer`) — hardness 3.0, blast resistance 12. A sculk sensor
variant with an 8-block listening radius: on a vibration it opens, screams for 100 ticks,
and deals **6–8 magic damage** with knockback to everything in range, unless it is being
held shut by a redstone signal. Crafted from 3 sculk, 3 Skreecher Souls and 3 bone blocks.

**Void Worm Beak** (`void_worm_beak`) — while powered by redstone it chomps and deals **5
damage every 5 ticks** to anything inside its own block space. Crafted from 2 Void Worm
Mandibles.

**Leafcutter Anthill** (`leafcutter_anthill`) and **Leafcutter Ant Chamber**
(`leafcutter_ant_chamber`) — the two halves of an ant colony, created by using a
Leafcutter Ant Pupa. The colony holds up to 10 ants on this server
(`leafcutterAntColonySize`), grows Gongylidia at a 30% chance per leaf delivered, and
regains a lost worker every 25 leaf feedings if it is below half strength. Ants break
leaves 20% of the time when harvesting. Breaking the Chamber without Silk Touch drops a
Leafcutter Ant Pupa on a Fortune-weighted chance (10% at Fortune 0, rising to guaranteed
at Fortune 3).

**Void Worm Effigy** (`void_worm_effigy`) — hardness 1.5, placeable on any face. Crafted
from a Void Worm Beak, 4 ender pearls and 4 purpur blocks.

### Eggs and spawn blocks

| Block | ID | Notes |
|---|---|---|
| Crocodile Egg | `crocodile_egg` | Hardness 0.5, 1–4 eggs per block, hatches on random tick; Silk Touch only |
| Caiman Egg | `caiman_egg` | As above |
| Platypus Egg | `platypus_egg` | As above |
| Terrapin Egg | `terrapin_egg` | Has a block entity; drops nothing when broken |
| Triops Eggs | `triops_eggs` | Frogspawn-style; hatches Triops |

Crocodile Eggs and Caiman Eggs come from the animals themselves; Crocodile Eggs are also a
wandering trader offer.

### Building and terrain blocks

| Block | ID | Notes |
|---|---|---|
| Block of Straddlite | `straddlite_block` | Hardness 1.0, blast resistance 1200, ancient-debris sound, fireproof item. 9 Straddlite; uncrafts back |
| Block of Bison Fur | `bison_fur_block` | Hardness 0.6, wool sound. 9 Bison Fur; uncrafts back. 4 Bison Fur also make 1 brown wool |
| Bison Fur Carpet | `bison_carpet` | 2 Blocks of Bison Fur make 3 carpets |
| Rainbow Glass | `rainbow_glass` | Hardness 0.2, light level 11, slippery (friction 0.97), non-solid. Silk Touch only. 8 glass + a Rainbow Jelly makes 8 |
| Banana Slug Slime Block | `banana_slug_slime_block` | Slows movement to 40% and jumping to 50%; converts nearby blocks to Crystallized Mucus. 9 Banana Slug Slime; uncrafts back |
| Crystallized Banana Slug Mucus | `crystalized_banana_slug_mucus` | Hardness 0.1, decays like leaves when more than 7 blocks from a Slime Block; Silk Touch only |
| Banana Peel | `banana_peel` | Hardness 0.2, no collision, friction 0.99999 — anything crossing it slides |
| Ender Residue | `ender_residue` | Hardness 0.2, light level 3. Left behind by a burrowing Void Worm; ages out and disappears, and drops nothing |
| Skunk Spray | `skunk_spray` | Instabreak, no collision, decays on random tick; placed by Stink in a Bottle |
| Anti-Sea Bear Circle | `sand_circle` / `red_sand_circle` | Sand and Red Sand variants that fall like sand and drop plain sand. Standing on one makes a mob invalid as a Sea Bear target |

### Registered but unreachable

Twelve blocks have display names, blockstates, models and Java classes shipped in the jar
but **are not in `AMBlockRegistry`**. Verified by set-differencing the `register("…")`
string literals in the decompiled registry class against the `block.alexsmobs.*` keys in
`en_us.json`: 25 registered names, 37 lang names, and the 12 below appear only in lang.
The registration lines are present but commented out in the upstream source. These blocks
cannot be obtained, placed or referenced by ID in-game, and a datapack that names them
will fail:

`purpur_planks`, `purpur_planks_stairs`, `purpur_planks_slab`, `purpur_planks_wall`,
`end_pirate_door`, `end_pirate_trapdoor`, `end_pirate_anchor` (Void Anchor),
`end_pirate_anchor_winch` (Void Winch), `end_pirate_ship_wheel`, `end_pirate_flag`,
`phantom_sail`, `spectre_sail`.

## Music discs, novelty and internal items

| Item | ID | Notes |
|---|---|---|
| Music Disc (Thime) | `music_disc_thime` | LudoCrypt — Thime, 314 seconds, comparator output 14, Rare |
| Music Disc (Daze) | `music_disc_daze` | LudoCrypt — Daze, 191 seconds, comparator output 14, Rare. Made in a Capsid from any music disc |
| Maraca | `maraca` | Right-click plays a shake, 3-tick cooldown. Wooden planks, a Rattlesnake Rattle and a wooden rod. Dropped by the maraca Cockroach variant |
| Bear Dust | `bear_dust` | Epic rarity, right-click plays a sound, hidden from the creative tab. Rare Grizzly Bear drop |
| Halo | `halo` | Render-only; worn by certain Gorillas and Kangaroos, not obtainable |
| Novelty Hat | `novelty_hat` | Cosmetic; tooltip "He was number one!" |

### Internal items

Eleven registered items exist only so the game can render something in a specific place —
they carry names like "This is not a Falconry Glove" and never enter a player inventory:
`tab_icon`, `halo`, `falconry_glove_inventory`, `falconry_glove_hand`,
`vine_lasso_inventory`, `vine_lasso_hand`, `skelewag_sword_inventory`,
`skelewag_sword_hand`, `stink_ray_hand`, `stink_ray_inventory`, `stink_ray_empty_hand`,
`stink_ray_empty_inventory`, plus the 11 `dimensional_carver_shard_0`…`_10` entries.

**Translation-key bug:** `alexsmobs:stink_ray_empty_inventory` is registered, but the
language file's only matching key is `item.alexsmobs.stink_empty_inventory`. Its class,
`ItemInventoryOnly`, does not override `getDescriptionId()` — the only item in the mod
that does is `ItemStinkBottle`, and that override returns the standard
`getOrCreateDescriptionId()` so the placed-block item keeps its item key rather than the
Skunk Spray block key. So the empty Stink Ray really does resolve to a key with no
translation. Harmless — nothing shows it to a player under normal play — but worth knowing
if `item.alexsmobs.stink_ray_empty_inventory` ever surfaces in a log or command output.
`insulated_with_fur` is the other lang key with no matching item; that one is correct, as
it is the Bison Fur boots tooltip line rather than an item name.

Block items are translated through their block's `block.alexsmobs.*` key, which is
vanilla `BlockItem` behaviour, so the absence of `item.alexsmobs.<block>` keys for the 24
block items is not a defect.

## The Capsid

The Capsid is the mod's transmutation block. It has no GUI: right-clicking with an item
inserts one, right-clicking again with a different item swaps and pops out the old one,
and hoppers can feed it from any side but cannot pull items out.

An item sitting in a Capsid converts when the Capsid is the **top** block of its column —
if another Capsid sits directly above, the item is instead floated up and pushed into the
container above, which is how a stack of Capsids acts as a conveyor. While converting, the
Capsid visibly vibrates; interrupting it resets the timer to zero.

Four recipes ship as data in `data/alexsmobs/capsid_recipes/`:

| Input | Output | Time |
|---|---|---|
| `minecraft:cod` | Cosmic Cod | 120 ticks (6 s) |
| Any item in `#minecraft:music_discs` | Music Disc (Daze) | 120 ticks (6 s) |
| Crimson Mosquito Larva | Mysterious Worm | 120 ticks (6 s) |
| Dimensional Carver | Shattered Dimensional Carver | 200 ticks (10 s) |

One further conversion is hard-coded rather than data-driven: an **Eye of Ender** in a
Capsid placed directly on top of a vertically oriented **End Rod** consumes both blocks
after 20 ticks and spawns an Enderiophage. This is the only route to a tame-able
Enderiophage other than finding one.

Capsids drop from Enderiophages and are also an accepted Animal Dictionary ingredient.

## Recipes and recipe types

84 recipe files ship in `data/alexsmobs/recipes/`.

| Type | Count |
|---|---|
| `minecraft:crafting_shaped` | 41 |
| `minecraft:crafting_shapeless` | 17 |
| `minecraft:smelting` | 6 |
| `minecraft:smoking` | 6 |
| `minecraft:campfire_cooking` | 6 |
| `alexsmobs:capsid` (separate `capsid_recipes` directory) | 4 |
| `alexsmobs:mimicream_repair` | 1 |
| `alexsmobs:bison_upgrade` | 1 |

All smelting recipes are food (Emu Egg, Kangaroo Meat, Lobster Tail, Moose Ribs, Catfish),
each at 0.15 experience and the vanilla 200/100/600-tick times for furnace, smoker and
campfire.

## Server notes

- **`giveBookOnStartup = true`** — every player receives an Animal Dictionary on first join.
- **`addLootToChests = true`** — enables the Ancient Dart in Jungle Temple chests and
  dispensers (guaranteed) and Ancient Hogshoes in Piglin bartering (2.5%).
- **`transmutingExperienceCost = 3`** and **`transmutingTableExplodes = true`** — both mod
  defaults; the second one is the surprising one to tell players about.
- **`voidWormSpawnDimensions = ["minecraft:the_end"]`** — the Mysterious Worm does nothing
  in the Overworld or Nether.
- **`mimicreamRepair = true`** with the default two-item blacklist — Mimicream duplication
  is live.
- `data/domesticationinnovation/` tags ship inside the jar (pet-store cage and fish-tank
  entity type lists). **Domestication Innovation is not installed on this server**, so
  those tags load against nothing and change no item or block behaviour here.
