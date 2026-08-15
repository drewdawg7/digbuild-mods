<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Status Effects, Enchantments and Damage Types

Covers the 19 registered mob effects, the 15 registered potions, the 4
enchantments, the 2 custom damage types and the 9 custom death messages.

Sources: `alexsmobs.jar` version **1.22.9** (Forge 47.1.0+, Citadel 2.6.0+),
decompiled with JADX; `assets/alexsmobs/lang/en_us.json` for display names;
`data/alexsmobs/damage_type/*.json` for damage type definitions; the live
server's `/config/alexsmobs.toml` for the config gates called out below.

Where the decompiled code used SRG names, the constants were cross-read against
the clean upstream source (**`AlexModGuy/AlexsMobs`, branch `1.20`**) — that is
how the vanilla base potions in the brewing table below were resolved. The two
sources agree on every value quoted here. `alexsmobs.fandom.com` was not used:
it returns HTTP 402 and is unreachable.

Only three SRG attribute names appear anywhere in the effect package, and all
three are confirmed mappings rather than inferences: `f_22278_` =
`generic.knockback_resistance`, `f_22279_` = `generic.movement_speed`,
`f_22283_` = `generic.attack_speed` (confirmed via `EffectOrcaMight`). No effect
in this package touches `f_22280_` (FLYING_SPEED), the one mapping still
inferred pack-wide, so nothing here rests on it.

## Effect count: 19 effects, 20 files

The `effect/` package holds 20 `.java` files but the lang file has 19
`effect.alexsmobs.*.description` keys. **This is a file-count artifact, not a
registry/lang mismatch** — verified by set-diffing the `register("…")` string
literals in `AMEffectRegistry` against the lang keys, not by counting:

| Check | Result |
|---|---|
| `EFFECT_DEF_REG.register()` literals | 19 |
| `effect.alexsmobs.<id>.description` keys | 19 |
| `alexsmobs.potion.<id>` name keys | 20 |
| Registered effects with no description key | **none** |
| Description keys with no registered effect | **none** |
| Registered effects with no name key | **none** |
| Name keys with no registered effect | `speed_iii` — see below |

Two things reconcile the counts:

- The twentieth **file** is `ProperBrewingRecipe.java`, a Forge `BrewingRecipe`
  subclass that fixes NBT matching for potion inputs. It is not a `MobEffect`.
  Counting the other way there are only 18 effect classes for 19 effects,
  because `EffectSunbird` takes a `boolean curse` and is registered twice, as
  `sunbird_blessing` and `sunbird_curse`.
- The twentieth **name key**, `alexsmobs.potion.speed_iii`, is not an orphan
  either: it names the registered *potion* `alexsmobs:speed_iii`, which applies
  vanilla Speed rather than any custom effect. It is correctly filed in the
  potion-name namespace and has no matching effect by design.

Worth knowing when tracing keys: every effect overrides `getDescriptionId` to
return **`alexsmobs.potion.<id>`**, so the name shown in the HUD comes from that
namespace, while `effect.alexsmobs.<id>.description` supplies only the tooltip
description line. A grep for `effect.alexsmobs.*` will therefore never find an
effect's display name. (17 of those override literals are plain string returns;
`EffectSunbird` supplies the remaining two through a ternary on `curse`, which
is why a naive `return "…"` grep finds 17 rather than 19.)

## Status effects

Category is the `MobEffectCategory` passed to the `MobEffect` constructor. It is
what the game uses to colour the icon and to decide what milk/`clearEffects`
style logic treats as a curse; it is the authoritative buff-vs-debuff answer and
no row below is a guess.

### Reference table

