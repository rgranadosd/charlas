"""Shopify domain plugin and price memory helpers."""

from __future__ import annotations

import os
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

import requests
from semantic_kernel.functions import kernel_function

from config import _auth_trace_enabled, get_debug_mode
from oauth_session import OAuthCallbackHandler, OAuthClient
from ui_console import Colors


class PriceMemory:
    def __init__(self):
        self.history = {}

    def remember(self, pid, old, new):
        self.history[pid] = {"old": old, "new": new}

    def get_old(self, pid):
        return self.history.get(pid, {}).get("old")


class ShopifyPlugin:
    def __init__(self, force_auth: bool = False):
        self.memory = PriceMemory()
        self.oauth = OAuthClient(force_auth=force_auth)
        self._token_cache = None
        self._token_initialized = False
        self._user_permissions = set()
        self._force_auth = force_auth

        if force_auth:
            self._user_permissions = set()
            self._token_initialized = False

        if get_debug_mode():
            print(Colors.cyan("[DEBUG] ShopifyPlugin inicializado (sin autenticación aún)"))

    def _get_token(self):
        if not self._token_initialized or self._force_auth:
            if self._force_auth:
                if _auth_trace_enabled():
                    print(Colors.debug("Forzando nueva autenticación completa..."))
                self._user_permissions = set()
            else:
                if _auth_trace_enabled():
                    print(Colors.debug("Autenticación OAuth iniciada..."))

            self._token_initialized = True
            token = self.oauth.ensure_token()

            if not token:
                print(Colors.red("No se pudo obtener token OAuth. Verifica WSO2 Identity Server."))
                self._user_permissions = set()
                return None

            self._force_auth = False
            try:
                self.oauth.store.force_auth = False
            except Exception:
                pass

            if hasattr(OAuthCallbackHandler, "user_permissions") and OAuthCallbackHandler.user_permissions is not None:
                self._user_permissions = OAuthCallbackHandler.user_permissions
                if self._user_permissions and get_debug_mode():
                    print(Colors.green(f"Permisos OAuth cargados: {sorted(self._user_permissions)}"))
                elif not self._user_permissions:
                    print(Colors.yellow("Usuario autenticado pero sin permisos."))
            else:
                print(Colors.yellow("No se pudieron verificar permisos WSO2."))
                self._user_permissions = set()

            return token

        return self.oauth.ensure_token()

    def _has_permission(self, required_permission):
        return required_permission in self._user_permissions

    def _check_permission(self, required_permission, action_name):
        if not self._token_initialized:
            token = self._get_token()
            if not token:
                return Colors.red(f"Necesitas iniciar sesión para {action_name}.")

        if not self._has_permission(required_permission):
            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] Permisos actuales: {sorted(self._user_permissions)}"))
                print(Colors.cyan(f"[DEBUG] Permiso requerido: {required_permission}"))
                print(Colors.cyan(f"[DEBUG] Token inicializado: {self._token_initialized}"))
            return Colors.red(f"No tienes permisos para {action_name}.")
        return None

    def _api(self, method, path, data=None):
        shopify_token = os.getenv("SHOPIFY_API_TOKEN")
        if not shopify_token:
            return {"error": "SHOPIFY_API_TOKEN no configurado en el archivo .env"}

        shopify_store = os.getenv("SHOPIFY_STORE_URL", "https://rafa-ecommerce.myshopify.com")
        url = f"{shopify_store}/admin/api/2024-01{path}"
        headers = {
            "X-Shopify-Access-Token": shopify_token,
            "Content-Type": "application/json",
        }

        if get_debug_mode():
            print(Colors.cyan(f"[API] {method} {url}"))
            print(Colors.cyan(f"[DEBUG] Token Shopify configurado: {shopify_token[:10]}..."))

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, verify=False)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, verify=False)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, verify=False)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, verify=False)
            else:
                return {"error": f"Método no soportado: {method}"}

            if response.status_code == 401:
                error_msg = "Token de Shopify inválido o expirado. Verifica SHOPIFY_API_TOKEN en .env"
                print(Colors.red(f"[SHOPIFY ERROR 401] {error_msg}"))
                if get_debug_mode():
                    print(Colors.red(f"Response: {response.text}"))
                return {"error": error_msg}
            if response.status_code == 403:
                error_msg = "Sin permisos para esta operación en Shopify. Verifica los scopes del token."
                print(Colors.red(f"[SHOPIFY ERROR 403] {error_msg}"))
                return {"error": error_msg}
            if response.status_code not in [200, 201]:
                if get_debug_mode():
                    print(Colors.red(f"API Error {response.status_code}: {response.text}"))
                return {"error": f"Shopify API Error {response.status_code}: {response.text[:200]}"}

            return response.json() if response.content else {}
        except requests.exceptions.ConnectionError:
            error_msg = f"No se pudo conectar a Shopify. Verifica SHOPIFY_STORE_URL: {shopify_store}"
            print(Colors.red(f"[CONNECTION ERROR] {error_msg}"))
            return {"error": error_msg}
        except Exception as exc:
            if get_debug_mode():
                print(Colors.red(f"Exception en API call: {str(exc)}"))
            return {"error": f"Error inesperado: {str(exc)}"}

    def find_id_by_name(self, name):
        permission_error = self._check_permission("View Products", "buscar productos")
        if permission_error:
            return None

        data = self._api("GET", "/products.json")
        if "products" in data:
            for product in data["products"]:
                if name.lower() in product["title"].lower():
                    return str(product["id"])
        return None

    def get_product_price(self, product_id):
        permission_error = self._check_permission("View Products", "consultar precios de productos")
        if permission_error:
            return permission_error

        current = self._api("GET", f"/products/{product_id}.json")
        if "product" in current:
            title = current["product"]["title"]
            price = current["product"]["variants"][0]["price"]
            return f"El precio de '{title}' es {price}€"
        return Colors.red("Producto no encontrado")

    @kernel_function(name="get_products_list")
    def get_products_list(self, show_price=True):
        permission_error = self._check_permission("View Products", "ver productos del catálogo")
        if permission_error:
            return permission_error

        data = self._api("GET", "/products.json")
        if "products" in data:
            lines = []
            for product in data["products"]:
                price_txt = f" - {product['variants'][0]['price']}€" if show_price else ""
                lines.append(f"- ID: {product['id']} - {product['title']}{price_txt}")
            return "\n".join(lines)
        return "Error al listar"

    def get_product_titles(self, limit: int = 50):
        permission_error = self._check_permission("View Products", "leer productos del catálogo")
        if permission_error:
            return {"error": permission_error}

        data = self._api("GET", f"/products.json?limit={int(limit)}")
        if "products" in data:
            return [product.get("title") for product in data["products"] if product.get("title")]
        if "error" in data:
            return {"error": data["error"]}
        return {"error": "No se pudieron obtener productos"}

    @kernel_function(name="update_product_price")
    def update_product_price(self, product_id, price):
        permission_error = self._check_permission("Update Prices", "modificar precios de productos")
        if permission_error:
            return permission_error

        current = self._api("GET", f"/products/{product_id}.json")
        if "product" not in current:
            return Colors.red("Producto no encontrado")
        variant_id = current["product"]["variants"][0]["id"]
        old = current["product"]["variants"][0]["price"]
        payload = {"product": {"id": int(product_id), "variants": [{"id": variant_id, "price": str(price)}]}}
        response = self._api("PUT", f"/products/{product_id}.json", payload)
        if "product" in response:
            self.memory.remember(product_id, old, price)
            return Colors.green(f"Precio actualizado: {old}€ -> {price}€")
        return Colors.red("Error al actualizar")

    def update_product_price_by_percent(self, product_id: str, percent: float):
        permission_error = self._check_permission("Update Prices", "modificar precios de productos")
        if permission_error:
            return permission_error

        current = self._api("GET", f"/products/{product_id}.json")
        if "product" not in current:
            return Colors.red("Producto no encontrado")

        title = current["product"].get("title", "")
        old_str = str(current["product"]["variants"][0]["price"])
        try:
            old = Decimal(old_str)
        except Exception:
            return Colors.red("No pude leer el precio actual del producto")

        factor = Decimal("1") + (Decimal(str(percent)) / Decimal("100"))
        new = (old * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        response = self.update_product_price(product_id, str(new))
        if response.startswith(Colors.GREEN):
            return Colors.green(f"Precio actualizado ({percent:+g}%): {old_str}€ -> {new}€ ({title})")
        return response

    def _get_or_create_homepage_collection_id(self) -> Optional[str]:
        data = self._api("GET", "/custom_collections.json?limit=250")
        if "custom_collections" in data:
            for collection in data["custom_collections"]:
                title = (collection.get("title") or "").strip().lower()
                if title == "home page":
                    return str(collection.get("id"))

        payload = {"custom_collection": {"title": "Home Page"}}
        created = self._api("POST", "/custom_collections.json", payload)
        if "custom_collection" in created:
            return str(created["custom_collection"].get("id"))
        return None

    def _get_homepage_collection_id(self) -> Optional[str]:
        data = self._api("GET", "/custom_collections.json?limit=250")
        if "custom_collections" in data:
            for collection in data["custom_collections"]:
                title = (collection.get("title") or "").strip().lower()
                if title == "home page":
                    return str(collection.get("id"))
        return None

    def _get_collect_id(self, product_id: str, collection_id: str) -> Optional[str]:
        data = self._api("GET", f"/collects.json?product_id={int(product_id)}&collection_id={int(collection_id)}")
        if "collects" in data and data["collects"]:
            return str(data["collects"][0].get("id"))
        return None

    def _get_homepage_products(self) -> List[str]:
        collection_id = self._get_homepage_collection_id()
        if not collection_id:
            return []

        data = self._api("GET", f"/collects.json?collection_id={int(collection_id)}&limit=250")
        if "collects" not in data:
            return []

        product_ids = [str(item.get("product_id")) for item in data["collects"]]
        if not product_ids:
            return []

        products_data = self._api("GET", "/products.json")
        if "products" not in products_data:
            return []

        id_to_name = {str(product.get("id")): product.get("title") for product in products_data["products"]}
        return [id_to_name.get(pid) for pid in product_ids if pid in id_to_name]

    @kernel_function(name="feature_product_homepage")
    def feature_product_homepage(self, product_name: str):
        permission_error = self._check_permission("Update Descriptions", "destacar productos en Home Page")
        if permission_error:
            return permission_error

        product_id = self.find_id_by_name(product_name)
        if not product_id:
            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] Producto '{product_name}' no encontrado en catalogo"))
            return Colors.red(f"Producto '{product_name}' no encontrado")

        collection_id = self._get_or_create_homepage_collection_id()
        if not collection_id:
            return Colors.red("No se pudo crear u obtener la coleccion 'Home Page'")

        existing_collect = self._get_collect_id(product_id, collection_id)
        if existing_collect:
            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] '{product_name}' ya esta en Home Page, omitiendo"))
            return f"'{product_name}' ya estaba en Home Page"

        payload = {"collect": {"product_id": int(product_id), "collection_id": int(collection_id)}}
        response = self._api("POST", "/collects.json", payload)
        if "collect" in response:
            return Colors.green(f"'{product_name}' destacado en Home Page")
        if "error" in response:
            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] Error al destacar '{product_name}': {response}"))
            return Colors.red(f"No se pudo destacar '{product_name}'")
        return Colors.red(f"No se pudo destacar '{product_name}'")

    @kernel_function(name="remove_product_homepage")
    def remove_product_homepage(self, product_name: str):
        permission_error = self._check_permission("Update Descriptions", "quitar productos de Home Page")
        if permission_error:
            return permission_error

        product_id = self.find_id_by_name(product_name)
        if not product_id:
            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] Producto '{product_name}' no encontrado para eliminar"))
            return Colors.red(f"Producto '{product_name}' no encontrado")

        collection_id = self._get_homepage_collection_id()
        if not collection_id:
            return Colors.yellow("La coleccion 'Home Page' no existe")

        collect_id = self._get_collect_id(product_id, collection_id)
        if not collect_id:
            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] '{product_name}' no estaba en Home Page"))
            return f"'{product_name}' no estaba en Home Page"

        response = self._api("DELETE", f"/collects/{collect_id}.json")
        if "error" in response:
            return Colors.red(f"No se pudo quitar '{product_name}' de Home Page")
        return Colors.green(f"'{product_name}' eliminado de Home Page")

    @kernel_function(name="update_description")
    def update_description(self, product_id, text):
        permission_error = self._check_permission("Update Descriptions", "actualizar descripciones de productos")
        if permission_error:
            return permission_error

        payload = {"product": {"id": int(product_id), "body_html": text}}
        response = self._api("PUT", f"/products/{product_id}.json", payload)
        return Colors.green("Descripción actualizada") if "product" in response else Colors.red("Error")

    @kernel_function(name="get_product_description")
    def get_product_description(self, product_id):
        permission_error = self._check_permission("View Products", "consultar descripciones de productos")
        if permission_error:
            return permission_error

        current = self._api("GET", f"/products/{product_id}.json")
        if "product" in current:
            title = current["product"].get("title", "")
            body_html = current["product"].get("body_html") or ""
            return f"Descripción de '{title}':\n{body_html}"
        return Colors.red("Producto no encontrado")

    @kernel_function(name="update_title")
    def update_title(self, product_id, title):
        permission_error = self._check_permission("Update Descriptions", "actualizar títulos de productos")
        if permission_error:
            return permission_error

        payload = {"product": {"id": int(product_id), "title": str(title)}}
        response = self._api("PUT", f"/products/{product_id}.json", payload)
        return Colors.green("Título actualizado") if "product" in response else Colors.red("Error")

    @kernel_function(name="revert_price")
    def revert_price(self, product_id):
        old = self.memory.get_old(product_id)
        if old:
            return self.update_product_price(product_id, old)
        return Colors.red("No hay historial")

    @kernel_function(name="count_products")
    def count_products(self):
        permission_error = self._check_permission("View Products", "contar productos")
        if permission_error:
            return permission_error

        data = self._api("GET", "/products/count.json")
        return f"Total: {data.get('count', 0)}"

    @kernel_function(name="sort_products")
    def sort_products(self):
        permission_error = self._check_permission("View Products", "ver productos del catálogo")
        if permission_error:
            return permission_error

        data = self._api("GET", "/products.json")
        if "products" in data:
            products = sorted(data["products"], key=lambda item: float(item["variants"][0]["price"]), reverse=True)
            lines = [f"- {product['variants'][0]['price']}€ - {product['title']}" for product in products]
            return "Productos ordenados (Mayor a menor):\n" + "\n".join(lines)
        return "Error"


__all__ = ["PriceMemory", "ShopifyPlugin"]
