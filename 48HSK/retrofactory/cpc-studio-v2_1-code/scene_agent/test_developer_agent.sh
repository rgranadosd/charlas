#!/usr/bin/env bash
# test_developer_agent.sh — Battery test for the development worker agent
# Usage: bash scene_agent/test_developer_agent.sh
# NO set -e so the script never aborts on a single failing step

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
cd "$REPO_ROOT"
source .venv/bin/activate

G="\033[32m"; Y="\033[33m"; R="\033[31m"; B="\033[36m"; W="\033[1m"; RS="\033[0m"

PASS=0; FAIL=0; WARN=0
RESULTS=()
LOG_DIR="scene_agent/test_logs"
mkdir -p "$LOG_DIR"

strip_ansi() { sed 's/\x1b\[[0-9;]*m//g'; }

extract_from_log() {
    local log_file="$1" field="$2"
    python3 - <<PYEOF 2>/dev/null
import re
text = open("$log_file").read()
# Strip ANSI escape codes
text = re.sub(r'\x1b\[[0-9;]*m', '', text)
if "$field" == "status":
    m = re.search(r'"status":\s*"(\w+)"', text)
    print(m.group(1) if m else "UNKNOWN")
elif "$field" == "files":
    paths = re.findall(r'"path":\s*"([^"]+)"', text)
    print(", ".join(paths) if paths else "empty")
elif "$field" == "model":
    m = re.search(r'\[2/3\]\s+\[([^\]]+)\]', text)
    print(m.group(1) if m else "unknown")
PYEOF
}

run_task() {
    local step="$1" task_id="$2" goal="$3"
    local log_file="$LOG_DIR/${step}_${task_id}.log"

    echo -e "\n${B}${W}━━━ Step ${step} · ${task_id} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RS}"
    echo -e "${W}goal:${RS} ${goal}"

    python -m scene_agent.developer_agent "$task_id" "$goal" 2>&1 | tee "$log_file"
    local EXIT=${PIPESTATUS[0]}

    STATUS=$(extract_from_log "$log_file" "status")
    FILES=$(extract_from_log  "$log_file" "files")
    MODEL=$(extract_from_log  "$log_file" "model")

    if [[ $EXIT -ne 0 ]]; then
        echo -e "${R}  ✗ worker salió con código $EXIT — ver $log_file${RS}"
        ((FAIL++))
        RESULTS+=("${R}[FAIL]${RS} ${step} ${task_id} — exit=$EXIT")
    elif [[ "$STATUS" == "done" && "$FILES" != "empty" ]]; then
        echo -e "${G}  ✓ status=done  modelo=${MODEL}  files: ${FILES}${RS}"
        ((PASS++))
        RESULTS+=("${G}[ OK ]${RS} ${step} ${task_id} — modelo=${MODEL}, files: ${FILES}")
    elif [[ "$STATUS" == "done" ]]; then
        echo -e "${Y}  ⚠ status=done pero files_to_write vacío${RS}"
        ((WARN++))
        RESULTS+=("${Y}[WARN]${RS} ${step} ${task_id} — done sin archivos")
    elif [[ "$STATUS" == "needs_clarification" ]]; then
        echo -e "${Y}  ⚠ status=needs_clarification${RS}"
        ((WARN++))
        RESULTS+=("${Y}[WARN]${RS} ${step} ${task_id} — needs_clarification")
    elif [[ "$STATUS" == "blocked" ]]; then
        echo -e "${R}  ✗ status=blocked${RS}"
        ((FAIL++))
        RESULTS+=("${R}[FAIL]${RS} ${step} ${task_id} — blocked")
    else
        echo -e "${R}  ✗ status inesperado '${STATUS}' — ver $log_file${RS}"
        ((FAIL++))
        RESULTS+=("${R}[FAIL]${RS} ${step} ${task_id} — status=${STATUS}")
    fi
}

echo -e "${W}════════════════════════════════════════════════════════════${RS}"
echo -e "${W}  DEVELOPER AGENT — batch test (5 tasks)${RS}"
echo -e "${W}════════════════════════════════════════════════════════════${RS}"
echo -e "  Logs: $LOG_DIR/\n"

run_task 1 "T003" "expose score counter in HUD using cpct_drawStringM0 at top-right"
run_task 2 "T004" "expose lives counter in HUD using cpct_drawStringM0 at top-right"
run_task 3 "T001" "manage projectile state with width <= 4px and erase/draw pattern"
run_task 4 "T005" "enforce floor boundary rule: reset ball and decrement lives — distinct from block collision"
run_task 5 "T006" "enforce block collision rule: bounce and destroy block — distinct from floor boundary"

echo -e "\n${W}════════════════════════════════════════════════════════════${RS}"
echo -e "${W}  RESULTS${RS}"
echo -e "${W}════════════════════════════════════════════════════════════${RS}"
for r in "${RESULTS[@]}"; do echo -e "  $r"; done
echo -e "\n  Passed: ${G}${PASS}${RS}  Warned: ${Y}${WARN}${RS}  Failed: ${R}${FAIL}${RS}"
[[ $FAIL -gt 0 ]] && exit 1 || exit 0
