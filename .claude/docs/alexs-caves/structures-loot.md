<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Structures & Loot

14 structures. All but one are confined to a single Alex's Caves biome; the
Underground Cabin is the exception and is the entry point to the whole mod.

## Placement

`spacing` / `separation` are in chunks. `raw_generation` structures are carved as part
of terrain shaping (they *are* the landscape feature); `underground_structures` are
placed as buildings afterwards.

| Structure | Biome | Spacing | Separation | Salt | Step |
|---|---|---:|---:|---:|---|
| `abyssal_ruins` | abyssal_chasm | 5 | 3 | 45 | `underground_structures` |
| `acid_pit` | toxic_caves | 6 | 3 | 2 | `underground_structures` |
| `cake_cave` | candy_cavity | 6 | 5 | 3 | `raw_generation` |
| `dino_bowl` | primordial_caves | 4 | 2 | 1 | `raw_generation` |
| `donut_arch` | candy_cavity | 11 | 7 | 22331293834 | `underground_structures` |
| `ferrocave` | magnetic_caves | 6 | 3 | 3 | `raw_generation` |
| `forlorn_bridge` | forlorn_hollows | 8 | 7 | 22 | `underground_structures` |
| `forlorn_canyon` | forlorn_hollows | 6 | 4 | 6 | `raw_generation` |
| `gingerbread_town` | candy_cavity | 13 | 11 | 92463117 | `underground_structures` |
| `licowitch_tower` | candy_cavity | 21 | 16 | 23916271 | `underground_structures` |
| `ocean_trench` | abyssal_chasm | 2 | 1 | 2 | `raw_generation` |
| `soda_bottle` | candy_cavity | 8 | 3 | 11224949 | `underground_structures` |
| `underground_cabin` | has_underground_cabins | 10 | 2 | 99 | `underground_structures` |
| `volcano` | primordial_caves | 14 | 8 | 9129 | `underground_structures` |

> **Salt collision.** `cake_cave` and `ferrocave` both use salt 3, and `ocean_trench`
> and `acid_pit` both use salt 2. StructureEssentials logs a warning about this on
> every boot. It is harmless here — each pair sits in different biomes so they can
> never contend for the same chunk. See [server-notes.md](server-notes.md).

## What each one is

- **`abyssal_ruins`** — Sunken ruins with diving gear and pottery sherds.
- **`acid_pit`** — Toxic Caves acid feature.
- **`cake_cave`** — Candy Cavity terrain feature.
- **`dino_bowl`** — Primordial Caves arena-shaped terrain feature.
- **`donut_arch`** — Candy Cavity terrain feature.
- **`ferrocave`** — Magnetic Caves terrain feature.
- **`forlorn_bridge`** — Spans the Forlorn Hollows canyons.
- **`forlorn_canyon`** — The Forlorn Hollows' defining terrain feature.
- **`gingerbread_town`** — Largest Candy Cavity structure; Gingerbread Men wander through it (`gingerbread_men_wander_through`).
- **`licowitch_tower`** — Candy Cavity boss lair, with a separate secret-room loot table. Generates far from the other Candy Cavity structures.
- **`ocean_trench`** — The Abyssal Chasm's defining terrain feature; ignores stone in frozen oceans (`trench_ignores_stone_in`).
- **`soda_bottle`** — Candy Cavity landmark; source of Purple Soda.
- **`underground_cabin`** — The progression entry point — holds a Spelunkery Table and a Cave Tablet. The only AC structure that generates *outside* AC biomes.
- **`volcano`** — Holds the Volcanic Core that summons the Luxtructosaurus.

## Chest loot

From `data/alexscaves/loot_tables/chests/`. Item counts and weights omitted for
readability — see the JSON for exact rolls.

**`abyssal_ruins`** (17)

> `cave_tablet`, `book`, `gunpowder`, `pearl`, `tripodfish`, `lanternfish`, `muck`, `marine_snow`, `hero_pottery_sherd`, `guardian_pottery_sherd`, `diving_helmet`, `diving_chestplate`, `diving_leggings`, `diving_boots`, `game_controller`, `scrap_metal`, `copper_ingot`

**`caveman_house`** (18)

