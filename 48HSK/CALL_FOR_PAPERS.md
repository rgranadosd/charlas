# 🎤 Call for Papers - Propuestas de Temas

## 🔥 Propuesta Principal (SENSACIONALISTA)

### 📌 Título
**"Cómo Proteger un AI Agent que Roba Datos de Shopify, Conecta con OpenAI y Actualiza OBS en Vivo: La Seguridad Que Nadie te Enseña"**

#### Versión Alternativa (Profesional)
**"Securización de Agentes de IA Multi-Componente: Orquestación Segura con OAuth2, API Gateways y Model Context Protocol en Arquitecturas Modernas"**

---

## Resumen Ejecutivo (Abstract)

### Versión Corta (150 palabras)

```
Tu AI Agent necesita acceder a APIs sensibles: Shopify, OpenAI, Weather, OBS...
¿Dónde guardas los tokens? ¿Cómo evitas que alguien robe credenciales? 
¿Qué pasa si un token expira a las 3am?

Este talk no es teoría. Es una arquitectura production-ready que resuelve 
TODOS esos problemas con patrones que funcionan en el mundo real:

✅ OAuth2 PKCE: Autenticación segura de usuarios (sin exponer credenciales)
✅ Client Credentials: Token-to-token para APIs
✅ API Gateway: Rate limiting centralizado (detiene ataques)
✅ Model Context Protocol: Integración segura de herramientas (validación Zod)
✅ Token Management: Refresh automático, expiration handling, rotación

Demostración en vivo: Un AI Agent que recomienda productos Shopify 
basado en el clima, actualiza OBS Studio en tiempo de ejecución, 
¡y todo está auditado y securizado!

Para arquitectos, security engineers y developers que quieren llevar 
sus AI Agents a producción sin que explote.
```

### Versión Extendida (350 palabras)

```
ESCENARIO REAL: Tu startup acaba de crear un AI Agent cool. 
El problema: necesita acceso a Shopify, OpenAI, APIs externas, y actualizar 
interfaces en vivo. La pregunta incómoda: ¿Es seguro?

La mayoría de developers NO lo hacen seguro. Los tokens están en .env, 
en logs, a veces hardcodeados. Los secrets de exponen en Slack. 
Los tokens expiran sin notice. Es un desastre.

Esta sesión presenta la SOLUCIÓN REAL que usamos en producción:

═══════════════════════════════════════════════════════════════

ACTO 1: EL PROBLEMA (Los riesgos que no ves)
- Token expirado = App crash silencioso a las 3am
- Credenciales en logs = Breach garantizado
- Rate limiting ignorado = APIs externas te bloquean
- Sin auditoría = Compliance te demanda

═══════════════════════════════════════════════════════════════

ACTO 2: LA ARQUITECTURA SEGURA

1️⃣ Autenticación Multi-Capa
   • OAuth2 + PKCE: Login de usuarios (seguro)
   • Client Credentials: APIs internas (escalable)
   • Token caching + refresh automático (nunca expira)
   • Detección de 401/403 con reintentos

2️⃣ API Gateway (WSO2)
   • Proxy centralizado para TODO
   • Rate limiting inteligente (10-100 req/min)
   • Logging y auditoría automática
   • Circuit breaker si backend falla

3️⃣ Model Context Protocol (MCP)
   • Framework seguro para herramientas
   • Validación Zod (rechaza requests malformadas)
   • Aislamiento de permisos
   • Schema definition clara

4️⃣ Monitoreo y Alertas
   • Error rate > 5% → ALERTA
   • Latencia > 2s → ALERTA
   • Quota exceeded → BLOQUEA

═══════════════════════════════════════════════════════════════

ACTO 3: DEMO EN VIVO (El momento épico)

Usuario ejecuta: $ ./start_demo.sh --city Barcelona

➡️ OAuth2 PKCE: Login (vemos el código_challenge en URL)
➡️ Weather MCP: "¿Clima en Barcelona?" → Open-Meteo (libre)
➡️ Shopify API: 50 productos via proxy seguro
➡️ OpenAI GPT-4o-mini: "Recomienda 8 para 25°C"
➡️ OBS Studio: Rótulo se actualiza MIENTRAS se procesa

RESULTADO: Una recomendación validada a través de 5 capas de seguridad,
con logs centralizados, sin exposición de credenciales.

═══════════════════════════════════════════════════════════════

ACTO 4: LECCIONES APRENDIDAS

✓ OAuth2 es non-negotiable en 2026
✓ API Gateway no es opcional (es tu muro de fuego)
✓ MCP escala mejor que "hardcodear tools"
✓ Monitoreo > debugging después de un crash
✗ Nunca confíes en los defaults de seguridad

═══════════════════════════════════════════════════════════════

STACK TÉCNICO
• Python 3.14 + Semantic Kernel 1.37.0
• WSO2 Identity Server 7.1 (OAuth2)
• WSO2 API Manager 4.6 (Gateway)
• FastMCP + FastAPI (Servidores)
• Shopify GraphQL + OpenAI GPT-4o-mini
• PostgreSQL + OBS Studio

═══════════════════════════════════════════════════════════════

PÚBLICO: Arquitectos, Security Engineers, Backend Developers
DURACIÓN: 45-60 minutos
NIVEL: Intermedio-Avanzado
REPO: github.com/rgranadosd/charlas (código real)
```

