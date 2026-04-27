#!/usr/bin/env bash

set -euo pipefail

APIM_HOME="${APIM_HOME:-/Users/rafagranados/Develop/wso2/wso2am-4.6.0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_FILE="$SCRIPT_DIR/src/main/java/com/example/apim/guardrails/InputSanitizationMediator.java"
TARGET_DIR="$SCRIPT_DIR/target"
CLASSES_DIR="$TARGET_DIR/classes"
JAR_FILE="$TARGET_DIR/InputSanitizationMediator.jar"
MANIFEST_FILE="$TARGET_DIR/MANIFEST.MF"

if [[ ! -d "$APIM_HOME" ]]; then
    echo "APIM_HOME no existe: $APIM_HOME" >&2
    exit 1
fi

SYNAPSE_CORE_JAR="$(find "$APIM_HOME/repository/components/plugins" -maxdepth 1 -name 'synapse-core_*.jar' | head -n 1)"
if [[ -z "$SYNAPSE_CORE_JAR" ]]; then
    echo "No se encontró synapse-core en $APIM_HOME/repository/components/plugins" >&2
    exit 1
fi

SYNAPSE_CORE_VERSION="$(basename "$SYNAPSE_CORE_JAR" | sed -E 's/^synapse-core_(.*)\.jar$/\1/')"

mkdir -p "$CLASSES_DIR"
find "$CLASSES_DIR" -type f -delete

CLASSPATH=""
for lib_dir in "$APIM_HOME/repository/components/plugins" "$APIM_HOME/repository/components/lib"; do
    while IFS= read -r -d '' jar_file; do
        if [[ -z "$CLASSPATH" ]]; then
            CLASSPATH="$jar_file"
        else
            CLASSPATH="$CLASSPATH:$jar_file"
        fi
    done < <(find "$lib_dir" -maxdepth 1 -name '*.jar' -print0)
done

javac \
    -encoding UTF-8 \
    -source 11 \
    -target 11 \
    -cp "$CLASSPATH" \
    -d "$CLASSES_DIR" \
    "$SRC_FILE"

cat > "$MANIFEST_FILE" <<EOF
Manifest-Version: 1.0
Bundle-ManifestVersion: 2
Bundle-Name: Input Sanitization Mediator Fragment
Bundle-SymbolicName: com.example.apim.sanitize.fragment
Bundle-Version: 1.0.0
Fragment-Host: synapse-core;bundle-version="$SYNAPSE_CORE_VERSION"
Export-Package: com.example.apim.guardrails
EOF

jar cfm "$JAR_FILE" "$MANIFEST_FILE" -C "$CLASSES_DIR" .

rm -f "$APIM_HOME/repository/components/lib/InputSanitizationMediator.jar"
cp "$JAR_FILE" "$APIM_HOME/repository/components/dropins/"
cp "$SCRIPT_DIR/InputSanitizationPolicy.xml" \
   "$APIM_HOME/repository/deployment/server/synapse-configs/default/sequences/"
cp "$SCRIPT_DIR/WSO2AM--Ext--In.xml" \
   "$APIM_HOME/repository/deployment/server/synapse-configs/default/sequences/"

echo "Build y despliegue completados en $APIM_HOME usando fragment bundle para synapse-core $SYNAPSE_CORE_VERSION"