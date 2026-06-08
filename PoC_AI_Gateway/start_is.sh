#!/bin/bash

set -euo pipefail

LOG_FILE="/tmp/start_is.log"
exec > >(tee -a "$LOG_FILE") 2>&1

IS_DIR="/Users/rafagranados/Develop/wso2/wso2is-7.1.0"
IS_PORT=9443  # Puerto por defecto (offset 0)

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
  for p in "$IS_PORT"; do
    if lsof -i ":$p" -sTCP:LISTEN -t >/dev/null 2>&1; then
      PIDS=$(lsof -i ":$p" -sTCP:LISTEN -t | tr '\n' ' ')
      log "Puerto $p ocupado por: $PIDS. Matando..."
      kill -9 $PIDS 2>/dev/null || true
    fi
  done
  # Cerrar restos conocidos
  pkill -f "wso2server\|carbon.*is" 2>/dev/null || true
}

start_is() {
  if [ ! -f "$IS_DIR/bin/wso2server.sh" ]; then
    log "ERROR: No encuentro $IS_DIR/bin/wso2server.sh"; exit 1
  fi
  
  log "Limpiando procesos y recursos anteriores..."
  pkill -9 -f "wso2server" 2>/dev/null || true
  pkill -9 -f "carbon.*is" 2>/dev/null || true
  lsof -ti :9443 | xargs kill -9 2>/dev/null || true
  rm -f "$IS_DIR/wso2carbon.pid" 2>/dev/null || true
  sleep 2
  
  log "Iniciando WSO2 Identity Server desde $IS_DIR (puerto por defecto 9443, offset 0)"
  cd "$IS_DIR"
  export CARBON_HOME="$IS_DIR"
  
  # Usar start para manejar correctamente el proceso
  ./bin/wso2server.sh start
  
  sleep 5
  if [ -f "$IS_DIR/wso2carbon.pid" ]; then
    PID=$(cat "$IS_DIR/wso2carbon.pid")
    log "Identity Server iniciado con PID: $PID"
  else
    log "Verificando si el servidor se inició..."
    ps aux | grep "[w]so2server" && log "Proceso encontrado" || log "⚠️  Proceso no encontrado aún"
  fi
  sleep 5
}

healthcheck() {
  wait_for_port localhost "$IS_PORT" 240
  # Verificar que responde - IS 7.1.0 usa /console en lugar de /carbon
  local tries=0
  while true; do
    code=$(curl -sk -o /dev/null -w "%{http_code}" "https://localhost:${IS_PORT}/console/") || code=000
    log "IS console http=$code"
    [[ "$code" =~ ^[45] ]] && tries=$((tries+1)) && [ "$tries" -lt 15 ] && { sleep 4; continue; }
    [[ "$code" =~ ^[45] ]] && { log "ERROR: Identity Server no responde correctamente"; exit 1; }
    break
  done
  log "Identity Server operativo"
}

open_browser() {
  if command -v open >/dev/null 2>&1; then
    log "Abriendo Identity Server Console en navegador"
    open "https://localhost:${IS_PORT}/console" || true
  fi
}

main() {
  log "Inicio start_is.sh (logs en $LOG_FILE)"
  log "IS_DIR=$IS_DIR"
  log "IS_PORT=$IS_PORT (offset 0, puerto por defecto)"
  free_ports
  start_is
  healthcheck
  open_browser
  log "Listo"
}

main "$@"

