#!/bin/bash
# =============================================================================
# Milvus Deployment Script for WSO2 API Manager Semantic Cache
# Local copy inside AGENT directory — collocated with the demo project
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
HEALTH_URL="http://localhost:9091/healthz"
MAX_RETRIES=30
RETRY_INTERVAL=5
REQUIRED_PORTS=(9000 9001 19530 9091 3000)
declare -a COMPOSE_CMD=()

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

resolve_compose_cmd() {
    if podman compose version >/dev/null 2>&1; then
        COMPOSE_CMD=("podman" "compose")
        log_info "Usando comando nativo: podman compose"
        return 0
    fi

    if ! command -v podman-compose >/dev/null 2>&1; then
        log_error "No se encontró podman compose ni podman-compose"
        return 1
    fi

    local pc_path
    pc_path="$(command -v podman-compose)"

    if "$pc_path" version >/dev/null 2>&1; then
        COMPOSE_CMD=("$pc_path")
        log_info "Usando comando: $pc_path"
        return 0
    fi

    if command -v python3 >/dev/null 2>&1 && python3 "$pc_path" version >/dev/null 2>&1; then
        COMPOSE_CMD=("python3" "$pc_path")
        log_warn "podman-compose roto como ejecutable; usando fallback con python3"
        return 0
    fi

    log_error "No se pudo ejecutar podman compose (ni nativo ni vía podman-compose)"
    return 1
}

