#!/usr/bin/env bash
# Builds modsync-agent.jar from source using any JDK 11+ on PATH.
set -euo pipefail
cd "$(dirname "$0")"

OUT=modsync-agent.jar
CLASSES=build/classes
rm -rf "$CLASSES" && mkdir -p "$CLASSES"

# --release 17 => bytecode the game server's Java 17 can load.
javac --release 17 -d "$CLASSES" src/digbuild/modsync/ModSyncAgent.java

jar --create --file "$OUT" --manifest manifest.mf -C "$CLASSES" .
echo "built $OUT"
