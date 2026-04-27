#!/usr/bin/env bash

set -euo pipefail

APIM_HOME="${APIM_HOME:-/Users/rafagranados/Develop/wso2/wso2am-4.6.0}"
CARBON_LOG="${CARBON_LOG:-$APIM_HOME/repository/logs/wso2carbon.log}"
HTTP_LOG="${HTTP_LOG:-$APIM_HOME/repository/logs/http_access.log}"
SANITIZE_PATTERN="${SANITIZE_PATTERN:-InputSanitizationMediator sanitized request payload}"
TAIL_LINES="${TAIL_LINES:-5}"
FOLLOW_MODE=0
SINCE_FILTER=""
MESSAGE_ID_FILTER=""
USE_LATEST_MESSAGE_ID=0

usage() {
    cat <<EOF
Usage: $(basename "$0") [options]

Options:
  --follow                 Follow new sanitize and HTTP access lines in real time.
  --since TEXT             Filter current output by a literal timestamp fragment.
  --message-id ID          Filter Carbon log lines by a specific messageId.
  --latest-message-id      Resolve the messageId from the latest sanitize log line.
  --tail N                 Show the last N HTTP access lines. Default: $TAIL_LINES
  -h, --help               Show this help.

Examples:
  ./check_latest_sanitization_logs.sh
  ./check_latest_sanitization_logs.sh --since "00:36"
  ./check_latest_sanitization_logs.sh --latest-message-id
  ./check_latest_sanitization_logs.sh --follow
EOF
}

while (($#)); do
    case "$1" in
        --follow)
            FOLLOW_MODE=1
            shift
            ;;
        --since)
            if [[ $# -lt 2 ]]; then
                echo "Missing value for --since" >&2
                exit 1
            fi
            SINCE_FILTER="$2"
            shift 2
            ;;
        --message-id)
            if [[ $# -lt 2 ]]; then
                echo "Missing value for --message-id" >&2
                exit 1
            fi
            MESSAGE_ID_FILTER="$2"
            shift 2
            ;;
        --latest-message-id)
            USE_LATEST_MESSAGE_ID=1
            shift
            ;;
        --tail)
            if [[ $# -lt 2 ]]; then
                echo "Missing value for --tail" >&2
                exit 1
            fi
            TAIL_LINES="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [[ ! -f "$CARBON_LOG" ]]; then
    echo "Missing Carbon log: $CARBON_LOG" >&2
    exit 1
fi

if [[ ! -f "$HTTP_LOG" ]]; then
    echo "Missing HTTP access log: $HTTP_LOG" >&2
    exit 1
fi

if [[ "$USE_LATEST_MESSAGE_ID" == "1" ]]; then
    latest_sanitize_line="$(grep -F "$SANITIZE_PATTERN" "$CARBON_LOG" | tail -n 1 || true)"
    if [[ -z "$latest_sanitize_line" ]]; then
        echo "No sanitize log lines found in $CARBON_LOG" >&2
        exit 1
    fi

    resolved_message_id="$(printf '%s\n' "$latest_sanitize_line" | sed -n 's/.*messageId=\([^, ]*\).*/\1/p')"
    if [[ -z "$resolved_message_id" ]]; then
        echo "Could not resolve messageId from latest sanitize log line" >&2
        exit 1
    fi

    MESSAGE_ID_FILTER="$resolved_message_id"
fi

filter_current_lines() {
    local file_path="$1"
    local initial_pattern="$2"
    local extra_pattern="$3"
    local lines

    if [[ -n "$initial_pattern" ]]; then
        lines="$(grep -F "$initial_pattern" "$file_path" || true)"
    else
        lines="$(cat "$file_path")"
    fi

    if [[ -n "$SINCE_FILTER" ]]; then
        lines="$(printf '%s\n' "$lines" | grep -F "$SINCE_FILTER" || true)"
    fi

    if [[ -n "$extra_pattern" ]]; then
        lines="$(printf '%s\n' "$lines" | grep -F "$extra_pattern" || true)"
    fi

    printf '%s\n' "$lines"
}

show_current_view() {
    local current_sanitize_lines
    local current_http_lines

    current_sanitize_lines="$(filter_current_lines "$CARBON_LOG" "$SANITIZE_PATTERN" "$MESSAGE_ID_FILTER")"

    echo "--- Latest sanitize log ---"
    if [[ -n "$current_sanitize_lines" ]]; then
        printf '%s\n' "$current_sanitize_lines" | tail -n 1
    fi

    if [[ -n "$MESSAGE_ID_FILTER" ]]; then
        echo
        echo "Resolved messageId: $MESSAGE_ID_FILTER"
    fi

    echo
    echo "--- Latest HTTP access logs ---"
    current_http_lines="$(tail -n "$TAIL_LINES" "$HTTP_LOG")"
    if [[ -n "$SINCE_FILTER" ]]; then
        current_http_lines="$(printf '%s\n' "$current_http_lines" | grep -F "$SINCE_FILTER" || true)"
    fi
    printf '%s\n' "$current_http_lines"
}

if [[ "$FOLLOW_MODE" == "1" ]]; then
    show_current_view
    echo
    echo "--- Following sanitize and HTTP logs ---"
    tail -n 0 -f "$CARBON_LOG" "$HTTP_LOG" | awk \
        -v carbon_log="$CARBON_LOG" \
        -v http_log="$HTTP_LOG" \
        -v sanitize_pattern="$SANITIZE_PATTERN" \
        -v message_id="$MESSAGE_ID_FILTER" '
        /^==> / {
            current_file = $2
            next
        }
        {
            if (current_file == carbon_log) {
                if (index($0, sanitize_pattern) && (message_id == "" || index($0, message_id))) {
                    print "[carbon] " $0
                    fflush()
                }
            } else if (current_file == http_log) {
                print "[http] " $0
                fflush()
            }
        }'
    exit 0
fi

show_current_view