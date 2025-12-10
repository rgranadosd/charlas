#!/bin/bash

# ============================================
# SCRIPT PARA CREAR ARCHIVOS .env
# ============================================
# Este script crea los archivos .env necesarios
# basándose en los archivos env.example

set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  CREAR ARCHIVOS .env${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Función para crear .env desde template
crear_env() {
    local dir=$1
    local template=$2
    local nombre=$3
    
    if [ -f "$dir/$template" ]; then
        if [ ! -f "$dir/.env" ]; then
            cp "$dir/$template" "$dir/.env"
            echo -e "${GREEN}✓${NC} Creado: $nombre/.env"
            echo -e "${YELLOW}  → Edita $dir/.env con tus valores reales${NC}"
        else
            echo -e "${YELLOW}⚠${NC} Ya existe: $nombre/.env (no se sobrescribió)"
        fi
    else
        echo -e "${YELLOW}⚠${NC} Template no encontrado: $dir/$template"
    fi
}

# 1. AGENT/.env
echo -e "${BLUE}1. Creando AGENT/.env...${NC}"
crear_env "AGENT" "env.example" "AGENT"
echo ""

# 2. RAG/python-rag/.env
echo -e "${BLUE}2. Creando RAG/python-rag/.env...${NC}"
if [ ! -f "RAG/python-rag/.env" ]; then
    cat > "RAG/python-rag/.env" << 'EOF'
# Groq Token (requerido)
GROQ-TOKEN=your_groq_token_here

# OpenAI API Key (opcional)
OPENAI_API_KEY=your_openai_key_here
EOF
    echo -e "${GREEN}✓${NC} Creado: RAG/python-rag/.env"
    echo -e "${YELLOW}  → Edita RAG/python-rag/.env con tus valores reales${NC}"
else
    echo -e "${YELLOW}⚠${NC} Ya existe: RAG/python-rag/.env (no se sobrescribió)"
fi
echo ""

# 3. MCP/.env
echo -e "${BLUE}3. Creando MCP/.env...${NC}"
crear_env "MCP" "env.example" "MCP"
echo ""

# 4. AI GATEWAY/aigateway-demo/.env
echo -e "${BLUE}4. Creando AI GATEWAY/aigateway-demo/.env...${NC}"
crear_env "AI GATEWAY/aigateway-demo" ".env.example" "AI GATEWAY/aigateway-demo"
echo ""

echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✓ Proceso completado${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "${YELLOW}IMPORTANTE:${NC}"
echo -e "${YELLOW}1. Edita cada archivo .env con tus valores reales${NC}"
echo -e "${YELLOW}2. Nunca compartas tus claves API${NC}"
echo -e "${YELLOW}3. Los archivos .env están en .gitignore${NC}"
echo ""
echo -e "${BLUE}Para más información, consulta: CONFIGURAR_ENV.md${NC}"

