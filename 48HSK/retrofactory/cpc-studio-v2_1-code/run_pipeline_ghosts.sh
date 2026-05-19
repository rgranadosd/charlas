#!/usr/bin/env bash
set -Eeuo pipefail

DEBUG=0
USE_MOCKS=1
EXPLICIT_NOMOCKS=0
AUTO_CONFIRM_REAL=0
DEFAULT_MOCK_TRACE="/Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code/pipeline_ghosts_last_success.json"
MOCK_TRACE="${DEFAULT_MOCK_TRACE}"
MOCK_STEPS="auto"

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --debug)
      DEBUG=1
      shift
      ;;
    --mock-trace)
      [[ $# -ge 2 ]] || { echo "Missing value for --mock-trace" >&2; exit 2; }
      MOCK_TRACE="$2"
      USE_MOCKS=1
      shift 2
      ;;
    --mock-steps)
      [[ $# -ge 2 ]] || { echo "Missing value for --mock-steps" >&2; exit 2; }
      MOCK_STEPS="$2"
      shift 2
      ;;
    --nomocks)
      USE_MOCKS=0
      EXPLICIT_NOMOCKS=1
      shift
      ;;
    --yes-real)
      AUTO_CONFIRM_REAL=1
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--debug] [--nomocks] [--yes-real] [--mock-trace <trace.json>] [--mock-steps <auto|all|none|csv>]" >&2
      exit 0
      ;;
    *)
      echo "Usage: $0 [--debug] [--nomocks] [--yes-real] [--mock-trace <trace.json>] [--mock-steps <auto|all|none|csv>]" >&2
      exit 2
      ;;
  esac
done

ROOT="/Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code"
VENV_ACTIVATE="/Users/rafagranados/Develop/charlas/48HSK/.venv/bin/activate"
CAP32_APP="/Applications/Caprice32.app"
CAP32_BIN="${CAP32_APP}/Contents/MacOS/Caprice32"
CAP32_RESOURCES_DIR="${CAP32_APP}/Contents/Resources"
CAP32_CFG="/tmp/cap32_pipeline_ghosts.cfg"
CAP32_BOOT_TIME="320"

STDOUT_FILE="${ROOT}/pipeline_ghosts_output.json"
STDERR_FILE="${ROOT}/pipeline_ghosts_stderr.log"
LOG_FILE="${ROOT}/pipeline_ghosts_output.log"
TRACE_CACHE_FILE="${ROOT}/pipeline_ghosts_last_success.json"

timestamp() { date +"%Y-%m-%d %H:%M:%S"; }

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "${LOG_FILE}" >&2
}

confirm_real_ai_usage() {
  local reason="$1"

  if [[ "${EXPLICIT_NOMOCKS}" -eq 1 ]]; then
    return 0
  fi

  if [[ ! -t 0 ]]; then
    log "[ERROR] se requiere confirmacion para usar IA real (${reason}), pero no hay terminal interactiva"
    log "[ERROR] usa --nomocks para ejecutar sin confirmacion"
    return 1
  fi

  printf '[%s] [CONFIRM] para continuar hace falta usar IA real (%s). Permitir? [y/N]: ' "$(timestamp)" "${reason}" >&2
  local reply
  read -r reply
  reply="$(printf '%s' "${reply}" | tr '[:upper:]' '[:lower:]')"
  if [[ "${reply}" == "y" || "${reply}" == "yes" || "${reply}" == "s" || "${reply}" == "si" ]]; then
    log "[INFO] permiso concedido para usar IA real"
    return 0
  fi

  log "[INFO] permiso denegado; se aborta para evitar llamadas reales"
  return 1
}

run_pipeline_once() {
  local -a args=("$@")
  python -u -m app.main "${args[@]}" \
    > >(tee "${STDOUT_FILE}") \
    2> >(tee "${STDERR_FILE}" >&2)
}

