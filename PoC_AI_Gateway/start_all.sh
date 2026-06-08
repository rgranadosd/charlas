#!/bin/bash

set -euo pipefail

LOG_FILE="/tmp/start_all.log"
exec > >(tee -a "$LOG_FILE") 2>&1

AIGW_DIR="/Users/rafagranados/Develop/wso2/PoC_AI_Gateway/aigateway-demo"
STREAMLIT_PORT=8502

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

wait_for_port() {
  local host="$1" port="$2" timeout="${3:-60}" elapsed=0
  while ! nc -z "$host" "$port" 2>/dev/null; do
    sleep 2; elapsed=$((elapsed+2));
    if [ "$elapsed" -ge "$timeout" ]; then return 1; fi
  done
}

start_demo() {
  log "Preparando Streamlit en puerto $STREAMLIT_PORT"
  if lsof -i ":$STREAMLIT_PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
    PIDS=$(lsof -i ":$STREAMLIT_PORT" -sTCP:LISTEN -t | tr '\n' ' ')
    log "Puerto $STREAMLIT_PORT ocupado por: $PIDS. Matando..."
    kill -9 $PIDS 2>/dev/null || true
  fi
  cd "$AIGW_DIR"
  if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
    log "Activado .venv de aigateway-demo"
  fi
  nohup streamlit run demo_ui.py --server.port "$STREAMLIT_PORT" >/tmp/aigateway-demo.streamlit.log 2>&1 &
  if wait_for_port localhost "$STREAMLIT_PORT" 90; then
    log "Streamlit escuchando en http://localhost:$STREAMLIT_PORT"
    if command -v open >/dev/null 2>&1; then
      open "http://localhost:${STREAMLIT_PORT}" || true
    fi
  else
    log "ADVERTENCIA: Streamlit no levantó a tiempo. Revisa /tmp/aigateway-demo.streamlit.log"
  fi
}

main() {
  log "Inicio start_all.sh (logs en $LOG_FILE)"
  # Actualizar variables de entorno del sistema para evitar puertos antiguos
  export WSO2_TOKEN_URL=https://localhost:9453/oauth2/token
  export OPENAI_CHAT_COMPLETIONS_URL=https://localhost:8253/openaiapi/2.3.0/chat/completions
  export MISTRAL_CHAT_COMPLETIONS_URL=https://localhost:8253/mistralaiapi/0.0.2/v1/chat/completions
  export ANTHROPIC_CHAT_COMPLETIONS_URL=https://localhost:8253/anthropicapi/v1/messages
  # 1) Arrancar Identity Server (offset 20 = puerto 9463)
  /Users/rafagranados/Develop/wso2/PoC_AI_Gateway/start_is.sh
  # 2) Arrancar APIM y abrir Publisher (offset 10 = puerto 9453)
  /Users/rafagranados/Develop/wso2/PoC_AI_Gateway/start_apim.sh
  # 3) Lanzar la demo cuando APIM ya está operativo
  start_demo
  log "Listo"
}

main "$@"
