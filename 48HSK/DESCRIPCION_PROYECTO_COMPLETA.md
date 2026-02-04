# 📋 Descripción Completa del Proyecto - Para otra IA

## 1. VISIÓN GENERAL DEL PROYECTO

### Nombre
**48HSK AI Agent** - Un agente de IA multi-componente que recomienda productos Shopify basado en datos de clima en tiempo real, con arquitectura de seguridad enterprise-grade.

### Propósito Principal
Demostrar cómo construir un **AI Agent production-ready** que:
- Accede a múltiples APIs externas (Shopify, OpenAI, Weather)
- Mantiene seguridad en todos los niveles (OAuth2, API Gateway, token management)
- Integra herramientas de forma segura (Model Context Protocol)
- Actualiza interfaces en vivo (OBS Studio)
- Escala en producción sin comprometer seguridad

---

## 2. FLUJO TÉCNICO COMPLETO

### Flujo Principal: Recomendación de Productos

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USUARIO EJECUTA COMANDO                                      │
│    $ ./start_demo.sh --city Barcelona --products 50             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 2. AGENT INICIA SESSION (agent_gpt4.py)                         │
│    • Lee .env (credenciales)                                    │
│    • Checa si token OAuth2 existe (token_cache.json)            │
│    • Si no existe → Dispara OAuth2 PKCE flow                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 3. OAuth2 PKCE FLOW (si no hay token)                           │
│    • Agent genera code_verifier + code_challenge                │
│    • Abre navegador: https://localhost:9443/authorize           │
│    • Usuario ingresa credenciales en WSO2 IS                    │
│    • WSO2 redirige a http://localhost:8000/callback?code=ABC    │
│    • Agent obtiene access_token + refresh_token                 │
│    • Guarda en token_cache.json (seguro)                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 4. OBTIENE TOKEN APIM (Client Credentials)                      │
│    • POST https://localhost:9453/oauth2/token                   │
│    • grant_type=client_credentials                              │
│    • client_id + client_secret (desde .env)                     │
│    • Response: Bearer eyJhbGc... (TTL 3600s)                    │
│    • Cache en memoria con refresh automático                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 5. OBTIENE DATOS WEATHER (Weather MCP)                          │
│    • Tool: get_weather("Barcelona")                             │
│    • Vía APIM Gateway: https://localhost:8253/weather-mcp       │
│    • Auth: Bearer {APIM_TOKEN}                                  │
│    • Weather MCP → Open-Meteo API (libre)                       │
│    • Response: {temp: 25, rain: 0, condition: "Partly Cloudy"}  │
│    • Cache por 3600s                                            │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 6. OBTIENE PRODUCTOS SHOPIFY                                    │
│    • _api("GET", "/products.json")                              │
│    • Headers: X-Shopify-Access-Token: {SHOPIFY_API_TOKEN}       │
│    • Directo a Shopify: rafa-ecommerce.myshopify.com            │
│    • Response: 50 productos con precio, inventario, etc         │
│    • Cache en memoria por sesión                                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 7. REASONING CON LLM (OpenAI GPT-4o-mini)                       │
│    • Semantic Kernel crea prompt con contexto:                  │
│      "Clima: 25°C, sin lluvia, nublado"                         │
│      "Productos disponibles: [lista de 50]"                     │
│      "Recomienda 8 productos ideales"                           │
│    • Via APIM Gateway:                                          │
│      POST https://localhost:8253/openaiapi/2.3.0/chat/...       │
│    • Auth: Bearer {APIM_TOKEN}                                  │
│    • OpenAI reasoning:                                          │
│      25°C → ropa ligera (camiseta, shorts)                      │
│      Sin lluvia → sin paraguas                                  │
│      Nublado → protección UV (gafas, sombrero)                  │
│    • Response: [Sudadera 49€, Shorts 39€, Gafas UV 29€, ...]   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 8. ACTUALIZA OBS STUDIO (OBS MCP)                               │
│    • Tool: setObsText(inputName="RotuloDemo", text="...")       │
│    • Vía stdio + OBS Bridge (Node.js)                           │
│    • Bridge: http://localhost:8888/call/SetInputSettings        │
│    • Conecta a OBS via WebSocket 4455                           │
│    • OBS actualiza fuente de texto EN VIVO                      │
│    • Visible en stream si está broadcasting                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 9. RESULTADO FINAL                                              │
│    ✅ Recomendación generada y auditada                         │
│    ✅ OBS actualizado en vivo                                   │
│    ✅ Logs en APIM con timestamp + user                         │
│    ✅ Token refresh automático si necesario                     │
│    ✅ Fallback si algún servicio falla                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. COMPONENTES PRINCIPALES

