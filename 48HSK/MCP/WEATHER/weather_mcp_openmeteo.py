#!/usr/bin/env python3
"""
Weather MCP Server for Spanish Fashion Retail (Open-Meteo Version)

This MCP server provides weather forecasting capabilities for Spanish cities,
designed to help e-commerce agents make data-driven decisions about inventory,
pricing, and marketing strategies based on weather conditions.

Uses Open-Meteo API (no API key required, unlimited calls, better for Spain)

Author: Demo for Fashion Retail Agent
"""

import json
import logging
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.applications import Starlette
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
# El transporte stdio del MCP es sensible a ruido en salida; además, el Inspector
# marca cualquier salida en stderr como "Error output" aunque sea INFO.
# Forzamos un nivel más alto para evitar logs informativos del framework.
_LOG_LEVEL = os.getenv("WEATHER_MCP_LOG_LEVEL", "INFO").upper()  # Cambio temporal a INFO para debugging
logging.basicConfig(
    level=getattr(logging, _LOG_LEVEL, logging.INFO),
    force=True,
)
logging.getLogger("mcp").setLevel(getattr(logging, _LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)


# Initialize FastMCP server
# APIM 4.6 necesita validar la URL antes de conectar
mcp = FastMCP(
    "weather_mcp", 
    host="0.0.0.0", 
    port=8080,
    streamable_http_path="/mcp"
)

# Get the underlying Starlette app - streamable_http_app() returns a Starlette app
# with MCP endpoints already configured
original_app = mcp.streamable_http_app()

# Primero agregamos middleware CORS y logging a la app original
# Update CORS middleware to include specific APIM domain
# Based on FastAPI docs: when using credentials, cannot use "*" wildcard
original_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Keep wildcard for now, but ensure credentials are handled
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS for preflight
    allow_headers=["*"],
)

