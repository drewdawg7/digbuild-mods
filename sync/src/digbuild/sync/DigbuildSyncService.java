package digbuild.sync;

import cpw.mods.modlauncher.api.IEnvironment;
import cpw.mods.modlauncher.api.ITransformer;
import cpw.mods.modlauncher.api.ITransformationService;
import java.nio.file.Path;
import java.util.List;
import java.util.Set;

/**
 * digbuild-sync: pulls new mods at launch, before Forge reads mods/.
 *
 * A ModLauncher service rather than a Forge mod, because a mod cannot add mods.
 * ModDirTransformerDiscoverer scans mods/ for jars declaring this service and
 * hoists them onto the boot layer ahead of everything else, so a jar downloaded
 * here is in place before ModsFolderLocator lists the directory and loads on
 * the same launch. No restart, and no fighting Windows over a jar the game
 * already has open.
 *
 * That is also why this jar carries no mods.toml: ModsFolderLocator skips
 * anything in ModDirTransformerDiscoverer.allExcluded(), which is exactly the
 * service jars, so Forge never scans it and never wants one. One jar cannot be
 * both, which is the reason there is no in-game UI here -- the switch is
 * config/digbuild-sync.properties.
 *
 * Transforms nothing. ITransformationService is the hook that runs early
 * enough; the transformer list is empty on purpose.
 */
public final class DigbuildSyncService implements ITransformationService {

    @Override
    public String name() {
        return "digbuild-sync";
    }

    @Override
    public void onLoad(IEnvironment env, Set<String> otherServices) {
        // Nothing here: GAMEDIR and LAUNCHTARGET are set by processArguments,
        // which modlauncher runs after every onLoad and before every
        // initialize. Verified in TransformationServicesHandler -- doing the
        // work here would read an empty game directory.
    }

    @Override
    public void initialize(IEnvironment env) {
        Path gameDir = env.getProperty(IEnvironment.Keys.GAMEDIR.get()).orElse(null);
        if (gameDir == null) return;

        SyncLog log = new SyncLog(gameDir);
        try {
            String target = env.getProperty(IEnvironment.Keys.LAUNCHTARGET.get()).orElse("");

            // The jar ships inside the pack, so it also sits in the game
            // server's mods/ and gets loaded there. Syncing a server against
            // the manifest built from that same server is a loop, so the server
            // side is simply not a thing this does.
            if (!target.toLowerCase().contains("client")) {
                log.info("launch target '" + target + "' is not a client; nothing to do");
                return;
            }

            new SyncCore(gameDir, SyncConfig.load(gameDir, log), log).run();
        } catch (Throwable t) {
            // Nothing this service does is worth a failed launch. Every path
            // below here already handles its own errors; this is the backstop
            // for the ones that are not errors, like a SecurityManager.
            log.warn("sync aborted", t);
        }
    }

    @Override
    public List<ITransformer> transformers() {
        return List.of();
    }
}
