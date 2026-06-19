#!/usr/bin/env bash
# Usage:
#   ./run_pipeline.sh "prompt"  [--project name] [--no-emu] [--dry-run] [--rebuild-rag]
#
# Examples:
#   ./run_pipeline.sh "Arkanoid with score and lives"
#   ./run_pipeline.sh "Arkanoid game" --project breakout --no-emu
#   ./run_pipeline.sh "Arkanoid game" --rebuild-rag    ← force RAG index rebuild first

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# venv may be in the project root or one level up
if [ -f ".venv/bin/python3" ]; then
  VENV=".venv/bin/python3"
elif [ -f "../.venv/bin/python3" ]; then
  VENV="../.venv/bin/python3"
else
  echo "ERROR: virtualenv not found (.venv/bin/python3 or ../.venv/bin/python3)"
  exit 1
fi

# --rebuild-rag: delete the index so load_or_build() recreates it
REBUILD_RAG=0
ARGS=()
for arg in "$@"; do
  if [ "$arg" = "--rebuild-rag" ]; then
    REBUILD_RAG=1
  else
    ARGS+=("$arg")
  fi
done

if [ "$REBUILD_RAG" = "1" ]; then
  INDEX="retrostudio_agent/data/rag_index_emb.json"
  echo "→ Forzando rebuild del índice RAG …"
  rm -f "$INDEX"
  echo "  índice eliminado — se reconstruirá con mistral-embed al arrancar"
fi

exec PYTHONPATH="$SCRIPT_DIR" "$VENV" -m scene_agent.pipeline "${ARGS[@]}"
