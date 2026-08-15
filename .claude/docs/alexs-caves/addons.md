<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Add-ons & Dependencies

## Alex's Caves Spellbooks (`alexs_caves_spellbooks` 1.1.2)

By cyber_rat. A bridge mod between Alex's Caves and Iron's Spells 'n Spellbooks —
it does not add content to the cave biomes themselves, it makes AC materials usable
in the Iron's Spells progression. Small: 61 files, all rights reserved license.

**Requires both parents.** Version range on Iron's Spells is
`[1.20.1-3.0.0, 1.20.1-4.0.0)`; this server runs 3.16.2, which is in range.

### Spells

| Spell | ID |
|---|---|
| Conjure Grottoceratops | `conjure_grottoceratops` |
| Conjure Vesper | `conjure_vesper` |
| Demonic Howl | `demonic_howl` |

Two of these summon Alex's Caves mobs as spell minions — `summoned_grottoceratops`
and `summoned_vesper` are registered as distinct entity types and tagged into
`irons_spellbooks:summons`.

### Armour

| Item | ID |
|---|---|
| Dread Boots | `dread_robes_boots` |
| Dread Armor | `dread_robes_chestplate` |
| Dread Hood | `dread_robes_helmet` |
| Dread Leggings | `dread_robes_leggings` |
| Elder Vallumraptor Hide | `elder_vallumraptor_hide` |
| Primordial Mage Armor | `primordial_mage_chestplate` |
| Primordial Mage Helmet | `primordial_mage_helmet` |
| Primordial Mage Toga | `primordial_mage_leggings` |
| Vallumraptor Hide | `vallumraptor_hide` |

Two sets: **Primordial Mage** (crafted, from Vallumraptor hides) and **Dread Robes**
(smithing upgrades). Both are GeckoLib-animated armour models.

### Data it overrides

This is the part that matters for debugging, because it silently changes base-mod
behaviour:

- **`data/alexscaves/loot_tables/entities/vallumraptor.json`** — overrides Alex's
  Caves' own (empty) Vallumraptor loot table to add `vallumraptor_hide` and
  `elder_vallumraptor_hide`. If a player asks why the wiki says Vallumraptors drop
  nothing but they got hides, this is why.
- `data/irons_spellbooks/tags/blocks/spectral_hammer_mineable.json` — lets the
  Spectral Hammer spell mine AC blocks.
- `data/irons_spellbooks/tags/entity_types/summons.json` — registers the two new
  summons.

It also ships mixins (`mixins.alexs_caves_spellbooks.json`).

## Citadel (`citadel` 2.6.3)

Alexthe668's shared library — **a hard dependency**, not optional. Alex's Caves
requires `>= 2.6.0`. Citadel provides the animation system, entity property tracking,
and datapack helpers that AC builds on. It is also used by Alex's Mobs and Ice and
Fire, both present on this server.

### Live config (`citadel-common.toml`)

| Option | Value | Meaning |
|---|---|---|
| `Track Entities` | `true` | Tracks entity properties (freezing, stone mobs) server-side. Disabling can reduce lag but breaks features. |
| `Skip Datapack Warnings` | `true` | Suppresses datapack warnings. |
| `chunkGenSpawnModifier` | `1.0` | Multiplier for entities spawned at chunk generation. |
| `April Fools Content` | `true` | Allows April Fools content to display. |

All stock defaults.

> **Note:** the server log shows AllTheLeaks failing to get a VarHandle for
> `CitadelServerData.dataMap`. See [server-notes.md](server-notes.md).

## Sibling mods that are *not* Alex's Caves add-ons

Easy to conflate, all present on this server, none of them extend Alex's Caves:

| Mod | What it actually is |
|---|---|
| `alexsmobs` 1.22.9 | Alex's Mobs — same author, separate mod, surface/overworld creatures |
| `alexsdelight` 1.5 | Farmer's Delight integration for **Alex's Mobs**, not Alex's Caves |

Confirmed by reading each jar's `mods.toml` dependency block: neither declares
`alexscaves` as a dependency.

## Add-ons that exist but are NOT installed

For reference when considering pack additions — Alex's Caves has a moderately active
add-on ecosystem (extra biomes, Tremorzilla tweaks, JEI-style guides). None beyond
Spellbooks are on this server.