# Add logging middleware to debug incoming requests
@original_app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")  # Log all headers for debugging
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Add health check endpoint to the app
@original_app.route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for WSO2."""
    from starlette.responses import JSONResponse
    return JSONResponse({"status": "ok", "service": "weather_mcp"})

# Bearer Token para WSO2 MCP Playground
MCP_BEARER_TOKEN = "weather-mcp-2026"

# Bearer Token middleware - placed AFTER CORS to allow preflight requests
@original_app.middleware("http")
async def verify_bearer_token(request, call_next):
    """Middleware Bearer Token para WSO2"""
    # Skip token verification for OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        return await call_next(request)
    
    # Skip token verification for health endpoint
    if request.url.path == "/health":
        return await call_next(request)
    
    auth = request.headers.get("authorization")
    
    # Aceptar CUALQUIER Bearer token (APIM ya validó la autenticación)
    # Esto permite que APIM envíe su propio token OAuth2/JWT
    if auth and auth.startswith("Bearer "):
        return await call_next(request)
    
    return JSONResponse(
        {"error": "Bearer token required"},
        status_code=401
    )

# ASGI Middleware Wrapper para inyectar Accept header ANTES de que FastMCP lo valide
# Esto intercepta a nivel ASGI antes de que Starlette procese el request
class ASGIAcceptHeaderWrapper:
    """
    ASGI middleware que inyecta el Accept header correcto.
    Se ejecuta ANTES de cualquier middleware de Starlette o validación de FastMCP.
    """
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        logger.info(f"🎯 ASGI Wrapper ejecutándose: type={scope.get('type')}, path={scope.get('path')}")
        
        if scope["type"] == "http" and scope["path"] == "/mcp":
            # Obtener headers actuales
            headers = dict(scope.get("headers", []))
            accept_header = headers.get(b"accept", b"").decode("latin1")
            
            logger.info(f"🔍 Accept header original: '{accept_header}'")
            
            # Si no tiene ambos tipos requeridos, inyectar el correcto
            if "application/json" not in accept_header or "text/event-stream" not in accept_header:
                logger.warning(f"🔧 ASGI Wrapper: Accept header incorrecto: '{accept_header}' - Inyectando el correcto")
                
                # Modificar headers en scope ANTES de pasar a la app
                new_headers = []
                for name, value in scope.get("headers", []):
                    if name.lower() != b"accept":
                        new_headers.append((name, value))
                
                # Agregar el Accept header correcto
                new_headers.append((b"accept", b"application/json, text/event-stream"))
                scope["headers"] = new_headers
                
                logger.info(f"✅ Accept header inyectado correctamente")
        
        # Pasar el scope modificado a la aplicación original
        await self.app(scope, receive, send)

# Envolver la app de FastMCP con nuestro wrapper ASGI
app_instance = ASGIAcceptHeaderWrapper(original_app)

# Export for uvicorn
asgi_app = app_instance

# Verificar que el wrapper está en su lugar
print(f"✅ ASGI app configurada: {type(asgi_app).__name__}")
print(f"✅ Wrapper activo: {isinstance(asgi_app, ASGIAcceptHeaderWrapper)}")

# Open-Meteo API Configuration
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Spanish cities with coordinates
SPANISH_CITIES = {
    "Madrid": {"lat": 40.4168, "lon": -3.7038},
    "Barcelona": {"lat": 41.3874, "lon": 2.1686},
    "Valencia": {"lat": 39.4699, "lon": -0.3763},
    "Sevilla": {"lat": 37.3891, "lon": -5.9845},
    "Zaragoza": {"lat": 41.6488, "lon": -0.8891},
    "Málaga": {"lat": 36.7213, "lon": -4.4213},
    "Murcia": {"lat": 37.9922, "lon": -1.1307},
    "Bilbao": {"lat": 43.2627, "lon": -2.9253},
    "Alicante": {"lat": 38.3452, "lon": -0.4810},
    "Córdoba": {"lat": 37.8882, "lon": -4.7794},
    "Burgos": {"lat": 42.3439, "lon": -3.6969},
    "La Coruña": {"lat": 43.3623, "lon": -8.4115},
}

# WMO Weather interpretation codes
# https://open-meteo.com/en/docs
WMO_CODES = {
    0: "Clear",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail",
}


class ResponseFormat(str, Enum):
    """Output format options for weather data."""
    MARKDOWN = "markdown"
    JSON = "json"


class SpanishCity(str, Enum):
    """Major Spanish cities for weather forecasting."""
    MADRID = "Madrid"
    BARCELONA = "Barcelona"
    VALENCIA = "Valencia"
    SEVILLA = "Sevilla"
    ZARAGOZA = "Zaragoza"
    MALAGA = "Málaga"
    MURCIA = "Murcia"
    BILBAO = "Bilbao"
    ALICANTE = "Alicante"
    CORDOBA = "Córdoba"
    BURGOS = "Burgos"
    LA_CORUNA = "La Coruña"


# ============================================================================
# Input Models
# ============================================================================

class GetCurrentWeatherInput(BaseModel):
    """Input parameters for getting current weather."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    city: SpanishCity = Field(
        ...,
        description="Spanish city to get weather for (e.g., 'Barcelona', 'Madrid')"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


class GetForecastInput(BaseModel):
    """Input parameters for getting weather forecast."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    city: SpanishCity = Field(
        ...,
        description="Spanish city to get forecast for (e.g., 'Barcelona', 'Madrid')"
    )
    days: int = Field(
        default=5,
        description="Number of days to forecast (1-7)",
        ge=1,
        le=7
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


class GetRetailInsightsInput(BaseModel):
    """Input parameters for getting retail-focused weather insights."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    city: SpanishCity = Field(
        ...,
        description="Spanish city to analyze (e.g., 'Barcelona', 'Madrid')"
    )
    days: int = Field(
        default=3,
        description="Number of days to analyze (1-7)",
        ge=1,
        le=7
    )


# ============================================================================
# Helper Functions
# ============================================================================

def _handle_api_error(e: Exception) -> str:
    """Consistent error formatting for all weather API calls."""
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 400:
            return "Error: Invalid request parameters. Please check city coordinates."
        elif e.response.status_code == 429:
            return "Error: Too many requests. Please wait a moment."
        return f"Error: Weather API request failed with status {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. Please try again."
    elif isinstance(e, KeyError):
        return f"Error: City not found in database: {str(e)}"
    return f"Error: Unexpected error occurred: {type(e).__name__}: {str(e)}"


