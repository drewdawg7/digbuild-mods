<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Configuration

## Summary

The server runs **39 of 39 options at their mod defaults**. Nothing in `alexscaves-general.toml` has been customised.

This was verified mechanically: defaults were read out of the `ACServerConfig`
constructor bytecode (every `define`/`defineInRange` call and its default
argument) and compared against the live TOML pulled from the server. Zero
differences.

The practical consequence: **any Alex's Caves behaviour players report is stock
mod behaviour**, not a server tuning decision. That is a useful thing to know
before debugging.


## Files

| Path | Scope | Notes |
|---|---|---|
| `config/alexscaves-general.toml` | server | all gameplay options, table below |
| `config/alexscaves-client.toml` | client | rendering only, no gameplay effect |
| `config/alexscaves_biome_generation/*.json` | server | per-biome placement, see [biomes.md](biomes.md) |
| `config/citadel-common.toml` | server | dependency library, see [addons.md](addons.md) |

## Every option

Default column is from the jar; server column is live. Identical values throughout,
so the table doubles as a reference for what each knob does.

### `[generation]`

| Option | Value | Meaning |
|---|---|---|
| `cave_biome_mean_width` | `300.0` | Average radius (in blocks) of an Alex's Caves cave biome. |
| `cave_biome_mean_separation` | `900` | Average separation (in blocks) between each Alex's Caves cave biome. |
| `cave_biome_width_randomness` | `0.15` | How irregularly shaped Alex's Caves cave biomes can generate. 0 = all biomes nearly circular. 1 = biomes completely squiggly in shape. |
| `cave_biome_spacing_randomness` | `0.45` | Average spacing in between Alex's Caves cave biomes. 0 = all biomes nearly perfectly equidistant. 1 = biomes completely randomly spread out, sometimes next to eachother. |
| `warn_generation_incompatibility` | `true` | Whether to warn users when a server starts if an incompatible generation mod is detected. |

### `[mob-spawning]`

| Option | Value | Meaning |
|---|---|---|
| `cave_creature_spawn_count_modifier` | `1.75` | Cave Creatures (All dinosaurs, raycats, etc) spawn at this frequency. Their cap is calculated by multiplying this number with the default mob cap for surface animals. |
| `drowned_diving_gear_spawn_chance` | `0.2` | The percent chance that drowned have to spawn wearing diving gear in the Abyssal Chasm. 0 = no diving gear wearing drowned will spawn |

### `[mob-behavior]`

| Option | Value | Meaning |
|---|---|---|
| `pathfinding_threads` | `5` | How many cpu cores big mobs(tremorzilla, atlatitan, grottoceratops etc) should utilize when pathing. Bigger number = less impact on TPS |
| `luxtructosaurus_block_drop_chance` | `0.75` | Chance that blocks destroyed by luxtructosaurus attacks drop themselves, if mob griefing is enabled. |
| `atlatitan_max_block_explosion_resistance` | `10` | The maximum explosion resistance that a block can have to be destroyed by an atlatitan stomp. Set to zero to disable all atlatitan block breaking. |
| `nucleeper_fuse_time` | `300` | How long (in game ticks) it takes for a nucleeper to explode. |
| `devastating_tremorzilla_beam` | `true` | True if the Tremorzilla beam breaks even more blocks. |
| `watcher_possession` | `true` | Whether the Watcher can take control of the camera. |
| `watcher_possession_cooldown` | `300` | How long (in game ticks) between watcher possession attempts. |

### `[block-behavior]`

| Option | Value | Meaning |
|---|---|---|
| `walking_on_magnets` | `true` | True if players wearing boots can walk on any scarlet neodymium surface. |
| `amber_monolith_mean_time` | `32000` | How long (in game ticks) it usually takes for an amber monolith to spawn an animal. |
| `nuclear_furnace_blasting_only` | `true` | True if the Nuclear Furnace only uses 'Blasting' recipes, false to use all smelting recipes. |
| `nuclear_furnace_custom_type` | `false` | True if the Nuclear Furnace should only use recipes using the `alexscaves:nuclear_furnace` recipe type, false to use regular behavior. |

### `[item-behavior]`

