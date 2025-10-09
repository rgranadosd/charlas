#!/bin/bash
# Copyright 2025 Sample AI Agent Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ============================================
# SCRIPT DE PRUEBAS COMPLETO
# Sample AI Agent for WSO2 API Manager - Shopify Integration
# ============================================

set -e

echo "🚀 TEST COMPLETO WSO2-SHOPIFY"
echo "============================================"

# Verificar archivo .env en directorio actual
if [ ! -f ".env" ]; then
    echo "❌ Error: No se encuentra .env en $(pwd)"
    echo "   Ejecuta: cp env.example .env"
    exit 1
fi

echo "✅ Archivo .env encontrado en $(pwd)"

# Cargar variables
source .env

# Verificar variables críticas
if [ -z "$SHOPIFY_API_TOKEN" ]; then
    echo "❌ Error: Falta SHOPIFY_API_TOKEN en .env"
    exit 1
fi

echo "✅ Variables cargadas correctamente"

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: No se encuentra entorno virtual"
    exit 1
fi

source venv/bin/activate
echo "✅ Entorno virtual activado"

# Test Shopify
echo ""
echo "🛒 PROBANDO SHOPIFY"
echo "==================="

SHOPIFY_URL="https://rafa-ecommerce.myshopify.com/admin/api/2024-01/shop.json"
RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/shopify_response.json \
  -H "X-Shopify-Access-Token: $SHOPIFY_API_TOKEN" \
  "$SHOPIFY_URL")

if [ "$RESPONSE" == "200" ]; then
    SHOP_NAME=$(python3 -c "import json; print(json.load(open('/tmp/shopify_response.json'))['shop']['name'])" 2>/dev/null || echo "N/A")
    echo "✅ Shopify conectado: $SHOP_NAME"
    
    # Contar productos
    PRODUCTS=$(curl -s -H "X-Shopify-Access-Token: $SHOPIFY_API_TOKEN" \
      "https://rafa-ecommerce.myshopify.com/admin/api/2024-01/products/count.json" | \
      python3 -c "import sys,json; print(json.load(sys.stdin)['count'])" 2>/dev/null || echo "N/A")
    echo "   Productos: $PRODUCTS"
else
    echo "❌ Error Shopify: código $RESPONSE"
fi

# Test WSO2 (si está configurado)
if [ ! -z "$WSO2_TOKEN_ENDPOINT" ] && [ ! -z "$WSO2_CONSUMER_KEY" ]; then
    echo ""
    echo "🌐 PROBANDO WSO2"
    echo "==============="
    
    WSO2_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/wso2_token.json \
      -X POST "$WSO2_TOKEN_ENDPOINT" \
      -H "Authorization: Basic $(printf "%s:%s" "$WSO2_CONSUMER_KEY" "$WSO2_CONSUMER_SECRET" | base64)" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "grant_type=client_credentials" -k)
    
    if [ "$WSO2_RESPONSE" == "200" ]; then
        TOKEN=$(python3 -c "import json; print(json.load(open('/tmp/wso2_token.json'))['access_token'])" 2>/dev/null)
        echo "✅ WSO2 token obtenido: ${TOKEN:0:16}..."
    else
        echo "⚠️  WSO2 error: código $WSO2_RESPONSE"
    fi
else
    echo ""
    echo "⚠️  WSO2 no configurado completamente"
fi

# Test Python
echo ""
echo "🐍 VERIFICANDO PYTHON"
echo "===================="

if python3 -c "import semantic_kernel, requests, dotenv" 2>/dev/null; then
    echo "✅ Dependencias Python OK"
else
    echo "❌ Faltan dependencias Python"
fi

if [ -f "agent_gpt4.py" ]; then
    echo "✅ Script agent_gpt4.py encontrado"
else
    echo "❌ No se encuentra agent_gpt4.py"
fi

# Resumen
echo ""
echo "============================================"
echo "🎯 RESUMEN"
echo "============================================"
echo "Shopify: $([ "$RESPONSE" == "200" ] && echo "✅ OK" || echo "❌ Error")"
echo "WSO2: $([ "$WSO2_RESPONSE" == "200" ] && echo "✅ OK" || echo "⚠️  Verificar")"
echo ""
echo "🚀 Para iniciar: ./start_agent.sh"

# Limpiar archivos temporales
rm -f /tmp/shopify_response.json /tmp/wso2_token.json
