package digbuild.sync;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Brings mods/ into line with the published manifest.
 *
 * Runs from DigbuildSyncService before Forge has looked at the folder, which is
 * what makes an update land on the launch that downloads it instead of the one
 * after. Two consequences worth keeping in mind when editing this:
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
    /** Downloads land here first, so a half-written jar is never in mods/. */
    private static final String STAGING = ".digbuild-sync";

    /** Where a jar the player added goes when it cannot stay. Never deleted. */
    private static final String DISABLED = ".digbuild-sync-disabled";

    /**
     * This jar does not update itself.
     *
     * By the time any of this runs, its own jar is open on the boot layer --
     * replacing it is impossible on Windows and pointless everywhere else,
     * since the old class is already loaded. Downloading a renamed newer copy
     * would be worse: both would declare the service and both would run.
     *
     * So a new digbuild-sync reaches players the way the first one did, in the
     * pack zip from the wiki. Matched by prefix rather than by the running
     * file's name so a version bump is covered too.
     */
    private static final String SELF_PREFIX = "digbuild-sync";

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

        Manifest manifest;
        try {
            manifest = Manifest.parse(fetch(config.manifestUrl));
        } catch (Exception e) {
            // Offline is the common case here, and a player who cannot reach
            // GitHub should still be able to launch and play single-player.
            log.warn("could not read the manifest; leaving mods/ alone", e);
            return;
        }
        log.info("manifest lists " + manifest.byName().size() + " mods");

        LocalState state = LocalState.load(gameDir, log);
        Map<String, Path> local = listJars();

        // First run adopts the jars that came out of the zip -- anything the
        // manifest also names. A jar the player added is left unmanaged, and
        // unmanaged means never deleted for being absent from the manifest.
        if (state.isFirstRun()) {
            int adopted = 0;
            for (String name : local.keySet()) {
                if (manifest.byName().containsKey(name)) {
                    state.manage(name);
                    adopted++;
                }
            }
            log.info("first run: adopted " + adopted + " of " + local.size() + " jars in mods/");
        }

        List<Manifest.Entry> wanted = new ArrayList<>();
        for (Manifest.Entry entry : manifest.byName().values()) {
            if (isSelf(entry.name())) continue;
            Path path = local.get(entry.name());
            if (path == null || !entry.sha1().equals(hash(path, entry.name(), state))) {
                wanted.add(entry);
            }
        }

        // Managed jars the manifest no longer names: this pack removed them.
        List<String> dropped = new ArrayList<>();
        if (config.removeDropped) {
            for (String name : state.managed()) {
                if (isSelf(name)) continue;
                if (!manifest.byName().containsKey(name) && local.containsKey(name)) {
                    dropped.add(name);
                }
            }
        }

        if (wanted.isEmpty() && dropped.isEmpty()) {
            log.info("mods/ already matches the manifest");
            state.save(local.keySet(), log);
            return;
        }

        long bytes = wanted.stream().mapToLong(Manifest.Entry::size).sum();
        log.info("%d to download (%d MB), %d to remove"
                .formatted(wanted.size(), bytes / (1024 * 1024), dropped.size()));

        Progress progress = Progress.open(wanted.size(), bytes, config.progressWindow);
        try {
            install(wanted, bytes, local, state, progress);
            for (String name : dropped) {
                remove(local.get(name), "dropped from the pack");
                state.unmanage(name);
            }
        } finally {
            progress.close();
        }
        state.save(listJars().keySet(), log);
    }

    /** Downloads, verifies, then moves into place -- one jar at a time. */
    private void install(List<Manifest.Entry> wanted, long totalBytes, Map<String, Path> local,
                         LocalState state, Progress progress) {
        Path staging = modsDir.resolve(STAGING);
        long done = 0;

        for (Manifest.Entry entry : wanted) {
            progress.update(entry.name(), done, totalBytes);
            Path tmp = staging.resolve(entry.name() + ".part");
            try {
                Files.createDirectories(staging);
                download(entry, tmp);

                String got = sha1(tmp);
                if (!got.equals(entry.sha1())) {
                    // A truncated or tampered jar is worse than a missing one:
                    // Forge would fail to read it and abort the boot.
                    throw new IOException("sha1 mismatch: expected " + entry.sha1() + ", got " + got);
                }

                // Before it lands: clear any jar declaring the same mod id. A
                // version bump changes the filename, so the old one is not
                // "dropped" by name and would otherwise duplicate the mod id.
                for (String stale : collisions(tmp, entry.name(), local)) {
                    // Ours to delete only if we installed it. A jar the player
                    // added is moved aside instead: it cannot stay -- Forge
                    // aborts the boot on a duplicate mod id -- but deleting
                    // someone's own mod to fix our own upgrade is not on.
                    if (state.managed().contains(stale)) {
                        remove(local.get(stale), "replaced by " + entry.name());
                    } else {
                        quarantine(local.get(stale), entry.name());
                    }
                    state.unmanage(stale);
                    local.remove(stale);
                }

                Path dest = modsDir.resolve(entry.name());
                Files.move(tmp, dest, StandardCopyOption.REPLACE_EXISTING);
                state.manage(entry.name());
                state.rememberHash(entry.name(), Files.size(dest),
                        Files.getLastModifiedTime(dest).toMillis(), entry.sha1());
                local.put(entry.name(), dest);
                log.info("installed " + entry.name());
            } catch (Exception e) {
                // Keep going: one unreachable jar should cost that mod, not the
                // other 147. The next launch retries it.
                log.warn("could not install " + entry.name(), e);
                try {
                    Files.deleteIfExists(tmp);
                } catch (IOException ignored) {
                }
            }
            done += entry.size();
        }

        try {
            Files.deleteIfExists(staging);  // only succeeds when nothing was left behind
        } catch (IOException ignored) {
        }
    }

    /**
     * Local jars sharing a mod id with the staged one.
     *
     * Deliberately checks ids rather than names, and deliberately applies to
     * unmanaged jars too: a stale copy of a pack mod is a boot failure whoever
     * put it there, and remove_dropped=false turns the whole behaviour off.
     */
    private Set<String> collisions(Path staged, String name, Map<String, Path> local) {
        Set<String> out = new LinkedHashSet<>();
        if (!config.removeDropped) return out;

        Set<String> ids = ModIds.of(staged);
        if (ids.isEmpty()) return out;

        for (Map.Entry<String, Path> e : local.entrySet()) {
            if (e.getKey().equals(name)) continue;  // same file, being replaced in place
            if (isSelf(e.getKey())) continue;
            if (!java.util.Collections.disjoint(ModIds.of(e.getValue()), ids)) {
                out.add(e.getKey());
            }
        }
        return out;
    }

    private static boolean isSelf(String name) {
        return name.startsWith(SELF_PREFIX);
    }

    private void download(Manifest.Entry entry, Path dest) throws IOException, InterruptedException {
        IOException last = null;
        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                HttpRequest req = HttpRequest.newBuilder(URI.create(entry.url()))
                        .timeout(config.timeout)
                        .header("User-Agent", "digbuild-sync")
                        .build();
                HttpResponse<InputStream> res =
                        http.send(req, HttpResponse.BodyHandlers.ofInputStream());
                if (res.statusCode() != 200) {
                    throw new IOException("HTTP " + res.statusCode() + " for " + entry.url());
                }
                try (InputStream in = res.body(); OutputStream out = Files.newOutputStream(dest)) {
                    in.transferTo(out);
                }
                return;
            } catch (IOException e) {
                last = e;
                log.info("retrying " + entry.name() + " (attempt " + attempt + " failed)");
            }
        }
        throw last;
    }

    /**
     * Moves a jar out of mods/ into mods/.digbuild-sync-disabled/.
     *
     * The one case: the player installed their own copy of a mod the pack also
     * ships, and the pack's copy is a different version. Both cannot sit in
     * mods/, and the pack's has to win or the server rejects them -- but the
     * file is theirs, so it is set aside rather than destroyed and the log says
     * where it went.
     */
    private void quarantine(Path jar, String replacedBy) {
        if (jar == null) return;
        try {
            Path parked = modsDir.resolve(DISABLED);
            Files.createDirectories(parked);
            Files.move(jar, parked.resolve(jar.getFileName().toString()),
                    StandardCopyOption.REPLACE_EXISTING);
            log.info("moved " + jar.getFileName() + " to mods/" + DISABLED
                    + " -- it declares the same mod id as " + replacedBy);
        } catch (IOException e) {
            log.warn("could not move " + jar.getFileName() + " aside", e);
        }
    }

    private void remove(Path jar, String why) {
        if (jar == null) return;
        try {
            Files.deleteIfExists(jar);
            log.info("removed " + jar.getFileName() + " -- " + why);
        } catch (IOException e) {
            log.warn("could not remove " + jar.getFileName(), e);
        }
    }

    private Map<String, Path> listJars() {
        Map<String, Path> out = new LinkedHashMap<>();
        // Non-recursive on purpose: .digbuild-sync-disabled/ lives under mods/
        // and its contents are explicitly not part of the pack.
        try (DirectoryStream<Path> jars = Files.newDirectoryStream(modsDir, "*.jar")) {
            for (Path jar : jars) {
                if (Files.isRegularFile(jar)) out.put(jar.getFileName().toString(), jar);
            }
        } catch (IOException e) {
            log.warn("could not list " + modsDir, e);
        }
        return out;
    }

    /** Cached by size and mtime, so an unchanged pack costs one stat per jar. */
    private String hash(Path jar, String name, LocalState state) {
        try {
            long size = Files.size(jar);
            long mtime = Files.getLastModifiedTime(jar).toMillis();
            String cached = state.cachedHash(name, size, mtime);
            if (cached != null) return cached;

            String sha1 = sha1(jar);
            state.rememberHash(name, size, mtime, sha1);
            return sha1;
        } catch (IOException e) {
            log.warn("could not hash " + name, e);
            return "";  // treated as a mismatch, so it is re-downloaded
        }
    }

    private static String sha1(Path file) throws IOException {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-1");
            byte[] buffer = new byte[1 << 16];
            try (InputStream in = Files.newInputStream(file)) {
                for (int n; (n = in.read(buffer)) > 0; ) digest.update(buffer, 0, n);
            }
            StringBuilder sb = new StringBuilder(40);
            for (byte b : digest.digest()) sb.append(Character.forDigit((b >> 4) & 0xf, 16))
                    .append(Character.forDigit(b & 0xf, 16));
            return sb.toString();
        } catch (java.security.NoSuchAlgorithmException e) {
            throw new IOException("no SHA-1 in this JVM", e);
        }
    }

    private String fetch(String url) throws IOException, InterruptedException {
        HttpRequest req = HttpRequest.newBuilder(URI.create(url))
                .timeout(config.timeout)
                .header("User-Agent", "digbuild-sync")
                .build();
        HttpResponse<byte[]> res = http.send(req, HttpResponse.BodyHandlers.ofByteArray());
        if (res.statusCode() != 200) throw new IOException("HTTP " + res.statusCode() + " for " + url);
        return new String(res.body(), StandardCharsets.UTF_8);
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