run_llm_preflight() {
  log "[INFO] running LLM preflight checks"

  python - <<'PY'
import os
import sys
import concurrent.futures

from app.services.llm_service import build_model, _resolve_provider_and_model


YELLOW = "\033[33m"
RESET  = "\033[0m"
PREFLIGHT_WALL_TIMEOUT = 20  # wall-clock seconds per model check

def stderr(message: str) -> None:
  sys.stderr.write(message + "\n")
  sys.stderr.flush()

def _call_llm(llm):
  return llm.invoke([
    {"role": "system", "content": "You are a healthcheck assistant."},
    {"role": "user", "content": "Reply with exactly OK."},
  ])

checks = [
  "orchestrator",
  "narrative",
]

checked = set()
for prompt_name in checks:
  provider, model_override = _resolve_provider_and_model(prompt_name, None)
  model_name = model_override or "<provider-default>"
  key = (provider, model_override or "")
  if key in checked:
    stderr(f"[INFO] [PREFLIGHT] skip duplicate route prompt={prompt_name} provider={provider} model={model_name}")
    continue

  checked.add(key)
  stderr(f"[INFO] [PREFLIGHT] checking prompt={prompt_name} provider={provider} model={model_name} wall_timeout={PREFLIGHT_WALL_TIMEOUT}s")
  try:
    llm = build_model(model_override=model_override, provider=provider, timeout=PREFLIGHT_WALL_TIMEOUT)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
      future = ex.submit(_call_llm, llm)
      try:
        response = future.result(timeout=PREFLIGHT_WALL_TIMEOUT)
      except concurrent.futures.TimeoutError:
        raise TimeoutError(f"wall-clock timeout after {PREFLIGHT_WALL_TIMEOUT}s")
    content = getattr(response, "content", response)
    if isinstance(content, list):
      parts = []
      for item in content:
        if isinstance(item, str):
          parts.append(item)
        elif isinstance(item, dict):
          parts.append(str(item.get("text") or item.get("content") or ""))
      content = " ".join(parts)
    text = str(content).strip()
    stderr(f"[INFO] [PREFLIGHT] ok prompt={prompt_name} provider={provider} model={model_name} response={YELLOW}{text[:80]}{RESET}")
  except Exception as exc:
    stderr(f"[WARN] [PREFLIGHT] unreachable prompt={prompt_name} provider={provider} model={model_name} detail={exc} (continuing anyway)")
    continue

image_enabled = os.getenv("ART_ASSETS_IMAGE_ENABLED", "").strip().lower() in {"1", "true", "yes", "on"}
image_model = os.getenv("ART_ASSETS_IMAGE_MODEL", "black-forest-labs/flux.2-klein-4b").strip()
if image_enabled:
  stderr(
    f"[WARN] [PREFLIGHT] ART_ASSETS_IMAGE_MODEL={image_model} is configured but visual backend is currently stubbed; no live endpoint check is performed"
  )
else:
  stderr(f"[INFO] [PREFLIGHT] art visual backend disabled for model={image_model}")
PY

  log "[INFO] LLM preflight checks passed"
}

prepare_caprice32_cfg() {
  cp "${CAP32_RESOURCES_DIR}/cap32.cfg" "${CAP32_CFG}"
  sed -i '' "s|^model=.*|model=2|" "${CAP32_CFG}"
  sed -i '' "s|^joystick_emulation=.*|joystick_emulation=1|" "${CAP32_CFG}"
  sed -i '' "s|^boot_time=.*|boot_time=${CAP32_BOOT_TIME}|" "${CAP32_CFG}"
  sed -i '' "s|^resources_path=.*|resources_path=${CAP32_RESOURCES_DIR}/resources|" "${CAP32_CFG}"
  sed -i '' "s|^dsk_path=.*|dsk_path=${CAP32_RESOURCES_DIR}/disk|" "${CAP32_CFG}"
  sed -i '' "s|^tape_path=.*|tape_path=${CAP32_RESOURCES_DIR}/tape|" "${CAP32_CFG}"
  sed -i '' "s|^rom_path=.*|rom_path=${CAP32_RESOURCES_DIR}/rom|" "${CAP32_CFG}"
}

launch_caprice32_with_autocmd() {
  local dsk_path="$1"
  local autocmd="$2"

  (
    cd "${CAP32_RESOURCES_DIR}"
    "${CAP32_BIN}" \
      -c "${CAP32_CFG}" \
      -O "system.boot_time=${CAP32_BOOT_TIME}" \
      --autocmd "${autocmd}" \
      "${dsk_path}"
  ) &
}

