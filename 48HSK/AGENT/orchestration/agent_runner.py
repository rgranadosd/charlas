"""Agent orchestration extracted from the legacy monolith."""

from __future__ import annotations

import json
import re
import sys
import traceback
from typing import Optional

from semantic_kernel.functions import KernelArguments

from config import _thinking_enabled, get_debug_mode
from ui_console import Colors, ThinkingIndicator


def _parse_percent_adjustment(user_input: str) -> float | None:
    match = re.search(r"(\d+(?:[\.,]\d+)?)\s*(%|por\s*ciento)", user_input, flags=re.IGNORECASE)
    if not match:
        return None
    raw = match.group(1).replace(",", ".")
    try:
        pct = float(raw)
    except Exception:
        return None

    lower = user_input.lower()
    if any(word in lower for word in ["reduce", "reducir", "baja", "bajar", "decrementa", "decrementar", "rebaja", "rebajar", "descuento", "descuenta", "disminuye", "disminuir"]):
        pct = -abs(pct)
    elif any(word in lower for word in ["incrementa", "incrementar", "aumenta", "aumentar", "sube", "subir", "incremento", "aumento"]):
        pct = abs(pct)
    return pct


class AgentRunner:
    def __init__(self, kernel, shopify_plugin, weather_plugin=None):
        self.kernel = kernel
        self.shopify_plugin = shopify_plugin
        self.weather_plugin = weather_plugin
        self._last_recommended_products = []
        self._last_product_reasons = {}
        self._last_insights_city = None
        self._last_weather_summary = None
        self._last_pricing_actions = []
        self._system_prompt = (
            "Eres un asistente de e-commerce para gestión de tiendas Shopify. "
            "Responde siempre en español, de forma concisa y profesional. "
            "NUNCA uses emojis, iconos ni caracteres especiales decorativos en tus respuestas. "
            "Usa solo texto plano."
        )

    async def _invoke_with_system(self, user_prompt: str) -> str:
        full_prompt = f"[Sistema]: {self._system_prompt}\n\n[Usuario]: {user_prompt}"
        return str(await self.kernel.invoke_prompt(full_prompt)).strip()

    def _format_retail_insights_agent(self, raw_text: str) -> str:
        if not raw_text:
            return raw_text

        text = str(raw_text)
        if "Análisis de Retail" not in text:
            return raw_text

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        city = "tu ciudad"
        for line in lines:
            if line.startswith("# Análisis de Retail para "):
                city = line.replace("# Análisis de Retail para ", "").strip()
                break

        sections = {
            "Productos a Destacar": [],
            "Oportunidades de Pricing": [],
            "Gestión de Inventario": [],
            "Optimización Logística": [],
            "Estrategias de Marketing": [],
        }
        section = None
        days = []
        for line in lines:
            if line.startswith("### "):
                title = line[4:].strip()
                if title in sections:
                    section = title
                    continue
                if title[:4].isdigit():
                    days.append(title)
                section = None
                continue
            if line.startswith("- ") and section:
                sections[section].append(line[2:].strip())

        productos = sections["Productos a Destacar"]
        self._last_recommended_products = productos[:]
        pricing = sections["Oportunidades de Pricing"]
        inventario = sections["Gestión de Inventario"]
        marketing = sections["Estrategias de Marketing"]

        self._last_pricing_actions = pricing[:]

        resumen = []
        resumen.append(f"Claro. Aquí tienes el plan accionable para {city} basado en tu catálogo:")
        if productos:
            resumen.append(f"• Productos a destacar ahora: {', '.join(productos[:3])}.")
        else:
            resumen.append("• Productos a destacar ahora: no hay coincidencias claras en catálogo.")
        if pricing:
            resumen.append(f"• Pricing recomendado: {', '.join(pricing[:2])}.")
        if inventario:
            resumen.append(f"• Inventario: {', '.join(inventario[:2])}.")
        if marketing:
            resumen.append(f"• Marketing: {marketing[0]}.")
        if days:
            resumen.append(f"• Ventana clave: {', '.join(days[:3])}.")
        resumen.append("Si quieres, preparo acciones concretas (home, pricing o campañas) sobre esos productos.")
        return "\n".join(resumen)

    async def _remove_non_sense_products(self) -> str:
        if not self._last_weather_summary:
            return Colors.red("No tengo contexto de clima reciente. Pideme insights primero.")

        productos_actuales = self.shopify_plugin._get_homepage_products()
        if get_debug_mode():
            current = ", ".join(productos_actuales) if productos_actuales else "ninguno"
            print(Colors.cyan(f"[DEBUG] Productos actualmente en Home Page: {current}"))

        if not productos_actuales:
            return "La coleccion Home Page esta vacia. No hay nada que quitar."

        recomendados_str = ", ".join(self._last_recommended_products) if self._last_recommended_products else "ninguno"
        filter_prompt = (
            f"CLIMA ACTUAL en {self._last_insights_city}:\n{self._last_weather_summary}\n\n"
            f"PRODUCTOS ACTUALMENTE en Home Page:\n{', '.join(productos_actuales)}\n\n"
            f"PRODUCTOS RECOMENDADOS para este clima:\n{recomendados_str}\n\n"
            "TAREA: Analiza el clima actual y razona que productos de los ACTUALMENTE en Home Page "
            "NO tienen sentido promocionar dadas las condiciones meteorologicas.\n\n"
            "Razona sobre cada producto: es logico destacarlo con este clima? "
            "Por ejemplo, si llueve no tiene sentido destacar gafas de sol. "
            "Si hace frio no tiene sentido destacar ropa de verano ligera.\n\n"
            "IMPORTANTE: Los productos RECOMENDADOS no deben quitarse.\n\n"
            "Devuelve SOLO los nombres EXACTOS de productos a QUITAR, separados por coma.\n"
            "Si todos tienen sentido para el clima, devuelve NINGUNO.\n"
            "RESPUESTA:"
        )

        if get_debug_mode():
            print(Colors.cyan(f"[DEBUG] Prompt de filtrado:\n{filter_prompt[:500]}..."))

        filter_result = str(await self.kernel.invoke_prompt(filter_prompt)).strip()
        if get_debug_mode():
            print(Colors.cyan(f"[DEBUG] Respuesta LLM productos a quitar: {filter_result}"))

        if filter_result.upper() == "NINGUNO" or not filter_result:
            return "Todos los productos destacados tienen sentido para el clima actual. No hay nada que quitar."

        productos_quitar = [product.strip() for product in filter_result.split(",") if product.strip()]
        if get_debug_mode():
            print(Colors.cyan(f"[DEBUG] Productos parseados a quitar: {productos_quitar}"))

        productos_validados = []
        for product in productos_quitar:
            for actual in productos_actuales:
                if product.lower() in actual.lower() or actual.lower() in product.lower():
                    productos_validados.append(actual)
                    break

        if get_debug_mode():
            print(Colors.cyan(f"[DEBUG] Productos validados a quitar: {productos_validados}"))

        if not productos_validados:
            return "No se encontraron productos coincidentes para quitar de Home Page."

        responses = []
        for name in productos_validados:
            responses.append(self.shopify_plugin.remove_product_homepage(name))
        return "\n".join(responses)

    def _parse_percent_from_action(self, action: str) -> float:
        if not action:
            return 0.0
        nums = re.findall(r"\d+(?:\.\d+)?", action)
        percent = 0.0
        if len(nums) >= 2 and "-" in action:
            percent = (float(nums[0]) + float(nums[1])) / 2.0
        elif nums:
            percent = float(nums[0])
        if any(keyword in action.lower() for keyword in ["bajar", "reducir", "descontar", "rebajar"]):
            percent = -abs(percent)
        else:
            percent = abs(percent)
        return percent

    def _select_products_for_pricing(self, action: str, titles: list[str]) -> list[str]:
        action_l = action.lower()
        keyword_map = {
            "impermeable": ["impermeable", "chubasquero", "raincoat"],
            "abrigo": ["abrigo", "plumón", "plumon", "parka", "anorak"],
            "verano": ["camiseta", "vestido", "sandalia", "short", "bermuda", "polo"],
            "entretiempo": ["chaqueta", "cazadora", "jersey", "cardigan"],
        }
        keywords = []
        if "imperme" in action_l:
            keywords = keyword_map["impermeable"]
        elif "abrigo" in action_l:
            keywords = keyword_map["abrigo"]
        elif "verano" in action_l:
            keywords = keyword_map["verano"]
        elif "entretiempo" in action_l:
            keywords = keyword_map["entretiempo"]
        if not keywords:
            return []

        matched = []
        for title in titles:
            title_l = title.lower()
            if any(keyword in title_l for keyword in keywords):
                matched.append(title)
        return matched

    def _apply_pricing_actions(self) -> str:
        if not self._last_pricing_actions:
            return Colors.red("No tengo recomendaciones de pricing recientes. Pideme insights primero.")

        titles = self.shopify_plugin.get_product_titles()
        if not isinstance(titles, list) or not titles:
            return Colors.red("No pude cargar el catálogo para aplicar pricing.")

        responses = []
        applied = 0
        for action in self._last_pricing_actions:
            percent = self._parse_percent_from_action(action)
            if percent == 0:
                continue
            products = self._select_products_for_pricing(action, titles)
            if not products:
                continue
            for name in products:
                pid = self.shopify_plugin.find_id_by_name(name)
                if pid and str(pid).isdigit():
                    responses.append(self.shopify_plugin.update_product_price_by_percent(pid, percent))
                    applied += 1
        if not responses:
            return Colors.yellow("No encontré productos compatibles con las recomendaciones de pricing.")
        responses.append(f"Precios actualizados en {applied} productos.")
        return "\n".join(responses)

    def _clean_json(self, text):
        try:
            if text is None:
                return None
            s = str(text).strip()
            if not s:
                return None
            if s.startswith("```"):
                lines = s.splitlines()
                if lines:
                    lines = lines[1:]
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                s = "\n".join(lines).strip()
            try:
                return json.loads(s)
            except Exception:
                pass

            obj_start = s.find("{")
            obj_end = s.rfind("}")
            if obj_start != -1 and obj_end != -1 and obj_end > obj_start:
                return json.loads(s[obj_start:obj_end + 1])

            arr_start = s.find("[")
            arr_end = s.rfind("]")
            if arr_start != -1 and arr_end != -1 and arr_end > arr_start:
                return json.loads(s[arr_start:arr_end + 1])

            return None
        except Exception:
            return None

    def _extract_weather_signals(self, text: Optional[str]):
        if not text:
            return {"max_temp": None, "min_temp": None, "max_rain": None}

        def _to_float(value: str):
            try:
                return float(value.replace(",", "."))
            except Exception:
                return None

        max_temps = []
        min_temps = []
        for match in re.findall(r"Temperatura:\s*([\-\d\.,]+)°C\s*-\s*([\-\d\.,]+)°C", text):
            low = _to_float(match[0])
            high = _to_float(match[1])
            if low is not None:
                min_temps.append(low)
            if high is not None:
                max_temps.append(high)

        rains = []
        for match in re.findall(r"Lluvia esperada:\s*([\-\d\.,]+)\s*mm", text):
            value = _to_float(match)
            if value is not None:
                rains.append(value)

        return {
            "max_temp": max(max_temps) if max_temps else None,
            "min_temp": min(min_temps) if min_temps else None,
            "max_rain": max(rains) if rains else None,
        }

    def _normalize_city_name(self, city: str) -> str:
        if not city:
            return "Madrid"
        raw = city.strip().lower()
        city_map = {
            "madrid": "Madrid",
            "barcelona": "Barcelona",
            "valencia": "Valencia",
            "sevilla": "Sevilla",
            "zaragoza": "Zaragoza",
            "malaga": "Málaga",
            "málaga": "Málaga",
            "murcia": "Murcia",
            "bilbao": "Bilbao",
            "vitoria": "Vitoria",
            "vitoria-gasteiz": "Vitoria",
            "alicante": "Alicante",
            "cordoba": "Córdoba",
            "córdoba": "Córdoba",
            "burgos": "Burgos",
            "la coruna": "La Coruña",
            "la coruña": "La Coruña",
            "santa cruz de tenerife": "Santa Cruz de Tenerife",
            "santa cruz": "Santa Cruz de Tenerife",
            "buenaventura": "Buenaventura",
        }
        return city_map.get(raw, city.strip().title())

    async def _extract_json(self, function_name: str, user_input: str):
        try:
            response = await self.kernel.invoke(
                function_name=function_name,
                plugin_name="extractor",
                arguments=KernelArguments(input=user_input),
            )
            return self._clean_json(str(response))
        except Exception:
            return None

    async def run(self, user_input, silent: bool = False):
        indicator = ThinkingIndicator("")
        if (not silent) and (not get_debug_mode()) and _thinking_enabled():
            indicator.start()

        result = ""
        try:
            intent_prompt = (
                "Clasifica la intención en: ['listar', 'consultar_precio', 'actualizar_precio', 'consultar_descripcion', 'descripcion', 'actualizar_titulo', 'revertir', 'contar', 'ordenar', 'clima_actual', 'pronostico_clima', 'insights_retail', 'consultar_destacados', 'destacar_producto', 'quitar_destacado', 'general']\n"
                "EJEMPLOS SHOPIFY:\n"
                "User: 'Cuanto vale la gift card?' -> {\"category\": \"consultar_precio\"}\n"
                "User: 'Pon la Gift Card a 50' -> {\"category\": \"actualizar_precio\"}\n"
                "User: 'Dame la descripción de la Camiseta' -> {\"category\": \"consultar_descripcion\"}\n"
                "User: 'Actualiza la descripcion de la Camiseta a Nueva camiseta' -> {\"category\": \"descripcion\"}\n"
                "User: 'Cambia el nombre de la Camiseta a Camiseta Apicuriosa' -> {\"category\": \"actualizar_titulo\"}\n"
                "User: 'Qué productos tengo en destacados?' -> {\"category\": \"consultar_destacados\"}\n"
                "User: 'Muéstrame los productos de Home Page' -> {\"category\": \"consultar_destacados\"}\n"
                "User: 'Destaca el producto Camiseta Barcelona Skyline en Home Page' -> {\"category\": \"destacar_producto\"}\n"
                "User: 'Quita de Home Page la Camiseta Barcelona Skyline' -> {\"category\": \"quitar_destacado\"}\n"
                "User: 'Cuantos productos hay?' -> {\"category\": \"contar\"}\n"
                "User: 'Dame la lista sin precios' -> {\"category\": \"listar\"}\n"
                "User: 'Quiero ver el catálogo con precios' -> {\"category\": \"listar\"}\n"
                "\nEJEMPLOS WEATHER:\n"
                "User: '¿Qué tiempo hace en Madrid?' -> {\"category\": \"clima_actual\"}\n"
                "User: 'Cómo va a estar el clima en Barcelona?' -> {\"category\": \"pronostico_clima\"}\n"
                "User: 'Dame insights de retail para Valencia' -> {\"category\": \"insights_retail\"}\n"
                "User: '¿Va a llover en Sevilla?' -> {\"category\": \"pronostico_clima\"}\n"
                "User: 'Qué debo hacer con mi inventario según el clima?' -> {\"category\": \"insights_retail\"}\n"
                f"\nUser: '{user_input}'\n"
                "Output JSON:"
            )

            indicator.stop()
            indicator = ThinkingIndicator("")
            if (not silent) and (not get_debug_mode()) and _thinking_enabled():
                indicator.start()
            raw = str(await self.kernel.invoke_prompt(intent_prompt))
            data = self._clean_json(raw)
            intent = data.get("category", "general") if data else "general"
            u_lower = user_input.lower()

            if any(key in u_lower for key in ["descripción", "descripcion", "description", "body_html"]):
                if any(value in u_lower for value in ["dame", "muestra", "muéstrame", "ver", "enseña", "cual es", "cuál es"]):
                    intent = "consultar_descripcion"
                if any(value in u_lower for value in ["actualiza", "modifica", "cambia", "pon", "actualizar", "modificar", "cambiar"]):
                    intent = "descripcion"

            if any(key in u_lower for key in ["título", "titulo", "nombre", "renombra", "renombrar"]):
                if any(value in u_lower for value in ["actualiza", "modifica", "cambia", "pon", "actualizar", "modificar", "cambiar", "renombra", "renombrar"]):
                    intent = "actualizar_titulo"

            if any(key in u_lower for key in ["destacados", "destacado", "home page", "homepage"]):
                if any(value in u_lower for value in ["qué", "que", "cuáles", "cuales", "muestra", "muéstrame", "ver", "tengo", "hay", "lista", "dame"]):
                    intent = "consultar_destacados"

            if intent != "consultar_destacados":
                if any(key in u_lower for key in ["destaca", "destacar", "highlight"]):
                    if any(key in u_lower for key in ["producto", "productos", "product", "estos", "esos", "los que", "recomendados"]):
                        intent = "destacar_producto"

            if intent != "consultar_destacados":
                if any(key in u_lower for key in ["actualiza", "actualizar", "actualízame", "actualizarme"]):
                    if any(key in u_lower for key in ["destacados", "destacado", "home page", "homepage", "home"]):
                        intent = "destacar_producto"

            if any(key in u_lower for key in ["quita", "quitar", "remove", "elimina", "saca"]):
                if any(key in u_lower for key in ["home page", "homepage", "home", "destacado", "destacados"]):
                    intent = "quitar_destacado"

            if get_debug_mode():
                indicator.stop()
                print(f"\nDEBUG Intent: {intent}")
                indicator = ThinkingIndicator("")
                indicator.start()

            if intent == "listar":
                no_price_keywords = ["sin precio", "no precio", "sin el precio", "oculta el precio", "ocultar precio", "no quiero ver los precios", "sin coste"]
                show_p = not any(keyword in u_lower for keyword in no_price_keywords)
                result = self.shopify_plugin.get_products_list(show_price=show_p)
            elif intent == "contar":
                result = self.shopify_plugin.count_products()
            elif intent == "ordenar":
                result = self.shopify_plugin.sort_products()
            elif intent == "consultar_precio":
                permission_error = self.shopify_plugin._check_permission("View Products", "consultar precios de productos")
                if permission_error:
                    result = permission_error
                else:
                    ext_prompt = f"Extrae solo el nombre del producto de: '{user_input}'. Responde solo con el nombre."
                    pname = str(await self.kernel.invoke_prompt(ext_prompt)).strip()
                    pid = pname
                    if not pid.isdigit():
                        found = self.shopify_plugin.find_id_by_name(pname)
                        pid = found if found else pid
                    if pid and pid.isdigit():
                        result = self.shopify_plugin.get_product_price(pid)
                    else:
                        result = Colors.red(f"No encontré el producto '{pname}'")
            elif intent == "actualizar_precio":
                permission_error = self.shopify_plugin._check_permission("Update Prices", "modificar precios de productos")
                if permission_error:
                    result = permission_error
                else:
                    if any(key in u_lower for key in ["precios", "pricing"]) and any(key in u_lower for key in ["me has dicho", "como dices", "como dijiste", "recomendado", "recomendados", "según el clima", "segun el clima", "segun clima", "según clima"]):
                        result = self._apply_pricing_actions()
                    else:
                        pct = _parse_percent_adjustment(user_input)
                        if pct is not None:
                            pref = await self._extract_json("extract_product_ref", user_input)
                            pname = str((pref or {}).get("product") or "").strip()
                            if not pname:
                                d2 = await self._extract_json("extract_price_args", user_input)
                                pname = str((d2 or {}).get("product") or "").strip()

                            pid = pname
                            if pid and not pid.isdigit():
                                found = self.shopify_plugin.find_id_by_name(pname)
                                pid = found if found else pid

                            if pid and pid.isdigit():
                                result = self.shopify_plugin.update_product_price_by_percent(pid, pct)
                            else:
                                result = Colors.red("Producto no encontrado.")
                        else:
                            data = await self._extract_json("extract_price_args", user_input)
                            if data and data.get("product") and data.get("price"):
                                pname = str(data.get("product")).strip()
                                new_price = str(data.get("price")).strip()
                                pid = pname
                                if not pid.isdigit():
                                    found = self.shopify_plugin.find_id_by_name(pname)
                                    pid = found if found else pid
                                if pid.isdigit():
                                    result = self.shopify_plugin.update_product_price(pid, new_price)
                                else:
                                    result = Colors.red("Producto no encontrado.")
                            else:
                                result = Colors.red("Datos incompletos.")
            elif intent == "descripcion":
                permission_error = self.shopify_plugin._check_permission("Update Descriptions", "actualizar descripciones de productos")
                if permission_error:
                    result = permission_error
                else:
                    data = await self._extract_json("extract_description_args", user_input)
                    if not (data and data.get("product") and data.get("text")):
                        data = await self._extract_json("extract_description_args_fallback", user_input)
                    if data and data.get("product") and data.get("text"):
                        pname = str(data.get("product")).strip()
                        new_desc = str(data.get("text")).strip()
                        pid = pname
                        if not pid.isdigit():
                            found = self.shopify_plugin.find_id_by_name(pname)
                            pid = found if found else pid
                        if pid.isdigit():
                            result = self.shopify_plugin.update_description(pid, new_desc)
                        else:
                            result = Colors.red("Producto no encontrado.")
                    else:
                        if get_debug_mode():
                            indicator.stop()
                            print(f"\nDEBUG extract_description_args -> {data}")
                            indicator.start()
                        result = Colors.red("Datos incompletos.")
            elif intent == "consultar_descripcion":
                permission_error = self.shopify_plugin._check_permission("View Products", "consultar descripciones de productos")
                if permission_error:
                    result = permission_error
                else:
                    data = await self._extract_json("extract_product_ref", user_input)
                    if data and data.get("product"):
                        pname = str(data.get("product")).strip()
                        pid = pname
                        if not pid.isdigit():
                            found = self.shopify_plugin.find_id_by_name(pname)
                            pid = found if found else pid
                        if pid and pid.isdigit():
                            result = self.shopify_plugin.get_product_description(pid)
                        else:
                            result = Colors.red("Producto no encontrado.")
                    else:
                        result = Colors.red("Datos incompletos.")
            elif intent == "actualizar_titulo":
                permission_error = self.shopify_plugin._check_permission("Update Descriptions", "actualizar títulos de productos")
                if permission_error:
                    result = permission_error
                else:
                    data = await self._extract_json("extract_title_args", user_input)
                    if not (data and data.get("product") and data.get("title")):
                        data = await self._extract_json("extract_title_args_fallback", user_input)
                    if data and data.get("product") and data.get("title"):
                        pname = str(data.get("product")).strip()
                        new_title = str(data.get("title")).strip()
                        pid = pname
                        if not pid.isdigit():
                            found = self.shopify_plugin.find_id_by_name(pname)
                            pid = found if found else pid
                        if pid.isdigit():
                            result = self.shopify_plugin.update_title(pid, new_title)
                        else:
                            result = Colors.red("Producto no encontrado.")
                    else:
                        result = Colors.red("Datos incompletos.")
            elif intent == "revertir":
                permission_error = self.shopify_plugin._check_permission("Update Prices", "revertir precios")
                if permission_error:
                    result = permission_error
                else:
                    prompt = f"Extrae ID o nombre de: {user_input}. Solo texto."
                    pid = str(await self.kernel.invoke_prompt(prompt)).strip()
                    if not pid.isdigit():
                        found = self.shopify_plugin.find_id_by_name(pid)
                        pid = found if found else pid
                    if pid.isdigit():
                        result = self.shopify_plugin.revert_price(pid)
                    else:
                        result = Colors.red("Producto no encontrado.")
            elif intent == "clima_actual":
                if self.weather_plugin:
                    prompt = f"Extrae SOLO el nombre de la ciudad mencionada en: '{user_input}'. Si no hay ciudad, devuelve 'madrid'. Solo la ciudad, nada más."
                    city_raw = str(await self.kernel.invoke_prompt(prompt)).strip()
                    city = self._normalize_city_name(city_raw)
                    result = self.weather_plugin.get_current_weather(city=city)
                else:
                    result = Colors.red("Plugin de clima no disponible")
            elif intent == "pronostico_clima":
                if self.weather_plugin:
                    prompt = f"Extrae la ciudad y número de días (si se menciona) de: '{user_input}'. Devuelve JSON con {{\"city\": \"nombre\", \"days\": numero}}. Si no hay ciudad, usa 'madrid'. Si no hay días, usa 5."
                    extraction = str(await self.kernel.invoke_prompt(prompt)).strip()
                    data = self._clean_json(extraction)
                    city_raw = data.get("city", "madrid") if data else "madrid"
                    city = self._normalize_city_name(city_raw)
                    days = int(data.get("days", 5)) if data and data.get("days") else 5
                    result = self.weather_plugin.get_weather_forecast(city=city, days=days)
                else:
                    result = Colors.red("Plugin de clima no disponible")
            elif intent == "insights_retail":
                permission_error = self.shopify_plugin._check_permission("Update Prices", "dar consejos relacionados con el tiempo")
                if permission_error:
                    result = permission_error
                else:
                    if self.weather_plugin:
                        prompt = f"Extrae SOLO el nombre de la ciudad mencionada en: '{user_input}'. Si no hay ciudad, devuelve 'madrid'. Solo la ciudad, nada más."
                        city_raw = str(await self.kernel.invoke_prompt(prompt)).strip()
                        city = self._normalize_city_name(city_raw)
                        weather_forecast = self.weather_plugin.get_weather_forecast(city=city, days=5)
                        self._last_insights_city = city
                        self._last_weather_summary = weather_forecast[:800] if weather_forecast else None

                        products = []
                        view_perm = self.shopify_plugin._check_permission("View Products", "leer productos del catálogo")
                        if not view_perm:
                            titles = self.shopify_plugin.get_product_titles()
                            if isinstance(titles, list) and titles:
                                products = titles

                        if not products:
                            result = Colors.red("No hay productos en el catálogo para analizar")
                        else:
                            reasoning_prompt = f'''Eres un experto en retail de moda con sentido común.

PRONÓSTICO DEL CLIMA para {city}:
{weather_forecast}

CATÁLOGO DE PRODUCTOS DISPONIBLES:
{', '.join(products)}

TAREA: Selecciona EXACTAMENTE 8 productos que tengan sentido para el clima previsto.

REGLAS ESTRICTAS DE RAZONAMIENTO:
1. SOLO recomienda paraguas/chubasqueros si hay LLUVIA PREVISTA (>0mm). "Nublado" NO significa lluvia.
2. SOLO recomienda abrigos pesados si la temperatura es BAJA (<15°C).
3. Con temperaturas 15-25°C: ropa ligera, camisetas, vestidos son apropiados.
4. Con temperaturas >25°C: ropa muy ligera, shorts, sandalias.
5. NO INVENTES condiciones que no están en el pronóstico.

Para cada producto, da una razón BASADA EN LOS DATOS REALES del pronóstico.

Devuelve un JSON con este formato EXACTO:
{{
    "productos_destacar": [
        {{"nombre": "producto1", "razon": "razón basada en datos reales del pronóstico"}},
        {{"nombre": "producto2", "razon": "razón basada en datos reales"}},
        ...
    ],
    "razon_clima": "resumen del clima REAL y estrategia",
    "acciones_pricing": ["acción1", "acción2"],
    "acciones_marketing": ["acción1"]
}}

Usa SOLO nombres EXACTOS del catálogo. EXACTAMENTE 8 productos.
RESPUESTA JSON:'''

                            if get_debug_mode():
                                print(Colors.cyan(f"[DEBUG] Prompt de razonamiento clima:\n{reasoning_prompt[:600]}..."))

                            llm_response = str(await self.kernel.invoke_prompt(reasoning_prompt)).strip()
                            if get_debug_mode():
                                print(Colors.cyan(f"[DEBUG] Respuesta LLM razonamiento: {llm_response}"))

                            parsed = self._clean_json(llm_response)
                            if parsed:
                                productos_raw = parsed.get("productos_destacar", [])
                                razon = parsed.get("razon_clima", "")
                                pricing = parsed.get("acciones_pricing", [])
                                marketing = parsed.get("acciones_marketing", [])

                                productos_map = {product.lower(): product for product in products}
                                productos_validados = []
                                razones_productos = {}

                                for item in productos_raw:
                                    if isinstance(item, dict):
                                        nombre = item.get("nombre", "")
                                        razon_prod = item.get("razon", "")
                                    else:
                                        nombre = str(item)
                                        razon_prod = ""

                                    if nombre.lower() in productos_map:
                                        prod_real = productos_map[nombre.lower()]
                                        if prod_real not in productos_validados:
                                            productos_validados.append(prod_real)
                                            razones_productos[prod_real] = razon_prod
                                    else:
                                        for cat_product in products:
                                            if nombre.lower() in cat_product.lower() or cat_product.lower() in nombre.lower():
                                                if cat_product not in productos_validados:
                                                    productos_validados.append(cat_product)
                                                    razones_productos[cat_product] = razon_prod
                                                break

                                self._last_recommended_products = productos_validados[:]
                                self._last_product_reasons = razones_productos.copy()
                                self._last_pricing_actions = pricing[:]

                                resumen = []
                                resumen.append(f"Plan accionable para {city} basado en el clima previsto:")
                                resumen.append(f"• Análisis: {razon}")
                                if productos_validados:
                                    resumen.append("• Productos a destacar:")
                                    for product in productos_validados:
                                        razon_p = razones_productos.get(product, "")
                                        if razon_p:
                                            resumen.append(f"  - {product}: {razon_p}")
                                        else:
                                            resumen.append(f"  - {product}")
                                else:
                                    resumen.append("• Productos a destacar: no hay coincidencias claras.")
                                if pricing:
                                    resumen.append(f"• Pricing: {', '.join(pricing[:2])}.")
                                if marketing:
                                    resumen.append(f"• Marketing: {marketing[0]}.")
                                resumen.append("Si quieres, preparo acciones concretas (actualiza destacados, pricing).")
                                result = "\n".join(resumen)
                            else:
                                raw_weather = self.weather_plugin.get_retail_weather_insights(city=city, products=products)
                                result = self._format_retail_insights_agent(raw_weather)
                    else:
                        result = Colors.red("Plugin de clima no disponible")
            elif intent == "consultar_destacados":
                permission_error = self.shopify_plugin._check_permission("View Products", "consultar productos destacados")
                if permission_error:
                    result = permission_error
                else:
                    productos = self.shopify_plugin._get_homepage_products()
                    if get_debug_mode():
                        print(Colors.cyan("[DEBUG] Consultando productos en Home Page"))
                    if not productos:
                        result = "La colección Home Page está vacía. No hay productos destacados actualmente."
                    else:
                        result = f"Productos destacados en Home Page ({len(productos)}):\n- " + "\n- ".join(productos)
            elif intent == "destacar_producto":
                referencias_batch = [
                    "estos productos", "esos productos", "estos", "esos",
                    "los productos", "esos que", "los que me",
                    "que me recomiendas", "que recomiendas", "recomendados",
                    "los recomendados", "productos recomendados", "que me has dicho",
                    "que has dicho", "que dijiste", "como dices", "como dijiste",
                    "haz las acciones", "haz las acciones de destacar", "haz acciones de destacar",
                    "haz las acciones de destacar productos", "haz acciones de destacar productos",
                ]
                es_batch = any(ref in u_lower for ref in referencias_batch)
                if not es_batch:
                    if any(key in u_lower for key in ["destacados", "destacado", "home page", "homepage", "home"]):
                        if self._last_recommended_products:
                            es_batch = True

                if get_debug_mode() and es_batch:
                    print(Colors.cyan("[DEBUG] Detectado comando batch"))

                if es_batch:
                    if not self._last_recommended_products:
                        result = Colors.red("No tengo productos recientes para destacar. Pideme insights primero.")
                    elif not self._last_weather_summary:
                        result = Colors.red("No tengo contexto de clima. Pideme insights primero.")
                    else:
                        if get_debug_mode():
                            print(Colors.cyan(f"[DEBUG] Productos a destacar: {', '.join(self._last_recommended_products)}"))
                        responses = []
                        target_count = 8
                        final_targets = self._last_recommended_products[:target_count]

                        if get_debug_mode():
                            print(Colors.cyan(f"[DEBUG] Productos finales ({len(final_targets)}): {', '.join(final_targets)}"))

                        actuales = self.shopify_plugin._get_homepage_products()
                        actuales = actuales or []

                        responses.append("--- CAMBIOS EN HOME PAGE ---")
                        for name in actuales:
                            if name not in final_targets:
                                responses.append(self.shopify_plugin.remove_product_homepage(name))

                        responses.append("")
                        responses.append("--- PRODUCTOS AÑADIDOS ---")
                        for name in final_targets:
                            razon = self._last_product_reasons.get(name, "")
                            if name not in actuales:
                                add_result = self.shopify_plugin.feature_product_homepage(name)
                                if razon:
                                    responses.append(f"{add_result}")
                                    responses.append(f"   Razón: {razon}")
                                else:
                                    responses.append(add_result)
                            else:
                                if razon:
                                    responses.append(f"'{name}' ya estaba en Home Page")
                                    responses.append(f"   Razón: {razon}")
                                else:
                                    responses.append(f"'{name}' ya estaba en Home Page")

                        responses.append("")
                        responses.append(f"Home Page actualizado con {len(final_targets)} productos.")
                        result = "\n".join(responses)
                else:
                    prompt = (
                        f"Extrae SOLO el nombre del producto a destacar en Home Page de: '{user_input}'. "
                        "Devuelve solo el nombre del producto, nada más."
                    )
                    product_name = str(await self.kernel.invoke_prompt(prompt)).strip()
                    if not product_name:
                        result = Colors.red("No pude identificar el producto a destacar")
                    else:
                        if get_debug_mode():
                            print(Colors.cyan(f"[DEBUG] Producto a destacar: {product_name}"))
                        result = self.shopify_plugin.feature_product_homepage(product_name)
            elif intent == "quitar_destacado":
                filtro_inteligente = any(key in u_lower for key in ["no tengan sentido", "no tiene sentido", "no encajan", "no encajen", "no correspondan", "sobran", "sobren"])
                if filtro_inteligente:
                    result = await self._remove_non_sense_products()
                else:
                    prompt = (
                        f"Extrae SOLO el nombre del producto a quitar de Home Page de: '{user_input}'. "
                        "Devuelve solo el nombre del producto, nada más."
                    )
                    product_name = str(await self.kernel.invoke_prompt(prompt)).strip()
                    if not product_name:
                        result = Colors.red("No pude identificar el producto a quitar")
                    else:
                        if get_debug_mode():
                            print(Colors.cyan(f"[DEBUG] Producto a quitar: {product_name}"))
                        result = self.shopify_plugin.remove_product_homepage(product_name)
            else:
                result = str(await self.kernel.invoke_prompt(user_input))

        except Exception as exc:
            result = f"Error: {exc}"
            if get_debug_mode():
                traceback.print_exc()
        finally:
            indicator.stop()
            if not silent:
                sys.stdout.flush()
                print(f"\n{Colors.cyan(result)}\n")

        return result


Agent = AgentRunner

__all__ = ["Agent", "AgentRunner"]
