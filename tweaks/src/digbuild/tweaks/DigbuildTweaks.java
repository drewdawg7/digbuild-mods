package digbuild.tweaks;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

/** Entrypoint. Nothing happens during construction: tweaks read registries,
 *  and those are only populated and frozen by common setup. The tick listener
 *  is what makes config edits live -- see Tweaks. */
@Mod("digbuildtweaks")
public class DigbuildTweaks {

    public DigbuildTweaks() {
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::setup);
        MinecraftForge.EVENT_BUS.addListener(this::tick);
    }

    private void setup(FMLCommonSetupEvent event) {
        // enqueueWork would be later than necessary: nothing here touches the
        // server, only frozen registries and the config directory.
        Tweaks.setup();
    }

    private void tick(TickEvent.ServerTickEvent event) {
        if (event.phase == TickEvent.Phase.END) {
            Tweaks.poll();
        }
    }
}
