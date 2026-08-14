package digbuild.modsync;

import java.io.IOException;
import java.lang.instrument.Instrumentation;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * In-JVM scheduler for a managed (shell-less) Pterodactyl game server.
 *
 * Runs as a -javaagent so it starts with the JVM, independent of Forge. Every
 * N seconds it fingerprints the mods/ folder and, when the fingerprint changes,
 * fires a GitHub repository_dispatch. The heavy lifting (pull changed jars,
 * build the zip, publish the release) happens on the GitHub runner in response.
 *
 * No external dependencies: everything here is JDK 11+ (server runs Java 17).
 * The token is read from a config file on disk, never baked into this jar.
 */
public final class ModSyncAgent {

    private static final String UA = "digbuild-modsync-agent";

    /** -javaagent entry point (JVM startup). */
    public static void premain(String args, Instrumentation inst) {
        start(args);
    }

    /** dynamic-attach entry point, for completeness. */
    public static void agentmain(String args, Instrumentation inst) {
        start(args);
    }

    /** standalone entry point, for local testing: java -jar agent.jar config.properties */
    public static void main(String[] args) throws InterruptedException {
        start(args.length > 0 ? args[0] : null);
        Thread.currentThread().join();
    }

    private static void start(String configPath) {
        final Properties cfg = loadConfig(configPath);

        final Path modsDir = Paths.get(cfg.getProperty("mods.dir", "/home/container/mods"));
        final Path stateFile = Paths.get(cfg.getProperty("state.file", "/home/container/.modsync-hash"));
        final long interval = parseLong(cfg.getProperty("interval.seconds", "900"), 900);
        final long firstDelay = parseLong(cfg.getProperty("first.delay.seconds", "30"), 30);
        final String repo = cfg.getProperty("github.repo");        // "owner/name"
        final String token = cfg.getProperty("github.token");
        final String event = cfg.getProperty("github.event_type", "mods-changed");

        if (repo == null || repo.isBlank() || token == null || token.isBlank()) {
            log("github.repo and github.token are required; agent idle.");
            return;
        }

        final ScheduledExecutorService exec = Executors.newSingleThreadScheduledExecutor(r -> {
            Thread t = new Thread(r, "modsync-agent");
            t.setDaemon(true);            // must never hold the JVM open on shutdown
            return t;
        });

        exec.scheduleWithFixedDelay(() -> tick(modsDir, stateFile, repo, token, event),
                firstDelay, interval, TimeUnit.SECONDS);

        log("started; watching " + modsDir + " every " + interval + "s -> " + repo);
    }

    private static void tick(Path modsDir, Path stateFile, String repo, String token, String event) {
        try {
            String current = fingerprint(modsDir);
            String previous = readState(stateFile);
            if (current.equals(previous)) {
                return;                    // the common case: nothing to do
            }
            log("mods changed (" + shortHash(previous) + " -> " + shortHash(current) + "); dispatching");
            if (dispatch(repo, token, event, current)) {
                writeState(stateFile, current);
            } else {
                log("dispatch failed; will retry next tick");
            }
        } catch (Throwable t) {            // a bad tick must never kill the schedule
            log("tick error: " + t);
        }
    }

    /** Hash of sorted "name:size:mtime" over every *.jar in the folder. */
    private static String fingerprint(Path modsDir) throws Exception {
        List<String> rows = new ArrayList<>();
        if (Files.isDirectory(modsDir)) {
            try (DirectoryStream<Path> ds = Files.newDirectoryStream(modsDir, "*.jar")) {
                for (Path p : ds) {
                    long size = Files.size(p);
                    long mtime = Files.getLastModifiedTime(p).toMillis();
                    rows.add(p.getFileName() + ":" + size + ":" + mtime);
                }
            }
        }
        Collections.sort(rows);
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        md.update(String.join("\n", rows).getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : md.digest()) {
            sb.append(Character.forDigit((b >> 4) & 0xf, 16));
            sb.append(Character.forDigit(b & 0xf, 16));
        }
        return sb.toString();
    }

    private static boolean dispatch(String repo, String token, String event, String hash) {
        try {
            String body = "{\"event_type\":\"" + event
                    + "\",\"client_payload\":{\"hash\":\"" + hash + "\"}}";
            HttpClient client = HttpClient.newBuilder()
                    .connectTimeout(Duration.ofSeconds(20)).build();
            HttpRequest req = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.github.com/repos/" + repo + "/dispatches"))
                    .timeout(Duration.ofSeconds(30))
                    .header("Authorization", "Bearer " + token)
                    .header("Accept", "application/vnd.github+json")
                    .header("X-GitHub-Api-Version", "2022-11-28")
                    .header("User-Agent", UA)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(body))
                    .build();
            HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
            if (res.statusCode() / 100 == 2) {
                return true;
            }
            log("github " + res.statusCode() + ": " + res.body());
            return false;
        } catch (Exception e) {
            log("dispatch exception: " + e);
            return false;
        }
    }

    private static Properties loadConfig(String path) {
        Properties p = new Properties();
        if (path == null || path.isBlank()) {
            log("no config path passed via -javaagent=...; agent idle.");
            return p;
        }
        try {
            p.load(Files.newBufferedReader(Paths.get(path), StandardCharsets.UTF_8));
        } catch (IOException e) {
            log("cannot read config " + path + ": " + e);
        }
        return p;
    }

    private static String readState(Path f) {
        try {
            return Files.exists(f) ? Files.readString(f, StandardCharsets.UTF_8).trim() : "";
        } catch (IOException e) {
            return "";
        }
    }

    private static void writeState(Path f, String hash) {
        try {
            Files.writeString(f, hash, StandardCharsets.UTF_8);
        } catch (IOException e) {
            log("cannot persist state: " + e);
        }
    }

    private static long parseLong(String s, long def) {
        try {
            return Long.parseLong(s.trim());
        } catch (Exception e) {
            return def;
        }
    }

    private static String shortHash(String h) {
        return (h == null || h.isEmpty()) ? "none" : h.substring(0, Math.min(8, h.length()));
    }

    private static void log(String msg) {
        System.out.println("[modsync] " + msg);
    }

    private ModSyncAgent() {}
}
