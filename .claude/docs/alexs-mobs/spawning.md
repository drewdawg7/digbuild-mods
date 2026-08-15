<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Spawning

Ninety JSON files in `config/alexsmobs/` decide which biomes each Alex's Mobs creature may
appear in. **All ninety on this server are byte-identical to the mod's generated defaults**, as are
all 176 spawn weights and roll counts in `alexsmobs.toml` — see [config.md](config.md).

## How a spawn is decided

Five gates, in order. A mob appears only if all five pass.

1. **Biome rule** — the JSON in `config/alexsmobs/`. A list of OR'd groups; within a group every
   condition must hold. A condition is either a biome tag or an exact biome id, and may be negated.
   This is what the "Biomes" column below translates.
2. **Spawn weight** — the mob joins that biome's pool for its mob category with this weight, and is
   drawn against every other entry in the same category. Weight `0` removes it entirely.
3. **Placement type** — where the game may put it: on ground, in water, in lava, on leaves
   (a type this mod adds), or unrestricted.
4. **Placement predicate** — the mob's own `can…Spawn` check: block underneath, light level, height,
   weather, sky access. This is the "Conditions" column.
5. **Spawn rolls** — a final 1-in-N gate (`0` = no gate). Spawn eggs and spawners skip gates 4 and 5.

Group sizes are hard-coded in `AMWorldRegistry.addBiomeSpawns` and are not configurable.

**Reading the numbers.** Weight is meaningful only against the other entries in the same mob
category in the same biome — a weight of 70 for the Straddler is large because Basalt Deltas has a
short monster list, while 30 for the Elephant competes with every vanilla savanna animal. Group
size is the min–max the game tries to place per successful spawn attempt.

## Which biome mods this server actually has

The stock configs name biomes from six external mods. Only two of them are installed here:

| Namespace | Mod | Installed |
|---|---|---|
| `terralith` | Terralith 2.5.4 | **yes** — 421 references, all live |
| `alexscaves` | Alex's Caves 2.0.2 | **yes** — 2 references (Abyssal Chasm) |
| `biomesoplenty` | Biomes O' Plenty | no — 36 references, all inert |
| `incendium` | Incendium | no — 9 references, all inert |
| `byg` | Oh The Biomes You'll Go | no — 4 references, all inert |
| `autumnity` | Autumnity | no — 1 reference, inert |

Entries naming an absent mod simply never match; they cost nothing and are left in place because
they are the stock defaults. They are still listed below, marked *(not installed)*, so the tables
stay a faithful record of the file.

One entry, `snowy_maple_woods` in the Moose config, is written without a namespace. It resolves as
`minecraft:snowy_maple_woods`, which does not exist. It is an upstream typo — the intended biome,
`terralith:snowy_maple_forest`, is listed separately in the same file, so nothing is lost.

## Overworld

### Swamps, marshes and rivers

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Alligator Snapping Turtle | 20 | 1-in-1 | 1–2 | creature | Swamps except mangrove swamp; Terralith Ice Marsh, Orchid Swamp; *(BOP Tundra Bog, not installed)* | Standing on natural ground (stone, dirt, sand, gravel, terracotta or mud), below sea level + 4 |
| Anaconda | 12 | — | 1–1 | creature | All swamps including mangrove swamp; Terralith Ice Marsh, Orchid Swamp, Amethyst Rainforest, Tropical Jungle, Skylands Summer | Same ground types, below sea level + 4 |
| Crocodile | 20 | 1-in-1 | 1–2 | creature | Swamps, mangrove swamp, and any river that is not cold; Terralith Orchid Swamp, Red Oasis, Warm River; *(BOP Tropic Beach)* | Same ground types, below sea level + 4 |
| Caiman | 29 | — | 2–4 | creature | Mangrove swamp only; Terralith Underground Jungle cave | Standing on mud or muddy mangrove roots |
| Mudskipper | 28 | — | 2–4 | creature | Mangrove swamp; Terralith Underground Jungle cave | Standing on mud or muddy mangrove roots |
| Shoebill | 10 | — | 1–2 | creature | Swamps except mangrove swamp; Terralith Orchid Swamp, Red Oasis | Standard animal rules: spawnable ground, light above 8 |
| Platypus | 20 | — | 1–2 | creature | Rivers that are not cold; Terralith Warm River; *(BOP Tundra Bog)* | Natural ground, below sea level + 4 |
| Terrapin | 4 | — | 1–2 | water ambient | Same biomes as the Platypus | In a water source block |
| Catfish | 4 | 1-in-2 | 1–3 | water ambient | Swamps except mangrove swamp; rivers that are not cold; Terralith Orchid Swamp, Ice Marsh, Warm River | In a water source block |

