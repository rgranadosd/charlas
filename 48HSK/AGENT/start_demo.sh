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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_FILE="$SCRIPT_DIR/agent_gpt4.py"
ENV_FILE="$SCRIPT_DIR/.env"

PURGE_SESSION=false
VERBOSE=false
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

cd "$SCRIPT_DIR"

if [ ! -f "$AGENT_FILE" ]; then
    warn "${RED}ERROR: agent_gpt4.py no encontrado en $SCRIPT_DIR${NC}"
    exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
    warn "${RED}ERROR: No se encontró el archivo .env en $SCRIPT_DIR${NC}"
    exit 1
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
    warn "${YELLOW}  pip install semantic-kernel openai httpx requests python-dotenv urllib3${NC}"
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

source "$VENV_DIR/bin/activate"

if [ -z "${VIRTUAL_ENV:-}" ]; then
    warn "${RED}ERROR: El entorno virtual no se activó correctamente${NC}"
    exit 1
fi

if ! python3 -c "import semantic_kernel, requests, dotenv, openai, httpx" 2>/dev/null; then
    log "${YELLOW}Instalando dependencias...${NC}"
    pip install -q -U pip
    pip install -q semantic-kernel openai httpx requests python-dotenv urllib3
fi

log "${GREEN}✓ Virtual environment activated successfully${NC}"
log "${GREEN}✓ Dependencies verified${NC}"
log "${ORANGE}Virtual environment: $VIRTUAL_ENV${NC}"
log "${ORANGE}Python version: $(python3 --version)${NC}"
log "${ORANGE}Python path: $(which python3)${NC}"
log "${ORANGE}Working directory: $(pwd)${NC}"
log "${ORANGE}Agent file: $AGENT_FILE${NC}"
log "${ORANGE}Venv directory: $VENV_DIR${NC}"
log ""

# Comprobación: WSO2 Identity Server
WSO2_BASE="${WSO2_IS_BASE:-https://localhost:9443}"
is_up=false
if curl -skf "${WSO2_BASE}/.well-known/openid-configuration" >/dev/null 2>&1; then
    is_up=true
else
    http_code=$(curl -sk -o /dev/null -w "%{http_code}" "${WSO2_BASE}/scim2/Users" || echo "000")
    if [[ "$http_code" =~ ^(200|201|204|301|302|401)$ ]]; then
        is_up=true
    fi
fi
if [ "$is_up" != true ]; then
    warn "${RED}ERROR: No se pudo verificar que WSO2 IS esté disponible.${NC}"
    warn "${YELLOW}Asegúrate de que WSO2 IS esté arrancado y accesible en ${WSO2_BASE}.${NC}"
    exit 1
fi
log "${GREEN}✓ WSO2 IS detectado correctamente${NC}"

if [ "$PURGE_SESSION" = true ]; then
    FINAL_ARGS=(--force-auth)
    log "${ORANGE}🔄 Ejecutando en modo PURGE con autenticación forzada${NC}"
else
    FINAL_ARGS=()
fi

if [ ${#EXTRA_ARGS[@]} -gt 0 ]; then
    FINAL_ARGS+=("${EXTRA_ARGS[@]}")
fi

log "${ORANGE}Comando: python3 $AGENT_FILE ${FINAL_ARGS[*]-}${NC}"
log ""

if [ ${#FINAL_ARGS[@]} -gt 0 ]; then
    python3 "$AGENT_FILE" "${FINAL_ARGS[@]}"
else
    python3 "$AGENT_FILE"
fi

log "${ORANGE}============================================${NC}"
log "${ORANGE}  AGENT FINISHED${NC}"
log "${ORANGE}============================================${NC}"
