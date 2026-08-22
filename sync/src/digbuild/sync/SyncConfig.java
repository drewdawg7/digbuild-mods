package digbuild.sync;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.Properties;

/**
 * config/digbuild-sync.properties -- written with defaults on first launch so
 * the switch is discoverable in the folder the player already edits, rather
 * than being a key they have to be told about.
 *
 * Read once per launch and never re-read: everything here is consumed before
 * the game window exists, so there is no live-reload to offer.
 */
final class SyncConfig {
    static final String FILE = "digbuild-sync.properties";

    /**
     * A fixed URL, deliberately not the /latest/ redirect: this is asked on
     * every launch, so the answer has to exist even when the pack has not
     * published a release in weeks. mod-store is the one release that is never
     * pruned, and the manifest is replaced in place each time it is rebuilt.
     */
    private static final String DEFAULT_MANIFEST =
            "https://github.com/drewdawg7/digbuild-mods/releases/download/mod-store/mods-manifest.tsv";

    private static final String TEMPLATE = """
            # digbuild-sync -- pulls new mods at launch, before Forge reads mods/.
            #
            # enabled: the master switch. false stops every network call and
            # every write; the pack then only changes when you change it, the
            # way it did before this jar existed.
            enabled = true

            # Where the published mod list lives. Points at the newest release
            # of drewdawg7/digbuild-mods; change it only to test against another.
            manifest = %s

            # Clean up jars the pack no longer uses. Deletes only files this
            # jar installed itself. A mod you installed that clashes with a pack
            # mod -- same mod id, different version -- is moved into
            # mods/.digbuild-sync-disabled/ instead, because Forge will not boot
            # with both; nothing you added is ever deleted.
            remove_dropped = true

            # Seconds to wait on the manifest fetch and on each jar. A slow
            # connection should hold up the boot; a dead host should not.
            timeout_seconds = 60

            # Show a progress window while downloading. Off means the boot just
            # appears to take longer, so leave it on unless it misbehaves.
            progress_window = true
            """.formatted(DEFAULT_MANIFEST);

    final boolean enabled;
    final String manifestUrl;
    final boolean removeDropped;
    final Duration timeout;
    final boolean progressWindow;

    private SyncConfig(Properties p) {
        this.enabled = bool(p, "enabled", true);
        this.manifestUrl = p.getProperty("manifest", DEFAULT_MANIFEST).trim();
        this.removeDropped = bool(p, "remove_dropped", true);
        this.timeout = Duration.ofSeconds(integer(p, "timeout_seconds", 60));
        this.progressWindow = bool(p, "progress_window", true);
    }

    static SyncConfig load(Path gameDir, SyncLog log) {
        Path file = gameDir.resolve("config").resolve(FILE);
        Properties p = new Properties();

        if (Files.isRegularFile(file)) {
            try (InputStream in = Files.newInputStream(file)) {
                p.load(in);
            } catch (IOException e) {
                // Defaults rather than a dead boot: an unreadable config should
                // not be the thing that stops a player launching.
                log.warn("could not read " + FILE + "; using defaults", e);
            }
        } else {
            try {
                Files.createDirectories(file.getParent());
                Files.writeString(file, TEMPLATE, StandardCharsets.UTF_8);
                log.info("wrote config/" + FILE);
            } catch (IOException e) {
                log.warn("could not write config/" + FILE, e);
            }
            try {
                p.load(new java.io.StringReader(TEMPLATE));
            } catch (IOException ignored) {
            }
        }
        return new SyncConfig(p);
    }

    private static boolean bool(Properties p, String key, boolean fallback) {
        String v = p.getProperty(key);
        return v == null ? fallback : Boolean.parseBoolean(v.trim());
    }

    private static int integer(Properties p, String key, int fallback) {
        try {
            String v = p.getProperty(key);
            return v == null ? fallback : Math.max(1, Integer.parseInt(v.trim()));
        } catch (NumberFormatException e) {
            return fallback;
        }
    }
}
