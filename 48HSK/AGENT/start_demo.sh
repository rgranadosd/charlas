#!/usr/bin/env bash

# ============================================
# SCRIPT PARA INICIAR EL AGENTE PYTHON IA x WSO2
# ============================================
# Uso: ./start_demo.sh [--purge] [otros argumentos]
#   --purge: Borra cache de tokens y fuerza nueva autenticación completa

set -euo pipefail

# Colores (evitar azul: lo tratamos como "debug" y se ve fatal)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
ORANGE='\033[38;5;208m'
NC='\033[0m'

# Dependencias fijadas para evitar incompatibilidades en runtime
PY_DEPS=(
    "semantic-kernel==1.37.0"
    "openai>=1.59.0,<2"
    "httpx==0.28.1"
    "requests==2.32.5"
    "python-dotenv>=1,<2"
    "urllib3<3"
)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_FILE="$SCRIPT_DIR/agent_gpt4.py"
ENV_FILE="$SCRIPT_DIR/.env"
PRECHECK_FILE="$SCRIPT_DIR/pre_demo_check.sh"
CONFIG_FILE="$SCRIPT_DIR/start_demo.conf"

if [ -f "$CONFIG_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
    set +a
fi

MILVUS_SCRIPT_DEFAULT="$SCRIPT_DIR/milvus-deployment/milvus.sh"
MILVUS_SCRIPT="${MILVUS_DEPLOYMENT_SCRIPT:-$MILVUS_SCRIPT_DEFAULT}"
WSO2_ROOT_DEFAULT="/Users/rafagranados/Develop/wso2"
WSO2_ROOT="${WSO2_HOME_ROOT:-$WSO2_ROOT_DEFAULT}"
IS_SCRIPT_DEFAULT="$WSO2_ROOT/wso2is-7.2.0/bin/wso2server.sh"
APIM_SCRIPT_DEFAULT="$WSO2_ROOT/wso2am-4.6.0/bin/api-manager.sh"
IS_SCRIPT="${WSO2_IS_START_SCRIPT:-$IS_SCRIPT_DEFAULT}"
APIM_SCRIPT="${WSO2_APIM_START_SCRIPT:-$APIM_SCRIPT_DEFAULT}"

PURGE_SESSION=false
VERBOSE=false
SKIP_PRECHECK=false
declare -a EXTRA_ARGS=()
declare -a FINAL_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --purge)
            PURGE_SESSION=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --skip-precheck)
            SKIP_PRECHECK=true
            shift
            ;;
        *)
            EXTRA_ARGS+=("$1")
            shift
            ;;
    esac
done

log() {
    if [ "$VERBOSE" = true ]; then
        # shellcheck disable=SC2059
        printf "%b\n" "$1"
    fi
}

warn() {
    # shellcheck disable=SC2059
    printf "%b\n" "$1"
}

dedupe_paths() {
    awk '!seen[$0]++'
}

