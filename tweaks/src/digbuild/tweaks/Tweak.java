package digbuild.tweaks;

import java.util.List;

/**
 * One gameplay tweak.
 *
 * A tweak owns a config file under config/digbuild-tweaks/ and is handed its
 * contents at server setup and again every time that file changes on disk --
 * see Tweaks. apply() therefore has to be re-runnable: it replaces whatever the
 * previous call published rather than adding to it.
 *
 * Anything a tweak needs from the game is available by the time apply() first
 * runs (common setup), so registries may be read here but not in a constructor.
 */
public abstract class Tweak {

    /** Short id. Names the log lines and, by default, the config file. */
    public abstract String id();

    /** File name under config/digbuild-tweaks/, or null for a tweak with no
     *  config -- apply() is then called once, at setup, with an empty list. */
    public String config() {
        return id() + ".properties";
    }

    /** Written out when the config file is missing. */
    public String defaultConfig() {
        return "";
    }

    /** Comment-stripped, blank-stripped config lines. */
    public abstract void apply(List<String> lines);

    protected void log(String msg) {
        Tweaks.log(id() + ": " + msg);
    }
}
