# 🔑 Variables de Entorno Necesarias para AGENT

## ✅ OBLIGATORIAS (Sin estas, el agente NO funcionará)

### 1. WSO2 API Manager (Gateway) - OBLIGATORIO
```bash
# Endpoint para obtener el token de acceso del APIM Gateway
WSO2_TOKEN_ENDPOINT=https://localhost:8243/token

# Consumer Key y Consumer Secret del APIM
# Obtener del WSO2 API Manager Developer Portal
WSO2_CONSUMER_KEY=tu_consumer_key_aqui
WSO2_CONSUMER_SECRET=tu_consumer_secret_aqui

# URL base del Gateway de WSO2
WSO2_GW_URL=https://localhost:8243
```

### 2. Shopify - OBLIGATORIO
```bash
# Token de API de Shopify
SHOPIFY_API_TOKEN=tu_shopify_token_aqui
```

### 3. OpenAI - OBLIGATORIO
```bash
# Clave de API de OpenAI
OPENAI_API_KEY=tu_openai_key_aqui
```

---

## ⚙️ OPCIONALES (Solo si usas Identity Server para validación de usuario)

### WSO2 Identity Server (Opcional)
```bash
# Solo necesario si quieres validar usuario/contraseña contra Identity Server
# Si NO configuras estas, el agente usará solo Client Credentials (sin validación de usuario)
WSO2_USERNAME=Rafa
WSO2_PASSWORD=tu_password_aqui
WSO2_CLIENT_ID=tu_client_id_aqui
WSO2_CLIENT_SECRET=tu_client_secret_aqui

# Endpoint de Identity Server (opcional, se construye automáticamente si no se especifica)
# WSO2_IS_TOKEN_ENDPOINT=https://localhost:9443/oauth2/token
```

**Nota:** Si configuras `WSO2_USERNAME`, el agente validará el usuario contra Identity Server antes de continuar. Si no lo configuras, solo usará Client Credentials para obtener el token del APIM Gateway.

---

## 📋 Resumen Rápido

**Mínimo necesario para que funcione:**
1. ✅ `WSO2_TOKEN_ENDPOINT` - Endpoint del APIM Gateway
2. ✅ `WSO2_CONSUMER_KEY` - Consumer Key del APIM
3. ✅ `WSO2_CONSUMER_SECRET` - Consumer Secret del APIM
4. ✅ `WSO2_GW_URL` - URL base del Gateway
5. ✅ `SHOPIFY_API_TOKEN` - Token de Shopify
6. ✅ `OPENAI_API_KEY` - API Key de OpenAI

**Opcional (solo si quieres validación de usuario):**
- `WSO2_USERNAME`
- `WSO2_PASSWORD`
- `WSO2_CLIENT_ID`
- `WSO2_CLIENT_SECRET`
- `WSO2_IS_TOKEN_ENDPOINT` (se construye automáticamente)

---

## 🔍 Dónde Obtener Cada Valor

### WSO2 Consumer Key/Secret
1. Accede al **WSO2 API Manager Developer Portal**
2. Crea una **aplicación**
3. Genera **Consumer Key** y **Consumer Secret**
4. Copia los valores

### WSO2 Endpoints
- **WSO2_TOKEN_ENDPOINT**: `https://tu-servidor:8243/token` (puerto 8243 para APIM)
- **WSO2_GW_URL**: `https://tu-servidor:8243` (puerto 8243 para Gateway)
- **WSO2_IS_TOKEN_ENDPOINT**: `https://tu-servidor:9443/oauth2/token` (puerto 9443 para Identity Server)

### Shopify Token
1. Ve a tu **Shopify Admin**
2. **Settings** → **Apps and sales channels** → **Develop apps**
3. Crea una app y genera un **API token**

### OpenAI API Key
1. Ve a: https://platform.openai.com/api-keys
2. Inicia sesión
3. Crea una nueva API key o copia una existente

---

## 📝 Ejemplo de Archivo .env Completo

```bash
# ============================================
# WSO2 API MANAGER / GATEWAY (OBLIGATORIO)
# ============================================
WSO2_TOKEN_ENDPOINT=https://localhost:8243/token
WSO2_CONSUMER_KEY=tu_consumer_key_aqui
WSO2_CONSUMER_SECRET=tu_consumer_secret_aqui
WSO2_GW_URL=https://localhost:8243

# ============================================
# SHOPIFY (OBLIGATORIO)
# ============================================
SHOPIFY_API_TOKEN=tu_shopify_token_aqui

# ============================================
# OPENAI (OBLIGATORIO)
# ============================================
OPENAI_API_KEY=tu_openai_key_aqui

# ============================================
# WSO2 IDENTITY SERVER (OPCIONAL)
# ============================================
# Solo si quieres validación de usuario
# WSO2_USERNAME=Rafa
# WSO2_PASSWORD=tu_password_aqui
# WSO2_CLIENT_ID=tu_client_id_aqui
# WSO2_CLIENT_SECRET=tu_client_secret_aqui
```

