# 🔑 Guía para Configurar Archivos .env

Esta guía te ayudará a recrear los archivos `.env` que necesitas para cada componente del proyecto.

## 📋 Resumen de Archivos .env Necesarios

### 1. AGENT/.env
**Ubicación:** `AGENT/.env`  
**Template:** `AGENT/env.example`

**Variables necesarias:**
```bash
# WSO2 API Manager - Endpoints
WSO2_TOKEN_ENDPOINT=https://localhost:9453/oauth2/token
APIM_GATEWAY_URL=https://localhost:8253
WSO2_GW_URL=https://localhost:8243

# WSO2 API Manager - Credenciales Cliente (Client Credentials)
WSO2_CONSUMER_KEY=your_consumer_key_here
WSO2_CONSUMER_SECRET=your_consumer_secret_here

# Shopify (solo token, conexión va a través de APIM)
SHOPIFY_API_TOKEN=your_shopify_api_token_here

# OpenAI (accedido a través de APIM Gateway)
OPENAI_API_KEY=your_openai_api_key_here
```

**Para crear:**
```bash
cd AGENT
cp env.example .env
# Edita .env con tus valores reales
```

---

### 2. RAG/python-rag/.env
**Ubicación:** `RAG/python-rag/.env`  
**Template:** No hay env.example, pero se necesita crear

**Variables necesarias:**
```bash
# Groq (requerido)
GROQ-TOKEN=your_groq_token_here

# OpenAI (opcional)
OPENAI_API_KEY=your_openai_key_here
```

**Para crear:**
```bash
cd RAG/python-rag
# Crea el archivo .env manualmente
cat > .env << EOF
GROQ-TOKEN=your_groq_token_here
OPENAI_API_KEY=your_openai_key_here
EOF
```

---

### 3. MCP/.env
**Ubicación:** `MCP/.env`  
**Template:** `MCP/env.example`

**Variables necesarias:**
```bash
# OBS WebSocket
OBS_HOST=localhost
OBS_PORT=4444
OBS_PASS=your_obs_password_here
```

**Para crear:**
```bash
cd MCP
cp env.example .env
# Edita .env con tus valores reales
```

---

### 4. AI GATEWAY/aigateway-demo/.env
**Ubicación:** `AI GATEWAY/aigateway-demo/.env`  
**Template:** `AI GATEWAY/aigateway-demo/.env.example`

**Variables necesarias:**
```bash
# WSO2 API Manager
WSO2_APIM_HOST=localhost
WSO2_APIM_PORT=9453
WSO2_CONSUMER_KEY=your_shared_consumer_key
WSO2_CONSUMER_SECRET=your_shared_consumer_secret

# URLs de endpoints WSO2
OPENLLM_CHAT_COMPLETIONS_URL=https://your-wso2-server:8253/openaiapi/2.3.0/chat/completions
OPENAI_CHAT_COMPLETIONS_URL=https://your-wso2-server:8253/openaiapi/2.3.0/chat/completions
MISTRAL_CHAT_COMPLETIONS_URL=https://your-wso2-server:8253/mistralaiapi/0.0.2/v1/chat/completions
ANTHROPIC_CHAT_COMPLETIONS_URL=https://your-wso2-server:8253/anthropicapi/v1/messages
```

**Para crear:**
```bash
cd "AI GATEWAY/aigateway-demo"
cp .env.example .env
# Edita .env con tus valores reales
```

---

## 🔍 Dónde Encontrar tus API Keys

### Groq Token
1. Ve a: https://console.groq.com/
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys"
4. Genera o copia tu token

### OpenAI API Key
1. Ve a: https://platform.openai.com/api-keys
2. Inicia sesión
3. Crea una nueva API key o copia una existente

### WSO2 Credentials
1. Accede al WSO2 API Manager Developer Portal
2. Crea una aplicación
3. Genera Consumer Key y Consumer Secret
4. Obtén el Token Endpoint URL

### Shopify API Token
1. Ve a tu tienda Shopify Admin
2. Settings → Apps and sales channels → Develop apps
3. Crea una app y genera un API token

---

## ⚠️ IMPORTANTE

- ✅ Los archivos `.env` están en `.gitignore` y NO se suben a git
- ✅ Nunca compartas tus claves reales
- ✅ Cada componente necesita su propio archivo `.env`
- ✅ Los archivos `env.example` son solo plantillas sin valores reales

---

## 🚀 Script Rápido para Crear Todos los .env

```bash
# AGENT
cd AGENT && cp env.example .env && echo "✓ AGENT/.env creado - Edita con tus valores"

# RAG
cd ../RAG/python-rag && cat > .env << 'EOF'
GROQ-TOKEN=your_groq_token_here
OPENAI_API_KEY=your_openai_key_here
EOF
echo "✓ RAG/python-rag/.env creado - Edita con tus valores"

# MCP
cd ../../MCP && cp env.example .env && echo "✓ MCP/.env creado - Edita con tus valores"

# AI GATEWAY
cd "../AI GATEWAY/aigateway-demo" && cp .env.example .env && echo "✓ AI GATEWAY/.env creado - Edita con tus valores"
```

