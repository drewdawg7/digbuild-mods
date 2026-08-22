package digbuild.sync;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.zip.CRC32;

/**
 * Downloads the published pack zip and extracts what the player is missing.
 *
 * The zip is what the pipeline already produces and what the wiki already hands
 * out; this reads the same file, so nothing about publishing changes. Runs from
 * DigbuildSyncService before Forge has looked at mods/, which is what makes an
 * update land on the launch that downloads it rather than the one after. Two
 * consequences worth keeping in mind when editing this:
 *
 *   - nothing here may touch a Minecraft or Forge class. The game's class
 *     loader does not exist yet; this is stdlib only, and that is a constraint
 *     rather than a style choice.
 *   - no jar in mods/ is open yet, so replacing one is an ordinary file move.
 *     That is why this works on Windows, where the same operation is impossible
 *     from inside a running game.
 *
 * Also runnable standalone -- see main() -- which is how verify_sync.py
 * exercises it without a Minecraft install.
 */
public final class SyncCore {
    /** The download and the extraction land here first, never in mods/ directly. */
    private static final String STAGING = ".digbuild-sync";

    /**
     * This jar does not update itself.
     *
     * By the time any of this runs, its own jar is open on the boot layer --
     * replacing it is impossible on Windows and pointless everywhere else,
     * since the old class is already loaded. Extracting a renamed newer copy
     * would be worse: both would declare the service and both would run.
     *
     * So a new digbuild-sync reaches players the way the first one did, in the
     * pack zip they downloaded by hand. Matched by prefix rather than by the
     * running file's name so a version bump is covered too.
     */
    private static final String SELF_PREFIX = "digbuild-sync";

    /** The pack ships its own list of what to delete. */
    private static final String REMOVALS = "remove-mods.txt";

    private final Path gameDir;
    private final Path modsDir;
    private final SyncConfig config;
    private final SyncLog log;
    private final HttpClient http;

    SyncCore(Path gameDir, SyncConfig config, SyncLog log) {
        this.gameDir = gameDir;
        this.modsDir = gameDir.resolve("mods");
        this.config = config;
        this.log = log;
        this.http = HttpClient.newBuilder()
                .followRedirects(HttpClient.Redirect.NORMAL)  // /latest/ is a redirect, twice
                .connectTimeout(config.timeout)
                .build();
    }

    void run() {
        if (!config.enabled) {
            log.info("disabled in config/" + SyncConfig.FILE);
            return;
        }
        if (!Files.isDirectory(modsDir)) {
            log.info("no mods folder at " + modsDir + "; nothing to sync");
            return;
        }

        Path staging = modsDir.resolve(STAGING);
        Path zip = staging.resolve("pack.zip");
        Progress progress = null;
        try {
            Files.createDirectories(staging);

            String tag = download(zip);
            if (tag == null) {
                log.info("pack is unchanged since the last launch");
                return;
            }

            progress = Progress.open(config.progressWindow);
            extract(zip, progress);
            rememberTag(tag);
        } catch (Exception e) {
            // Offline is the common case, and a player who cannot reach GitHub
            // should still be able to launch and play.
            log.warn("could not update the pack; leaving mods/ alone", e);
        } finally {
            if (progress != null) progress.close();
            try {
                Files.deleteIfExists(zip);
                Files.deleteIfExists(staging);
            } catch (IOException ignored) {
            }
        }
    }

    /**
     * Fetches the pack, or returns null when there is nothing new.
     *
     * The zip is hundreds of megabytes and most launches change nothing, so the
     * ETag of the last one that was extracted is sent back as If-None-Match and
     * an unchanged pack costs one request that returns 304 and no body.
     */
    private String download(Path dest) throws IOException, InterruptedException {
        HttpRequest.Builder req = HttpRequest.newBuilder(URI.create(config.packUrl))
                .timeout(config.timeout)
                .header("User-Agent", "digbuild-sync");

        String seen = lastTag();
        if (seen != null && !seen.isEmpty()) req.header("If-None-Match", seen);

        log.info("checking " + config.packUrl);
        HttpResponse<InputStream> res = http.send(req.build(), HttpResponse.BodyHandlers.ofInputStream());
        try (InputStream in = res.body()) {
            if (res.statusCode() == 304) return null;
            if (res.statusCode() != 200) throw new IOException("HTTP " + res.statusCode());

            long length = res.headers().firstValueAsLong("Content-Length").orElse(-1);
            log.info("downloading the pack" + (length > 0 ? " (" + length / (1024 * 1024) + " MB)" : ""));
            try (OutputStream out = Files.newOutputStream(dest)) {
                in.transferTo(out);
            }
        }
        // No ETag is not an error; it just means the next launch downloads again.
        return res.headers().firstValue("ETag").orElse("");
    }

