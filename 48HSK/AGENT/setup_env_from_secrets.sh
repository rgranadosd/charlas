#!/bin/bash
# Script para configurar .env desde variables de entorno del sistema
# Útil cuando las credenciales están en GitHub Secrets (para CI/CD) o variables de entorno del sistema

set -e

ENV_FILE=".env"

echo "============================================"
echo "  CONFIGURANDO .env DESDE VARIABLES DE ENTORNO"
echo "============================================"

# Crear .env desde env.example si no existe
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "env.example" ]; then
        cp env.example "$ENV_FILE"
        echo "✓ Archivo .env creado desde env.example"
    else
        echo "✗ Error: No se encontró env.example"
        exit 1
    fi
fi

# Función para actualizar variable en .env
update_env_var() {
    local var_name=$1
    local var_value=$2
    
    if [ -n "$var_value" ]; then
        # Si la variable existe, actualizarla; si no, agregarla
        if grep -q "^${var_name}=" "$ENV_FILE"; then
            # macOS usa sed -i '', Linux usa sed -i
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s|^${var_name}=.*|${var_name}=${var_value}|" "$ENV_FILE"
            else
                sed -i "s|^${var_name}=.*|${var_name}=${var_value}|" "$ENV_FILE"
            fi
            echo "✓ ${var_name} actualizado desde variable de entorno"
        else
            echo "${var_name}=${var_value}" >> "$ENV_FILE"
            echo "✓ ${var_name} agregado desde variable de entorno"
        fi
    else
        echo "⚠ ${var_name} no está definida en variables de entorno"
    fi
}

# WSO2 Configuration
update_env_var "WSO2_TOKEN_ENDPOINT" "$WSO2_TOKEN_ENDPOINT"
update_env_var "WSO2_CONSUMER_KEY" "$WSO2_CONSUMER_KEY"
update_env_var "WSO2_CONSUMER_SECRET" "$WSO2_CONSUMER_SECRET"
update_env_var "WSO2_GW_URL" "$WSO2_GW_URL"

# WSO2 Identity Server (opcional)
update_env_var "WSO2_USERNAME" "$WSO2_USERNAME"
update_env_var "WSO2_PASSWORD" "$WSO2_PASSWORD"
update_env_var "WSO2_CLIENT_ID" "$WSO2_CLIENT_ID"
update_env_var "WSO2_CLIENT_SECRET" "$WSO2_CLIENT_SECRET"
update_env_var "WSO2_IS_TOKEN_ENDPOINT" "$WSO2_IS_TOKEN_ENDPOINT"

# Shopify
update_env_var "SHOPIFY_API_TOKEN" "$SHOPIFY_API_TOKEN"

# OpenAI (opcional, ya que se usa a través de WSO2)
update_env_var "OPENAI_API_KEY" "$OPENAI_API_KEY"

echo ""
echo "============================================"
echo "  CONFIGURACIÓN COMPLETADA"
echo "============================================"
echo "Archivo .env actualizado en: $(pwd)/${ENV_FILE}"
echo ""
echo "Para usar este script con GitHub Secrets en CI/CD:"
echo "  - Configura los secrets en GitHub: Settings > Secrets and variables > Actions"
echo "  - En tu workflow, usa: env: \${{ secrets.SECRET_NAME }}"
echo "  - Luego ejecuta este script antes de ejecutar el agente"
echo ""

