<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Biomes

Six biomes, all in `minecraft:overworld`, all placed by Alex's Caves' own
biome source rather than by vanilla noise settings. They are tagged
`#alexscaves:alexs_caves_biomes`, and that tag drives several global rules:

- Ancient Cities never generate inside them (`has_no_ancient_cities_in`)
- Underground Cabins never generate inside them (`has_no_underground_cabins`)
- All vanilla music is overridden inside them (`override_all_vanilla_music_in`)
- Cave Maps draw a border at their edge (`cave_map_border_on`)

## Placement

Each biome has a JSON in `config/alexscaves_biome_generation/` on the server that
controls where it may appear. These are **live server values** — all currently stock.

| Biome | Continentalness | Depth | Temperature | Min distance from spawn | Rarity offset |
|---|---|---|---|---|---|
| Magnetic Caves | 0.6 … 1.0 | 0.2 … 1.0 | — | 400 blocks | 0 |
| Primordial Caves | 0.4 … 1.0 | 0.15 … 1.5 | — | 450 blocks | 1 |
| Toxic Caves | 0.5 … 1.0 | 0.3 … 1.5 | — | 650 blocks | 2 |
| Abyssal Chasm | -0.95 … -0.65 | 0.2 … 1.5 | -1.0 … 0.5 | 400 blocks | 3 |
| Forlorn Hollows | 0.6 … 1.0 | 0.3 … 1.5 | — | 650 blocks | 4 |
| Candy Cavity | 0.5 … 1.0 | 0.15 … 1.5 | — | 500 blocks | 5 |

**Reading these.** `continentalness` is the vanilla climate parameter: negative is
ocean, positive is inland. Abyssal Chasm's window (`-0.95 … -0.65`) is deep ocean only,
which is why it is the one biome you find by diving rather than by digging. `depth`
gates how far below the surface the biome sits. `distance_from_spawn` is a hard
exclusion radius around world spawn. `alexscaves_rarity_offset` biases the draw —
higher means rarer, so Magnetic Caves (0) is the most common and Candy Cavity (5) the
rarest.

Global shape and spacing are controlled by `alexscaves-general.toml` `[generation]`:
mean width 300 blocks, mean separation 900 blocks, width randomness 0.15, spacing
randomness 0.45. See [config.md](config.md).

Each file also has `disabled_completely` (all `false` here) and a `dimensions` list
(all `["minecraft:overworld"]`). Setting `disabled_completely: true` is the supported
way to turn a single biome off server-side.

## Ambience

| Biome | Fog | Sky | Water | Music | Ambient loop | Particle |
|---|---|---|---|---|---|---|
| Magnetic Caves | `#141118` | `#4D4359` | `#606FC1` | `magnetic_caves_music` | `magnetic_caves_ambience` | `magnetic_caves_ambient` |
| Primordial Caves | `#F2D860` | `#F1C973` | `#05A599` | `primordial_caves_music` | `primordial_caves_ambience` | `—` |
| Toxic Caves | `#85FE00` | `#08E501` | `#4B7272` | `toxic_caves_music` | `toxic_caves_ambience` | `fallout` |
| Abyssal Chasm | `#000F2C` | `#7BA4FF` | `#00154B` | `abyssal_chasm_music` | `abyssal_chasm_ambience` | `—` |
| Forlorn Hollows | `#201A15` | `#28211A` | `#5D6A84` | `forlorn_hollows_music` | `forlorn_hollows_ambience` | `falling_guano` |
| Candy Cavity | `#F6C2CF` | `#EF83B3` | `#FA49F8` | `candy_cavity_music` | `candy_cavity_ambience` | `sugar_flake` |

Abyssal Chasm additionally overrides underwater ambience
(`override_underwater_ambience_in`) and plays only the ambient loop underwater
(`only_ambient_loop_underwater`).

## Magnetic Caves

`alexscaves:magnetic_caves`

Dim, iron-grey caverns of Galena studded with Scarlet and Azure Neodymium. Magnetism is the biome's whole mechanic: like poles shove, opposite poles pull, and most of the local mobs are machines that exploit it. Wearing boots lets you walk on scarlet neodymium surfaces (config: `walking_on_magnets`).

### Spawn table

