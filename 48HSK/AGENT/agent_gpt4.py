import os
import requests
import asyncio
import json
import base64
import argparse
import threading
import time
import sys
import traceback
import re
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from openai import OpenAI, AsyncOpenAI
import httpx
from typing import Optional

# Para decodificar JWT
try:
    import jwt
except ImportError:
    jwt = None

# ============================================
# CONFIGURACIÓN Y UTILIDADES
# ============================================

DEBUG_MODE = False

class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    RESET = '\033[0m'
    
    @staticmethod
    def blue(text): return f"{Colors.BLUE}{text}{Colors.RESET}"
    @staticmethod
    def red(text): return f"{Colors.RED}[ERROR] {text}{Colors.RESET}"
    @staticmethod
    def green(text): return f"{Colors.GREEN}[OK] {text}{Colors.RESET}"
    @staticmethod
    def yellow(text): return f"{Colors.YELLOW}{text}{Colors.RESET}"
    @staticmethod
    def cyan(text): return f"{Colors.CYAN}{text}{Colors.RESET}"

class ThinkingIndicator:
    """Robust non-blocking loading animation."""
    def __init__(self, message="Thinking"):
        self.message = message
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        # Borrar línea completa y volver al inicio
        sys.stdout.write(f"\r{' ' * (len(self.message) + 10)}\r")
        sys.stdout.flush()

    def _animate(self):
        chars = [".  ", ".. ", "...", "   "]
        i = 0
        while self.running:
            sys.stdout.write(f"\r{Colors.blue(self.message)} {chars[i % len(chars)]}")
            sys.stdout.flush()
            time.sleep(0.3)
            i += 1

load_dotenv()

# ============================================
# LÓGICA SHOPIFY (Plugin)
# ============================================

class PriceMemory:
    def __init__(self): self.history = {}
    def remember(self, pid, old, new): self.history[pid] = {'old': old, 'new': new}
    def get_old(self, pid): return self.history.get(pid, {}).get('old')

