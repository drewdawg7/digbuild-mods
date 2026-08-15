<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Configuration

## Summary

The server runs **249 of 249 options in `config/alexsmobs.toml` at their mod defaults**, and
**90 of 90 spawn-biome JSONs in `config/alexsmobs/` byte-identical to the generated defaults**.
Nothing in this mod has been customised on this server.

This was verified mechanically. Every `define`/`defineInRange`/`defineList` call in the
`CommonConfig` constructor was parsed out of the decompiled jar, each `AMConfig.x` default
reference resolved to its static field initialiser, and the result compared key-by-key against
the live TOML pulled from the server. Two apparent differences resolved to constant folding by
the decompiler and are not differences:

| Option | Code default reads | Actual value | Live |
|---|---|---|---|
| `bananaChance` | `ItemDimensionalCarver.MAX_TIME` | `200` | `200` |
| `mungusBiomeMatches` | `AMConfig.mungusBiomeMatches` | the four-entry list below | identical |

**Zero real deviations from stock.** Any Alex's Mobs behaviour players report is stock mod
behaviour, not a server tuning decision.

## Files

| Path | Scope | Notes |
|---|---|---|
| `config/alexsmobs.toml` | server | all gameplay options, tables below |
| `config/alexsmobs/*_spawns.json` | server | per-mob biome rules, see [spawning.md](spawning.md) |
| `config/alexsmobs/{farseer,murmur,skreecher,underminer}.json` | server | same, four mobs whose files are not named `*_spawns` |
| `config/citadel-common.toml` | server | dependency library that implements the JSON biome-config format |

## `[general]`

57 options. Server value and stock default are identical for every row, so one value column serves both.

