#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APIM_HOME="${APIM_HOME:-/Users/rafagranados/Develop/wso2/wso2am-4.6.0}"
CARBON_LOG="${CARBON_LOG:-$APIM_HOME/repository/logs/wso2carbon.log}"
START_TIMEOUT_SECONDS="${START_TIMEOUT_SECONDS:-240}"
POST_START_STABILIZATION_SECONDS="${POST_START_STABILIZATION_SECONDS:-40}"
POLL_INTERVAL_SECONDS="${POLL_INTERVAL_SECONDS:-2}"
BUILD_SCRIPT="$SCRIPT_DIR/build.sh"

usage() {
    cat <<EOF
Usage: $(basename "$0")

Wait for APIM to be ready, survive the post-start undeploy window, and then
redeploy InputSanitizationPolicy in hot mode.
EOF
}

is_port_listening() {
    local port="$1"
    lsof -ti "tcp:${port}" -sTCP:LISTEN >/dev/null 2>&1
}

is_apim_listening() {
    is_port_listening 9453 && is_port_listening 8253
}

latest_startup_line() {
    if [[ ! -f "$CARBON_LOG" ]]; then
        return 1
    fi

    grep -n 'WSO2 Carbon started in' "$CARBON_LOG" | tail -n 1 | cut -d: -f1
}

has_post_start_cleanup() {
    local startup_line="$1"

    sed -n "$((startup_line + 1)),\$p" "$CARBON_LOG" | grep -Eq \
        "Sequence named 'InputSanitizationPolicy' has been undeployed|Sequence named 'WSO2AM--Ext--In' has been undeployed"
}

wait_for_apim_start() {
    local deadline=$((SECONDS + START_TIMEOUT_SECONDS))

    while (( SECONDS < deadline )); do
        if is_apim_listening; then
            local startup_line
            startup_line="$(latest_startup_line || true)"
            if [[ -n "$startup_line" ]]; then
                printf '%s' "$startup_line"
                return 0
            fi
        fi

        sleep "$POLL_INTERVAL_SECONDS"
    done

    return 1
}

wait_for_cleanup_window() {
    local startup_line="$1"
    local deadline=$((SECONDS + POST_START_STABILIZATION_SECONDS))

    while (( SECONDS < deadline )); do
        if has_post_start_cleanup "$startup_line"; then
            return 0
        fi

        sleep "$POLL_INTERVAL_SECONDS"
    done

    return 0
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

if [[ ! -x "$BUILD_SCRIPT" ]]; then
    echo "Missing build script: $BUILD_SCRIPT" >&2
    exit 1
fi

mkdir -p "$(dirname "$CARBON_LOG")"
touch "$CARBON_LOG"

startup_line="$(latest_startup_line || true)"

if [[ -z "$startup_line" ]] || ! is_apim_listening; then
    echo "Waiting for APIM listeners and startup confirmation..."
    if ! startup_line="$(wait_for_apim_start)"; then
        echo "Timed out waiting for APIM startup" >&2
        exit 1
    fi
fi

if ! has_post_start_cleanup "$startup_line"; then
    echo "Waiting for APIM post-start cleanup window..."
    wait_for_cleanup_window "$startup_line"
fi

echo "Redeploying InputSanitizationPolicy in hot mode..."
"$BUILD_SCRIPT"
echo "Input sanitization hot redeploy completed."