### A. AI Agent (agent_gpt4.py)
**Ubicación:** `/Users/rafagranados/Develop/charlas/48HSK/AGENT/agent_gpt4.py`
**Líneas:** 2708 líneas de Python

**Responsabilidades:**
- Orquestación central (Semantic Kernel 1.37.0)
- OAuth2 PKCE authentication
- Token management (caching, refresh, expiration)
- Shopify API calls
- MCP tool invocation
- Error handling y retry logic

**Métodos Clave:**
- `_get_token()`: Obtiene token OAuth2 del usuario
- `_get_apim_token()`: Obtiene token para APIM (Client Credentials)
- `_api(method, path, data)`: Llamadas REST a Shopify (directo)
- `_call_mcp_tool()`: Invoca herramientas MCP (Weather, OBS)
- `create_plan()`: Semantic Kernel function que genera recomendación

**Credenciales Necesarias (.env):**
```
WSO2_TOKEN_ENDPOINT=https://localhost:9453/oauth2/token
WSO2_CONSUMER_KEY=...
WSO2_CONSUMER_SECRET=...
SHOPIFY_API_TOKEN=...
OPENAI_API_KEY=...
```

---

### B. WSO2 Identity Server 7.1 (Autenticación)
**Ubicación:** `/Users/rafagranados/Develop/wso2/wso2is-7.1.0/`
**Puerto:** 9443 (HTTPS)

**Responsabilidades:**
- OAuth2 Authorization Server
- OIDC (OpenID Connect)
- PKCE support
- User management
- Token generation & validation

**Flujo OAuth2 PKCE:**
1. Agent: POST /authorize?code_challenge=X
2. IS: Redirige a login page
3. User: Ingresa credenciales
4. IS: Genera code=ABC123
5. Agent: POST /token con code + code_verifier
6. IS: Response: access_token + refresh_token

---

### C. WSO2 API Manager 4.6 (API Gateway)
**Ubicación:** `/Users/rafagranados/Develop/wso2/wso2am-4.6.0/`
**Puertos:** 
- 8253 (Gateway HTTPS)
- 9453 (Token Service HTTPS)
- 9443 (Admin Portal HTTPS)

**Responsabilidades:**
- Proxy centralizado para APIs
- OAuth2 token validation
- Rate limiting (100 req/min default)
- Request/response logging
- Analytics
- Circuit breaker

**APIs Proxeadas:**
```
GET/POST https://localhost:8253/shopify-admin/* 
  → Shopify Admin API 2024-01
  
GET https://localhost:8253/weather-mcp/*
  → Weather MCP FastAPI
  
POST https://localhost:8253/openaiapi/2.3.0/*
  → OpenAI Chat Completions
```

---

### D. Weather MCP Server
**Ubicación:** `/Users/rafagranados/Develop/charlas/48HSK/MCP/WEATHER/`
**Framework:** FastMCP + FastAPI
**Puerto:** 8080 (HTTP)

**Tool: get_weather**
```
Input:
  city: string (e.g., "Barcelona")
  days: integer (1-7, default 1)

Output:
  city: string
  temp_max: float
  temp_min: float
  rain_mm: float
  condition: string
  
Backend: Open-Meteo API (libre, sin auth)
```

**Flujo:**
1. Agent via APIM: POST /weather-mcp/mcp
2. Auth: Bearer token "weather-mcp-2026"
3. Weather MCP recibe request
4. Valida con Zod schema
5. Llama Open-Meteo API
6. Parsea y retorna JSON

---

### E. OBS MCP Server
**Ubicación:** `/Users/rafagranados/Develop/charlas/48HSK/MCP/OBS-MCP/`
**Componentes:**
- obs-mcp.js (Node.js MCP Server)
- bridge.py (HTTP bridge a OBS)

