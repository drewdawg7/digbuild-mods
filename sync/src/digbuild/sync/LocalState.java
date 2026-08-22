package digbuild.sync;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashSet;
import java.util.Properties;
import java.util.Set;
import java.util.TreeSet;

/**
 * config/digbuild-sync-state.properties -- what this jar installed, and a hash
 * cache so a launch that changes nothing does not re-read 466 MB.
 *
 * Two roles, one file:
 *
 *   managed = a\|b\|c            filenames this jar put in mods/
 *   hash.<filename> = <size>:<mtimeMillis>:<sha1>
 *
 * The managed set is the whole of the deletion safety. A jar that is not in it
 * was put there by the player, so it is never removed on the strength of the
 * manifest alone.
 */
final class LocalState {
    private static final String FILE = "digbuild-sync-state.properties";

    private final Path file;
    private final Properties props = new Properties();
    private final Set<String> managed = new LinkedHashSet<>();

    private LocalState(Path file) {
        this.file = file;
    }

    static LocalState load(Path gameDir, SyncLog log) {
        LocalState s = new LocalState(gameDir.resolve("config").resolve(FILE));
        if (Files.isRegularFile(s.file)) {
            try (InputStream in = Files.newInputStream(s.file)) {
                s.props.load(in);
            } catch (IOException e) {
                log.warn("could not read " + FILE + "; treating this as a first run", e);
            }
        }
        String m = s.props.getProperty("managed", "");
        for (String name : m.split("\\|")) {
            if (!name.isBlank()) s.managed.add(name);
        }
        return s;
    }

    boolean isFirstRun() {
        return props.isEmpty();
    }

    Set<String> managed() {
        return managed;
    }

    void manage(String name) {
        managed.add(name);
    }

    void unmanage(String name) {
        managed.remove(name);
        props.remove("hash." + name);
    }

    /** Cached sha1, or null when the file has changed under us since. */
    String cachedHash(String name, long size, long mtime) {
        String v = props.getProperty("hash." + name);
        if (v == null) return null;
        String[] f = v.split(":");
        if (f.length != 3) return null;
        return (f[0].equals(Long.toString(size)) && f[1].equals(Long.toString(mtime))) ? f[2] : null;
    }

    void rememberHash(String name, long size, long mtime, String sha1) {
        props.setProperty("hash." + name, size + ":" + mtime + ":" + sha1);
    }

    /** Drops cache rows for files that are gone, so the file cannot grow forever. */
    void save(Set<String> present, SyncLog log) {
        for (String key : new TreeSet<>(props.stringPropertyNames())) {
            if (key.startsWith("hash.") && !present.contains(key.substring(5))) {
                props.remove(key);
            }
        }
        props.setProperty("managed", String.join("|", managed));
        try {
            Files.createDirectories(file.getParent());
            try (OutputStream out = Files.newOutputStream(file)) {
                props.store(out, "written by digbuild-sync -- deleting this makes the "
                        + "next launch adopt whatever is in mods/ as the pack");
            }
        } catch (IOException e) {
            log.warn("could not write " + FILE + "; the next launch will re-hash mods/", e);
        }
    }
}
