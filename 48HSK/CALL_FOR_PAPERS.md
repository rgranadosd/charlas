# 🎤 Call for Papers - Propuestas de Temas

## Propuesta Principal

### 📌 Título
**"Securización de Agentes de IA Multi-Componente: Orquestación Segura con OAuth2, API Gateways y Model Context Protocol en Arquitecturas Modernas"**

#### Subtítulo (Opcional)
*De la teoría a la práctica: Cómo proteger un AI Agent que integra e-commerce, APIs externas y streaming en tiempo real*

---

## Resumen Ejecutivo (Abstract)

### Versión Corta (150 palabras)

```
Los agentes de IA modernos requieren acceso seguro a múltiples servicios: 
APIs externas, bases de datos, plataformas e-commerce y herramientas con UI 
en vivo. Este talk presenta una arquitectura production-ready que demuestra 
cómo orquestar de forma segura un AI Agent que integra Shopify, OpenAI, 
Weather APIs y sincronización en vivo con OBS Studio.

Exploraremos patrones de seguridad críticos:
- OAuth2 con PKCE para autenticación de usuarios
- Client Credentials para comunicación servicio-a-servicio
- API Gateway (WSO2) para rate limiting y auditoría centralizada
- Model Context Protocol (MCP) para integración segura de herramientas
- Token management, refresh flows y rotación de secretos

Con demostraciones en vivo de cómo el AI Agent recomienda productos 
basado en datos del clima, actualiza la interfaz OBS en tiempo de ejecución,
todo validado a través de múltiples capas de seguridad.
```

### Versión Extendida (300 palabras)

```
Los agentes de IA están revolucionando cómo interactuamos con aplicaciones, 
pero introducen desafíos críticos de seguridad: ¿cómo permitimos que un LLM 
acceda a datos sensibles sin exponerlos? ¿Cómo auditamos y controlamos cada 
llamada? ¿Cómo escalamos esto en producción?

Esta sesión presenta una solución real que combina:

1. **Autenticación Multi-Capa:**
   - OAuth2 Authorization Code + PKCE para usuarios finales
   - Client Credentials para APIs internas y herramientas
   - Token caching y refresh automático con manejo de expiración

2. **API Gateway como Control Point:**
   - WSO2 API Manager como proxy centralizado
   - Rate limiting per-API y per-usuario
   - Analytics, logging y detección de anomalías
   - Routing inteligente de requests

3. **Model Context Protocol (MCP):**
   - Framework seguro para conectar herramientas a LLMs
   - Validación de schemas con Zod
   - Aislamiento de permisos por herramienta
   - Integración directa con UI (OBS Studio)

4. **Caso de Uso Real:**
   - AI Agent recomienda productos Shopify basado en weather forecast
   - Integración con OpenAI GPT-4o-mini para reasoning
   - Actualizaciones en vivo de OBS Studio mientras el agent procesa
   - Todo validado a través de capas de seguridad

5. **Stack Tecnológico:**
   - Python + Semantic Kernel para orquestación
   - FastAPI + FastMCP para servidores de herramientas
   - WSO2 Identity Server + API Manager para seguridad
   - PostgreSQL para persistencia de sesiones

Demostraremos patrones replicables: cómo manejar tokens expirables, 
cómo implementar circuit breakers, cómo auditar accesos, y cómo debuggear 
flujos complejos sin exponer credenciales en logs.

Perfecto para: arquitectos, security engineers, backend developers 
que construyen aplicaciones IA en producción.
```

---

## Temas Alternativos

### Opción 2️⃣
**"OAuth2 en la Era de los Agentes de IA: Patrones de Seguridad para Multi-Servicio Orchestration"**

- Enfoque: OAuth2, autenticación distribuida
- Tiempo: 45 min
- Nivel: Intermedio-Avanzado

### Opción 3️⃣
**"API Gateway como Control Plane de Seguridad: Rate Limiting, Auditoría y Protección de Agentes LLM"**

- Enfoque: API Management, WSO2 APIM
- Tiempo: 60 min
- Nivel: Avanzado

### Opción 4️⃣
**"Model Context Protocol: Estándar Abierto para Integración Segura de Herramientas en Agentes de IA"**

- Enfoque: MCP, integración de tools, protocolo
- Tiempo: 40 min
- Nivel: Intermedio

### Opción 5️⃣
**"De Demo a Producción: Arquitectura de Seguridad para AI Agents que Acceden a e-Commerce, APIs Externas y Datos Sensibles"**

- Enfoque: Arquitectura completa, lessons learned
- Tiempo: 60 min
- Nivel: Intermedio-Avanzado