---

## 🎯 Temas Alternativos (Con Títulos Sensacionalistas)

### Opción 2️⃣
**"Los Hackers Están Buscando Tus Tokens: Cómo Proteger un AI Agent Multi-API"**
- Enfoque: OAuth2, token management
- Tiempo: 45 min
- Nivel: Intermedio

### Opción 3️⃣
**"Tu API Gateway es tu Mejor Firewall: Defendiendo Agentes LLM Contra Abuso"**
- Enfoque: Rate limiting, API management
- Tiempo: 60 min
- Nivel: Avanzado

### Opción 4️⃣
**"Model Context Protocol: El Estándar Que Las Grandes Tech Usaban en Secreto"**
- Enfoque: MCP, integración de tools
- Tiempo: 45 min
- Nivel: Intermedio

### Opción 5️⃣
**"De Startup a Producción: Cómo No Quebrar tu App de IA en la Escala"**
- Enfoque: Arquitectura, operaciones, lessons learned
- Tiempo: 60 min
- Nivel: Intermedio-Avanzado

---

## 📊 Estructura Completa (45 min)

### ⏱️ Minutos 0-3: Hook Explosivo
```
"Hace 6 meses descubrimos un token de Shopify en nuestros logs de producción.
Estaba ahí hace 3 meses. Nadie lo supo.

Hoy voy a mostrar cómo pasó... y cómo hacerlo IMPOSIBLE que pase.
```

### ⏱️ Minutos 3-10: El Problema (Dónde está el fuego)
```
❌ Problema 1: Tokens en variables de entorno (.env)
   → Si leakea .env, leakean TODOS los tokens
   
❌ Problema 2: Tokens expirados sin reintentos
   → 3am crash, nadie lo ve hasta mañana
   
❌ Problema 3: Sin rate limiting
   → Shopify te bloquea si pegas 1000 req/seg
   
❌ Problema 4: Sin auditoría
   → ¿Quién accedió a qué? ¿Cuándo? ¿Por qué?
   
❌ Problema 5: MCP tools sin validación
   → Un prompt injection = RCE en tu servidor
```

### ⏱️ Minutos 10-25: La Solución Arquitectónica

#### Bloque 1: OAuth2 PKCE (5 min)
```
User → Authorization Code → Callback Listener → Token (en cache seguro)

¿Por qué PKCE?
- No requiere backend secret
- Mobile/Desktop safe
- Está en RFC 7636 (estándar)

¿Por qué Client Credentials?
- Servicio a servicio (sin usuario)
- Token automático
- Refresh antes de expiración
```

#### Bloque 2: API Gateway (5 min)
```
┌──────────┐
│ AI Agent │──┐
└──────────┘  │
              ├──→ [APIM 8253] ←─┬─ Shopify
              ├──→ [APIM 8253] ←─┬─ OpenAI
              └──→ [APIM 8253] ←─┬─ Weather

Qué hace APIM:
✓ Valida Bearer token (401 → rechaza)
✓ Rate limit (100 req/min → enqueue)
✓ Logging (quién, qué, cuándo)
✓ Analytics (respuesta en <100ms)
✓ Circuit breaker (backend down → fallback)
```

#### Bloque 3: MCP Seguro (5 min)
```
Tool: get_weather
├─ Input schema (Zod): {city: string, days: 1-7}
├─ Auth: Bearer token "weather-mcp-2026"
├─ Rate: 10 req/min
├─ Logging: cada call loguea user + timestamp
└─ No permite: RCE, file access, network calls

Tool: set_obs_text
├─ Input schema (Zod): {inputName: string, text: string}
├─ Permisos: solo write_scene_items
├─ No permite: acceso a sources sensibles
└─ Validación: rechaza strings >1000 chars
```

### ⏱️ Minutos 25-35: Demo en Vivo (El Momento)
```
$ ./start_demo.sh --city Barcelona --products 50

[1] ✅ OAuth2 PKCE Login
    → Navegador abre https://localhost:9443/authorize?code_challenge=...
    → Usuario entra creds
    → Callback recibe code=ABC123
    → Intercambia por access_token + refresh_token

[2] ✅ Obtiene token APIM
    POST https://localhost:9453/oauth2/token
    grant_type=client_credentials
    → Response: Bearer eyJhbGc...

[3] ✅ Weather MCP
    GET https://localhost:8253/weather-mcp
    → Barcelona: 25°C, sin lluvia, nublado

[4] ✅ Shopify (vía APIM)
    POST https://localhost:8253/shopify-admin/graphql.json
    → 50 productos retornados

[5] ✅ OpenAI (vía APIM)
    POST https://localhost:8253/openaiapi/2.3.0/chat/completions
    → GPT-4o: "Para 25°C: Sudadera, shorts, gafas UV..."

[6] ✅ OBS MCP
    Tool call: setObsText({inputName: "RotuloDemo", text: "Sudadera 49€"})
    → OBS se actualiza EN VIVO

[7] 📊 Logs Centralizados
    APIM dashboard muestra:
    - 6 requests en 2.3 segundos
    - 0 errors
    - Audit trail completo
```

