package digbuild.patch.mixin;

import java.util.Iterator;
import java.util.Map;

import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Bounds StructureTemplateManager's template cache.
 *
 * f_230345_ is a plain ConcurrentHashMap filled by computeIfAbsent and never
 * evicted -- every structure template the server ever loads stays resident for
 * the session. With this mod set that is the leak: measured 6,523,851
 * StructureBlockInfo and 6,537,678 BlockPos live, 16x what they were an hour
 * earlier, growing the live set 762 -> 1182 MiB and the committed floor with it.
 *
 * A web map's render is what drives it -- walking every tile loads every chunk,
 * which loads structures -- but the unbounded cache is what turns that traffic
 * into permanent residency, and any map mod produces the same traffic.
 *
 * Vanilla clears this same map wholesale on resource reload, so dropping
 * entries is a supported operation; anything evicted is re-read on next use.
 * Eviction goes to a low-water mark rather than clear() so a render in progress
 * does not repeatedly reload its whole working set.
 *
 * SRG names with remap=false: this is built with plain javac and has no refmap,
 * and SRG is what the Forge runtime actually uses. verify_patch.py checks both
 * names against the server's own srg jar.
 */
@Mixin(targets = "net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager", remap = false)
public abstract class StructureTemplateCacheMixin {

    /** Templates kept before eviction kicks in. */
    private static final int DIGBUILD_CAP = 1024;
    /** Evict down to this, so eviction is occasional rather than per-insert. */
    private static final int DIGBUILD_LOW_WATER = 768;

    @Shadow
    @Final
    private Map f_230345_;

    @Inject(
        method = "m_230407_(Lnet/minecraft/resources/ResourceLocation;)Ljava/util/Optional;",
        at = @At("RETURN"),
        remap = false
    )
    @SuppressWarnings("rawtypes")
    private void digbuild$boundTemplateCache(CallbackInfoReturnable cir) {
        Map cache = this.f_230345_;
        if (cache == null || cache.size() <= DIGBUILD_CAP) {
            return;
        }
        // ConcurrentHashMap has no ordering to exploit, and a cache does not
        // need one -- drop arbitrary entries until back under the mark. The
        // iterator is weakly consistent, so this is safe against concurrent
        // worldgen threads.
        Iterator<?> it = cache.keySet().iterator();
        while (cache.size() > DIGBUILD_LOW_WATER && it.hasNext()) {
            it.next();
            it.remove();
        }
    }
}