| Category | Mob | Weight | Group size |
|---|---|---|---|
| `ambient` | Notor | 20 | 1–4 |
| `ambient` | Bat *(vanilla)* | 10 | 8–8 |
| `monster` | Magnetron | 80 | 1–1 |
| `monster` | Teletor | 225 | 1–1 |
| `monster` | Boundroid | 350 | 1–2 |
| `monster` | Ferrouslime | 200 | 1–2 |
| `monster` | Spider *(vanilla)* | 100 | 4–4 |
| `monster` | Zombie *(vanilla)* | 95 | 4–4 |
| `monster` | Zombie Villager *(vanilla)* | 5 | 1–1 |
| `monster` | Skeleton *(vanilla)* | 20 | 4–4 |
| `monster` | Creeper *(vanilla)* | 100 | 4–4 |
| `monster` | Slime *(vanilla)* | 100 | 4–4 |
| `monster` | Enderman *(vanilla)* | 10 | 1–4 |
| `monster` | Witch *(vanilla)* | 5 | 1–1 |
| `monster` | Drowned *(vanilla)* | 95 | 4–4 |
| `underground_water_creature` | Glow Squid *(vanilla)* | 10 | 4–6 |

## Primordial Caves

`alexscaves:primordial_caves`

A prehistoric refuge lit from the ceiling by **Ambersol**, a form of amber that illuminates everything beneath it. Because the biome is at daylight brightness, hostile mobs do not spawn here at all — the entire spawn table is `cave_creature` and `water_ambient`. Dinosaurs, Pewen conifers, ancient jungle trees and mud lakes.

### Spawn table

| Category | Mob | Weight | Group size |
|---|---|---|---|
| `water_ambient` | Trilocaris | 15 | 1–2 |
| `cave_creature` | Subterranodon | 6 | 3–5 |
| `cave_creature` | Vallumraptor | 6 | 6–7 |
| `cave_creature` | Grottoceratops | 27 | 2–4 |
| `cave_creature` | Tremorsaurus | 5 | 1–1 |
| `cave_creature` | Relicheirus | 13 | 1–1 |
| `cave_creature` | Frog *(vanilla)* | 7 | 1–2 |
| `cave_creature` | Atlatitan | 10 | 2–3 |

## Toxic Caves

`alexscaves:toxic_caves`

An irradiated industrial wasteland of **Radrock**, cut through by pits of **Acid** that corrode armour and then the wearer. Geothermal vents bubble; sulfur stacks grow under dripping acidic radrock. Ruins hold loot but also radioactive items — picking up a Waste Drum or Uranium Rod inflicts **Irradiated**, which blocks all natural healing and at higher levels deals steady damage.

### Spawn table

| Category | Mob | Weight | Group size |
|---|---|---|---|
| `ambient` | Gammaroach | 55 | 8–8 |
| `ambient` | Bat *(vanilla)* | 10 | 8–8 |
| `cave_creature` | Raycat | 10 | 1–1 |
| `monster` | Brainiac | 160 | 1–2 |
| `monster` | Nucleeper | 45 | 1–1 |
| `monster` | Spider *(vanilla)* | 100 | 4–4 |
| `monster` | Zombie *(vanilla)* | 95 | 4–4 |
| `monster` | Zombie Villager *(vanilla)* | 5 | 1–1 |
| `monster` | Skeleton *(vanilla)* | 100 | 4–4 |
| `monster` | Creeper *(vanilla)* | 100 | 4–4 |
| `monster` | Slime *(vanilla)* | 100 | 4–4 |
| `monster` | Enderman *(vanilla)* | 10 | 1–4 |
| `monster` | Witch *(vanilla)* | 5 | 1–1 |
| `monster` | Drowned *(vanilla)* | 95 | 4–4 |
| `underground_water_creature` | Glow Squid *(vanilla)* | 10 | 4–6 |
| `water_ambient` | Radgill | 10 | 1–3 |

## Abyssal Chasm

`alexscaves:abyssal_chasm`

The only biome that generates **exclusively under surface oceans** — its continentalness window is negative where every other biome's is positive. A crushing deep-sea trench of Abyssmarine and whale fall, home to the Deep Ones, whose faction opinion of you shifts between friendly, neutral, cautious and aggressive based on your actions.

