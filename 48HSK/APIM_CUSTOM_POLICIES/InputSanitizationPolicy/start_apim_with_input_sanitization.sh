#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APIM_HOME="${APIM_HOME:-/Users/rafagranados/Develop/wso2/wso2am-4.6.0}"
API_MANAGER_SH="$APIM_HOME/bin/api-manager.sh"
START_LOG="${START_LOG:-/tmp/wso2am-start.log}"
DEPLOY_HELPER="$SCRIPT_DIR/deploy_input_sanitization_when_ready.sh"

usage() {
    cat <<EOF
Usage: $(basename "$0")

Start APIM only if it is down, then hot-redeploy InputSanitizationPolicy when
the runtime is ready.
EOF
}

is_port_listening() {
    local port="$1"
    lsof -ti "tcp:${port}" -sTCP:LISTEN >/dev/null 2>&1
}

is_apim_running() {
    is_port_listening 9453 && is_port_listening 8253
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

if [[ ! -x "$API_MANAGER_SH" ]]; then
    echo "Missing APIM launcher: $API_MANAGER_SH" >&2
    exit 1
fi

if [[ ! -x "$DEPLOY_HELPER" ]]; then
    echo "Missing deploy helper: $DEPLOY_HELPER" >&2
    exit 1
fi

if is_apim_running; then
    echo "APIM is already running. Reapplying input sanitization in hot mode..."
else
    echo "Starting APIM in background..."
    nohup "$API_MANAGER_SH" > "$START_LOG" 2>&1 &
fi

"$DEPLOY_HELPER"