---

## Estructura de la Presentación (Principal)

### Acto 1: El Problema (10 min)
```
❌ Problema inicial:
   - Usuario: "Quiero un asistente que recomiende productos en tiempo real"
   - Desafío: El LLM necesita acceso a Shopify, Weather, OpenAI, OBS...
   - Pregunta: ¿Cómo hacerlo de forma SEGURA en producción?

⚠️ Riesgos:
   - Exposición de credenciales en logs/traces
   - Acceso no auditado a APIs sensibles
   - Token expirados causando fallos silenciosos
   - Rate limiting de servicios externos
   - Inyección de prompts maliciosos
```

### Acto 2: La Solución (35 min)

#### 2.1 Autenticación (10 min)
```
🔐 OAuth2 PKCE para usuarios:
   ┌─────────┐    Authorization Code    ┌──────────────┐
   │ Usuario │◄──────────────────────────┤ WSO2 IS 7.1  │
   └─────────┘      + Token Refresh      └──────────────┘

🔐 Client Credentials para servicios:
   ┌────────────┐    Bearer Token    ┌──────────────┐
   │ AI Agent   │◄──────────────────┤ APIM Token   │
   │ MCP Tools  │    (3600s TTL)     │ Service      │
   └────────────┘                    └──────────────┘

🔄 Token Management:
   - Caching automático
   - Refresh antes de expiración
   - Manejo de errores 401/403
```

#### 2.2 API Gateway (10 min)
```
🌐 WSO2 API Manager como Control Point:

   ┌────────────┐
   │ AI Agent   │
   └─────┬──────┘
         │ Request
         ▼
   ┌──────────────────────────┐
   │ APIM Gateway (:8253)     │
   ├──────────────────────────┤
   │ ✓ Valida Bearer Token    │
   │ ✓ Rate Limit (100 req/m) │
   │ ✓ Logging + Analytics    │
   │ ✓ Circuit Breaker        │
   │ ✓ Request Transformation │
   └────────┬─────────────────┘
            │ Forward
            ▼
   ┌────────────────────┐
   │ Shopify / OpenAI   │
   └────────────────────┘
```

#### 2.3 Model Context Protocol (10 min)
```
🔌 MCP: Estándar para integrar tools de forma segura

Weather MCP:
├─ Tool: get_weather(city)
├─ Schema: {city: string, days: 1-7}
├─ Autenticación: Bearer Token
├─ Rate Limit: 10 req/min
└─ Auditoría: Cada call loguea (user, timestamp, params)

OBS MCP:
├─ Tool: setObsText(inputName, text)
├─ Schema: Validación Zod
├─ Aislamiento: No permite acceso a sources sensibles
└─ Scopes: ["write_scene_items"]
```

### Acto 3: Demo en Vivo (10 min)
```
🎬 Escenario: Recomendación de productos basada en clima

Usuario ejecuta:
$ ./start_demo.sh --city Barcelona --products 50

Proceso:
1. ✅ OAuth2 PKCE login (Bearer token guardado)
2. ✅ Request token APIM (Client Credentials)
3. ✅ Weather MCP: "¿Qué clima en Barcelona?" (25°C, sin lluvia)
4. ✅ Shopify API: "Dame 50 productos"
5. ✅ OpenAI GPT-4o-mini: "Recomienda 8 productos para 25°C"
6. ✅ OBS MCP: Actualiza rótulo con cada recomendación
7. ✅ Vista en vivo en OBS Studio (rótulo actualizado)

Output visible:
- CLI mostrando flujo de autenticación
- OBS Studio actualizándose con cada producto recomendado
- Logs centralizados en APIM con auditoría
```

### Acto 4: Lecciones Aprendidas (5 min)
```
📚 Lecciones Aprendidas:

1. OAuth2 es tu amigo:
   ✓ PKCE para apps mobile/desktop
   ✓ Client Credentials para backend-to-backend
   ✓ Refresh tokens para users
   ✗ Nunca guardes secrets en logs

2. API Gateway no es opcional:
   ✓ Centraliza auditoría
   ✓ Protege contra abuse
   ✓ Simplifica rotación de tokens
   ✗ No intentes hacer esto sin él

3. MCP es el estándar:
   ✓ Escala a múltiples tools
   ✓ Validación de schemas
   ✓ Aislamiento de permisos
   ✗ No hardcodees endpoints

4. Monitoreo es crítico:
   ✓ Alerta si error rate > 5%
   ✓ Alerta si latencia > 2s
   ✓ Alerta si quota exceeded
   ✗ No esperes hasta el crash
```

