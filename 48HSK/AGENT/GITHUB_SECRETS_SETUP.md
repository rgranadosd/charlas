# 🔐 Configuración de GitHub Secrets

Este documento lista todos los secrets que debes configurar en GitHub para que el workflow los use automáticamente.

## 📋 Secrets a Configurar en GitHub

Ve a tu repositorio: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### Secrets Requeridos:

1. **WSO2_TOKEN_ENDPOINT**
   - Valor: `https://localhost:9453/oauth2/token`

2. **WSO2_CONSUMER_KEY**
   - Valor: `tu_consumer_key_aqui` (obtener del WSO2 Developer Portal)

3. **WSO2_CONSUMER_SECRET**
   - Valor: `tu_consumer_secret_aqui` (obtener del WSO2 Developer Portal)

4. **WSO2_GW_URL**
   - Valor: `https://localhost:8253`

5. **SHOPIFY_API_TOKEN**
   - Valor: `tu_shopify_token_aqui` (obtener de Shopify Admin → Apps → Develop apps)

### Secrets Opcionales:

6. **WSO2_USERNAME** (si usas Password Grant)
   - Valor: Tu usuario de WSO2

7. **WSO2_PASSWORD** (si usas Password Grant)
   - Valor: Tu contraseña de WSO2

8. **WSO2_CLIENT_ID** (si usas Password Grant)
   - Valor: Tu Client ID de WSO2 Identity Server

9. **WSO2_CLIENT_SECRET** (si usas Password Grant)
   - Valor: Tu Client Secret de WSO2 Identity Server

10. **OPENAI_API_KEY** (opcional, ya que se usa a través de WSO2)
    - Valor: Tu API key de OpenAI

## 🚀 Uso del Workflow

Una vez configurados los secrets:

1. El workflow `.github/workflows/setup-env.yml` se ejecutará automáticamente en cada push
2. O puedes ejecutarlo manualmente desde: **Actions** → **Setup Environment from Secrets** → **Run workflow**
3. El workflow creará/actualizará el archivo `AGENT/.env` con los valores de los secrets

## ⚠️ IMPORTANTE

- Los secrets están encriptados en GitHub
- Solo están disponibles en GitHub Actions workflows
- NO se pueden descargar localmente (por seguridad)
- Para uso local, configura el `.env` manualmente o usa variables de entorno del sistema