def _get_weather_emoji(wmo_code: int) -> str:
    """Get emoji representation of weather condition from WMO code."""
    if wmo_code == 0 or wmo_code == 1:
        return "☀️"
    elif wmo_code == 2 or wmo_code == 3:
        return "☁️"
    elif 45 <= wmo_code <= 48:
        return "🌫️"
    elif 51 <= wmo_code <= 67:
        return "🌧️"
    elif 71 <= wmo_code <= 77:
        return "❄️"
    elif 80 <= wmo_code <= 82:
        return "🌦️"
    elif 85 <= wmo_code <= 86:
        return "🌨️"
    elif wmo_code >= 95:
        return "⛈️"
    return "🌤️"


def _wmo_to_condition(wmo_code: int) -> str:
    """Convert WMO code to weather condition string."""
    return WMO_CODES.get(wmo_code, "Unknown")


def _is_rainy_condition(wmo_code: int) -> bool:
    """Check if WMO code represents rainy conditions."""
    # Drizzle, rain, freezing rain, rain showers
    return (51 <= wmo_code <= 67) or (80 <= wmo_code <= 82) or (wmo_code >= 95)


def _analyze_retail_impact(temp: float, wmo_code: int, precipitation: float) -> Dict[str, Any]:
    """
    Analyze weather data to provide fashion retail insights.
    
    Returns recommendations for:
    - Products to promote
    - Pricing suggestions
    - Marketing opportunities
    - Inventory redistribution
    - Logistics optimization
    """
    
    recommendations = {
        "temperature_range": "cold" if temp < 15 else "moderate" if temp < 25 else "hot",
        "precipitation": precipitation > 0 or _is_rainy_condition(wmo_code),
        "suggested_products": [],
        "pricing_opportunities": [],
        "marketing_angles": [],
        "inventory_actions": [],
        "logistics_optimization": []
    }
    
    # Temperature-based recommendations
    if temp < 10:
        recommendations["suggested_products"].extend([
            "Abrigos de invierno",
            "Bufandas y guantes",
            "Jerseys gruesos"
        ])
        recommendations["pricing_opportunities"].append(
            "Subir precios de ropa de abrigo (+10-15%)"
        )
        recommendations["inventory_actions"].extend([
            "Aumentar stock de ropa de invierno en almacén local",
            "Reducir exposición de ropa de verano en tienda"
        ])
        recommendations["logistics_optimization"].extend([
            "Redirigir abrigos desde regiones cálidas a esta ubicación",
            "Preparar envíos prioritarios de productos térmicos"
        ])
    elif temp < 20:
        recommendations["suggested_products"].extend([
            "Chaquetas ligeras",
            "Jerseys finos",
            "Pantalones largos"
        ])
        recommendations["inventory_actions"].append(
            "Mantener stock equilibrado de entretiempo"
        )
    else:
        recommendations["suggested_products"].extend([
            "Camisetas de manga corta",
            "Pantalones cortos",
            "Vestidos ligeros",
            "Sandalias"
        ])
        recommendations["pricing_opportunities"].append(
            "Promocionar ropa de verano"
        )
        recommendations["inventory_actions"].extend([
            "Devolver abrigos a almacén central (baja demanda)",
            "Aumentar stock de ropa ligera en tienda física"
        ])
        recommendations["logistics_optimization"].extend([
            "Redirigir ropa de verano desde regiones frías",
            "Enviar stock sobrante de abrigos a zonas más frías"
        ])
    
    # Precipitation-based recommendations
    if _is_rainy_condition(wmo_code) or precipitation > 0:
        recommendations["suggested_products"].extend([
            "Impermeables y chubasqueros",
            "Botas de agua",
            "Paraguas"
        ])
        recommendations["pricing_opportunities"].extend([
            "Subir precios de impermeables (+15-20%)",
            "Destacar botas de agua en homepage"
        ])
        recommendations["marketing_angles"].append(
            "Campaña 'Protegido de la lluvia' con productos impermeables"
        )
        recommendations["inventory_actions"].extend([
            "Aumentar stock de productos impermeables urgentemente",
            "Preparar paraguas para venta rápida en puntos de venta"
        ])
        recommendations["logistics_optimization"].append(
            "Envío express de impermeables desde almacén central si stock local bajo"
        )
    
    # Clear/sun conditions
    condition_name = _wmo_to_condition(wmo_code)
    if "Clear" in condition_name and temp > 20:
        recommendations["marketing_angles"].append(
            "Promoción 'Días de sol' con gafas de sol y ropa ligera"
        )
    
    return recommendations


