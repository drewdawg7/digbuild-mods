<!-- Generated from alexscaves-2.0.2.jar + live server config. Provenance: ../README.md -->

# Alex's Caves — Mobs

Stats below are read directly out of `createAttributes()` in the decompiled entity
classes, so they are exact. Blank cells mean the entity does not override that
attribute and inherits the vanilla default for its base class.

Attribute field names were validated against the official wiki's Tremorzilla stat
block (500 health / 10 armor / 30 attack / 100% knockback resistance), which matches
the code constants exactly.

## All mobs by health

| Mob | ID | Biome | HP | Attack | Armor | Speed | Follow | KB resist |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Luxtructosaurus | `luxtructosaurus` | — | 600 | 12 | 20 | 0.325 | 256 | 1 |
| Tremorzilla | `tremorzilla` | — | 500 | 30 | 10 | 0.3 | 128 | 1 |
| Atlatitan | `atlatitan` | Primordial | 400 | 8 |  | 0.325 |  | 1 |
| Hullbreaker | `hullbreaker` | Abyssal | 400 | 16 |  | 0.3 |  |  |
| Forsaken | `forsaken` | — | 250 | 10 |  | 0.25 | 64 | 0.6 |
| Gum Worm | `gum_worm` | Candy | 150 | 9 | 10 | 0.25 | 128 |  |
| Tremorsaurus | `tremorsaurus` | Primordial | 150 | 14 | 8 | 0.2 | 32 | 0.9 |
| Relicheirus | `relicheirus` | Primordial | 120 | 12 |  | 0.2 |  |  |
| Deep One Mage | `deep_one_mage` | Abyssal | 80 | 4 |  | 0.25 |  |  |
| Deep One Knight | `deep_one_knight` | Abyssal | 60 | 5 |  | 0.25 |  |  |
| Grottoceratops | `grottoceratops` | Primordial | 50 | 10 | 8 | 0.2 | 32 | 0.9 |
| Brainiac | `brainiac` | Toxic | 40 | 5 | 8 | 0.25 | 32 |  |
| Licowitch | `licowitch` | — | 40 | 3 |  | 0.25 | 48 |  |
| Nucleeper | `nucleeper` | Toxic | 40 |  | 4 | 0.2 |  |  |
| Caniac | `caniac` | Candy | 38 | 2 |  | 0.25 | 48 |  |
| Gummy Bear | `gummy_bear` | Candy | 36 | 4 |  | 0.25 |  |  |
| Candicorn | `candicorn` | Candy | 30 | 6 |  | 0.25 | 64 |  |
| Deep One | `deep_one` | Abyssal | 30 | 3 |  | 0.25 |  |  |
| Magnetron | `magnetron` | Magnetic | 30 | 2 | 6 | 0.2 | 32 |  |
| Watcher | `watcher` | — | 30 | 4 |  | 0.25 | 256 |  |
| Vallumraptor | `vallumraptor` | Primordial | 28 | 3 |  | 0.2 | 32 |  |
| Raycat | `raycat` | Toxic | 24 | 1 |  | 0.3 |  |  |
| Boundroid | `boundroid` | Magnetic | 20 | 5 | 20 | 0.2 | 32 |  |
| Boundroid Winch | `boundroid_winch` | — | 20 |  |  | 0.2 | 32 |  |
| Mine Guardian | `mine_guardian` | — | 20 | 1 |  | 0.25 |  |  |
| Subterranodon | `subterranodon` | Primordial | 20 | 2 |  | 0.2 | 32 |  |
| Underzealot | `underzealot` | Forlorn | 20 | 4 |  | 0.25 | 20 |  |
| Teletor | `teletor` | Magnetic | 18 | 2 |  | 0.2 | 32 |  |
| Corrodent | `corrodent` | Forlorn | 16 | 3 | 2 | 0.25 |  |  |
| Vesper | `vesper` | Forlorn | 16 | 3 |  | 0.25 | 52 |  |
| Gammaroach | `gammaroach` | Toxic | 14 | 2 |  | 0.4 |  |  |
| Gumbeeper | `gumbeeper` | Candy | 14 | 4 | 4 | 0.2 | 32 |  |
| Ferrouslime | `ferrouslime` | Magnetic | 10 | 2 |  | 0.35 |  |  |
| Gingerbread Man | `gingerbread_man` | — | 10 | 2 |  | 0.45 | 48 |  |
| Gossamer Worm | `gossamer_worm` | Abyssal | 10 |  |  | 0.1 |  |  |
| Trilocaris | `trilocaris` | Primordial | 10 | 1 |  | 0.15 |  |  |
| Radgill | `radgill` | Toxic | 8 |  |  | 0.25 |  |  |
| Sea Pig | `sea_pig` | Abyssal | 8 |  |  | 0.05 |  |  |
| Tripodfish | `tripodfish` | Abyssal | 8 |  |  | 0.3 |  |  |
| Notor | `notor` | Magnetic | 6 |  |  | 0.15 |  |  |
| Caramel Cube | `caramel_cube` | Candy | 4 | 2 |  | 0.25 |  |  |
| Gloomoth | `gloomoth` | Forlorn | 4 |  |  | 0.2 |  |  |
| Sweetish Fish | `sweetish_fish` | Candy | 4 |  |  | 0.25 |  |  |
| Lanternfish | `lanternfish` | Abyssal | 2 |  |  | 0.15 |  |  |

