package digbuild.modsync;

import net.minecraftforge.fml.common.Mod;

/**
 * Forge entry point. Forge instantiates this during mod construction on every
 * server boot — which is how we run in-JVM without any JVM-arg injection (the
 * host's loader ignores both LOADER_STARTUPFLAGS and user_jvm_args.txt).
 *
 * The constructor just hands off to the agent and returns; the agent runs on
 * its own daemon thread, so mod loading is never blocked.
 */
@Mod("digbuildmodsync")
public final class ModSyncMod {
    public ModSyncMod() {
        String cfg = System.getProperty("modsync.config", "/home/container/modsync.properties");
        ModSyncAgent.launch(cfg);
    }
}
