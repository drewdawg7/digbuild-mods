#!/usr/bin/env bash
# Builds digbuild-modsync-<ver>.jar, a minimal Forge 1.20.1 mod that runs the
# agent on server boot. Compile-only dependency is the @Mod annotation, taken
# from the Forge jars the server itself uses (pulled into ./forgelib).
set -euo pipefail
cd "$(dirname "$0")"

VER=1.0.0
OUT="digbuild-modsync-${VER}.jar"
CP="forgelib/javafmllanguage.jar:forgelib/fmlcore.jar"
STAGE=build/mod
rm -rf "$STAGE" && mkdir -p "$STAGE/META-INF"

javac --release 17 -cp "$CP" -d "$STAGE" \
  src/digbuild/modsync/ModSyncAgent.java \
  src/digbuild/modsync/ModSyncMod.java

cp mods.toml "$STAGE/META-INF/mods.toml"
cp pack.mcmeta "$STAGE/pack.mcmeta"   # silences "missing metadata in pack" warnings
jar --create --file "$OUT" -C "$STAGE" .
echo "built $OUT"
