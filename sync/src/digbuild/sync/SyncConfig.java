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

    /** The same file, and the same link, the wiki's install page hands out. */
    private static final String DEFAULT_PACK =
            "https://github.com/drewdawg7/digbuild-mods/releases/latest/download/mods-latest.zip";

    /** Printed on the wiki's install page; not a secret, just packaging. */
    private static final String DEFAULT_PASSWORD = "digbuild-lfxwgd";

    private static final String TEMPLATE = """
            # digbuild-sync -- pulls new mods at launch, before Forge reads mods/.
            #
            # enabled: the master switch. false stops every network call and
            # every write; the pack then only changes when you change it, the
            # way it did before this jar existed.
            enabled = true

            # The pack itself -- the same download the wiki hands out, and the
            # password printed on the same page. Change these only to test
            # against another pack.
            pack = %s
            password = %s

            # Seconds to wait on the download. A slow connection should hold up
            # the boot; a dead host should not.
            timeout_seconds = 60

            # Show a progress window while downloading. Off means the boot just
            # appears to take longer, so leave it on unless it misbehaves.
            progress_window = true
            """.formatted(DEFAULT_PACK, DEFAULT_PASSWORD);

    final boolean enabled;
    final String packUrl;
    final String password;
    final Duration timeout;
    final boolean progressWindow;

    private SyncConfig(Properties p) {
        this.enabled = bool(p, "enabled", true);
        this.packUrl = p.getProperty("pack", DEFAULT_PACK).trim();
        this.password = p.getProperty("password", DEFAULT_PASSWORD).trim();
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