| ID | Display name | Category | Particle colour |
|---|---|---|---|
| `alexsmobs:knockback_resistance` | Knockback Resistance | **buff** (BENEFICIAL) | `#865337` |
| `alexsmobs:lava_vision` | Lava Vision | **buff** (BENEFICIAL) | `#FF6A00` |
| `alexsmobs:sunbird_blessing` | Sunbird's Blessing | **buff** (BENEFICIAL) | `#FFEAB9` |
| `alexsmobs:sunbird_curse` | Sunbird's Curse | **debuff** (HARMFUL) | `#FFEAB9` |
| `alexsmobs:poison_resistance` | Poison Resistance | **buff** (BENEFICIAL) | `#51FFAF` |
| `alexsmobs:oiled` | Oiled | **buff** (BENEFICIAL) | `#FFE89C` |
| `alexsmobs:orcas_might` | Orca's Might | **buff** (BENEFICIAL) | `#4A4A52` |
| `alexsmobs:bug_pheromones` | Bug Pheromones | **buff** (BENEFICIAL) | `#78464B` |
| `alexsmobs:soulsteal` | Soulsteal | **buff** (BENEFICIAL) | `#93FDFF` |
| `alexsmobs:clinging` | Clinging | **buff** (BENEFICIAL) | `#BD4B4B` |
| `alexsmobs:ender_flu` | Ender Flu | **debuff** (HARMFUL) | `#6836AA` |
| `alexsmobs:fear` | Scared Still | **neutral** (NEUTRAL) | `#7474F7` |
| `alexsmobs:tigers_blessing` | Tiger's Blessing | **buff** (BENEFICIAL) | `#FFD75E` |
| `alexsmobs:debilitating_sting` | Debilitating Sting | **neutral** (NEUTRAL) | `#FFF385` |
| `alexsmobs:exsanguination` | Exsanguination | **debuff** (HARMFUL) | `#ED5151` |
| `alexsmobs:earthquake` | Earthquake | **debuff** (HARMFUL) | `#F0E9E1` |
| `alexsmobs:fleet_footed` | Fleet-Footed | **buff** (BENEFICIAL) | `#685441` |
| `alexsmobs:power_down` | Power Outage | **neutral** (NEUTRAL) | `#000000` |
| `alexsmobs:mosquito_repellent` | Mosquito Repellent | **buff** (BENEFICIAL) | `#CC7E70` |

Three effects are NEUTRAL rather than HARMFUL despite being hostile in practice
(**Scared Still**, **Debilitating Sting**, **Power Outage**). That is the value
in the source and it is not a mistake in this document: NEUTRAL means the game
will not treat them as curses for anything that filters on category. Nothing in
this mod reads that distinction, but Apotheosis and Iron's Spells effects that
strip "debuffs" by category will skip these three.

### Mechanics, sources and cures

Attribute modifiers registered through `MobEffect.addAttributeModifier` are
scaled by the game as `amount × (amplifier + 1)`. Amplifier 0 is level I.

**Knockback Resistance** — `+0.5` ADDITION to `generic.knockback_resistance`,
i.e. 50% at level I and 100% at level II. No tick behaviour. Obtained only by
brewing (see potions below); the strong variant is level II. Removed by milk.

**Lava Vision** — no attribute modifiers and an empty tick method; the whole
effect is client-side rendering, which clears lava fog so you can see through
lava. Fog opacity is the config value `lavaVisionOpacity`, **0.65** on this
server (mod default). `shadersCompat` is **false**, so no part of the effect is
disabled. Brewed only. Removed by milk.

**Sunbird's Blessing** — sets fall distance to 0 every tick (no fall damage);
while gliding with an elytra and pitched more than 10° down, adds
`0.02 + (|pitch| / 90) × 0.02` upward velocity per tick; when not gliding, not
on the ground and not sneaking, multiplies downward velocity by 0.6. Amplifier
is not read — level II does nothing extra. Applied automatically for 600 ticks
(30 s) to any player inside a Sunbird's scorch area, rechecked every 100 ticks,
and only if the player has neither Blessing nor Curse already. **Attacking a
Sunbird removes the Blessing and replaces it with the Curse.**

**Sunbird's Curse** — the same class with `curse = true`. Stops elytra flight
outright (`stopFallFlying`) and adds `-0.2` vertical velocity per tick while
airborne, so you cannot glide. Creative players with flight enabled are exempt.
Applied for 600 ticks (30 s) to whatever damages a Sunbird, and for 200 ticks
(10 s) to Phantoms caught in a Sunbird's scorch (which also sets them on fire
for 4 s). Removed by milk; not otherwise curable.

**Poison Resistance** — clears vanilla Poison every tick while active. No
immunity flag, so poison is re-applied and then stripped a tick later rather
than blocked. Brewed only.

**Oiled** — while in water: adds `+0.1` upward velocity per tick unless
sneaking (sneaking zeroes fall distance instead), and damps vertical velocity by
0.9 while airborne. Net effect is floating on the surface. Obtained by drinking
**Fish Oil**, 1200 ticks (60 s) — gated on config `fishOilMeme`, **true** on
this server. Removed by milk.

