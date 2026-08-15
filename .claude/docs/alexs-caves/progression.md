<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Progression

The mod gates its biomes behind a deliberate discovery loop. Nothing about it is
random-chance-only: every step has a findable source. This is the single most
important thing to document for players, because without it the biomes are
effectively unfindable.

## The loop

```
Underground Cabin  ──► Cave Tablet  +  Paper
                            │
                            ▼
                   Spelunkery Table  ──► (translation minigame, ×3)
                            │
                            ▼
                       Cave Codex  ──┬──► Cave Compendium entries (knowledge)
                                     │
                                     └──► + Paper ──► Cave Map ──► nearest biome
```

## 1. Find an Underground Cabin

Small structures scattered through ordinary Overworld caves — **not** inside
Alex's Caves biomes (they are explicitly excluded by the
`has_no_underground_cabins` tag). Placement: spacing 10, separation 2, salt 99.

Three ways to locate one, all enabled on this server:

| Source | Chance / availability | Config key |
|---|---|---|
| Abandoned Mineshaft chests contain a map | 15% | `cabin_map_loot_chance` |
| Cartographer villagers sell maps | enabled | `cartographers_sell_cabin_maps` |
| Wandering Traders sell maps | enabled | `wandering_traders_sell_cabin_maps` |

A cabin contains ordinary loot, a **Spelunkery Table**, and a **Cave Tablet**.

## 2. Get a Cave Tablet

Each tablet corresponds to one specific biome. Besides cabins, tablets are
salted into vanilla loot tables — one vanilla structure per biome:

| Biome tablet | Vanilla source | Chance on this server |
|---|---|---|
| Magnetic Caves | Bastion Remnant | 45% |
| Primordial Caves | Suspicious Sand (desert temple archaeology) | 15% |
| Toxic Caves | Jungle Temple | 50% |
| Abyssal Chasm | Underwater Ruins | 40% |
| Forlorn Hollows | Woodland Mansion | 75% |
| Candy Cavity | Witch Hut | 90% |

Vanilla Witch Huts have no chest, so the mod **adds one**
(`loot_chest_in_witch_huts`, enabled) specifically to give the Candy Cavity
tablet a home. That chest's loot table is `alexscaves:chests/witch_hut`.

All six percentages above are the mod defaults and are unmodified on this server.

## 3. Translate it at a Spelunkery Table

Place the tablet and a sheet of paper in the table. Runes on the tablet become
visible; clicking a rune reveals it, and moving the lens over a revealed word
shows its translation. It is a substitution cipher — the same rune means the
same letter across tablets, so players get faster as they learn the alphabet.

**You get five wrong attempts before the tablet is destroyed.** Complete the
translation three times and the tablet + paper become a **Cave Codex**.

The table has a JEI integration (`SpelunkeryTableRecipeCategory`), so the
recipe is discoverable in-game.

## 4. Spend the Codex

A Cave Codex does two things:

- **Unlocks Cave Compendium entries** for its biome — the in-game guidebook.
  On this server `only_one_research_needed` is **false** (the default), so each
  chapter must be unlocked with its own codex rather than one codex unlocking
  everything.
- **Crafts into a Cave Map** with paper. The map points to the nearest instance
  of that biome.

## 5. Cave Maps

Recipe type `alexscaves:cave_map`. When used, the map searches outward for the
biome. Two config knobs govern the search, both stock here:

- `cave_map_search_attempts` = 128000 — how many samples it takes. Higher =
  larger effective radius, slower.
- `cave_map_search_width` = 64 — block width per sample. Higher = faster but may
  skip biomes narrower than the step.

With mean biome width 300 and mean separation 900, a 64-block step will not skip
a normal biome, and 128k attempts comfortably covers the search area. These
defaults are well matched; there is no reason to change them unless players
report maps failing.

## The Cave Compendium

The guidebook (`alexscaves:cave_book`) is a custom book implementation, not
Patchouli, even though Patchouli is present on this server for other mods. Its
content lives in `assets/alexscaves/books/` — a shared structure tree plus
per-language text.

Structure, per biome: **Introduction → Resources → Inhabitants (one entry per
mob) → Utilities**. Each entry is gated behind a `required_progression` key
(e.g. `alexscaves:magnetic_caves_mobs`), which is what the codex unlocks.

Because this text is the mod author's own explanation of each mechanic, it is
the best source for wiki prose — see
`assets/alexscaves/books/en_us/<biome>/*.txt` in the extracted jar.
