package digbuild.tweaks.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import digbuild.tweaks.tweak.CraftCarryover;
import net.minecraft.core.RegistryAccess;
import net.minecraft.world.inventory.CraftingContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.ShapedRecipe;
import net.minecraft.world.item.crafting.ShapelessRecipe;

/**
 * Post-processes the crafted result of the two vanilla recipe types.
 *
 * assemble() is the right seam, and the menu is the wrong one: FastWorkbench
 * @Overwrites CraftingMenu.slotsChanged and routes the whole grid through its
 * own FastBenchUtil.slotChangedCraftingGrid, so an injector on vanilla's
 * CraftingMenu.slotChangedCraftingGrid would never fire for a crafting table on
 * this server. Everything -- vanilla menus, FastWorkbench, JEI's recipe
 * transfer, any automation mod -- goes through the recipe, and the result slot
 * previews what assemble() returns, so the affixes are visible before the craft
 * rather than appearing on take.
 *
 * Both types return this.result.copy(), so the value handed back at RETURN is a
 * fresh stack and mutating it cannot touch the recipe's own result template.
 * The bridge overload taking a plain Container is deliberately not targeted --
 * it delegates here, and hooking both would apply twice.
 *
 * SRG names with remap=false, checked by verify_patch.py.
 */
@Mixin(value = { ShapedRecipe.class, ShapelessRecipe.class }, remap = false)
public abstract class CraftingCarryoverMixin {

    @Inject(
        method = "m_5874_(Lnet/minecraft/world/inventory/CraftingContainer;Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/item/ItemStack;",
        at = @At("RETURN"),
        remap = false
    )
    private void digbuild$carryIngredientData(CraftingContainer grid, RegistryAccess registries,
                                              CallbackInfoReturnable<ItemStack> cir) {
        CraftCarryover.carry(grid, cir.getReturnValue());
    }
}