**Orca's Might** — `+3.0` ADDITION to `generic.attack_speed`, so +3 per level.
Applied for 1000 ticks (50 s) with a 1-in-6 per-tick roll while you are swimming
and an Orca has selected you for its play behaviour. **Attacking an Orca strips
it immediately.**

**Bug Pheromones** — no tick behaviour; handled in a `LivingChangeTargetEvent`
handler that cancels any arthropod mob targeting a holder of the effect, unless
that mob was already hurt by them (`getLastHurtByMob`). Hitting a bug therefore
overrides it for that individual. Brewed only.

**Soulsteal** — no tick behaviour; handled in `LivingDamageEvent`. On dealing
damage, with `level = amplifier + 1`, chance `0.25 + level × 0.25` to heal
`min(damage ÷ 2 × level, 2 + 2 × level)`, and only if you are below max health.
Level I: 50% chance, up to 4 HP. Level II (strong potion): 75% chance, up to
6 HP. Brewed only.

**Clinging** — lets you walk on ceilings. While upside-down (solid block above
and not standing on ground) it zeroes fall distance, adds `+0.3` upward velocity
per tick when not up against a wall and not sneaking, and damps horizontal
velocity to 0.998. Eye height is recomputed to the top of the hitbox while
inverted. The screen-flip is config `clingingFlipEffect`, **false** on this
server, so the camera does not invert here. Brewed only.

**Ender Flu** — the payload lands when the effect **runs out naturally**: the
victim takes `(amplifier + 1) × 10` damage and spawns that many Enderiophages.
Sources: an Enderiophage that still has both eyes latches on and, on a 1-in-3
roll, applies 12000 ticks (10 min) — if you already have it, the amplifier goes
up by one instead, capped at 4 (level V, so 50 damage and 5 phages); and eating
**Cosmic Cod**, 15% chance of 12000 ticks. **Cure: eat a Chorus Fruit — 1-in-3
chance to remove the effect per fruit eaten.** Feeding a Chorus Fruit to an
infected Rabbit has a 40% chance to cure it; feeding one to an Endergrade with
the flu also clears it. Milk works as normal.

**Scared Still** — `-1.0` MULTIPLY_BASE on `generic.movement_speed`, i.e. −100%
per level; movement speed floors at 0, so you cannot walk. Also zeroes any
upward velocity each tick while not in water, and locks FOV modifier to 1.0.
Applied for 100 ticks (5 s) by a Tiger the first time it breaks stealth on a
given target (once per target ID). Removed by milk.

**Tiger's Blessing** — no tick behaviour; two event hooks. Tigers do not select
a holder as a target, and when a holder attacks something that is not a Tiger
and not on their team, every non-baby Tiger within 32 blocks joins in against
that target. Obtained by throwing a **meat food item** to a Tiger (rotten flesh
excluded): 40% for raw or cooked chicken, 30% for raw or cooked porkchop, 10%
for any other meat. Duration 12000 ticks (10 min). **Attacking a Tiger removes
it.**

**Debilitating Sting** — two entirely different behaviours by mob type.
Registers `-1.0` MULTIPLY_BASE on `generic.movement_speed`, but the apply and
remove overrides only run for `MobType.ARTHROPOD`, so **non-arthropods get no
slow**. Non-arthropods instead take 1 generic damage per tick while above half
health, and stop taking it at or below half. Arthropods are paralysed: velocity
zeroed, no-clip and no-gravity while inside a block, forced downward otherwise,
and despawn is denied at amplifier > 0. When an arthropod's timer hits 1 tick it
takes `(amplifier + 1) × 30` damage, and at amplifier > 0 a **baby Tarantula
Hawk** spawns at the surface above it. Applied by a Tarantula Hawk's sting:
**2400 ticks (120 s) on arthropods, 600 ticks (30 s) on everything else**,
amplifier 1 if the hawk is on its breeding-burial behaviour, otherwise 0.
Removed by milk.