**Tools:**
1. `setObsText(inputName, text)`: Actualiza texto en OBS
2. `setSceneItemEnabled(itemName, enabled)`: Show/hide elementos

**Flujo:**
1. Agent via stdio: setObsText({inputName: "RotuloDemo", text: "Sudadera"})
2. OBS MCP valida con Zod
3. HTTP POST a bridge.py (localhost:8888)
4. Bridge conecta a OBS via WebSocket 4455
5. OBS ejecuta SetInputSettings
6. Response: {status: "ok"}

---

### F. Shopify Admin API
**Endpoints:** https://rafa-ecommerce.myshopify.com/admin/api/2024-01
**Authentication:** X-Shopify-Access-Token header
**Tipo:** REST + GraphQL

**Operaciones Usadas:**
```
GET /products.json
  → Lista de productos con id, title, price, inventory_quantity

POST /graphql.json
  → GraphQL query para queries complejas
  
PUT /products/{id}.json
  → Actualizar producto (precio, descripción, etc)
```

**Ejemplo: Get products**
```bash
curl -X GET https://rafa-ecommerce.myshopify.com/admin/api/2024-01/products.json \
  -H "X-Shopify-Access-Token: shpat_xxxxx" \
  -H "Content-Type: application/json"
```

---

### G. OpenAI API
**Modelo:** GPT-4o-mini
**Access:** Vía APIM Gateway (https://localhost:8253/openaiapi/2.3.0)
**Authentication:** Bearer token (APIM)

**Uso:**
```python
# Semantic Kernel invoca OpenAI
# Prompt incluye:
# - Datos de clima (temp, rain, condition)
# - Listado de productos disponibles
# - Instrucción: "Recomienda 8 productos"

# OpenAI reasoning:
# - Analiza clima
# - Filtra productos relevantes
# - Justifica cada recomendación

# Response: array de 8 productos con precios y razones
```

---

## 4. FLUJOS DE SEGURIDAD

### Autenticación - OAuth2 PKCE
```
┌──────────────────────────────────────────────────────────────┐
│ OAuth2 Authorization Code + PKCE Flow                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Agent                WSO2 IS              Browser            │
│  │                      │                      │             │
│  ├─ 1. Generate────────→│                      │             │
│  │  code_verifier       │                      │             │
│  │  code_challenge      │                      │             │
│  │                      │                      │             │
│  ├─ 2. Open browser────────────────────────────→             │
│  │  /authorize?        │                      │             │
│  │  code_challenge=X   │                      │             │
│  │                      │                      │             │
│  │                      ├─ 3. Redirige a login page          │
│  │                      │                      │             │
│  │                      │                      ├─ User       │
│  │                      │                      │  credentials │
│  │                      │                      │             │
│  │                      ├─ 4. Valida credenciales           │
│  │                      │                      │             │
│  │                      ├─ 5. Genera code=ABC123            │
│  │                      │                      │             │
│  │                      ├─ 6. Redirige callback─→            │
│  │                      │                      │             │
│  ├─ 7. Recibe code←────────────────────────────┤             │
│  │                      │                      │             │
│  ├─ 8. POST /token────→│                      │             │
│  │  code=ABC123         │                      │             │
│  │  code_verifier=X     │                      │             │
│  │                      │                      │             │
│  │                      ├─ 9. Valida code_verifier          │
│  │                      │                      │             │
│  │                      ├─ 10. Genera tokens                 │
│  │                      │                      │             │
│  ←─ 11. Response ──────┤                      │             │
│  │  access_token        │                      │             │
│  │  refresh_token       │                      │             │
│  │  id_token            │                      │             │
│  │  expires_in: 3600    │                      │             │
│  │                      │                      │             │
│  ├─ 12. Cache en disk                         │             │
│  │  token_cache.json                          │             │
│  │                      │                      │             │
│  ✅ AUTENTICADO                                │             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Seguridad PKCE:**
- Code verifier: 128 caracteres aleatorios (Base64URL)
- Code challenge: SHA256(code_verifier)
- Previene: Authorization code interception
- No requiere backend secret
- Mobile/Desktop safe

---

### Client Credentials - Token APIM
```
┌──────────────────────────────────────────────────────────┐
│ Client Credentials Flow (API to API)                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Agent                    APIM Token Service             │
│  │                             │                        │
│  ├─ 1. POST /oauth2/token────→│                        │
│  │  grant_type=                │                        │
│  │  client_credentials         │                        │
│  │  client_id=...              │                        │
│  │  client_secret=...          │                        │
│  │  Base64: encr(id:secret)    │                        │
│  │                             │                        │
│  │                    ├─ 2. Valida credenciales        │
│  │                    │                                │
│  │                    ├─ 3. Genera access_token        │
│  │                    │    scope: read_products,       │
│  │                    │           write_products,      │
│  │                    │           update_descriptions  │
│  │                    │    expires_in: 3600            │
│  │                    │                                │
│  ←─ 4. Response ─────┤                                 │
│  │  {                  │                                │
│  │    access_token:    │                                │
│  │      eyJhbGc...     │                                │
│  │    token_type:      │                                │
│  │      Bearer         │                                │
│  │    expires_in:      │                                │
│  │      3600           │                                │
│  │    scope: read...   │                                │
│  │  }                  │                                │
│  │                     │                                │
│  ├─ 5. Cache en memoria                                │
│  │  _token_cache = token                               │
│  │  _token_expires_at = now + 3600 - 30 buffer        │
│  │                     │                                │
│  ├─ 6. Usa token en requests:                          │
│  │  GET /shopify-admin/products.json                   │
│  │  Authorization: Bearer eyJhbGc...                   │
│  │                     │                                │
│  │  ✅ AUTORIZADO (APIM valida scopes)               │
│  │                                                     │
│  ├─ 7. Si token expira (expires_at < now):           │
│  │  ├─ Auto-refresh antes de expiración              │
│  │  └─ Transición seamless                            │
│  │                                                     │
│  ⏱️  TTL: 3600 segundos (1 hora)                       │
│  ⏱️  Buffer de refresh: 30 segundos antes              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

### Rate Limiting en APIM
```
┌──────────────────────────────────────────────────────────┐
│ Rate Limiting (Throttling Policy)                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Request 1    ┌──────────────────┐                       │
│  ──────────→  │ APIM Rate Limit  │─→ 200 OK             │
│               │  (100 req/min)   │   [1/100]             │
│               └──────────────────┘                       │
│                                                          │
│  Request 2    ┌──────────────────┐                       │
│  ──────────→  │ Check counter    │─→ 200 OK             │
│               │ [2/100]          │                       │
│               └──────────────────┘                       │
│                                                          │
│  ...                                                     │
│                                                          │
│  Request 100  ┌──────────────────┐                       │
│  ──────────→  │ [100/100]        │─→ 200 OK             │
│               │ Counter = 0      │   (reset en 1 min)   │
│               └──────────────────┘                       │
│                                                          │
│  Request 101  ┌──────────────────┐                       │
│  ──────────→  │ [101 > 100]      │─→ 429 Too Many       │
│               │ Enqueue o reject │   Requests (Retry)   │
│               └──────────────────┘                       │
│                                                          │
│  Efectos:                                               │
│  ✓ Protege Shopify de flood                            │
│  ✓ Protege OpenAI de overspend                         │
│  ✓ Equitable para múltiples users                      │
│  ✓ Logs de intentos excedidos                          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

### Token Management (Refresh & Expiration)
```python
# En agent_gpt4.py

def _get_apim_token(self):
    """Token con cache y refresh automático"""
    now = time.time()
    
    # ✓ Token existe y aún es válido (buffer 30s)
    if self._token_cache and now < (self._token_expires_at - 30):
        return self._token_cache  # Return cached
    
    # ✗ Token expirado o no existe → Renovar
    try:
        from oauth2_apim import _fetch_oauth2_token_sync
        token, expires_in = _fetch_oauth2_token_sync()
        
        # Cache
        self._token_cache = token
        self._token_expires_at = time.time() + expires_in
        
        return token
    except Exception as e:
        return None

# En _api() method
def _api(self, method, path, data=None):
    headers = {
        "X-Shopify-Access-Token": os.getenv("SHOPIFY_API_TOKEN"),
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, verify=False)
    
    # ✓ Success
    if response.status_code == 200:
        return response.json()
    
    # ✗ Token inválido → Retry
    elif response.status_code == 401:
        print("Token expirado, refreshing...")
        # ... retry logic
    
    # ✗ Sin permisos
    elif response.status_code == 403:
        return {"error": "Sin permisos"}
```

---

## 5. FLUJOS DE ERROR Y RECUPERACIÓN

### Manejo de Tokens Expirados
```
Scenario: Token APIM expira durante request

1. Agent hace request con token expirado
   GET /shopify-admin/products
   Authorization: Bearer eyJ...OLD

2. APIM valida token → 401 Unauthorized

3. Agent recibe 401:
   a) Limpia token cache
   b) Refresh forcado: _get_apim_token(force_refresh=True)
   c) Obtiene nuevo token
   d) Reintentar request original