| Option | Value | Meaning |
|---|---|---|
| `giveBookOnStartup` | `true` | Whether all players should get an Animal Dictionary when joining the world for the first time. |
| `lavaVisionOpacity` | `0.65` | Lava Opacity for the Lava Vision Potion. |
| `shadersCompat` | `false` | Whether to disable certain aspects of the Lava Vision Potion. Enable if issues with shaders persist. |
| `bananasDropFromLeaves` | `true` | Whether bananas should drop from blocks tagged with #alexsmobs:drops_bananas |
| `bananaChance` | `200` | 1 out of this number chance for leaves to drop a banana when broken. Fortune is automatically factored in |
| `spidersAttackFlies` | `true` | Whether spiders should target fly mobs. |
| `wolvesAttackMoose` | `true` | Whether wolves should target moose mobs. |
| `polarBearsAttackSeals` | `true` | Whether polar bears should target seal mobs. |
| `catsAndFoxesAttackJerboas` | `true` | Whether cats, ocelots and foxes should target jerboa mobs. |
| `dolphinsAttackFlyingFish` | `true` | Whether dolphins should target flying fish mobs. |
| `lavaBottleEnabled` | `true` | Whether lava can be bottled with a right click of a glass bottle. |
| `neutralBoneSerpents` | `false` | Whether bone serpents are neutral or hostile. |
| `mimicubeSpawnInEndCity` | `true` | Whether mimicubes spawns should be restricted solely to the end city structure or to whatever biome is specified in their respective biome config. |
| `mimicreamRepair` | `true` | Whether mimicream can be used to duplicate items. |
| `mimicreamBlacklist` | `["alexsmobs:blood_sprayer", "alexsmobs:hemolymph_blaster"]` | Blacklist for items that mimicream cannot make a copy of. Ex: "minecraft:stone_sword", "alexsmobs:blood_sprayer" |
| `raccoonStealFromChests` | `true` | Whether wild raccoons steal food from chests. |
| `crowsStealCrops` | `true` | Whether wild crows steal crops from farmland. |
| `fishOilMeme` | `true` | Whether fish oil gives players a special levitation effect. |
| `soulVultureSpawnOnFossil` | `true` | Whether soul vulture spawns should be restricted solely to the nether fossil structure or to whatever biome is specified in their respective biome config. |
| `acaciaBlossomsDropFromLeaves` | `true` | Whether acacia blossoms should drop from blocks tagged with #alexsmobs:drops_acacia_blossoms |
| `acaciaBlossomChance` | `130` | 1 out of this number chance for leaves to drop an acacia when broken. Fortune is automatically factored in |
| `wanderingTraderOffers` | `true` | Whether wandering traders offer items like acacia blossoms, mosquito larva, crocodile egg, etc. |
| `mungusBiomeTransformationType` | `2` | 0 = no mungus biome transformation. 1 = mungus changes blocks, but not chunk's biome. 2 = mungus transforms blocks and biome of chunk. |
| `mungusBiomeMatches` | see below | List of all mungus mushrooms, biome transformations and surface blocks. Each is seperated by a \|. Add an entry with a block registry name, biome registry name, and block registry name(for the ground). |
| `limitGusterSpawnsToWeather` | `true` | Whether guster spawns are limited to when it is raining/thundering. |
| `warpedMoscoTransformation` | `true` | Whether Crimson Mosquitoes can transform into Warped Moscos if attacking a Mungus or any listed creature. |
| `warpedMoscoMobTriggers` | `[""]` | List of extra(non mungus) mobs that will trigger a crimson mosquito to become a warped mosquito. Ex: "minecraft:mooshroom", "alexsmobs:warped_toad" |
| `straddleboardEnchants` | `true` | True if straddleboard enchants are enabled. |
| `emuTargetSkeletons` | `true` | Whether emu should target skeletons. |
| `emuPantsDodgeChance` | `0.45` | Percent chance for emu leggings to dodge projectile attacks. |
| `cachalotDestruction` | `true` | Whether cachalots can destroy wood blocks if angry. |
| `cachalotVolume` | `3.0` | Relative volume of cachalot whales compared to other animals. Note that irl they are the loudest animal. Turn this down if you find their clicks annoying. |
| `leafcutterAntFungusGrowChance` | `0.3` | Percent chance for fungus to grow per each leaf a leafcutter ant returns to the colony. |
| `leafcutterAntRepopulateFeedings` | `25` | How many feedings of leaves does a leafcutter colony need in order to regain a worker ant, if below half the max members. |
| `leafcutterAntColonySize` | `10` | Max number of ant entities allowed inside a leafcutter anthill. |
| `leafcutterAntBreakLeavesChance` | `0.2` | Percent chance for leafcutter ants to break leaves blocks when harvesting. Set to zero so that they can not break any blocks. |
| `falconryTeleportsBack` | `false` | Makes eagles teleport back to their owner if they get stuck during controlled flight. Useful for when playing with the Optifine mod, since this mod is the fault of many issues with the falconry system. |
| `fireproofTarantulaHawk` | `false` | Makes Tarantula Hawks fireproof, perfect if you also want these guys to spawn in the nether. |
| `voidWormSpawnDimensions` | `["minecraft:the_end"]` | List of dimensions in which spawning void worms via mysterious worm items is allowed. |
| `voidWormDamageModifier` | `1.0` | All void worm damage is scaled to this. |
| `voidWormMaxHealth` | `160.0` | Max Health of the void worm boss. |
| `voidWormSummonable` | `true` | Whether the void worm boss is summonable or not, via the mysterious worm item. |
| `seagullStealing` | `true` | Whether seagulls should steal food out of players' hotbar slots. |
| `seagullStealingBlacklist` | `[]` | List of items that seagulls cannot take from players. |
| `clingingFlipEffect` | `false` | Whether the Clinging Potion effect should flip the screen. Warning: may cause nausea. |
| `tusklinShoesBarteringChance` | `0.02500000037252903` | Percent chance of getting Pigshoes from Piglin Bartering. Set to zero to disable. |
| `rainbowGlassFidelity` | `16.0` | The visual zoom of the rainbow pattern on the rainbow glass block. Higher number = bigger pattern. |
| `bunfungusTransformation` | `true` | Whether Rabbits can transform into Bunfungus if fed Mungal spores. |
| `addLootToChests` | `true` | True if some Alex's Mobs items should spawn in loot chests. |
| `transmutationBlacklist` | `["minecraft:beacon"]` | List of items that cannot be put in a Transmuting Table. |
| `limitTransmutingToLootTables` | `false` | True if transmutation tables should not have the ability to pick up new items to transmute, and only give options from the loot tables. |
| `transmutingTableExplodes` | `true` | True if transmutation tables can explode when broken. |
| `transmutingExperienceCost` | `3` | The experience, in levels, that each transmutation of a stack takes in the transmuting table. |
| `transmutingWeightAddStep` | `3.0` | The step value multiplied by the log of the stack size when transmuting an item, used to determine its weight for appearing in future transmutation possibilities. Higher number = more likely to appear. |
| `transmutingWeightRemoveStep` | `4.0` | The step value that an item looses when selecting it as the transmutation result. Keep this number higher than the one above for balance reasons. Higher number = less likely to appear after transmuting multiple times. |
| `skreechersSummonWarden` | `true` | True if skreechers can summon a new warden, when applicable. |
| `underminerDisappearDistance` | `8.0` | The distance in blocks that will cause an underminer to dissapear when approached by a player. |