## Drops

From `data/alexscaves/loot_tables/entities/`. Ranges are before Looting.

| Mob | Drops |
|---|---|
| Atlatitan | `dinosaur_chop ×7–9`, `heavy_bone ×5–9` |
| Boundroid | `heavyweight ×0–1`, `chain ×2–3` |
| Brainiac | `green_soylent ×-2–1`, `rotten_flesh ×0–2`, `charred_remnant ×0–1` |
| Candicorn | `sweet_puff ×0–1` |
| Caniac | `candy_cane ×0–2`, `sharpened_candy_cane ×0–1` |
| Caramel Cube | `caramel ×0–2` |
| Corrodent | `corrodent_teeth ×0–1`, `coarse_dirt ×0–2` |
| Deep One | *(none in loot table)* |
| Deep One Knight | *(none in loot table)* |
| Deep One Mage | *(none in loot table)* |
| Ferrouslime | `ferrouslime_ball ×0–1` |
| Forsaken | `pure_darkness ×7–12` |
| Gammaroach | `toxic_paste ×0–3` |
| Gingerbread Man | `gingerbread_crumbs ×0–1` |
| Gloomoth | `moth_dust ×0–2` |
| Gossamer Worm | `bioluminesscence ×0–3` |
| Grottoceratops | `dinosaur_chop ×1–2`, `tough_hide ×0–2` |
| Gum Worm | `sweet_tooth ×2–4` |
| Gumbeeper | `gumball_pile ×0–2`, `gunpowder ×0–1` |
| Gummy Bear | `gelatin_red ×0–3`, `sweetish_fish_red ×0–1` |
| Hullbreaker | `enigmatic_engine`, `immortal_embryo`, `sea_glass_shards ×2–5`, `copper_ingot ×2–8`, `scrap_metal ×2–4` |
| Lanternfish | `lanternfish` |
| Licowitch | `radiant_essence ×0–1`, `sugar_staff`, `vanilla_ice_cream_scoop ×0–1`, `chocolate_ice_cream_scoop ×0–1`, `sweetberry_ice_cream_scoop ×0–1` |
| Luxtructosaurus | `tectonic_shard ×7–11` |
| Magnetron | *(none in loot table)* |
| Mine Guardian | `depth_charge ×0–2` |
| Notor | `notor_gizmo ×0–1` |
| Nucleeper | `fissile_core ×0–1`, `gunpowder ×0–2` |
| Radgill | `radgill` |
| Raycat | `bone ×0–1` |
| Relicheirus | `dinosaur_chop ×1–2`, `heavy_bone ×1–3`, `feather ×1–4` |
| Sea Pig | `sea_pig` |
| Subterranodon | *(none in loot table)* |
| Sweetish Fish | `sweetish_fish_red` |
| Teletor | `raw_azure_neodymium ×1–2`, `raw_scarlet_neodymium ×1–2`, `telecore ×0–1` |
| Tremorsaurus | `dinosaur_chop ×0–2`, `heavy_bone ×2–3` |
| Tremorzilla | `uranium ×20–40`, `uranium_shard ×10–20` |
| Trilocaris | `trilocaris_tail ×0–1` |
| Tripodfish | `tripodfish` |
| Underzealot | `dark_tatters ×0–2`, `desolate_dagger` |
| Vallumraptor | *(none in loot table)* |
| Vesper | `guano ×0–2`, `vesper_wing ×0–1` |
| Watcher | `occult_gem ×0–1`, `dark_tatters ×0–2` |

Six entities have loot tables with no pools — `deep_one`, `deep_one_knight`,
`deep_one_mage`, `magnetron`, `subterranodon`, `vallumraptor`. Their drops (if any)
are handled in code rather than by loot table. Note that the Spellbooks add-on
**overrides** `alexscaves:entities/vallumraptor` to add hide drops — see
[addons.md](addons.md).

## Bosses and summoned mobs

Four of the most dangerous entities never appear in any biome spawn table. This is
worth stating plainly on the wiki, because players otherwise assume they spawn
naturally and avoid the biomes for the wrong reason.

### Tremorzilla — 500 HP, 30 attack

**Not a natural spawn.** Detonate a **Nuclear Bomb** (or Nucleeper) on a placed **Tremorzilla Egg**. The egg's `canHatchAt` is hardcoded `false` so it never hatches on its own, and `NuclearExplosionEntity` special-cases the egg so it is destroyed regardless of blast-resistance limits.

