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
LOG_FILE="${ROOT}/pipeline_ghosts_output.log"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

trace() {
  printf '[%s] [DEBUG] %s\n' "$(timestamp)" "$*"
}

error_log() {
  printf '[%s] [ERROR] %s\n' "$(timestamp)" "$*"
}

warn_log() {
  printf '[%s] [WARN] %s\n' "$(timestamp)" "$*"
}

trace_log() {
  [[ "${DEBUG}" -eq 1 ]] || return 0
  trace "$*" | tee -a "${LOG_FILE}"
}

on_error() {
  local exit_code=$?
  local line_no=$1
  error_log "ERROR at line ${line_no} (exit=${exit_code})" | tee -a "${LOG_FILE}" >&2
  echo "EXIT=${exit_code}"
  exit "${exit_code}"
}

trap 'on_error ${LINENO}' ERR

: > "${LOG_FILE}"
trace_log "Starting Ghosts-like full pipeline run"

if [[ ! -d "${ROOT}" ]]; then
  error_log "root directory does not exist: ${ROOT}" | tee -a "${LOG_FILE}" >&2
  echo "EXIT=1" | tee -a "${LOG_FILE}"
  exit 1
fi

cd "${ROOT}"
trace_log "PWD=$(pwd)"

if [[ ! -f "app/main.py" ]]; then
  error_log "missing app/main.py in ${ROOT}" | tee -a "${LOG_FILE}" >&2
  echo "EXIT=1" | tee -a "${LOG_FILE}"
  exit 1
fi

if [[ -f "${VENV_ACTIVATE}" ]]; then
  # shellcheck disable=SC1090
  source "${VENV_ACTIVATE}"
  trace_log "Virtualenv activated from ${VENV_ACTIVATE}"
else
  warn_log "virtualenv activation script not found, using current Python" | tee -a "${LOG_FILE}" >&2
fi

if ! command -v python >/dev/null 2>&1; then
  error_log "python command is not available in PATH" | tee -a "${LOG_FILE}" >&2
  echo "EXIT=1" | tee -a "${LOG_FILE}"
  exit 1
fi

trace_log "Using Python at $(command -v python)"
trace_log "Python version: $(python --version 2>&1)"

REQUEST="Crea un juego de acción y plataformas para Amstrad CPC 6128, inspirado en Ghosts 'n Goblins, con dificultad alta, enemigos por oleadas y control preciso"

trace_log "Launching pipeline command"
if [[ "${DEBUG}" -eq 1 ]]; then
  set -x
fi
if [[ "${DEBUG}" -eq 1 ]]; then
  export LLM_DEBUG=1
else
  export LLM_DEBUG=0
fi
python -u -m app.main --request "${REQUEST}" 2>&1 | tee -a "${LOG_FILE}"
cmd_exit=${PIPESTATUS[0]}
if [[ "${DEBUG}" -eq 1 ]]; then
  set +x
fi

trace_log "Pipeline execution finished"
echo "EXIT=${cmd_exit}" | tee -a "${LOG_FILE}"
exit "${cmd_exit}"