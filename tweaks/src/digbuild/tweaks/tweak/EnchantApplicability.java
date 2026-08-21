package digbuild.tweaks.tweak;

import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import digbuild.tweaks.Tweak;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.TridentItem;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentCategory;
import net.minecraftforge.registries.ForgeRegistries;

/**
 * Widens which items an enchantment may be applied to, from an allowlist.
 *
 * Item/enchantment compatibility is code on 1.20.1, not data. Vanilla's
 * EnchantmentCategory.WEAPON is `item instanceof SwordItem`, so Looting,
 * Fire Aspect and Knockback, and every modded enchantment that reuses WEAPON
 * (apotheosis:scavenger among them), are sword-only by construction -- and no
 * datapack or mod config in this pack reaches it.
 *
 * Rules only ever widen. allows() returning false means "no opinion", which
 * leaves the vanilla answer untouched, so nothing here can take an enchantment
 * away from an item that already accepts it.
 *
 * Ids are resolved when the config is read, not per call: the result is an
 * identity lookup on the way through two methods the enchanting screen calls in
 * a loop over every enchantment in the game.
 */
public final class EnchantApplicability extends Tweak {

    /** Resolved allowlist, replaced wholesale on each reload. Null until the
     *  first apply(), which is before anything can enchant anything. */
    private static volatile Map<Enchantment, List<String>> active;

    private boolean listedCandidates;

    @Override
    public String id() {
        return "enchant-applicability";
    }

    // --- the hot path -----------------------------------------------------

    /** True if this pairing is one the allowlist adds. Never false-negatives
     *  vanilla: a false here means "not our business". */
    public static boolean allows(Enchantment ench, ItemStack stack) {
        Map<Enchantment, List<String>> rules = active;
        if (rules == null || stack == null) {
            return false;
        }
        List<String> targets = rules.get(ench);
        if (targets == null) {
            return false;
        }
        Item item = stack.m_41720_();
        for (int i = 0; i < targets.size(); i++) {
            if (matches(targets.get(i), item)) {
                return true;
            }
        }
        return false;
    }

    /** Aliases are instanceof checks, so modded axes and tridents count without
     *  being listed; anything else is an exact item id. */
    private static boolean matches(String target, Item item) {
        switch (target) {
            case "axe":
                return item instanceof AxeItem;
            case "trident":
                return item instanceof TridentItem;
            case "sword":
                return item instanceof SwordItem;
            case "pickaxe":
                return item instanceof PickaxeItem;
            case "shovel":
                return item instanceof ShovelItem;
            case "hoe":
                return item instanceof HoeItem;
            default:
                ResourceLocation id = ForgeRegistries.ITEMS.getKey(item);
                return id != null && target.equals(id.toString());
        }
    }

    // --- config -----------------------------------------------------------

    @Override
    public void apply(List<String> lines) {
        Map<String, List<String>> rules = new LinkedHashMap<>();
        for (String line : lines) {
            parse(line, rules);
        }

        Map<Enchantment, List<String>> resolved = new IdentityHashMap<>();
        List<String> summary = new ArrayList<>();
        for (Map.Entry<String, List<String>> rule : rules.entrySet()) {
            ResourceLocation id = ResourceLocation.m_135820_(rule.getKey());
            Enchantment ench = id == null ? null : ForgeRegistries.ENCHANTMENTS.getValue(id);
            if (ench == null) {
                log("unknown enchantment " + rule.getKey()
                    + " -- no loaded mod registers it, rule ignored");
                continue;
            }
            resolved.put(ench, rule.getValue());
            summary.add(rule.getKey() + " -> " + String.join("+", rule.getValue()));
            warnIfOverridden(ench, rule.getKey());
        }

        active = resolved;
        log(resolved.size() + " rule(s) active: " + String.join(", ", summary));
        if (!listedCandidates) {
            listedCandidates = true;
            log("sword-only enchantments present: " + String.join(", ", swordOnly()));
        }
    }

