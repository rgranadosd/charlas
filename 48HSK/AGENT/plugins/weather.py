"""Weather MCP integration plugin."""

from __future__ import annotations

import json
import os
import time
import traceback
from typing import List, Optional

import requests
from semantic_kernel.functions import kernel_function

from config import get_debug_mode
from ui_console import Colors


class WeatherPlugin:
    """Plugin para interactuar con el MCP Weather a través de WSO2 APIM."""

    def __init__(self, force_auth: bool = False):
        self._token_cache = None
        self._token_expires_at = 0
        self._mcp_session_id = None

        self.mcp_base_url = os.getenv("WSO2_WEATHER_MCP_URL", "https://localhost:9453/weather-mcp/1.0.0")
        self.mcp_local_base_url = os.getenv("WEATHER_MCP_LOCAL_URL", "http://localhost:8080")
        self.enable_local_fallback = os.getenv("WEATHER_MCP_LOCAL_FALLBACK", "true").lower() in ("1", "true", "yes", "on")

        if get_debug_mode():
            print(Colors.cyan(f"[DEBUG] WeatherPlugin inicializado - URL: {self.mcp_base_url}"))

    def _is_local_mcp(self) -> bool:
        return "localhost:8080" in self.mcp_base_url or "127.0.0.1:8080" in self.mcp_base_url

    def _is_apim_auth_failure(self, response: requests.Response) -> bool:
        text = response.text if response is not None else ""
        return '"code":"900900"' in text or "Unclassified Authentication Failure" in text

    def _switch_to_local_mcp(self):
        self.mcp_base_url = self.mcp_local_base_url.rstrip("/")
        self._mcp_session_id = None
        if get_debug_mode():
            print(Colors.yellow(f"[MCP] Fallback a MCP local: {self.mcp_base_url}"))

    def _build_apim_compat_base_url(self) -> str | None:
        base = self.mcp_base_url.rstrip("/")
        if self._is_local_mcp() or not base.startswith("http"):
            return None

        parts = base.split("/")
        if len(parts) < 4:
            return None

        maybe_version = parts[-1]
        if maybe_version and maybe_version[0].isdigit():
            # Some APIM imports with version embedded in context end up exposing
            # /<context>/<version>/<version>/..., so we retry with this form.
            return f"{base}/{maybe_version}"
        return None

    def _switch_to_apim_compat_url(self) -> bool:
        compat_base = self._build_apim_compat_base_url()
        if not compat_base or compat_base == self.mcp_base_url.rstrip("/"):
            return False

        self.mcp_base_url = compat_base
        self._mcp_session_id = None
        if get_debug_mode():
            print(Colors.yellow(f"[MCP] Reintentando con ruta APIM compat: {self.mcp_base_url}"))
        return True

    def _normalize_city(self, city: str) -> str:
        if not city:
            return city
        normalized = city.strip().lower()
        city_map = {
            "barcelona": "Barcelona",
            "madrid": "Madrid",
            "valencia": "Valencia",
            "sevilla": "Sevilla",
            "zaragoza": "Zaragoza",
            "malaga": "Málaga",
            "murcia": "Murcia",
            "bilbao": "Bilbao",
            "vitoria": "Vitoria",
            "vitoria-gasteiz": "Vitoria",
            "alicante": "Alicante",
            "cordoba": "Córdoba",
            "burgos": "Burgos",
            "la coruna": "La Coruña",
            "coruna": "La Coruña",
            "buenaventura": "Buenaventura",
            "santa cruz de tenerife": "Santa Cruz de Tenerife",
            "tenerife": "Santa Cruz de Tenerife",
        }
        return city_map.get(normalized, city.strip().title())

    def _get_apim_token(self):
        now = time.time()
        if self._token_cache and now < (self._token_expires_at - 30):
            return self._token_cache

        try:
            from oauth2_apim import _fetch_oauth2_token_sync

            token, expires_in = _fetch_oauth2_token_sync()
            self._token_cache = token
            self._token_expires_at = time.time() + expires_in
            return token
        except Exception as exc:
            if get_debug_mode():
                print(Colors.red(f"Error obteniendo token APIM: {exc}"))
            return None

    def _initialize_mcp_session(self, token: str) -> str | None:
        url = f"{self.mcp_base_url}/mcp"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        init_payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "WeatherPlugin", "version": "1.0"},
            },
            "id": 1,
        }

        try:
            if get_debug_mode():
                print(Colors.cyan("[MCP] Inicializando sesión MCP..."))

            response = requests.post(url, headers=headers, json=init_payload, verify=False)
            session_id = response.headers.get("mcp-session-id")

            if get_debug_mode():
                print(Colors.cyan(f"[MCP] Init Status: {response.status_code}"))
                print(Colors.cyan(f"[MCP] Session ID obtenido: {session_id}"))

            if response.status_code == 200 and session_id:
                return session_id
            if get_debug_mode():
                print(Colors.red(f"[MCP] Error inicializando sesión: {response.text[:500]}"))
            return None
        except Exception as exc:
            if get_debug_mode():
                print(Colors.red(f"[MCP] Exception en init: {str(exc)}"))
            return None

    def _call_mcp(self, tool_name: str, params: dict | None = None, _retried: bool = False):
        if self._is_local_mcp():
            token = os.getenv("WEATHER_MCP_LOCAL_TOKEN", "weather-mcp-2026")
        else:
            token = self._get_apim_token()
            if not token:
                return {"error": "No se pudo obtener token de autenticación APIM"}

        if not self._mcp_session_id:
            self._mcp_session_id = self._initialize_mcp_session(token)
            if not self._mcp_session_id:
                if self.enable_local_fallback and (not self._is_local_mcp()) and (not _retried):
                    if get_debug_mode():
                        print(Colors.yellow("[MCP] Falló init vía APIM, intentando fallback local..."))
                    self._switch_to_local_mcp()
                    return self._call_mcp(tool_name, params, _retried=True)
                return {"error": "No se pudo inicializar sesión MCP"}

        url = f"{self.mcp_base_url}/mcp"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self._mcp_session_id,
        }
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": {"params": params or {}}},
            "id": 2,
        }

        try:
            if get_debug_mode():
                print(Colors.cyan(f"[MCP] Llamando a {tool_name} con params: {params}"))
                print(Colors.cyan(f"[MCP] URL: {url}"))
                print(Colors.cyan(f"[MCP] Session ID: {self._mcp_session_id}"))

            response = requests.post(url, headers=headers, json=payload, verify=False)

            if get_debug_mode():
                print(Colors.cyan(f"[MCP] Status: {response.status_code}"))
                print(Colors.cyan(f"[MCP] Response (first 500 chars): {response.text[:500]}"))

            if response.status_code == 200:
                try:
                    response_text = response.text
                    if response_text.startswith("event:"):
                        for line in response_text.split("\n"):
                            if line.startswith("data:"):
                                json_data = line[5:].strip()
                                json_response = json.loads(json_data)
                                break
                        else:
                            return {"error": "No se encontró data en respuesta SSE"}
                    else:
                        json_response = json.loads(response_text)

                    if "result" in json_response:
                        result = json_response["result"]
                        if isinstance(result, dict) and "content" in result:
                            content_list = result.get("content", [])
                            if content_list and isinstance(content_list, list):
                                text_content = ""
                                for item in content_list:
                                    if isinstance(item, dict) and item.get("type") == "text":
                                        text_content += item.get("text", "")
                                return {"content": text_content} if text_content else result
                        return result
                    if "error" in json_response:
                        return {"error": f"MCP Error: {json_response['error']}"}
                    return json_response
                except Exception as exc:
                    print(Colors.red(f"[MCP] Error parsing response: {exc}"))
                    print(Colors.red(f"[MCP] Response: {response.text[:1000]}"))
                    return {"error": f"Respuesta inválida del MCP: {str(exc)}"}
            if response.status_code == 400:
                if "Missing session ID" in response.text or "session" in response.text.lower():
                    if get_debug_mode():
                        print(Colors.yellow("[MCP] Session expirada, reinicializando..."))
                    self._mcp_session_id = None
                    return self._call_mcp(tool_name, params)
                return {"error": f"Error MCP 400: {response.text[:200]}"}
            if response.status_code == 401:
                if self.enable_local_fallback and (not self._is_local_mcp()) and self._is_apim_auth_failure(response) and (not _retried):
                    self._switch_to_local_mcp()
                    return self._call_mcp(tool_name, params, _retried=True)
                if not _retried:
                    if get_debug_mode():
                        print(Colors.yellow("[MCP] Token inválido/expirado, renovando..."))
                    self._token_cache = None
                    self._token_expires_at = 0
                    self._mcp_session_id = None
                    return self._call_mcp(tool_name, params, _retried=True)
                return {"error": "Token de autenticación inválido o expirado"}
            if response.status_code == 403:
                if self.enable_local_fallback and (not self._is_local_mcp()) and self._is_apim_auth_failure(response) and (not _retried):
                    self._switch_to_local_mcp()
                    return self._call_mcp(tool_name, params, _retried=True)
                return {"error": "Sin permisos para esta operación"}
            if response.status_code == 404:
                if not _retried:
                    if self._switch_to_apim_compat_url():
                        return self._call_mcp(tool_name, params, _retried=True)
                    if get_debug_mode():
                        print(Colors.yellow("[MCP] 404 recibido, reinicializando sesión y reintentando..."))
                    self._mcp_session_id = None
                    return self._call_mcp(tool_name, params, _retried=True)
                return {"error": f"Endpoint no encontrado: {url}"}

            if self.enable_local_fallback and (not self._is_local_mcp()) and self._is_apim_auth_failure(response) and (not _retried):
                if get_debug_mode():
                    print(Colors.yellow("[MCP] APIM rechazó request (900900), fallback a MCP local..."))
                self._switch_to_local_mcp()
                return self._call_mcp(tool_name, params, _retried=True)
            if get_debug_mode():
                print(Colors.red(f"MCP Error {response.status_code}: {response.text}"))
            return {"error": f"Error MCP {response.status_code}: {response.text[:200]}"}
        except requests.exceptions.ConnectionError:
            return {"error": f"No se pudo conectar al MCP Weather: {self.mcp_base_url}"}
        except Exception as exc:
            if get_debug_mode():
                print(Colors.red(f"Exception en MCP call: {str(exc)}"))
                traceback.print_exc()
            return {"error": f"Error inesperado: {str(exc)}"}

    @kernel_function(
        name="get_current_weather",
        description="Obtiene el clima actual de una ciudad (España o Colombia). Ciudades disponibles: madrid, barcelona, valencia, sevilla, malaga, bilbao, zaragoza, murcia, palma, las_palmas, alicante, cordoba, valladolid, vigo, gijon, la_coruna, granada, vitoria, elche, oviedo, santa_cruz_tenerife, pamplona, almeria, san_sebastian, burgos, santander, castellon, albacete, logrono, badajoz, salamanca, huelva, lleida, tarragona, leon, cadiz, jaen, orense, lugo, caceres, melilla, ceuta, buenaventura",
    )
    def get_current_weather(self, city: str = "madrid"):
        city_normalized = self._normalize_city(city)
        result = self._call_mcp("get_current_weather", {"city": city_normalized, "response_format": "markdown"})
        if "error" in result:
            return Colors.red(f"Error: {result['error']}")
        return result.get("content", "No se pudo obtener información del clima")

    @kernel_function(
        name="get_weather_forecast",
        description="Obtiene el pronóstico del clima para los próximos días en una ciudad. Parámetros: city (nombre de la ciudad), days (número de días, máximo 7)",
    )
    def get_weather_forecast(self, city: str = "madrid", days: int = 5):
        city_normalized = self._normalize_city(city)
        result = self._call_mcp("get_weather_forecast", {"city": city_normalized, "days": min(days, 7), "response_format": "markdown"})
        if "error" in result:
            return Colors.red(f"Error: {result['error']}")
        return result.get("content", "No se pudo obtener el pronóstico del clima")

    @kernel_function(
        name="get_retail_weather_insights",
        description="Obtiene insights de clima enfocados en retail y e-commerce para una ciudad. Incluye recomendaciones de inventario y estrategias de marketing basadas en el pronóstico del clima.",
    )
    def get_retail_weather_insights(self, city: str = "madrid", days: int = 3, products: Optional[List[str]] = None):
        city_normalized = self._normalize_city(city)
        params = {"city": city_normalized, "days": min(days, 7)}
        if products:
            params["products"] = products
        result = self._call_mcp("get_retail_weather_insights", params)
        if "error" in result:
            return Colors.red(f"Error: {result['error']}")
        return result.get("content", "No se pudieron obtener insights de retail")


__all__ = ["WeatherPlugin"]