class ShopifyPlugin:
    def __init__(self):
        self.memory = PriceMemory()

    def _validate_user_against_is(self):
        """
        Valida usuario/contraseña contra Identity Server (solo para autenticación inicial).
        No retorna token para usar en API, solo valida que el usuario existe y las credenciales son correctas.
        
        Returns:
            bool: True si el usuario fue validado exitosamente, False en caso contrario
        """
        username = os.getenv("WSO2_USERNAME")
        password = os.getenv("WSO2_PASSWORD")
        client_id = os.getenv("WSO2_CLIENT_ID")
        client_secret = os.getenv("WSO2_CLIENT_SECRET")
        
        if not (username and password and client_id and client_secret):
            return False  # No hay credenciales de usuario configuradas
        
        # Para Password Grant, usar endpoint de Identity Server (puerto 9443)
        token_endpoint = os.getenv("WSO2_TOKEN_ENDPOINT", "")
        is_url = os.getenv("WSO2_IS_TOKEN_ENDPOINT")  # Endpoint específico de IS si está configurado
        
        if not is_url:
            # Detectar si el endpoint actual es de APIM y construir el de IS
            if "9453" in token_endpoint or "8253" in token_endpoint or "8243" in token_endpoint:
                # Reemplazar puerto de APIM por puerto de IS (9443)
                is_url = token_endpoint.replace(":9453", ":9443").replace(":8253", ":9443").replace(":8243", ":9443")
            elif "9443" in token_endpoint:
                is_url = token_endpoint
            else:
                # Por defecto, usar puerto 9443
                is_url = "https://localhost:9443/oauth2/token"
        
        # Password Grant: valida usuario/contraseña contra IS (OBLIGATORIO)
        data = {
            "grant_type": "password",
            "username": username,
            "password": password
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers["Authorization"] = f"Basic {creds}"
        
        try:
            if DEBUG_MODE:
                print(Colors.cyan(f"Validando usuario '{username}' contra Identity Server: {is_url}"))
            r = requests.post(is_url, headers=headers, data=data, verify=False, timeout=10)
            if r.status_code == 200:
                if DEBUG_MODE:
                    print(Colors.green(f"✓ Usuario '{username}' validado exitosamente en Identity Server"))
                return True
            else:
                # Si falla, mostrar error
                try:
                    error_json = r.json()
                    error_detail = error_json.get('error_description', str(error_json))
                    print(Colors.red(f"✗ Validación de usuario falló (HTTP {r.status_code}): {error_detail}"))
                except:
                    print(Colors.red(f"✗ Validación de usuario falló (HTTP {r.status_code})"))
                return False
        except Exception as e:
            print(Colors.red(f"✗ Error al validar usuario: {e}"))
            return False
    
    def _get_token(self):
        """
        Obtiene token de acceso de WSO2 APIM Gateway para usar en llamadas API.
        Siempre usa Client Credentials Grant con Consumer Key/Secret (APIM).
        NO valida usuario aquí, eso se hace en _validate_user_against_is().
        
        Returns:
            token: Token de acceso de APIM o None si falla
        """
        url = os.getenv("WSO2_TOKEN_ENDPOINT")
        if not url:
            return None
            
        consumer_key = os.getenv("WSO2_CONSUMER_KEY")
        consumer_secret = os.getenv("WSO2_CONSUMER_SECRET")
        
        if not (consumer_key and consumer_secret):
            return None
        
        headers = {"Authorization": f"Basic {base64.b64encode(f'{consumer_key}:{consumer_secret}'.encode()).decode()}", 
                  "Content-Type": "application/x-www-form-urlencoded"}
        try:
            if DEBUG_MODE:
                print(Colors.cyan(f"Obteniendo token de APIM Gateway: {url}"))
            r = requests.post(url, headers=headers, data="grant_type=client_credentials", verify=False, timeout=10)
            if r.status_code == 200:
                response = r.json()
                token = response.get("access_token")
                if token:
                    if DEBUG_MODE:
                        print(Colors.green(f"✓ Token de APIM obtenido exitosamente"))
                    return token
            else:
                try:
                    error_json = r.json()
                    error_detail = error_json.get('error_description', str(error_json))
                    if DEBUG_MODE:
                        print(Colors.red(f"✗ Error obteniendo token APIM (HTTP {r.status_code}): {error_detail}"))
                except:
                    if DEBUG_MODE:
                        print(Colors.red(f"✗ Error obteniendo token APIM (HTTP {r.status_code})"))
        except Exception as e:
            if DEBUG_MODE:
                print(Colors.red(f"✗ Error en client credentials: {e}"))
        
        return None

    def _validate_user(self, token):
        """
        Valida que el usuario esté autenticado en WSO2 IS.
        Si el token se obtuvo correctamente, el usuario está autenticado.
        Retorna True si el token es válido, False en caso contrario.
        """
        if not token:
            return False
        
        # Si el token es JWT, decodificarlo para verificar que es válido
        if token.startswith("eyJ"):
            try:
                decoded = jwt.decode(token, options={"verify_signature": False})
                # Si tiene sub (subject), el usuario está autenticado
                return "sub" in decoded
            except Exception:
                return False
        
        # Si no es JWT pero existe, asumir que es válido (UUID token)
        return True
    
    def _api(self, method, path, data=None):
        # Obtener token de APIM Gateway para las llamadas API
        token = self._get_token()
        if not token: 
            return {
                "error": "Authentication Error: Unable to obtain APIM Gateway token",
                "details": "Failed to obtain access token from APIM Gateway. Please check your credentials.",
                "suggestion": "Verify:\n  - WSO2_CONSUMER_KEY and WSO2_CONSUMER_SECRET are correct\n  - WSO2_TOKEN_ENDPOINT is correct\n  - WSO2 APIM Gateway is running and accessible"
            }
        
        # Verificar que WSO2_GW_URL esté configurado
        gw_url = os.getenv('WSO2_GW_URL')
        if not gw_url:
            return {"error": "Configuration Error: WSO2_GW_URL not configured"}
        
        # Verificar que SHOPIFY_API_TOKEN esté configurado
        shopify_token = os.getenv("SHOPIFY_API_TOKEN")
        if not shopify_token or shopify_token == "your_shopify_api_token_here":
            return {
                "error": "Configuration Error: SHOPIFY_API_TOKEN not configured",
                "details": "The SHOPIFY_API_TOKEN environment variable is missing or not set to a valid value.",
                "suggestion": "Please configure SHOPIFY_API_TOKEN in your .env file with a valid Shopify API token."
            }
        
        url = f"{gw_url}/shopify/1.0.0{path}"
        headers = {
            "Authorization": f"Bearer {token}", 
            "X-Shopify-Access-Token": shopify_token, 
            "Content-Type": "application/json"
        }
        
        try:
            if method == 'GET': 
                r = requests.get(url, headers=headers, verify=False, timeout=10)
            else: 
                r = requests.put(url, headers=headers, json=data, verify=False, timeout=10)
            
            # Check HTTP status code first
            if r.status_code == 401 or r.status_code == 403:
                error_detail = "Invalid Credentials"
                try:
                    error_json = r.json()
                    if isinstance(error_json, dict):
                        error_code = error_json.get('code', '')
                        error_msg = error_json.get('message', 'Invalid Credentials')
                        error_desc = error_json.get('description', '')
                        if error_code == '900901':
                            return {
                                "error": f"WSO2 Gateway Authentication Failed (Code: {error_code})",
                                "details": error_desc or error_msg,
                                "suggestion": "Please verify:\n  - WSO2_CLIENT_ID and WSO2_CLIENT_SECRET are correct\n  - WSO2_USERNAME and WSO2_PASSWORD are valid\n  - The token endpoint URL is correct\n  - Your user has permission to access the Shopify API"
                            }
                        return {"error": f"Authentication Failed: {error_msg}", "details": error_desc}
                except:
                    pass
                return {"error": f"Authentication Failed (HTTP {r.status_code}): {error_detail}"}
            
            if r.status_code != 200:
                return {"error": f"HTTP {r.status_code} Error", "details": r.text[:200] if r.text else "No response body"}
            
            # Si hay contenido, intentar parsear JSON
            if r.content:
                try:
                    response_data = r.json()
                    # Check if response contains WSO2 error structure
                    if isinstance(response_data, dict) and 'code' in response_data and 'message' in response_data:
                        error_code = response_data.get('code', '')
                        error_msg = response_data.get('message', '')
                        error_desc = response_data.get('description', '')
                        return {
                            "error": f"WSO2 Gateway Error (Code: {error_code})",
                            "details": error_desc or error_msg,
                            "suggestion": "Check your WSO2 Gateway configuration and API permissions"
                        }
                    return response_data
                except:
                    return {"error": f"Invalid JSON response: {r.text[:200]}"}
            else:
                return {"error": f"Empty response (HTTP {r.status_code})"}
                
        except requests.exceptions.ConnectionError as e:
            return {"error": f"Connection Error: Cannot connect to {gw_url}. Is WSO2 Gateway running?"}
        except requests.exceptions.Timeout:
            return {"error": f"Timeout: Gateway at {gw_url} did not respond"}
        except Exception as e: 
            return {"error": f"API Error: {str(e)}"}

    def find_id_by_name(self, name):
        data = self._api("GET", "/products.json")
        if "products" in data:
            for p in data["products"]:
                if name.lower() in p["title"].lower():
                    return str(p['id'])
        return None

    def get_product_price(self, product_id):
        curr = self._api("GET", f"/products/{product_id}.json")
        if "product" in curr:
            title = curr["product"]["title"]
            price = curr["product"]["variants"][0]["price"]
            return f"The price of '{title}' is ${price}"
        return Colors.red("Product not found")

    @kernel_function(name="get_products_list")
    def get_products_list(self, show_price=True):
        data = self._api("GET", "/products.json")
        if "error" in data:
            error_msg = f"Error: {data['error']}"
            if "details" in data:
                error_msg += f"\n{data['details']}"
            if "suggestion" in data:
                error_msg += f"\n\n{data['suggestion']}"
            return error_msg
        if "products" in data:
            lines = []
            for p in data["products"]:
                price_txt = f" - ${p['variants'][0]['price']}" if show_price else ""
                lines.append(f"- ID: {p['id']} - {p['title']}{price_txt}")
            return "\n".join(lines)
        return f"Error listing products: {json.dumps(data, indent=2) if isinstance(data, dict) else str(data)}"

    @kernel_function(name="update_product_price")
    def update_product_price(self, product_id, price):
        curr = self._api("GET", f"/products/{product_id}.json")
        if "product" not in curr: return Colors.red("Product not found")
        vid = curr["product"]["variants"][0]["id"]
        old = curr["product"]["variants"][0]["price"]
        payload = {"product": {"id": int(product_id), "variants": [{"id": vid, "price": str(price)}]}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        if "product" in res:
            self.memory.remember(product_id, old, price)
            return Colors.green(f"Price updated: ${old} -> ${price}")
        return Colors.red("Error updating price")

    @kernel_function(name="update_description")
    def update_description(self, product_id, text):
        payload = {"product": {"id": int(product_id), "body_html": text}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        return Colors.green("Description updated") if "product" in res else Colors.red("Error")

    @kernel_function(name="revert_price")
    def revert_price(self, product_id):
        old = self.memory.get_old(product_id)
        if old: return self.update_product_price(product_id, old)
        return Colors.red("No previous history")

    @kernel_function(name="count_products")
    def count_products(self):
        d = self._api("GET", "/products/count.json")
        return f"Total: {d.get('count', 0)}"

    @kernel_function(name="sort_products")
    def sort_products(self):
        data = self._api("GET", "/products.json")
        if "products" in data:
            prods = sorted(data["products"], key=lambda x: float(x['variants'][0]['price']), reverse=True)
            lines = [f"- ${p['variants'][0]['price']} - {p['title']}" for p in prods]
            return "Products sorted (Highest to lowest):\n" + "\n".join(lines)
        return "Error"

# ============================================
# AGENTE INTELIGENTE
# ============================================

class Agent:
    def __init__(self, kernel, plugin):
        self.kernel = kernel
        self.plugin = plugin

    def _clean_json(self, text):
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            return json.loads(match.group()) if match else json.loads(text)
        except: return None

    async def run(self, user_input):
        # Instantiate the indicator each time to avoid thread errors
        indicator = ThinkingIndicator("Thinking")
        if not DEBUG_MODE: indicator.start()
        
        result = ""
        try:
            # 1. CLASSIFY INTENT (Improved prompt)
            intent_prompt = (
                "Classify the intent into one of: ['listar', 'consultar_precio', 'actualizar_precio', 'descripcion', 'revertir', 'contar', 'ordenar', 'general']\n"
                "EXAMPLES:\n"
                "User: 'How much is the gift card?' -> {\"category\": \"consultar_precio\"}\n"
                "User: 'Set the gift card price to 50' -> {\"category\": \"actualizar_precio\"}\n"
                "User: 'How many products are there?' -> {\"category\": \"contar\"}\n"
                "User: 'Show me the list without prices' -> {\"category\": \"listar\"}\n"
                "User: 'I want to see the catalog with prices' -> {\"category\": \"listar\"}\n"
                f"User: '{user_input}'\n"
                "Output JSON:"
            )
            
            raw = str(await self.kernel.invoke_prompt(intent_prompt))
            data = self._clean_json(raw)
            intent = data.get("category", "general") if data else "general"
            
            if DEBUG_MODE: 
                indicator.stop()
                print(f"\nDEBUG Intent: {intent}")
                indicator.start()

            # 2. EJECUTAR ACCIÓN
            if intent == "listar": 
                u_lower = user_input.lower()
                # Keywords to hide prices
                no_price_keywords = ["sin precio", "no precio", "sin el precio", "oculta el precio", "ocultar precio", "no quiero ver los precios", "sin coste"]
                
                if any(k in u_lower for k in no_price_keywords):
                    show_p = False
                else:
                    # Si hay duda, el default es mostrar precios (True), salvo que el LLM diga lo contrario
                    # Pero para hacerlo rápido y robusto, asumimos True a menos que sea explícito
                    show_p = True
                
                result = self.plugin.get_products_list(show_price=show_p)

            elif intent == "contar": result = self.plugin.count_products()
            elif intent == "ordenar": result = self.plugin.sort_products()
            
            elif intent == "consultar_precio":
                ext_prompt = f"Extract only the product name from: '{user_input}'. Respond only with the name."
                pname = str(await self.kernel.invoke_prompt(ext_prompt)).strip()
                pid = pname
                if not pid.isdigit():
                    found = self.plugin.find_id_by_name(pname)
                    pid = found if found else pid
                if pid and pid.isdigit(): result = self.plugin.get_product_price(pid)
                else: result = Colors.red(f"No encontré el producto '{pname}'")

            elif intent == "actualizar_precio":
                ext_prompt = ("Extract JSON: {\"product\": \"name or id\", \"price\": \"number\"}. " f"Input: {user_input}")
                data = self._clean_json(str(await self.kernel.invoke_prompt(ext_prompt)))
                if data and data.get("product") and data.get("price"):
                    pid = str(data.get("product"))
                    if not pid.isdigit():
                        found = self.plugin.find_id_by_name(pid)
                        pid = found if found else pid
                    if pid.isdigit(): result = self.plugin.update_product_price(pid, data.get("price"))
                    else: result = Colors.red("Product not found.")
                else: result = Colors.red("Incomplete data.")

            elif intent == "descripcion":
                ext_prompt = ("Extract JSON: {\"product\": \"name or id\", \"text\": \"new description\"}. " f"Input: {user_input}")
                data = self._clean_json(str(await self.kernel.invoke_prompt(ext_prompt)))
                if data and data.get("product") and data.get("text"):
                    pid = str(data.get("product"))
                    if not pid.isdigit():
                        found = self.plugin.find_id_by_name(pid)
                        pid = found if found else pid
                    if pid.isdigit(): result = self.plugin.update_description(pid, data.get("text"))
                    else: result = Colors.red("Product not found.")
                else: result = Colors.red("Incomplete data.")

            elif intent == "revertir":
                prompt = f"Extract ID or name from: {user_input}. Return only text."
                pid = str(await self.kernel.invoke_prompt(prompt)).strip()
                if not pid.isdigit():
                    found = self.plugin.find_id_by_name(pid)
                    pid = found if found else pid
                if pid.isdigit(): result = self.plugin.revert_price(pid)
                else: result = Colors.red("Product not found.")

            else: result = str(await self.kernel.invoke_prompt(user_input))

        except Exception as e:
            result = f"Error: {e}"
            if DEBUG_MODE: traceback.print_exc()
        
        finally:
            indicator.stop()
            sys.stdout.flush()
            print(f"\n{Colors.cyan(result)}\n")

# ============================================
# MAIN LOOP
# ============================================

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()

    async def main():
        global DEBUG_MODE
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--debug', action='store_true')
        args = parser.parse_args()
        DEBUG_MODE = args.debug

        print(Colors.blue("=== SHOPIFY AI AGENT (v2.5 FINAL) ==="))
        
        # Verificar que WSO2 Gateway está configurado
        gw_url = os.getenv('WSO2_GW_URL')
        if not gw_url:
            return print(Colors.red("Missing WSO2_GW_URL"))
        
        # Obtener token de WSO2 Gateway primero
        plugin = ShopifyPlugin()
        wso2_token = plugin._get_token()
        
        if not wso2_token:
            return print(Colors.red("Error: No se pudo obtener token de WSO2 Gateway"))
        
        # Configurar OpenAI para usar WSO2 AI Gateway
        # El endpoint completo de OpenAI en WSO2 es: {WSO2_GW_URL}/openaiapi/2.3.0/chat/completions
        # El SDK de OpenAI agrega automáticamente /v1/chat/completions al base_url
        # WSO2 espera: /openaiapi/2.3.0/chat/completions (sin /v1)
        # Necesitamos interceptar y quitar el /v1 de la URL
        openai_gateway_base = f"{gw_url}/openaiapi/2.3.0"
        
        kernel = sk.Kernel()
        try:
            # Crear un cliente HTTP personalizado que intercepta las URLs
            # y quita el /v1 antes de enviar a WSO2
            class WSO2HTTPClient(httpx.AsyncClient):
                def __init__(self, *args, **kwargs):
                    # No pasar base_url aquí - AsyncOpenAI lo manejará
                    kwargs.pop('base_url', None)
                    # IMPORTANTE: verify=False para certificados autofirmados
                    kwargs['verify'] = False
                    super().__init__(*args, **kwargs)
                    self.wso2_base_url = openai_gateway_base
                    self.wso2_token = wso2_token
                    self.plugin = plugin  # Guardar referencia al plugin para refrescar token
                    self.token_lock = asyncio.Lock()  # Lock para refrescar token de forma thread-safe
                
                async def _refresh_token_if_needed(self):
                    """Refrescar token si es necesario"""
                    # Por ahora, siempre usar el token actual
                    # En el futuro se puede agregar lógica para refrescar si expira
                    current_token = self.plugin._get_token()
                    if current_token:
                        self.wso2_token = current_token
                        if DEBUG_MODE:
                            print(Colors.cyan(f"[WSO2 Interceptor] Token refrescado"))
                
                async def send(self, request, **kwargs):
                    # Refrescar token antes de cada request para asegurar que esté vigente
                    async with self.token_lock:
                        await self._refresh_token_if_needed()
                    
                    # Interceptar en send() - aquí es donde AsyncOpenAI envía las requests
                    url_str = str(request.url)
                    
                    if DEBUG_MODE:
                        print(Colors.cyan(f"[WSO2 Interceptor] URL original: {url_str}"))
                    
                    # Interceptar y quitar /v1/chat/completions
                    if "/v1/chat/completions" in url_str:
                        new_url_str = url_str.replace("/v1/chat/completions", "/chat/completions")
                        if DEBUG_MODE:
                            print(Colors.cyan(f"[WSO2 Interceptor] URL corregida: {url_str} -> {new_url_str}"))
                        # Crear nuevo request con URL corregida
                        request.url = httpx.URL(new_url_str)
                    
                    # Reemplazar siempre el token con el de WSO2 (AsyncOpenAI puede agregar uno con api_key)
                    request.headers["Authorization"] = f"Bearer {self.wso2_token}"
                    if DEBUG_MODE:
                        print(Colors.cyan(f"[WSO2 Interceptor] Token WSO2: {self.wso2_token[:30]}..."))
                        print(Colors.cyan(f"[WSO2 Interceptor] Enviando a: {request.url}"))
                    
                    # verify=False ya está configurado en __init__, no se pasa en send()
                    try:
                        response = await super().send(request, **kwargs)
                        # Si recibimos 401, intentar refrescar token y reintentar
                        if response.status_code == 401:
                            if DEBUG_MODE:
                                print(Colors.yellow(f"[WSO2 Interceptor] 401 recibido, refrescando token..."))
                            async with self.token_lock:
                                await self._refresh_token_if_needed()
                            # Reintentar con nuevo token
                            request.headers["Authorization"] = f"Bearer {self.wso2_token}"
                            response = await super().send(request, **kwargs)
                        return response
                    except Exception as e:
                        if DEBUG_MODE:
                            print(Colors.red(f"[WSO2 Interceptor] Error: {e}"))
                        raise
            
            # Crear cliente HTTP personalizado con interceptación
            # IMPORTANTE: verify=False para certificados autofirmados de localhost
            http_client = WSO2HTTPClient(
                timeout=30.0,
                verify=False  # Para certificados autofirmados de localhost
            )
            
            # Crear cliente AsyncOpenAI con el HTTP client personalizado
            # El base_url incluye /v1 para que el SDK funcione, pero el interceptor lo quitará
            openai_client = AsyncOpenAI(
                api_key="wso2-gateway-dummy",  # Dummy key, WSO2 maneja auth real
                base_url=f"{openai_gateway_base}/v1",  # SDK agregará /chat/completions
                http_client=http_client,
                timeout=30.0,
                max_retries=2
            )
            
            # Configurar Semantic Kernel con el cliente AsyncOpenAI
            kernel.add_service(OpenAIChatCompletion(
                service_id="openai",
                ai_model_id="gpt-4o-mini",
                async_client=openai_client
            ))
            
            print(Colors.green(f"✓ OpenAI configurado para usar WSO2 Gateway"))
            print(Colors.blue(f"  Gateway Base URL: {openai_gateway_base}"))
            print(Colors.blue(f"  Endpoint corregido: {openai_gateway_base}/chat/completions"))
            print(Colors.blue(f"  Token WSO2: {wso2_token[:30]}..."))
        except Exception as e:
            return print(Colors.red(f"OpenAI error: {e}"))

        plugin = ShopifyPlugin()
        
        # PASO 1: Validar usuario contra Identity Server (si hay credenciales configuradas)
        username = os.getenv("WSO2_USERNAME")
        if username:
            if not plugin._validate_user_against_is():
                print(Colors.red("✗ El agente requiere validación de usuario contra Identity Server"))
                print(Colors.yellow("  Por favor verifica:"))
                print(Colors.yellow("  - WSO2_USERNAME y WSO2_PASSWORD son correctos"))
                print(Colors.yellow("  - WSO2_CLIENT_ID y WSO2_CLIENT_SECRET son correctos para Identity Server"))
                print(Colors.yellow("  - WSO2_IS_TOKEN_ENDPOINT (por defecto: https://localhost:9443/oauth2/token)"))
                print(Colors.yellow("  - El usuario existe en WSO2 Identity Server"))
                print(Colors.yellow("  - El grant type 'password' está habilitado para el cliente"))
                print(Colors.yellow("  - WSO2 Identity Server está corriendo y accesible"))
                print(Colors.red("\n✗ El agente no puede continuar sin validación de usuario. Saliendo..."))
                return
            else:
                print(Colors.green(f"✓ Usuario '{username}' autenticado exitosamente en WSO2 Identity Server"))
        
        # PASO 2: Verificar que se puede obtener token de APIM para las llamadas API
        token = plugin._get_token()
        if not token:
            print(Colors.red("✗ Error: No se pudo obtener token de APIM Gateway"))
            print(Colors.yellow("  Por favor verifica:"))
            print(Colors.yellow("  - WSO2_TOKEN_ENDPOINT es correcto"))
            print(Colors.yellow("  - WSO2_CONSUMER_KEY y WSO2_CONSUMER_SECRET son correctos (para APIM)"))
            print(Colors.yellow("  - WSO2 APIM Gateway está corriendo y accesible"))
            print(Colors.red("\n✗ El agente no puede continuar sin token de APIM. Saliendo..."))
            return
        
        agent = Agent(kernel, plugin)
        print(Colors.green("Ready. Type 'exit' (or 'salir') to quit."))

        while True:
            try:
                u = input(f"{Colors.blue('You >')} ")
                if u.lower() in ['exit', 'quit', 'salir']: break
                if u.strip(): await agent.run(u)
            except KeyboardInterrupt: break
    
    try: asyncio.run(main())
    except: pass
