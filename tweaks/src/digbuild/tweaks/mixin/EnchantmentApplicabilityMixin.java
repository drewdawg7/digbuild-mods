package digbuild.tweaks.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import digbuild.tweaks.tweak.EnchantApplicability;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;

/**
 * Widens enchantment applicability for the pairings in the allowlist.
 *
 * Two checks, because the anvil and the enchanting table do not share one.
 * Traced through the Forge-patched classes on this server rather than assumed:
 *
 *   anvil / /enchant   Enchantment.canEnchant   (m_6081_), which by default is
 *                      this.category.canEnchant(item)
 *   enchanting table   EnchantmentHelper.getAvailableEnchantmentResults calls
 *                      Enchantment.canApplyAtEnchantingTable(stack), a Forge
 *                      addition, which bounces to the item and lands in
 *                      IForgeItem's default -- and that reads the category
 *                      directly, never canEnchant. Patching canEnchant alone
 *                      would put the enchantment on the anvil and leave it off
 *                      the table.
 *
 * Both inject at HEAD and only ever cancel with true, so an enchantment the
 * allowlist says nothing about takes the vanilla path untouched.
 *
 * SRG names with remap=false: built with plain javac, no refmap, and SRG is
 * what the Forge runtime uses. canApplyAtEnchantingTable is Forge's own and
 * keeps its name. verify_patch.py checks both against the server's jars.
 */
@Mixin(value = Enchantment.class, remap = false)
public abstract class EnchantmentApplicabilityMixin {

    @Inject(
        method = "m_6081_(Lnet/minecraft/world/item/ItemStack;)Z",
        at = @At("HEAD"),
        cancellable = true,
        remap = false
    )
    private void digbuild$widenCanEnchant(ItemStack stack, CallbackInfoReturnable<Boolean> cir) {
        if (EnchantApplicability.allows((Enchantment) (Object) this, stack)) {
            cir.setReturnValue(Boolean.TRUE);
        }
    }

    @Inject(
        method = "canApplyAtEnchantingTable(Lnet/minecraft/world/item/ItemStack;)Z",
        at = @At("HEAD"),
        cancellable = true,
        remap = false
    )
    private void digbuild$widenTable(ItemStack stack, CallbackInfoReturnable<Boolean> cir) {
        if (EnchantApplicability.allows((Enchantment) (Object) this, stack)) {
            cir.setReturnValue(Boolean.TRUE);
        }
    }
}