`mungusBiomeMatches` is four `mushroom|biome|ground` triples, stock and unmodified:

```
minecraft:red_mushroom    | minecraft:mushroom_fields | minecraft:mycelium
minecraft:brown_mushroom  | minecraft:mushroom_fields | minecraft:mycelium
minecraft:crimson_fungus  | minecraft:crimson_forest  | minecraft:crimson_nylium
minecraft:warped_fungus   | minecraft:warped_forest   | minecraft:warped_nylium
```

## `[spawning]`

176 options: a spawn weight and a spawn-roll count for each of 88 naturally-spawning mobs.
Server value and stock default are identical for every row.

- **Spawn weight** — added to the pool of other mobs eligible in that biome. Higher = more common;
  `0` disables the spawn entirely. The weight is compared against every other entry in the same
  mob category for that biome, so the number only means something relative to its neighbours.
- **Spawn rolls** — an extra 1-in-N gate applied after the biome and placement checks pass
  (`rollSpawn` in `AMEntityRegistry`: `rolls <= 0 || random.nextInt(rolls) == 0`). `0` means no
  extra gate. Mobs placed by a spawn egg or spawner bypass it.

| Mob | Weight option | Weight | Rolls option | Rolls |
|---|---|---|---|---|
| Alligator Snapping Turtle | `alligatorSnappingTurtleSpawnWeight` | `20` | `alligatorSnappingTurtleSpawnRolls` | `1` |
| Anaconda | `anacondaSpawnWeight` | `12` | `anacondaSpawnRolls` | `0` |
| Anteater | `anteaterSpawnWeight` | `7` | `anteaterSpawnRolls` | `0` |
| Bald Eagle | `baldEagleSpawnWeight` | `15` | `baldEagleSpawnRolls` | `0` |
| Banana Slug | `bananaSlugSpawnWeight` | `14` | `bananaSlugSpawnRolls` | `0` |
| Bison | `bisonSpawnWeight` | `9` | `bisonSpawnRolls` | `0` |
| Blobfish | `blobfishSpawnWeight` | `30` | `blobfishSpawnRolls` | `0` |
| Blue Jay | `blueJaySpawnWeight` | `16` | `blueJaySpawnRolls` | `0` |
| Bone Serpent | `boneSerpentSpawnWeight` | `8` | `boneSeprentSpawnRolls` | `40` |
| Bunfungus | `bunfungusSpawnWeight` | `3` | `bunfungusSpawnRolls` | `0` |
| Cachalot Whale | `cachalotWhaleSpawnWeight` | `2` | `cachalotWhaleSpawnRolls` | `0` |
| Caiman | `caimanSpawnWeight` | `29` | `caimanSpawnRolls` | `0` |
| Capuchin Monkey | `capuchinMonkeySpawnWeight` | `28` | `capuchinMonkeySpawnRolls` | `0` |
| Catfish | `catfishSpawnWeight` | `4` | `catfishSpawnRolls` | `2` |
| Cave Centipede | `caveCentipedeSpawnWeight` | `8` | `caveCentipedeSpawnRolls` | `1` |
| Cockroach | `cockroachSpawnWeight` | `4` | `cockroachSpawnRolls` | `0` |
| Comb Jelly | `combJellySpawnWeight` | `5` | `combJellySpawnRolls` | `1` |
| Cosmaw | `cosmawSpawnWeight` | `9` | `cosmawSpawnRolls` | `0` |
| Cosmic Cod | `cosmicCodSpawnWeight` | `5` | `cosmicCodSpawnRolls` | `0` |
| Crimson Mosquito | `crimsonMosquitoSpawnWeight` | `15` | `crimsonMosquitoSpawnRolls` | `0` |
| Crocodile | `crocodileSpawnWeight` | `20` | `crocSpawnRolls` | `1` |
| Crow | `crowSpawnWeight` | `10` | `crowSpawnRolls` | `0` |
| Devils Hole Pupfish | `devilsHolePupfishSpawnWeight` | `23` | `devilsHolePupfishSpawnRolls` | `0` |
| Dropbear | `dropbearSpawnWeight` | `19` | `dropbearSpawnRolls` | `1` |
| Elephant | `elephantSpawnWeight` | `30` | `elephantSpawnRolls` | `0` |
| Emu | `emuSpawnWeight` | `20` | `emuSpawnRolls` | `0` |
| Endergrade | `endergradeSpawnWeight` | `10` | `endergradeSpawnRolls` | `0` |
| Enderiophage | `enderiophageSpawnWeight` | `4` | `enderiophageSpawnRolls` | `2` |
| Farseer | `farseerSpawnWeight` | `30` | `farseerSpawnRolls` | `0` |
| Flutter | `flutterSpawnWeight` | `13` | `flutterSpawnRolls` | `0` |
| Fly | `flySpawnWeight` | `3` | `flySpawnRolls` | `1` |
| Flying Fish | `flyingFishSpawnWeight` | `8` | `flyingFishSpawnRolls` | `0` |
| Frilled Shark | `frilledSharkSpawnWeight` | `11` | `frilledSharkSpawnRolls` | `0` |
| Froststalker | `froststalkerSpawnWeight` | `20` | `froststalkerSpawnRolls` | `0` |
| Gazelle | `gazelleSpawnWeight` | `40` | `gazelleSpawnRolls` | `0` |
| Gelada Monkey | `geladaMonkeySpawnWeight` | `5` | `geladaMonkeySpawnRolls` | `0` |
| Giant Squid | `giantSquidSpawnWeight` | `3` | `giantSquidSpawnRolls` | `0` |
| Gorilla | `gorillaSpawnWeight` | `25` | `gorillaSpawnRolls` | `0` |
| Grizzly Bear | `grizzlyBearSpawnWeight` | `8` | `grizzlyBearSpawnRolls` | `0` |
| Guster | `gusterSpawnWeight` | `35` | `gusterSpawnRolls` | `0` |
| Hammerhead Shark | `hammerheadSharkSpawnWeight` | `8` | `hammerheadSharkSpawnRolls` | `1` |
| Hummingbird | `hummingbirdSpawnWeight` | `19` | `hummingbirdSpawnRolls` | `1` |
| Jerboa | `jerboaSpawnWeight` | `12` | `jerboaSpawnRolls` | `2` |
| Kangaroo | `kangarooSpawnWeight` | `25` | `kangarooSpawnRolls` | `0` |
| Komodo Dragon | `komodoDragonSpawnWeight` | `16` | `komodoDragonSpawnRolls` | `1` |
| Laviathan | `laviathanSpawnWeight` | `15` | `laviathanSpawnRolls` | `1` |
| Lobster | `lobsterSpawnWeight` | `7` | `lobsterSpawnRolls` | `0` |
| Maned Wolf | `manedWolfSpawnWeight` | `8` | `manedWolfSpawnRolls` | `0` |
| Mantis Shrimp | `mantisShrimpSpawnWeight` | `15` | `mantisShrimpSpawnRolls` | `0` |
| Mimic Octopus | `mimicOctopusSpawnWeight` | `9` | `mimicOctopusSpawnRolls` | `0` |
| Mimicube | `mimicubeSpawnWeight` | `40` | `mimicubeSpawnRolls` | `0` |
| Moose | `mooseSpawnWeight` | `9` | `mooseSpawnRolls` | `0` |
| Mudskipper | `mudskipperSpawnWeight` | `28` | `mudskipperSpawnRolls` | `0` |
| Mungus | `mungusSpawnWeight` | `4` | `mungusSpawnRolls` | `1` |
| Murmur | `murmurSpawnWeight` | `5` | `murmurSpawnRolls` | `1` |
| Orca | `orcaSpawnWeight` | `2` | `orcaSpawnRolls` | `6` |
| Platypus | `platypusSpawnWeight` | `20` | `platypusSpawnRolls` | `0` |
| Potoo | `potooSpawnWeight` | `15` | `potooSpawnRolls` | `0` |
| Raccoon | `raccoonSpawnWeight` | `10` | `raccoonSpawnRolls` | `0` |
| Rain Frog | `rainFrogSpawnWeight` | `10` | `rainFrogSpawnRolls` | `0` |
| Rattlesnake | `rattlesnakeSpawnWeight` | `12` | `rattlesnakeSpawnRolls` | `0` |
| Rhinoceros | `rhinocerosSpawnWeight` | `24` | `rhinocerosSpawnRolls` | `0` |
| Roadrunner | `roadrunnerSpawnWeight` | `9` | `roadrunnerSpawnRolls` | `1` |
| Rocky Roller | `rockyRollerSpawnWeight` | `60` | `rockyRollerSpawnRolls` | `0` |
| Seagull | `seagullSpawnWeight` | `21` | `seagullSpawnRolls` | `0` |
| Seal | `sealSpawnWeight` | `20` | `sealSpawnRolls` | `0` |
| Shoebill | `shoebillSpawnWeight` | `10` | `shoebillSpawnRolls` | `0` |
| Skelewag | `skelewagSpawnWeight` | `15` | `skelewagSpawnRolls` | `0` |
| Skreecher | `skreecherSpawnWeight` | `10` | `skreecherSpawnRolls` | `1` |
| Skunk | `skunkSpawnWeight` | `7` | `skunkSpawnRolls` | `0` |
| Snow Leopard | `snowLeopardSpawnWeight` | `18` | `snowLeopardSpawnRolls` | `0` |
| Soul Vulture | `soulVultureSpawnWeight` | `30` | `soulVultureSpawnRolls` | `0` |
| Spectre | `spectreSpawnWeight` | `10` | `spectreSpawnRolls` | `5` |
| Straddler | `straddlerSpawnWeight` | `70` | `straddlerSpawnRolls` | `0` |
| Stradpole | `stradpoleSpawnWeight` | `10` | `stradpoleSpawnRolls` | `3` |
| Sugar Glider | `sugarGliderSpawnWeight` | `15` | `sugarGliderSpawnRolls` | `0` |
| Sunbird | `sunbirdSpawnWeight` | `5` | `sunbirdSpawnRolls` | `6` |
| Tarantula Hawk | `tarantulaHawkSpawnWeight` | `6` | `tarantulaHawkSpawnRolls` | `1` |
| Tasmanian Devil | `tasmanianDevilSpawnWeight` | `10` | `tasmanianDevilSpawnRolls` | `0` |
| Terrapin | `terrapinSpawnWeight` | `4` | `terrapinSpawnRolls` | `0` |
| Tiger | `tigerSpawnWeight` | `30` | `tigerSpawnRolls` | `0` |
| Toucan | `toucanSpawnWeight` | `23` | `toucanSpawnRolls` | `0` |
| Triops | `triopsSpawnWeight` | `8` | `triopsSpawnRolls` | `0` |
| Tusklin | `tusklinSpawnWeight` | `18` | `tusklinSpawnRolls` | `0` |
| Underminer | `underminerSpawnWeight` | `50` | `underminerSpawnRolls` | `1` |
| Void Worm | `voidWormSpawnWeight` | `0` | `voidWormSpawnRolls` | `0` |
| Warped Mosco | `warpedMoscoSpawnWeight` | `1` | `warpedMoscoSpawnRolls` | `1000` |
| Warped Toad | `warpedToadSpawnWeight` | `30` | `warpedToadSpawnRolls` | `0` |