---

## Stack Técnico Destacado

| Capa | Tecnología | Propósito | Seguridad |
|------|-----------|----------|-----------|
| **Orquestación** | Python 3.14 + Semantic Kernel 1.37.0 | AI Agent | - |
| **LLM** | OpenAI GPT-4o-mini | Reasoning | Token Bearer + Rate Limit |
| **Autenticación** | WSO2 Identity Server 7.1 | OAuth2 + OIDC | PKCE, mTLS |
| **API Gateway** | WSO2 API Manager 4.6 | Proxy + Rate Limit | Bearer Token, Throttling |
| **Tools** | FastMCP + FastAPI | MCP Servers | Zod Validation, Logging |
| **e-Commerce** | Shopify Admin API 2024-01 | Product Data | Token Access |
| **Weather** | Open-Meteo + FastMCP | Forecast | Rate Limit |
| **Streaming** | OBS + Node.js SDK | Real-time Output | WebSocket Token |
| **Persistencia** | PostgreSQL | Sessions + Cache | TLS, Scoped Queries |

---

## Público Objetivo

✅ **Arquitectos de Software** que diseñan sistemas IA  
✅ **Security Engineers** que auditan aplicaciones LLM  
✅ **Backend Developers** que implementan agentes en producción  
✅ **DevOps** que mantienen infraestructura de IA  
✅ **Product Managers** que entienden trade-offs seguridad vs UX  

---

## Puntos de Diferenciación

🎯 **No es teórico**: Todo demostrado con código real en vivo  
🎯 **Replicable**: Los patrones funcionan en cualquier AI Agent  
🎯 **Production-ready**: Maneja errores, tokens expirados, rate limits  
🎯 **Open source**: Todo código disponible en GitHub  
🎯 **Multi-servicio**: Muestra integración real de múltiples APIs  

---

## Conferencias Ideales

- **Spring ONE** (VMware/Pivotal): Enterprise, seguridad, API management
- **PyCon**: Python, AI, arquitectura
- **OWASP AppSec**: Seguridad en aplicaciones IA
- **KubeCon**: Cloud-native, API gateway, observability
- **Postman**: APIs, integración, documentación
- **API Days**: API Management, OAuth, rate limiting
- **Lambda World**: Functional programming, AI, backend
- **Tech Talks de empresas**: Shopify, OpenAI, WSO2

---

## Keywords para SEO/Marketing

`AI Security` `OAuth2` `PKCE` `API Gateway` `Model Context Protocol` 
`LLM Integration` `Shopify API` `WSO2` `Rate Limiting` `Token Management` 
`Production Deployment` `e-Commerce` `Real-time Streaming` `OpenAI`
`API Management` `Semantic Kernel` `FastAPI` `Security Best Practices`

---

## Materiales a Preparar

- [ ] Slides con diagramas (Mermaid)
- [ ] Demo script completo
- [ ] Repo con código limpio y comentado
- [ ] Documento de arquitectura (ARQUITECTURA.md)
- [ ] Guía de setup para reproducir
- [ ] Vídeo de backup (si fail la demo en vivo)
- [ ] Q&A preparadas sobre seguridad
- [ ] Benchmark de latencia/throughput

---

## Tiempo Estimado

| Formato | Duración | Estructura |
|---------|----------|-----------|
| **Charla Corta** | 30 min | Problema (5) + OAuth2 (8) + Gateway (8) + Demo (7) + Q&A (2) |
| **Charla Standard** | 45 min | Igual + MCP (7) + Lessons (5) |
| **Workshop** | 120 min | Charla 45 min + Hands-on coding 60 min + Q&A 15 min |

---

## Hook de Apertura (First 30 seconds)

```
"Hace 6 meses alguien me pidió: 
 'Quiero un bot que lea el clima y me recomiende ropa.'
 
Suena simple. Pero en realidad preguntaban:
 '¿Cómo permito que un LLM acceda a datos sensibles sin exponerlos?
  ¿Cómo audito cada llamada?
  ¿Cómo lo escalo en producción?'
  
Hoy vamos a ver cómo construí eso usando OAuth2, API Gateways 
y Model Context Protocol.

Y sí, va a haber explosiones en vivo. A través de OBS. En directo."
```

---

## Call to Action Final

```
Este talk no es sobre teoría de seguridad.
Es sobre patrones que FUNCIONAN.

Saldrás con:
✅ Una arquitectura replicable
✅ Código production-ready
✅ Respuestas a preguntas que te harán tus users
✅ Confianza de que tu AI Agent es seguro

GitHub: github.com/rgranadosd/charlas
```
