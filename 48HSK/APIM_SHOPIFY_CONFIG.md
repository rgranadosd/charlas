# 🛍️ Configuración APIM para Proxy Shopify

Este documento describe cómo configurar WSO2 API Manager para proxear las llamadas de Shopify.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│  Agent (agent_gpt4.py)                                          │
│  POST /shopify-admin/graphql.json                               │
│  Authorization: Bearer {APIM_TOKEN}                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  APIM Gateway (:8253)                                           │
│  ┌─────────────────────────────────────────────────────────────┐
│  │ 1. Valida Bearer token (OAuth2 Client Credentials)          │
│  │ 2. Verifica scopes (read_products, write_products)          │
│  │ 3. Rate limiting (ej: 100 req/min)                          │
│  │ 4. Logging & Monitoring                                     │
│  │ 5. Forward a Shopify con X-Shopify-Access-Token             │
│  └─────────────────────────────────────────────────────────────┘
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Shopify Admin API 2024-01                                      │
│  POST /graphql.json                                             │
│  X-Shopify-Access-Token: {SHOPIFY_API_TOKEN}                    │
└─────────────────────────────────────────────────────────────────┘
```

## Beneficios

✅ **Seguridad**: Shopify token no se expone al cliente  
✅ **Control**: Rate limiting, auditoría centralizada  
✅ **Flexibilidad**: Token rotation sin cambiar agent_gpt4.py  
✅ **Monitoreo**: Métricas y logs en APIM  
✅ **Escalabilidad**: APIM puede hacer caching, load balancing  

## Configuración en WSO2 API Manager 4.6

### 1. Crear la API en APIM

#### 1.1 Acceder a Publisher
```
https://localhost:9443/publisher
Login: admin / admin
```

#### 1.2 Crear Nueva API
- **Name:** Shopify Admin API Proxy
- **Context:** `/shopify-admin`
- **Version:** 1.0.0
- **Endpoint Type:** HTTP/REST

#### 1.3 Endpoint Configuration

**Backend Endpoint:**
```
https://rafa-ecommerce.myshopify.com/admin/api/2024-01
```

**Endpoint Settings:**
- Timeout: 30s
- Retry Count: 3
- Circuit Breaker: Enabled

### 2. Políticas (Policies)

#### 2.1 Request Interceptor Policy (Agregar Shopify Token)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sequence xmlns="http://ws.apache.org/ns/synapse" name="ShopifyAuthPolicy">
    <log level="custom">
        <property name="msg" value="=== SHOPIFY PROXY REQUEST ==="/>
        <property name="path" expression="get-property('To')"/>
        <property name="method" expression="get-property('http.request.method')"/>
    </log>
    
    <!-- Obtener Shopify token de propiedades del servidor -->
    <property name="shopify_token" value="$SHOPIFY_API_TOKEN" scope="default" type="STRING"/>
    
    <!-- Agregar header X-Shopify-Access-Token -->
    <header name="X-Shopify-Access-Token" scope="transport" action="set" value="{shopify_token}"/>
    
    <!-- Remover Authorization header del cliente (ya validado por APIM) -->
    <header name="Authorization" scope="transport" action="remove"/>
    
    <!-- Agregar User-Agent -->
    <header name="User-Agent" scope="transport" action="set" value="WSO2-APIM/4.6 ShopifyProxy/1.0"/>
    
    <!-- Logging -->
    <log level="custom">
        <property name="msg" value="Shopify headers configured"/>
        <property name="x-shopify-token-set" expression="boolean(get-property('transport', 'X-Shopify-Access-Token'))"/>
    </log>
</sequence>
```

#### 2.2 Response Interceptor Policy (Logging)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sequence xmlns="http://ws.apache.org/ns/synapse" name="ShopifyResponsePolicy">
    <log level="custom">
        <property name="msg" value="=== SHOPIFY PROXY RESPONSE ==="/>
        <property name="status" expression="get-property('http.sc')"/>
        <property name="response-time" expression="get-property('RESPONSE_TIME')"/>
    </log>
    
    <!-- Si hay error, agregar detalles -->
    <filter source="get-property('http.sc')" regex="[4-5][0-9][0-9]">
        <then>
            <log level="custom">
                <property name="error-msg" value="Shopify returned error"/>
                <property name="body" expression="get-property('MESSAGE_BODY')"/>
            </log>
        </then>
    </filter>
</sequence>
```

### 3. Scopes (OAuth2)

**Scopes requeridos para el token APIM:**
```
read_products
write_products
write_price
update_descriptions
read_orders
write_orders
```

**Configurar en APIM:**
```
APIM Developer Portal → Applications → [tu app]
→ Scopes → Agregar scopes anteriores
```

### 4. Rate Limiting

**Policy: Throttle API**
- Tier: Gold (1000 req/min)
- Stop on Quota Reach: true

```xml
<policy name="Throttle API" type="throttling">
    <quotaPolicy>
        <limit>1000</limit>
        <unit>min</unit>
        <tier>Gold</tier>
    </quotaPolicy>
