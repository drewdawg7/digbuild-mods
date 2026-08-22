package digbuild.sync;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/**
 * The mod ids a jar declares, read straight out of its META-INF/mods.toml.
 *
 * This exists for one case: a version bump renames the file, so the old jar is
 * not "dropped from the manifest" by name -- it is simply a filename nobody
 * mentions. Left in place, Forge aborts the boot on the duplicate mod id, so
 * the player gets a broken game rather than an untouched one. Matching ids is
 * what makes "replace jei-15.2.0 with jei-15.3.0" different from "delete a mod
 * the player added".
 *
 * A regex rather than a TOML parser because the only shape that matters is
 * `modId="x"` at the head of a [[mods]] block, and pulling in a parser for one
 * line would be the largest dependency in the jar.
 */
final class ModIds {
    private static final Pattern MOD_ID = Pattern.compile(
            "(?m)^\\s*modId\\s*=\\s*[\"']([a-z0-9_.-]+)[\"']");

    private ModIds() {}

    static Set<String> of(Path jar) {
        Set<String> ids = new LinkedHashSet<>();
        try (ZipFile zip = new ZipFile(jar.toFile())) {
            ZipEntry entry = zip.getEntry("META-INF/mods.toml");
            if (entry == null) return ids;  // a library jar, or this very service
            try (InputStream in = zip.getInputStream(entry)) {
                Matcher m = MOD_ID.matcher(new String(in.readAllBytes(), StandardCharsets.UTF_8));
                while (m.find()) ids.add(m.group(1));
            }
        } catch (IOException | RuntimeException e) {
            // An unreadable jar yields no ids, which means it is never treated
            // as colliding -- the conservative direction: keep the file.
            return ids;
        }
        return ids;
    }
}