    /** Writes every jar the player does not already have, byte for byte. */
    private void extract(Path zip, Progress progress) throws IOException {
        try (EncryptedZip pack = EncryptedZip.open(zip)) {
            List<EncryptedZip.Entry> jars = new ArrayList<>();
            EncryptedZip.Entry removals = null;

            for (EncryptedZip.Entry entry : pack.entries()) {
                String name = fileName(entry.name());
                if (name.equals(REMOVALS)) {
                    removals = entry;
                } else if (name.endsWith(".jar") && !name.startsWith(SELF_PREFIX)) {
                    jars.add(entry);
                }
            }
            log.info("pack contains " + jars.size() + " mods");

            int written = 0;
            for (int i = 0; i < jars.size(); i++) {
                EncryptedZip.Entry entry = jars.get(i);
                String name = fileName(entry.name());
                progress.update(name, i, jars.size());

                if (matches(modsDir.resolve(name), entry)) continue;

                Path tmp = zip.resolveSibling(name + ".part");
                Files.write(tmp, pack.contents(entry, config.password));
                Files.move(tmp, modsDir.resolve(name), StandardCopyOption.REPLACE_EXISTING);
                log.info("installed " + name);
                written++;
            }

            log.info(written == 0 ? "every mod was already up to date"
                                  : "installed " + written + " mod" + (written == 1 ? "" : "s"));

            if (removals != null) {
                applyRemovals(new String(pack.contents(removals, config.password),
                        StandardCharsets.UTF_8));
            }
        }
    }

    /**
     * Deletes the mods the pack says to delete.
     *
     * remove-mods.txt is the list the pipeline already maintains and the wiki
     * already tells players to action by hand -- extracting a zip adds and
     * overwrites but never removes, and a mod left behind is sometimes a boot
     * failure rather than dead weight. Only names on that list are touched, so
     * a mod the player added themselves is never one of them.
     */
    private void applyRemovals(String listing) {
        int removed = 0;
        for (String line : listing.split("\\R")) {
            String name = line.trim();
            if (name.isEmpty() || name.startsWith("#")) continue;
            if (name.startsWith(SELF_PREFIX)) continue;

            Path jar = modsDir.resolve(fileName(name));
            if (!Files.isRegularFile(jar)) continue;
            try {
                Files.delete(jar);
                log.info("removed " + name + " -- dropped from the pack");
                removed++;
            } catch (IOException e) {
                log.warn("could not remove " + name, e);
            }
        }
        if (removed > 0) log.info("removed " + removed + " mod" + (removed == 1 ? "" : "s"));
    }

    /** True when the file on disk is already exactly this entry. */
    private boolean matches(Path jar, EncryptedZip.Entry entry) {
        try {
            if (!Files.isRegularFile(jar) || Files.size(jar) != entry.size()) return false;

            // Size alone would miss a rebuilt jar of identical length, and the
            // zip carries a CRC for every entry, so the comparison is free of
            // any extra bookkeeping on our side.
            CRC32 crc = new CRC32();
            byte[] buffer = new byte[1 << 16];
            try (InputStream in = Files.newInputStream(jar)) {
                for (int n; (n = in.read(buffer)) > 0; ) crc.update(buffer, 0, n);
            }
            return crc.getValue() == entry.crc();
        } catch (IOException e) {
            return false;  // unreadable: treat as missing and rewrite it
        }
    }

    /** Zip entries may carry a directory prefix; mods/ is flat. */
    private static String fileName(String entryName) {
        int slash = entryName.lastIndexOf('/');
        return slash < 0 ? entryName : entryName.substring(slash + 1);
    }

    private Path tagFile() {
        return gameDir.resolve("config").resolve("digbuild-sync-state.properties");
    }

    private String lastTag() {
        Properties p = new Properties();
        try (InputStream in = Files.newInputStream(tagFile())) {
            p.load(in);
        } catch (IOException e) {
            return null;  // first launch, or the file was cleared to force a refetch
        }
        return p.getProperty("etag");
    }

    private void rememberTag(String tag) {
        Properties p = new Properties();
        p.setProperty("etag", tag);
        try {
            Files.createDirectories(tagFile().getParent());
            try (OutputStream out = Files.newOutputStream(tagFile())) {
                p.store(out, "written by digbuild-sync -- delete this to force a full re-check");
            }
        } catch (IOException e) {
            log.warn("could not record the pack version; the next launch will re-download", e);
        }
    }

    /** Standalone entry point: java -cp ... digbuild.sync.SyncCore <gamedir> */
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("usage: SyncCore <gamedir>");
            System.exit(2);
        }
        Path gameDir = Path.of(args[0]);
        SyncLog log = new SyncLog(gameDir);
        new SyncCore(gameDir, SyncConfig.load(gameDir, log), log).run();
    }
}
