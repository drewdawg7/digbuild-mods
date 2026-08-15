<!-- Generated from alexsmobs-1.22.9.jar + live server config. Provenance: ../README.md -->

# Alex's Mobs — Taming, Breeding, Mounts and Progression

Everything below is read out of the decompiled `alexsmobs-1.22.9.jar` and the
jar's own `data/` and `assets/` trees, cross-checked against
`/config/alexsmobs.toml` on the live server. Where the mod registers something
but never describes it, this doc says so rather than guessing.

## The Animal Dictionary

`alexsmobs:animal_dictionary` is the mod's guidebook and the entry point to its
advancement tree.

**Every player is given one on first join.** `giveBookOnStartup = true` in
`/config/alexsmobs.toml` (the mod default), so nobody has to craft it.

If a player loses it, it is a shapeless recipe (`recipes/animal_dictionary.json`):

| Slot | Ingredient |
|---|---|
| 1 | `minecraft:book` |
| 2 | any item in `#alexsmobs:animal_dictionary_ingredient` |
| 3 | any item in `#forge:dyes/green` |

`#alexsmobs:animal_dictionary_ingredient` holds 17 mob drops: crocodile scute,
bear fur, roadrunner feather, gazelle horn, rattlesnake rattle, komodo spit,
centipede leg, moose antler, raccoon tail, cockroach wing, spiked scute,
straddlite, emu feather, dropbear claw, cachalot whale tooth, capsid, rocky
shell.

### How it reads

- **Right-click holding it** opens the book at its index page.
- **Right-click an Alex's Mobs creature with it** opens that creature's entry
  directly (`ItemAnimalDictionary.interactLivingEntity`). Multi-part mobs are
  folded to their head entry — a Bone Serpent, Cave Centipede, Void Worm,
  Anaconda or Murmur body segment opens the same page as the head.
- Right-clicking a vanilla or other-mod entity does nothing.

### Nothing in it is locked

The book is 106 page definitions under `assets/alexsmobs/book/animal_dictionary/`
(91 of them with English body text in `en_us/`). Unlike the Alex's Caves Cave
Compendium, **no page has an unlock condition** — `GUIAnimalDictionary` extends
Citadel's `GuiBasicBook` with no progression check, and none of the page JSON
carries a gating key. Every entry is readable from the moment the book is in
hand.

### What the player gets from it

- Per-species prose written by the mod author, including the taming and
  breeding items and any mechanic the species has.
- In-book crafting grids: each page can embed the recipes relevant to that
  species (the Bald Eagle page shows the Falconry Glove and Falconry Hood
  grids, for example).
- The `alexsmobs:alexsmobs/root` advancement, which fires on
  `minecraft:consume_item` for the dictionary — i.e. holding right-click on the
  book. All 105 other Alex's Mobs advancements descend from it.

