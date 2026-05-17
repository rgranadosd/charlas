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
CAP32_APP="/Applications/Caprice32.app"
CAP32_BIN="${CAP32_APP}/Contents/MacOS/Caprice32"
CAP32_RESOURCES_DIR="${CAP32_APP}/Contents/Resources"
CAP32_CFG="/tmp/cap32_pipeline_ghosts.cfg"
CAP32_BOOT_TIME="320"

STDOUT_FILE="${ROOT}/pipeline_ghosts_output.json"
STDERR_FILE="${ROOT}/pipeline_ghosts_stderr.log"
LOG_FILE="${ROOT}/pipeline_ghosts_output.log"

timestamp() { date +"%Y-%m-%d %H:%M:%S"; }

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" | tee -a "${LOG_FILE}" >&2
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

# Launch Caprice32 with the generated DSK
if [[ "${cmd_exit}" -eq 0 ]]; then
  GENERATED_PROJECT_DIR=$(python -c "import json; d=json.load(open('${STDOUT_FILE}')); print(d.get('generated_project_path') or d.get('project_path') or '')" 2>/dev/null || true)
  CONTRACT_STATUS=$(python -c "import json, re; d=json.load(open('${STDOUT_FILE}')); texts=[str(d.get('contract_validation','')), str(d.get('contractvalidation','')), str(d.get('final_output',''))];
for text in texts:
  m=re.search(r\"status='([^']+)'\", text)
  if m:
    print(m.group(1))
    raise SystemExit(0)
print('')" 2>/dev/null || true)
  BUILD_STATUS=$(python -c "import json, re; d=json.load(open('${STDOUT_FILE}')); texts=[str(d.get('build_validation','')), str(d.get('final_output',''))];
for text in texts:
  m=re.search(r\"build_validation:\\s*\\{.*?\\\"status\\\":\\s*\\\"([^\\\"]+)\\\"\", text, re.S)
  if m:
    print(m.group(1))
    raise SystemExit(0)
  m=re.search(r\"status='([^']+)'\", text)
  if m and 'build_validation' in text:
    print(m.group(1))
    raise SystemExit(0)
print('')" 2>/dev/null || true)
  GENERATED_DSK=""
  if [[ -n "${GENERATED_PROJECT_DIR}" ]]; then
    GENERATED_DSK="${GENERATED_PROJECT_DIR}/$(basename "${GENERATED_PROJECT_DIR}").dsk"
  fi

  if [[ -n "${CONTRACT_STATUS}" && "${CONTRACT_STATUS}" != "pass" ]]; then
    log "[WARN] contract_validation status is ${CONTRACT_STATUS}; refusing to auto-launch generated output"
    GENERATED_DSK=""
  fi

  if [[ -n "${BUILD_STATUS}" && "${BUILD_STATUS}" != "pass" ]]; then
    log "[WARN] build_validation status is ${BUILD_STATUS}; refusing to auto-launch generated output"
    GENERATED_DSK=""
  fi

  if [[ -n "${GENERATED_PROJECT_DIR}" && ! -f "${GENERATED_DSK}" ]]; then
    if [[ -n "${BUILD_STATUS}" && "${BUILD_STATUS}" != "pass" ]]; then
      log "[WARN] current pipeline run produced ${GENERATED_PROJECT_DIR} but build status is ${BUILD_STATUS}; refusing to boot a stale DSK"
      GENERATED_DSK=""
    else
      log "[WARN] current pipeline run produced ${GENERATED_PROJECT_DIR} but no DSK was found at ${GENERATED_DSK}"
      GENERATED_DSK=""
    fi
  fi

  if [[ -z "${GENERATED_PROJECT_DIR}" ]]; then
    log "[WARN] pipeline output did not expose a generated project path; refusing unsafe fallback to a previous DSK"
  fi

  if [[ -n "${GENERATED_DSK}" && -f "${GENERATED_DSK}" && -n "${BUILD_STATUS}" && "${BUILD_STATUS}" != "pass" ]]; then
    log "[WARN] build_validation status is ${BUILD_STATUS}; refusing to auto-launch an invalid generated DSK"
  elif [[ -n "${GENERATED_DSK}" && -f "${GENERATED_DSK}" ]]; then
    pkill -f -i Caprice32 2>/dev/null || true
    log "[INFO] launching Caprice32 with ${GENERATED_DSK}"
    DSK_BASENAME="$(basename "${GENERATED_DSK}" .dsk)"
    GENERATED_PROJECT_DIR="$(dirname "${GENERATED_DSK}")"
    BINARY_ADDRESSES_LOG="${GENERATED_PROJECT_DIR}/obj/binaryAddresses.log"
    if [[ ! -x "${CAP32_BIN}" || ! -f "${CAP32_RESOURCES_DIR}/cap32.cfg" ]]; then
      log "[WARN] Caprice32 is not installed at ${CAP32_APP}, skipping emulator launch"
      exit "${cmd_exit}"
    fi
    prepare_caprice32_cfg

    MAP_FILE="${GENERATED_PROJECT_DIR}/obj/${DSK_BASENAME}.map"
    NOI_FILE="${GENERATED_PROJECT_DIR}/obj/${DSK_BASENAME}.noi"
    LOAD_ADDRESS_HEX="$(python -c "import pathlib, re, sys; text=pathlib.Path(sys.argv[1]).read_text(encoding='utf-8', errors='ignore'); m=re.search(r'Load\s+Address\s*=\s*([0-9A-Fa-f]+)', text); print(m.group(1).upper() if m else '')" "${BINARY_ADDRESSES_LOG}" 2>/dev/null || true)"
    RUN_ADDRESS_DEC="$(python -c "import pathlib, re, sys; paths=sys.argv[1:];
patterns=(
  r'Run\s+Address\s*=\s*([0-9A-Fa-f]+)',
  r'cpc_run_address\s+0x([0-9A-Fa-f]+)',
  r'\b([0-9A-Fa-f]+)\s+cpc_run_address\b',
  r'_main\s+0x([0-9A-Fa-f]+)',
  r'\b([0-9A-Fa-f]+)\s+_main\b',
);
for path in paths:
  if not path:
    continue
  file_path = pathlib.Path(path)
  if not file_path.exists():
    continue
  text = file_path.read_text(encoding='utf-8', errors='ignore')
  for pattern in patterns:
    match = re.search(pattern, text)
    if match:
      value = match.group(1)
      try:
        print(int(value, 16))
        raise SystemExit(0)
      except ValueError:
        continue
print('')" "${BINARY_ADDRESSES_LOG}" "${MAP_FILE}" "${NOI_FILE}" 2>/dev/null || true)"
    GENERATED_BIN="${GENERATED_PROJECT_DIR}/obj/${DSK_BASENAME}.bin"
    GENERATED_DISC_BAS="${GENERATED_PROJECT_DIR}/dsk_files/DISC.BAS"
    CAP32_BOOTSTRAP_BIN="/tmp/${DSK_BASENAME}_cap32_boot.bin"
    CAP32_BOOTSTRAP_OFFSET_HEX="8000"

    if [[ -f "${GENERATED_DISC_BAS}" ]]; then
      log "[INFO] Caprice32 boot using DISC.BAS disk loader"
      DISC_AUTO_CMD=$'|disc\nrun"disc"\n'
      launch_caprice32_with_autocmd "${GENERATED_DSK}" "${DISC_AUTO_CMD}"
    elif [[ -n "${LOAD_ADDRESS_HEX}" && -n "${RUN_ADDRESS_DEC}" && -f "${GENERATED_BIN}" ]]; then
      if python - "${GENERATED_BIN}" "${CAP32_BOOTSTRAP_BIN}" "${CAP32_BOOTSTRAP_OFFSET_HEX}" "${LOAD_ADDRESS_HEX}" "${RUN_ADDRESS_DEC}" <<'PY'
import pathlib
import sys

source_path = pathlib.Path(sys.argv[1])
bootstrap_path = pathlib.Path(sys.argv[2])
bootstrap_offset = int(sys.argv[3], 16)
load_address = int(sys.argv[4], 16)
run_address = int(sys.argv[5])
payload = source_path.read_bytes()
stub_size = 18
source_address = bootstrap_offset + stub_size
if len(payload) > 0xFFFF:
    raise SystemExit(1)
stub = bytes((
    0xF3,
    0x31, 0xF0, 0xBF,
    0x21, source_address & 0xFF, (source_address >> 8) & 0xFF,
    0x11, load_address & 0xFF, (load_address >> 8) & 0xFF,
    0x01, len(payload) & 0xFF, (len(payload) >> 8) & 0xFF,
    0xED, 0xB0,
    0xC3, run_address & 0xFF, (run_address >> 8) & 0xFF,
))
bootstrap_path.write_bytes(stub + payload)
PY
      then
        log "[INFO] Caprice32 disk-command boot using run address ${RUN_ADDRESS_DEC} (preferred over injected runner)"
        printf -v BIN_AUTO_CMD '|disc\nmemory 16383\nload"%s.BIN"\ncall %s\n' "${DSK_BASENAME}" "${RUN_ADDRESS_DEC}"
        launch_caprice32_with_autocmd "${GENERATED_DSK}" "${BIN_AUTO_CMD}"
      else
        log "[WARN] failed to build Caprice32 bootstrap payload, falling back to disk-command boot"
        printf -v BIN_AUTO_CMD '|disc\nmemory 16383\nload"%s.BIN"\ncall %s\n' "${DSK_BASENAME}" "${RUN_ADDRESS_DEC}"
        launch_caprice32_with_autocmd "${GENERATED_DSK}" "${BIN_AUTO_CMD}"
      fi
    elif [[ -n "${RUN_ADDRESS_DEC}" ]]; then
      log "[INFO] Caprice32 direct boot using run address ${RUN_ADDRESS_DEC}"
      printf -v BIN_AUTO_CMD '|disc\nmemory 16383\nload"%s.BIN"\ncall %s\n' "${DSK_BASENAME}" "${RUN_ADDRESS_DEC}"
      launch_caprice32_with_autocmd "${GENERATED_DSK}" "${BIN_AUTO_CMD}"
    else
      log "[WARN] run address not found, falling back to DISC.BAS boot"
      DISC_AUTO_CMD=$'|disc\nrun"disc"\n'
      launch_caprice32_with_autocmd "${GENERATED_DSK}" "${DISC_AUTO_CMD}"
    fi
    disown
  elif [[ -n "${GENERATED_PROJECT_DIR}" ]]; then
    log "[WARN] skipping emulator launch because the current pipeline run did not produce a bootable DSK"
  else
    log "[WARN] no DSK found, skipping emulator launch"
  fi
fi

exit "${cmd_exit}"