**Exsanguination** — ticks once per second (`duration % 20 == 0`) and deals
`min(amplifier + 1, round(remainingDuration ÷ 20))` damage, so the last few
seconds taper. Applied at amplifier 2 (level III) for 60 ticks (3 s), which is
3 + 2 + 1 = 6 damage total, by a **Frilled Shark** bite and by blocking with the
**Shield of the Deep** against an attacker within 4 blocks. Removed by milk.

**Earthquake** — no attribute modifiers and an empty tick method; purely a
client-side camera shake whose intensity reads the remaining duration. Applied
for 20 ticks (1 s), refreshed continuously, to every living entity except other
Rocky Rollers within a 6×8×6 expansion of a rolling **Rocky Roller**'s hitbox.
It deals no damage on its own. Ends a second after you leave the radius.

**Fleet-Footed** — adds a flat `+0.2` ADDITION `generic.movement_speed`
modifier, applied only while you are sprinting and off the ground and removed
about 5 ticks after you land. The bonus is a fixed constant, **not** scaled by
amplifier. Obtained by hand-feeding a **Jerboa** an item it begs for
(`#alexsmobs:jerboa_begs_for`): 30% chance, 12000 ticks (10 min). **Attacking a
Jerboa removes it.**

**Power Outage** — `-1.0` MULTIPLY_BASE on `generic.movement_speed` (−100% per
level, immobilising), zeroes upward velocity out of water, locks FOV modifier to
1.0, and plays a sound on the first tick. Applied by the Grizzly Bear April
Fools behaviour for `2 × (maxMusicBoxTime + 100)` ticks, where `maxMusicBoxTime`
is `100 + rand(130)`, i.e. **400–658 ticks (20–33 s)**. That goal only runs when
`AlexsMobs.isAprilFools()` — calendar date 1 April, or config
`superSecretSettings`, which is **false** on this server. **On any other date
this effect is unobtainable here.** Applied with `showIcon = true` but
`ambient = false, visible = false`.

**Mosquito Repellent** — no tick behaviour; Crimson Mosquitoes will not target a
holder and actively avoid them. Obtained by eating **Mosquito Repellent Stew**:
100% chance, 24000 ticks (20 min). No other source. Removed by milk.

### Potions and brewing

15 potions are registered. All are brewed in an ordinary Brewing Stand and all
convert to splash / lingering / tipped-arrow forms normally.

| Result | Base | Ingredient | Effect applied |
|---|---|---|---|
| Knockback Resistance | Potion of Strength | Bear Fur | `knockback_resistance` 3600t (3:00) |
| Knockback Resistance (long) | Knockback Resistance | Redstone | 9600t (8:00) |
| Knockback Resistance (strong) | Knockback Resistance | Glowstone Dust | 1800t (1:30), amplifier 1 |
| Lava Vision | **Lava Bottle** (not a potion) | Bone Serpent Tooth | `lava_vision` 3600t (3:00) |
| Lava Vision (long) | Lava Vision | Redstone | 9600t (8:00) |
| Poison Bottle | Potion of Poison | Rattlesnake Rattle | — (crafting intermediate) |
| Poison Resistance | Poison Bottle **or** Komodo Spit Bottle | Centipede Leg | `poison_resistance` 3600t (3:00) |
| Poison Resistance (long) | Poison Resistance | Komodo Spit | 9600t (8:00) |
| Swiftness (Speed III) | Potion of Swiftness II | Gazelle Horn | vanilla Speed 2200t (1:50), amplifier 2 |
| Bug Pheromones | Awkward Potion | Cockroach Wing | `bug_pheromones` 3600t (3:00) |
| Bug Pheromones (long) | Bug Pheromones | Redstone | 9600t (8:00) |
| Soulsteal | Awkward Potion | Soul Heart | `soulsteal` 3600t (3:00) |
| Soulsteal (long) | Soulsteal | Redstone | 9600t (8:00) |
| Soulsteal (strong) | Soulsteal | Glowstone Dust | 1800t (1:30), amplifier 1 |
| Clinging | Awkward Potion | Dropbear Claw | `clinging` 3600t (3:00) |
| Clinging (long) | Clinging | Redstone | 9600t (8:00) |

Notes players will hit:

- **Knockback Resistance starts from a Potion of Strength**, not an Awkward
  Potion. There is no other route to it.
- **Lava Vision starts from a Lava Bottle**, an item, not a potion — bottle lava
  directly with a glass bottle (config `lavaBottleEnabled`, **true** here).