### Jungles

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Capuchin Monkey | 28 | — | 9–16 | creature | Jungles except bamboo jungle; mangrove swamp; Terralith Amethyst Canyon, Amethyst Rainforest, Jungle Mountains, Rocky Jungle, Tropical Jungle, Skylands Summer | Spawns in leaves. On leaves, logs, grass block or air, light above 8 |
| Toucan | 23 | — | 5–5 | creature | Jungles except bamboo jungle; the same six Terralith jungles | Spawns in leaves; no further restriction |
| Gorilla | 25 | — | 7–7 | creature | Jungles except bamboo jungle; the same six Terralith jungles | On leaves, logs, grass block or air, light above 8 |
| Anteater | 7 | — | 1–3 | creature | Jungles except bamboo jungle; the same six Terralith jungles | Light above 8 |
| Hummingbird | 19 | 1-in-1 | 7–7 | creature | Flower forest, sunflower plains, all jungles, meadow, cherry grove; Terralith Blooming Valley, Blooming Plateau, Lavender Forest/Valley, Moonlight Grove/Valley, Sakura Grove/Valley, Amethyst Canyon, Amethyst Rainforest, Jungle Mountains, Rocky Jungle, Tropical Jungle, Valley Clearing, Orchid Swamp, Skylands Autumn/Spring/Summer | On leaves, logs, grass block or air, light above 8 |
| Komodo Dragon | 16 | 1-in-1 | 1–2 | creature | Jungles that are not dense — in practice sparse jungle; Terralith Sandstone Valley, Red Oasis, Skylands Summer; *(BOP Tropics)* | Natural ground, light above 8 |
| Tiger | 30 | — | 1–3 | creature | Bamboo jungle, cherry grove; Terralith Sakura Grove/Valley, Amethyst Canyon, Amethyst Rainforest, Skylands Spring; *(BOP Bamboo Grove, Snowblossom Grove)* | Light above 8 |