4. Request con nuevo token:
   GET /shopify-admin/products
   Authorization: Bearer eyJ...NEW

5. ✅ Success (200 OK)

Max retries: 1 (para evitar loops infinitos)
Log: Timestamp, usuario, token_old, token_new
```

### Fallback si Shopify está Down
```
Scenario: Shopify API devuelve 503

1. Agent intenta GET /products.json
   Response: 503 Service Unavailable

2. Agent manejo de error:
   if response.status_code == 503:
       # Intenta cached data (si existe)
       if self.cached_products:
           return self.cached_products
       
       # Si no hay cache → Error
       return {"error": "Shopify is down"}

3. User feedback:
   "Shopify temporalmente no disponible.
    Usando datos en caché (actualizado hace 2 horas)"

4. APIM Circuit Breaker:
   Después de 3 errores 5xx:
   - Abre el circuito
   - Rechaza nuevos requests durante 30s
   - Luego, half-open para probar recuperación
```

### MCP Tool Validation Errors
```python
# setObsText tool en OBS MCP

from zod import z

SetObsTextSchema = z.object({
    inputName: z.string().describe("Text source name"),
    text: z.string().max(1000).describe("Text to display")
})

# Si input inválido:
input_malformed = {
    "inputName": "RotuloDemo",
    "text": "A" * 2000  # > 1000 chars
}

