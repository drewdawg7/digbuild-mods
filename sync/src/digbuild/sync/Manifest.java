package digbuild.sync;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The published mod list: one tab-separated row per jar.
 *
 *   #digbuild-sync 1
 *   <sha1>\t<size>\t<filename>\t<url>
 *
 * Tab-separated rather than JSON because both ends are ours and neither has a
 * JSON parser -- the client is stdlib-only Java and the publisher is stdlib-only
 * Python, so a format needing no library on either side costs nothing and keeps
 * the diff in a release readable. Tab rather than space because mod filenames
 * contain spaces often enough to matter.
 *
 * The url is carried per row rather than derived from the filename so the
 * storage layout can move without every installed client needing a new jar.
 */
record Manifest(Map<String, Entry> byName) {

    record Entry(String sha1, long size, String name, String url) {}

    static final int VERSION = 1;

    static Manifest parse(String body) {
        Map<String, Entry> out = new LinkedHashMap<>();
        List<String> lines = body.lines().toList();

        if (lines.isEmpty() || !lines.get(0).startsWith("#digbuild-sync ")) {
            throw new IllegalArgumentException("not a digbuild-sync manifest");
        }
        int version = Integer.parseInt(lines.get(0).substring("#digbuild-sync ".length()).trim());
        if (version != VERSION) {
            // Forward compatibility is the publisher's problem, not something to
            // guess at here: a client that cannot read the format must say so
            // and leave mods/ alone rather than act on half of it.
            throw new IllegalArgumentException(
                    "manifest is version " + version + ", this jar reads " + VERSION
                            + " -- reinstall the pack from the wiki");
        }

        List<String> malformed = new ArrayList<>();
        for (String line : lines.subList(1, lines.size())) {
            if (line.isBlank() || line.startsWith("#")) continue;
            String[] f = line.split("\t");
            if (f.length != 4) {
                malformed.add(line);
                continue;
            }
            try {
                out.put(f[2], new Entry(f[0].toLowerCase(), Long.parseLong(f[1]), f[2], f[3]));
            } catch (NumberFormatException e) {
                malformed.add(line);
            }
        }
        if (!malformed.isEmpty()) {
            throw new IllegalArgumentException(malformed.size() + " malformed manifest rows");
        }
        if (out.isEmpty()) {
            // Same guard sync_mods.py carries at the other end: an empty listing
            // is far more likely to be a broken publish than a pack with no
            // mods, and acting on it would delete everything.
            throw new IllegalArgumentException("manifest lists no mods");
        }
        return new Manifest(out);
    }
}
