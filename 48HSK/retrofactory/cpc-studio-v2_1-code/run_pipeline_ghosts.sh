#!/usr/bin/env bash
set -Eeuo pipefail

DEBUG=0
if [[ "${1:-}" == "--debug" ]]; then
  DEBUG=1
  shift
fi

if [[ "$#" -gt 0 ]]; then
  echo "Usage: $0 [--debug]" >&2
  exit 2
fi

ROOT="/Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code"
VENV_ACTIVATE="/Users/rafagranados/Develop/charlas/48HSK/.venv/bin/activate"

STDOUT_FILE="${ROOT}/pipeline_ghosts_output.json"
STDERR_FILE="${ROOT}/pipeline_ghosts_stderr.log"
LOG_FILE="${ROOT}/pipeline_ghosts_output.log"

timestamp() { date +"%Y-%m-%d %H:%M:%S"; }

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "${LOG_FILE}" >&2
}

on_error() {
  local exit_code=$?
  local line_no=$1
  log "[ERROR] line ${line_no} exit=${exit_code}"
  echo "EXIT=${exit_code}" | tee -a "${LOG_FILE}" >&2
  exit "${exit_code}"
}
trap 'on_error ${LINENO}' ERR

: > "${LOG_FILE}"
: > "${STDOUT_FILE}"
: > "${STDERR_FILE}"

[[ -d "${ROOT}" ]] || { log "[ERROR] root directory does not exist: ${ROOT}"; exit 1; }
cd "${ROOT}"

[[ -f "app/main.py" ]] || { log "[ERROR] missing app/main.py"; exit 1; }

if [[ -f "${VENV_ACTIVATE}" ]]; then
  # shellcheck disable=SC1090
  source "${VENV_ACTIVATE}"
fi

command -v python >/dev/null 2>&1 || { log "[ERROR] python not found"; exit 1; }

REQUEST="Crea un juego de acción y plataformas para Amstrad CPC 6128, inspirado en Ghosts 'n Goblins, con dificultad alta, enemigos por oleadas y control preciso"

if [[ "${DEBUG}" -eq 1 ]]; then
  export LLM_DEBUG=1
else
  export LLM_DEBUG=0
fi

log "[INFO] launching pipeline"
python -u -m app.main --request "${REQUEST}" \
  > >(tee "${STDOUT_FILE}") \
  2> >(tee "${STDERR_FILE}" >&2)

cmd_exit=$?

echo "EXIT=${cmd_exit}" | tee -a "${LOG_FILE}" >&2

printf '\n===== wc =====\n' >&2
wc -c "${STDOUT_FILE}" "${STDERR_FILE}" >&2
printf '\n===== stdout head =====\n' >&2
head -n 40 "${STDOUT_FILE}" >&2 || true
printf '\n===== stderr tail =====\n' >&2
tail -n 80 "${STDERR_FILE}" >&2 || true

exit "${cmd_exit}"