</policy>
```

### 5. Validar Bearer Token (OAuth2)

**Policy: OAuth2 Mandatory**
```xml
<policy name="OAuth2" type="authentication">
    <oauth2>
        <required>true</required>
        <scopes>read_products,write_products</scopes>
    </oauth2>
</policy>
```

### 6. Publish API

1. **Pre-release:** Test en Dev → Staging
2. **Release:** Prod with versioning

```
Context: /shopify-admin/v1
Version: 1.0.0
```

## Endpoints Disponibles

Una vez publicada, los endpoints serán accesibles en:

```
GET  https://localhost:8253/shopify-admin/v1/products.json
GET  https://localhost:8253/shopify-admin/v1/products/{id}.json
POST https://localhost:8253/shopify-admin/v1/products.json
PUT  https://localhost:8253/shopify-admin/v1/products/{id}.json
DELETE https://localhost:8253/shopify-admin/v1/products/{id}.json

POST https://localhost:8253/shopify-admin/v1/graphql.json
```

## Ejemplo de Uso en Agent

```python
def _api(self, method, path, data=None):
    # Token APIM (Client Credentials)
    apim_token = self._get_apim_token()
    
    # APIM Gateway URL
    apim_gateway = os.getenv("APIM_GATEWAY_URL", "https://localhost:8253")
    url = f"{apim_gateway}/shopify-admin{path}"
    
    headers = {
        "Authorization": f"Bearer {apim_token}",
        "Content-Type": "application/json"
    }
    
    # APIM hace el proxy y agrega X-Shopify-Access-Token automáticamente
    response = requests.get(url, headers=headers, verify=False)
    return response.json()

# Uso:
# GET /shopify-admin/v1/products.json
products = self._api("GET", "/products.json")

# POST /shopify-admin/v1/graphql.json
query = {
    "query": """
        query {
            products(first: 10) {
                edges {
                    node {
                        id
                        title
                        totalInventory
                    }
                }
            }
        }
    """
}
graphql_result = self._api("POST", "/graphql.json", data=query)
```

## Troubleshooting

### Error 401: Bearer token inválido
```
Solución: Verificar que _get_apim_token() está usando credenciales correctas
- WSO2_CONSUMER_KEY
- WSO2_CONSUMER_SECRET
- WSO2_TOKEN_ENDPOINT
```

### Error 403: Sin permisos
```
Solución: Verificar scopes en token APIM
- read_products ✓
- write_products ✓
- update_descriptions ✓
```

### Error 504: Gateway Timeout
```
Solución: 
1. Verificar conectividad a Shopify
2. Aumentar timeout en APIM (endpoint settings)
3. Verificar Shopify API rate limits (40 req/s)
```

### Shopify regresa 422: Invalid GraphQL query
```
Solución:
1. Validar sintaxis GraphQL (schema en Shopify admin)
2. Verificar que campos existen en API 2024-01
3. Consultar: https://shopify.dev/api/admin-graphql/2024-01
```

## Monitoreo

### Métricas en APIM

1. **Dashboard → API Analytics**
   - Req/sec por endpoint
   - Error rate
   - Response time p50, p95, p99

2. **Logs**
   ```bash
   tail -f /wso2am-4.6.0/repository/logs/wso2carbon.log | grep "shopify"
   ```

3. **Alerts**
   - Error rate > 5%
   - Response time > 2s
   - Quota exceeded

## Variables de Entorno

```bash
# .env del Agent
APIM_GATEWAY_URL=https://localhost:8253
WSO2_TOKEN_ENDPOINT=https://localhost:9453/oauth2/token
WSO2_CONSUMER_KEY=shopify_proxy_app_key
WSO2_CONSUMER_SECRET=shopify_proxy_app_secret
SHOPIFY_API_TOKEN=shpat_xxxxxxxxxxxxx

# .env del APIM (si se configura como property)
SHOPIFY_API_TOKEN=shpat_xxxxxxxxxxxxx
```

## Seguridad

✅ **Rotación de tokens:** Solo cambiar SHOPIFY_API_TOKEN en APIM  
✅ **Auditoría:** Todos los requests quedan logueados en APIM  
✅ **Rate limiting:** Protege contra abuse  
✅ **OAuth2 Client Credentials:** Mutual TLS (mTLS) en prod  
✅ **IP Whitelisting:** Restricción de IPs que pueden llamar (opcional)

## Referencias

- [WSO2 APIM 4.6 Docs](https://apim.docs.wso2.com/en/4.6.0/)
- [Shopify Admin API](https://shopify.dev/api/admin-graphql/2024-01)
- [OAuth2 Client Credentials](https://oauth.net/2/grant-types/client-credentials/)
