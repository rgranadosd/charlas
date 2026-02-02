#!/usr/bin/env python3
"""
Agente Shopify Simplificado - Sin WSO2 OAuth
Funciona directamente con Shopify API sin autenticación OAuth
"""

import os
import requests
import asyncio
import json
import argparse
import time
import sys
import traceback
import re
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function
from pathlib import Path

# Cargar .env
env_file = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_file)

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

class PriceMemory:
    def __init__(self): self.history = {}
    def remember(self, pid, old, new): self.history[pid] = {'old': old, 'new': new}
    def get_old(self, pid): return self.history.get(pid, {}).get('old')

class SimpleShopifyPlugin:
    def __init__(self):
        self.memory = PriceMemory()
        # Verificar configuración inmediatamente
        self.shopify_token = os.getenv("SHOPIFY_API_TOKEN")
        self.shopify_store = os.getenv("SHOPIFY_STORE_URL", "https://rafa-ecommerce.myshopify.com")
        
        if not self.shopify_token:
            raise ValueError("SHOPIFY_API_TOKEN no configurado en .env")
        
        print(Colors.blue("Plugin Shopify inicializado"))
        print(Colors.green("Shopify conectado - verificando..."))
        
        # Test inmediato
        try:
            count_result = self._api("GET", "/products/count.json")
            if "count" in count_result:
                print(Colors.green(f"Shopify conectado - {count_result['count']} productos"))
            else:
                print(Colors.yellow("Shopify conectado pero respuesta inesperada"))
        except Exception as e:
            print(Colors.red(f"Error conectando a Shopify: {e}"))

    def _api(self, method, path, data=None):
        url = f"{self.shopify_store}/admin/api/2024-01{path}"
        headers = {
            "X-Shopify-Access-Token": self.shopify_token,
            "Content-Type": "application/json"
        }
        
        if DEBUG_MODE:
            print(Colors.cyan(f"[API] {method} {url}"))
        
        try:
            if method == 'GET': 
                r = requests.get(url, headers=headers, timeout=10)
            else: 
                r = requests.put(url, headers=headers, json=data, timeout=10)
            
            if r.status_code not in [200, 201]:
                if DEBUG_MODE:
                    print(Colors.red(f"API Error {r.status_code}: {r.text}"))
                return {"error": f"Shopify API Error {r.status_code}"}
            
            return r.json() if r.content else {}
            
        except Exception as e: 
            if DEBUG_MODE:
                print(Colors.red(f"Exception en API call: {str(e)}"))
            return {"error": f"Error conectando a Shopify: {str(e)}"}

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
        if "error" in data:
            return Colors.red(f"Error: {data['error']}")
            
        if "products" in data:
            lines = []
            for p in data["products"]:
                price_txt = f" - ${p['variants'][0]['price']}" if show_price else ""
                lines.append(f"- ID: {p['id']} - {p['title']}{price_txt}")
            return "\n".join(lines)
        return Colors.red("Error al listar productos")

    @kernel_function(name="update_product_price")
    def update_product_price(self, product_id, price):
        curr = self._api("GET", f"/products/{product_id}.json")
        if "error" in curr:
            return Colors.red(f"Error: {curr['error']}")
        if "product" not in curr: 
            return Colors.red("Producto no encontrado")
            
        vid = curr["product"]["variants"][0]["id"]
        old = curr["product"]["variants"][0]["price"]
        payload = {"product": {"id": int(product_id), "variants": [{"id": vid, "price": str(price)}]}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        
        if "error" in res:
            return Colors.red(f"Error: {res['error']}")
        if "product" in res:
            self.memory.remember(product_id, old, price)
            return Colors.green(f"Precio actualizado: ${old} -> ${price}")
        return Colors.red("Error al actualizar precio")

    @kernel_function(name="update_description")
    def update_description(self, product_id, text):
        payload = {"product": {"id": int(product_id), "body_html": text}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        if "error" in res:
            return Colors.red(f"Error: {res['error']}")
        return Colors.green("Descripción actualizada") if "product" in res else Colors.red("Error")

    @kernel_function(name="revert_price")
    def revert_price(self, product_id):
        old = self.memory.get_old(product_id)
        if old: 
            return self.update_product_price(product_id, old)
        return Colors.red("No hay historial de precios para este producto")

    @kernel_function(name="count_products")
    def count_products(self):
        d = self._api("GET", "/products/count.json")
        if "error" in d:
            return Colors.red(f"Error: {d['error']}")
        return f"Total: {d.get('count', 0)} productos"

    @kernel_function(name="sort_products")
    def sort_products(self):
        data = self._api("GET", "/products.json")
        if "error" in data:
            return Colors.red(f"Error: {data['error']}")
        if "products" in data:
            prods = sorted(data["products"], key=lambda x: float(x['variants'][0]['price']), reverse=True)
            lines = [f"- ${p['variants'][0]['price']} - {p['title']}" for p in prods]
            return "Productos ordenados (Mayor a menor):\n" + "\n".join(lines)
        return Colors.red("Error al ordenar productos")

class SimpleAgent:
    def __init__(self, kernel, plugin):
        self.kernel = kernel
        self.plugin = plugin

    def _clean_json(self, text):
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            return json.loads(match.group()) if match else json.loads(text)
        except: 
            return None

    async def run(self, user_input):        
        result = ""
        try:
            # 1. Clasificar intención
            intent_prompt = (
                "Clasifica la intención en: ['listar', 'consultar_precio', 'actualizar_precio', 'descripcion', 'revertir', 'contar', 'ordenar', 'general']\n"
                "EJEMPLOS:\n"
                "User: 'Cuanto vale la gift card?' -> {\"category\": \"consultar_precio\"}\n"
                "User: 'Pon la Gift Card a 50' -> {\"category\": \"actualizar_precio\"}\n"
                "User: 'Cuantos productos hay?' -> {\"category\": \"contar\"}\n"
                "User: 'Dame la lista' -> {\"category\": \"listar\"}\n"
                f"User: '{user_input}'\n"
                "Output JSON:"
            )
            
            raw = str(await self.kernel.invoke_prompt(intent_prompt))
            data = self._clean_json(raw)
            intent = data.get("category", "general") if data else "general"
            
            if DEBUG_MODE: 
                print(f"DEBUG Intent: {intent}")

            # 2. Ejecutar acción
            if intent == "listar": 
                u_lower = user_input.lower()
                no_price_keywords = ["sin precio", "no precio", "sin el precio", "oculta el precio"]
                show_p = not any(k in u_lower for k in no_price_keywords)
                result = self.plugin.get_products_list(show_price=show_p)

            elif intent == "contar": 
                result = self.plugin.count_products()
            elif intent == "ordenar": 
                result = self.plugin.sort_products()
            
            elif intent == "consultar_precio":
                ext_prompt = f"Extrae solo el nombre del producto de: '{user_input}'. Responde solo con el nombre."
                pname = str(await self.kernel.invoke_prompt(ext_prompt)).strip()
                pid = pname
                if not pid.isdigit():
                    found = self.plugin.find_id_by_name(pname)
                    pid = found if found else pid
                if pid and pid.isdigit(): 
                    result = self.plugin.get_product_price(pid)
                else: 
                    result = Colors.red(f"No encontré el producto '{pname}'")

            elif intent == "actualizar_precio":
                ext_prompt = f"Extrae JSON: {{\"product\": \"nombre o id\", \"price\": \"numero\"}}. Input: {user_input}"
                data = self._clean_json(str(await self.kernel.invoke_prompt(ext_prompt)))
                if data and data.get("product") and data.get("price"):
                    pid = str(data.get("product"))
                    if not pid.isdigit():
                        found = self.plugin.find_id_by_name(pid)
                        pid = found if found else pid
                    if pid and pid.isdigit(): 
                        result = self.plugin.update_product_price(pid, data.get("price"))
                    else: 
                        result = Colors.red("Producto no encontrado.")
                else: 
                    result = Colors.red("Datos incompletos.")

            elif intent == "descripcion":
                ext_prompt = f"Extrae JSON: {{\"product\": \"nombre o id\", \"text\": \"nueva descripcion\"}}. Input: {user_input}"
                data = self._clean_json(str(await self.kernel.invoke_prompt(ext_prompt)))
                if data and data.get("product") and data.get("text"):
                    pid = str(data.get("product"))
                    if not pid.isdigit():
                        found = self.plugin.find_id_by_name(pid)
                        pid = found if found else pid
                    if pid and pid.isdigit(): 
                        result = self.plugin.update_description(pid, data.get("text"))
                    else: 
                        result = Colors.red("Producto no encontrado.")
                else: 
                    result = Colors.red("Datos incompletos.")

            elif intent == "revertir":
                prompt = f"Extrae ID o nombre de: {user_input}. Solo texto."
                pid = str(await self.kernel.invoke_prompt(prompt)).strip()
                if not pid.isdigit():
                    found = self.plugin.find_id_by_name(pid)
                    pid = found if found else pid
                if pid and pid.isdigit(): 
                    result = self.plugin.revert_price(pid)
                else: 
                    result = Colors.red("Producto no encontrado.")

            else: 
                result = str(await self.kernel.invoke_prompt(user_input))

        except Exception as e:
            result = f"Error: {e}"
            if DEBUG_MODE: 
                traceback.print_exc()
        
        print(f"\n{Colors.cyan(result)}\n")

async def main():
    global DEBUG_MODE
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Modo debug')
    args = parser.parse_args()
    DEBUG_MODE = args.debug

    print(Colors.blue("=== AGENTE SHOPIFY SIMPLE ==="))
    if DEBUG_MODE: 
        print(Colors.cyan("[DEBUG MODE ON]"))
    
    if not os.getenv("OPENAI_API_KEY"): 
        return print(Colors.red("Falta OPENAI_API_KEY en .env"))

    kernel = sk.Kernel()
    try:
        kernel.add_service(OpenAIChatCompletion(
            service_id="openai", 
            api_key=os.getenv("OPENAI_API_KEY"), 
            ai_model_id="gpt-4o-mini"
        ))
    except: 
        return print(Colors.red("Error configurando OpenAI"))

    try:
        plugin = SimpleShopifyPlugin()
        agent = SimpleAgent(kernel, plugin)
        print(Colors.green("Listo. Escribe 'salir' para terminar."))

        while True:
            try:
                u = input(f"{Colors.blue('Tú >')} ")
                if u.lower() in ['exit', 'quit', 'salir']: 
                    break
                if u.strip(): 
                    await agent.run(u)
            except KeyboardInterrupt: 
                break
    except Exception as e:
        print(Colors.red(f"Error inicializando: {e}"))

if __name__ == "__main__":
    try: 
        asyncio.run(main())
    except: 
        pass