#!/bin/bash

set -euo pipefail

# Navigate to the script's directory
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR" || exit

YELLOW='\033[38;5;226m'
RESET='\033[0m'

PREWARM_ONLY=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prewarm)
            PREWARM_ONLY=true
            shift
            ;;
        *)
            echo -e "${YELLOW}Unknown option: $1${RESET}"
            echo "Usage: ./run-demo.sh [--prewarm]"
            exit 1
            ;;
    esac
done

echo -e "${YELLOW}================================================================================${RESET}"
echo -e "${YELLOW}                        RAG DEMO - Interactive Demo${RESET}"
echo -e "${YELLOW}================================================================================${RESET}"
echo ""

find_working_python() {
    local candidates=(
        "/opt/homebrew/bin/python3.13"
        "/opt/homebrew/bin/python3.12"
        "/opt/homebrew/bin/python3.11"
        "$(command -v python3 2>/dev/null || true)"
        "/usr/bin/python3"
    )

    for py in "${candidates[@]}"; do
        [ -z "$py" ] && continue
        if [ -x "$py" ] && "$py" --version >/dev/null 2>&1; then
            echo "$py"
            return 0
        fi
    done

    return 1
}

venv_is_healthy() {
    [ -x "venv/bin/python" ] || return 1

    local probe_output
    probe_output=$(./venv/bin/python -c 'import sys; print(sys.version_info[0])' 2>/dev/null || true)
    [ "$probe_output" = "3" ]
}

deps_are_healthy() {
    ./venv/bin/python - <<'PY' >/dev/null 2>&1
import importlib

required = [
    "requests",
    "httpx",
    "openai",
    "dotenv",
    "numpy",
    "sentence_transformers",
]

for module in required:
    importlib.import_module(module)
PY
}

recreate_venv() {
    local base_python="$1"
    echo -e "${YELLOW}Creating virtual environment with ${base_python}...${RESET}"
    rm -rf venv
    "$base_python" -m venv venv
    ./venv/bin/python -m pip install -q --upgrade pip
    echo -e "${YELLOW}Installing dependencies...${RESET}"
    ./venv/bin/python -m pip install -q -r requirements.txt
    echo ""
}

prewarm_embedding_model() {
    local model_name="${RAG_EMBEDDING_MODEL:-intfloat/multilingual-e5-small}"
    echo -e "${YELLOW}Prewarming embedding model: ${model_name}${RESET}"
    echo -e "${YELLOW}This downloads/caches the model now so the live demo starts faster later.${RESET}"
    export RAG_PREWARM_MODEL="$model_name"
    ./venv/bin/python - <<PY
import os
from sentence_transformers import SentenceTransformer

model_name = os.environ["RAG_PREWARM_MODEL"]
SentenceTransformer(model_name)
print(f"Model ready: {model_name}")
PY
    unset RAG_PREWARM_MODEL
    echo ""
}

if ! venv_is_healthy; then
    if [ -d "venv" ]; then
        echo -e "${YELLOW}Existing virtual environment is invalid. Recreating it...${RESET}"
    else
        echo -e "${YELLOW}Virtual environment not found. Creating it...${RESET}"
    fi

    BASE_PYTHON="$(find_working_python)"
    if [ -z "$BASE_PYTHON" ]; then
        echo -e "${YELLOW}No working Python interpreter was found to create the virtual environment.${RESET}"
        exit 1
    fi

    recreate_venv "$BASE_PYTHON"
fi

if ! deps_are_healthy; then
    echo -e "${YELLOW}Missing or broken Python dependencies detected. Reinstalling requirements...${RESET}"
    ./venv/bin/python -m pip install -q -r requirements.txt
    echo ""
fi

if [ "$PREWARM_ONLY" = true ]; then
    prewarm_embedding_model
    echo -e "${YELLOW}Prewarm finished.${RESET}"
    exit 0
fi

# Run the interactive demo script using the python from the virtual environment
./venv/bin/python demo_interactiva.py

echo -e "${YELLOW}Demo finished.${RESET}"
