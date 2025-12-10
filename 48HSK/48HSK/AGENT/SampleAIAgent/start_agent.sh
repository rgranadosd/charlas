#!/bin/bash

# ============================================
# SCRIPT PARA INICIAR EL AGENTE PYTHON IA x WSO2
# ============================================
# Este script activa el entorno virtual y ejecuta el agente

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  STARTING PYTHON AI AGENT x WSO2${NC}"
echo -e "${BLUE}============================================${NC}"

# Verificar que estamos en el directorio correcto
if [ ! -f "agent_gpt4.py" ]; then
    echo -e "${RED}ERROR: agent_gpt4.py not found${NC}"
    echo -e "${YELLOW}Make sure to run this script from the project directory${NC}"
    exit 1
fi

# Verificar o crear el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}No se encontró el entorno virtual 'venv'${NC}"
    echo -e "${BLUE}Creando entorno virtual...${NC}"
    
    # Verificar que Python está disponible
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}ERROR: python3 no está instalado o no está en el PATH${NC}"
        exit 1
    fi
    
    # Crear el entorno virtual
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo crear el entorno virtual${NC}"
        echo -e "${YELLOW}Asegúrate de que python3-venv está instalado:${NC}"
        echo -e "${BLUE}  macOS: python3 viene con venv incluido${NC}"
        echo -e "${BLUE}  Linux: sudo apt-get install python3-venv${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Entorno virtual creado exitosamente${NC}"
fi

# Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}ADVERTENCIA: No se encontró el archivo .env${NC}"
    echo -e "${YELLOW}Copia env.example a .env y configura tus credenciales:${NC}"
    echo -e "${BLUE}  cp env.example .env${NC}"
    echo -e "${BLUE}  nano .env${NC}"
    echo ""
    read -p "¿Quieres continuar de todas formas? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Ejecución cancelada${NC}"
        exit 1
    fi
fi

# Activar el entorno virtual
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Esperar un momento para que se active completamente
sleep 1

# Verificar que el entorno virtual está activo
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}ERROR: El entorno virtual no se activó correctamente${NC}"
    exit 1
fi

# Verificar que Python está disponible en el entorno virtual
PYTHON_PATH=$(which python3)
if [[ "$PYTHON_PATH" != *"venv"* ]]; then
    echo -e "${RED}ERROR: Python3 no está usando el entorno virtual${NC}"
    echo -e "${YELLOW}Python encontrado en: $PYTHON_PATH${NC}"
    echo -e "${YELLOW}Debería estar en: $(pwd)/venv/bin/python3${NC}"
    exit 1
fi

# Verificar que pip también está usando el entorno virtual
PIP_PATH=$(which pip3)
if [[ "$PIP_PATH" != *"venv"* ]]; then
    echo -e "${YELLOW}ADVERTENCIA: pip3 no está usando el entorno virtual${NC}"
    echo -e "${YELLOW}pip3 encontrado en: $PIP_PATH${NC}"
fi

# Verificar que las dependencias están instaladas
echo -e "${BLUE}Checking dependencies...${NC}"

# Verificar que requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}ADVERTENCIA: requirements.txt no encontrado${NC}"
    echo -e "${YELLOW}Algunas dependencias pueden faltar${NC}"
else
    # Verificar dependencias críticas
    if ! python3 -c "import semantic_kernel, requests, dotenv" 2>/dev/null; then
        echo -e "${YELLOW}Algunas dependencias faltan. Instalando desde requirements.txt...${NC}"
        pip3 install --upgrade pip
        pip3 install -r requirements.txt
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}ERROR: No se pudieron instalar las dependencias${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}✓ Dependencias instaladas${NC}"
    fi
fi

# Mostrar información del entorno
echo -e "${GREEN}✓ Virtual environment activated successfully${NC}"
echo -e "${GREEN}✓ Dependencies verified${NC}"
echo -e "${BLUE}Virtual environment: $VIRTUAL_ENV${NC}"
echo -e "${BLUE}Python version: $(python3 --version)${NC}"
echo -e "${BLUE}Python path: $(which python3)${NC}"
echo -e "${BLUE}Working directory: $(pwd)${NC}"
echo ""

# Ejecutar el agente
echo -e "${GREEN}Starting agent...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the agent${NC}"
echo ""

# Ejecutar el script Python y pasar todos los argumentos
python3 agent_gpt4.py "$@"

# Si llegamos aquí, el script terminó
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  AGENT FINISHED${NC}"
echo -e "${BLUE}============================================${NC}"