run_compose() {
    if [ ${#COMPOSE_CMD[@]} -eq 0 ]; then
        resolve_compose_cmd || return 1
    fi
    "${COMPOSE_CMD[@]}" "$@"
}

# --- Verify podman connectivity, restart machine if SSH tunnel is stale ---
verify_podman_connection() {
    # Quick smoke test: can we actually talk to podman?
    if podman info --format '{{.Host.RemoteSocket.Path}}' &>/dev/null; then
        log_info "Conexión Podman verificada"
        return 0
    fi

    log_warn "Podman no responde (SSH tunnel roto). Reiniciando máquina..."
    podman machine stop 2>/dev/null || true
    sleep 3
    podman machine start
    if [ $? -ne 0 ]; then
        log_error "No se pudo reiniciar la máquina Podman"
        exit 1
    fi
    sleep 3

    if ! podman info --format '{{.Host.RemoteSocket.Path}}' &>/dev/null; then
        log_error "Podman sigue sin responder tras reinicio"
        exit 1
    fi
    log_info "Máquina Podman reiniciada y conectada"
}

# --- Verificar dependencias ---
check_deps() {
    if ! command -v podman &>/dev/null; then
        log_error "Podman no está instalado. Instálalo con: brew install podman"
        exit 1
    fi
    if ! podman machine inspect podman-machine-default &>/dev/null; then
        log_error "No hay máquina Podman creada. Ejecuta: podman machine init"
        exit 1
    fi
    if ! resolve_compose_cmd; then
        log_error "Instala/actualiza Podman y podman-compose (o habilita 'podman compose')"
        exit 1
    fi
}

# --- Asegurar que la máquina Podman está arrancada ---
ensure_machine() {
    if ! podman machine inspect podman-machine-default --format '{{.State}}' 2>/dev/null | grep -qi "running"; then
        log_warn "Máquina Podman detenida. Arrancando..."
        podman machine start
        if [ $? -ne 0 ]; then
            log_error "No se pudo arrancar la máquina Podman"
            exit 1
        fi
        log_info "Máquina Podman arrancada"
        sleep 3
    else
        log_info "Máquina Podman ya está corriendo"
    fi
    # Verify the connection actually works (fixes stale SSH tunnels)
    verify_podman_connection
    # Unset DOCKER_HOST — Podman forwards on /var/run/docker.sock automatically
    unset DOCKER_HOST 2>/dev/null || true
}

# --- Limpiar contenedores muertos/corruptos ---
cleanup_dead_containers() {
    local containers=("milvus-etcd" "milvus-minio" "milvus-standalone" "milvus-attu")
    for c in "${containers[@]}"; do
        local state
        state=$(podman inspect --format '{{.State.Status}}' "$c" 2>/dev/null)
        if [ $? -eq 0 ] && [ "$state" != "running" ]; then
            log_warn "Contenedor '$c' en estado '$state'. Eliminando..."
            podman rm -f "$c" 2>/dev/null || true
        fi
    done
}

cleanup_port_conflicts() {
    local unresolved=0
    local port

    # Remove podman containers already binding required host ports.
    while IFS='|' read -r cid cname cports; do
        [ -z "$cid" ] && continue
        for port in "${REQUIRED_PORTS[@]}"; do
            if echo "$cports" | grep -q ":${port}->"; then
                log_warn "Contenedor '$cname' ocupa puerto ${port}. Eliminando para evitar conflicto..."
                podman rm -f "$cid" >/dev/null 2>&1 || true
                break
            fi
        done
    done < <(podman ps --format '{{.ID}}|{{.Names}}|{{.Ports}}' 2>/dev/null)

    # If host processes still bind those ports, try a safe auto-cleanup.
    for port in "${REQUIRED_PORTS[@]}"; do
        local pids
        pids=$(lsof -nP -t -iTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
        [ -z "$pids" ] && continue

        while IFS= read -r pid; do
            [ -z "$pid" ] && continue
            local comm
            comm=$(ps -p "$pid" -o comm= 2>/dev/null | xargs)

            if echo "$comm" | grep -Eqi 'podman|gvproxy|docker|minio|milvus|attu'; then
                log_warn "Proceso '$comm' (PID $pid) ocupa puerto ${port}. Cerrando..."
                kill -TERM "$pid" 2>/dev/null || true
                sleep 1
                if kill -0 "$pid" 2>/dev/null; then
                    kill -KILL "$pid" 2>/dev/null || true
                fi
            else
                log_warn "Puerto ${port} en uso por proceso no gestionado ('$comm', PID $pid)"
                unresolved=1
            fi
        done <<< "$pids"
    done

    if [ "$unresolved" -ne 0 ]; then
        log_error "Hay puertos ocupados por procesos externos. Libéralos y reintenta."
        return 1
    fi

    return 0
}

# --- Verificar si Milvus ya está corriendo ---
is_milvus_running() {
    curl -sf "$HEALTH_URL" &>/dev/null
}

# --- Levantar los servicios ---
start_services() {
    log_info "Levantando Milvus con Podman Compose..."
    cd "$SCRIPT_DIR"
    cleanup_port_conflicts || exit 1
    run_compose -f "$COMPOSE_FILE" up -d 2>&1
    if [ $? -ne 0 ]; then
        log_error "Fallo al levantar los servicios. Intentando limpieza..."
        run_compose -f "$COMPOSE_FILE" down --remove-orphans 2>/dev/null || true
        cleanup_dead_containers
        cleanup_port_conflicts || exit 1
        log_info "Reintentando..."
        run_compose -f "$COMPOSE_FILE" up -d 2>&1
        if [ $? -ne 0 ]; then
            log_error "No se pudieron levantar los servicios"
            exit 1
        fi
    fi
}

# --- Esperar a que Milvus esté healthy ---
wait_for_healthy() {
    log_info "Esperando a que Milvus esté listo..."
    local attempt=0
    while [ $attempt -lt $MAX_RETRIES ]; do
        if is_milvus_running; then
            log_info "Milvus está healthy y listo"
            return 0
        fi
        attempt=$((attempt + 1))
        echo -n "."
        sleep $RETRY_INTERVAL
    done
    echo ""
    log_error "Milvus no respondió después de $((MAX_RETRIES * RETRY_INTERVAL)) segundos"
    log_warn "Revisando logs de Milvus..."
    podman logs milvus-standalone --tail 20 2>&1
    exit 1
}

# --- Mostrar estado final ---
show_status() {
    echo ""
    echo "============================================="
    log_info "Milvus desplegado correctamente"
    echo "============================================="
    echo ""
    podman ps --filter "label=io.podman.compose.project=milvus-deployment" \
        --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null \
    || podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "  Milvus API:    http://localhost:19530"
    echo "  Milvus Health: http://localhost:9091/healthz"
    echo "  MinIO Console: http://localhost:9001"
    echo "  Attu UI:       http://localhost:3000"
    echo ""
}

# --- Parar todo ---
stop_services() {
    log_info "Deteniendo Milvus..."
    cd "$SCRIPT_DIR"
    verify_podman_connection
    unset DOCKER_HOST 2>/dev/null || true
    run_compose -f "$COMPOSE_FILE" down 2>&1
    log_info "Milvus detenido"
}

# --- Main ---
case "${1:-start}" in
    start)
        check_deps
        ensure_machine
        if is_milvus_running; then
            log_info "Milvus ya está corriendo"
            show_status
            exit 0
        fi
        cleanup_dead_containers
        start_services
        wait_for_healthy
        show_status
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        sleep 3
        cleanup_dead_containers
        check_deps
        ensure_machine
        start_services
        wait_for_healthy
        show_status
        ;;
    status)
        check_deps
        ensure_machine
        if is_milvus_running; then
            log_info "Milvus está corriendo"
            show_status
        else
            log_warn "Milvus NO está corriendo"
            exit 1
        fi
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
