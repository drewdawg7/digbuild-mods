package digbuild.sync;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

/**
 * Stdout plus logs/digbuild-sync.log.
 *
 * Not slf4j: this runs during transformer discovery, before Forge has
 * configured logging, so anything routed through log4j at that point either
 * vanishes or initialises the logging system earlier than Forge expects. A
 * plain file is also what a player can be asked for when a sync misbehaves --
 * latest.log does not start until much later in the boot.
 */
final class SyncLog {
    private static final DateTimeFormatter CLOCK = DateTimeFormatter.ofPattern("HH:mm:ss");

    private final Path file;

    SyncLog(Path gameDir) {
        Path f = null;
        try {
            Path logs = gameDir.resolve("logs");
            Files.createDirectories(logs);
            f = logs.resolve("digbuild-sync.log");
            // Truncated per launch. The interesting failure is always the one
            // that just happened, and an append-forever file in logs/ is litter.
            Files.writeString(f, "", StandardCharsets.UTF_8);
        } catch (IOException ignored) {
            // A read-only or missing game dir is not a reason to stop syncing.
        }
        this.file = f;
    }

    void info(String message) {
        String line = "[" + LocalTime.now().format(CLOCK) + "] [digbuild-sync] " + message;
        System.out.println(line);
        if (file == null) return;
        try {
            Files.writeString(file, line + System.lineSeparator(), StandardCharsets.UTF_8,
                    StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (IOException ignored) {
        }
    }

    void warn(String message, Throwable cause) {
        StringWriter sw = new StringWriter();
        if (cause != null) cause.printStackTrace(new PrintWriter(sw));
        info("WARN " + message + (cause == null ? "" : System.lineSeparator() + sw));
    }
}