try:
    SetObsTextSchema.parse(input_malformed)
except ValidationError as e:
    return {
        "error": "Input validation failed",
        "details": str(e)
    }
```

---

## 6. CONFIGURACIÓN DE ENTORNO

### .env (AGENT)
```bash
# WSO2 Identity Server (OAuth2)
WSO2_TOKEN_ENDPOINT=https://localhost:9453/oauth2/token
WSO2_AUTHORIZE_ENDPOINT=https://localhost:9443/oauth2/authorize
WSO2_CONSUMER_KEY=shopify_agent_app
WSO2_CONSUMER_SECRET=xxxxxxxxxxxxx

# APIM Gateway
APIM_GATEWAY_URL=https://localhost:8253

# Shopify
SHOPIFY_STORE_URL=https://rafa-ecommerce.myshopify.com
SHOPIFY_API_TOKEN=shpat_xxxxxxxxxxxxx

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Debug
DEBUG_MODE=false
AGENT_SHOW_THINKING=false
```

### Archivos Generados
```
AGENT/
├── token_cache.json          # OAuth2 tokens (local)
│   ├── access_token: "eyJ..."
│   ├── refresh_token: "ref..."
│   ├── expires_at: 1707043200
│   └── user: "admin@example.com"
│
├── .env                       # Credenciales (NO en git)
│
└── logs/
    └── agent.log            # Execution logs
