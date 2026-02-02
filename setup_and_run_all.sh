#!/bin/bash
# setup_and_run_all.sh
# Este script automatiza todo el flujo: crea entorno virtual, instala dependencias, genera config para Inspector y ejecuta el servidor MCP.

set -e

cd "$(dirname "$0")/WEATHER"

# Crear entorno virtual si no existe
echo "[1/5] Comprobando entorno virtual..."
if [ ! -d "venv" ]; then
    echo "No se encontró venv. Creando..."
    python3 -m venv venv
    echo "Entorno virtual creado."
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias si hay requirements.txt
echo "[2/5] Instalando dependencias (si existen)..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "No se encontró requirements.txt. Se asume que las dependencias ya están instaladas."
fi

# Instalar mcp si no está
python3 -c "import mcp" 2>/dev/null || {
    echo "[3/5] Instalando paquete mcp..."
    pip install mcp
}

# Generar archivo de configuración para Inspector MCP
echo "[4/5] Generando archivo inspector_config.json..."
cat > inspector_config.json <<EOL
{
  "command": "python3 weather_mcp_openmeteo.py",
  "workingDirectory": "$(pwd)",
  "env": {},
  "proxySessionToken": "",
  "args": [],
  "name": "Weather MCP Local"
}
EOL

# Ejecutar el servidor MCP
echo "[5/5] Ejecutando weather_mcp_openmeteo.py..."
python3 weather_mcp_openmeteo.py