def _format_current_weather_markdown(city: str, data: Dict[str, Any]) -> str:
    """Format current weather data as markdown."""
    current = data.get("current", {})
    temp = current.get("temperature_2m", 0)
    feels_like = current.get("apparent_temperature", temp)
    humidity = current.get("relative_humidity_2m", 0)
    wind = current.get("wind_speed_10m", 0)
    precipitation = current.get("precipitation", 0)
    wmo_code = current.get("weather_code", 0)
    
    condition = _wmo_to_condition(wmo_code)
    emoji = _get_weather_emoji(wmo_code)
    
    output = f"""# Tiempo Actual en {city} {emoji}

## Condiciones
- **Estado**: {condition}
- **Temperatura**: {temp}°C
- **Sensación térmica**: {feels_like}°C
- **Humedad**: {humidity}%
- **Viento**: {wind} km/h
"""
    
    if precipitation > 0:
        output += f"- **Precipitación**: {precipitation} mm\n"
    
    return output


def _format_forecast_markdown(city: str, data: Dict[str, Any], days: int) -> str:
    """Format forecast data as markdown."""
    daily = data.get("daily", {})
    dates = daily.get("time", [])[:days]
    temp_max = daily.get("temperature_2m_max", [])[:days]
    temp_min = daily.get("temperature_2m_min", [])[:days]
    precipitation = daily.get("precipitation_sum", [])[:days]
    wmo_codes = daily.get("weather_code", [])[:days]
    
    output = f"# Previsión del Tiempo para {city}\n\n"
    
    for i in range(min(days, len(dates))):
        date = dates[i]
        t_max = temp_max[i] if i < len(temp_max) else 0
        t_min = temp_min[i] if i < len(temp_min) else 0
        precip = precipitation[i] if i < len(precipitation) else 0
        wmo = wmo_codes[i] if i < len(wmo_codes) else 0
        
        condition = _wmo_to_condition(wmo)
        emoji = _get_weather_emoji(wmo)
        avg_temp = round((t_max + t_min) / 2, 1)
        
        output += f"## {date} {emoji}\n"
        output += f"- **Condición predominante**: {condition}\n"
        output += f"- **Temperatura**: {t_min}°C - {t_max}°C (media: {avg_temp}°C)\n"
        
        if precip > 0:
            output += f"- **Lluvia esperada**: {round(precip, 1)} mm\n"
        
        output += "\n"
    
    return output


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool(
    name="get_current_weather",
    annotations={
        "title": "Obtener Tiempo Actual",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_current_weather(params: Optional[GetCurrentWeatherInput] = None) -> str:
    """
    Obtiene el tiempo actual para una ciudad española.
    
    Esta herramienta consulta la API de Open-Meteo para obtener condiciones
    meteorológicas en tiempo real, incluyendo temperatura, humedad, viento y precipitación.
    
    Args:
        params (GetCurrentWeatherInput): Parámetros validados que incluyen:
            - city (SpanishCity): Ciudad española a consultar
            - response_format (ResponseFormat): Formato de salida (markdown o json)
    
    Returns:
        str: Datos del tiempo actual en el formato solicitado
    """
    try:
        logger.info(f"🔍 get_current_weather called with params: {params}")
        logger.info(f"🔍 Type of params: {type(params)}")
        # Provide defaults if params is None
        if params is None:
            params = GetCurrentWeatherInput(city=SpanishCity.MADRID, response_format=ResponseFormat.MARKDOWN)
        
        logger.info(f"🔍 Ciudad solicitada: {params.city.value}")
        coords = SPANISH_CITIES[params.city.value]
        logger.info(f"🔍 Coordenadas para {params.city.value}: {coords}")
        
        # Verificar que el parámetro city se respeta correctamente
        logger.info(f"🔍 Ciudad recibida: {params.city.value}")
        logger.info(f"🔍 Coordenadas utilizadas: {coords}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL,
                params={
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "current": "temperature_2m,apparent_temperature,precipitation,weather_code,relative_humidity_2m,wind_speed_10m",
                    "timezone": "Europe/Madrid"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return _format_current_weather_markdown(params.city.value, data)
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="get_weather_forecast",
    annotations={
        "title": "Obtener Previsión del Tiempo",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_weather_forecast(params: Optional[GetForecastInput] = None) -> str:
    """
    Obtiene la previsión meteorológica para los próximos días en una ciudad española.
    
    Proporciona previsiones detalladas por día, incluyendo temperatura máxima/mínima,
    condiciones meteorológicas y precipitación acumulada.
    
    Args:
        params (GetForecastInput): Parámetros validados que incluyen:
            - city (SpanishCity): Ciudad española a consultar
            - days (int): Número de días a predecir (1-7)
            - response_format (ResponseFormat): Formato de salida (markdown o json)
    
    Returns:
        str: Previsión del tiempo en el formato solicitado con estructura:
            - Fecha
            - Temperatura (min/max/media)
            - Condiciones meteorológicas
            - Precipitación esperada
    """
    try:
        logger.info(f"🔍 get_weather_forecast called with params: {params}")
        logger.info(f"🔍 Type of params: {type(params)}")
        # Provide defaults if params is None
        if params is None:
            params = GetForecastInput(city=SpanishCity.MADRID, days=5, response_format=ResponseFormat.MARKDOWN)
        
        logger.info(f"🔍 Ciudad solicitada: {params.city.value}")
        coords = SPANISH_CITIES[params.city.value]
        logger.info(f"🔍 Coordenadas para {params.city.value}: {coords}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL,
                params={
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
                    "timezone": "Europe/Madrid",
                    "forecast_days": params.days
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return _format_forecast_markdown(params.city.value, data, params.days)
    
    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="get_retail_weather_insights",
    annotations={
        "title": "Obtener Insights de Retail según el Tiempo",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_retail_weather_insights(params: Optional[GetRetailInsightsInput] = None) -> str:
    """
    Analiza el tiempo previsto y proporciona recomendaciones específicas para retail de moda.
    
    Esta herramienta combina datos meteorológicos con lógica de negocio para sugerir:
    - Productos a promocionar
    - Oportunidades de ajuste de precios
    - Estrategias de marketing
    - Gestión de inventario
    - Optimización logística
    
    Ideal para e-commerce de moda que quiere optimizar sus operaciones según el clima.
    
    Args:
        params (GetRetailInsightsInput): Parámetros validados que incluyen:
            - city (SpanishCity): Ciudad española a analizar
            - days (int): Número de días a analizar (1-7)
    
    Returns:
        str: Análisis detallado en formato markdown con:
            - Resumen de condiciones previstas
            - Productos recomendados para destacar
            - Oportunidades de pricing dinámico
            - Sugerencias de gestión de inventario
            - Recomendaciones de optimización logística
            - Estrategias de campañas de marketing
            - Desglose día por día
    """
    try:
        logger.info(f"🔍 get_retail_weather_insights called with params: {params}")
        logger.info(f"🔍 Type of params: {type(params)}")
        # Provide defaults if params is None
        if params is None:
            params = GetRetailInsightsInput(city=SpanishCity.MADRID, days=3)
        
        logger.info(f"🔍 Ciudad solicitada: {params.city.value}")
        coords = SPANISH_CITIES[params.city.value]
        logger.info(f"🔍 Coordenadas para {params.city.value}: {coords}")
        
        # Get forecast data
        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL,
                params={
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
                    "current": "temperature_2m,precipitation,weather_code",
                    "timezone": "Europe/Madrid",
                    "forecast_days": params.days
                },
                timeout=10.0
            )
            response.raise_for_status()
            forecast_data = response.json()
        
        # Analyze each day
        daily = forecast_data.get("daily", {})
        dates = daily.get("time", [])[:params.days]
        temp_max = daily.get("temperature_2m_max", [])[:params.days]
        temp_min = daily.get("temperature_2m_min", [])[:params.days]
        precipitation = daily.get("precipitation_sum", [])[:params.days]
        wmo_codes = daily.get("weather_code", [])[:params.days]
        
        daily_insights = []
        for i in range(min(params.days, len(dates))):
            avg_temp = round((temp_max[i] + temp_min[i]) / 2, 1) if i < len(temp_max) and i < len(temp_min) else 15
            precip = precipitation[i] if i < len(precipitation) else 0
            wmo = wmo_codes[i] if i < len(wmo_codes) else 0
            
            insights = _analyze_retail_impact(avg_temp, wmo, precip)
            daily_insights.append({
                "date": dates[i] if i < len(dates) else "Unknown",
                "insights": insights,
                "avg_temp": avg_temp,
                "precipitation": precip
            })
        
        # Format output
        city = params.city.value
        output = f"# 🛍️ Análisis de Retail para {city}\n\n"
        output += f"## Resumen Ejecutivo\n\n"
        
        # Aggregate recommendations
        all_products = set()
        all_pricing = set()
        all_marketing = set()
        all_inventory = set()
        all_logistics = set()
        
        for day in daily_insights:
            insights = day["insights"]
            all_products.update(insights["suggested_products"])
            all_pricing.update(insights["pricing_opportunities"])
            all_marketing.update(insights["marketing_angles"])
            all_inventory.update(insights["inventory_actions"])
            all_logistics.update(insights["logistics_optimization"])
        
        output += f"### 📦 Productos a Destacar\n"
        for product in all_products:
            output += f"- {product}\n"
        
        output += f"\n### 💰 Oportunidades de Pricing\n"
        if all_pricing:
            for opportunity in all_pricing:
                output += f"- {opportunity}\n"
        else:
            output += "- Mantener precios actuales (condiciones estables)\n"
        
        output += f"\n### 🏭 Gestión de Inventario\n"
        if all_inventory:
            for action in all_inventory:
                output += f"- {action}\n"
        else:
            output += "- Mantener distribución actual de stock\n"
        
        output += f"\n### 🚚 Optimización Logística\n"
        if all_logistics:
            for action in all_logistics:
                output += f"- {action}\n"
        else:
            output += "- No se requieren movimientos de stock entre ubicaciones\n"
        
        output += f"\n### 📢 Estrategias de Marketing\n"
        if all_marketing:
            for strategy in all_marketing:
                output += f"- {strategy}\n"
        else:
            output += "- Promoción general según temporada\n"
        
        # Daily breakdown
        output += f"\n## Desglose por Día\n\n"
        for day in daily_insights:
            wmo_for_day = wmo_codes[daily_insights.index(day)] if daily_insights.index(day) < len(wmo_codes) else 0
            emoji = _get_weather_emoji(wmo_for_day)
            precip_emoji = " ⚠️" if day["precipitation"] > 0 else ""
            
            output += f"### {day['date']} {emoji}{precip_emoji}\n"
            output += f"- **Temperatura media**: {day['avg_temp']}°C\n"
            output += f"- **Rango**: {day['insights']['temperature_range']}\n"
            if day["insights"]["precipitation"]:
                output += f"- **Precipitación**: Sí ({round(day['precipitation'], 1)} mm)\n"
            output += f"\n**Productos clave**: {', '.join(day['insights']['suggested_products'][:3]) if day['insights']['suggested_products'] else 'Stock general'}\n\n"
        
        return output
    
    except Exception as e:
        return _handle_api_error(e)


# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    # Modo Streamable HTTP para APIM 4.6
    # FastMCP expone automáticamente el endpoint /mcp cuando usas este transporte
    import uvicorn
    logger.info("🚀 Starting Weather MCP Server...")
    logger.info("📡 Health check: http://0.0.0.0:8080/health")
    logger.info("🌤️  MCP endpoint: http://0.0.0.0:8080/mcp")
    uvicorn.run(asgi_app, host="0.0.0.0", port=8080)