#!/bin/bash

set -euo pipefail

LOG_FILE="/tmp/start_apim.log"
exec > >(tee -a "$LOG_FILE") 2>&1

APIM_DIR="${APIM_DIR:-/Users/rafagranados/Develop/wso2/PoC_AI_Gateway/wso2am-4.6.0-beta}"
ALT_APIM_DIR="/Users/rafagranados/Develop/wso2/PoC_AI_Gateway/borrar_ahora/wso2am-4.6.0-beta"
APIM_PORT=9453
GW_PORT=8253

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

wait_for_port() {
  local host="$1" port="$2" timeout="${3:-240}" elapsed=0
  log "Esperando puerto ${host}:${port} (timeout ${timeout}s)"
  while ! nc -z "$host" "$port" 2>/dev/null; do
    sleep 2; elapsed=$((elapsed+2)); printf "."
    if [ "$elapsed" -ge "$timeout" ]; then echo; log "TIMEOUT ${host}:${port}"; return 1; fi
  done
  echo; log "Puerto ${host}:${port} disponible"
}

free_ports() {
  for p in "$APIM_PORT" "$GW_PORT"; do
    if lsof -i ":$p" -sTCP:LISTEN -t >/dev/null 2>&1; then
      PIDS=$(lsof -i ":$p" -sTCP:LISTEN -t | tr '\n' ' ')
      log "Puerto $p ocupado por: $PIDS. Matando..."
      kill -9 $PIDS 2>/dev/null || true
    fi
  done
  # Cerrar restos conocidos
  pkill -f wso2am 2>/dev/null || true
  pkill -f carbon 2>/dev/null || true
}

start_apim() {
  if [ ! -x "$APIM_DIR/bin/api-manager.sh" ]; then
    if [ -x "$ALT_APIM_DIR/bin/api-manager.sh" ]; then
      APIM_DIR="$ALT_APIM_DIR"
      log "Usando APIM_DIR alternativo: $APIM_DIR"
    else
      log "ERROR: No encuentro $APIM_DIR/bin/api-manager.sh"; exit 1
    fi
  fi
  log "Iniciando WSO2 APIM desde $APIM_DIR"
  "$APIM_DIR/bin/api-manager.sh" start || true
}

healthcheck() {
  wait_for_port localhost "$APIM_PORT" 240
  wait_for_port localhost "$GW_PORT" 240
  # Cabeceras rápidas
  curl -skI "https://localhost:${APIM_PORT}/carbon/" | head -n1 || true
  curl -skI "https://localhost:${GW_PORT}/" | head -n1 || true
  # Evitar 5xx en token endpoint
  local tries=0
  while true; do
    code=$(curl -sk -o /dev/null -w "%{http_code}" -X POST "https://localhost:${APIM_PORT}/oauth2/token" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=client_credentials") || code=000
    log "token http=$code"
    [[ "$code" =~ ^5 ]] && tries=$((tries+1)) && [ "$tries" -lt 15 ] && { sleep 4; continue; }
    [[ "$code" =~ ^5 ]] && { log "ERROR: /oauth2/token sigue en 5xx"; exit 1; }
    break
  done
  log "APIM operativo"
}

open_browser() {
  if command -v open >/dev/null 2>&1; then
    log "Abriendo APIM Publisher en navegador"
    open "https://localhost:${APIM_PORT}/publisher" || true
  fi
}

main() {
  log "Inicio start_apim.sh (logs en $LOG_FILE)"
  log "APIM_DIR=$APIM_DIR"
  free_ports
  start_apim
  healthcheck
  open_browser
  log "Listo"
}

main "$@"