> `cave_tablet`, `bone`, `bowl`, `limestone_spear`, `charcoal`, `flint`, `amber`, `tough_hide`, `dinosaur_pottery_sherd`, `footprint_pottery_sherd`, `fiddlehead`, `dinosaur_nugget`, `pine_nuts`, `tree_star`, `primitive_club`, `primordial_helmet`, `primordial_tunic`, `primordial_pants`

**`forlorn_ruins`** (10)

> `cave_tablet`, `book`, `bone`, `string`, `moth_ball`, `burrowing_arrow`, `peering_coprolith`, `occult_gem`, `guano`, `dark_tatters`

**`gingerbread_town`** (11)

> `cave_tablet`, `candy_cane`, `gingerbread_crumbs`, `bread`, `cookie`, `peppermint_powder`, `vanilla_ice_cream_scoop`, `chocolate_ice_cream_scoop`, `sweetberry_ice_cream_scoop`, `caramel_apple`, `sprinkles`

**`licowitch_tower`** (18)

> `cave_tablet`, `disc_fragment_tasty`, `candy_cane`, `peppermint_powder`, `gumball_pile`, `purple_soda_bottle`, `caramel_apple`, `sundrop`, `frostmint_spear`, `radiant_essence`, `name_tag`, `cookie`, `vanilla_ice_cream_scoop`, `chocolate_ice_cream_scoop`, `sweetberry_ice_cream_scoop`, `hot_chocolate_bottle`, `purple_soda_bottle_rocket`, `book`

**`licowitch_tower_secret`** (8)

> `cave_tablet`, `candy_cane`, `disc_fragment_tasty`, `radiant_essence`, `diamond`, `gold_ingot`, `alex_meal`, `book`

**`magnetic_ruins`** (18)

> `cave_tablet`, `book`, `iron_ingot`, `iron_boots`, `name_tag`, `azure_neodymium_ingot`, `scarlet_neodymium_ingot`, `raw_azure_neodymium`, `raw_scarlet_neodymium`, `scrap_metal`, `notor_gizmo`, `metal_swarf`, `raw_iron`, `arrow`, `seeking_arrow`, `tnt`, `telecore`, `polarity_armor_trim_smithing_template`

**`toxic_ruins`** (17)

> `cave_tablet`, `bone`, `spelunkie`, `slam`, `green_soylent`, `cinder_brick`, `poisonous_potato`, `rotten_flesh`, `waste_drum`, `music_disc_11`, `uranium_rod`, `radon_bottle`, `cinder_block`, `hazmat_mask`, `hazmat_chestplate`, `hazmat_leggings`, `hazmat_boots`

**`underground_cabin`** (13)

> `paper`, `book`, `torch`, `copper_ingot`, `raw_iron`, `iron_ingot`, `glow_berries`, `cobblestone`, `coal`, `iron_pickaxe`, `stone_pickaxe`, `iron_helmet`, `diamond`

**`underground_cabin_abyssal_chasm`** (2)

> `cave_book`, `cave_tablet`

**`underground_cabin_candy_cavity`** (2)

> `cave_book`, `cave_tablet`

**`underground_cabin_forlorn_hollows`** (2)

> `cave_book`, `cave_tablet`

**`underground_cabin_magnetic_caves`** (2)

> `cave_book`, `cave_tablet`

**`underground_cabin_primordial_caves`** (2)

> `cave_book`, `cave_tablet`

**`underground_cabin_toxic_caves`** (2)

> `cave_book`, `cave_tablet`

**`witch_hut`** (14)

> `brewing_stand`, `fermented_spider_eye`, `book`, `brown_mushroom`, `red_mushroom`, `gunpowder`, `sugar`, `redstone`, `glass_bottle`, `glowstone_dust`, `stick`, `golden_carrot`, `glistering_melon_slice`, `rabbit_foot`

Note the six `underground_cabin_<biome>` tables: each contains exactly a `cave_book`
and a `cave_tablet`. That is the mechanism that guarantees a cabin always yields a
usable tablet, with the biome varying per cabin.

`witch_hut` is the loot table for the chest Alex's Caves *adds* to vanilla witch huts
(`loot_chest_in_witch_huts`). It is mostly brewing ingredients as camouflage; the point
of it is the Candy Cavity cave tablet, which lands at 90%.
