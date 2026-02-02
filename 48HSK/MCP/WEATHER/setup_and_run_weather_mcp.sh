#!/bin/bash
# setup_and_run_weather_mcp.sh
# Este script activa el entorno virtual, instala dependencias si es necesario y ejecuta el servidor MCP de weather.

set -e

cd "$(dirname "$0")"

# Crear y/o activar entorno virtual
if [ ! -d "venv" ]; then
    echo "No se encontró el entorno virtual (venv). Creando..."
    python3 -m venv venv
    echo "Entorno virtual creado."
fi
source venv/bin/activate

# Generar archivo de configuración para Inspector MCP (para usar con --config/--server)
# Usamos el Python del venv para evitar el error: spawn python ENOENT
cat > inspector_config.json <<EOL
{
    "mcpServers": {
        "weather": {
            "command": "./venv/bin/python",
            "args": ["weather_mcp_openmeteo.py"],
            "env": {}
        }
    }
}
EOL
echo "Archivo inspector_config.json generado para el Inspector MCP (usa ./venv/bin/python)."

# Instalar dependencias si hay requirements.txt
if [ -f requirements.txt ]; then
    echo "Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "No se encontró requirements.txt. Se asume que las dependencias ya están instaladas."
fi

# Verificar que el paquete mcp está instalado
python3 -c "import mcp" 2>/dev/null || {
    echo "[ERROR] El paquete 'mcp' no está instalado en este entorno. Instálalo con: pip install mcp"
    exit 1
}

kill_port_if_listening() {
    local port="$1"
    if lsof -i :"$port" -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "El puerto $port está ocupado. Matando proceso anterior..."
        lsof -i :"$port" -sTCP:LISTEN -t | xargs kill -9
        sleep 1
    fi
}

# Evitar conflictos de puertos del Inspector (UI / proxy pueden variar según versión)
kill_port_if_listening 6274
kill_port_if_listening 6277


# Lanzar Inspector MCP en segundo plano usando config+server
echo "Lanzando Inspector MCP (npx @modelcontextprotocol/inspector) en segundo plano..."
INSPECTOR_LOG="inspector.log"
rm -f "$INSPECTOR_LOG"

DANGEROUSLY_OMIT_AUTH=true npx @modelcontextprotocol/inspector --config inspector_config.json --server weather 2>&1 | tee "$INSPECTOR_LOG" &
INSPECTOR_PID=$!

# Esperar a que el Inspector publique la URL y abrirla
echo "Esperando a que el Inspector publique la URL..."
INSPECTOR_URL=""
for _ in $(seq 1 40); do
    # Preferir la URL con token (la UI del Inspector exige el token para evitar "Connection Error - proxy session token")
    INSPECTOR_URL=$(grep -Eo 'http://(localhost|127\.0\.0\.1):[0-9]+/\?MCP_PROXY_AUTH_TOKEN=[0-9a-f]+' "$INSPECTOR_LOG" | head -n 1 || true)
    if [ -z "$INSPECTOR_URL" ]; then
        INSPECTOR_URL=$(grep -Eo 'http://(localhost|127\.0\.0\.1):[0-9]+' "$INSPECTOR_LOG" | head -n 1 || true)
    fi
    if [ -n "$INSPECTOR_URL" ]; then
        break
    fi
    sleep 0.5
done

if [ -n "$INSPECTOR_URL" ]; then
    echo "Abriendo la interfaz web del Inspector: $INSPECTOR_URL"
    open "$INSPECTOR_URL"
else
    echo "[WARN] No se detectó la URL del Inspector en $INSPECTOR_LOG."
    echo "Revisa el log: $(pwd)/$INSPECTOR_LOG"
fi

echo "Inspector lanzado. Para detenerlo: kill $INSPECTOR_PID"