- **Speed III is a real Potion of Swiftness with amplifier 2**, brewed from
  Swiftness II plus a Gazelle Horn. Its lang name is just "Potion of Swiftness",
  so it is indistinguishable from vanilla in the tooltip except by the effect
  line.
- No potion exists for the remaining 11 effects.

## Enchantments

All four are registered against a custom `EnchantmentCategory` named
`straddleboard`, whose predicate is `item instanceof ItemStraddleboard`. They
therefore apply to exactly one item: the **Straddleboard**. Slot is MAINHAND.

Every one of `isDiscoverable`, `isTradeable`, `isAllowedOnBooks` and
`canApplyAtEnchantingTable` is ANDed with the config flag
`straddleboardEnchants`, which is **true** on this server — so all four are
obtainable normally: enchanting table, books, villager trades, loot. None is
treasure-only.

None of the four overrides `checkCompatibility`, so the vanilla default applies
and **all four can coexist on one board**.

| ID | Display name | Max level | Rarity | `getMinCost` | `getMaxCost` |
|---|---|---|---|---|---|
| `alexsmobs:straddle_jump` | Straddle Jump | **3** | COMMON | `4 + (L − 1) × 5` → 4 / 9 / 14 | `6 + (L + 1) × 6 + 10` → 28 / 34 / 40 |
| `alexsmobs:lavawax` | Lavawaxed | **1** | UNCOMMON | `6 + (L + 1) × 6` → 18 | `1 + L × 10 + 10` → 21 |
| `alexsmobs:serpentfriend` | Serpent Charmer | **1** | RARE | 18 | 21 |
| `alexsmobs:board_return` | Returning Board | **1** | UNCOMMON | 18 | 21 |

`L` is the enchantment level, 1-indexed. Straddle Jump overrides both cost
methods; the other three share `StraddleEnchantment`'s. Note the odd
consequence of the overrides: **Straddle Jump I has a min cost of 4 but a max
cost of 28**, an unusually wide band, and the three level-1 enchantments sit in
a 3-point band at 18–21.

These are the vanilla-side numbers Apotheosis needs. Apotheosis re-reads
`Rarity`, `getMinCost` and `getMaxCost` when it builds its enchanting tiers, so
the values above are the inputs, not the final in-game costs on this server.

Per-level effects:

- **Straddle Jump** — the board's jump charge multiplier is
  `0.075 + level × 0.05`, and the hop lasts `5 + charge × multiplier` ticks.
  Unenchanted 0.075; I = 0.125, II = 0.175, III = 0.225, so level III is three
  times the unenchanted jump scaling. Only fires while the board is on lava.
- **Lavawaxed** — while a player is riding the board, every 50 ticks (2.5 s)
  grants vanilla **Fire Resistance** for 100 ticks (5 s), `ambient = true`,
  `visible = false`. Level is only checked as > 0. Separately, and independent
  of any enchantment, riding the board extinguishes a burning rider.
- **Serpent Charmer** — sets `shouldSerpentFriend()`, which makes Bone Serpents
  neutral toward the rider. Level only checked as > 0.
- **Returning Board** — when the board entity breaks, it tries
  `player.addItem(board)` back into the rider's inventory and only drops the
  item on the ground if that fails or there is no rider. Level only checked
  as > 0.

## Custom damage types

Two, both defined as data files in `data/alexsmobs/damage_type/`.

| | `alexsmobs:farseer` | `alexsmobs:freddy` |
|---|---|---|
| `exhaustion` | 0.1 | 0.1 |
| `scaling` | `when_caused_by_living_non_player` | `never` |
| `message_id` | `farseer` | `freddy` |
| Death message | randomised, see below | `death.attack.freddy` |

**Neither type is in any damage type tag.** The jar ships no
`data/*/tags/damage_type/` directory at all, so neither is tagged
`bypasses_armor`, `bypasses_shield`, `bypasses_invulnerability`,
`bypasses_effects`, `bypasses_resistance`, `bypasses_enchantments`,
`is_projectile`, `is_explosion`, `is_fire` or `no_knockback`. Practical
consequence for players: **both are ordinary attack damage.** Armour, Protection,
Resistance and shields all apply, and both respect the normal half-second
invulnerability window.

`scaling: when_caused_by_living_non_player` means Farseer damage is scaled up by
world difficulty (both are dealt by mobs, so Farseer scales and Freddy does
not).

