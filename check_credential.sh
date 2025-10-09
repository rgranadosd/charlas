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
# SCRIPT PARA VERIFICAR CREDENCIALES WSO2
# ============================================

set -e

echo "🔐 VERIFICANDO CREDENCIALES WSO2"
echo "================================="

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "❌ Error: No se encuentra .env"
    echo "   Ejecuta: cp env.example .env"
    exit 1
fi

echo "✅ Archivo .env encontrado"

# Cargar variables
source .env

# Verificar variables WSO2
if [ -z "$WSO2_TOKEN_ENDPOINT" ]; then
    echo "❌ Error: WSO2_TOKEN_ENDPOINT no configurado"
    exit 1
fi

if [ -z "$WSO2_CONSUMER_KEY" ]; then
    echo "❌ Error: WSO2_CONSUMER_KEY no configurado"
    exit 1
fi

if [ -z "$WSO2_CONSUMER_SECRET" ]; then
    echo "❌ Error: WSO2_CONSUMER_SECRET no configurado"
    exit 1
fi

echo "✅ Variables WSO2 configuradas"

# Probar endpoint de token
echo ""
echo "🌐 PROBANDO ENDPOINT WSO2"
echo "========================="

echo "Endpoint: $WSO2_TOKEN_ENDPOINT"
echo "Consumer Key: ${WSO2_CONSUMER_KEY:0:8}..."
echo "Consumer Secret: ${WSO2_CONSUMER_SECRET:0:8}..."

# Hacer petición de token
RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/wso2_response.json \
  -X POST "$WSO2_TOKEN_ENDPOINT" \
  -H "Authorization: Basic $(printf "%s:%s" "$WSO2_CONSUMER_KEY" "$WSO2_CONSUMER_SECRET" | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" -k)

echo "Respuesta HTTP: $RESPONSE"

if [ "$RESPONSE" == "200" ]; then
    echo "✅ Token obtenido exitosamente"
    TOKEN=$(python3 -c "import json; print(json.load(open('/tmp/wso2_response.json'))['access_token'])" 2>/dev/null)
    echo "Token: ${TOKEN:0:16}..."
    echo "✅ Credenciales WSO2 válidas"
else
    echo "❌ Error obteniendo token"
    echo "Respuesta del servidor:"
    cat /tmp/wso2_response.json 2>/dev/null || echo "No hay respuesta"
fi

# Limpiar archivos temporales
rm -f /tmp/wso2_response.json

echo ""
echo "================================="
echo "Verificación completada"