discover_latest_executable() {
    local pattern
    local matches=()

    for pattern in "$@"; do
        while IFS= read -r match; do
            if [ -x "$match" ]; then
                matches+=("$match")
            fi
        done < <(compgen -G "$pattern" || true)
    done

    if [ ${#matches[@]} -eq 0 ]; then
        return 1
    fi

    printf '%s\n' "${matches[@]}" | dedupe_paths | LC_ALL=C sort | tail -n 1
}

resolve_wso2_is_script() {
    if [ -n "${WSO2_IS_START_SCRIPT:-}" ] && [ -x "$WSO2_IS_START_SCRIPT" ]; then
        printf '%s\n' "$WSO2_IS_START_SCRIPT"
        return 0
    fi

    if [ -x "$IS_SCRIPT" ]; then
        printf '%s\n' "$IS_SCRIPT"
        return 0
    fi

    discover_latest_executable \
        "$WSO2_ROOT/wso2is-*/bin/wso2server.sh" \
        "$WSO2_ROOT/wso2is-*/bin/adaptive.sh"
}

resolve_wso2_apim_script() {
    if [ -n "${WSO2_APIM_START_SCRIPT:-}" ] && [ -x "$WSO2_APIM_START_SCRIPT" ]; then
        printf '%s\n' "$WSO2_APIM_START_SCRIPT"
        return 0
    fi

    if [ -x "$APIM_SCRIPT" ]; then
        printf '%s\n' "$APIM_SCRIPT"
        return 0
    fi

    discover_latest_executable "$WSO2_ROOT/wso2am-*/bin/api-manager.sh"
}

is_wso2_available() {
    local base_url="$1"
    if curl -skf "${base_url}/.well-known/openid-configuration" >/dev/null 2>&1; then
        return 0
    fi
    local status
    status=$(curl -sk -o /dev/null -w "%{http_code}" "${base_url}/scim2/Users" || echo "000")
    [[ "$status" =~ ^(200|201|204|301|302|401)$ ]]
}

is_apim_token_available() {
    local token_url="${WSO2_APIM_TOKEN_ENDPOINT:-https://localhost:9453/oauth2/token}"
    local status
    status=$(curl -sk -o /dev/null -w "%{http_code}" "$token_url" || echo "000")
    [[ "$status" =~ ^(200|400|401|405)$ ]]
}

cleanup_stale_wso2_processes() {
    local script_path="$1"
    local label="$2"
    local product_home
    local wso2_pids

    product_home="$(cd "$(dirname "$script_path")/.." && pwd)"
    wso2_pids=$(pgrep -f "$product_home" 2>/dev/null || true)

    if [ -z "$wso2_pids" ]; then
        return 0
    fi

    warn "${YELLOW}Detectados procesos previos de ${label} (PIDs: $wso2_pids). Limpiando antes del autoarranque...${NC}"
    kill -TERM $wso2_pids 2>/dev/null || true
    sleep 8

    local still_running
    still_running=$(pgrep -f "$product_home" 2>/dev/null || true)
    if [ -n "$still_running" ]; then
        warn "${YELLOW}Forzando cierre de procesos bloqueados de ${label} (PIDs: $still_running)...${NC}"
        kill -KILL $still_running 2>/dev/null || true
        sleep 2
    fi
}

ensure_wso2_is_running() {
    local base_url="$1"
    local is_script

    if is_wso2_available "$base_url"; then
        log "${GREEN}✓ WSO2 IS ya estaba disponible${NC}"
        return 0
    fi

    is_script="$(resolve_wso2_is_script || true)"
    if [ -z "$is_script" ] || [ ! -x "$is_script" ]; then
        warn "${RED}ERROR: WSO2 IS no está disponible y no se encontró script ejecutable.${NC}"
        warn "${YELLOW}Buscado en:${NC} $WSO2_ROOT/wso2is-*/bin/{wso2server.sh,adaptive.sh}"
        warn "${YELLOW}Define WSO2_IS_START_SCRIPT si quieres fijar la ruta manualmente.${NC}"
        return 1
    fi

    cleanup_stale_wso2_processes "$is_script" "WSO2 IS"

    warn "${ORANGE}WSO2 IS no disponible. Intentando arranque automático con:${NC} $is_script"
    nohup "$is_script" >/tmp/wso2is_autostart.log 2>&1 &

    for _ in {1..45}; do
        if is_wso2_available "$base_url"; then
            IS_SCRIPT="$is_script"
            log "${GREEN}✓ WSO2 IS arrancado automáticamente${NC}"
            return 0
        fi
        sleep 4
    done

    warn "${RED}ERROR: WSO2 IS no respondió tras autoarranque${NC}"
    warn "${YELLOW}Revisa log:${NC} /tmp/wso2is_autostart.log"
    return 1
}

ensure_apim_running() {
    local apim_script

    if is_apim_token_available; then
        log "${GREEN}✓ WSO2 APIM ya estaba disponible${NC}"
        return 0
    fi

    apim_script="$(resolve_wso2_apim_script || true)"
    if [ -z "$apim_script" ] || [ ! -x "$apim_script" ]; then
        warn "${RED}ERROR: WSO2 APIM no está disponible y no se encontró script ejecutable.${NC}"
        warn "${YELLOW}Buscado en:${NC} $WSO2_ROOT/wso2am-*/bin/api-manager.sh"
        warn "${YELLOW}Define WSO2_APIM_START_SCRIPT si quieres fijar la ruta manualmente.${NC}"
        return 1
    fi

    cleanup_stale_wso2_processes "$apim_script" "WSO2 APIM"

    warn "${ORANGE}WSO2 APIM no disponible. Intentando arranque automático con:${NC} $apim_script"
    nohup "$apim_script" >/tmp/apim_autostart.log 2>&1 &

    for _ in {1..45}; do
        if is_apim_token_available; then
            APIM_SCRIPT="$apim_script"
            log "${GREEN}✓ WSO2 APIM arrancado automáticamente${NC}"
            return 0
        fi
        sleep 4
    done

    warn "${RED}ERROR: WSO2 APIM no respondió tras autoarranque${NC}"
    warn "${YELLOW}Revisa log:${NC} /tmp/apim_autostart.log"
    return 1
}

cd "$SCRIPT_DIR"

if [ ! -f "$AGENT_FILE" ]; then
    warn "${RED}ERROR: agent_gpt4.py no encontrado en $SCRIPT_DIR${NC}"
    exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
    warn "${RED}ERROR: No se encontró el archivo .env en $SCRIPT_DIR${NC}"
    exit 1
fi

# Asegurar Milvus/Zilliz antes de checks de gateway (evita fallo de Semantic Cache)
if [ -x "$MILVUS_SCRIPT" ]; then
    if ! curl -sf "http://localhost:9091/healthz" >/dev/null 2>&1; then
        warn "${ORANGE}Levantando Milvus/Zilliz para APIM Semantic Cache...${NC}"
        if ! "$MILVUS_SCRIPT" start; then
            warn "${RED}ERROR: No se pudo levantar Milvus/Zilliz con $MILVUS_SCRIPT${NC}"
            warn "${YELLOW}Puedes probar manualmente: $MILVUS_SCRIPT start${NC}"
            exit 1
        fi
    else
        log "${GREEN}✓ Milvus/Zilliz ya estaba activo${NC}"
    fi
else
    warn "${YELLOW}WARN: No se encontró script ejecutable de Milvus/Zilliz en: $MILVUS_SCRIPT${NC}"
    warn "${YELLOW}Si APIM usa Semantic Cache, define MILVUS_DEPLOYMENT_SCRIPT o corrígelo en start_demo.sh${NC}"
fi

# Detectar venv (preferir ./venv)
VENV_DIR=""
if [ -d "$SCRIPT_DIR/venv" ]; then
    VENV_DIR="$SCRIPT_DIR/venv"
elif [ -d "$SCRIPT_DIR/../venv" ]; then
    VENV_DIR="$SCRIPT_DIR/../venv"
else
    warn "${RED}ERROR: No se encontró un entorno virtual (./venv ni ../venv)${NC}"
    warn "${YELLOW}Crea uno aquí e instala dependencias:${NC}"
    warn "${YELLOW}  python3 -m venv venv${NC}"
    warn "${YELLOW}  source venv/bin/activate${NC}"
    warn "${YELLOW}  pip install -U pip${NC}"
    warn "${YELLOW}  pip install ${PY_DEPS[*]}${NC}"
    exit 1
fi

VENV_PY=""
for py_candidate in "$VENV_DIR/bin/python3" "$VENV_DIR/bin/python"; do
    if [ -x "$py_candidate" ]; then
        VENV_PY="$py_candidate"
        break
    fi
done

if [ -z "$VENV_PY" ]; then
    warn "${RED}ERROR: No se encontró un intérprete Python ejecutable dentro de $VENV_DIR/bin${NC}"
    exit 1
fi

# Matar instancias previas
log "${ORANGE}🔪 Matando instancias previas del agente...${NC}"
AGENT_PIDS=$(pgrep -f "python.*agent_gpt4.py" 2>/dev/null || true)
if [ -n "$AGENT_PIDS" ]; then
    log "${YELLOW}Encontradas instancias corriendo (PIDs: $AGENT_PIDS)${NC}"
    kill -TERM $AGENT_PIDS 2>/dev/null || true
    sleep 2
    STILL_RUNNING=$(pgrep -f "python.*agent_gpt4.py" 2>/dev/null || true)
    if [ -n "$STILL_RUNNING" ]; then
        log "${RED}Forzando terminación (SIGKILL)...${NC}"
        kill -KILL $STILL_RUNNING 2>/dev/null || true
    fi
    log "${GREEN}✓ Instancias previas terminadas${NC}"
else
    log "${GREEN}✓ No hay instancias previas corriendo${NC}"
fi

log "${ORANGE}🔪 Liberando puertos de callback OAuth...${NC}"
for port in 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010; do
    PORT_PID=$(lsof -ti:$port 2>/dev/null || true)
    if [ -n "$PORT_PID" ]; then
        log "${YELLOW}Liberando puerto $port (PID: $PORT_PID)${NC}"
        kill -TERM $PORT_PID 2>/dev/null || true
    fi
done
log "${GREEN}✓ Puertos liberados${NC}"

if [ "$PURGE_SESSION" = true ]; then
    log "${ORANGE}🔥 Limpiando sesión...${NC}"
    rm -f "$SCRIPT_DIR/token_cache.json" 2>/dev/null || true
    log "${GREEN}✓ Sesión local limpiada${NC}"
    sleep 1
fi

if [ -f "$VENV_DIR/bin/activate" ]; then
    # Intentamos activar para arrastrar variables del entorno, pero el arranque
    # usa siempre el binario del venv para evitar activate scripts rotos.
    # shellcheck disable=SC1090
    source "$VENV_DIR/bin/activate" || true
fi

export VIRTUAL_ENV="$VENV_DIR"
export PATH="$VENV_DIR/bin:$PATH"
hash -r 2>/dev/null || true

ensure_python_pip() {
    if "$VENV_PY" -m pip --version >/dev/null 2>&1; then
        return 0
    fi

    log "${YELLOW}pip no está disponible en el entorno; intentando bootstrap con ensurepip...${NC}"
    "$VENV_PY" -m ensurepip --upgrade >/dev/null 2>&1 || true

    if ! "$VENV_PY" -m pip --version >/dev/null 2>&1; then
        warn "${RED}ERROR: No se pudo inicializar pip en el entorno virtual${NC}"
        exit 1
    fi
}

ensure_python_pip

if ! "$VENV_PY" - <<'PY' 2>/dev/null
import importlib.metadata as md

def major(version: str) -> int:
    return int(str(version).split('.', 1)[0])

required_exact = {
    'semantic-kernel': '1.37.0',
    'httpx': '0.28.1',
    'requests': '2.32.5',
}

for pkg, expected in required_exact.items():
    installed = md.version(pkg)
    if installed != expected:
        raise SystemExit(1)

openai_ver = md.version('openai')
if major(openai_ver) >= 2:
    raise SystemExit(1)

dotenv_ver = md.version('python-dotenv')
if major(dotenv_ver) != 1:
    raise SystemExit(1)

urllib3_ver = md.version('urllib3')
if major(urllib3_ver) >= 3:
    raise SystemExit(1)

print('ok')
PY
then
    log "${GREEN}✓ Dependencias compatibles detectadas${NC}"
else
    log "${YELLOW}Instalando/ajustando dependencias compatibles...${NC}"
    "$VENV_PY" -m pip install -q -U pip
    "$VENV_PY" -m pip install -q "${PY_DEPS[@]}"
fi

log "${GREEN}✓ Virtual environment activated successfully${NC}"
log "${GREEN}✓ Dependencies verified${NC}"
log "${ORANGE}Virtual environment: $VIRTUAL_ENV${NC}"
log "${ORANGE}Python version: $($VENV_PY --version)${NC}"
log "${ORANGE}Python path: $VENV_PY${NC}"
log "${ORANGE}Working directory: $(pwd)${NC}"
log "${ORANGE}Agent file: $AGENT_FILE${NC}"
log "${ORANGE}Venv directory: $VENV_DIR${NC}"
log ""

# Comprobación: WSO2 Identity Server
WSO2_BASE="${WSO2_IS_BASE:-https://localhost:9443}"
if ! ensure_wso2_is_running "$WSO2_BASE"; then
    warn "${RED}ERROR: No se pudo verificar que WSO2 IS esté disponible.${NC}"
    warn "${YELLOW}Asegúrate de que WSO2 IS esté arrancado y accesible en ${WSO2_BASE}.${NC}"
    exit 1
fi
log "${GREEN}✓ WSO2 IS detectado correctamente${NC}"

if ! ensure_apim_running; then
    warn "${RED}ERROR: No se pudo verificar que WSO2 APIM esté disponible.${NC}"
    warn "${YELLOW}Asegúrate de que WSO2 APIM esté arrancado y accesible en ${WSO2_APIM_TOKEN_ENDPOINT:-https://localhost:9453/oauth2/token}.${NC}"
    exit 1
fi
log "${GREEN}✓ WSO2 APIM detectado correctamente${NC}"

if [ "$PURGE_SESSION" = true ]; then
    FINAL_ARGS=(--force-auth)
    log "${ORANGE}🔄 Ejecutando en modo PURGE con autenticación forzada${NC}"
else
    FINAL_ARGS=()
fi

if [ ${#EXTRA_ARGS[@]} -gt 0 ]; then
    FINAL_ARGS+=("${EXTRA_ARGS[@]}")
fi

log "${ORANGE}Comando: $VENV_PY $AGENT_FILE ${FINAL_ARGS[*]-}${NC}"
log ""

if [ "$SKIP_PRECHECK" != true ] && [ -f "$PRECHECK_FILE" ]; then
    log "${ORANGE}Ejecutando pre-demo check...${NC}"
    if ! "$PRECHECK_FILE"; then
        warn "${RED}ERROR: pre_demo_check.sh falló. Abortando arranque.${NC}"
        warn "${YELLOW}Si quieres continuar sin check: ./start_demo.sh --skip-precheck${NC}"
        exit 1
    fi
    log "${GREEN}✓ Pre-demo check completado${NC}"
fi

if [ ${#FINAL_ARGS[@]} -gt 0 ]; then
    "$VENV_PY" "$AGENT_FILE" "${FINAL_ARGS[@]}"
else
    "$VENV_PY" "$AGENT_FILE"
fi

log "${ORANGE}============================================${NC}"
log "${ORANGE}  AGENT FINISHED${NC}"
log "${ORANGE}============================================${NC}"
