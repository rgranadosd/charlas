#!/bin/bash
# run_weather_mcp.sh

set -e
cd "$(dirname "$0")"

# 1. Configuración de Entorno
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi
source venv/bin/activate

ensure_python_pip() {
    if python3 -m pip --version >/dev/null 2>&1; then
        return 0
    fi

    echo "🛠️  pip no está disponible. Intentando bootstrap con ensurepip..."
    python3 -m ensurepip --upgrade >/dev/null 2>&1 || true

    if ! python3 -m pip --version >/dev/null 2>&1; then
        echo "❌ No se pudo inicializar pip en el entorno virtual"
        exit 1
    fi
}

ensure_python_pip

# 2. Instalación de dependencias
echo "📥 Instalando dependencias..."
python3 -m pip install "mcp[cli]" uvicorn fastapi httpx

# 3. Modos de Ejecución
MODE="${1:-serve}" # Por defecto 'serve' si no se pasa argumento

if [ "$MODE" == "inspect" ]; then
    # --- MODO INSPECTOR (Visual para Debug) ---
    echo "🕵️  Lanzando MCP Inspector (Modo STDIO)..."
    
    # Generar config temporal solo para el inspector
    cat > inspector_config.json <<EOL
{
    "mcpServers": {
        "weather": {
            "command": "$(pwd)/venv/bin/python",
            "args": ["$(pwd)/weather_mcp_openmeteo.py", "--stdio"],
            "env": { "PYTHONUNBUFFERED": "1" }
        }
    }
}
EOL
    # Lanzar inspector oficial
    npx @modelcontextprotocol/inspector --config inspector_config.json

elif [ "$MODE" == "serve" ]; then
    # --- MODO SERVIDOR (Para WSO2) ---
    echo "🚀 Lanzando Servidor MCP HTTP Stream (Para WSO2)..."
    echo "📡 URL para WSO2: http://localhost:8080/mcp"
    
    if lsof -i :8080 > /dev/null 2>&1; then
        echo "⚠️  El puerto 8080 está en uso. Matando el proceso..."
        lsof -ti :8080 | xargs kill -9
        sleep 2  # Esperar para asegurarse de que el puerto se libera
        if lsof -i :8080 > /dev/null 2>&1; then
            echo "❌ No se pudo liberar el puerto 8080. Por favor, verifica manualmente."
            exit 1
        fi
        echo "✅ Puerto 8080 liberado."
    fi

    # Lanzar el servidor MCP con uvicorn (soporta HTTP Streaming)
    python3 -m uvicorn weather_mcp_openmeteo:asgi_app --host 0.0.0.0 --port 8080 --log-level info

else
    echo "❌ Modo desconocido. Usa: ./run_weather_mcp.sh [inspect|serve]"
    exit 1
fi
