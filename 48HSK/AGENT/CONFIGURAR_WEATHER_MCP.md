# Configuración de Weather MCP con WSO2 APIM

Este documento explica cómo integrar el servicio Weather MCP con el agente a través de WSO2 API Manager.

## Arquitectura

```
Agente (agent_gpt4.py)
    ↓
WSO2 APIM (Gateway con OAuth2)
    ↓
Weather MCP Server (FastAPI en localhost:8080)
    ↓
Open-Meteo API (datos meteorológicos)
```

## Paso 1: Iniciar el Weather MCP Server

El servidor MCP debe estar ejecutándose antes de publicar la API en APIM:

```bash
cd /Users/rafagranados/Develop/charlas/48HSK/MCP/WEATHER
./run_weather_mcp.sh
```

Verificar que el servidor está activo:
```bash
curl -H "Authorization: Bearer weather-mcp-2026" http://localhost:8080/health
```

Deberías ver: `{"status":"ok","service":"weather_mcp"}`

## Paso 2: Crear la API en WSO2 APIM

### 2.1 Acceder al Publisher Portal

1. Navega a: https://localhost:9453/publisher
2. Login con tus credenciales de WSO2

### 2.2 Crear Nueva API REST

1. Click en "Create API" > "Import Open API"
2. O crear manualmente una API REST con estos detalles:

**Información Básica:**
- **Name**: Weather MCP
- **Context**: /weather-mcp
- **Version**: 1.0.0
- **Endpoint**: http://localhost:8080

**Recursos (Endpoints):**

```
GET  /health              - Health check
POST /mcp/tools/get_current_weather         - Clima actual
POST /mcp/tools/get_weather_forecast        - Pronóstico clima
POST /mcp/tools/get_retail_weather_insights - Insights retail
```

### 2.3 Configurar el Backend

En la sección "Endpoints":
- **Production Endpoint**: http://localhost:8080
- **Sandbox Endpoint**: http://localhost:8080

### 2.4 Configurar Seguridad

1. En la sección "API Configurations" > "Runtime":
   - **Application Level Security**: OAuth2
   - Desmarcar "API Key" si no lo necesitas

2. En "Resources", para cada recurso:
   - **Auth Type**: Application & Application User
   - **Throttling**: Unlimited (o según necesites)

### 2.5 Configurar CORS

En "API Configurations" > "Runtime" > "CORS Configuration":
- Enable CORS: ✓
- Access Control Allow Origins: *
- Access Control Allow Credentials: true
- Access Control Allow Headers: authorization, content-type, accept
- Access Control Allow Methods: GET, POST, OPTIONS

### 2.6 Publicar la API

1. Click en "Lifecycle" > "Publish"
2. La API debería estar visible en el Developer Portal

## Paso 3: Crear Aplicación y Suscribirse

### 3.1 Acceder al Developer Portal

1. Navega a: https://localhost:9453/devportal
2. Login con tus credenciales

### 3.2 Crear o Usar Aplicación Existente

Si ya tienes una aplicación (ej: "Rafa's Agent App"):
1. Ve a "Applications" > Tu aplicación
2. En la pestaña "Production Keys" o "Sandbox Keys":
   - **Consumer Key**: Copia este valor
   - **Consumer Secret**: Copia este valor

Si necesitas crear una nueva:
1. Click en "Applications" > "Add Application"
2. Nombre: "Weather MCP App"
3. Throttling Tier: Unlimited
4. Click "Save"

### 3.3 Suscribirse a la API Weather MCP

1. Ve a "APIs" > "Weather MCP"
2. Click en "Subscribe"
3. Selecciona tu aplicación
4. Selecciona el Tier (ej: Unlimited)
5. Click "Subscribe"

### 3.4 Obtener Credenciales OAuth2

En tu aplicación:
1. Ve a "Production Keys" o "Sandbox Keys"
2. Si no hay claves generadas, click en "Generate Keys"
3. **Importante**: Los scopes deben incluir:
   - `default` (para acceso general)
   - O configurar scopes personalizados en WSO2 IS

Copia:
- **Consumer Key** → `WSO2_APIM_CONSUMER_KEY`
- **Consumer Secret** → `WSO2_APIM_CONSUMER_SECRET`

## Paso 4: Configurar Variables de Entorno

Edita el archivo `.env` en la carpeta `AGENT`:

