<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Overview

**Alex's Caves** adds six rare, self-contained cave biomes deep under the
Overworld, each with its own terrain, resources, mobs, gear tree and boss. The
biomes are large, far apart, and deliberately hard to stumble into — the mod
ships a translation minigame whose whole purpose is to tell you where one is.

## Versions on this server

| Mod | ID | Version | Role |
|---|---|---|---|
| Alex's Caves | `alexscaves` | 2.0.2 | the mod |
| Citadel | `citadel` | 2.6.3 | **required** library (same author) |
| Alex's Caves Spellbooks | `alexs_caves_spellbooks` | 1.1.2 | add-on (Iron's Spells bridge) |

Authors: Alexthe668, Noonyeyz. License: LGPL.
Issue tracker: <https://github.com/AlexModGuy/AlexsCaves/issues>

## Dependency graph

```
alexscaves 2.0.2
├── citadel        >= 2.6.0   (mandatory, both sides)   ✓ 2.6.3 installed
└── forge          >= 47.1.3  (mandatory)               ✓ 47.4.10 installed

alexs_caves_spellbooks 1.1.2
├── alexscaves     >= 2.0.0   (mandatory)               ✓ 2.0.2 installed
├── irons_spellbooks [1.20.1-3.0.0, 1.20.1-4.0.0)       ✓ 3.16.2 installed
├── forge          >= 47                                ✓
└── minecraft      [1.20.1, 1.21)                       ✓
```

All dependency ranges are satisfied by what is currently installed.

## Scale of the content

Counted from the jar:

| | Count |
|---|---|
| Cave biomes | 6 |
| Structures | 14 |
| Entity types | 44 living mobs (+ projectiles, vehicles, block entities) |
| Blocks (localised) | 351 |
| Items (localised) | 261 |
| Enchantments | 51 |
| Status effects | 8 |
| Damage types | 11 |
| Recipes | 467 |
| Loot tables | 407 |
| Advancements | 146 |

## The six biomes at a glance

| Biome | ID | Signature resource | Boss |
|---|---|---|---|
| Magnetic Caves | `alexscaves:magnetic_caves` | Scarlet/Azure Neodymium, Galena | — |
| Primordial Caves | `alexscaves:primordial_caves` | Amber, Ambersol, Pewen wood | Luxtructosaurus |
| Toxic Caves | `alexscaves:toxic_caves` | Uranium, Sulfur, Radrock | Tremorzilla |
| Abyssal Chasm | `alexscaves:abyssal_chasm` | Abyssmarine, Pearl, Bioluminescence | Hullbreaker |
| Forlorn Hollows | `alexscaves:forlorn_hollows` | Guanostone, Coprolith, Occult Gem | Forsaken |
| Candy Cavity | `alexscaves:candy_cavity` | Chocolate, Gingerbread, Rock Candy | Licowitch |

Candy Cavity is the biome added in 2.0.

## Creative tabs

Seven tabs: one parent (`itemGroup.alexscaves`) plus one per biome. The per-biome
tabs are the mod's own grouping of its content and are reproduced verbatim in
[blocks-items.md](blocks-items.md).

## Client/server split

`alexscaves` registers the network channel `alexscaves:main_channel` and is
required on both sides — clients without it are rejected. The mod ships client
config separately (`alexscaves-client.toml`), which controls rendering-side
things only (screen shake, shaders, first-person animations) and has no
gameplay effect.
