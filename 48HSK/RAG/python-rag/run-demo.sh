#!/bin/bash

# Navigate to the script's directory
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR" || exit

YELLOW='\033[38;5;226m'
RESET='\033[0m'

echo -e "${YELLOW}================================================================================${RESET}"
echo -e "${YELLOW}                        RAG DEMO - Interactive Demo${RESET}"
echo -e "${YELLOW}================================================================================${RESET}"
echo ""

# Activate the virtual environment
source ./venv/bin/activate

# Run the interactive demo script using the python from the virtual environment
./venv/bin/python demo_interactiva.py

# Deactivate the virtual environment
deactivate