```

---

## 7. ARQUITECTURA DE SEGURIDAD RESUMIDA

```
┌─────────────────────────────────────────────────────────────┐
│                    AI AGENT (Python)                        │
├─────────────────────────────────────────────────────────────┤
│  • Semantic Kernel 1.37.0                                   │
│  • OAuth2 PKCE token (user authentication)                  │
│  • Client Credentials token (APIM access)                  │
│  • Token caching + refresh automático                       │
│  • Error handling y retry logic                             │
└────┬────────────────────────────────────────────────────────┘
     │
     ├─ GET /authorize (OAuth2 PKCE)
     │  └─→ WSO2 Identity Server :9443
     │      • Login user
     │      • Generate access + refresh tokens
     │      • Token cache en disk (token_cache.json)
     │
     ├─ GET /oauth2/token (Client Credentials)
     │  └─→ WSO2 APIM Token Service :9453
     │      • Autentica con client_id + client_secret
     │      • Genera Bearer token (3600s TTL)
     │      • Cache en memoria
     │
     ├─ GET/POST /*
     │  └─→ WSO2 APIM Gateway :8253
     │      • Valida Bearer token (401 si inválido)
     │      • Rate limiting (100 req/min)
     │      • Logging + Analytics
     │      • Circuit breaker si backend falla
     │      ├─→ Shopify Admin API (proxy)
     │      ├─→ OpenAI API (proxy)
     │      └─→ Weather MCP (proxy)
     │
     └─ stdio + HTTP:8888
        └─→ OBS MCP
            • Valida con Zod schema
            • Bearer token "weather-mcp-2026"
            • WebSocket a OBS Studio :4455
```

---

## 8. STACK TECNOLÓGICO COMPLETO

| Capa | Tecnología | Versión | Puerto | Propósito |
|------|-----------|---------|--------|-----------|
| **Orquestación** | Python | 3.14 | - | AI Agent logic |
| **Framework IA** | Semantic Kernel | 1.37.0 | - | LLM orchestration |
| **HTTP Client** | requests | 2.x | - | API calls |
| **OAuth2 User** | WSO2 Identity Server | 7.1 | 9443 | User auth |
| **OAuth2 Service** | WSO2 APIM Token | 4.6 | 9453 | API auth |
| **API Gateway** | WSO2 APIM Gateway | 4.6 | 8253 | Proxy + security |
| **MCP Server (Weather)** | FastMCP + FastAPI | latest | 8080 | Tool server |
| **MCP Server (OBS)** | Node.js SDK | 18+ | stdio | Tool server |
| **OBS Bridge** | Python aiohttp | 3.x | 8888 | OBS connector |
| **e-Commerce API** | Shopify Admin API | 2024-01 | 443 | Product data |
| **LLM** | OpenAI | GPT-4o-mini | 443 | Reasoning |
| **Weather API** | Open-Meteo | free | 443 | Forecast |
| **OBS Studio** | - | latest | 4455 | UI updates |
| **Database** | PostgreSQL | 14+ | 5432 | Sessions (future) |

---

## 9. CASOS DE USO DEMOSTRADOS

### Demo Principal: "Recomendación de Productos por Clima"
```
Entrada:  --city Barcelona --products 50
Proceso: Climate → Shopify → OpenAI → OBS
Salida:   8 productos recomendados con explicación
Tiempo:   ~5 segundos
Validaciones: 5+ capas de seguridad
Logs:     Todas las operaciones auditadas
```

### Casos de Uso Secundarios (Potential)
1. **Precio dinámico**: Ajustar precios según climate demand
2. **Inventory alert**: Notificar si stock bajo de productos recomendados
3. **User preferences**: Personalizar recomendaciones por usuario favorito
4. **Multi-language**: Traducir recomendaciones a idioma user
5. **A/B testing**: Comparar recomendaciones diferentes MCPs

---

## 10. MÉTRICAS Y MONITOREO

### Métricas Capturadas
```
Por Request:
├─ Timestamp
├─ User ID
├─ Method (GET/POST/PUT/DELETE)
├─ Endpoint
├─ Status code
├─ Response time (ms)
├─ Error (si aplica)
└─ Tokens usado (count)

Agregados (Dashboard APIM):
├─ Request per second
├─ Error rate (%)
├─ P50/P95/P99 latency
├─ Quota usage
└─ Top endpoints
```

### Alertas Configuradas
```
✓ Error rate > 5% → Alert
✓ Response time > 2000ms → Alert
✓ Quota exceeded → Block + Alert
✓ Token refresh failed → Alert
✓ Backend down (3x 5xx) → Circuit open
```

---

## 11. DIAGRAMA FINAL (Arquitectura Completa)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USUARIO FINAL                              │
│                      (CLI Terminal / Browser)                       │
└────────────┬────────────────────────────────────────────────────────┘
             │
             │ ./start_demo.sh --city Barcelona
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     AGENT (agent_gpt4.py)                           │
│                    Python + Semantic Kernel                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ • Read credenciales from .env                               │  │
│  │ • Check token_cache.json para OAuth2                        │  │
│  │ • Si no existe → Trigger PKCE flow                          │  │
│  │ • Get APIM token (Client Credentials)                       │  │
│  │ • Call MCP tools (Weather, OBS)                             │  │
│  │ • Call Shopify API (directo con token)                      │  │
│  │ • Invoke OpenAI via APIM                                    │  │
│  │ • Return recomendations                                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────┬─────────────────┬─────────────────┬──────────────────────────┘
     │                 │                 │
     │                 │                 │
     ▼                 ▼                 ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ WSO2 IS     │  │ WSO2 APIM    │  │ OBS MCP      │
│ :9443       │  │ :8253        │  │ stdio/8888   │
│             │  │              │  │              │
│ OAuth2 PKCE │  │ Gateway      │  │ setObsText   │
│ + User Auth │  │ + Rate Limit │  │ + Validation │
└────┬────────┘  └──┬───────┬──┘  └──┬───────────┘
     │              │       │        │
     │              │       │        │
     │          ┌───▼───────▼───┐   │
     │          │               │   │
     │    ┌─────▼──────┐   ┌────▼──┘
     │    │ Shopify    │   │
     │    │ Admin API  │   │ OBS Studio
     │    │ 2024-01    │   │ WebSocket 4455
     │    └─────┬──────┘   │ (UI update)
     │          │          │
     │    ┌─────▼──────┐  │
     │    │ OpenAI     │  │
     │    │ GPT-4o mini│  │
     │    └─────┬──────┘  │
     │          │         │
     │    ┌─────▼──────┐  │
     │    │ Weather    │  │
     │    │ MCP/Meteo  │  │
     │    └────────────┘  │
     │                    │
     └────────────────────┘
           (via APIM)
```

---

## 12. REPOSITORIO Y CÓDIGO

**GitHub:** https://github.com/rgranadosd/charlas

**Estructura:**
```
charlas/
├── 48HSK/
│   ├── AGENT/
│   │   ├── agent_gpt4.py (main)
│   │   ├── oauth2_apim.py
│   │   ├── banners/
│   │   ├── .env (NO en git)
│   │   └── token_cache.json (NO en git)
│   │
│   ├── MCP/
│   │   ├── WEATHER/
│   │   │   └── FastMCP server
│   │   └── OBS-MCP/
│   │       ├── obs-mcp.js
│   │       └── bridge.py
│   │
│   ├── ARQUITECTURA.md
│   ├── DIAGRAMA_COMUNICACIONES.md
│   ├── APIM_SHOPIFY_CONFIG.md
│   ├── CONFIGURAR_ENV.md
│   ├── CALL_FOR_PAPERS.md
│   └── README.md
│
├── wso2am-4.6.0/ (API Manager)
└── wso2is-7.1.0/ (Identity Server)
```

---

## 13. CLAVES DEL PROYECTO

✅ **Seguridad en capas**: OAuth2 + API Gateway + Token Management  
✅ **Escalable**: MCP permite N tools sin tocar agent core  
✅ **Production-ready**: Error handling, logging, monitoring  
✅ **Demo-friendly**: Visual updates en OBS durante ejecución  
✅ **Replicable**: Patrones aplicables a cualquier AI Agent  
✅ **Open source**: MIT License, código disponible en GitHub  

---

## 14. PRÓXIMOS PASOS

1. **Persistencia**: PostgreSQL para session storage
2. **Alerting**: Integrar Slack/PagerDuty para emergencies
3. **Streaming**: Token streaming desde OpenAI (partial SSE)
4. **Caching**: Redis para mejor performance
5. **Multi-user**: Soporte para múltiples usuarios simultáneos
6. **A/B testing**: Comparar recomendaciones de diferentes MCPs
7. **Analytics**: Dashboard con trends y patterns
8. **Mobile**: App móvil con same OAuth2 flow

---

**FIN DE DESCRIPCIÓN COMPLETA**

Para usar esta descripción con otra IA, puedes:
1. Copiar-pegar directamente
2. Usar como context para prompt engineering
3. Adaptar secciones específicas según necesidad
4. Completar con outputs actuales del código
