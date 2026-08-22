package digbuild.sync;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GraphicsEnvironment;
import javax.swing.BorderFactory;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.SwingUtilities;
import javax.swing.WindowConstants;

/**
 * A progress window for the download.
 *
 * Needed because of where this runs: transformer discovery is before Minecraft
 * has opened a window, so a large download is a black screen and a launcher
 * that looks hung. Swing is the only toolkit available that early, and it is in
 * the JDK.
 *
 * Every method swallows its own failures. A missing display, a headless CI run
 * or a hostile window manager must cost the player a progress bar, never a
 * launch.
 */
final class Progress {
    private JDialog dialog;
    private JProgressBar bar;
    private JLabel status;

    static Progress open(int fileCount, long totalBytes, boolean wanted) {
        Progress p = new Progress();
        if (!wanted || GraphicsEnvironment.isHeadless()) return p;
        try {
            SwingUtilities.invokeAndWait(() -> p.build(fileCount, totalBytes));
        } catch (Exception ignored) {
        }
        return p;
    }

    private void build(int fileCount, long totalBytes) {
        dialog = new JDialog((java.awt.Frame) null, "digbuild", false);
        dialog.setDefaultCloseOperation(WindowConstants.DO_NOTHING_ON_CLOSE);

        bar = new JProgressBar(0, 1000);
        status = new JLabel("Preparing...");

        JPanel panel = new JPanel(new BorderLayout(0, 8));
        panel.setBorder(BorderFactory.createEmptyBorder(16, 16, 16, 16));
        panel.add(new JLabel("Updating mods: %d file%s, %s"
                .formatted(fileCount, fileCount == 1 ? "" : "s", mb(totalBytes))), BorderLayout.NORTH);
        panel.add(bar, BorderLayout.CENTER);
        panel.add(status, BorderLayout.SOUTH);

        dialog.setContentPane(panel);
        dialog.setPreferredSize(new Dimension(460, 140));
        dialog.pack();
        dialog.setLocationRelativeTo(null);
        dialog.setAlwaysOnTop(true);
        dialog.setVisible(true);
    }

    void update(String file, long done, long total) {
        if (dialog == null) return;
        int permille = total <= 0 ? 0 : (int) Math.min(1000, done * 1000 / total);
        SwingUtilities.invokeLater(() -> {
            bar.setValue(permille);
            status.setText(file);
        });
    }

    void close() {
        if (dialog == null) return;
        SwingUtilities.invokeLater(() -> {
            dialog.setVisible(false);
            dialog.dispose();
        });
    }

    private static String mb(long bytes) {
        return bytes < 1024 * 1024 ? (bytes / 1024) + " KB" : (bytes / (1024 * 1024)) + " MB";
    }
}