### Spawn table

| Category | Mob | Weight | Group size |
|---|---|---|---|
| `monster` | Deep One Mage | 2 | 1–1 |
| `monster` | Deep One Knight | 4 | 1–1 |
| `monster` | Deep One | 8 | 1–1 |
| `monster` | Spider *(vanilla)* | 100 | 4–4 |
| `monster` | Zombie *(vanilla)* | 95 | 4–4 |
| `monster` | Zombie Villager *(vanilla)* | 5 | 1–1 |
| `monster` | Skeleton *(vanilla)* | 100 | 4–4 |
| `monster` | Creeper *(vanilla)* | 100 | 4–4 |
| `monster` | Slime *(vanilla)* | 100 | 4–4 |
| `monster` | Witch *(vanilla)* | 5 | 1–1 |
| `monster` | Drowned *(vanilla)* | 2 | 1–1 |
| `underground_water_creature` | Glow Squid *(vanilla)* | 100 | 4–6 |
| `underground_water_creature` | Hullbreaker | 20 | 1–1 |
| `water_ambient` | Lanternfish | 100 | 15–20 |
| `water_creature` | Squid *(vanilla)* | 1 | 1–4 |
| `water_creature` | Dolphin *(vanilla)* | 1 | 1–2 |
| `deep_sea_creature` | Tripodfish | 40 | 1–2 |
| `deep_sea_creature` | Sea Pig | 50 | 3–4 |
| `deep_sea_creature` | Gossamer Worm | 20 | 1–1 |

## Forlorn Hollows

`alexscaves:forlorn_hollows`

Canyons drowned in unnatural darkness where almost no light reaches. Millennia of guano have petrified into **Guanostone** and **Coprolith**. Placing light sources here attracts attention rather than providing safety. Underzealots abduct local wildlife and sacrifice it to create the biome's two apex horrors.

### Spawn table

| Category | Mob | Weight | Group size |
|---|---|---|---|
| `ambient` | Gloomoth | 20 | 4–4 |
| `ambient` | Bat *(vanilla)* | 10 | 8–8 |
| `monster` | Underzealot | 100 | 1–1 |
| `monster` | Corrodent | 90 | 3–4 |
| `monster` | Vesper | 60 | 2–3 |

## Candy Cavity

`alexscaves:candy_cavity`

Added in 2.0. A confectionery cave of chocolate, gingerbread and rock candy, created — per the mod's own framing — by Licowitches, with reality-altering properties to match. Sugar Rush locally changes the tick rate of the game (config: `sugar_rush_slows_time`).

### Spawn table

| Category | Mob | Weight | Group size |
|---|---|---|---|
| `monster` | Caniac | 100 | 1–1 |
| `monster` | Gumbeeper | 100 | 1–2 |
| `monster` | Gum Worm | 80 | 1–1 |
| `monster` | Caramel Cube | 40 | 2–3 |
| `water_ambient` | Sweetish Fish | 10 | 1–3 |
| `cave_creature` | Candicorn | 100 | 4–6 |
| `cave_creature` | Gummy Bear | 100 | 1–3 |

## Custom spawn categories

Alex's Caves registers two of its own `MobCategory`s:

- **`alexscaves:cave_creature`** — dinosaurs, Raycats, Candicorns, Gummy Bears. Its
  cap is the vanilla surface-animal cap multiplied by
  `cave_creature_spawn_count_modifier` (**1.75** on this server, which is the mod default).
- **`alexscaves:deep_sea_creature`** — Tripodfish, Sea Pigs, Gossamer Worms in the
  Abyssal Chasm.

Because these are separate categories, they do not compete with the vanilla monster or
creature caps — which is why Primordial Caves can stay densely populated with dinosaurs.

## A note on the vanilla mobs in these tables

Magnetic, Toxic and Abyssal all include the standard hostile roster (zombies, skeletons,
creepers, spiders, slimes, endermen, witches, drowned) at vanilla-ish weights alongside
their own mobs. Primordial and Candy Cavity do **not** — Primordial because it is lit to
daylight levels, Candy Cavity because its table is entirely bespoke. Forlorn Hollows
likewise has no vanilla hostiles, only bats.
