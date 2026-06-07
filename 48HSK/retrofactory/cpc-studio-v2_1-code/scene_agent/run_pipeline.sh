#!/usr/bin/env bash
# run_pipeline.sh - Safe launcher for scene_agent.pipeline from any directory.
# Usage:
#   bash scene_agent/run_pipeline.sh "create an Arkanoid-style game" --project breakout --no-emu
#   bash scene_agent/run_pipeline.sh arkanoid_prompt.txt --project breakout --no-emu

set -u -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="$(cd "$REPO_ROOT/../.." && pwd)"

AUTO_INSTALL=0
if [[ "${1:-}" == "--install-missing" ]]; then
  AUTO_INSTALL=1
  shift
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scene_agent/run_pipeline.sh \"<prompt>\" [pipeline args...]" >&2
  echo "       bash scene_agent/run_pipeline.sh <prompt_file.txt> [pipeline args...]" >&2
  echo "       bash scene_agent/run_pipeline.sh --install-missing \"<prompt>\" [pipeline args...]" >&2
  exit 2
fi

ACTUAL_PROMPT="$1"

# Check if first argument is a file (contains '.' and file exists)
if [[ "$1" == *"."* && -f "$1" ]]; then
  # Read prompt from file
  if [[ ! -r "$1" ]]; then
    echo "Error: Cannot read file '$1'" >&2
    exit 1
  fi
  ACTUAL_PROMPT="$(cat "$1")"
  if [[ -z "$ACTUAL_PROMPT" ]]; then
    echo "Error: File '$1' is empty" >&2
    exit 1
  fi
  echo "✓ Loading prompt from file: $1" >&2
else
  echo "✓ Using prompt from command line" >&2
fi

# Activate virtual environment if user is not already inside one.
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  if [[ -f "$REPO_ROOT/.venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "$REPO_ROOT/.venv/bin/activate"
  elif [[ -f "$WORKSPACE_ROOT/.venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "$WORKSPACE_ROOT/.venv/bin/activate"
  fi
fi

if [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
  PYTHON_BIN="$VIRTUAL_ENV/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "Error: no Python interpreter found in PATH." >&2
  exit 1
fi

cd "$REPO_ROOT"

# Ensure package import works even when caller started from scene_agent/.
if ! "$PYTHON_BIN" -c "import scene_agent" >/dev/null 2>&1; then
  if [[ -n "${PYTHONPATH:-}" ]]; then
    export PYTHONPATH="$REPO_ROOT:$PYTHONPATH"
  else
    export PYTHONPATH="$REPO_ROOT"
  fi
fi

IMPORT_ERR="$($PYTHON_BIN - <<'PY'
import traceback
try:
    import scene_agent.pipeline  # noqa: F401
except Exception:
    print(traceback.format_exc())
PY
)"

if [[ -n "$IMPORT_ERR" ]]; then
  MISSING_MODULE="$($PYTHON_BIN - <<'PY'
import traceback
missing = ""
try:
    import scene_agent.pipeline  # noqa: F401
except ModuleNotFoundError as exc:
    missing = exc.name or ""
except Exception:
    pass
print(missing)
PY
)"

  if [[ -n "$MISSING_MODULE" ]]; then
    echo "Missing Python module: $MISSING_MODULE" >&2
    if [[ "$AUTO_INSTALL" -eq 1 ]]; then
      echo "Installing missing dependency with pip..." >&2
      if ! "$PYTHON_BIN" -m pip install "$MISSING_MODULE"; then
        echo "Error: pip install failed for $MISSING_MODULE" >&2
        exit 1
      fi
      if ! "$PYTHON_BIN" -c "import scene_agent.pipeline" >/dev/null 2>&1; then
        echo "Error: import still failing after installation." >&2
        echo "$IMPORT_ERR" >&2
        exit 1
      fi
    else
      echo "Run with --install-missing to auto-install it, or install manually:" >&2
      echo "  $PYTHON_BIN -m pip install $MISSING_MODULE" >&2
      exit 1
    fi
  else
    echo "Error importing scene_agent.pipeline:" >&2
    echo "$IMPORT_ERR" >&2
    exit 1
  fi
fi

# Detect --lg flag to choose LangGraph pipeline
shift  # Remove the original first argument (file or prompt)
USE_LG=0
REMAINING_ARGS=()
for arg in "$@"; do
  if [[ "$arg" == "--lg" ]]; then
    USE_LG=1
  else
    REMAINING_ARGS+=("$arg")
  fi
done

if [[ "$USE_LG" -eq 1 ]]; then
  exec "$PYTHON_BIN" -m scene_agent.pipeline_lg "$ACTUAL_PROMPT" "${REMAINING_ARGS[@]}"
else
  exec "$PYTHON_BIN" -m scene_agent.pipeline "$ACTUAL_PROMPT" "${REMAINING_ARGS[@]}"
fi