    private void parse(String line, Map<String, List<String>> into) {
        int eq = line.indexOf('=');
        if (eq < 0) {
            log("ignoring malformed line: " + line);
            return;
        }
        // Not java.util.Properties: it splits on ':' as readily as '=', which
        // would turn "minecraft:looting = axe" into the key "minecraft".
        String id = line.substring(0, eq).trim().toLowerCase();
        if (id.indexOf(':') < 0) {
            id = "minecraft:" + id;
        }
        List<String> targets = new ArrayList<>();
        for (String t : line.substring(eq + 1).split(",")) {
            String target = t.trim().toLowerCase();
            if (!target.isEmpty()) {
                targets.add(target);
            }
        }
        if (targets.isEmpty()) {
            log("ignoring " + id + ": no targets");
            return;
        }
        into.put(id, targets);
    }

    /**
     * Both injectors sit on Enchantment itself. An enchantment that overrides
     * the method decides for itself and never reaches them -- vanilla's
     * DamageEnchantment is the stock example, overriding canEnchant so axes
     * take Sharpness. Nothing on the default allowlist does, but a mod update
     * could, and the failure mode is otherwise invisible: the rule is accepted,
     * logged as active, and quietly does nothing.
     */
    private void warnIfOverridden(Enchantment ench, String id) {
        check(ench, id, "m_6081_", "anvils");
        check(ench, id, "canApplyAtEnchantingTable", "the enchanting table");
    }

    private void check(Enchantment ench, String id, String method, String where) {
        try {
            Class<?> owner = ench.getClass().getMethod(method, ItemStack.class).getDeclaringClass();
            if (owner != Enchantment.class) {
                log("note: " + id + " overrides " + method + " in " + owner.getName()
                    + " -- the rule may not take effect at " + where);
            }
        } catch (Throwable t) {
            log("note: could not inspect " + method + " on " + id + " (" + t + ")");
        }
    }

    /** Everything in the sword-only category, so extending the allowlist does
     *  not mean unzipping jars to find out what is even a candidate. */
    private static List<String> swordOnly() {
        List<String> ids = new ArrayList<>();
        for (Enchantment ench : ForgeRegistries.ENCHANTMENTS) {
            if (ench.f_44672_ == EnchantmentCategory.WEAPON) {
                ResourceLocation id = ForgeRegistries.ENCHANTMENTS.getKey(ench);
                if (id != null) {
                    ids.add(id.toString());
                }
            }
        }
        return ids;
    }

    @Override
    public String defaultConfig() {
        return "# Which items an enchantment may be applied to.\n"
            + "#\n"
            + "# One rule per line:\n"
            + "#\n"
            + "#     <enchantment id> = <target>[, <target>...]\n"
            + "#\n"
            + "# A target is an item class alias -- axe, trident, sword, pickaxe, shovel, hoe\n"
            + "# -- which covers modded items of that class too, or an exact item id such as\n"
            + "# minecraft:trident.\n"
            + "#\n"
            + "# Saved edits are picked up within about ten seconds; no restart, no reload\n"
            + "# command. The result is logged, including any id no loaded mod registers.\n"
            + "#\n"
            + "# Rules only widen: nothing here can take an enchantment away from an item\n"
            + "# that already accepts it. The boot log lists every sword-only enchantment on\n"
            + "# the server, which is where to look for more to add.\n"
            + "#\n"
            + "# Only the applicability check moves. Whether the enchantment then *does*\n"
            + "# anything is the enchantment's business. All four below were checked in the\n"
            + "# jars and read the killer's main-hand stack, so they work from an axe or a\n"
            + "# melee trident stab -- but a thrown trident is not in the hand when the mob\n"
            + "# dies, so none of them apply to the throw.\n"
            + "#\n"
            + "# Deliberately absent, having been considered:\n"
            + "#   minecraft:sweeping    gated on ToolActions.SWORD_SWEEP, so it would show\n"
            + "#                         on the item and do nothing\n"
            + "#   sharpness/smite/bane  already work on axes; DamageEnchantment overrides\n"
            + "#                         canEnchant but falls through to super, so adding\n"
            + "#                         'trident' here would work if you want it\n"
            + "#   majruszsenchantments  do not use EnchantmentCategory at all, and\n"
            + "#                         CustomEnchantment overrides canEnchant, so a rule\n"
            + "#                         would take at the table and not at the anvil. Their\n"
            + "#                         IS_MELEE predicate already covers axes anyway.\n"
            + "\n"
            + "minecraft:looting = axe, trident\n"
            + "apotheosis:scavenger = axe, trident\n"
            + "apotheosis:knowledge = axe, trident\n"
            + "apotheosis:capturing = axe, trident\n";
    }
}
