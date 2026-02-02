#!/bin/bash

# Script de Setup y Testing para Weather MCP (Open-Meteo)
# Automatiza: venv creation + deps install + testing

set -e  # Exit on error

VENV_DIR="venv"
PYTHON_CMD="python3"
TEST_SCRIPT="test_weather_mcp.py"
MCP_SCRIPT="weather_mcp_openmeteo.py"

echo "🚀 Weather MCP - Setup & Test Automation"
echo "========================================"
echo ""

# Check Python
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python3 no encontrado. Instálalo primero."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "✅ $PYTHON_VERSION detectado"
echo ""

# Create venv if doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creando virtualenv..."
    $PYTHON_CMD -m venv $VENV_DIR
    echo "✅ Virtualenv creado"
else
    echo "✅ Virtualenv ya existe"
fi
echo ""

# Activate venv
echo "🔌 Activando virtualenv..."
source $VENV_DIR/bin/activate

# Upgrade pip
echo "📦 Actualizando pip..."
pip install --upgrade pip -q

# Install dependencies
echo "📦 Instalando dependencias..."
pip install mcp httpx pydantic -q
echo "✅ Dependencias instaladas"
echo ""

# Run tests
echo "🧪 Ejecutando tests..."
echo "========================================"
echo ""

if [ -f "$TEST_SCRIPT" ]; then
    python $TEST_SCRIPT
    TEST_RESULT=$?
else
    echo "❌ No se encuentra $TEST_SCRIPT"
    exit 1
fi

echo ""
echo "========================================"

if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ Setup completo - Todo listo para usar"
    echo ""
    echo "💡 Para probar el MCP ahora:"
    echo "   npx @modelcontextprotocol/inspector python $MCP_SCRIPT"
    echo ""
    echo "💡 Para activar el venv manualmente:"
    echo "   source venv/bin/activate"
else
    echo "❌ Tests fallaron - revisa errores arriba"
    exit 1
fi
