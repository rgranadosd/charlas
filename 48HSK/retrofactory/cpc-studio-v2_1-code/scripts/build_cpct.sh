#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code"
CPCTELERA_HOME="$PROJECT_ROOT/tools/cpctelera/cpctelera"
GENERATED_PROJECTS="$PROJECT_ROOT/generated_projects"
PROJECT_NAME="${1:-testcpct}"

source "$HOME/.profile" || true
export CPCT_PATH="$CPCTELERA_HOME"
export PATH="$CPCTELERA_HOME/tools/scripts:$PATH"

cd "$GENERATED_PROJECTS"
rm -rf "$PROJECT_NAME"
cpct_mkproject "$PROJECT_NAME"
cd "$PROJECT_NAME"
make

echo
echo "Build completada:"
echo "  $GENERATED_PROJECTS/$PROJECT_NAME/$PROJECT_NAME.cdt"
echo "  $GENERATED_PROJECTS/$PROJECT_NAME/$PROJECT_NAME.dsk"