### Luxtructosaurus — 600 HP, 12 attack

**Not a natural spawn.** Throw an **Ominous Catalyst** near a Volcanic Core. The core attracts the item from up to 20 blocks horizontally, and when it reaches the core it is consumed and an *enraged* Luxtructosaurus spawns at the volcano's summit. 24000-tick (20 minute) cooldown per core.

### Forsaken — 250 HP, 10 attack

**Not a natural spawn.** An Underzealot abducts a **Vesper**; on sacrifice the vesper is *converted* into a Forsaken (`VesperEntity` → `ACEntityRegistry.FORSAKEN`).

### Watcher — 30 HP, 4 attack

**Not a natural spawn.** An Underzealot abducts a **Gloomoth**, carries it, and after a countdown the gloomoth is *converted* into a Watcher (`GloomothEntity` → `ACEntityRegistry.WATCHER`).

The official wiki summarises the Forlorn Hollows pair as "Underzealots seeking
sacrifices to spawn Watchers and Forsaken", which is right about the trigger but
vague about the source. The code is specific: the abducted mob is *converted* via
`LivingEntity.convertTo(..)` (with `ForgeEventFactory.onLivingConvert`), so the
Gloomoth/Vesper is consumed and becomes the new entity. Kill the underzealot's
captive, or the underzealot, and you prevent the spawn.

Other non-natural spawns:

- **Licowitch** — Not in the biome spawn table; occupies the Licowitch Tower structure.
- **Mine Guardian** — Not in any biome spawn table; tied to Abyssal Chasm structures.
- **Gingerbread Man** — Spawns from Gingerbread Town structures rather than the biome spawn table.

## Mob mechanics worth documenting

Pulled from the mod's own guidebook text and confirmed against the code:

- **Deep Ones** (Abyssal Chasm) run a faction reputation system. Chat messages
  announce shifts: *"The Deep Ones now regard you as a friend / with neutrality /
  with caution / with aggression"* (`entity.alexscaves.deep_one.reaction_*`).
- **Gloomoths** drop Moth Dust, which can be thrown to scent-mark a target — most
  Forlorn Hollows mobs will then attack it. Crafted into Moth Balls, it keeps
  gloomoths away from placed light sources.
- **Underzealots** drop the Desolate Dagger: low listed damage, but each hit leaves a
  spectral red blade above the target that lands a second, delayed hit.
- **Nucleepers** are creepers with a 300-tick fuse (`nucleeper_fuse_time`) that
  detonate a nuclear blast rather than a normal explosion.
- **Atlatitan** stomps break blocks up to explosion resistance 10
  (`atlatitan_max_block_explosion_resistance`); set to 0 to disable entirely.
- **Luxtructosaurus** attacks break blocks, which drop themselves 75% of the time
  (`luxtructosaurus_block_drop_chance`), and only if `mobGriefing` is on.
- **Tremorzilla's** beam has `devastating_tremorzilla_beam` **enabled** on this
  server (the mod default), meaning the beam breaks noticeably more blocks.
- **Watcher** can take over the player camera — `watcher_possession` is enabled,
  with a 300-tick cooldown between attempts. This is the single most likely
  "is the server broken?" support question in the pack; see
  [server-notes.md](server-notes.md).
- **Amber Monoliths** repopulate nearby animals on roughly a 32000-tick timer
  (`amber_monolith_mean_time`); the species picked depends on what is already
  nearby and its natural rarity.

## Status effects

| Effect | ID |
|---|---|
| Bubbled | `bubbled` |
| Darkness Incarnate | `darkness_incarnate` |
| Deepsight | `deepsight` |
| Irradiated | `irradiated` |
| Magnetizing | `magnetizing` |
| Rage | `rage` |
| Stunned | `stunned` |
| Sugar Rush | `sugar_rush` |

**Irradiated** is the one to explain to players: it stops *all* natural healing
while active, and at higher amplifiers deals continuous damage. It is applied by
carrying radioactive items (Waste Drum, Uranium Rod) as well as by Toxic Caves
hazards. Hazmat armour reduces both it and acid damage.

## Damage types

| Damage type | Exhaustion |
|---|---|
| `alexscaves:acid` | 0.1 |
| `alexscaves:dark_arrow` | 0.3 |
| `alexscaves:desolate_dagger` | 0.3 |
| `alexscaves:forsaken_sonic_boom` | 0.3 |
| `alexscaves:gumball` | 0.3 |
| `alexscaves:intentional_game_design` | 0.3 |
| `alexscaves:nuke` | 0.1 |
| `alexscaves:radiation` | 0.1 |
| `alexscaves:raygun` | 0.3 |
| `alexscaves:spirit_dinosaur` | 0.3 |
| `alexscaves:tremorzilla_beam` | 0.3 |

All eleven use `scaling: never`, so they deal the same damage on every difficulty.
That matters here: this server runs **difficulty=easy**, which reduces vanilla mob
damage but does **not** soften any of these.
