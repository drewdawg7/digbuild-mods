package digbuild.tweaks;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import digbuild.tweaks.tweak.CraftCarryover;
import digbuild.tweaks.tweak.EnchantApplicability;

/**
 * The tweak registry, and the reason a config edit does not need a restart.
 *
 * Config files are polled rather than read once: every POLL_TICKS the server
 * stats each file, and a changed size or mtime re-runs that tweak's apply().
 * Two stats every ten seconds is not measurable next to a tick, and it is the
 * only mechanism that needs no command, no /reload of the whole datapack set,
 * and nothing installed on the client -- edit the file through the panel and
 * the next poll picks it up.
 *
 * Only config is live. Changing what a tweak *does*, or adding a mixin, is a
 * rebuild and a restart: mixins are applied by the class transformer when the
 * target class is first loaded and cannot be re-applied afterwards.
 */
public final class Tweaks {

    /** Every tweak. New ones go here and in the mixins config if they need one. */
    private static final List<Tweak> ALL = Arrays.asList(
        new EnchantApplicability(),
        new CraftCarryover()
    );

    /** Relative to the server root, which is the directory Forge boots in. */
    private static final Path DIR = Paths.get("config", "digbuild-tweaks");

    /** 200 ticks is ten seconds at a healthy tick rate, and longer when the
     *  server is struggling -- which is when it should be doing less, not more. */
    private static final int POLL_TICKS = 200;

    private static final Map<String, String> STAMPS = new HashMap<>();

    private static int ticks;

    private Tweaks() {
    }

    /** First pass, at common setup: writes any missing config and applies all. */
    public static void setup() {
        for (Tweak tweak : ALL) {
            refresh(tweak, true);
        }
    }

    /** Called every server tick; does real work POLL_TICKS apart. */
    public static void poll() {
        if (++ticks < POLL_TICKS) {
            return;
        }
        ticks = 0;
        for (Tweak tweak : ALL) {
            refresh(tweak, false);
        }
    }

    private static void refresh(Tweak tweak, boolean first) {
        String name = tweak.config();
        if (name == null) {
            if (first) {
                run(tweak, new ArrayList<>());
            }
            return;
        }
        Path path = DIR.resolve(name);
        try {
            if (!Files.exists(path)) {
                Files.createDirectories(DIR);
                Files.write(path, tweak.defaultConfig().getBytes(StandardCharsets.UTF_8));
                log(tweak.id() + ": wrote default " + path);
            }
            String stamp = stamp(path);
            if (!first && stamp.equals(STAMPS.get(tweak.id()))) {
                return;
            }
            STAMPS.put(tweak.id(), stamp);
            if (!first) {
                log(tweak.id() + ": " + path.getFileName() + " changed, reloading");
            }
            run(tweak, strip(Files.readAllLines(path, StandardCharsets.UTF_8)));
        } catch (IOException e) {
            log(tweak.id() + ": could not read " + path + " (" + e + ")");
        }
    }

    /** A bad config is a bad config, not a dead server: a tweak that throws is
     *  reported and skipped, and the next edit gets another attempt. */
    private static void run(Tweak tweak, List<String> lines) {
        try {
            tweak.apply(lines);
        } catch (Throwable t) {
            log(tweak.id() + ": apply failed (" + t + ")");
        }
    }

    private static String stamp(Path path) throws IOException {
        return Files.getLastModifiedTime(path).toMillis() + ":" + Files.size(path);
    }

    private static List<String> strip(List<String> raw) {
        List<String> out = new ArrayList<>();
        for (String line : raw) {
            int hash = line.indexOf('#');
            String stripped = (hash < 0 ? line : line.substring(0, hash)).trim();
            if (!stripped.isEmpty()) {
                out.add(stripped);
            }
        }
        return out;
    }

    /** stdout, like the heap patch: one prefix, greppable, and no logger to
     *  acquire during mod construction. */
    static void log(String msg) {
        System.out.println("[digbuild] tweaks: " + msg);
    }
}