Two option names are misspelled upstream and are spelled that way in the live file too:
`boneSeprentSpawnRolls` (for the Bone Serpent) and `crocSpawnRolls` (for the Crocodile).

`voidWormSpawnWeight` is `0` by default, which is what makes the Void Worm summon-only.

## `[uniqueSpawning]`

| Option | Value | Meaning |
|---|---|---|
| `caveCentipedeSpawnHeight` | `0` | Maximum world y-level that cave centipedes can spawn at |
| `blobfishSpawnHeight` | `25` | Maximum world y-level that blobfish can spawn at |
| `beachedCachalotWhales` | `true` | Whether to enable beached cachalot whales to spawn on beaches during thunder storms. |
| `beachedCachalotWhaleSpawnChance` | `5` | Percent chance increase for each failed attempt to spawn a beached cachalot whale. Higher value = more spawns. |
| `beachedCachalotWhaleSpawnDelay` | `24000` | Delay (in ticks) between attempts to spawn beached cachalot whales. Default is a single day. Works like wandering traders. |
| `leafcutterAnthillSpawnChance` | `0.004999999888241291` | Percent chance for leafcutter anthills to spawn as world gen in each chunk. Set to zero to disable spawning. |
| `geladaMonkeySpawnRolls` | `0` | Minimum world y-level that gelada monkeys can spawn at |
| `restrictPupfishSpawns` | `true` | Whether to restrict all pupfish spawns to one chunk (similar to real life) or have them only obey their spawn config. |
| `pupfishChunkSpawnDistance` | `2000` | The maximum distance a pupfish spawn chunk is from world spawn(0, 0) in blocks. |
| `restrictSkelewagSpawns` | `true` | Whether to restrict all skelewag spawns to shipwreck structures. |
| `restrictFarseerSpawns` | `true` | Whether to restrict all farseer spawns to near the world border. |
| `restrictUnderminerSpawns` | `true` | Whether to restrict all underminer spawns to abandoned mineshafts. |
| `farseerBorderSpawnDistance` | `100` | The maximum distance a farseer can spawn from the world border. |
| `murmurSpawnHeight` | `-30` | Maximum world y-level that murmur can spawn at |

