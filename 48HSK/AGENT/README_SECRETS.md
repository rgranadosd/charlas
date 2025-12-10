# 🔐 Configuración de Credenciales desde GitHub Secrets

Este documento explica cómo configurar las credenciales usando GitHub Secrets para uso en CI/CD.

## ⚠️ IMPORTANTE

**GitHub Secrets NO se pueden descargar automáticamente a archivos `.env` locales.** Los Secrets solo están disponibles en:
- GitHub Actions workflows
- GitHub Codespaces (con configuración especial)
- No están disponibles para descarga directa a archivos locales

## 📋 Para Uso Local

Si quieres usar las credenciales localmente, debes configurarlas manualmente en `AGENT/.env` o usar variables de entorno del sistema.

## 🚀 Para Uso en GitHub Actions (CI/CD)

### 1. Configurar Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Haz clic en **New repository secret**
4. Agrega cada una de estas variables:

```
WSO2_TOKEN_ENDPOINT=https://localhost:9453/oauth2/token
WSO2_CONSUMER_KEY=tu_consumer_key_aqui
WSO2_CONSUMER_SECRET=tu_consumer_secret_aqui
WSO2_GW_URL=https://localhost:8253
SHOPIFY_API_TOKEN=tu_shopify_token_aqui
```

### 2. Usar en GitHub Actions

El workflow `.github/workflows/setup-env.yml` está configurado para:
- Leer los secrets de GitHub
- Ejecutar el script `setup_env_from_secrets.sh`
- Crear/actualizar el archivo `.env` automáticamente

### 3. Ejecutar el Workflow

Puedes ejecutar el workflow manualmente desde:
- **Actions** → **Setup Environment from Secrets** → **Run workflow**

## 🔧 Para Uso Local con Variables de Entorno

Si quieres usar variables de entorno del sistema localmente:

```bash
export WSO2_TOKEN_ENDPOINT="https://localhost:9453/oauth2/token"
export WSO2_CONSUMER_KEY="tu_consumer_key_aqui"
export WSO2_CONSUMER_SECRET="tu_consumer_secret_aqui"
export WSO2_GW_URL="https://localhost:8253"
export SHOPIFY_API_TOKEN="tu_shopify_token_aqui"

cd AGENT
./setup_env_from_secrets.sh
```

## 📝 Notas de Seguridad

- ✅ Los archivos `.env` están en `.gitignore` y NO se suben a git
- ✅ Los Secrets de GitHub están encriptados
- ✅ Nunca compartas tus credenciales en código o commits
- ⚠️ Los Secrets solo están disponibles en GitHub Actions, no se pueden descargar localmente

