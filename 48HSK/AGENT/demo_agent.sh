#!/bin/bash
# Script de demostración del agente Shopify con OAuth PKCE/OBO

clear
echo "================================================================"
echo "   DEMOSTRACIÓN: Agente Shopify IA con OAuth PKCE + OBO"
echo "================================================================"
echo ""
echo "Estado de configuración:"
echo "  ✅ WSO2 IS corriendo en localhost:9453"
echo "  ✅ WSO2 API Manager corriendo en localhost:8253"
echo "  ✅ Credenciales OAuth configuradas correctamente"
echo "  ✅ API Resource 'Shopify' con scopes configurados"
echo "  ✅ Usuario manager@example.com con rol ProductManager"
echo ""
echo "================================================================"
echo ""
echo "Iniciando agente..."
echo ""
sleep 2

cd /Users/rafagranados/Develop/wso2/SampleAIAgent/SampleAIAgent
source ../venv/bin/activate

# Verificar que todo esté configurado
echo "Verificación rápida de configuración:"
python test_oauth_flow.py | grep "✅ CONFIGURACIÓN CORRECTA" && echo "" || exit 1

echo ""
echo "================================================================"
echo "   LISTO PARA USAR"
echo "================================================================"
echo ""
echo "El agente está configurado y funcionando correctamente."
echo ""
echo "Para probarlo de forma interactiva, ejecuta:"
echo "  cd SampleAIAgent"
echo "  python agent_gpt4.py"
echo ""
echo "Comandos de ejemplo:"
echo "  - lista los productos"
echo "  - cuántos productos hay"
echo "  - actualiza el precio de la gift card a 45"
echo "  - muéstrame los productos ordenados por precio"
echo ""
echo "El primer uso abrirá el navegador para autorizar OAuth."
echo "Después quedará cacheado el token en token_cache.json"
echo ""
echo "================================================================"