find_latest_generated_dsk() {
  python - "${ROOT}/generated_projects" <<'PY'
from pathlib import Path
import sys

base = Path(sys.argv[1])
if not base.exists():
    raise SystemExit(0)

candidates = [p for p in base.glob("run*/*.dsk") if p.is_file()]
if not candidates:
    raise SystemExit(0)

candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
print(candidates[0])
PY
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

[[ -d "${ROOT}" ]] || { log "[ERROR] root directory does not exist: ${ROOT}"; exit 1; }
cd "${ROOT}"

[[ -f "app/main.py" ]] || { log "[ERROR] missing app/main.py"; exit 1; }

if [[ -f "${VENV_ACTIVATE}" ]]; then
  # shellcheck disable=SC1090
  source "${VENV_ACTIVATE}"
fi

if [[ -f "${ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT}/.env"
  set +a
fi

command -v python >/dev/null 2>&1 || { log "[ERROR] python not found"; exit 1; }

REQUEST="Crea un juego de acción y plataformas para Amstrad CPC 6128, inspirado en Ghosts 'n Goblins, con dificultad alta, enemigos por oleadas y control preciso"

if [[ "${DEBUG}" -eq 1 ]]; then
  export LLM_DEBUG=1
else
  export LLM_DEBUG=0
fi

: "${MISTRAL_MODEL:=mistral-small-latest}"
: "${MISTRAL_FALLBACK_MODEL:=mistral-small-latest}"
: "${NVIDIA_MODEL:=moonshotai/kimi-k2.6}"

# Cost guardrails: keep retries conservative unless user overrides via env.
: "${LLM_MAX_RETRIES:=4}"
: "${LLM_RETRY_MAX_DELAY:=30}"

export LLM_MAX_RETRIES
export LLM_RETRY_MAX_DELAY
export MISTRAL_MODEL
export MISTRAL_FALLBACK_MODEL
export NVIDIA_MODEL

if [[ "${USE_MOCKS}" -eq 1 && ! -f "${MOCK_TRACE}" ]]; then
  if confirm_real_ai_usage "mock trace no encontrada"; then
    USE_MOCKS=0
  else
    exit 1
  fi
fi

if [[ "${EXPLICIT_NOMOCKS}" -eq 1 && "${AUTO_CONFIRM_REAL}" -eq 0 ]]; then
  if ! confirm_real_ai_usage "--nomocks fuerza uso de IA real"; then
    exit 1
  fi
fi

if [[ "${USE_MOCKS}" -eq 1 ]]; then
  log "[INFO] ciclo mock: se omite LLM preflight real"
else
  run_llm_preflight
fi

if [[ "${USE_MOCKS}" -eq 0 ]]; then
  log "[INFO] ciclo en modo real (--nomocks)"
else
  log "[INFO] mock replay solicitado con trace=${MOCK_TRACE} steps=${MOCK_STEPS}"
fi

log "[INFO] launching pipeline"
PY_ARGS=(--request "${REQUEST}")
if [[ "${USE_MOCKS}" -eq 1 ]]; then
  PY_ARGS+=(--mock-trace "${MOCK_TRACE}" --mock-steps "${MOCK_STEPS}")
fi

if run_pipeline_once "${PY_ARGS[@]}"; then
  cmd_exit=0
else
  cmd_exit=$?

  if [[ "${USE_MOCKS}" -eq 1 && "${EXPLICIT_NOMOCKS}" -eq 0 ]] && grep -qi "strict mock mode" "${STDERR_FILE}"; then
    if confirm_real_ai_usage "la traza no cubre todos los pasos mockeables"; then
      USE_MOCKS=0
      run_llm_preflight
      : > "${STDOUT_FILE}"
      : > "${STDERR_FILE}"
      PY_ARGS=(--request "${REQUEST}")
      if run_pipeline_once "${PY_ARGS[@]}"; then
        cmd_exit=0
      else
        cmd_exit=$?
      fi
    fi
  fi
fi

echo "EXIT=${cmd_exit}" | tee -a "${LOG_FILE}" >&2

if [[ "${cmd_exit}" -eq 0 ]]; then
  if python -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" "${STDOUT_FILE}" >/dev/null 2>&1; then
    cp "${STDOUT_FILE}" "${TRACE_CACHE_FILE}"
    log "[INFO] updated mock trace cache: ${TRACE_CACHE_FILE}"
  else
    log "[WARN] salida no valida como JSON; no se actualiza cache de mocks"
  fi
fi

printf '\n===== wc =====\n' >&2
wc -c "${STDOUT_FILE}" "${STDERR_FILE}" >&2
printf '\n===== stdout head =====\n' >&2
head -n 40 "${STDOUT_FILE}" >&2 || true
printf '\n===== stderr tail =====\n' >&2
tail -n 80 "${STDERR_FILE}" >&2 || true

if [[ "${cmd_exit}" -eq 0 ]]; then
  GENERATED_PROJECT_DIR=$(python -c "import json; d=json.load(open('${STDOUT_FILE}')); print(d.get('generated_project_path') or d.get('project_path') or '')" 2>/dev/null || true)
  GENERATED_DSK=""
  FALLBACK_DSK=""
  if [[ -n "${GENERATED_PROJECT_DIR}" ]]; then
    GENERATED_DSK="${GENERATED_PROJECT_DIR}/$(basename "${GENERATED_PROJECT_DIR}").dsk"
  fi

  if [[ -n "${GENERATED_DSK}" && ! -f "${GENERATED_DSK}" ]]; then
    FALLBACK_DSK="$(find_latest_generated_dsk)"
    if [[ -n "${FALLBACK_DSK}" && -f "${FALLBACK_DSK}" ]]; then
      log "[WARN] DSK del run actual no encontrado; se usara el ultimo DSK disponible: ${FALLBACK_DSK}"
      GENERATED_DSK="${FALLBACK_DSK}"
    fi
  fi

  if [[ -n "${GENERATED_DSK}" && -f "${GENERATED_DSK}" ]]; then
    RUN_STEM="$(basename "${GENERATED_DSK}" .dsk)"
    RUN_BIN_NAME="${RUN_STEM}.bin"

    pkill -f -i Caprice32 2>/dev/null || true
    log "[INFO] launching Caprice32 with ${GENERATED_DSK}"

    if [[ ! -x "${CAP32_BIN}" || ! -f "${CAP32_RESOURCES_DIR}/cap32.cfg" ]]; then
      log "[WARN] Caprice32 is not installed at ${CAP32_APP}, skipping emulator launch"
      exit "${cmd_exit}"
    fi

    prepare_caprice32_cfg
    DISC_AUTO_CMD="$(printf 'run\"%s\"\n' "${RUN_BIN_NAME}")"
    launch_caprice32_with_autocmd "${GENERATED_DSK}" "${DISC_AUTO_CMD}"
    disown
  else
    log "[WARN] no DSK found, skipping emulator launch"
  fi
fi

exit "${cmd_exit}"