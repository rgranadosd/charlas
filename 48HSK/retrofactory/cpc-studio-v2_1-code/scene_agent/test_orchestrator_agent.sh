#!/usr/bin/env bash
# test_orchestrator_agent.sh — Battery test for the orchestrator agent
# Usage: bash scene_agent/test_orchestrator_agent.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
cd "$REPO_ROOT"
source .venv/bin/activate

G="\033[32m"; Y="\033[33m"; R="\033[31m"; B="\033[36m"; W="\033[1m"; DIM="\033[2m"; RS="\033[0m"

PASS=0; FAIL=0; WARN=0
RESULTS=()
LOG_DIR="scene_agent/test_logs"
mkdir -p "$LOG_DIR"

strip_ansi() { sed 's/\x1b\[[0-9;]*m//g'; }

run_orchestrator() {
    local step="$1" project="$2" prompt="$3" min_tasks="$4"
    local log_file="$LOG_DIR/orch_${step}_${project}.log"

    echo -e "\n${B}${W}━━━ Orch Step ${step} · ${project} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RS}"
    echo -e "${W}prompt:${RS} ${prompt}"

    python -m scene_agent.orchestrator_agent "$project" "$prompt" 2>&1 | tee "$log_file"
    local EXIT=${PIPESTATUS[0]}

    # Extraer modelo (sin ANSI)
    MODEL=$(python3 - <<PYEOF 2>/dev/null
import re
text = open("$log_file").read()
text = re.sub(r'\x1b\[[0-9;]*m', '', text)
m = re.search(r'modelo\s*:\s*([^\n]+)', text)
print(m.group(1).strip() if m else "unknown")
PYEOF
)

    # Parsear el contrato JSON completo (una sola vez para tasks + validación)
    PARSE=$(python3 - <<PYEOF 2>/dev/null
import re, json, sys

text = open("$log_file").read()
text = re.sub(r'\x1b\[[0-9;]*m', '', text)

# Buscar el bloque JSON más largo que empiece por { y contenga "tasks"
contract = None
for m in re.finditer(r'\{', text):
    candidate = text[m.start():]
    depth = 0
    for i, ch in enumerate(candidate):
        if ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                try:
                    d = json.loads(candidate[:i+1])
                    if "tasks" in d and "intent" in d:
                        contract = d
                except Exception:
                    pass
                break
    if contract:
        break

if contract:
    print(len(contract["tasks"]))
    print("yes")
else:
    print(0)
    print("no")
PYEOF
)
    TASKS=$(echo "$PARSE" | head -1)
    HAS_INTENT=$(echo "$PARSE" | tail -1)

    if [[ $EXIT -ne 0 ]]; then
        echo -e "${R}  ✗ orquestador salió con código $EXIT — ver $log_file${RS}"
        ((FAIL++))
        RESULTS+=("${R}[FAIL]${RS} orch/${step} ${project} — exit=${EXIT}")
    elif [[ "$HAS_INTENT" == "yes" && "$TASKS" -ge "$min_tasks" ]]; then
        echo -e "${G}  ✓ contrato válido  modelo=${MODEL}  tareas=${TASKS} (≥${min_tasks})${RS}"
        ((PASS++))
        RESULTS+=("${G}[ OK ]${RS} orch/${step} ${project} — modelo=${MODEL}, tareas=${TASKS}")
    elif [[ "$HAS_INTENT" == "yes" ]]; then
        echo -e "${Y}  ⚠ contrato válido pero pocas tareas: ${TASKS} (esperadas ≥${min_tasks})${RS}"
        ((WARN++))
        RESULTS+=("${Y}[WARN]${RS} orch/${step} ${project} — tareas=${TASKS} < ${min_tasks}")
    else
        echo -e "${R}  ✗ JSON de contrato inválido o incompleto — ver $log_file${RS}"
        ((FAIL++))
        RESULTS+=("${R}[FAIL]${RS} orch/${step} ${project} — contrato inválido")
    fi
}

echo -e "${W}════════════════════════════════════════════════════════════${RS}"
echo -e "${W}  ORCHESTRATOR AGENT — batch test (3 prompts)${RS}"
echo -e "${W}════════════════════════════════════════════════════════════${RS}"
echo -e "  Logs: $LOG_DIR/\n"

run_orchestrator 1 "breakout_wso2"   "breakout game with WSO2 branding, score and lives HUD"  5
run_orchestrator 2 "simple_game"     "paddle game with ball and blocks"                         3
run_orchestrator 3 "hud_only"        "add score counter and lives counter to existing game HUD" 2

echo -e "\n${W}════════════════════════════════════════════════════════════${RS}"
echo -e "${W}  RESULTS${RS}"
echo -e "${W}════════════════════════════════════════════════════════════${RS}"
for r in "${RESULTS[@]}"; do echo -e "  $r"; done
echo -e "\n  Passed: ${G}${PASS}${RS}  Warned: ${Y}${WARN}${RS}  Failed: ${R}${FAIL}${RS}"
[[ $FAIL -gt 0 ]] && exit 1 || exit 0
