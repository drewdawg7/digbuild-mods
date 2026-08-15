package digbuild.patch;

import java.lang.management.ManagementFactory;

import com.sun.management.HotSpotDiagnosticMXBean;

/**
 * Sets the heap sizing flags the host refuses to pass.
 *
 * G1's stock MaxHeapFreeRatio is 70, which pins committed heap at roughly
 * live/0.30 and never lets it back down: measured here as 2736 MB committed
 * against 812 MB live, unchanged even by a full GC. That gap is JVM sizing
 * policy, not anything the game is holding, so no amount of tuning inside the
 * server reaches it. Setting the ratio took the container from ~5.4 GB to
 * ~2.1 GB with no other change.
 *
 * Normally this is -XX:MaxHeapFreeRatio on the command line. That route does
 * not exist on PebbleHost. Both were tried and both were confirmed dead by
 * reading the JVM's own recorded arguments out of a spark dump:
 *
 *   - the panel's LOADER_STARTUPFLAGS variable is accepted and silently dropped
 *   - Forge's @user_jvm_args.txt is not read either; the host's start.sh builds
 *     the java command itself
 *
 * So set them from inside instead. All three are `manageable` HotSpot flags,
 * which is exactly the category that may be written at runtime through
 * HotSpotDiagnosticMXBean -- this is a supported API, not a trick.
 *
 * Values are read back and logged rather than assumed: a flag that silently
 * refuses to change would otherwise look identical to one that worked.
 */
final class HeapTuning {

    /** Hand memory back once free space passes this, rather than G1's 70. */
    private static final String[][] FLAGS = {
        {"MinHeapFreeRatio", "10"},
        {"MaxHeapFreeRatio", "25"},
        // G1 only resizes during a collection, and an idle server never
        // triggers one, so the ratios above need something to act on.
        {"G1PeriodicGCInterval", "180000"},
        {"G1PeriodicGCSystemLoadThreshold", "0"},
    };

    private HeapTuning() {
    }

    static void apply() {
        HotSpotDiagnosticMXBean bean;
        try {
            bean = ManagementFactory.getPlatformMXBean(HotSpotDiagnosticMXBean.class);
        } catch (Throwable t) {
            log("no HotSpotDiagnosticMXBean (" + t + "); heap sizing left alone");
            return;
        }
        if (bean == null) {
            log("no HotSpotDiagnosticMXBean; heap sizing left alone");
            return;
        }
        for (String[] flag : FLAGS) {
            set(bean, flag[0], flag[1]);
        }
    }

    private static void set(HotSpotDiagnosticMXBean bean, String name, String value) {
        String before;
        try {
            before = bean.getVMOption(name).getValue();
        } catch (Throwable t) {
            // An unrecognised flag throws rather than returning null, and a
            // different collector is a perfectly ordinary reason for that.
            log("skipping " + name + " -- not present on this JVM");
            return;
        }
        if (same(before, value)) {
            log(name + " already " + before);
            return;
        }
        try {
            bean.setVMOption(name, value);
        } catch (Throwable t) {
            log("could not set " + name + " (" + t + "); still " + before);
            return;
        }
        String after = bean.getVMOption(name).getValue();
        log(name + ": " + before + " -> " + after
            + (same(after, value) ? "" : " (REFUSED -- wanted " + value + ")"));
    }

    /** Numeric compare: the bean reports doubles as "0.0" against a "0" here,
     *  which is equal in every sense except String.equals. */
    private static boolean same(String a, String b) {
        if (a.equals(b)) {
            return true;
        }
        try {
            return Double.compare(Double.parseDouble(a), Double.parseDouble(b)) == 0;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    /** stdout: this runs during mod construction, before any logger a mod
     *  might provide is available. */
    private static void log(String msg) {
        System.out.println("[digbuild] heap tuning: " + msg);
    }
}