### ⏱️ Minutos 35-40: Lecciones Aprendidas
```
📚 LECCIÓN 1: OAuth2 es el estándar, no la excepción
   - PKCE para apps no-backend
   - Authorization Code + refresh para users
   - Client Credentials para servicios

📚 LECCIÓN 2: API Gateway NO es overhead
   - Es tu firewall, tu auditor, tu monitor
   - Te ahorra 10x en time debugging
   - En AWS/Azure/GCP es managed

📚 LECCIÓN 3: MCP > hardcodear tools
   - Escalas a N tools sin tocar agent code
   - Validación centralizada
   - Permisos por tool

📚 LECCIÓN 4: Token expiration is a feature, not a bug
   - Refresh automático antes de expiración
   - Retry on 401
   - Logs si algo falla

📚 LECCIÓN 5: Monitoreo es crítico
   - Alerta si error_rate > 5%
   - Alerta si latencia > 2s
   - Alerta si quota_exceeded

⚠️ DON'T:
   ✗ Guardar tokens en .env sin rotación
   ✗ Hardcodear credenciales
   ✗ Ignorar expiración de tokens
   ✗ Hacer requests sin validación
   ✗ Omitir logging de accesos
```

### ⏱️ Minutos 40-45: Q&A + Cierre
```
Preguntas frecuentes ya preparadas:

P: ¿Qué pasa si el API Gateway se cae?
R: Failover a replica (Kubernetes), con circuit breaker en agent

P: ¿Cómo manejas secretos rotados?
R: Zero-downtime rotation en APIM, agent reintenta con nuevo token

P: ¿OAuth2 para cada request? ¿Qué overhead?
R: Token caching (3600s TTL), overhead ~10ms por refresh

P: ¿MCP es solo para OpenAI?
R: No, Anthropic (Claude) también lo usa, es estándar abierto

P: ¿Dónde está el código?
R: github.com/rgranadosd/charlas (MIT License)
```

---

## 🎯 Stack Destacado

| Componente | Tecnología | Rol | Seguridad |
|-----------|-----------|-----|----------|
| **Orquestador** | Python 3.14 + Semantic Kernel | AI Reasoning | - |
| **Auth Usuario** | WSO2 IS + OAuth2 PKCE | Login | Token Bearer + PKCE |
| **Auth Servicio** | Client Credentials | API-to-API | Token Bearer (3600s) |
| **Gateway** | WSO2 APIM 4.6 | Proxy + Rate Limit | Bearer Token + Throttle |
| **Tools** | FastMCP + FastAPI | MCP Servers | Zod + Bearer Token |
| **e-Commerce** | Shopify Admin API 2024-01 | Productos | Token Access |
| **LLM** | OpenAI GPT-4o-mini | Reasoning | Via APIM Gateway |
| **Weather** | Open-Meteo + FastMCP | Forecasts | Libre + Rate Limit |
| **Output** | OBS + Node.js SDK | Real-time UI | Bearer Token |
| **Storage** | PostgreSQL | Sessions | TLS + Scoped Queries |

---

## 📌 Keywords para SEO

```
AI Security | OAuth2 | PKCE | API Gateway | LLM Security | Token Management
Model Context Protocol | WSO2 APIM | Rate Limiting | API Management
Shopify Integration | OpenAI Security | Production Deployment | Backend Security
Secure Architecture | Microservices | API Security | Authentication
```

---

## 🎬 Conferencias Ideales

### Tier 1 (Top Tier)
- **Spring ONE (Pivotal/VMware)** - Enterprise, API, security focus
- **Postman API Summit** - APIs, integration, best practices
- **API Days** - API management, security, standards
- **KubeCon** - Cloud-native, observability, security

### Tier 2 (Specialized)
- **OWASP AppSec** - Security, AI threats, best practices
- **PyCon** - Python, AI, architecture
- **Lambda World** - Backend, functional, AI

### Tier 3 (Community)
- **Tech Talks internos** (Shopify, OpenAI, Microsoft, Google)
- **Meetups locales** de DevOps, Python, Security

---

## 🎁 Materiales Incluidos

```
✅ Slides con diagramas Mermaid (animados)
✅ Demo script reproducible (end-to-end)
✅ Repo con código comentado (MIT License)
✅ Documentación de arquitectura (ARQUITECTURA.md)
✅ Guía de setup completa
✅ Vídeo de backup (si falla demo en vivo)
✅ Benchmark de performance
✅ Q&A document con respuestas técnicas
```

---

## 🚀 CTA Final

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

No es teoría. Es arquitectura que FUNCIONA.

Si tu AI Agent accede a APIs sensibles,
este talk te ahorra MESES de debugging.

GitHub: github.com/rgranadosd/charlas
Licencia: MIT (úsalo, modifícalo, mejóralo)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
