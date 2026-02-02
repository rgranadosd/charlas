# MCP Weather Server (Open-Meteo)

## ¿Qué es este servidor MCP?
Este servidor MCP (Model Context Protocol) proporciona información meteorológica en tiempo real y previsiones para ciudades españolas, usando la API pública de Open-Meteo. Está diseñado para integrarse con agentes LLM (Modelos de Lenguaje) que toman decisiones en e-commerce, retail y logística basadas en el clima.

## Ciudades soportadas
Actualmente puedes consultar el tiempo para:
- Madrid
- Barcelona
- Valencia
- Sevilla
- Zaragoza
- Málaga
- Murcia
- Bilbao
- Alicante
- Córdoba
- Burgos
- La Coruña

## Herramientas expuestas (MCP Tools)
El servidor expone las siguientes herramientas para el agente LLM:

### 1. get_current_weather
Obtiene el tiempo actual para una ciudad española.
- **Parámetros:**
  - `city`: (str) Ciudad (ver lista arriba)
  - `response_format`: (str) "markdown" o "json"
- **Ejemplo de uso:**
```json
{
  "city": "Madrid",
  "response_format": "markdown"
}
```

### 2. get_weather_forecast
Obtiene la previsión meteorológica para los próximos días en una ciudad.
- **Parámetros:**
  - `city`: (str) Ciudad
  - `days`: (int) Número de días (1-7)
  - `response_format`: (str) "markdown" o "json"

## ¿Cómo influye el clima en las decisiones del agente LLM?
El agente LLM utiliza la información meteorológica para:
- **Gestión de inventario:**
  - Si se prevé lluvia, prioriza productos impermeables, paraguas, botas, etc.
  - Si hay calor, prioriza ropa ligera, aire acondicionado, ventiladores.
  - Si hay frío, prioriza abrigos, calefactores, mantas.
- **Optimización logística:**
  - Ajusta rutas y tiempos de entrega según condiciones adversas (lluvia, nieve, viento).
  - Recomienda stock extra en ciudades con previsión de mal tiempo.
- **Estrategias de marketing:**
  - Lanza campañas promocionales de productos relevantes según el clima.
  - Personaliza banners y recomendaciones en la web según el tiempo local.

## Ejemplo de flujo de decisión
1. El agente consulta el tiempo actual y la previsión para Madrid.
2. Detecta que habrá lluvia los próximos 3 días.
3. Recomienda aumentar el stock de paraguas y chubasqueros en almacenes de Madrid.
4. Sugiere una campaña de marketing de "Vístete para la lluvia".
5. Ajusta las rutas de reparto para evitar zonas con riesgo de inundación.

## ¿Cómo consultar desde el Inspector MCP?
1. Ejecuta el servidor con el script `setup_and_run_weather_mcp.sh`.
2. Abre la interfaz web del Inspector MCP.
3. Selecciona la herramienta deseada (por ejemplo, `get_current_weather`).
4. Introduce los parámetros y pulsa "Run".

## Ampliar ciudades
Para añadir más ciudades, edita el diccionario `SPANISH_CITIES` y el enum `SpanishCity` en el archivo `weather_mcp_openmeteo.py`.

## API utilizada
- [Open-Meteo](https://open-meteo.com/): API pública, sin límite de llamadas ni necesidad de API key.

## Modo SSE (Server-Sent Events) para WSO2 y Web

Este servidor MCP también puede ejecutarse como un servidor web compatible con transporte SSE, necesario para integraciones con WSO2 y otros clientes web.

### ¿Cómo lanzar el servidor en modo SSE?

Ejecuta:
```sh
python3 weather_mcp_openmeteo.py sse
```
Esto levantará un servidor FastAPI en el puerto 8080 con el endpoint `/mcp`.

- Endpoint: `POST /mcp`
- Puerto: `8080`
- Transporte: Server-Sent Events (SSE)

### ¿Para qué sirve el modo SSE?
Permite que WSO2 y otros sistemas web reciban respuestas MCP en tiempo real mediante eventos SSE, en vez de stdio.

### ¿Cómo probarlo?
Puedes enviar una petición POST a `http://localhost:8080/mcp` con el JSON MCP y recibirás los resultados por SSE.

Ejemplo con `curl`:
```sh
curl -N -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"city": "Madrid", "response_format": "markdown"}'
```

---

**Este servidor MCP es modular y puede integrarse fácilmente con cualquier agente LLM que soporte el protocolo MCP.**

## Ejecución robusta para WSO2 y desarrollo

Para depuración visual (Inspector MCP):
```sh
./run_weather_mcp.sh inspect
```
Esto lanza el Inspector MCP en modo stdio para pruebas locales y debugging humano.

Para integración con WSO2 o clientes HTTP/SSE (recomendado):
```sh
./run_weather_mcp.sh serve
```
Esto lanza el servidor MCP en modo HTTP/SSE usando uvicorn directamente sobre la app ASGI de FastMCP, escuchando en todas las interfaces (host=0.0.0.0, puerto 8080).

- Endpoint SSE para WSO2: `http://<tu-ip>:8080/sse`

**Importante:** El Inspector MCP solo sirve para depuración visual y no expone el endpoint HTTP/SSE requerido por WSO2. Para producción/integración, usa el modo `serve` que garantiza compatibilidad y control total de host/puerto.