The advancement side of the mod is 106 JSON files in
`data/alexsmobs/advancements/alexsmobs/` and 212 `advancements.*` keys in
`assets/alexsmobs/lang/en_us.json` (a title and a description for each). None of
them unlock anything mechanically; they are a checklist of the mod's content.
Full table in [Advancement reference](#advancement-reference) below.

## Taming

Twenty entity classes extend `TamableAnimal`. Nineteen of them have a taming
mechanism in code, and **eighteen are actually reachable** — the Orca has no
taming path at all, and the Komodo Dragon's is unreachable because its taming
tag ships empty. Both are explained under the table.

Taming methods fall into four shapes:

- **Hand-fed** — right-click the mob with the item. Each feed rolls.
- **Thrown** — drop the item on the ground near the mob (Q). The mob picks it
  up, eats it over a few seconds, then rolls. Hand-feeding these does not work.
- **Counted** — a minimum number of feeds before any roll is possible, plus a
  hard ceiling at which taming is guaranteed.
- **Hatched** — the mob is born tame.

### Taming master table

| Creature | Registry id | Item | Method | Chance from code |
|---|---|---|---|---|
| Bald Eagle | `alexsmobs:bald_eagle` | Fish Oil (`alexsmobs:fish_oil`) | hand-fed | **50%** per feed (`random.nextBoolean()`) |
| Caiman | `alexsmobs:caiman` | — | hatched | born tame from a Caiman Egg |
| Capuchin Monkey | `alexsmobs:capuchin_monkey` | any banana (`#alexsmobs:bananas`) | hand-fed **or** thrown | **20%** per feed (`nextInt(5) == 0`), same odds either way |
| Cosmaw | `alexsmobs:cosmaw` | Cosmic Cod (`alexsmobs:cosmic_cod`) | thrown | **30%** per feed, after ~1.5 s of eating |
| Crocodile | `alexsmobs:crocodile` | — | hatched | born tame from a Crocodile Egg |
| Crow | `alexsmobs:crow` | Pumpkin Seeds | thrown | **30%** per feed, after 3 s of eating |
| Elephant | `alexsmobs:elephant` | Acacia Blossom (`alexsmobs:acacia_blossom`) | thrown | **33%** per feed (`nextInt(3) == 0`) |
| Flutter | `alexsmobs:flutter` | any flower (`#minecraft:flowers`) | hand-fed, **distinct types only** | after 4 distinct flower species: **33%** per feed; guaranteed on the 7th distinct species |
| Gorilla | `alexsmobs:gorilla` | any banana (`#alexsmobs:bananas`) | thrown | **30%** per feed, after 5 s of eating |
| Grizzly Bear | `alexsmobs:grizzly_bear` | Salmon, while honeyed | thrown | **30%** per feed |
| Kangaroo | `alexsmobs:kangaroo` | Carrot | hand-fed, counted | no roll for the first 10 carrots; **50%** per carrot from the 11th; guaranteed on the 16th |
| Komodo Dragon | `alexsmobs:komodo_dragon` | *(tag is empty)* | hand-fed | **not reachable** — see note |
| Mantis Shrimp | `alexsmobs:mantis_shrimp` | Tropical Fish | hand-fed, counted | no roll for the first 10; **17%** per feed from the 11th (`nextInt(6)`); guaranteed on the 31st |
| Mimic Octopus | `alexsmobs:mimic_octopus` | Lobster Tail, raw or cooked | hand-fed, counted, **state-gated** | only rolls while the octopus is in its plain overlay form; no roll for the first 5; **50%** from the 6th; guaranteed on the 9th |
| Mudskipper | `alexsmobs:mudskipper` | Lobster Tail, raw or cooked | hand-fed | **50%** per feed |
| Raccoon | `alexsmobs:raccoon` | any egg (`#forge:eggs`) | thrown, **washed** | **30%**, rolled after the raccoon carries the egg to water and washes it |
| Sugar Glider | `alexsmobs:sugar_glider` | Sweet Berries | hand-fed | **50%** per feed |
| Tarantula Hawk | `alexsmobs:tarantula_hawk` | Spider Eye | hand-fed, counted | no roll for the first 14; **17%** per feed from the 15th; guaranteed on the 26th |
| Warped Toad | `alexsmobs:warped_toad` | Mosquito Larva (`alexsmobs:mosquito_larva`) | hand-fed | **33%** per feed |
| Orca | `alexsmobs:orca` | — | — | **no taming path exists in code** |

Notes on the awkward rows:

- **Grizzly Bear** needs two throws. Throw a honey item first — honeycomb, honey
  block, honeycomb block or honey bottle (`#alexsmobs:grizzly_honey`) — which
  heals it 10 and makes it *honeyed* for **35 seconds**. It will only pick up
  thrown salmon during that window, and only then can the 30% roll happen.
  Outside the window the salmon is ignored.
- **Elephant** only accepts the taming roll if it is **untusked, or a baby**. A
  grown tusked elephant thrown acacia blossoms eats them and stays wild — which
  is why `tame_elephant_tusked` is a challenge advancement: tame it as a calf
  and let it grow tusks.
- **Flutter** counts *distinct* flower item ids, not feeds. Feeding the same
  flower twice does not advance the count, and a non-flower item makes it shake
  its head.
- **Mimic Octopus** must not be mimicking a block or another mob when fed;
  otherwise the feed is consumed and no roll happens. Ink Sac
  (`#alexsmobs:mimic_octopus_toggles_mimic`) toggles mimicry off.
- **Raccoon** taming is not on the feed. The raccoon takes the thrown egg, walks
  to water, washes it, and the 30% roll happens when the wash finishes.
- **Komodo Dragon**: the code requires a *single stack* of 59–74 items from
  `#alexsmobs:komodo_dragon_tameables` (`58 + nextInt(16)`, and the check is
  `size > tameAmount`), consuming the whole stack whether it works or not. That
  tag ships **empty** in the jar, and this server has no world datapack
  overriding it (`/world/datapacks` is empty). As shipped, the Komodo Dragon
  cannot be tamed, and because its breeding item check also requires it to be
  tamed, it cannot be bred by hand either. It still reproduces on its own — see
  Breeding.
- **Orca** extends `TamableAnimal` for the owner and sitting plumbing, but no
  code path anywhere in the jar calls `tame()` or `setOwnerUUID()` on one.
  **Orca's Might** is not a taming reward and does not involve feeding: swim
  (the sprint-swim pose, not just floating) within 16 blocks of an orca that is
  not targeting you, and every tick there is a **1 in 6** chance it grants you
  Orca's Might for **50 seconds**. Attacking the orca strips the effect
  immediately.
- **Crocodile and Caiman** are the only born-tame species. When a
  `crocodile_egg` or `caiman_egg` block hatches, `BlockReptileEgg` tames every
  hatchling to the nearest player **within 20 blocks** and sets it sitting. No
  player nearby means wild babies. Eggs only tick toward hatching when the block
  under them is sand or a crocodile-spawn block, and they hatch fastest around
  dawn.

### What a tamed mob does

All tamed Alex's Mobs creatures accept a **name tag** like any other mob. The
Crocodile handles the name tag explicitly before its own interaction so that
naming it does not also toggle its sitting state.

**Healing.** Feeding a tamed mob its foodstuffs heals it. The amounts, from
`heal()` calls:

| Creature | Heal item | HP restored |
|---|---|---|
| Bald Eagle | any fish (`#minecraft:fishes`) | 10 |
| Caiman | any fish | 5 |
| Capuchin Monkey | eggs, insects, bananas | 5 |
| Cosmaw | cosmic cod | 4 |
| Crocodile | any meat food item | 10 |
| Crow | eggs, sugar, seeds, pumpkin seeds | 4 |
| Elephant | leaves, saplings, crops, bananas, blossoms | 10 |
| Flutter | bone meal | 5 |
| Gorilla | bananas, leaves, sugar cane, apple, bamboo | 5 |
| Grizzly Bear | honey items | 10 |
| Grizzly Bear | salmon, beetroot, bee nest | 4 |
| Kangaroo | any food item | the item's own hunger value |
| Mantis Shrimp | any fish | 5 |
| Mimic Octopus | lobster tail | 5 |
| Mudskipper | insect items | 5 |
| Raccoon | eggs, sugar | 5 |
| Sugar Glider | insect items | 5 |
| Tarantula Hawk | any flower | 5 |
| Warped Toad | insect items | 5 |

`#alexsmobs:insect_items` is Maggot, Mosquito Larva and Leafcutter Ant Pupa.

### The command system

Right-clicking a tamed mob you own, with an empty hand or with an item it does
not want, **cycles its command state**. The new state is printed to the action
bar using the `entity.alexsmobs.all.command_*` lang keys:

| State | Action bar text | Behaviour |
|---|---|---|
| 0 | *"%s is wandering"* | free-roams, does not follow |
| 1 | *"%s is following"* | follows its owner |
| 2 | *"%s is staying"* | sits and stays put (`setInSittingPose(true)`) |

Sixteen of the nineteen tameable species use this. Two of them add a fourth
state with its own lang key:

| Creature | State 3 | Action bar text |
|---|---|---|
| Crow | gathering | *"%s is gathering items"* — picks up nearby dropped items |
| Mantis Shrimp | breaking | *"%s is breaking blocks"* |

The three tameable species **without** a command cycle are the **Crocodile**
(right-click toggles sit/stand only), the **Elephant** and the **Gorilla**.

Newly tamed mobs are not consistent about their starting state: the Bald Eagle,
Cosmaw and Crow are set to *following* the moment they are tamed; the rest start
at *wandering*.

## Breeding

Fifty-six species have a breeding item. Unless a row says otherwise, breeding
is vanilla-standard: feed two adults, they enter love mode, a baby spawns, and
**both parents go on a 5-minute cooldown** (`setAge(6000)`, 6000 ticks) before
they can breed again. Babies grow up over the vanilla 20 minutes.

### Breeding master table

| Creature | Breeding item | Baby |
|---|---|---|
| Alligator Snapping Turtle | Cod | Alligator Snapping Turtle |
| Anaconda | Chicken, Cooked Chicken | Anaconda, inheriting the parent's yellow/green colour |
| Anteater | Leafcutter Ant Pupa | Anteater |
| Bald Eagle | Rotten Flesh | Bald Eagle |
| Banana Slug | Brown Mushroom | Banana Slug, inheriting the parent's variant |
| Bison | Wheat | Bison |
| Blue Jay | insect items | Blue Jay |
| Cachalot Whale | **Wheat** — see note | Cachalot Whale, inheriting albinism |
| Caiman | Raw Catfish, Cooked Catfish | Caiman |
| Capuchin Monkey | insect items — **must be tamed** | Capuchin Monkey, inheriting the parent's variant |
| Cockroach | Sugar | Cockroach, flagged "breaded" |
| Cosmaw | Cosmic Cod — **must be tamed** | Cosmaw |
| Crocodile | Rotten Flesh | Crocodile |
| Crow | Pumpkin Seeds — **must be tamed** | Crow |
| Elephant | Acacia Blossom — **must be tamed** | Elephant; tusked if no tusked elephant is within 15 blocks, otherwise 50/50 |
| Emu | Wheat | Emu, inheriting the parent's variant |
| Endergrade | Chorus Fruit | Endergrade |
| Flutter | Bone Meal — **must be tamed** | Flutter (born tame); also converts 15–24 nearby amethyst blocks to their budding form |
| Fly | Rotten Flesh | Fly, flagged no-despawn |
| Froststalker | Porkchop, Cooked Porkchop | Froststalker |
| Gazelle | Wheat, Acacia Blossom | Gazelle |
| Gelada Monkey | Dead Bush | Gelada Monkey, 50% chance of being a leader |
| Gorilla | any banana — **must be tamed** | Gorilla |
| Grizzly Bear | Salmon — **must be tamed** | Grizzly Bear |
| Hummingbird | any flower | Hummingbird |
| Jerboa | insect items | Jerboa, born befriended |
| Kangaroo | Dead Bush, Grass | Kangaroo |
| Komodo Dragon | Rotten Flesh — **must be tamed**, so unreachable | Komodo Dragon |
| Laviathan | Mosquito Larva | Laviathan |
| Maned Wolf | Rabbit, Cooked Rabbit, Chicken, Cooked Chicken | Maned Wolf |
| Mantis Shrimp | Lobster Tail — **must be tamed** | Mantis Shrimp, random variant of 3 |
| Mimic Octopus | Tropical Fish — **must be tamed** | Mimic Octopus |
| Moose | Dandelion | Moose |
| Mudskipper | insect items, Lobster Tail | Mudskipper |
| Mungus | Mungal Spores | Mungus |
| Orca | Salmon | Orca |
| Platypus | Lobster Tail | Platypus |
| Potoo | insect items | Potoo |
| Raccoon | Bread | Raccoon |
| Rain Frog | insect items | Rain Frog, inheriting variant, born disturbed |
| Rattlesnake | any meat food item | Rattlesnake |
| Rhinoceros | Dead Bush, Grass | Rhinoceros |
| Roadrunner | insect items | Roadrunner |
| Seagull | Cod | Seagull |
| Seal | Lobster Tail, Cooked Lobster Tail | Seal, arctic if the biome is arctic |
| Skunk | Sweet Berries | Skunk |
| Snow Leopard | Moose Ribs, Cooked Moose Ribs | Snow Leopard |
| Sugar Glider | Honeycomb | Sugar Glider |
| Tarantula Hawk | Fermented Spider Eye — **must be tamed** | *no direct baby* — see below |
| Tasmanian Devil | any meat food item except its howling foods | Tasmanian Devil |
| Terrapin | Seagrass | Terrapin |
| Tiger | Acacia Blossom | Tiger; white with 10% / 40% / 80% chance for zero / one / two white parents |
| Toucan | any egg | Toucan, inheriting variant |
| Triops | Carrot | Triops — lays eggs, see below |
| Tusklin | Red Mushroom | Tusklin |
| Warped Toad | Mosquito Larva — **must be tamed** | Warped Toad |

Species with **no** breeding path at all: Enderiophage, Leafcutter Ant, Shoebill,
Spectre and Sunbird all return `null` for their offspring, and Shoebill's food
check returns `false` outright.

### Breeding that is not vanilla

- **Moose** — feeding it a dandelion only works **1 time in 5**; the other four
  times the moose refuses with the "angry" particle effect and the item is not
  consumed. It also has to be a full-grown moose not already in love.
- **Froststalker** — will only enter love mode for a player it accepts as a
  leader, which means a player **wearing the Froststalker Helmet**
  (`alexsmobs:froststalker_helmet`) on their head, and not one that has recently
  hit it. This is why `breed_froststalker` is a challenge advancement and why it
  sits under `froststalker_helmet` in the tree.
- **Komodo Dragon** — reproduces **parthenogenetically**. A single Komodo Dragon
  in love mode with no partner in range stands still for **3 seconds** and then
  spawns **2 or 3** babies by itself. With a partner it also produces 2–3 at
  once rather than one. Either way it then goes on a 10-second slaughter
  cooldown. Since its food check requires it to be tamed and taming is
  unreachable, no player can start this — wild ones do it on their own.
- **Tarantula Hawk** — breeding produces no baby on the spot. The pair sets a
  "bred" flag, hunts down an arthropod, stings it with **Debilitating Sting II**,
  drags it to sand and buries it. When the effect runs out the victim dies and
  **one baby Tarantula Hawk** digs its way out. The sting lasts **2 minutes** on
  arthropods and **30 seconds** on anything else. Both parents still take the
  standard 5-minute cooldown.
- **Triops** — does not use vanilla love mode. Feed a Triops a carrot; it
  becomes willing, finds a partner within 10 blocks, and after mating the pair
  takes a **60–240 second** breeding cooldown. The pregnant Triops then lays a
  `triops_eggs` block rather than spawning a baby directly. Both must be in
  water.
- **Crocodile and Caiman** — breeding lays an egg block, not a baby. The
  `breed_crocodile` advancement's own description warns not to trample the eggs.
  Hatchlings are tame to a nearby player (see Taming).
- **Flutter** — the baby is born already tamed to the parents' owner.

### Befriending without taming

Four species have a relationship that is not `TamableAnimal` taming and carries
none of the command, sit or heal behaviour:

- **Jerboa** — feed it any seed (`#forge:seeds`) or an insect item and it
  becomes **befriended**: it stops fleeing and no longer despawns. Babies bred
  from befriended jerboas are born befriended.
- **Blue Jay** and **Raccoon** — give either one **Glow Berries**
  (`#alexsmobs:blue_jay_teaming_foods` / `_raccoon_teaming_foods`) and it will
  no longer treat you as a threat, and blue jays and raccoons that share a
  bonded player stop fighting each other.
- **Seagull** and **Seal** — accept "offerings" (lobster tails, and any fish
  respectively) that change their disposition without taming them.

## Mounts and transport

Eight things can be ridden. Only three of them need taming first, and only two
need a vanilla saddle.

| Mount | Registry id | How you mount it | Steerable | Item needed | Speed | Traversal |
|---|---|---|---|---|---|---|
| Elephant | `alexsmobs:elephant` | right-click a tamed adult you own | yes, full control | none | movement speed 0.35 walking, **0.65 charging** | ground |
| Grizzly Bear | `alexsmobs:grizzly_bear` | right-click a tamed adult you own without sneaking | yes, full control | none | movement speed 0.25 | ground |
| Komodo Dragon | `alexsmobs:komodo_dragon` | saddle a tamed adult, then right-click | yes, only while saddled | `minecraft:saddle` | 0.23, **doubled to 0.46** while ridden | ground |
| Tusklin | `alexsmobs:tusklin` | saddle any adult, then right-click. No taming | heading only — it always runs forward | `minecraft:saddle` | movement speed 0.30 | ground |
| Endergrade | `alexsmobs:endergrade` | saddle one, then right-click. No taming | only while you hold a Chorus on a Stick | `minecraft:saddle` + `alexsmobs:chorus_on_a_stick` | 0.15 base, ×0.2 on the ground and ×0.8 in the air | **free flight**, no gravity, no fall damage |
| Laviathan | `alexsmobs:laviathan` | fit the straddle saddle to an adult, then right-click. **Up to 4 riders** | only when it wears **both** the straddle helmet and the straddle saddle; the lowest-numbered seat drives | `alexsmobs:straddle_saddle` + `alexsmobs:straddle_helmet` | movement speed 0.30, ×0.75 swimming, ×0.25 on land | **swims in lava**, fire-immune, auto-climbs walls |
| Straddleboard | `alexsmobs:straddleboard` | place the board, right-click it. Sneak to dismount | yes, steers with your look, jumps | `alexsmobs:straddleboard` | thrust 0.115 per unit of input, drag ×0.975 | **surfs on lava only** — gravity is zeroed only over lava |
| Cosmaw | `alexsmobs:cosmaw` | you do not mount it; a tamed Cosmaw catches its owner mid-fall | no | none | movement speed 0.30 | flight; it carries you to a safe spot and drops you |

Details worth knowing:

- **Elephant charge.** Right-click **wheat** while mounted to trigger a charge:
  up to 5 seconds at nearly double speed, then a 10-second cooldown. Contact
  deals 2.4× the elephant's attack damage and flings the target. While ridden,
  the elephant also adopts your attack target with 4 extra blocks of reach.
- **Grizzly Bear.** Sneak-right-click cycles commands; stand up and right-click
  to mount. While ridden it attacks whatever you attack.
- **Komodo Dragon.** Shears remove the saddle and give it back. Because the
  taming tag ships empty (see Taming), no player on this server can reach the
  Komodo Dragon mount without a datapack.
- **Tusklin** bucks you off after **3 seconds**, or **8 seconds** if it is
  wearing `alexsmobs:pigshoes` in its feet slot. Pigshoes also soften the
  launch. Pigshoes come from Piglin bartering at **2.5%**
  (`tusklinShoesBarteringChance`). While ridden and moving it damages nearby
  entities for 4–7.
- **Laviathan.** Sneak-right-click ejects every passenger. It refuses new
  passengers at 4, or while its eyes are submerged. Both the saddle and the
  helmet drop when it dies. Wearing the saddle, it also scoops up small passive
  land mobs that touch it — players are explicitly excluded from that.
- **Straddleboard.** Riding it into a wall **kills you outright** (100 damage)
  and destroys the board. It extinguishes your fire every tick. Jumping only
  works over lava.
- **Cosmaw pickup** triggers when its owner is tamed, not sitting, off the
  ground and has fallen more than 4 blocks. It teleports to you if you are more
  than 100 blocks away or below Y −20.

### Falconry

Hold the **Falconry Glove** (`alexsmobs:falconry_glove`, 4 leather + 1
`alexsmobs:bear_fur`) in either hand and right-click a tamed adult **Bald
Eagle** to perch it on your arm. A **Potoo** perches the same way with no taming
step. Only one bird at a time.

**Left-click** with the glove to launch the bird. It raytraces up to 128 blocks
for a creature; if it finds one it flies out, attacks, and returns to the glove.
With no target it just hops off.

The **Falconry Hood** (`alexsmobs:falconry_hood`, 3 leather + 1
`alexsmobs:roadrunner_feather`) is right-clicked onto the eagle and removed with
shears. Launching a **hooded** eagle hands you first-person control of it:

- It flies to a point 4.5 blocks ahead of your view each tick.
- Ramming a creature deals **5 + up to 3 speed bonus + 0–1** damage, on a
  1.1-second cooldown.
- Past **150 blocks** from you it force-returns for 5 seconds.
- Control ends when you sneak, when you die, or after **10 minutes** of
  continuous flight.
- `falconryTeleportsBack` is **false** on this server (the mod default), so a
  stuck eagle does not teleport home mid-flight.

### Grapple, boost and other movement items

| Item | Recipe | What it does |
|---|---|---|
| `alexsmobs:squid_grapple` | 3 Lost Tentacle + crossbow + 3 copper ingots | Charged like a bow — full power at 1 second of draw. The hook sticks to a block and pulls you toward it while you are more than 2 blocks away, zeroing fall distance. **Up to 4 hooks out at once**; a fifth withdraws the oldest. Repaired with Lost Tentacle |
| `alexsmobs:enderiophage_rocket` | 1 Capsid + 2 iron nuggets + 2 end stone → 3 | A firework. Right-click a block to launch, or right-click **while elytra-flying** for a vanilla-style boost. Flight lasts 0.9–1.6 s. Works in dispensers |
| `alexsmobs:tarantula_hawk_elytra` | — | A chestplate that flies as an elytra. 800 durability, repaired with `alexsmobs:tarantula_hawk_wing_fragment` |
| `alexsmobs:flying_fish_boots` | — | Press jump while swimming near the surface to launch out of the water into a 1.75-second glide |
| `alexsmobs:vine_lasso` | — | Tethers another mob to you. Moves mobs, not the player |

### Riding you, or carrying you off

These are not mounts — the mob is the passenger, or you are its prisoner.

| Creature | What happens |
|---|---|
| Crow | A tamed crow perches on you — up to **2** at once |
| Capuchin Monkey | Sneak-right-click a tamed one to have it ride your shoulder |
| Sugar Glider | Sneak-right-click a tamed one to have it ride you |
| Bald Eagle, Potoo | Perch on the Falconry Glove |
| Crimson Mosquito | Latches onto you to drink blood |
| Enderiophage | Latches onto you |
| Crocodile | Its lunge **grabs** anything narrower than itself that is not blocking or sneaking, holds it 2 blocks in front, and deals 2 damage every 2 seconds |
| Warped Mosco | Its suck attack grabs a target within 4.7 blocks and deals its full attack damage **every 4 ticks** while regenerating itself |
| Tarantula Hawk | Drags off **arthropods only**. Players get stung for 30 seconds of Debilitating Sting but are never carried |

### Straddleboard enchantments

`straddleboardEnchants = true` on this server, so all four are obtainable.

| Enchantment | Rarity | Effect |
|---|---|---|
| `alexsmobs:straddle_jump` | common | Jump strength `0.075 + 0.05 × level`, scaled by how long you charge |
| `alexsmobs:lavawax` | uncommon | Fire Resistance on the rider, refreshed every 2.5 s |
| `alexsmobs:serpentfriend` | rare | Bone Serpents ignore a rider on an enchanted board |
| `alexsmobs:board_return` | uncommon | A destroyed board returns to the last rider's inventory instead of dropping |

</content>

## Progression chains

Alex's Mobs has no tech tree. What it has is a set of independent chains, each
ending in one notable item or creature. Each is given below as the steps in
order, with the advancement ids that mark them.

### Void Worm → Dimensional Carver → Transmutation Table

The mod's longest chain, 10 advancements deep.

1. **Kill an Enderiophage** in the End Midlands. It drops **1 Capsid**
   (`alexsmobs:capsid`), guaranteed, with no conditions. *(`capsid`)*
2. **Kill a Fly** for a Maggot, and **a Crimson Mosquito** for a Mosquito
   Proboscis, then craft **Mosquito Larva** (shapeless, maggot + proboscis).
   *(`crimson_mosquito_larva`)*
3. **Place the capsid** and right-click the Mosquito Larva into it. After
   **6 seconds** it becomes a **Mysterious Worm**. The block above the capsid
   must not be another capsid. *(`mysterious_worm`)*
4. **Drop the Mysterious Worm into the void of the End** and let the item fall
   below **Y −60**. The item is destroyed and a Void Worm spawns at Y 0 above
   you with **25–39 segments**. *(`void_worm_summon`)*
   - Gated by `voidWormSummonable = true` and
     `voidWormSpawnDimensions = ["minecraft:the_end"]`. Max health is
     `voidWormMaxHealth = 160.0` and damage scale `voidWormDamageModifier = 1.0`
     — all stock. It has 4 armour, 256-block follow range and 5 attack damage.
   - The Void Worm never spawns naturally: its spawn weight is 0 and its biome
     list is empty. Summoning is the only source.
5. **Kill the head.** It drops **1 Void Worm Eye** and **2 Void Worm Mandibles**,
   both guaranteed, with no looting or player-kill condition. *(`void_worm_kill`)*
   - Killing a **body segment** instead splits the worm in two: the parent keeps
     `max(segments / 2 − 1, 1)` segments and a second worm spawns with half the
     max health and 0.8× speed. **Split worms drop nothing** — their loot table
     is empty. *(`void_worm_split`)*
6. **Craft the Dimensional Carver**:
   ```
   M E M     M = alexsmobs:void_worm_mandible  ×2
     X       E = alexsmobs:void_worm_eye       ×1
     X       X = #forge:ingots/netherite       ×2
   ```
   It takes **10 seconds** to use and has a **10-second** cooldown, and opens a
   portal to your respawn point and dimension. *(`dimensional_carver`)*
7. **Put the Dimensional Carver in a capsid** for **10 seconds** to get the
   **Shattered Dimensional Carver**, which instead opens a portal up to
   **1,000,000 blocks** in the direction you face, clamped to the world border.
   *(`shattered_dimensional_carver`)*
8. **Meet a Farseer.** They only spawn within **100 blocks of the world border**
   (`restrictFarseerSpawns = true`, `farseerBorderSpawnDistance = 100`), which is
   where the shattered carver puts you. *(`farseer`)*
9. **Kill a Farseer** for a Farseer Arm (0–1, +0–1 per Looting level), and craft
   the **Transmutation Table**:
   ```
    N      N = minecraft:nether_star   ×1
   S S     S = alexsmobs:farseer_arm   ×2
   OOO     O = minecraft:obsidian      ×3
   ```
   *(`transmutation_table`)*
10. **Transmute 1000 items on one table.** The counter lives on the block, not
    the player. *(`transmute_1000_items`)*

Void Worm Beak (2 mandibles) and Void Worm Effigy (beak + 3 ender pearls +
3 purpur blocks) are decorative; the beak opens and closes on a redstone signal.

**How the Transmutation Table works.** It offers three results at a time, rolled
from three loot tables — common (14 entries: dirt, cobblestone, sand, red sand,
stick, torch, kelp, snowball, clay ball, granite, diorite, andesite, cobbled
deepslate, netherrack), uncommon (16, including raw iron, raw copper, raw gold,
coal, glowstone dust, slime ball, feather, book, flint, gunpowder, redstone,
pumpkin, melon slice, wheat, capsid, acacia blossom) and rare (16, including
diamond, emerald, mimicream, quartz, amethyst shard, lapis lazuli, ender pearl,
blaze rod, prismarine crystals and shards, shulker shell, end rod, nautilus
shell, gilded blackstone, ghast tear).

- Each exchange costs **3 experience levels** (`transmutingExperienceCost`).
- Output count is `input count ÷ (input max stack ÷ output max stack)`, minimum 1.
- Only stackable items can be inserted. `minecraft:beacon` is blacklisted.
- The table learns. With `limitTransmutingToLootTables = false`, one of the three
  slots can be replaced by something you have transmuted before, at
  `min(1.875% × total weight, 20%)`. Weight grows by 3.0 × log(stack size) each
  time you feed an item in and drops by 4.0 each time you pick it as a result.
- `transmutingTableExplodes = true`: breaking the table sets off a **radius-3**
  block-destroying explosion.

### Straddler, Stradpole and lava travel

1. **Find Straddlers in Basalt Deltas** (spawn weight 70) or **Stradpoles in
   lava** (weight 10, 3 rolls). *(`straddler`)*
2. **Get Straddlite**, either way:
   - Kill a Straddler: **20% + 5% per Looting level**.
   - Right-click a **Stradpole** with **Mosquito Larva**. One larva is consumed
     per attempt and there is a **45%** chance it grows into a Straddler.
     Stradpoles drop nothing when killed and can be bucketed with a water bucket.
     *(`stradpole_feed`)*
3. **Craft what you need:**

   | Item | Grid | Ingredients |
   |---|---|---|
   | Straddleboard | ` SN` / `SNS` / `NS ` | 4 Straddlite, 3 netherite ingots *(`straddleboard`)* |
   | Straddle Saddle | `EE` / `SS` | 2 saddles, 2 Straddlite *(`straddle_saddle`)* |
   | Straddle Helmet | ` S ` / `S S` / `L L` | 3 Straddlite, 2 string |
   | Straddlite Block | 3×3 | 9 Straddlite (reverses for 9) |

4. **Fit the Straddle Saddle to an adult Laviathan** by right-clicking it, then
   right-click again to ride. The Straddle Helmet fits the same way and is what
   makes it steerable. Both drop when it dies. Laviathans heal 10 from Magma
   Cream and breed with Mosquito Larva. *(`laviathan_four_passengers` for riding
   one with three other players aboard)*

### Crimson Mosquito → Warped Mosco

1. **Kill a Crimson Mosquito** for a Mosquito Proboscis and a Blood Sac. The
   drop rates depend on the mosquito's state:

   | State | Proboscis | Blood Sac |
   |---|---|---|
   | Normal | 10% +1%/looting | — |
   | Full of blood | 10% +1%/looting | 80% +1%/looting |
   | Grown from a Fly | 30% +3%/looting | 10% +1%/looting |
   | Grown from a Fly, full | 50% +3%/looting | **100%** |

2. **Craft the Blood Sprayer**: `SS ` / `BBP` / `B  ` — 2 Blood Sac, 1 Mosquito
   Proboscis, 3 nether brick. *(`blood_sprayer`)*
3. **Sicken a mosquito.** Let a Crimson Mosquito drink from a **Mungus carrying
   warped fungus with 5 or more mushrooms on it**. The drink deals 7 damage
   instead of 2 and suppresses the Mungus explosion. After **5 seconds** the
   mosquito starts swelling; at **8 seconds** it is replaced by a **Warped
   Mosco**. *(`crimson_mosquito_sick`)*
   - Gated by `warpedMoscoTransformation = true`.
     `warpedMoscoMobTriggers = [""]` on this server, so a Mungus is the only
     trigger mob. Warped Moscos do not spawn naturally — their biome list is
     empty.
   - Right-clicking a mosquito with `alexsmobs:warped_mixture` also works, but
     that item has **no recipe, loot table or trade anywhere in the jar** — how
     a player obtains it is not documented.
4. **Kill the Warped Mosco**: Warped Muscle at **70% +10%/looting**, and 1–5
   Hemolymph Sacs guaranteed. *(`warped_mosco_kill`)*
5. **Craft the Hemolymph Blaster**: `SSS` / `CBP` / `M  ` — 3 Hemolymph Sac,
   1 Mimicream (a Mimicube drop), 1 Blood Sprayer, 1 Mosquito Proboscis,
   1 Warped Muscle. *(`hemolymph_blaster`)*

Mosquito Larva also grows Stradpoles, breeds Laviathans and Warped Toads, tames
Warped Toads, feeds Anteaters, and makes the Mysterious Worm.

### Leafcutter anthill → Anteater

1. **Find a Leafcutter Anthill** — 0.5% of chunks
   (`leafcutterAnthillSpawnChance = 0.005`). Stomping it angers the colony.
   *(`stomp_leafcutter_anthill`)*
2. **Let the colony farm.** Leafcutter Ant Chamber blocks below the hill grow
   fungus through 6 stages at **30%** per leaf an ant delivers
   (`leafcutterAntFungusGrowChance`). The colony caps at 10 ants
   (`leafcutterAntColonySize`), ants break leaves 20% of the time
   (`leafcutterAntBreakLeavesChance`), and a colony below half strength needs
   **25** leaf deliveries to regain a worker (`leafcutterAntRepopulateFeedings`).
3. **Harvest Gongylidia.** Right-click a chamber at full fungus for
   **1 Gongylidia**; the block resets to empty. Put a **Shroomlight within the
   3×3×3 around the chamber** or every leafcutter ant within 20×6×20 is angered.
   There is a 50% chance the chamber also spreads to an adjacent unlit block.
   *(`gongylidia`)*
4. **Get a Leafcutter Ant Pupa**, either way:
   - Break a chamber **without Silk Touch**: **10% / 14.3% / 25% / 100%** for
     Fortune 0 / 1 / 2 / 3. Silk Touch always returns the chamber block instead.
   - Right-click an anthill that still has a queen with **1 Gongylidia** to
     release her, then kill the queen (pupa ×0–1, +0–1 per Looting level). Worker
     ants drop nothing. Gongylidia is also the ants' food — it pacifies and heals
     them.
   *(`leafcutter_ant_pupa`)*
5. **Place the pupa** on a block in `#alexsmobs:leafcutter_pupa_usable_on` to
   start your own colony, **or breed Anteaters with it** — it is the only item
   in `#alexsmobs:anteater_breedables`. *(`breed_anteater`)*

### Soul Vulture → Soul Heart → Spectre

1. **Find a Soul Vulture** in the Nether. `soulVultureSpawnOnFossil = true`
   restricts them to Nether Fossil structures. *(`soul_vulture`)*
2. **Let it feed.** A vulture gains a soul level each time it damages something
   while below full health, capped at 5. Above level 2 it is **bloated** and
   switches to its richer loot table.
3. **Kill a bloated Soul Vulture**: bone ×0–2 and coal ×0–1 as normal, plus a
   **Soul Heart ×0–1** (no Looting bonus). *(`soul_heart`)*
4. **Spend the Soul Heart:**
   - **Lure a Spectre** in the End with it, then lead it with a lead to ride.
     *(`spectre`)*
   - **Brew it** into an awkward potion for the **Soulsteal** effect.

### Enderiophage, capsid and the locators

- **Enderiophage → Capsid**, guaranteed on kill. *(`capsid`)*
- **Capsid → Enderiophage.** Place a capsid directly on top of a **vertical End
  Rod** and put an **Ender Eye** in the capsid. After **1 second** both blocks
  are consumed and an Enderiophage spawns.
- **Capsid recipes:** Cod → Cosmic Cod (6 s, *`cosmic_cod`*); any music disc →
  Music Disc "Daze" (6 s); Mosquito Larva → Mysterious Worm (6 s); Dimensional
  Carver → Shattered Dimensional Carver (10 s).
- **Enderiophage Rocket**: ` C ` / ` I ` / `EIE` — 1 Capsid, 2 iron nuggets,
  2 end stone, yields **3**. *(`enderiophage_rocket`)*
- **Ambergris → Echolocator.** Cachalot Whales drop nothing on death. Ambergris
  comes from **rescuing a beached whale**: push it back into water without
  hurting it and it swims to you and coughs up **2–3 Ambergris** within 10
  blocks. Whale teeth drop at **10%** per successful charge attack.
  *(`save_cachalot_whale`)*
- **Echolocator** (finds caves): `CPC` / `PAP` / ` P ` — 2 Cachalot Whale Tooth,
  1 Ambergris, 4 iron ingots. *(`echolocator`)*
- **Endolocator** (finds End Portal frames): ` P ` / `PAP` / ` P ` —
  1 Echolocator, 4 ender pearls. *(`endolocator`)*
- **Pupfish Locator**: `SBS` / `BAB` / `SBS` — 1 Echolocator, 4 slime balls,
  4 Fish Bones. *(`strange_fish_finder`, then `devils_hole_pupfish_bucket`)*

### Falconry chain

1. **Kill 4 Blobfish** (1 each, guaranteed) and craft **Fish Oil** — shapeless,
   1 glass bottle + 4 Blobfish.
2. **Tame a Bald Eagle** with the fish oil. *(`tame_bald_eagle`)*
3. **Kill a Grizzly Bear** for Bear Fur and craft the **Falconry Glove** —
   ` L ` / `LLL` / ` H `, 4 leather + 1 Bear Fur. *(`falconry_glove`)*
4. **Kill a Roadrunner** for a Roadrunner Feather and craft the **Falconry
   Hood** — 3 leather + 1 feather. *(`falconry_hood`)*
5. **Score a kill 100 blocks out** with a hooded eagle.
   *(`bald_eagle_challenge`)*

### Blessings

| Effect | How to get it | Duration | What it does |
|---|---|---|---|
| **Sunbird's Blessing** | Stand within **15 blocks horizontally / 32 vertically** of a Sunbird. It applies the effect every **5 seconds** to everyone in range who does not already have it | **30 s**, refreshed | Fall damage zeroed; downward velocity cut to 60% while airborne and not sneaking; elytra gliding gains lift above 10° pitch. **Attacking the Sunbird strips it** |
| **Tiger's Blessing** | **Throw meat on the ground** near a Tiger. It heals 5 and rolls: **40%** for porkchop or cooked porkchop, **30%** for chicken or cooked chicken, **10%** for any other edible meat. Rotten flesh is excluded | **10 minutes** | Every adult Tiger within **32 blocks** attacks whatever non-ally you attack |
| **Orca's Might** | **Sprint-swim** near a wild Orca that is not targeting you. Each tick has a **1-in-6** chance | **50 s** | **+3 flat attack damage**. Being targeted by the orca strips it |

### Armour and gear from mob drops

| Item | Grid | Ingredients | Where the part comes from |
|---|---|---|---|
| Crocodile Chestplate | `S S` / `SSS` / `SSS` | 8 Crocodile Scute | Crocodile, 0–2 (+0–1/looting) |
| Rocky Chestplate | `S S` / `SSS` / `SSS` | 8 Rocky Shell | Rocky Roller, **75% +10%/looting** |
| Froststalker Helmet | ` H ` / `III` / `I I` | 1 Froststalker Horn, 5 packed ice | Froststalker, **23% +10%/looting, player kill only** |
| Spiked Turtle Shell | `HHH` / `HCH` | 5 Spiked Scute, 1 turtle helmet | Shear a moss-covered Alligator Snapping Turtle |
| Centipede Leggings | `SSS` / `S S` / `S S` | 7 Centipede Leg | Cave Centipede head, 0–2 |
| Emu Leggings | `FKF` / `K K` / `F F` | 4 Emu Feather, 3 Kangaroo Hide | Emu 0–2; Kangaroo 0–2 |
| Moose Headgear | `AIA` / `S S` | 2 Moose Antler, 1 iron ingot, 2 string | Moose sheds antlers |
| Frontier Cap | `HHH` / `HCH` / `T  ` (or mirrored) | 5 Bear Fur, 1 Raccoon Tail, 1 leather helmet | Grizzly 0–2; Raccoon 0–1 |
| Roadrunner Boots | `F F` / `F F` / `SBS` | 4 Roadrunner Feather, 1 leather boots, 2 chiselled sandstone | Roadrunner 0–1 |
| Flying Fish Boots | `S S` / `F F` | 2 Flying Fish, 2 string | Flying Fish, 1 guaranteed |
| Tarantula Hawk Elytra | `WEW` | 2 Tarantula Hawk Wing + 1 elytra | Each wing is 9 fragments; the hawk drops 0–1 fragments, so **18 fragments** total |
| Shield of the Deep | `SSS` / `PHP` / `TPT` | 3 Serrated Shark Tooth, 2 Shark Tooth, 3 prismarine bricks, 1 heart of the sea | Shark drops |
| Tendon Whip | ` CC` / `TTC` / `ST ` | 3 Dropbear Claw, 3 Elastic Tendon, 1 wooden rod | Murmur drops 0–2 tendons |
| Novelty Hat | not crafted | — | Skelewag, **1% +1.5%/looting** |
| Unsettling Kimono | not crafted | — | Murmur, **10%** (weight 1 against red wool's 9) |

### Shorter chains

- **Skreecher → Sculk Boomer.** Skreecher Soul drops guaranteed but **only on a
  player kill**. Craft `FFF` / `SSS` / `BBB` — 3 sculk, 3 Skreecher Soul, 3 bone
  blocks. *(`skreecher` → `sculk_boomer`)*
- **Guster → Gustmaker / Pocket Sand.** Guster Eye drops at **20% +10%/looting**
  from all three variants. Gustmaker: 7 cut sandstone, 1 Guster Eye, 1 redstone.
  Pocket Sand: 3 sand, 5 leather, 1 Guster Eye. *(`guster` → `gustmaker`,
  `pocket_sand`)*
- **Rattlesnake → Maraca → La Cucaracha.** Rattlesnake Rattle 0–1 → Maraca
  (` P ` / `PRP` / ` S `, 3 planks + rattle + wooden rod). Give the maraca to a
  Cockroach; that cockroach's loot then returns the maraca plus a **Sombrero at
  20% +1%/looting**. *(`rattlesnake` → `maraca` → `la_cucaracha`)*
- **Giant Squid → Squid Grapple.** A Lost Tentacle only appears when a Cachalot
  Whale grabs a Giant Squid: each escape roll is 30% to break free, and **20%**
  of those shed a tentacle. Giant Squid kills only give 4–8 ink sacs. Craft
  `TTT` / `CBC` / ` C ` — 3 Lost Tentacle, 1 crossbow, 3 copper ingots.
  *(`lost_tentacle` → `squid_grapple`)*
- **Skunk → Stink Bottle → Stink Ray.** Catch skunk spray in a glass bottle, then
  `SS ` / `IIH` / `I  ` — 2 Stink Bottle, 3 iron ingots, 1 hopper.
  *(`skunk` → `stink_bottle` → `stink_ray`)*
- **Skelewag drops**, all one kill: Skelewag Sword **10% +5%/looting**, Fish
  Bones **30% +20%/looting**, Novelty Hat **1% +1.5%/looting**, bone 0–2.

## Advancement reference

106 advancement files, 212 lang keys (a title and a description for each). The
tree is a single tree: `alexsmobs:alexsmobs/root` is the only root and every
other advancement descends from it. Frames break down as **85 task, 18
challenge, 3 goal**.

Root fires on `minecraft:consume_item` for `alexsmobs:animal_dictionary` — hold
right-click on the book.

Where an advancement lists several criteria, the JSON puts them in one
`requirements` OR-group, so any one of them completes it. The common
kill / hurt / interact triple means simply meeting the creature counts.

### Tree

```
root
├─ acacia_blossom
│  └─ tame_elephant
│     ├─ elephant_swag
│     └─ tame_elephant_tusked
├─ banana
│  ├─ banana_slug
│  ├─ tame_capuchin
│  │  └─ sopa_de_macaco
│  └─ tame_gorilla
├─ bison_spyglass
├─ breed_hummingbird
│  └─ hummingbird_feeder
├─ crimson_mosquito
│  ├─ blood_sprayer
│  ├─ crimson_mosquito_larva
│  │  └─ tame_warped_toad
│  └─ crimson_mosquito_sick
│     └─ warped_mosco_kill
│        └─ hemolymph_blaster
├─ crocodile
│  ├─ alligator_snapping_turtle
│  │  └─ spiked_scute
│  │     └─ spiked_turtle_shell
│  └─ breed_crocodile
│     └─ crocodile_chestplate
├─ enderiophage
│  ├─ capsid
│  │  ├─ cosmic_cod
│  │  │  └─ tame_cosmaw
│  │  ├─ enderiophage_rocket
│  │  └─ mysterious_worm
│  │     └─ void_worm_summon
│  │        ├─ void_worm_kill
│  │        │  └─ dimensional_carver
│  │        │     └─ shattered_dimensional_carver
│  │        │        └─ farseer
│  │        │           └─ transmutation_table
│  │        │              └─ transmute_1000_items
│  │        └─ void_worm_split
│  └─ ender_flu
├─ froststalker_kill
│  └─ froststalker_helmet
│     └─ breed_froststalker
├─ grizzly_bear
│  └─ tame_grizzly_bear
├─ guster
│  ├─ gustmaker
│  └─ pocket_sand
├─ kangaroo
│  └─ emu
│     └─ emu_dodge
├─ laviathan_spyglass
├─ lost_tentacle
│  └─ squid_grapple
├─ maned_wolf_apple
├─ murmur
├─ orcas_might
├─ rainbow_jelly
│  └─ rainbow_glass
├─ rattlesnake
│  └─ maraca
│     └─ la_cucaracha
├─ rocky_roller
│  └─ rocky_shell
│     └─ rocky_chestplate
├─ save_cachalot_whale
│  └─ echolocator
│     └─ endolocator
├─ seagull_steal
├─ skelewag
│  ├─ fish_bones
│  │  └─ strange_fish_finder
│  │     └─ devils_hole_pupfish_bucket
│  └─ skelewag_skull
│     └─ novelty_hat
├─ skreecher
│  └─ sculk_boomer
├─ skunk
│  └─ stink_bottle
│     └─ stink_ray
├─ soul_vulture
│  └─ soul_heart
│     └─ spectre
├─ stomp_leafcutter_anthill
│  └─ gongylidia
│     └─ leafcutter_ant_pupa
│        └─ breed_anteater
├─ straddler
│  ├─ straddle_saddle
│  │  └─ laviathan_four_passengers
│  ├─ straddleboard
│  └─ stradpole_feed
├─ sunbird_blessing
├─ tame_bald_eagle
│  └─ falconry_glove
│     └─ falconry_hood
│        └─ bald_eagle_challenge
├─ tame_flutter
├─ tame_mantis_shrimp
│  └─ mantis_shrimp_bucket
├─ tarantula_hawk
│  └─ tame_tarantula_hawk
├─ tigers_blessing
└─ underminer
   └─ ghostly_pickaxe
```

The longest chain is 12 deep: `root → enderiophage → capsid → mysterious_worm →
void_worm_summon → void_worm_kill → dimensional_carver →
shattered_dimensional_carver → farseer → transmutation_table →
transmute_1000_items`.

### Full table

| id | Title | Description | Parent | Frame | Trigger |
|---|---|---|---|---|---|
| `acacia_blossom` | Flowers of the Savanna | Obtain an Acacia Blossom from breaking Acacia Leaves | `root` | goal | Obtain Acacia Blossom |
| `alligator_snapping_turtle` | Alligator In Name Only | Encounter an Alligator Snapping Turtle | `crocodile` | task | Kill, hurt, or interact with Alligator Snapping Turtle |
| `bald_eagle_challenge` | Winning Play | Kill any creature from 100 blocks away with an eagle wearing a hood. | `falconry_hood` | challenge | `alexsmobs:bald_eagle_challenge` — a launched, hooded, tamed bald eagle scores a kill while at least 100 blocks from its owner |
| `banana` | Gone Bananas! | Obtain a Banana | `root` | task | Obtain any item in `#alexsmobs:bananas` |
| `banana_slug` | Convergent Evolution... | Encounter a Banana Slug. Not so appetising. | `banana` | task | Kill, hurt, or interact with Banana Slug |
| `bison_spyglass` | Perfect View in the Plains | Observe a Bison through the lens of a Spyglass. | `root` | challenge | Look at a Bison while using a Spyglass |
| `blood_sprayer` | Spray 'n Pray | Craft a Blood Sprayer from the drops of a Crimson Mosquito | `crimson_mosquito` | task | Obtain Blood Sprayer |
| `breed_anteater` | Aunt Anteater | Breed two Anteaters by feeding them pupae. | `leafcutter_ant_pupa` | task | Breed Anteaters |
| `breed_crocodile` | Crikey! | Breed two crocodiles with rotten flesh. Careful not to trample their eggs! | `crocodile` | task | Breed Crocodiles |
| `breed_froststalker` | Undercover Under Covers | Breed two Froststalkers with porkchops. | `froststalker_helmet` | challenge | Breed Froststalkers |
| `breed_hummingbird` | Sugar Rush | Breed two hummingbirds with flowers | `root` | task | Breed Hummingbirds |
| `capsid` | Capsid-19 | Obtain a Capsid from a slain Enderiophage. Use it to display items or to transfer them upwards | `enderiophage` | task | Obtain Capsid |
| `cosmic_cod` | Weird Fishes/Arpeggi | Create a Cosmic Cod by placing a Cod in a Capsid. | `capsid` | task | Obtain Cosmic Cod |
| `crimson_mosquito` | Nightmare Fuel | Encounter a crimson mosquito | `root` | task | Kill, hurt, or interact with Crimson Mosquito |
| `crimson_mosquito_larva` | Pest Control | Craft a Crimson Mosquito Larvae from a maggot and a special proboscis | `crimson_mosquito` | task | Obtain `alexsmobs:mosquito_larva` |
| `crimson_mosquito_sick` | Down with the Sickness | Feed a Crimson Mosquito a strange, fungal creature covered in Warped Fungus. Watch as the Crimson Mosquito transforms! | `crimson_mosquito` | task | `alexsmobs:mosquito_sick` — a Crimson Mosquito drinks from a warped-fungus creature and sickens; awarded to every player within 40×25×40 blocks |
| `crocodile` | Chompy | Encounter a Crocodile | `root` | task | Kill, hurt, or interact with Crocodile |
| `crocodile_chestplate` | Cover me with... scutes? | Craft a crocodile chestplate from many crocodile scutes | `breed_crocodile` | challenge | Obtain Crocodile Chestplate |
| `devils_hole_pupfish_bucket` | One Chunk Fish | Capture the rarest fish in a bucket. | `strange_fish_finder` | challenge | Obtain Devil's Hole Pupfish Bucket |
| `dimensional_carver` | Break On Through... | Using the drops of the Void Worm, create the Dimensional Carver, which allows you to dig through the fabric of reality to return home at any given point. | `void_worm_kill` | task | Obtain Dimensional Carver |
| `echolocator` | Echo-muh-cation! | Craft an Echolocator, which can reveal nearby caves | `save_cachalot_whale` | task | Obtain Echolocator |
| `elephant_swag` | Dressed to Impress | Place a colored carpet on an elephant | `tame_elephant` | task | `alexsmobs:elephant_swag` — the owner right-clicks a tamed elephant with a carpet colour it is not already wearing |
| `emu` | It's an Emu!!! | Encounter an Emu. Exercise caution. | `kangaroo` | task | Kill, hurt, or interact with Emu |
| `emu_dodge` | Begun, The Emu War Has | See an emu dodge a launched projectile. | `emu` | task | `alexsmobs:emu_dodge` — an emu dodges a projectile; awarded to the projectile's owner |
| `ender_flu` | Race Against The Clock | Catch the Ender Flu effect. Cure it by eating many Chorus Fruit or drinking milk. Be sure not to let it run its toll! | `enderiophage` | task | Gain the Ender Flu effect |
| `enderiophage` | Ender Distancing | Encounter an Enderiophage, a giant biomechanical construct found in the End Midlands. Be careful not to catch Ender Flu! | `root` | task | Kill, hurt, or interact with Enderiophage |
| `enderiophage_rocket` | Ad End-stra | Craft an Enderiophage Rocket, which can be used in place of Firework Rockets when in the End. | `capsid` | task | Obtain Enderiophage Rocket |
| `endolocator` | No End In Sight | Craft an Endolocator, which can reveal nearby End Portal Frames | `echolocator` | task | Obtain Endolocator |
| `falconry_glove` | Hand In Glove | Craft a Falconry Glove from Leather and Hair of Bear. Use it to pick up and launch tamed eagles! | `tame_bald_eagle` | task | Obtain Falconry Glove |
| `falconry_hood` | Blindsided | Craft a Falconry Hood from Leather and a Roadrunner Feather. Eagles wearing one can be manually directed! | `falconry_glove` | task | Obtain Falconry Hood |
| `farseer` | Farland Security | Encounter the Farseer, a monstrous defender of the world border. | `shattered_dimensional_carver` | task | Kill, hurt, or interact with Farseer |
| `fish_bones` | A Bone to Pick | Obtain Fish Bones from a Skelewag. | `skelewag` | task | Obtain Fish Bones |
| `froststalker_helmet` | An Impostor Amoung Us | Craft a Froststalker Helmet to walk amongst Froststalkers undetected. | `froststalker_kill` | task | Obtain Froststalker Helmet |
| `froststalker_kill` | Ice Scream | Slay a Froststalker. | `root` | goal | Kill Froststalker |
| `ghostly_pickaxe` | Ghost! Ghost! Toast? | Obtain a Ghostly Pickaxe from an Underminer. | `underminer` | task | Obtain Ghostly Pickaxe |
| `gongylidia` | Like a Truffle, with more Ant | Harvest Gongylidia from a Leafcutter Ant Chamber underground. Place Shroomlight near the chamber to make sure you don't upset the locals | `stomp_leafcutter_anthill` | task | Obtain Gongylidia |
| `grizzly_bear` | Pic-A-Nic Basket? | Encounter a Grizzly Bear | `root` | task | Kill, hurt, or interact with Grizzly Bear |
| `guster` | Eye of The Storm | Encounter a Guster during a stormy day in the desert | `root` | task | Kill, hurt, or interact with Guster |
| `gustmaker` | I Am Become Guster | Craft a Gustmaker. Now you can make your own mini-storms! | `guster` | task | Obtain Gustmaker |
| `hemolymph_blaster` | Blast from the... Future? | Craft a Hemolyph Blaster, the ultimate upgrade to the Blood Sprayer. | `warped_mosco_kill` | task | Obtain Hemolymph Blaster |
| `hummingbird_feeder` | Sugar... In Wator... | Craft a Hummingbird Feeder in order to keep hummingbirds nearby | `breed_hummingbird` | task | Obtain Hummingbird Feeder |
| `kangaroo` | We do a little trolling... | Encounter a Kangaroo | `root` | task | Kill, hurt, or interact with Kangaroo |
| `la_cucaracha` | Mariachi! | Give a Maraca to a cockroach and enjoy the show. ¡La Cucaracha! | `maraca` | challenge | Use a Maraca on a Cockroach |
| `laviathan_four_passengers` | Mass Transit | Ride a Laviathan with three other passengers. | `straddle_saddle` | task | `alexsmobs:laviathan_four_passengers` — a ridden Laviathan carries more than three passengers; checked every 2 seconds, awarded to each player aboard |
| `laviathan_spyglass` | Loch-Nether Monster! | Observe a Laviathan through the lens of a Spyglass. | `root` | challenge | Look at a Laviathan while using a Spyglass |
| `leafcutter_ant_pupa` | Ant Farm | Obtain a Leafcutter Ant Pupa, which can be placed on dirt to start a Leafcutter Ant colony. | `gongylidia` | task | Obtain Leafcutter Ant Pupa |
| `lost_tentacle` | A Small Price to Pay... | Obtain a Lost Tentacle from a battle between two titans. | `root` | task | Obtain Lost Tentacle |
| `maned_wolf_apple` | Hungry For Apples? | Feed a Maned Wolf an apple. | `root` | task | Use an Apple on a Maned Wolf |
| `mantis_shrimp_bucket` | A Fistful of Water | Sneak and give a tamed Mantis Shrimp a bucket of water so that it can live on land indefinitely | `tame_mantis_shrimp` | task | Use a Water Bucket on a Mantis Shrimp while sneaking |
| `maraca` | Mariachi? | Craft a Maraca with a Rattlesnake rattle | `rattlesnake` | task | Obtain Maraca |
| `murmur` | Flexible Schedule | Encounter the Murmur, which is not as it seems. | `root` | task | Kill, hurt, or interact with a Murmur or a Murmur Head (six criteria, any one) |
| `mysterious_worm` | Destroy The Child | Create a Mysterious Worm by putting a Crimson Mosquito Larva in a Capsid. | `capsid` | task | Obtain Mysterious Worm |
| `novelty_hat` | He Was Number One! | Obtain a Novelty Hat from a Skelewag. | `skelewag_skull` | task | Obtain Novelty Hat |
| `orcas_might` | Free Willy | Be granted a blessing from a wild Orca | `root` | challenge | Gain the Orca's Might effect |
| `pocket_sand` | Pocket Sand! | Craft a Pocket Of Sand. Sha-sha! | `guster` | task | Obtain Pocket Sand |
| `rainbow_glass` | Rainbow Road | Craft Rainbow Glass from Rainbow Jelly and Glass. | `rainbow_jelly` | task | Obtain Rainbow Glass |
| `rainbow_jelly` | Taste the Rainbow | Obtain Rainbow Jelly from a Comb Jelly. Use a sponge if you don't like what happens... | `root` | task | Obtain Rainbow Jelly |
| `rattlesnake` | No Step on Snake | Encounter a Rattlesnake | `root` | task | Kill, hurt, or interact with Rattlesnake |
| `rocky_chestplate` | You're too Slow! | Craft a Rock Shell Chestplate to roll into a ball. | `rocky_shell` | task | Obtain Rocky Chestplate |
| `rocky_roller` | KEEP ROLLIN' ROLLIN' ROLLIN' | Encounter a Rocky Roller in the dripstone caves. | `root` | task | Kill, hurt, or interact with Rocky Roller |
| `rocky_shell` | Rocks Off! | Obtain a Rocky Shell from slaying a Rocky Roller. | `rocky_roller` | task | Obtain Rocky Shell |
| `root` | Alex's Mobs | Discover the unique creatures of the world | — | task | Use an Animal Dictionary (`minecraft:consume_item`) |
| `save_cachalot_whale` | Save the Whales! | Save a beached Cachalot Whale by pushing it into the water, and then have it reward you by coughing up some Ambergris | `root` | challenge | Obtain Ambergris |
| `sculk_boomer` | Ok Boomer | Craft a Sculk Boomer using the souls of a few Skreechers. | `skreecher` | task | Obtain Sculk Boomer |
| `seagull_steal` | Mine? Mine? Mine? | Have food stolen from your inventory by a seagull. | `root` | task | `alexsmobs:seagull_steal` — a seagull removes a food item from your inventory |
| `shattered_dimensional_carver` | Ticket to the End of the World | Shatter a Dimensional Carver by placing it in a Capsid. Instead of opening a portal home, it will now open a portal one million blocks in any direction. | `dimensional_carver` | task | Obtain Shattered Dimensional Carver |
| `skelewag` | We Just Want our Hat Back | Encounter a Skelewag near a sunken ship. | `root` | task | Kill, hurt, or interact with Skelewag |
| `skelewag_skull` | Smitty WerbenJagerManJensen | Take a sword-like skull from a Skelewag. | `skelewag` | task | Obtain `alexsmobs:skelewag_sword` |
| `skreecher` | Sculk Cymbal | Encounter the Skreecher, a loud and obnoxious sculk monster. | `root` | task | Kill, hurt, or interact with Skreecher |
| `skunk` | Hippie Smell | Get sprayed by a Skunk. | `root` | task | `alexsmobs:skunk_spray` — caught in a skunk's spray, which also gives 15 seconds of Nausea |
| `sopa_de_macaco` | Uma Delicia | Craft sopa de macaco with a banana peel | `tame_capuchin` | challenge | Obtain Sopa De Macaco |
| `soul_heart` | The Soul-ly Ghost | Obtain a soul heart from slaying a bloated Soul Vulture | `soul_vulture` | task | Obtain Soul Heart |
| `soul_vulture` | Fetch Me Their Souls! | Encounter a Soul Vulture in the nether | `root` | task | Kill, hurt, or interact with Soul Vulture |
| `spectre` | The Iron Curtain | Lure a Spectre in the end with a Soul Heart. Use a lead on them to hitch a ride! | `soul_heart` | task | Kill, hurt, or interact with Spectre |
| `spiked_scute` | Shear the Scute | Shear a moss-covered Alligator Snapping Turtle and obtain a Spiked Scute | `alligator_snapping_turtle` | task | Obtain Spiked Scute |
| `spiked_turtle_shell` | Turtle-ology Majors Be Like | Craft a Spiked Turtle Shell | `spiked_scute` | challenge | Obtain Spiked Turtle Shell |
| `squid_grapple` | ... for Salvation | Craft a Grappling Squok from Lost Tentacles, a crossbow and copper ingots. | `lost_tentacle` | task | Obtain Squid Grapple |
| `stink_bottle` | Gamer Skunk Bath Water | Capture skunk spray using a glass bottle. | `skunk` | task | Obtain Stink Bottle |
| `stink_ray` | I SAID DART GUN! | Craft a Stink Ray. | `stink_bottle` | task | Obtain Stink Ray |
| `stomp_leafcutter_anthill` | Ant-Agonizer | Stomp on a Leafcutter Anthill - beware the angry denizens within! | `root` | task | `alexsmobs:stomp_leafcutter_anthill` — fall onto a Leafcutter Anthill block |
| `straddle_saddle` | The Family Sedan | Craft a Straddlite Saddle. Don't forget the trim! | `straddler` | challenge | Obtain Straddle Saddle |
| `straddleboard` | Surf Wax America | Craft a Straddleboard from some Netherite and Straddlerite. | `straddler` | challenge | Obtain Straddleboard |
| `straddler` | Straddle My Ol' Saddle | Encounter a Straddler in the Basalt Deltas. | `root` | task | Kill, hurt, or interact with Straddler |
| `stradpole_feed` | Like Father | Feed a Stradpole some Mosquito Larva, in hopes of turning it into a Straddler. | `straddler` | task | Use Mosquito Larva on a Stradpole |
| `strange_fish_finder` | The Quest for the Best | Craft a Strange Fish Finder from slimeballs, Fish Bones and an Echolocator. | `fish_bones` | task | Obtain `alexsmobs:pupfish_locator` |
| `sunbird_blessing` | The Power of the Sun | Receive a blessing from the great and noble sunbird | `root` | challenge | Gain the Sunbird's Blessing effect |
| `tame_bald_eagle` | Freedom Intensifies | Tame a bald eagle with fish oil. | `root` | task | Tame Bald Eagle |
| `tame_capuchin` | Monkey Business | Tame a capuchin monkey with bananas | `banana` | task | Tame Capuchin Monkey |
| `tame_cosmaw` | Its a Fish? Its a Bug? What is it? | Tame a Cosmaw by feeding it Cosmic Cod. | `cosmic_cod` | task | Tame Cosmaw |
| `tame_elephant` | Stampy! | Tame an elephant by feeding it Acacia Blossoms | `acacia_blossom` | task | Tame Elephant |
| `tame_elephant_tusked` | The Biggest Land Mammal | Tame a tusked elephant when it is a baby | `tame_elephant` | challenge | Tame an Elephant with NBT `{Tusked:true}` |
| `tame_flutter` | A Picky Fellow | Tame a Flutter by giving it multiple kinds of flowers. | `root` | task | Tame Flutter |
| `tame_gorilla` | In Memoriam | Tame a gorilla with bananas | `banana` | task | Tame Gorilla |
| `tame_grizzly_bear` | Arcturus! | Tame a Grizzly Bear by feeding it honey and salmon | `grizzly_bear` | task | Tame Grizzly Bear |
| `tame_mantis_shrimp` | Shrimp Friend | Tame a Mantis Shrimp with many feedings of Tropical Fish | `root` | task | Tame Mantis Shrimp |
| `tame_tarantula_hawk` | Big Iron | Tame a Tarantula Hawk by feeding it Spider Eyes. | `tarantula_hawk` | task | Tame Tarantula Hawk |
| `tame_warped_toad` | It Is Wednesday | Tame a Warped Toad, the perfect defense against any giant bug, with some larvae | `crimson_mosquito_larva` | task | Tame Warped Toad |
| `tarantula_hawk` | Rigged from the Start | Encounter a Tarantula Hawk in a desert. | `root` | task | Kill, hurt, or interact with Tarantula Hawk |
| `tigers_blessing` | Eye of the Tiger | Receive a Tiger's Blessing after feeding it Porkchops, Chicken or other meats. | `root` | challenge | Gain the Tiger's Blessing effect |
| `transmutation_table` | Reality Can Be Whatever I Want | Craft a Transmutation Table to convert materials into almost anything. | `farseer` | task | Obtain Transmutation Table |
| `transmute_1000_items` | Nonequivalent Exchange | Transmute 1000 items using the same Transmutation Table. | `transmutation_table` | task | `alexsmobs:transmute_1000_items` — one Transmutation Table block reaches 1000 transmuted items |
| `underminer` | Who Undermines the Underminer? | Break the block an Underminer is mining, revealing a hidden ore | `root` | task | `alexsmobs:undermine_underminer` — the block an Underminer is mining changes before it finishes; awarded to every player within 12 blocks |
| `void_worm_kill` | Wormy | Destroy the Void Worm. | `void_worm_summon` | challenge | `alexsmobs:void_worm_kill` — the original (non-split) Void Worm head dies to a player |
| `void_worm_split` | Should've Gone for the Head | Split a void worm in half by attacking one of its body segments. More worms, more problems! | `void_worm_summon` | task | `alexsmobs:void_worm_split` — destroy a Void Worm body segment, spawning a splitter worm |
| `void_worm_summon` | A Soul for a Soul | Toss the Mysterious Worm into the void of the End, and prepare to meet the Void Worm. | `mysterious_worm` | goal | `alexsmobs:void_worm_summon` — a dropped Mysterious Worm falls below Y −60 in a permitted dimension; awarded to whoever threw it |
| `warped_mosco_kill` | Destroyer of Chads | Slay the Warped Mosco, the swole defender of the Warped Forest. | `crimson_mosquito_sick` | challenge | Kill Warped Mosco |

### Notes

- All 13 Alex's Mobs custom triggers are bare `AMAdvancementTrigger` instances
  registered in `misc/AMAdvancementTriggerRegistry.java`; the JSON criterion
  carries no conditions, so the fire condition lives entirely in Java. Every one
  of them was traced to its call site — none are undocumented.
- Three ids do not match the item they check: `crimson_mosquito_larva` checks
  `alexsmobs:mosquito_larva`, `skelewag_skull` checks `alexsmobs:skelewag_sword`,
  and `strange_fish_finder` checks `alexsmobs:pupfish_locator`.
- `banana` is the only tag-based item check; every other one names an explicit id.
- Three triggers award to bystanders, not just the actor: `mosquito_sick`
  (40×25×40 blocks), `undermine_underminer` (12 blocks) and
  `laviathan_four_passengers` (every player aboard).
- Only `froststalker_kill` and `warped_mosco_kill` are kill-only; every other
  encounter advancement also accepts hurting or interacting.
