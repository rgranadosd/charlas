#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO_DIR="$SCRIPT_DIR/aigateway-demo"
PORT="${STREAMLIT_PORT:-8502}"

# Buscar un Python funcional
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3.10 /usr/bin/python3 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" --version >/dev/null 2>&1; then
    PYTHON="$candidate"
    break
  fi
done
if [ -z "$PYTHON" ]; then
  echo "No se encontro un Python funcional. Instala Python 3.10+ y vuelve a intentar."
  exit 1
fi
echo "Usando: $PYTHON ($($PYTHON --version 2>&1))"

if [ ! -d "$DEMO_DIR" ]; then
  echo "No se encontro la carpeta: $DEMO_DIR"
  exit 1
fi

cd "$DEMO_DIR"

if [ ! -f ".venv/bin/activate" ]; then
  echo "Creando entorno virtual en .venv ..."
  "$PYTHON" -m venv .venv
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
  echo "Instalando dependencias ..."
  pip install --upgrade pip -q
  pip install -r requirements.txt -q
else
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi
echo "Entorno virtual activado: .venv"

if lsof -i ":$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "El puerto $PORT ya esta en uso. Cierra ese proceso o usa otro puerto, por ejemplo:"
  echo "STREAMLIT_PORT=8503 ./Run_Demo.sh"
  exit 1
fi

echo "Levantando frontend en http://localhost:$PORT"
streamlit run demo_ui.py --server.port "$PORT"