| Option | Value | Meaning |
|---|---|---|
| `only_one_research_needed` | `false` | True if one Cave Codex is all that is needed to unlock every Cave Compendium entry. |
| `cave_map_search_attempts` | `128000` | How many attempts to find a biome a cave map engages in when used. Increase this to increase the search radius, or decrease it to make them faster. |
| `cave_map_search_width` | `64` | How wide each search attempt scans for a biome. Increasing this generally makes cave biome maps faster - at the cost of losing fidelity(may skip biomes smaller than this in block width). |
| `nuke_max_block_explosion_resistance` | `1000` | The maximum explosion resistance that a block can have to be destroyed by a nuclear explosion. Set to zero to disable all nuclear explosion block breaking. |
| `nuke_spawn_item_drops` | `true` | Whether some block items are dropped by nuclear explosions. False if all destroyed blocks do not drop items. |
| `nuclear_explosion_size_modifier` | `3.0` | The scale of nuclear bomb destruction. multiply this by 16 to get the radius of a nuclear bomb explosion. |
| `totem_of_possession_works_on_players` | `true` | Whether the Totem of Possession can be applied to players. |
| `darkness_cloak_charge_time` | `1000` | The amount of time (in ticks) it takes to charge up the Cloak of Darkness ability. |
| `darkness_cloak_fly_time` | `200` | The amount of time (in ticks) that players can fly with the Cloak of Darkness ability. |

### `[potion-behavior]`

| Option | Value | Meaning |
|---|---|---|
| `sugar_rush_slows_time` | `true` | Whether the Sugar Rush changes the tick rate of the game in the area of affected players. |

### `[vanilla-changes]`

| Option | Value | Meaning |
|---|---|---|
| `magnetic_tablet_loot_chance` | `0.45` | percent chance of bastion having a cave tablet for magnetic caves in its loot table: |
| `primordial_tablet_loot_chance` | `0.15` | percent chance of suspicious sand having a cave tablet for primordial caves in its loot table: |
| `toxic_tablet_loot_chance` | `0.5` | percent chance of jungle temple having a cave tablet for toxic caves in its loot table: |
| `abyssal_tablet_loot_chance` | `0.4` | percent chance of underwater ruins having a cave tablet for abyssal chasm in its loot table: |
| `forlorn_tablet_loot_chance` | `0.75` | percent chance of mansion having a cave tablet for forlorn hollows in its loot table: |
| `candy_cavity_loot_chance` | `0.9` | percent chance of witch hut chest having a cave tablet for candy cavity in its loot table: |
| `cabin_map_loot_chance` | `0.15` | percent chance of abandoned mineshaft chests having a map to a nearby underground mineshaft in their loot table: |
| `cartographers_sell_cabin_maps` | `true` | Whether the Cartographer Villagers can sell maps to Underground Cabins. |
| `wandering_traders_sell_cabin_maps` | `true` | Whether the Wandering Traders can sell maps to Underground Cabins. |
| `loot_chest_in_witch_huts` | `true` | Whether a loot chest is added to vanilla's witch huts. This is included to provide another place to find candy cavity biome cave tablets. |
| `enchantments_in_loot` | `false` | Whether the Enchantments added by AC appear in vanilla loot tables. |

## Options most worth revisiting

Not recommendations to change — just the ones whose defaults have the biggest
blast radius on a shared server:

| Option | Current | Why it matters |
|---|---|---|
| `nuclear_explosion_size_modifier` | `3.0` | Radius is this ×16 = **48 blocks**. On a survival server that is a very large hole, and `nuke_max_block_explosion_resistance` of 1000 means obsidian does not stop it. |
| `watcher_possession` | `true` | The Watcher can seize the player camera. Players who do not know this reliably report it as a bug or as being hacked. |
| `devastating_tremorzilla_beam` | `true` | Tremorzilla's beam breaks substantially more terrain. |
| `sugar_rush_slows_time` | `true` | Changes the local tick rate around affected players — visible to bystanders and interacts with anything timing-sensitive. |
| `totem_of_possession_works_on_players` | `true` | Players can be possessed by other players. Consider disabling if PvP-adjacent grief becomes an issue; `pvp=true` on this server. |
| `cave_creature_spawn_count_modifier` | `1.75` | 1.75× the surface-animal cap for dinosaurs et al. Combined with `pathfinding_threads=5` this is the main AC contribution to tick cost. |
| `pathfinding_threads` | `5` | Cores used for large-mob pathing. Raise if Atlatitan/Tremorzilla cause TPS dips; it moves work off the main thread. |

## Changing config safely

Alex's Caves config is Forge's standard TOML, read at server start. Edit via the
PebbleHost file manager or the Pterodactyl API and restart. Note that
`config/alexscaves_biome_generation/*.json` affects **worldgen** — changing
continentalness/depth windows or `disabled_completely` will not retroactively alter
already-generated chunks, only new ones, which will produce visible seams.
