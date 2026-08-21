package digbuild.tweaks.tweak;

import java.util.ArrayList;
import java.util.List;

import digbuild.tweaks.Tweak;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.inventory.CraftingContainer;
import net.minecraft.world.item.ItemStack;

/**
 * Carries chosen NBT from a crafting ingredient onto the crafted result.
 *
 * Vanilla builds a result from the recipe alone -- `this.result.copy()` -- so
 * everything an ingredient carried is gone the moment it is consumed. That is
 * fine for planks and awful for "craft a Raijin Helmet from a netherite
 * helmet", which silently eats the affixes, the rarity and every socketed gem.
 *
 * Apotheosis keeps all of that in one root compound, `affix_data` (affixes,
 * rarity, name, category, sockets, gems -- see AffixHelper and SocketHelper in
 * its jar), so carrying that single key across is the whole fix.
 *
 * The rolled name comes with it, and that is the right outcome rather than an
 * accident: affix_data.name is not a literal but a translatable template, and
 * Apotheosis' ItemStackMixin.apoth_affixItemName substitutes the *stack's own*
 * hover name into it at render time. So the result reads "Spellshielded Raijin
 * Helmet of Darkness" -- prefix and suffix kept, base name the new item's --
 * and a name that is not translatable is dropped by that same code.
 *
 * Three rules are not configurable, because each is a way this would otherwise
 * be exploitable or wrong: the result must be a single item, exactly one
 * ingredient may carry the tags, and a tag already on the result is left alone.
 */
public final class CraftCarryover extends Tweak {

    private static volatile String[] tags = new String[0];
    private static volatile boolean sameSlotOnly = true;

    @Override
    public String id() {
        return "craft-carryover";
    }

    // --- the hot path -----------------------------------------------------

    /** Mutates a freshly assembled result. Called for every grid change, so it
     *  does nothing at all until an ingredient actually carries one of the
     *  tags. */
    public static void carry(CraftingContainer grid, ItemStack result) {
        String[] keys = tags;
        if (keys.length == 0 || result == null || result.m_41619_()) {
            return;
        }
        // A recipe yielding a stack would otherwise turn one affixed input into
        // a stack of affixed outputs.
        if (result.m_41613_() != 1) {
            return;
        }

        ItemStack source = null;
        for (int i = 0; i < grid.m_6643_(); i++) {
            ItemStack stack = grid.m_8020_(i);
            if (stack.m_41619_() || !stack.m_41782_() || !carries(stack.m_41783_(), keys)) {
                continue;
            }
            if (source != null) {
                return;  // two candidates: no way to pick, so pick neither
            }
            source = stack;
        }
        if (source == null) {
            return;
        }
        // Affix modifiers are rolled for the slot the item is worn in, so a
        // helmet's affixes belong on helmets. Everything not armour reports as
        // main hand, which leaves weapon-to-weapon crafting allowed.
        if (sameSlotOnly && LivingEntity.m_147233_(source) != LivingEntity.m_147233_(result)) {
            return;
        }

        CompoundTag from = source.m_41783_();
        CompoundTag to = result.m_41784_();
        for (String key : keys) {
            if (from.m_128441_(key) && !to.m_128441_(key)) {
                to.m_128365_(key, from.m_128423_(key).m_6426_());
            }
        }
    }

    private static boolean carries(CompoundTag tag, String[] keys) {
        for (String key : keys) {
            if (tag.m_128441_(key)) {
                return true;
            }
        }
        return false;
    }

    // --- config -----------------------------------------------------------

    @Override
    public void apply(List<String> lines) {
        List<String> keys = new ArrayList<>();
        boolean slots = true;
        for (String line : lines) {
            int eq = line.indexOf('=');
            if (eq < 0) {
                log("ignoring malformed line: " + line);
                continue;
            }
            String key = line.substring(0, eq).trim().toLowerCase();
            String value = line.substring(eq + 1).trim();
            switch (key) {
                case "tags":
                    for (String t : value.split(",")) {
                        // NBT keys are case sensitive -- Enchantments, not
                        // enchantments -- so these are not lowercased.
                        if (!t.trim().isEmpty()) {
                            keys.add(t.trim());
                        }
                    }
                    break;
                case "same_slot_only":
                    slots = Boolean.parseBoolean(value);
                    break;
                default:
                    log("ignoring unknown setting: " + key);
            }
        }
        tags = keys.toArray(new String[0]);
        sameSlotOnly = slots;
        log(keys.isEmpty()
            ? "no tags listed; crafting results carry nothing"
            : "carrying " + String.join(", ", keys)
              + (slots ? " between items of the same equipment slot" : " between any items"));
    }

    @Override
    public String defaultConfig() {
        return "# NBT carried from a crafting ingredient onto the crafted result.\n"
            + "#\n"
            + "#     tags = <root nbt key>[, <root nbt key>...]\n"
            + "#     same_slot_only = true|false\n"
            + "#\n"
            + "# Vanilla builds a crafted item from the recipe alone, so anything an\n"
            + "# ingredient carried is gone the moment it is consumed -- which is what makes\n"
            + "# an armour upgrade recipe eat the affixes, rarity and sockets of the piece\n"
            + "# fed into it. Apotheosis keeps all of that in one compound, affix_data, so\n"
            + "# carrying that single key across is the whole fix.\n"
            + "#\n"
            + "# Add Enchantments to the list to keep enchantments through such a recipe\n"
            + "# too; it is left out by default because the anvil is the intended way to\n"
            + "# move those and it costs levels.\n"
            + "#\n"
            + "# Three rules are fixed, each closing a way this would otherwise go wrong:\n"
            + "#   - the result must be a single item, or one affixed input would pay for a\n"
            + "#     whole stack of affixed outputs\n"
            + "#   - exactly one ingredient may carry the tags; two is ambiguous, so nothing\n"
            + "#     is copied\n"
            + "#   - a tag the result already has is left alone\n"
            + "#\n"
            + "# same_slot_only requires the source and the result to be worn in the same\n"
            + "# slot. Affix attribute modifiers are rolled for the slot the item was found\n"
            + "# in, so turning it off is how you end up with a sword granting armour.\n"
            + "# Everything that is not armour counts as main hand, so weapon-to-weapon and\n"
            + "# tool-to-tool crafting is allowed either way.\n"
            + "#\n"
            + "# Saved edits are picked up within about ten seconds; no restart.\n"
            + "\n"
            + "tags = affix_data\n"
            + "same_slot_only = true\n";
    }
}
