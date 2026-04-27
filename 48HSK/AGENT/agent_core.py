"""Reusable agent core shared by CLI and HTTP service modes."""

from __future__ import annotations

import os
import traceback
from dataclasses import dataclass
from typing import Any, Optional

import semantic_kernel as sk
import urllib3
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings

from config import load_profile
from oauth2_apim import create_openai_client_with_gateway

# Reuse the proven implementation while moving orchestration out of the CLI script.
import agent_gpt4 as legacy


@dataclass
class InvokeResult:
    answer: str
    model: str
    session_id: Optional[str] = None


class RafaAgent:
    """Shared façade around the existing agent implementation."""

    def __init__(
        self,
        *,
        force_auth: bool = False,
        debug_mode: bool = False,
        env_profile: str = "service",
        model_id: str = "gpt-4o-mini",
    ) -> None:
        self.force_auth = force_auth
        self.debug_mode = debug_mode
        self.env_profile = env_profile
        self.model_id = model_id

        self.kernel: Optional[sk.Kernel] = None
        self.agent: Optional[legacy.Agent] = None
        self._initialized = False
        self._original_interactive_auth = legacy.OAuthClient._interactive_auth
        self._interactive_auth_patched = False

    @property
    def is_ready(self) -> bool:
        return self._initialized and self.agent is not None

    def initialize(self) -> None:
        if self._initialized:
            return

        load_profile(self.env_profile)
        legacy.DEBUG_MODE = self.debug_mode
        urllib3.disable_warnings()

        if self.env_profile == "service":
            allow_interactive = os.getenv("ALLOW_INTERACTIVE_AUTH_IN_SERVICE", "false").lower() in {
                "1",
                "true",
                "yes",
                "on",
            }
            self._set_interactive_auth(enabled=allow_interactive)

        self.kernel = self._build_kernel()

        shopify_plugin = legacy.ShopifyPlugin(force_auth=self.force_auth)
        weather_plugin = None
        if os.getenv("WSO2_WEATHER_MCP_URL") or os.getenv("WSO2_APIM_CONSUMER_KEY"):
            try:
                weather_plugin = legacy.WeatherPlugin(force_auth=self.force_auth)
            except Exception:
                if self.debug_mode:
                    traceback.print_exc()

        self.agent = legacy.Agent(self.kernel, shopify_plugin, weather_plugin)
        self._initialized = True

    async def ask(
        self,
        message: str,
        *,
        silent: bool = True,
        allow_interactive_auth: Optional[bool] = None,
    ) -> str:
        if not message or not message.strip():
            raise ValueError("message is required")

        if self.env_profile == "service" and allow_interactive_auth is not None:
            self._set_interactive_auth(enabled=allow_interactive_auth)

        if not self._initialized:
            self.initialize()

        assert self.agent is not None
        return await self.agent.run(message.strip(), silent=silent)

    def _set_interactive_auth(self, *, enabled: bool) -> None:
        if enabled and self._interactive_auth_patched:
            legacy.OAuthClient._interactive_auth = self._original_interactive_auth
            self._interactive_auth_patched = False
            return

        if (not enabled) and (not self._interactive_auth_patched):
            def _disabled_interactive_auth(_self):
                if legacy.DEBUG_MODE:
                    print(legacy.Colors.yellow("OAuth interactivo deshabilitado en modo servicio"))
                return None

            legacy.OAuthClient._interactive_auth = _disabled_interactive_auth
            self._interactive_auth_patched = True

    def _build_kernel(self) -> sk.Kernel:
        kernel = sk.Kernel()

        use_gateway_env = os.getenv("USE_WSO2_GATEWAY")
        has_apim_creds = bool(os.getenv("WSO2_APIM_CONSUMER_KEY") and os.getenv("WSO2_APIM_CONSUMER_SECRET"))
        prefer_gateway = (
            (use_gateway_env is None and has_apim_creds)
            or (use_gateway_env or "").strip().lower() in {"1", "true", "yes", "y", "on"}
        )

        gateway_client = None
        if prefer_gateway:
            gateway_client = create_openai_client_with_gateway()
            if self.debug_mode and not gateway_client:
                print(legacy.Colors.yellow("No se pudo crear cliente Gateway; usando OpenAI directo"))

        if gateway_client:
            kernel.add_service(
                OpenAIChatCompletion(
                    service_id="openai",
                    ai_model_id=self.model_id,
                    async_client=gateway_client,
                    api_key="unused",
                )
            )
        else:
            if not os.getenv("OPENAI_API_KEY"):
                raise RuntimeError("Falta OPENAI_API_KEY (o configura WSO2_* para usar el Gateway)")
            kernel.add_service(
                OpenAIChatCompletion(
                    service_id="openai",
                    api_key=os.getenv("OPENAI_API_KEY"),
                    ai_model_id=self.model_id,
                )
            )

        extractor_settings = OpenAIChatPromptExecutionSettings(
            service_id="openai",
            temperature=0,
            response_format={"type": "json_object"},
            structured_json_response=True,
        )

        kernel.add_function(
            plugin_name="extractor",
            function_name="extract_price_args",
            description="Extrae (product, price) para actualizar precio.",
            prompt=(
                "Devuelve SOLO un JSON con las claves exactas: product, price.\n"
                "- product: nombre del producto o ID numérico (string).\n"
                "- price: nuevo precio como número (string), sin moneda.\n"
                "Si falta algún dato, devuelve string vacío en esa clave.\n\n"
                "Texto del usuario: {{$input}}\n"
            ),
            prompt_execution_settings=extractor_settings,
        )

        kernel.add_function(
            plugin_name="extractor",
            function_name="extract_description_args",
            description="Extrae (product, text) para actualizar descripción.",
            prompt=(
                "Devuelve SOLO un JSON con las claves exactas: product, text.\n"
                "- product: nombre del producto o ID numérico (string).\n"
                "- text: nueva descripción (string).\n"
                "Interpretación: el usuario suele decir 'de <producto> a <texto>' o 'de <producto> por <texto>'.\n"
                "La palabra 'por' significa el NUEVO texto de la descripción.\n"
                "Si falta algún dato, devuelve string vacío en esa clave.\n"
                "No inventes productos ni texto; usa lo que aporte el usuario.\n\n"
                "EJEMPLOS:\n"
                "- 'Actualiza la descripcion de Camiseta Apiuriosa a Camiseta Apicuriosa' -> {\"product\":\"Camiseta Apiuriosa\",\"text\":\"Camiseta Apicuriosa\"}\n"
                "- 'Modifica la descripcion del producto Camiseta Apiuriosa por Camiseta Apicuriosa' -> {\"product\":\"Camiseta Apiuriosa\",\"text\":\"Camiseta Apicuriosa\"}\n"
                "- 'Cambia la descripción de 12345 por Nueva descripción' -> {\"product\":\"12345\",\"text\":\"Nueva descripción\"}\n\n"
                "Texto del usuario: {{$input}}\n"
            ),
            prompt_execution_settings=extractor_settings,
        )

        kernel.add_function(
            plugin_name="extractor",
            function_name="extract_description_args_fallback",
            description="Fallback para extraer (product, text) cuando el input es ambiguo.",
            prompt=(
                "Devuelve SOLO un JSON con las claves exactas: product, text.\n"
                "Reglas:\n"
                "- Si aparece 'por', toma lo que esté después como text.\n"
                "- Si aparece 'a', toma lo que esté después como text (si parece una frase).\n"
                "- El product es el nombre/ID mencionado justo antes de 'por' o 'a'.\n"
                "Si no puedes determinarlo con confianza, devuelve string vacío.\n\n"
                "Texto del usuario: {{$input}}\n"
            ),
            prompt_execution_settings=extractor_settings,
        )

        kernel.add_function(
            plugin_name="extractor",
            function_name="extract_product_ref",
            description="Extrae solo la referencia del producto (nombre o ID) desde el texto.",
            prompt=(
                "Devuelve SOLO un JSON con la clave exacta: product.\n"
                "- product: nombre del producto o ID numérico (string).\n"
                "Si falta, devuelve string vacío.\n\n"
                "EJEMPLOS:\n"
                "- 'Dame la descripción de la Camiseta Apicuriosa' -> {\"product\":\"Camiseta Apicuriosa\"}\n"
                "- 'Muéstrame la descripción del producto 15566164820341' -> {\"product\":\"15566164820341\"}\n\n"
                "Texto del usuario: {{$input}}\n"
            ),
            prompt_execution_settings=extractor_settings,
        )

        kernel.add_function(
            plugin_name="extractor",
            function_name="extract_title_args",
            description="Extrae (product, title) para actualizar el título/nombre del producto.",
            prompt=(
                "Devuelve SOLO un JSON con las claves exactas: product, title.\n"
                "- product: nombre del producto o ID numérico (string).\n"
                "- title: nuevo título/nombre (string).\n"
                "Interpretación: el usuario suele decir 'cambia el nombre/título de <producto> a <nuevo>' o '... por <nuevo>'.\n"
                "La palabra 'por' significa el NUEVO título.\n"
                "Si falta algún dato, devuelve string vacío en esa clave.\n"
                "No inventes productos ni títulos; usa lo que aporte el usuario.\n\n"
                "EJEMPLOS:\n"
                "- 'Cambia el nombre de Camiseta Apiuriosa a Camiseta Apicuriosa' -> {\"product\":\"Camiseta Apiuriosa\",\"title\":\"Camiseta Apicuriosa\"}\n"
                "- 'Renombra el producto 12345 por Nuevo Nombre' -> {\"product\":\"12345\",\"title\":\"Nuevo Nombre\"}\n\n"
                "Texto del usuario: {{$input}}\n"
            ),
            prompt_execution_settings=extractor_settings,
        )

        kernel.add_function(
            plugin_name="extractor",
            function_name="extract_title_args_fallback",
            description="Fallback para extraer (product, title) cuando el input es ambiguo.",
            prompt=(
                "Devuelve SOLO un JSON con las claves exactas: product, title.\n"
                "Reglas:\n"
                "- Si aparece 'por', toma lo que esté después como title.\n"
                "- Si aparece 'a', toma lo que esté después como title (si parece una frase).\n"
                "- El product es el nombre/ID mencionado justo antes de 'por' o 'a'.\n"
                "Si no puedes determinarlo con confianza, devuelve string vacío.\n\n"
                "Texto del usuario: {{$input}}\n"
            ),
            prompt_execution_settings=extractor_settings,
        )

        return kernel
