#!/bin/bash

# Script para verificar el estado del OBS MCP Bridge
# Verifica si el bridge está corriendo y si el MCP está operativo

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores de estado
BRIDGE_OK=0
MCP_OK=0
TOTAL_CHECKS=0

echo -e "${BLUE}🔍 Verificando estado del OBS MCP Bridge...${NC}\n"

# 1. Verificar si el bridge está corriendo (puerto 8888)
echo -e "${BLUE}1. Verificando bridge.py (puerto 8888)...${NC}"
if lsof -Pi :8888 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "   ${GREEN}✅ Bridge está corriendo en el puerto 8888${NC}"
    BRIDGE_OK=1
else
    echo -e "   ${RED}❌ Bridge NO está corriendo en el puerto 8888${NC}"
    echo -e "   ${YELLOW}   💡 Ejecuta: python bridge.py${NC}"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# 2. Verificar si hay un proceso bridge.py corriendo
echo -e "\n${BLUE}2. Verificando proceso bridge.py...${NC}"
if pgrep -f "bridge.py" > /dev/null; then
    PID=$(pgrep -f "bridge.py" | head -1)
    echo -e "   ${GREEN}✅ Proceso bridge.py encontrado (PID: $PID)${NC}"
    BRIDGE_OK=1
else
    echo -e "   ${RED}❌ No se encontró proceso bridge.py${NC}"
    echo -e "   ${YELLOW}   💡 Ejecuta: python bridge.py${NC}"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# 3. Probar conexión HTTP al bridge
echo -e "\n${BLUE}3. Probando conexión HTTP al bridge...${NC}"
if command -v curl >/dev/null 2>&1; then
    HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/openapi.json 2>/dev/null)
    if [ "$HTTP_RESPONSE" = "200" ]; then
        echo -e "   ${GREEN}✅ Bridge responde correctamente (HTTP $HTTP_RESPONSE)${NC}"
        BRIDGE_OK=1
    else
        echo -e "   ${RED}❌ Bridge no responde correctamente (HTTP $HTTP_RESPONSE)${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠️  curl no está disponible, saltando prueba HTTP${NC}"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# 4. Verificar que el archivo bridge.py existe
echo -e "\n${BLUE}4. Verificando archivo bridge.py...${NC}"
if [ -f "bridge.py" ]; then
    echo -e "   ${GREEN}✅ bridge.py existe${NC}"
    if [ -r "bridge.py" ]; then
        echo -e "   ${GREEN}✅ bridge.py es legible${NC}"
    else
        echo -e "   ${RED}❌ bridge.py no es legible${NC}"
    fi
else
    echo -e "   ${RED}❌ bridge.py no existe${NC}"
fi

# 5. Verificar que el archivo obs-mcp.js existe
echo -e "\n${BLUE}5. Verificando archivo obs-mcp.js...${NC}"
if [ -f "obs-mcp.js" ]; then
    echo -e "   ${GREEN}✅ obs-mcp.js existe${NC}"
    if [ -x "obs-mcp.js" ] || [ -r "obs-mcp.js" ]; then
        echo -e "   ${GREEN}✅ obs-mcp.js es ejecutable/legible${NC}"
        MCP_OK=1
    else
        echo -e "   ${RED}❌ obs-mcp.js no es ejecutable${NC}"
    fi
else
    echo -e "   ${RED}❌ obs-mcp.js no existe${NC}"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# 6. Verificar dependencias de Node.js
echo -e "\n${BLUE}6. Verificando dependencias de Node.js...${NC}"
if [ -d "node_modules" ]; then
    echo -e "   ${GREEN}✅ node_modules existe${NC}"
    if [ -f "node_modules/@modelcontextprotocol/sdk/package.json" ]; then
        echo -e "   ${GREEN}✅ MCP SDK instalado${NC}"
        MCP_OK=1
    else
        echo -e "   ${YELLOW}⚠️  MCP SDK no encontrado${NC}"
        echo -e "   ${YELLOW}   💡 Ejecuta: npm install${NC}"
    fi
else
    echo -e "   ${RED}❌ node_modules no existe${NC}"
    echo -e "   ${YELLOW}   💡 Ejecuta: npm install${NC}"
fi

# 7. Verificar archivo .env (opcional pero recomendado)
echo -e "\n${BLUE}7. Verificando configuración .env...${NC}"
if [ -f ".env" ]; then
    echo -e "   ${GREEN}✅ Archivo .env existe${NC}"
    if grep -q "OBS_PASS" .env 2>/dev/null; then
        echo -e "   ${GREEN}✅ OBS_PASS configurado${NC}"
    else
        echo -e "   ${YELLOW}⚠️  OBS_PASS no encontrado en .env${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠️  Archivo .env no existe (opcional)${NC}"
    echo -e "   ${YELLOW}   💡 Puedes crear uno basado en env.example${NC}"
fi

# Resumen final
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Verificar si el bridge está realmente operativo (puerto + proceso + HTTP)
BRIDGE_OPERATIVE=0
if lsof -Pi :8888 -sTCP:LISTEN -t >/dev/null 2>&1 && pgrep -f "bridge.py" > /dev/null; then
    if command -v curl >/dev/null 2>&1; then
        HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/openapi.json 2>/dev/null)
        if [ "$HTTP_RESPONSE" = "200" ]; then
            BRIDGE_OPERATIVE=1
        fi
    else
        # Si no hay curl, asumimos que está bien si el puerto y proceso están activos
        BRIDGE_OPERATIVE=1
    fi
fi

# Verificar si el MCP está listo (archivo existe y dependencias instaladas)
MCP_READY=0
if [ -f "obs-mcp.js" ] && [ -d "node_modules" ] && [ -f "node_modules/@modelcontextprotocol/sdk/package.json" ]; then
    MCP_READY=1
fi

if [ $BRIDGE_OPERATIVE -eq 1 ] && [ $MCP_READY -eq 1 ]; then
    echo -e "${GREEN}✅ SISTEMA OPERATIVO${NC}"
    echo -e "${GREEN}   El bridge y el MCP están listos para usar${NC}"
    echo -e "${GREEN}   - Bridge corriendo en http://localhost:8888${NC}"
    echo -e "${GREEN}   - MCP server listo (obs-mcp.js)${NC}"
    exit 0
else
    echo -e "${RED}❌ SISTEMA NO OPERATIVO${NC}"
    if [ $BRIDGE_OPERATIVE -eq 0 ]; then
        echo -e "${RED}   - Bridge no está corriendo o no responde${NC}"
        echo -e "${YELLOW}     Solución: python bridge.py${NC}"
    fi
    if [ $MCP_READY -eq 0 ]; then
        echo -e "${RED}   - MCP no está configurado correctamente${NC}"
        if [ ! -f "obs-mcp.js" ]; then
            echo -e "${YELLOW}     - Falta: obs-mcp.js${NC}"
        fi
        if [ ! -d "node_modules" ] || [ ! -f "node_modules/@modelcontextprotocol/sdk/package.json" ]; then
            echo -e "${YELLOW}     - Solución: npm install${NC}"
        fi
    fi
    exit 1
fi

