#!/bin/bash
# Configurar Moesif Analytics en WSO2 APIM

TOML_FILE="/Users/rafagranados/Develop/wso2/wso2am-4.6.0/repository/conf/deployment.toml"

echo "📊 Configurando Moesif Analytics en WSO2 APIM"
echo ""

# Verificar si ya existe configuración de Moesif
if grep -q "\[apim.analytics\]" "$TOML_FILE"; then
    echo "✓ Sección [apim.analytics] encontrada"
    
    # Activar analytics
    sed -i.backup_moesif 's/enable = false/enable = true/' "$TOML_FILE"
    sed -i.backup_moesif2 's/type = "choreo"/type = "moesif"/' "$TOML_FILE"
    
    echo "✓ Analytics habilitado con Moesif"
else
    echo "⚠️  No se encontró sección [apim.analytics]"
fi

echo ""
echo "📋 Configuración actual:"
grep -A 3 "\[apim.analytics\]" "$TOML_FILE" 2>/dev/null || echo "No se pudo leer la configuración"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 IMPORTANTE: Moesif requiere un Application Token"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Crear cuenta gratis en: https://www.moesif.com/"
echo "2. Obtener tu Application Token"
echo "3. Agregarlo en deployment.toml:"
echo ""
echo "   [apim.analytics]"
echo "   enable = true"
echo "   type = \"moesif\""
echo "   properties.application_id = \"TU_TOKEN_AQUI\""
echo ""
echo "4. Reiniciar APIM"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔄 Para aplicar cambios:"
echo "   /Users/rafagranados/Develop/wso2/wso2am-4.6.0/bin/api-manager.sh restart"