`geladaMonkeySpawnRolls` lives in this section with the comment "Minimum world y-level that gelada
monkeys can spawn at", which does not match the option. The value is used as a spawn-roll count like
every other `*SpawnRolls`; the comment is an upstream copy-paste error.

## `[dangerZone]`

| Option | Value | Meaning |
|---|---|---|
| `superSecretSettings` | `false` | Its been so long... |
| `pathfindingThreads` | `5` | How many cpu cores some mobs(elephants, leafcutter ants, bison etc) should utilize when pathing. Bigger number = less impact on TPS |

## Options most worth revisiting

Not recommendations to change — the ones whose stock defaults have the biggest blast radius on a
shared server.

| Option | Current | Why it matters |
|---|---|---|
| `raccoonStealFromChests` | `true` | Wild raccoons take food out of unprotected chests. Players read this as griefing. |
| `crowsStealCrops` | `true` | Wild crows pull crops off farmland. Same. |
| `seagullStealing` | `true` | Seagulls take food from the player hotbar, blacklist is empty. |
| `cachalotDestruction` | `true` | Angry cachalot whales break wood blocks — boats and dockside builds. |
| `mungusBiomeTransformationType` | `2` | Mungus rewrite both blocks **and** the chunk biome. Permanent terrain change by a passive mob. |
| `bananasDropFromLeaves` / `acaciaBlossomsDropFromLeaves` | `true` | 1-in-200 and 1-in-130 per leaf block, fortune-scaled. |
| `pathfindingThreads` | `5` | Cores used for large-mob pathing (elephants, leafcutter ants, bison). Raise if these cause TPS dips. |
| `voidWormMaxHealth` / `voidWormDamageModifier` | `160.0` / `1.0` | Boss tuning. Summonable at will with a Mysterious Worm in the End. |
| `transmutingTableExplodes` | `true` | Transmuting Tables explode when broken. |
| `superSecretSettings` | `false` | Undocumented upstream. Leave alone. |

## Changing config safely

Alex's Mobs config is Forge's standard TOML, read at server start; edit through the PebbleHost file
manager or the Pterodactyl API and restart. The per-mob JSONs in `config/alexsmobs/` are regenerated
on start **only when missing** — an existing file is read as-is, so editing one is persistent, and
deleting one restores the stock default. Spawn weights and biome rules affect only new spawn attempts,
not already-loaded entities, so changes take effect without a world reset.