```bash
# ==========================================
# WSO2 APIM OAuth2 - Client Credentials
# ==========================================
WSO2_APIM_TOKEN_ENDPOINT=https://localhost:9453/oauth2/token
WSO2_APIM_CONSUMER_KEY=tu_consumer_key_aqui
WSO2_APIM_CONSUMER_SECRET=tu_consumer_secret_aqui

# ==========================================
# WSO2 WEATHER MCP - Servicio de Clima
# ==========================================
WSO2_WEATHER_MCP_URL=https://localhost:9453/weather-mcp/1.0.0
```

## Paso 5: Probar la Integración

### 5.1 Verificar el Token OAuth2

Puedes probar obtener un token manualmente:

```bash
# Codificar credenciales en Base64
echo -n "CONSUMER_KEY:CONSUMER_SECRET" | base64

# Obtener token
curl -k -X POST https://localhost:9453/oauth2/token \
  -H "Authorization: Basic TU9EXzNfRE9_BASE64_AQUI==" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials"
```

### 5.2 Probar Llamada a la API

Con el token obtenido:

```bash
curl -k -X POST https://localhost:9453/weather-mcp/1.0.0/tools/get_current_weather \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"params": {"city": "madrid"}}'
```

### 5.3 Ejecutar el Agente

```bash
cd /Users/rafagranados/Develop/charlas/48HSK/AGENT
python agent_gpt4.py
```

Ejemplos de consultas:
- "¿Qué tiempo hace en Madrid?"
- "Dame el pronóstico para Barcelona"
- "Qué insights de retail tengo para Valencia?"

## Troubleshooting

### Error: "No se pudo conectar al MCP Weather"

- Verifica que el servidor MCP esté ejecutándose: `curl http://localhost:8080/health`
- Verifica la URL en `.env`: `WSO2_WEATHER_MCP_URL`

### Error: "Token de autenticación inválido"

- Verifica las credenciales en `.env`
- Revisa que la aplicación esté suscrita a la API en APIM
- Obtén un nuevo token manualmente para verificar

### Error: "Sin permisos para esta operación"

- Verifica que la aplicación tenga los scopes correctos
- En WSO2 IS, revisa los roles y permisos del usuario
- Asegúrate de que la API permita "Application & Application User"

### El agente no detecta Weather Plugin

- Verifica que `WSO2_WEATHER_MCP_URL` esté configurado en `.env`
- O que `WSO2_APIM_CONSUMER_KEY` esté configurado
- Ejecuta con `--debug` para ver logs: `python agent_gpt4.py --debug`

## Funcionalidades del Weather Plugin

### 1. get_current_weather
Obtiene el clima actual de una ciudad española.

**Uso en el agente:**
- "¿Qué tiempo hace en Madrid?"
- "Cómo está el clima en Barcelona?"

### 2. get_weather_forecast
Obtiene el pronóstico del clima para los próximos días (máximo 7).

**Uso en el agente:**
- "Dame el pronóstico para Valencia"
- "¿Va a llover en Sevilla los próximos 3 días?"

### 3. get_retail_weather_insights
Obtiene insights enfocados en retail: recomendaciones de inventario y estrategias de marketing basadas en el clima.

**Uso en el agente:**
- "Dame insights de retail para Málaga"
- "¿Qué productos debería promocionar según el clima de Barcelona?"

## Ciudades Disponibles

El MCP soporta las principales ciudades españolas:

madrid, barcelona, valencia, sevilla, malaga, bilbao, zaragoza, murcia, palma, las_palmas, alicante, cordoba, valladolid, vigo, gijon, la_coruna, granada, vitoria, elche, oviedo, santa_cruz_tenerife, pamplona, almeria, san_sebastian, burgos, santander, castellon, albacete, logrono, badajoz, salamanca, huelva, lleida, tarragona, leon, cadiz, jaen, orense, lugo, caceres, melilla, ceuta

## Próximos Pasos

1. **Configurar Rate Limiting**: Ajusta los tiers en APIM según tu uso
2. **Añadir Monitoreo**: Usa WSO2 Analytics para ver el uso de la API
3. **Personalizar Permisos**: Crea roles específicos en WSO2 IS para Weather
4. **Deploy Productivo**: Configura certificados SSL válidos y endpoints públicos

## Soporte

Para issues o preguntas:
- Revisa los logs del MCP: `/Users/rafagranados/Develop/charlas/48HSK/MCP/WEATHER/`
- Revisa los logs de APIM: `/path/to/wso2am/repository/logs/`
- Ejecuta el agente con `--debug` para más información
