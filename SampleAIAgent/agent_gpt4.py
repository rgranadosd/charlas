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
    def cyan(text): return f"{Colors.CYAN}{text}{Colors.RESET}"

class ThinkingIndicator:
    """Animación de carga robusta que no bloquea."""
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

    def _get_token(self):
        url = os.getenv("WSO2_TOKEN_ENDPOINT")
        key = os.getenv("WSO2_CONSUMER_KEY")
        secret = os.getenv("WSO2_CONSUMER_SECRET")
        if not all([url, key, secret]): return None
        creds = base64.b64encode(f"{key}:{secret}".encode()).decode()
        headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/x-www-form-urlencoded"}
        try:
            r = requests.post(url, headers=headers, data="grant_type=client_credentials", verify=False)
            return r.json().get("access_token") if r.status_code == 200 else None
        except: return None

    def _api(self, method, path, data=None):
        token = self._get_token()
        if not token: return {"error": "Token Error"}
        url = f"{os.getenv('WSO2_GW_URL')}/shopify/1.0.0{path}"
        headers = {"Authorization": f"Bearer {token}", "X-Shopify-Access-Token": os.getenv("SHOPIFY_API_TOKEN"), "Content-Type": "application/json"}
        try:
            if method == 'GET': r = requests.get(url, headers=headers, verify=False)
            else: r = requests.put(url, headers=headers, json=data, verify=False)
            return r.json() if r.content else {}
        except Exception as e: return {"error": str(e)}

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
            return f"El precio de '{title}' es ${price}"
        return Colors.red("Producto no encontrado")

    @kernel_function(name="get_products_list")
    def get_products_list(self, show_price=True):
        data = self._api("GET", "/products.json")
        if "products" in data:
            lines = []
            for p in data["products"]:
                price_txt = f" - ${p['variants'][0]['price']}" if show_price else ""
                lines.append(f"- ID: {p['id']} - {p['title']}{price_txt}")
            return "\n".join(lines)
        return "Error al listar"

    @kernel_function(name="update_product_price")
    def update_product_price(self, product_id, price):
        curr = self._api("GET", f"/products/{product_id}.json")
        if "product" not in curr: return Colors.red("Producto no encontrado")
        vid = curr["product"]["variants"][0]["id"]
        old = curr["product"]["variants"][0]["price"]
        payload = {"product": {"id": int(product_id), "variants": [{"id": vid, "price": str(price)}]}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        if "product" in res:
            self.memory.remember(product_id, old, price)
            return Colors.green(f"Precio actualizado: ${old} -> ${price}")
        return Colors.red("Error al actualizar")

    @kernel_function(name="update_description")
    def update_description(self, product_id, text):
        payload = {"product": {"id": int(product_id), "body_html": text}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        return Colors.green("Descripción actualizada") if "product" in res else Colors.red("Error")

    @kernel_function(name="revert_price")
    def revert_price(self, product_id):
        old = self.memory.get_old(product_id)
        if old: return self.update_product_price(product_id, old)
        return Colors.red("No hay historial")

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
            return "Productos ordenados (Mayor a menor):\n" + "\n".join(lines)
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
        # Instanciamos el indicador nuevo CADA VEZ para evitar errores de hilo
        indicator = ThinkingIndicator("Thinking")
        if not DEBUG_MODE: indicator.start()
        
        result = ""
        try:
            # 1. CLASIFICAR INTENCIÓN (Prompt Mejorado)
            intent_prompt = (
                "Clasifica la intención en: ['listar', 'consultar_precio', 'actualizar_precio', 'descripcion', 'revertir', 'contar', 'ordenar', 'general']\n"
                "EJEMPLOS:\n"
                "User: 'Cuanto vale la gift card?' -> {\"category\": \"consultar_precio\"}\n"
                "User: 'Pon la Gift Card a 50' -> {\"category\": \"actualizar_precio\"}\n"
                "User: 'Cuantos productos hay?' -> {\"category\": \"contar\"}\n"
                "User: 'Dame la lista sin precios' -> {\"category\": \"listar\"}\n"
                "User: 'Quiero ver el catálogo con precios' -> {\"category\": \"listar\"}\n"
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
                # Palabras clave para ocultar precios
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
                ext_prompt = f"Extrae solo el nombre del producto de: '{user_input}'. Responde solo con el nombre."
                pname = str(await self.kernel.invoke_prompt(ext_prompt)).strip()
                pid = pname
                if not pid.isdigit():
                    found = self.plugin.find_id_by_name(pname)
                    pid = found if found else pid
                if pid and pid.isdigit(): result = self.plugin.get_product_price(pid)
                else: result = Colors.red(f"No encontré el producto '{pname}'")

            elif intent == "actualizar_precio":
                ext_prompt = ("Extrae JSON: {\"product\": \"nombre o id\", \"price\": \"numero\"}. " f"Input: {user_input}")
                data = self._clean_json(str(await self.kernel.invoke_prompt(ext_prompt)))
                if data and data.get("product") and data.get("price"):
                    pid = str(data.get("product"))
                    if not pid.isdigit():
                        found = self.plugin.find_id_by_name(pid)
                        pid = found if found else pid
                    if pid.isdigit(): result = self.plugin.update_product_price(pid, data.get("price"))
                    else: result = Colors.red("Producto no encontrado.")
                else: result = Colors.red("Datos incompletos.")

            elif intent == "descripcion":
                ext_prompt = ("Extrae JSON: {\"product\": \"nombre o id\", \"text\": \"nueva descripcion\"}. " f"Input: {user_input}")
                data = self._clean_json(str(await self.kernel.invoke_prompt(ext_prompt)))
                if data and data.get("product") and data.get("text"):
                    pid = str(data.get("product"))
                    if not pid.isdigit():
                        found = self.plugin.find_id_by_name(pid)
                        pid = found if found else pid
                    if pid.isdigit(): result = self.plugin.update_description(pid, data.get("text"))
                    else: result = Colors.red("Producto no encontrado.")
                else: result = Colors.red("Datos incompletos.")

            elif intent == "revertir":
                prompt = f"Extrae ID o nombre de: {user_input}. Solo texto."
                pid = str(await self.kernel.invoke_prompt(prompt)).strip()
                if not pid.isdigit():
                    found = self.plugin.find_id_by_name(pid)
                    pid = found if found else pid
                if pid.isdigit(): result = self.plugin.revert_price(pid)
                else: result = Colors.red("Producto no encontrado.")

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

        print(Colors.blue("=== AGENTE SHOPIFY IA (v2.5 FINAL) ==="))
        if not os.getenv("OPENAI_API_KEY"): return print(Colors.red("Falta API KEY"))

        kernel = sk.Kernel()
        try:
            kernel.add_service(OpenAIChatCompletion(service_id="openai", api_key=os.getenv("OPENAI_API_KEY"), ai_model_id="gpt-4o-mini"))
        except: return print(Colors.red("Error OpenAI"))

        plugin = ShopifyPlugin()
        agent = Agent(kernel, plugin)
        print(Colors.green("Listo. Escribe 'salir' para terminar."))

        while True:
            try:
                u = input(f"{Colors.blue('Tú >')} ")
                if u.lower() in ['exit', 'quit', 'salir']: break
                if u.strip(): await agent.run(u)
            except KeyboardInterrupt: break
    
    try: asyncio.run(main())
    except: pass
