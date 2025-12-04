#!/bin/bash

set -euo pipefail

APP_DIR="/Users/rafagranados/Develop/charlas/48HSK/AI GATEWAY/aigateway-demo"
PORT=8502

cd "$APP_DIR"

echo "[run_demo] Directorio: $(pwd)"

# Función para verificar si el APIM está activo
check_apim_status() {
    local token_url="${WSO2_TOKEN_URL}"
    local host="${WSO2_APIM_HOST}"
    local port="${WSO2_APIM_PORT}"
    
    # Si tenemos la URL completa, extraer host y puerto de ella
    if [[ -n "$token_url" ]] && [[ $token_url =~ https?://([^:/]+)(:([0-9]+))? ]]; then
        host="${BASH_REMATCH[1]}"
        port="${BASH_REMATCH[3]:-$port}"
    fi
    
    echo "[run_demo] Verificando estado del APIM en $host:$port..."
    
    # Verificar si el puerto está abierto
    if command -v nc >/dev/null 2>&1; then
        if nc -z -w 2 "$host" "$port" 2>/dev/null; then
            echo "[run_demo] ✓ Puerto $port está abierto en $host"
            return 0
        else
            echo "[run_demo] ✗ Puerto $port no está accesible en $host"
            return 1
        fi
    elif command -v timeout >/dev/null 2>&1; then
        # Alternativa usando timeout y bash TCP
        if timeout 2 bash -c "echo >/dev/tcp/$host/$port" 2>/dev/null; then
            echo "[run_demo] ✓ Puerto $port está abierto en $host"
            return 0
        else
            echo "[run_demo] ✗ Puerto $port no está accesible en $host"
            return 1
        fi
    else
        # Si no hay herramientas de red, intentar curl
        if curl -k -s --connect-timeout 2 "$token_url" >/dev/null 2>&1; then
            echo "[run_demo] ✓ APIM responde en $token_url"
            return 0
        else
            echo "[run_demo] ✗ APIM no responde en $token_url"
            return 1
        fi
    fi
}

# Cargar variables de entorno del .env si existe
if [ -f .env ]; then
    echo "[run_demo] Cargando configuración desde .env..."
    # shellcheck disable=SC1091
    set -a
    source .env
    set +a
fi

# Configurar variables de entorno del APIM (host y puerto)
# Si no están definidas, usar valores por defecto
export WSO2_APIM_HOST="${WSO2_APIM_HOST:-localhost}"
export WSO2_APIM_PORT="${WSO2_APIM_PORT:-9453}"

# Construir URL del token si no está definida explícitamente
if [ -z "${WSO2_TOKEN_URL:-}" ]; then
    export WSO2_TOKEN_URL="https://${WSO2_APIM_HOST}:${WSO2_APIM_PORT}/oauth2/token"
    echo "[run_demo] WSO2_TOKEN_URL construida desde variables de entorno: ${WSO2_TOKEN_URL}"
else
    echo "[run_demo] WSO2_TOKEN_URL definida explícitamente: ${WSO2_TOKEN_URL}"
fi

# Verificar estado del APIM
if ! check_apim_status; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  ⚠ ADVERTENCIA: WSO2 API Manager no está accesible"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "El APIM no responde en: ${WSO2_TOKEN_URL}"
    echo ""
    echo "Por favor, verifica que:"
    echo "  1. El WSO2 API Manager esté ejecutándose"
    echo "  2. Las variables WSO2_APIM_HOST y WSO2_APIM_PORT en .env sean correctas"
    echo "     (o WSO2_TOKEN_URL si está definida explícitamente)"
    echo "  3. No haya problemas de red o firewall"
    echo ""
    read -p "¿Deseas continuar de todos modos? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "[run_demo] Abortando. Por favor, inicia el APIM y vuelve a intentar."
        exit 1
    fi
    echo "[run_demo] Continuando sin verificación del APIM..."
else
    echo "[run_demo] ✓ APIM está activo y accesible"
fi

echo ""

# Configurar entorno virtual
echo "[run_demo] Verificando entorno virtual..."
if [ -d .venv ] && [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
    echo "[run_demo] ✓ Entorno virtual (.venv) encontrado y activado"
    echo "[run_demo]   Python: $(python --version 2>&1)"
    echo "[run_demo]   Ubicación: $(pwd)/.venv"
else
    echo "[run_demo] ⚠ Entorno virtual (.venv) no existe"
    echo "[run_demo] Creando entorno virtual..."
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        echo "[run_demo] ✓ Entorno virtual creado exitosamente"
        # shellcheck disable=SC1091
        source .venv/bin/activate
        echo "[run_demo] ✓ Entorno virtual activado"
        echo "[run_demo] Actualizando pip..."
        pip install --upgrade pip
        # Usar variable de entorno para compatibilidad con Python 3.14+ (tiktoken/PyO3)
        # No hace daño si no es necesario, pero evita errores con Python 3.14+
        echo "[run_demo] Instalando dependencias desde requirements.txt..."
        echo "[run_demo] (Esto puede tardar varios minutos la primera vez)..."
        PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 pip install -r requirements.txt || pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "[run_demo] ✓ Dependencias instaladas correctamente"
        else
            echo "[run_demo] ✗ Error al instalar dependencias"
            exit 1
        fi
    else
        echo "[run_demo] ✗ Error al crear el entorno virtual"
        exit 1
    fi
fi

# Liberar puerto si está ocupado
if lsof -i ":$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
    PIDS=$(lsof -i ":$PORT" -sTCP:LISTEN -t | tr '\n' ' ')
    echo "[run_demo] Puerto $PORT ocupado por $PIDS. Cerrando..."
    kill -9 $PIDS 2>/dev/null || true
    sleep 1
fi

echo "[run_demo] Lanzando Streamlit en puerto $PORT"
echo "[run_demo] Abre tu navegador en: http://localhost:$PORT"
echo ""
exec streamlit run demo_ui.py --server.port "$PORT"

