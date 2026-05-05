#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$ROOT_DIR/.run"
PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
FRONTEND_PORT="${FRONTEND_PORT:-8091}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
RESOURCE_API_PORT="${RESOURCE_API_PORT:-8001}"
FRONTEND_ORIGIN="http://localhost:${FRONTEND_PORT}"

mkdir -p "$RUN_DIR"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Python virtualenv not found at $PYTHON_BIN" >&2
  echo "Create it first with: python -m venv .venv && .venv/bin/pip install -r backend/requirements.txt -r resource_api/requirements.txt" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required but was not found in PATH" >&2
  exit 1
fi

if [[ ! -d "$ROOT_DIR/frontend/node_modules" ]]; then
  echo "Installing frontend dependencies..."
  (cd "$ROOT_DIR/frontend" && npm install)
fi

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

load_env_file() {
  local file_path="$1"
  [[ -f "$file_path" ]] || return 0

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="$(trim "$line")"
    [[ -z "$line" || "${line:0:1}" == "#" ]] && continue
    [[ "$line" == *=* ]] || continue

    local key="${line%%=*}"
    local value="${line#*=}"

    key="$(trim "$key")"
    value="$(trim "$value")"

    if [[ "$value" == \"*\" && "$value" == *\" ]]; then
      value="${value:1:-1}"
    elif [[ "$value" == \'*\' && "$value" == *\' ]]; then
      value="${value:1:-1}"
    fi

    export "$key=$value"
  done < "$file_path"
}

declare -a pids=()

cleanup() {
  local exit_code=$?
  trap - EXIT INT TERM

  for pid in "${pids[@]:-}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
  done

  wait "${pids[@]:-}" 2>/dev/null || true
  echo
  echo "Services stopped. Logs remain in $RUN_DIR"
  exit "$exit_code"
}

trap cleanup EXIT INT TERM

start_backend() {
  (
    cd "$ROOT_DIR/backend"
    load_env_file "$ROOT_DIR/backend/.env"
    export BACKEND_HOST="0.0.0.0"
    export BACKEND_PORT="$BACKEND_PORT"
    export FRONTEND_ORIGINS="$FRONTEND_ORIGIN"
    export RESOURCE_API_BASE_URL="http://localhost:${RESOURCE_API_PORT}"
    exec "$PYTHON_BIN" -m uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
  ) >"$RUN_DIR/backend.log" 2>&1 &
  pids+=("$!")
}

start_resource_api() {
  (
    cd "$ROOT_DIR/resource_api"
    load_env_file "$ROOT_DIR/resource_api/.env"
    export RESOURCE_API_HOST="0.0.0.0"
    export RESOURCE_API_PORT="$RESOURCE_API_PORT"
    exec "$PYTHON_BIN" -m uvicorn app.main:app --host 0.0.0.0 --port "$RESOURCE_API_PORT" --reload
  ) >"$RUN_DIR/resource_api.log" 2>&1 &
  pids+=("$!")
}

start_frontend() {
  (
    cd "$ROOT_DIR/frontend"
    export VITE_BACKEND_BASE_URL="http://localhost:${BACKEND_PORT}"
    export VITE_ASGARDEO_SIGN_IN_REDIRECT_URL="$FRONTEND_ORIGIN"
    export VITE_ASGARDEO_SIGN_OUT_REDIRECT_URL="$FRONTEND_ORIGIN"
    exec npm run dev -- --host 0.0.0.0 --port "$FRONTEND_PORT"
  ) >"$RUN_DIR/frontend.log" 2>&1 &
  pids+=("$!")
}

echo "Starting backend on http://localhost:${BACKEND_PORT}"
start_backend

echo "Starting resource API on http://localhost:${RESOURCE_API_PORT}"
start_resource_api

echo "Starting frontend on ${FRONTEND_ORIGIN}"
start_frontend

cat <<EOF

Services starting.

- Frontend: ${FRONTEND_ORIGIN}
- Backend: http://localhost:${BACKEND_PORT}
- Resource API: http://localhost:${RESOURCE_API_PORT}

Logs:
- $RUN_DIR/frontend.log
- $RUN_DIR/backend.log
- $RUN_DIR/resource_api.log

If login fails, verify that your WSO2 IS / Asgardeo SPA allows ${FRONTEND_ORIGIN} as sign-in and sign-out redirect URI.
Press Ctrl+C to stop everything.
EOF

wait