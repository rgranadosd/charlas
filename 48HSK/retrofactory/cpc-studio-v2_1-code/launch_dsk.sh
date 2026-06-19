#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CAP32="$SCRIPT_DIR/cpctelera/tools/caprice32/cap32"

if [[ $# -lt 1 ]]; then
  echo "Usage: ./launch_dsk.sh <output_folder>" >&2
  echo "       ./launch_dsk.sh scene_agent/outputs/20260603_155307" >&2
  exit 1
fi

FOLDER="$1"

DSK="$(find "$FOLDER" -maxdepth 1 -type f \( -iname "*.dsk" \) | head -1)"

if [[ -z "$DSK" ]]; then
  echo "Error: no .dsk found in '$FOLDER'" >&2
  exit 1
fi

BINARY_NAME="$(basename "$DSK" .dsk | tr '[:lower:]' '[:upper:]' | cut -c1-8)"
AUTOCMD="run\"${BINARY_NAME}.BIN"

echo "Launching: $DSK  →  $AUTOCMD"
exec "$CAP32" "$DSK" -a "$AUTOCMD"
