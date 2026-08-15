package digbuild.patch;

import net.minecraftforge.fml.common.Mod;

/** Entrypoint. Nearly all the work is in the mixins -- javafml just wants a
 *  class to hang the mod id on -- but heap sizing has to run from real code,
 *  and the earlier it runs the less of the boot allocates against G1's stock
 *  ratios. */
@Mod("digbuildheappatch")
public class DigbuildPatchMod {

    public DigbuildPatchMod() {
        HeapTuning.apply();
    }
}