### `alexsmobs:farseer`

Dealt by the **Farseer**'s eye beam. The beam charges for 10 ticks, then fires
for `random(0..1) + max(6, target's max health × 0.1)` damage — a health-scaling
attack with a floor of 6, so it hurts high-health targets proportionally harder.
It fires up to 6 times, then goes on an 80–120 tick cooldown.

Its `DamageSource` is a custom subclass, `DamageSourceRandomMessages`, which
rolls `random.nextInt(3)` at death and picks `death.attack.farseer_<0..2>`
(or the `.player` variant when a killer is credited).

### `alexsmobs:freddy`

Dealt by the **Grizzly Bear April Fools** behaviour, the same one that applies
Power Outage — so it is only reachable on 1 April, or with config
`superSecretSettings` enabled, which is **false** on this server. After the
music-box sequence completes the bear leaps and deals:

- with the `keepInventory` gamerule **on**: `maxHealth − 1` damage, then the
  player's health is explicitly set back to 1 (a scripted near-death, not a
  kill);
- with `keepInventory` **off**: `maxHealth + 1000` damage — a guaranteed kill
  that armour and Resistance cannot realistically absorb given the magnitude,
  though it is not tagged to bypass them.

## Death messages

9 `death.*` keys. Both message families come from the two damage types above;
there are no other custom death messages in the mod.

| Key | Text | Cause |
|---|---|---|
| `death.attack.freddy` | Was that the bite of '87? | Killed by the Grizzly Bear April Fools attack. Note this key has **no `%s` placeholder** — the message names nobody — and no `.player` variant. |
| `death.attack.farseer_0` | `%s` was turned to static | Farseer beam, roll 0, no credited killer |
| `death.attack.farseer_1` | `%s` had the channels changed on them | Farseer beam, roll 1 |
| `death.attack.farseer_2` | `%s` was sent to the 4th dimension | Farseer beam, roll 2 |
| `death.attack.farseer_3` | `%s` was disintegrated | **Unreachable** — see below |
| `death.attack.farseer_0.player` | `%s` was turned to static by `%s` | Roll 0, killer credited (`getKillCredit()` non-null) |
| `death.attack.farseer_1.player` | `%s` had the channels changed on them by `%s` | Roll 1, killer credited |
| `death.attack.farseer_2.player` | `%s` was sent to the 4th dimension by `%s` | Roll 2, killer credited |
| `death.attack.farseer_3.player` | `%s` was disintegrated by `%s` | **Unreachable** |

**`farseer_3` cannot appear.** `DamageSourceRandomMessages.getLocalizedDeathMessage`
rolls `nextInt(3)`, which yields 0, 1 or 2 only, so the fourth message and its
`.player` variant are dead lang keys in 1.22.9. Verified in both the decompiled
jar and the clean upstream source, which agree on `nextInt(3)`. Do not publish
"was disintegrated" as an obtainable death message.

## Config gates that change any of the above

Read from the live `/config/alexsmobs.toml`. All five are at their mod defaults.

| Option | Live value | What it gates |
|---|---|---|
| `straddleboardEnchants` | `true` | All four enchantments are discoverable, tradeable, book-applicable and table-applicable |
| `lavaVisionOpacity` | `0.65` | Lava fog opacity under Lava Vision |
| `shadersCompat` | `false` | If true, disables parts of Lava Vision |
| `fishOilMeme` | `true` | Fish Oil grants Oiled |
| `clingingFlipEffect` | `false` | Clinging does not flip the camera here |
| `superSecretSettings` | `false` | Forces April Fools behaviour on; off, so Power Outage and `alexsmobs:freddy` are date-locked to 1 April |
| `lavaBottleEnabled` | `true` | Lava Bottle is obtainable, which is the only base for Lava Vision |

## Not documented / not verified

- No effect declares immunity or a cure item beyond what is listed; standard
  milk-bucket clearing was not re-verified per effect, it is vanilla behaviour
  for every `MobEffect`.
- The `#alexsmobs:jerboa_begs_for` item tag contents were not enumerated here.
- Whether Apotheosis or Iron's Spells alter these four enchantments' costs or
  rarity in practice was not checked against the live enchanting table; only the
  vanilla-side inputs are recorded.