The Leafcutter Ant has a config file, `leafcutter_anthill_spawns.json`, but it is not a mob spawn —
see [Mobs with no natural spawn](#mobs-with-no-natural-spawn).

### Savanna and badlands

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Gazelle | 40 | — | 7–7 | creature | Savannas; Terralith Arid Highlands, Brushland, Fractured Savanna, Savanna Badlands, Savanna Slopes, Shrubland, Red Oasis | Standard animal rules |
| Elephant | 30 | — | 3–5 | creature | Savannas; the same seven Terralith biomes | Standard animal rules |
| Rhinoceros | 24 | — | 3–5 | creature | Savannas; the same seven Terralith biomes | Standard animal rules |
| Maned Wolf | 8 | — | 1–1 | creature | Savannas; the same set minus Red Oasis | Standard animal rules |
| Kangaroo | 25 | — | 3–5 | creature | Badlands and savannas; Terralith Arid Highlands, Brushland, Fractured Savanna, Savanna Badlands, Savanna Slopes, Warped Mesa, White Mesa, Red Oasis; *(BOP Lush Desert)* | Natural ground, light above 8 |
| Emu | 20 | — | 2–5 | creature | Same biomes as the Kangaroo | Natural ground, light above 8 |

### Desert

Five mobs share one biome rule: any biome that is hot **and** dry **and** sandy but not badlands,
plus Terralith Ancient Sands, Desert Canyon, Desert Oasis, Desert Spires, Sandstone Valley, Red Oasis.

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Jerboa | 12 | 1-in-2 | 1–3 | ambient | The shared desert rule | Open sky directly above, and light level 4 or below — so night, in the open |
| Rain Frog | 10 | — | 1–3 | ambient | The shared desert rule | Standing on sand, **and only while it is raining or thundering** |
| Tarantula Hawk | 6 | 1-in-1 | 1–1 | creature | The shared desert rule | On sand with light above 8 |
| Triops | 8 | — | 2–6 | water ambient | The shared desert rule | Standard water-animal rules |
| Rattlesnake | 12 | — | 1–2 | creature | Badlands, **or** hot + dry + sandy; plus the Terralith desert set with Warped Mesa and White Mesa | Natural ground, light above 8 |
| Roadrunner | 9 | 1-in-1 | 2–2 | creature | Same as the Rattlesnake | Natural ground, light above 8 |
| Guster | 35 | — | 1–2 | monster | Hot + dry + sandy biomes that allow default monsters; Terralith Ancient Sands, Desert Canyon, Desert Spires, Ashen Savanna, Desert Caves | Standing on sand, **and only while it is raining or thundering** (`limitGusterSpawnsToWeather`) |

The Tarantula Hawk's predicate also passes anywhere in the Nether, and the Guster's weather gate is
waived there, but neither has a Nether biome in its config, so on this server that branch is
unreachable. Setting `fireproofTarantulaHawk` would still not put them in the Nether without a
config edit.

### Forests and taiga

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Grizzly Bear | 8 | — | 2–3 | creature | All forests except sparse jungle, all taiga, cherry grove; Terralith Alpine Grove, Alpine Highlands, Blooming Valley, Bryce Canyon, Cloud Forest, Forested Highlands, Highlands, Lavender Forest/Valley, Lush Valley, Moonlight Grove/Valley, Sakura Grove/Valley, Shield, Shield Clearing, Snowy Maple Forest, Snowy Shield, Temperate Highlands, Valley Clearing, Wintry Forest, Yosemite Lowlands, Skylands Autumn; *(BOP Redwood Forest, Snowblossom Grove)* | Standard animal rules |
| Blue Jay | 16 | — | 2–4 | creature | Identical rule to the Grizzly Bear | Spawns in leaves; light above 8 |
| Raccoon | 10 | — | 2–4 | creature | Forests, taiga, and plains that are not savanna, plus cherry grove; a similar long Terralith list including Birch Taiga, Cold/Hot/Rocky Shrubland, Steppe, Mirage Isles; *(BOP Redwood Forest, Snowblossom Grove)* | Standard animal rules |
| Crow | 10 | — | 3–5 | creature | Plains that are not savanna, all forests, all taiga, cherry grove; the widest Terralith list of any mob here, including all four Skylands, Mirage Isles and Cloud Forest; *(BOP Snowblossom Grove)* | Light above 8 |
| Skunk | 7 | — | 1–2 | creature | Forests that are not savanna, not cold and not sparse jungle, plus cherry grove; Terralith Birch Taiga, Blooming Valley, Mirage Isles, Lavender Forest/Valley, Moonlight Grove/Valley, Sakura Grove/Valley, Temperate Highlands | Standard animal rules |
| Tasmanian Devil | 10 | — | 1–2 | creature | Same as the Skunk, without cherry grove | Standard animal rules |
| Banana Slug | 14 | — | 2–3 | creature | Old growth pine taiga, old growth spruce taiga, any taiga that is both dense and rare; Terralith Forested Highlands, Shield, Skylands Autumn, Yosemite Lowlands; *(BOP Redwood Forest, Coniferous Forest, Fir Clearing; Autumnity Maple Forest)* | The block below must not be air |
| Potoo | 15 | — | 1–1 | creature | Dark forest only | Spawns in leaves; light above 8 |
| Sugar Glider | 15 | — | 2–4 | creature | Birch forest, old growth birch forest; Terralith White Cliffs | Spawns in leaves; light above 8 |
| Bald Eagle | 15 | — | 2–4 | creature | Biomes that are both hilly and coniferous; grove, windswept forest; Terralith Blooming Plateau, Blooming Valley, Bryce Canyon, Skylands Autumn/Spring/Winter, Lavender Forest/Valley, Moonlight Grove/Valley, Sakura Grove/Valley, Haze Mountain, Temperate Highlands, Alpine Grove; *(BOP Jade Cliffs)* | Light above 8 |

### Plains, highlands and open ground

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Bison | 9 | — | 6–10 | creature | Plains that are neither savanna nor hot; meadow; Terralith Cold Shrubland, Rocky Shrubland, Steppe, Valley Clearing; *(BOP Field, Forested Field, Grassland, Pasture, Prairie)* | Standard animal rules |
| Gelada Monkey | 5 | — | 9–16 | creature | Biomes that are both plains and plateau; Terralith Highlands, Hot Shrubland, Rocky Shrubland, Steppe, Valley Clearing | Standard animal rules |
| Fly | 3 | 1-in-1 | 2–3 | ambient | Any overworld biome | Above y 63, a 1-in-4 coin flip, sky light above 8 **and** block light exactly 0 — daylight, outdoors, no torches — on natural ground |

### Snow and mountains

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Snow Leopard | 18 | — | 1–2 | creature | Any snowy biome; snowy slopes, frozen peaks, jagged peaks; Terralith Frozen Cliffs, Glacial Chasm, Snowy Badlands, Snowy Maple Forest, Emerald Peaks, Rocky Mountains, Scarlet Mountains, Snowy Shield, Skylands Winter | On stone, dirt or grass block, light above 8 |
| Froststalker | 20 | — | 5–7 | creature | Ice spikes, frozen peaks; Terralith Frostfire Caves, Frozen Cliffs, Glacial Chasm, Snowy Badlands, Gravel Desert | On ice or a snow block, or any solid block, with light above 8 |
| Tusklin | 18 | — | 3–5 | creature | Ice spikes; any snowy plains-type biome; Terralith Snowy Badlands, Gravel Desert; *(BOP Snowblossom Grove)* | On a snow block or any solid block, light above 8 |
| Moose | 9 | — | 3–4 | creature | Snowy wasteland, snowy taiga; Terralith Alpine Grove, Snowy Badlands, Snowy Maple Forest, Snowy Shield, Wintry Forest, Wintry Lowlands, Gravel Desert, Skylands Winter; *(BOP Snowy Coniferous Forest, Snowy Fir Clearing, Snowblossom Grove)* | On grass or a snow layer; or on powder snow with light above 8 |
| Sunbird | 5 | 1-in-6 | 1–1 | creature | Any mountain biome; snowy slopes, frozen peaks, jagged peaks; 25 Terralith mountain, cliff, spire, canyon and Skylands biomes | Unrestricted placement, no block or light condition — the 1-in-6 roll is the only extra gate |

### Beaches and coast

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Seagull | 21 | — | 3–6 | creature | Beaches, stony shore; Terralith Basalt Cliffs, Granite Cliffs, White Cliffs, Gravel Beach, Skylands Autumn/Spring; *(BOP Dune Beach)* | Light above 8, and the block below must not be a fluid |
| Seal | 20 | — | 3–8 | creature | Beaches; cold oceans; Terralith Gravel Beach, stony shore; *(BOP Dune Beach)* | In frozen ocean and deep frozen ocean it must stand on **ice**; anywhere else on natural ground, ice, stone or a snow block. Light above 8 either way |
| Lobster | 7 | — | 3–5 | water ambient | Beaches, stony shore; Terralith Gravel Beach | On natural ground, or in water |

### Oceans

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Cachalot Whale | 2 | — | 1–2 | water creature | Cold oceans, lukewarm ocean, deep ocean, deep lukewarm ocean, **Abyssal Chasm** (Alex's Caves) | The water column above must reach open sky and top out within 15 blocks of sea level — it needs somewhere to surface |
| Orca | 2 | 1-in-6 | 3–4 | water creature | Cold oceans | In water, between y 46 and sea level |
| Hammerhead Shark | 8 | 1-in-1 | 2–3 | water creature | Hot oceans | In water, between y 46 and sea level |
| Mantis Shrimp | 15 | — | 1–4 | water creature | Hot oceans; mangrove swamp | The sea floor below must be coral, mud or muddy mangrove roots, below sea level + 1. In biomes tagged `spawns_white_mantis_shrimp` the spawn additionally fails half the time |
| Mimic Octopus | 9 | — | 1–2 | water creature | Hot oceans except deep warm ocean | Sea floor of natural ground, below sea level + 1 |
| Flying Fish | 8 | — | 3–6 | water ambient | Oceans that are neither cold nor hot, excluding deep ocean and deep lukewarm ocean | Standard water-animal rules |
| Blobfish | 30 | — | 2–2 | water ambient | Deep oceans | At or below **y 25** (`blobfishSpawnHeight`), water at the spot and directly above |
| Frilled Shark | 11 | — | 1–1 | water creature | Deep oceans | Water at the spot and directly above |
| Giant Squid | 3 | — | 1–2 | water creature | Deep oceans | Water at the spot and directly above |
| Comb Jelly | 5 | 1-in-1 | 2–3 | water ambient | Frozen ocean, deep frozen ocean, **Abyssal Chasm** (Alex's Caves) | Water at the spot and above, light 4 or below, **and only at night** (between dusk and dawn) |
| Skelewag | 15 | — | 2–3 | monster | Deep oceans that allow default monsters — **but see below** | Water below, difficulty above Peaceful, dark enough, and a 1-in-40 roll |

`restrictSkelewagSpawns` is `true`, so the Skelewag's biome rule never fires; it is added to
**shipwreck** structures instead, with weight 15 and group 1–2.

The Devil's Hole Pupfish (weight 23, group 5–12, water ambient) has "any overworld biome" as its
rule, but `restrictPupfishSpawns` is `true`, which confines it to a **single chunk** within 2000
blocks of world spawn (`pupfishChunkSpawnDistance`). It must additionally be in water, in an
unlit cave, below sea level. In practice it is one hidden pool, matching the real Devils Hole.

### Caves and underground

Six mobs share one biome rule: **any overworld biome except oceans, mushroom biomes and the deep
dark**, plus the thirteen Terralith cave biomes by name (Andesite, Desert, Diorite, Granite, Ice,
Infested, Thermal, Crystal, Frostfire, Mantle, Deep and Tuff Caves). The monster variants of the
rule also require the biome to allow default monsters.

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Cockroach | 4 | — | 5–5 | ambient | The shared cave rule | No sky access, **y 64 or below**, and dark (sky light beaten by a random 0–31 roll, block light 0–7) |
| Cave Centipede | 8 | 1-in-1 | 1–1 | monster | The shared cave rule, monsters allowed | No sky access, **y 0 or below** (`caveCentipedeSpawnHeight`), standard monster darkness rules |
| Murmur | 5 | 1-in-1 | 1–1 | monster | The shared cave rule, monsters allowed | No sky access, **y −30 or below** (`murmurSpawnHeight`) **or** in a biome tagged `spawns_murmurs_ignore_height` — which is cherry grove — plus monster darkness rules |
| Underminer | 50 | 1-in-1 | 1–1 | ambient | The shared cave rule — **but see below** | Below sea level; fails on a coin flip except during Halloween; then light must lose a 0–2 roll |
| Rocky Roller | 60 | — | 1–1 | monster | Dripstone caves; Terralith Andesite, Diorite and Granite Caves | Difficulty above Peaceful, dark enough, standing on dripstone block, pointed dripstone or any solid block |
| Flutter | 13 | — | 2–4 | ambient | Lush caves only | No sky access, standing on a moss block, y 64 or below, dark |
| Skreecher | 10 | 1-in-1 | 1–1 | monster | Biomes tagged `alexsmobs:skreechers_can_spawn_wardens`, which contains exactly **deep dark**, and which must allow default monsters | Difficulty above Peaceful, dark enough, standing on **sculk** |
| Farseer | 30 | — | 1–1 | monster | Any biome that allows default monsters, except mushroom fields — **but see below** | Difficulty above Peaceful, dark enough |

`restrictUnderminerSpawns` is `true`, so the Underminer's biome rule never fires; it is added to
structures tagged `#minecraft:mineshaft` instead, with weight 50 and group 1–1. Approach within
8 blocks (`underminerDisappearDistance`) and it vanishes.

`restrictFarseerSpawns` is `true`, so the Farseer is confined to within **100 blocks of the world
border** (`farseerBorderSpawnDistance`). On a server with the default 29,999,984-block border, this
means it effectively does not spawn.

Skreechers can summon a Warden (`skreechersSummonWarden` is `true`).

### Mushroom and rare biomes

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Mungus | 4 | 1-in-1 | 3–5 | creature | Biomes that are both mushroom and rare — mushroom fields; Terralith Mirage Isles | The block below must be solid |
| Bunfungus | 3 | — | 1–1 | creature | Identical rule to the Mungus | The block below must be solid |

Bunfungus can also be created by feeding Mungal Spores to a rabbit (`bunfungusTransformation`).

Mungus transform terrain. With `mungusBiomeTransformationType` at `2`, they rewrite both blocks
**and the chunk's biome** according to `mungusBiomeMatches` — four mushroom-to-biome mappings
covering red/brown mushroom to mushroom fields and crimson/warped fungus to their Nether forests.

## Nether

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Straddler | 70 | — | 1–3 | monster | Basalt deltas; *(BOP Withered Abyss; Incendium Volcanic Deltas, Withered Forest)* | Standing on a basalt-family block |
| Stradpole | 10 | 1-in-3 | 1–1 | water creature | Same biomes as the Straddler | Spawns in lava: lava at the spot, non-lava below it, air above |
| Soul Vulture | 30 | — | 2–3 | monster | Soul sand valley; *(BYG Warped Desert; Incendium Weeping Valley)* — **but see below** | On soul-fire base blocks or a listed perch, standard monster rules |
| Dropbear | 19 | 1-in-1 | 1–1 | monster | Nether wastes; *(BOP Crystalline Chasm)* | Standard monster rules |
| Crimson Mosquito | 15 | — | 4–4 | monster | Crimson forest; *(BYG Crimson Gardens; BOP Visceral Heap; Incendium Ash Barrens, Infernal Dunes)* | On a solid, spawnable block, dark enough, standard monster rules |
| Warped Toad | 30 | — | 5–5 | creature | Warped forest; *(BYG Crimson Gardens, Warped Desert; Incendium Inverted Forest, Quartz Flats)* | The block below must be lava or solid |
| Bone Serpent | 8 | 1-in-40 | 1–1 | monster | All Nether biomes that allow default monsters | Spawns in lava; there must be air at the top of the lava column above the spawn point |
| Laviathan | 15 | 1-in-1 | 1–1 | creature | All Nether biomes, monsters or not | Spawns in lava; same air-above-lava requirement |

`soulVultureSpawnOnFossil` is `true`, so the Soul Vulture's biome rule never fires; it is added to
**Nether Fossil** structures instead, with weight 30 and group 1–1.

Because Incendium, BYG and Biomes O' Plenty are absent, four of these mobs are effectively locked
to a single vanilla biome each: Straddler and Stradpole to basalt deltas, Crimson Mosquito to
crimson forest, Warped Toad to warped forest, Dropbear to nether wastes.

## The End

| Mob | Weight | Rolls | Group | Category | Biomes | Conditions |
|---|---|---|---|---|---|---|
| Endergrade | 10 | — | 2–6 | creature | Any End biome except the central island | The block below must not be air |
| Spectre | 10 | 1-in-5 | 1–2 | creature | Any End biome except the central island | None — the 1-in-5 roll is the only gate |
| Cosmaw | 9 | — | 1–2 | creature | End biomes except the central island and small end islands | The block below must not be air |
| Enderiophage | 4 | 1-in-2 | 2–2 | creature | End biomes except the central island, end barrens, end highlands and small end islands — i.e. **end midlands only** | None |
| Cosmic Cod | 5 | — | 9–13 | ambient | Any End biome, including the central island | No placement predicate is registered, so only the ground-placement default applies |
| Mimicube | 40 | — | 1–3 | monster | End biomes except the central island, monsters allowed — **but see below** | Standard monster rules |

`mimicubeSpawnInEndCity` is `true`, so the Mimicube's biome rule never fires; it is added to
**End City** structures instead, with weight 40 and group 1–3.

## Mobs with no natural spawn

| Mob | Spawn file | How it is obtained |
|---|---|---|
| Void Worm | `void_worm_spawns.json` — empty biome list | Weight is `0` as well. Summoned with a **Mysterious Worm**, and only in dimensions listed in `voidWormSpawnDimensions`, which is `["minecraft:the_end"]`. 160 max health, `voidWormSummonable` is `true` |
| Warped Mosco | `warped_mosco_spawns.json` — empty biome list | Weight `1`, rolls 1-in-1000, but with no biome the entry never registers. Created when a **Crimson Mosquito attacks a Mungus** (`warpedMoscoTransformation`); `warpedMoscoMobTriggers` can add other trigger mobs and is empty |
| Leafcutter Ant | `leafcutter_anthill_spawns.json` | Not a spawn table. The file gates a **worldgen feature** — the Leafcutter Anthill — into jungle biomes at a 0.5% chance per chunk (`leafcutterAnthillSpawnChance`). Ants come out of the hill, up to 10 per colony (`leafcutterAntColonySize`) |
| Beached Cachalot Whale | `cachalot_whale_beached_spawns.json` | Not a spawn table either. A separate ticking spawner (`BeachedCachalotWhaleSpawner`) tries once per in-game day (`beachedCachalotWhaleSpawnDelay` = 24000 ticks) **during a thunderstorm**, on beaches, stony shore and Terralith Gravel Beach. Each failed attempt raises the chance by 5 percentage points, capped at 100% (`beachedCachalotWhaleSpawnChance`) |
| Sea Bear | none | April Fools only. A player swimming while wearing a **Sombrero** has a per-tick 1-in-245 chance of one appearing 10–32 blocks away, if none is already nearby |
| Bunfungus | has one | Also obtainable by feeding Mungal Spores to a rabbit |
| Multi-part entities | none | Bone Serpent Bones, Anaconda body, Cachalot part, Giant Squid part, Centipede body/tail, Murmur head, Void Worm part are pieces of their parent, not independent spawns |

Four more mobs have a biome rule that is fully overridden by a `restrict…` option and so never
spawn from their biome list: **Mimicube** (End Cities), **Soul Vulture** (Nether Fossils),
**Skelewag** (shipwrecks), **Underminer** (mineshafts). The **Farseer** is not structure-bound but
is pinned to the world border, and the **Devil's Hole Pupfish** to one chunk near spawn.

## The four files that are not `*_spawns.json`

`farseer.json`, `murmur.json`, `skreecher.json` and `underminer.json` have the **same structure** as
every other file — a single `biomes` key holding OR'd condition groups — and are read by the same
Citadel `SpawnBiomeConfig` loader. The only thing different about them is the filename: the four
were added later and their `BiomeConfig` entries were registered as `alexsmobs:farseer` rather than
`alexsmobs:farseer_spawns`. There is no format difference and nothing extra to configure in them.

What they hold:

| File | Biome rule | Note |
|---|---|---|
| `farseer.json` | Any biome that allows default monsters, except mushroom fields | Overridden in practice by `restrictFarseerSpawns` |
| `murmur.json` | The shared cave rule, monsters allowed | The y −30 ceiling comes from `murmurSpawnHeight`, not from this file |
| `skreecher.json` | Biomes tagged `alexsmobs:skreechers_can_spawn_wardens` (deep dark), monsters allowed | The tag is the intended edit point for adding Skreecher biomes, not this file |
| `underminer.json` | The shared cave rule | Overridden in practice by `restrictUnderminerSpawns` |

Editing any of the four does nothing for the Farseer or the Underminer while their `restrict…`
options stay `true`, because those two are attached to structures and world-border distance rather
than to biomes.

## How these rules meet the pack's other worldgen mods

**Terralith 2.5.4** is the mod these configs were written against. Every Terralith biome named above
exists on this server, so the Terralith-specific entries all do real work — most visibly the
thirteen cave biomes, which carry the full cave-mob set, and the Skylands, which appear in eleven
different mobs' lists.

**Alex's Caves 2.0.2** is referenced directly, twice: the Cachalot Whale and the Comb Jelly both
list `alexscaves:abyssal_chasm`. Same author, so this is deliberate compatibility, not a coincidence.
The other five Alex's Caves biomes are not named anywhere in these configs — but the shared cave
rule is tag-based (any overworld biome that is not ocean, mushroom or deep dark), so **Cockroaches,
Cave Centipedes, Murmurs and Underminers can appear in them** unless the biome is tagged out.
Toxic Caves and Candy Cavity are underground overworld biomes and match. Abyssal Chasm is tagged
`is_ocean` and does not.

**Yung's Cave Biomes 2.0.5** and **Darker Depths 2.1.5** add underground biomes that are not named
anywhere in these configs. They reach the cave mobs the same tag-based way: the rule's only positive
requirement is `minecraft:is_overworld`, and its exclusions are ocean, mushroom and deep dark. Any
overworld cave biome from either mod therefore inherits Cockroaches, Cave Centipedes, Murmurs and
Underminers by default. The mobs pinned to a *named* vanilla cave biome — Rocky Roller (dripstone
caves) and Flutter (lush caves) — do **not** follow, because those entries are exact biome ids. If
Yung's replaces the vanilla dripstone or lush cave biome in a region, those two mobs go missing
there. *Not verified against those mods' biome tags — the reasoning is from the Alex's Mobs rule
alone.*

**Yung's Better Mineshafts 4.0.4** matters for the Underminer, which is attached to the structure
tag `#minecraft:mineshaft`. Yung's mineshafts replace the vanilla structure under the same
registry id, so the Underminer follows them.

**Yung's Better Ocean Monuments / shipwrecks** likewise: the Skelewag is attached to
`minecraft:shipwreck`, and the Mimicube to `minecraft:end_city`, both by builtin structure key.

**Absent mods.** Biomes O' Plenty, Incendium, BYG and Autumnity contribute 50 dead entries. The
practical effect is that the Nether mobs have exactly one biome each and several Overworld mobs are
narrower than the config file makes them look — for example the Banana Slug loses four of its
eleven listed biomes, and the Tiger loses two.

## Where the numbers come from

- **Biome rules** — the live `config/alexsmobs/*.json`, pulled from the server, verified
  byte-identical to `DefaultBiomes` in the decompiled jar.
- **Weights and rolls** — the live `config/alexsmobs.toml`, verified identical to the `AMConfig`
  static field initialisers.
- **Group sizes and mob categories** — `AMWorldRegistry.addBiomeSpawns` and
  `AMWorldRegistry.modifyStructure`.
- **Placement types and predicates** — `AMEntityRegistry.registerSpawnPlacements` and each entity's
  `can…Spawn` / `check…SpawnRules` method.
- **Block tags** — `data/alexsmobs/tags/blocks/` in the jar. `#alexsmobs:am_spawns`, the "natural
  ground" tag used by a dozen mobs, is overworld base stone, the dirt family, sand, gravel,
  terracotta and mud.
- SRG method names from the jadx output were cross-read against the clean 1.20 source at
  `AlexModGuy/AlexsMobs` to confirm `isBrightEnoughToSpawn`, `isDarkEnoughToSpawn`, `isSolid`,
  `getRawBrightness`, `FROZEN_OCEAN` and `DEEP_FROZEN_OCEAN`.
