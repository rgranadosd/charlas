#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample AI Agent for WSO2 API Manager - Shopify Integration
Intelligent ecommerce AI agent powered by Microsoft Semantic Kernel

Copyright 2025 Sample AI Agent Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import requests
import asyncio
import json
import base64
import argparse
import threading
import time
import sys
from dotenv import load_dotenv
import semantic_kernel as sk  # <<< SEMANTIC KERNEL
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion  # <<< SEMANTIC KERNEL
from semantic_kernel.functions import kernel_function  # <<< SEMANTIC KERNEL
from semantic_kernel.contents.chat_history import ChatHistory  # <<< SEMANTIC KERNEL

# Variable global para modo debug
DEBUG_MODE = False

# ============================================
# INDICADOR DE PROGRESO
# ============================================

class ThinkingIndicator:
    """Clase para mostrar un indicador de 'pensando...' animado"""
    
    def __init__(self, message="Pensando"):
        self.message = message
        self.running = False
        self.thread = None
    
    def start(self):
        """Inicia el indicador animado"""
        if not DEBUG_MODE and not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.daemon = True
            self.thread.start()
    
    def stop(self):
        """Detiene el indicador animado"""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=0.1)
            # Limpiar la línea
            if not DEBUG_MODE:
                print(f"\r{' ' * (len(self.message) + 10)}\r", end="", flush=True)
    
    def _animate(self):
        """Animación de puntos"""
        dots = 0
        while self.running:
            dots_str = "." * (dots % 4)
            padding = " " * (3 - len(dots_str))
            print(f"\r{Colors.blue(self.message)}{dots_str}{padding}", end="", flush=True)
            time.sleep(0.5)
            dots += 1

# ============================================
# SISTEMA DE COLORES ANSI
# ============================================

class Colors:
    """Clase para manejar colores ANSI de forma consistente"""
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Detectar si el terminal soporta colores
    _colors_enabled = None
    
    @classmethod
    def _detect_color_support(cls):
        """Detecta si el terminal actual soporta colores ANSI"""
        if cls._colors_enabled is not None:
            return cls._colors_enabled
            
        import sys
        
        # Verificar si stdout es un TTY
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            cls._colors_enabled = False
            return False
            
        # Verificar variables de entorno comunes
        term = os.getenv('TERM', '').lower()
        colorterm = os.getenv('COLORTERM', '').lower()
        
        # Terminales que soportan colores
        color_terms = ['xterm', 'screen', 'tmux', 'linux', 'ansi']
        
        if any(ct in term for ct in color_terms) or colorterm:
            cls._colors_enabled = True
        else:
            cls._colors_enabled = False
            
        return cls._colors_enabled
    
    @staticmethod
    def red(text):
        if Colors._detect_color_support():
            return f"{Colors.RED}{text}{Colors.RESET}"
        else:
            return f"[ERROR] {text}"
    
    @staticmethod
    def green(text):
        if Colors._detect_color_support():
            return f"{Colors.GREEN}{text}{Colors.RESET}"
        else:
            return f"[OK] {text}"
    
    @staticmethod
    def yellow(text):
        if Colors._detect_color_support():
            return f"{Colors.YELLOW}{text}{Colors.RESET}"
        else:
            return f"[AVISO] {text}"
    
    @staticmethod
    def blue(text):
        if Colors._detect_color_support():
            return f"{Colors.BLUE}{text}{Colors.RESET}"
        else:
            return f"[INFO] {text}"
    
    @staticmethod
    def cyan(text):
        if Colors._detect_color_support():
            return f"{Colors.CYAN}{text}{Colors.RESET}"
        else:
            return f"[DEBUG] {text}"

# NUEVA: Variable para respuesta directa sin LLM
DIRECT_MODE = False

# Cargar variables de entorno
load_dotenv('/Users/rafagranados/Develop/wso2/agente-ia-eci/.env')

print("=" * 60)
print("AGENTE DE DEPURACIÓN v1.3 (SHOPIFY + WSO2) - ANTI-ALUCINACIONES")
print("=" * 60)

# ============================================
# SISTEMA DE MEMORIA DE PRECIOS
# ============================================

class PriceMemory:
    """Clase para recordar cambios de precio anteriores"""
    def __init__(self):
        self.price_history = {}  # {product_id: {previous: precio_anterior, current: precio_actual}}
    
    def remember_price_change(self, product_id: str, old_price: str, new_price: str):
        """Guarda un cambio de precio"""
        self.price_history[product_id] = {
            'previous': old_price,
            'current': new_price
        }
        if DEBUG_MODE:
            print(f"   Guardado en memoria: ID {product_id} cambió de ${old_price} a ${new_price}")
    
    def get_previous_price(self, product_id: str) -> str or None:
        """Obtiene el precio anterior de un producto"""
        if product_id in self.price_history:
            return self.price_history[product_id]['previous']
        return None
    
    def has_history(self, product_id: str) -> bool:
        """Verifica si hay historial para un producto"""
        return product_id in self.price_history

# ============================================
# PLUGIN DE SHOPIFY (VERSIÓN REVISADA Y SIMPLIFICADA)
# ============================================

class ShopifyPlugin:
    """
    Plugin para interactuar con la tienda Shopify a través del Gateway de WSO2.
    Utiliza OAuth2 para autenticarse en el Gateway.
    """
    
    def __init__(self):
        self.price_memory = PriceMemory()  # Sistema de memoria de precios
    
    def _get_wso2_access_token(self) -> str or None:
        """Obtiene un token de acceso de WSO2."""
        if DEBUG_MODE:
            print("   Solicitando token de acceso a WSO2...")
        token_endpoint = os.getenv("WSO2_TOKEN_ENDPOINT")
        consumer_key = os.getenv("WSO2_CONSUMER_KEY")
        consumer_secret = os.getenv("WSO2_CONSUMER_SECRET")

        if not all([token_endpoint, consumer_key, consumer_secret]):
            print(f"   {Colors.red('ERROR')} Error: Faltan variables de WSO2 en el fichero .env")
            return None

        credentials = f"{consumer_key}:{consumer_secret}".encode("utf-8")
        encoded_credentials = base64.b64encode(credentials).decode("utf-8")
        headers = { "Authorization": f"Basic {encoded_credentials}", "Content-Type": "application/x-www-form-urlencoded" }
        payload = "grant_type=client_credentials"
        
        try:
            response = requests.post(token_endpoint, headers=headers, data=payload, verify=False)
            if response.status_code == 200:
                if DEBUG_MODE:
                    print(f"   {Colors.green('OK')} Token de acceso de WSO2 obtenido.")
                return response.json().get("access_token")
            else:
                print(f"   {Colors.red('ERROR')} Error al obtener token WSO2: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"   {Colors.red('ERROR')} Excepción al conectar con WSO2: {str(e)}")
            return None

    def _make_api_call(self, method: str, api_path: str, payload: dict = None) -> dict:
        """Función centralizada para hacer TODAS las llamadas a través de WSO2."""
        
        # Paso 1: Obtener token de WSO2
        wso2_token = self._get_wso2_access_token()
        if not wso2_token:
            return {"error": "Fallo al obtener token de WSO2."}

        # Paso 2: Preparar la petición
        wso2_gw_url = os.getenv("WSO2_GW_URL")
        shopify_api_token = os.getenv("SHOPIFY_API_TOKEN")

        full_url = f"{wso2_gw_url}{api_path}"
        if DEBUG_MODE:
            print(f"   URL completa: {full_url}")
        headers = {
            "Authorization": f"Bearer {wso2_token}", # Autenticación para el Gateway
            "X-Shopify-Access-Token": shopify_api_token # Cabecera para el backend de Shopify
        }
        if DEBUG_MODE:
            print(f"   Headers: Authorization=Bearer [TOKEN], X-Shopify-Access-Token=[TOKEN]")

        # Paso 3: Realizar la petición
        try:
            if method.upper() == 'GET':
                response = requests.get(full_url, headers=headers, verify=False)
            elif method.upper() == 'PUT':
                 headers["Content-Type"] = "application/json"
                 response = requests.put(full_url, headers=headers, json=payload, verify=False)
            else:
                return {"error": f"Método {method} no implementado."}
            
            # Paso 4: Devolver el resultado
            # Si la respuesta es exitosa pero no tiene contenido (ej. 204), devolvemos un JSON vacío
            if 200 <= response.status_code < 300:
                # Verificar si la respuesta es JSON válido
                try:
                    if response.content:
                        return response.json()
                    else:
                        return {}
                except json.JSONDecodeError:
                    # Si no es JSON, puede ser HTML (redirección)
                    if "text/html" in response.headers.get("content-type", ""):
                        print("    El Gateway devuelve HTML en lugar de JSON")
                        print(f"   {Colors.yellow('DEBUG')} DIAGNÓSTICO: Posible redirección o página de error")
                        print("   SOLUCIÓN: Verifica la configuración del endpoint en WSO2")
                        return {"error": "Gateway devuelve HTML", "detail": "La respuesta no es JSON válido"}
                    else:
                        return {"error": "Respuesta no válida", "detail": "No se pudo procesar la respuesta"}
            else:
                # Mostrar el error específico que devuelve el gateway
                error_detail = response.text
                print(f"   {Colors.red('ERROR')} Error del Gateway: {response.status_code}")
                print(f"   Detalle del error: {error_detail}")
                
                # Interpretar el error específico
                if response.status_code == 401:
                    if "Invalid API key or access token" in error_detail:
                        print(f"   {Colors.yellow('DEBUG')} DIAGNÓSTICO: El token de Shopify es inválido o ha expirado")
                        print("   SOLUCIÓN: Verifica SHOPIFY_API_TOKEN en el archivo .env")
                    elif "unrecognized login or wrong password" in error_detail:
                        print(f"   {Colors.yellow('DEBUG')} DIAGNÓSTICO: Credenciales de Shopify incorrectas")
                        print("   SOLUCIÓN: Verifica SHOPIFY_API_TOKEN en el archivo .env")
                    else:
                        print(f"   {Colors.yellow('DEBUG')} DIAGNÓSTICO: Error de autenticación en el Gateway")
                        print("   SOLUCIÓN: Verifica la configuración de WSO2")
                elif response.status_code == 403:
                    print(f"   {Colors.yellow('DEBUG')} DIAGNÓSTICO: Acceso denegado - posible problema de suscripción")
                    print("   SOLUCIÓN: Verifica que la aplicación esté suscrita a la API en WSO2")
                elif response.status_code == 404:
                    print(f"   {Colors.yellow('DEBUG')} DIAGNÓSTICO: Recurso no encontrado")
                    print("   SOLUCIÓN: Verifica la URL del Gateway y el contexto de la API")
                
                return {"error": f"Error del Gateway: {response.status_code}", "detail": error_detail}
                
        except requests.exceptions.RequestException as e:
            print(f"   {Colors.red('ERROR')} Error de conexión: {str(e)}")
            return {"error": "Excepción de conexión", "detail": str(e)}
        except json.JSONDecodeError as e:
            print(f"   {Colors.red('ERROR')} Error al decodificar JSON: {str(e)}")
            return {"error": "Error al procesar respuesta JSON", "detail": str(e)}
        except Exception as e:
            print(f"   {Colors.red('ERROR')} Error inesperado: {str(e)}")
            return {"error": "Error inesperado", "detail": str(e)}

    @kernel_function(name="get_products_list", description="Obtiene la lista de productos con sus IDs.")  # <<< SEMANTIC KERNEL
    def get_products_list(self) -> str:
        if DEBUG_MODE:
            print("\n[EJECUTANDO] → get_products_list()")
        data = self._make_api_call("GET", "/products.json")
        
        if "products" in data:
            products_data = data["products"]
            # CORRECCIÓN APLICADA: Ahora incluye el ID del producto
            product_info = [
                f"- ID: {p['id']} - {p['title']} - ${p.get('variants', [{}])[0].get('price', 'N/A')}" 
                for p in products_data
            ]
            return f"Productos encontrados ({len(products_data)} total):\n" + "\n".join(product_info)
        return f"No se pudieron obtener los productos. Razón: {data.get('error', 'Desconocida')} - {data.get('detail', '')}"

    @kernel_function(name="get_products_sorted", description="Obtiene productos ordenados por precio.")  # <<< SEMANTIC KERNEL
    def get_products_sorted(self, order: str = "desc") -> str:
        """
        Obtiene productos ordenados por precio
        order: 'asc' para menor a mayor, 'desc' para mayor a menor
        """
        if DEBUG_MODE:
            print(f"\n[EJECUTANDO] → get_products_sorted(order={order})")
        data = self._make_api_call("GET", "/products.json")
        
        if "products" in data:
            products_data = data["products"]
            
            # Preparar datos con ID, título, precio y precio numérico para ordenar
            products_with_details = []
            for p in products_data:
                price_str = p.get('variants', [{}])[0].get('price', 'N/A')
                try:
                    price_num = float(price_str) if price_str != 'N/A' else 0
                except (ValueError, TypeError):
                    price_num = 0
                
                products_with_details.append({
                    'id': p['id'],
                    'title': p['title'],
                    'price_str': price_str,
                    'price_num': price_num
                })
            
            # Ordenar por precio
            if order.lower() in ['asc', 'ascending', 'menor', 'low']:
                products_with_details.sort(key=lambda x: x['price_num'])
                order_desc = "de menor a mayor precio"
            else:
                products_with_details.sort(key=lambda x: x['price_num'], reverse=True)
                order_desc = "de mayor a menor precio"
            
            # Formatear la salida
            product_info = [
                f"- ID: {p['id']} - {p['title']} - ${p['price_str']}" 
                for p in products_with_details
            ]
            
            return f"Productos encontrados ({len(products_data)} total) ordenados {order_desc}:\n" + "\n".join(product_info)
        return f"No se pudieron obtener los productos. Razón: {data.get('error', 'Desconocida')} - {data.get('detail', '')}"

    @kernel_function(name="count_products", description="Cuenta el total de productos.")  # <<< SEMANTIC KERNEL
    def count_products(self) -> str:
        if DEBUG_MODE:
            print("\n[EJECUTANDO] → count_products()")
        data = self._make_api_call("GET", "/products/count.json")
        
        if "count" in data:
            return f"La tienda tiene {data['count']} productos en total."
        return f"No se pudo obtener el conteo. Razón: {data.get('error', 'Desconocida')} - {data.get('detail', '')}"

    @kernel_function(name="update_product_price", description="Actualiza el precio de un producto dado su ID.")  # <<< SEMANTIC KERNEL
    def update_product_price(self, product_id: str, new_price: str, remember_old: bool = True) -> str:
        """Actualiza el precio de un producto dado su ID."""
        if DEBUG_MODE:
            print(f"\n[EJECUTANDO] → update_product_price() para ID {product_id} a ${new_price}")
        
        # PASO 1: Obtener precio actual antes del cambio
        old_price = None
        if remember_old:
            if DEBUG_MODE:
                print("   Obteniendo precio actual...")
            current_data = self._make_api_call("GET", f"/products/{product_id}.json")
            if "product" in current_data and current_data["product"].get("variants"):
                old_price = current_data["product"]["variants"][0].get("price", "0")
                if DEBUG_MODE:
                    print(f"   Precio actual: ${old_price}")
            else:
                print(f"   {Colors.red('ERROR')} No se pudo obtener precio actual: {current_data}")
        
        # PASO 2: Preparar payload para la actualización
        if DEBUG_MODE:
            print("   Preparando actualización...")
        
        # Obtener el variant ID correcto
        current_data = self._make_api_call("GET", f"/products/{product_id}.json")
        if "product" not in current_data:
            return f"{Colors.red('ERROR')} Error: No se pudo obtener información del producto ID {product_id}"
        
        variants = current_data["product"].get("variants", [])
        if not variants:
            return f"{Colors.red('ERROR')} Error: El producto ID {product_id} no tiene variantes"
        
        variant_id = variants[0]["id"]  # Usar el ID de la variante
        if DEBUG_MODE:
            print(f"   Variant ID: {variant_id}")
        
        # El payload correcto debe incluir el variant ID
        payload = {
            "product": {
                "id": int(product_id),
                "variants": [{
                    "id": variant_id,
                    "price": new_price
                }]
            }
        }
        
        if DEBUG_MODE:
            print(f"   Payload enviado: {payload}")
        
        # PASO 3: Realizar la actualización
        if DEBUG_MODE:
            print("   Enviando actualización...")
        data = self._make_api_call("PUT", f"/products/{product_id}.json", payload=payload)
        
        if DEBUG_MODE:
            print(f"   Respuesta completa: {data}")
        
        # PASO 4: Verificar el resultado
        if data and "product" in data:
            # Verificar si realmente se actualizó
            updated_variants = data["product"].get("variants", [])
            if updated_variants and updated_variants[0].get("price"):
                updated_price = updated_variants[0]["price"]
                if DEBUG_MODE:
                    print(f"   {Colors.green('OK')} Precio confirmado en respuesta: ${updated_price}")
                
                # Comparar valores numéricos en lugar de strings para evitar problemas con decimales
                try:
                    updated_price_num = float(updated_price)
                    new_price_num = float(new_price)
                    
                    if abs(updated_price_num - new_price_num) < 0.01:  # Tolerancia para decimales
                        # PASO 5: Guardar en memoria el cambio
                        if old_price and remember_old:
                            self.price_memory.remember_price_change(product_id, old_price, new_price)
                        
                        return f"{Colors.green('OK')} Éxito confirmado: El precio del producto ID {product_id} se ha actualizado de ${old_price} a ${updated_price}."
                    else:
                        return f"{Colors.yellow('AVISO')} Actualización parcial: Se envió ${new_price} pero la respuesta muestra ${updated_price}"
                except ValueError:
                    # Si no se pueden convertir a números, usar comparación de strings como fallback
                    if str(updated_price) == str(new_price):
                        if old_price and remember_old:
                            self.price_memory.remember_price_change(product_id, old_price, new_price)
                        return f"{Colors.green('OK')} Éxito confirmado: El precio del producto ID {product_id} se ha actualizado de ${old_price} a ${updated_price}."
                    else:
                        return f"{Colors.yellow('AVISO')} Actualización parcial: Se envió ${new_price} pero la respuesta muestra ${updated_price}"
            else:
                return f" Respuesta sin confirmación de precio: {data}"
        else:
            return f"{Colors.red('ERROR')} Error en la actualización. Respuesta: {data.get('error', 'Desconocida')} - {data.get('detail', 'Sin detalles')}"

    @kernel_function(name="find_product_by_name", description="Busca un producto por su nombre y devuelve su ID.")  # <<< SEMANTIC KERNEL
    def find_product_by_name(self, product_name: str) -> dict:
        """Busca un producto por su nombre y devuelve información completa, con tolerancia a errores tipográficos"""
        if DEBUG_MODE:
            print(f"\n[EJECUTANDO] → find_product_by_name() buscando '{product_name}'")
        data = self._make_api_call("GET", "/products.json")
        
        if "products" in data:
            products_data = data["products"]
            product_name_lower = product_name.lower().strip()
            
            # 1. Buscar coincidencia exacta primero
            for product in products_data:
                if product['title'].lower() == product_name_lower:
                    price = product.get('variants', [{}])[0].get('price', 'N/A')
                    if DEBUG_MODE:
                        print(f"   {Colors.green('OK')} Coincidencia exacta encontrada: {product['title']}")
                    return {
                        'found': True,
                        'id': str(product['id']),
                        'name': product['title'],
                        'price': price
                    }
            
            # 2. Buscar coincidencia parcial (el nombre buscado está dentro del título)
            for product in products_data:
                if product_name_lower in product['title'].lower():
                    price = product.get('variants', [{}])[0].get('price', 'N/A')
                    if DEBUG_MODE:
                        print(f"   {Colors.green('OK')} Coincidencia parcial encontrada: {product['title']}")
                    return {
                        'found': True,
                        'id': str(product['id']),
                        'name': product['title'],
                        'price': price
                    }
            
            # 3. Buscar por similitud de palabras (tolerancia a errores tipográficos)
            import difflib
            best_match = None
            best_ratio = 0.6  # Umbral mínimo de similitud (60%)
            
            for product in products_data:
                product_title_lower = product['title'].lower()
                # Calcular similitud entre nombres
                ratio = difflib.SequenceMatcher(None, product_name_lower, product_title_lower).ratio()
                
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = product
            
            if best_match:
                price = best_match.get('variants', [{}])[0].get('price', 'N/A')
                if DEBUG_MODE:
                    print(f"   {Colors.yellow('SUGERENCIA')} Producto similar encontrado ({best_ratio:.1%} similitud): {best_match['title']}")
                return {
                    'found': True,
                    'id': str(best_match['id']),
                    'name': best_match['title'],
                    'price': price,
                    'similarity': best_ratio,
                    'suggestion': True
                }
            
            # 4. Si no hay coincidencias, mostrar productos disponibles para ayudar al usuario
            if DEBUG_MODE:
                print(f"   {Colors.red('ERROR')} No se encontró '{product_name}'")
            if DEBUG_MODE:
                print(f"   {Colors.yellow('SUGERENCIA')} Productos disponibles:")
                for i, product in enumerate(products_data[:5]):  # Mostrar solo los primeros 5
                    print(f"     - {product['title']}")
                if len(products_data) > 5:
                    print(f"     ... y {len(products_data) - 5} productos más")
        
        return {'found': False, 'error': 'Producto no encontrado'}

    @kernel_function(name="update_product_price_with_math", description="Actualiza el precio de un producto aplicando una operación matemática.")  # <<< SEMANTIC KERNEL
    def update_product_price_with_math(self, product_identifier: str, operation: str, value: float, is_id: bool = True) -> str:
        """Actualiza el precio de un producto aplicando una operación matemática (sumar, restar)"""
        if DEBUG_MODE:
            print(f"\n[EJECUTANDO] → update_product_price_with_math() {operation} {value} a producto {product_identifier}")
        
        # Obtener información del producto
        if is_id:
            product_id = product_identifier
            current_data = self._make_api_call("GET", f"/products/{product_id}.json")
            if "product" not in current_data:
                return f"{Colors.red('ERROR')} Error: No se pudo obtener información del producto ID {product_id}"
            product_name = current_data["product"]["title"]
        else:
            # Buscar por nombre
            search_result = self.find_product_by_name(product_identifier)
            if not search_result['found']:
                return f"{Colors.red('ERROR')} No se encontró el producto '{product_identifier}'"
            product_id = search_result['id']
            product_name = search_result['name']
            current_data = self._make_api_call("GET", f"/products/{product_id}.json")
        
        # Obtener precio actual
        if "product" in current_data and current_data["product"].get("variants"):
            current_price = float(current_data["product"]["variants"][0].get("price", "0"))
            if DEBUG_MODE:
                print(f"   Precio actual de '{product_name}': ${current_price}")
        else:
            return f"{Colors.red('ERROR')} No se pudo obtener el precio actual del producto"
        
        # Calcular nuevo precio
        if operation == 'add':
            new_price = current_price + value
            operation_text = f"añadiendo ${value}"
        elif operation == 'subtract':
            new_price = current_price - value
            operation_text = f"restando ${value}"
        else:
            return f"{Colors.red('ERROR')} Operación '{operation}' no soportada"
        
        if DEBUG_MODE:
            print(f"   Calculando: ${current_price} {operation_text} = ${new_price}")
        
        # Actualizar con el nuevo precio calculado
        result = self.update_product_price(product_id, str(new_price))
        
        # Detectar éxito con los nuevos patrones
        success_patterns = ["[OK] Éxito", "OK] Éxito", "Éxito confirmado", "se ha actualizado"]
        if any(pattern in result for pattern in success_patterns):
            return f"[32mOK[0m Operación exitosa: '{product_name}' actualizado de ${current_price} a ${new_price} ({operation_text})"
        else:
            return result

    @kernel_function(name="update_product_price_by_name", description="Actualiza el precio de un producto usando su nombre.")  # <<< SEMANTIC KERNEL
    def update_product_price_by_name(self, product_name: str, new_price: str) -> str:
        """Actualiza el precio de un producto buscándolo por nombre"""
        if DEBUG_MODE:
            print(f"\n[EJECUTANDO] → update_product_price_by_name() para '{product_name}' a ${new_price}")
        
        # Buscar el producto por nombre
        search_result = self.find_product_by_name(product_name)
        
        if search_result['found']:
            product_id = search_result['id']
            product_title = search_result['name']
            
            # Si es una sugerencia (producto similar), informar al usuario
            if search_result.get('suggestion'):
                similarity = search_result.get('similarity', 0)
                if DEBUG_MODE:
                    print(f"   {Colors.yellow('SUGERENCIA')} Usando producto similar: {product_title} (ID: {product_id}) - Similitud: {similarity:.1%}")
                result = self.update_product_price(product_id, new_price)
                # Agregar información sobre la sugerencia al resultado
                success_patterns = ["[OK] Éxito", "OK] Éxito", "Éxito confirmado", "se ha actualizado"]
                if any(pattern in result for pattern in success_patterns):
                    result += f"\n{Colors.yellow('NOTA')} Se usó '{product_title}' (similitud {similarity:.1%}) en lugar de '{product_name}'"
                return result
            else:
                if DEBUG_MODE:
                    print(f"   {Colors.green('OK')} Producto encontrado: {product_title} (ID: {product_id})")
                return self.update_product_price(product_id, new_price)
        else:
            return f"{Colors.red('ERROR')} No se encontró el producto '{product_name}'. Verifica el nombre o usa el ID del producto."

    @kernel_function(name="revert_price", description="Restaura el precio anterior de un producto.")  # <<< SEMANTIC KERNEL
    def revert_price(self, product_id: str) -> str:
        """Restaura el precio anterior de un producto"""
        if DEBUG_MODE:
            print(f"\n[EJECUTANDO] → revert_price() para ID {product_id}")
        
        if not self.price_memory.has_history(product_id):
            return f"{Colors.red('ERROR')} No hay historial de precios para el producto ID {product_id}"
        
        previous_price = self.price_memory.get_previous_price(product_id)
        if previous_price:
            # Usar la función de actualización pero sin recordar este cambio
            result = self.update_product_price(product_id, previous_price, remember_old=False)
            # Detectar éxito con los nuevos patrones
            success_patterns = ["[OK] Éxito", "OK] Éxito", "Éxito confirmado", "se ha actualizado"]
            if any(pattern in result for pattern in success_patterns):
                return f"Precio restaurado: ID {product_id} vuelve a costar ${previous_price}"
            else:
                return result
        return f"{Colors.red('ERROR')} No se pudo obtener el precio anterior para ID {product_id}"

# ============================================
# SISTEMA DE EJECUCIÓN MANUAL GARANTIZADA
# ============================================

class AgentWithManualExecution:
    def __init__(self, kernel, shopify_plugin):  # <<< SEMANTIC KERNEL
        self.kernel = kernel  # <<< SEMANTIC KERNEL
        self.shopify = shopify_plugin
        self.chat_history = ChatHistory()  # <<< SEMANTIC KERNEL
        
        # MEJORA 1: SYSTEM MESSAGE ANTI-ALUCINACIONES
        system_message = """Eres un asistente especializado en tienda Shopify. REGLAS CRÍTICAS:

1. SOLO responde con información EXACTA obtenida de las funciones de Shopify
2. NUNCA inventes productos, precios o IDs que no estén en los datos reales
3. Para listados: SIEMPRE incluye todos los IDs de productos
4. Para actualizaciones: SOLO confirma éxito si los datos indican éxito claramente
5. Si los datos muestran error, explica el error sin inventar soluciones

FORMATO OBLIGATORIO:
- Listados: "ID: [número] - [nombre] - $[precio]" para cada producto
- Actualizaciones exitosas: Confirma precio anterior → precio nuevo
- Errores: Explica exactamente lo que falló

PROHIBIDO: Inventar información, confirmar operaciones sin verificación real, usar palabras como "probablemente" o "creo que"."""
        
        self.chat_history.add_system_message(system_message)  # <<< SEMANTIC KERNEL

    async def process_with_guaranteed_execution(self, user_input: str):
        import re  # Importar re al principio del método
        
        # Crear indicador de progreso al inicio
        thinking = ThinkingIndicator("Procesando consulta")
        thinking.start()
        
        if DEBUG_MODE:
            print(f"\nUsuario: {user_input}")
        user_input_lower = user_input.lower()
        
        # Triggers mejorados para detectar intenciones
        triggers = {
            'list': ['productos', 'lista', 'catálogo', 'disponible', 'tienes', 'mostrar', 'ver', 'dame',
                     'barata', 'barato', 'cara', 'caro', 'precio', 'cuesta', 'económico', 'costoso',
                     'tabla', 'tablas', 'opciones', 'alternativas', 'oferta'],
            'count': ['cuántos', 'cantidad', 'número', 'total'],
            'sort_asc': ['menor', 'mayor', 'ascendente', 'descendente', 'ordenar', 'orden'],
            'update_price': ['actualizar', 'actualiza', 'cambiar', 'cambio', 'modificar', 'modifica'],
            'revert_price': ['vuelve', 'restaurar', 'deshacer', 'anterior', 'original', 'revertir', 'dejarlo']
        }
        
        execute_function = None
        sort_order = None
        product_id = None
        new_price = None
        product_name = None
        math_operation = None
        math_value = None
        
        # CORRECCIÓN: Detección más amplia y precisa de UPDATE_PRICE
        update_keywords = ['actualizar', 'actualiza', 'cambiar', 'cambio', 'modificar', 'modifica']
        math_keywords = ['añadiendo', 'añadiendole', 'sumando', 'sumandole', 'agregando', 'agregandole', 'restando', 'restandole', 'quitando', 'quitandole']
        price_patterns = [
            r'a\s+[\$€]?\d+',                    # "a 1000"
            r'precio\s+[\$€]?\d+',               # "precio 1000" 
            r'[\$€]\s*\d+',                      # "$1000"
            r'añadiendo(?:le)?\s+\d+',           # "añadiendo 1000" o "añadiendole 1000"
            r'sumando(?:le)?\s+\d+',             # "sumando 500" o "sumandole 500"
            r'agregando(?:le)?\s+\d+',           # "agregando 200" o "agregandole 200"
            r'restando(?:le)?\s+\d+',            # "restando 100" o "restandole 100"
            r'quitando(?:le)?\s+\d+',            # "quitando 50" o "quitandole 50"
        ]
        
        has_update_keyword = any(keyword in user_input_lower for keyword in update_keywords)
        has_math_keyword = any(keyword in user_input_lower for keyword in math_keywords)
        has_price_pattern = any(re.search(pattern, user_input_lower) for pattern in price_patterns)
        
        if (has_update_keyword or has_math_keyword) and has_price_pattern:
            execute_function = 'update_price'
            if DEBUG_MODE:
                print("   DETECTADO: UPDATE_PRICE")
            
            # Buscar ID del producto (después de "ID" o "id")
            id_match = re.search(r'id[:\s]*(\d+)', user_input_lower)
            
            # Buscar precio/operación - AMPLIADO SIGNIFICATIVAMENTE
            price_match = re.search(r'(?:a|precio|€|euros?|$|dollars?)[:\s]*(\d+\.?\d*)', user_input_lower)
            
            # Detectar operaciones matemáticas PRIMERO
            math_patterns = {
                'add': [
                    r'añadiendo(?:le)?\s+(\d+\.?\d*)', 
                    r'sumando(?:le)?\s+(\d+\.?\d*)', 
                    r'agregando(?:le)?\s+(\d+\.?\d*)'
                ],
                'subtract': [
                    r'restando(?:le)?\s+(\d+\.?\d*)', 
                    r'quitando(?:le)?\s+(\d+\.?\d*)'
                ]
            }
            
            for operation, patterns in math_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, user_input_lower)
                    if match:
                        math_operation = operation
                        math_value = float(match.group(1))
                        if DEBUG_MODE:
                            print(f"   Operación matemática detectada: {operation} {math_value}")
                        break
                if math_operation:
                    break
            
            # Si no hay operación matemática, buscar precio directo
            if not math_operation:
                if not price_match:
                    all_numbers = re.findall(r'(\d+\.?\d*)', user_input_lower)
                    if len(all_numbers) >= 1:
                        new_price = all_numbers[-1]
                        price_match = True
                
                if price_match and hasattr(price_match, 'group'):
                    new_price = price_match.group(1)
            
            # Buscar ID o nombre del producto
            if id_match:
                product_id = id_match.group(1)
                print(f"   ID detectado: {product_id}")
            else:
                # MEJORADO: Búsqueda por nombre más inteligente
                if DEBUG_MODE:
                    print("   No se encontró ID, buscando por nombre de producto...")
                
                # Buscar nombre de producto con patrones mejorados y más específicos
                name_patterns = [
                    # Patrón principal: "actualiza [el precio de] NOMBRE [operación] VALOR"
                    r'(?:actualiza|actualizar|modifica|modificar|cambiar|cambio)\s+(?:el\s+precio\s+(?:de|del)\s+)?(.+?)\s+(?:a|añadiendo|sumando|agregando|restando|quitando)\s+[\d.]+',
                    # Patrón alternativo: "precio de NOMBRE a VALOR"
                    r'precio\s+(?:de|del)\s+(.+?)\s+a\s+[\d.]+',
                    # Patrón para operaciones matemáticas: "NOMBRE sumando VALOR"
                    r'(.+?)\s+(?:añadiendo|sumando|agregando|restando|quitando)\s+[\d.]+',
                ]
                
                for i, pattern in enumerate(name_patterns):
                    name_match = re.search(pattern, user_input_lower, re.IGNORECASE)
                    if name_match:
                        extracted_name = name_match.group(1).strip()
                        
                        # Limpiar el nombre extraído
                        # Remover palabras de comando que pueden haber quedado
                        words_to_remove = ['actualiza', 'actualizar', 'modifica', 'modificar', 'cambiar', 'cambio', 'el', 'precio', 'de', 'del']
                        name_words = extracted_name.split()
                        cleaned_words = [word for word in name_words if word.lower() not in words_to_remove]
                        
                        if cleaned_words:  # Solo si queda algo después de limpiar
                            product_name = ' '.join(word.capitalize() for word in cleaned_words)
                            if DEBUG_MODE:
                                print(f"   Patrón {i+1} - Nombre extraído: '{product_name}'")
                            break
                
                # Patrón fallback más agresivo si los principales fallan
                if not product_name:
                    if DEBUG_MODE:
                        print("   Usando patrón fallback...")
                    # Buscar cualquier secuencia de palabras que pueda ser un nombre de producto
                    fallback_pattern = r'(?:actualiza|actualizar|modifica|modificar|cambiar)\s+(?:el\s+precio\s+de\s+)?(.+?)(?:\s+(?:a|añadiendo|sumando|agregando|restando|quitando)|$)'
                    name_match = re.search(fallback_pattern, user_input_lower, re.IGNORECASE)
                    if name_match:
                        extracted_name = name_match.group(1).strip()
                        # Remover números y operaciones del final
                        extracted_name = re.sub(r'\s+(?:a|añadiendo|sumando|agregando|restando|quitando)\s+[\d.]+.*$', '', extracted_name)
                        # Remover palabras de comando
                        words = extracted_name.split()
                        cleaned_words = [word for word in words if word.lower() not in ['precio', 'de', 'del', 'el', 'la']]
                        if cleaned_words:
                            product_name = ' '.join(word.capitalize() for word in cleaned_words)
                            print(f"   Fallback - Nombre extraído: '{product_name}'")
                
                if product_name:
                    if DEBUG_MODE:
                        print(f"   {Colors.green('OK')} Producto identificado: '{product_name}'")
                else:
                    print(f"   {Colors.yellow('DEBUG')} No se pudo extraer nombre de producto")
            
            # Mostrar precio final o operación detectada
            if math_operation and math_value:
                if DEBUG_MODE:
                    print(f"   Operación pendiente: {math_operation} {math_value}")
            elif new_price:
                pass  # Línea de debug comentada
                
        # Detectar intención de reversión de precio (NUEVO)
        elif any(k in user_input_lower for k in triggers['revert_price']):
            execute_function = 'revert'
            # Buscar ID en el mensaje
            id_match = re.search(r'id[:\s]*(\d+)', user_input_lower)
            if id_match:
                product_id = id_match.group(1)
            else:
                if DEBUG_MODE:
                    print("    No se encontró ID específico para la reversión")
                
        # Detectar intención de ordenación
        elif any(k in user_input_lower for k in triggers['sort_asc']):
            if any(word in user_input_lower for word in ['menor', 'ascendente', 'bajo', 'barato']):
                execute_function = 'sort'
                sort_order = 'asc'
            elif any(word in user_input_lower for word in ['mayor', 'descendente', 'alto', 'caro']):
                execute_function = 'sort'
                sort_order = 'desc'
            elif 'orden' in user_input_lower or 'ordenar' in user_input_lower:
                execute_function = 'sort'
                sort_order = 'desc'  # Por defecto mayor a menor
        elif any(k in user_input_lower for k in triggers['list']):
            execute_function = 'list'
        elif any(k in user_input_lower for k in triggers['count']):
            execute_function = 'count'
        
        shopify_data = None
        if execute_function:
            if DEBUG_MODE:
                print(Colors.blue(f"Intención detectada: {execute_function.upper()}"))
                print(Colors.blue("Ejecutando función de Shopify..."))
            
            if execute_function == 'list':
                shopify_data = self.shopify.get_products_list()
            elif execute_function == 'count':
                shopify_data = self.shopify.count_products()
            elif execute_function == 'sort':
                shopify_data = self.shopify.get_products_sorted(sort_order)
            elif execute_function == 'update_price':
                # NUEVO: Manejar operaciones matemáticas si existen
                if math_operation and math_value:
                    if product_id:
                        shopify_data = self.shopify.update_product_price_with_math(product_id, math_operation, math_value, is_id=True)
                    elif product_name:
                        shopify_data = self.shopify.update_product_price_with_math(product_name, math_operation, math_value, is_id=False)
                    else:
                        shopify_data = f"{Colors.red('ERROR')} Error: No se pudo identificar el producto para la operación matemática"
                
                # Actualización directa de precio si no hay operación matemática
                elif product_id and new_price:
                    shopify_data = self.shopify.update_product_price(product_id, new_price)
                elif product_name and new_price:
                    shopify_data = self.shopify.update_product_price_by_name(product_name, new_price)
                else:
                    error_msg = f"{Colors.red('ERROR')} Error: No pude extraer suficiente información del mensaje.\n"
                    error_msg += f"Debug info: product_id={product_id}, product_name='{product_name}', new_price={new_price}, math_op={math_operation}, math_val={math_value}\n"
                    error_msg += "Ejemplos válidos:\n"
                    error_msg += "- 'Actualizar precio del producto ID 123456 a 99.99'\n"
                    error_msg += "- 'Modificar el precio de Gift Card a 200'\n"
                    error_msg += "- 'Actualiza The Complete Snowboard añadiendo 1000'"
                    shopify_data = error_msg
            elif execute_function == 'revert':
                if product_id:
                    shopify_data = self.shopify.revert_price(product_id)
                else:
                    shopify_data = f"{Colors.red('ERROR')} Error: Necesito el ID del producto para restaurar su precio. Ejemplo: 'Vuelve el precio original del ID 123456'"
                
            if DEBUG_MODE:
                print(Colors.blue("Datos obtenidos de Shopify"))

        # MEJORA 2: MODO DIRECTO OPCIONAL (SIN LLM)
        if DIRECT_MODE and shopify_data:
            print(f"\n[MODO DIRECTO ACTIVADO]")
            print(f"DATOS DIRECTOS DE SHOPIFY:\n{shopify_data}")
            return shopify_data

        if shopify_data:
            # MEJORA 3: PROMPTS ULTRA-ESPECÍFICOS Y RESTRICTIVOS
            if execute_function == 'list' or execute_function == 'sort':
                enhanced_prompt = f'''DATOS EXACTOS DE SHOPIFY:
{shopify_data}

Usuario pidió: "{user_input}"

INSTRUCCIONES OBLIGATORIAS:
- Muestra CADA producto con formato: "ID: [número] - [nombre] - $[precio]"
- INCLUYE TODOS los productos y sus IDs reales
- NO inventes ni omitas productos
- USA EXACTAMENTE los datos proporcionados

Responde SOLO con los productos reales listados arriba.'''

            elif execute_function == 'update_price':
                # Detectar éxito con los nuevos patrones de Colors
                success_patterns = ["[OK] Éxito", "OK] Éxito", "Éxito confirmado", "se ha actualizado"]
                if any(pattern in shopify_data for pattern in success_patterns):
                    enhanced_prompt = f'''ACTUALIZACIÓN EXITOSA CONFIRMADA:
{shopify_data}

Usuario pidió: "{user_input}"

INSTRUCCIONES OBLIGATORIAS:
- La operación fue EXITOSA y el precio se actualizó correctamente
- Confirma el cambio de precio mencionando el precio anterior y nuevo
- Usa un tono positivo y confirma el éxito
- NO digas que falló o que hubo problemas
- Extrae la información del texto de arriba que contiene "Éxito confirmado"

Responde de forma positiva confirmando el cambio exitoso.'''
                else:
                    enhanced_prompt = f'''ACTUALIZACIÓN FALLÓ:
{shopify_data}

Usuario pidió: "{user_input}"

INSTRUCCIONES OBLIGATORIAS:
- Explica claramente que la operación NO funcionó
- Menciona el error exacto que aparece arriba
- NO confirmes que se actualizó nada
- NO inventes soluciones

Responde explicando SOLO el error mostrado arriba.'''

            elif execute_function == 'count':
                enhanced_prompt = f'''CONTEO EXACTO:
{shopify_data}

Usuario pidió: "{user_input}"

INSTRUCCIONES OBLIGATORIAS:
- Confirma el número exacto que aparece arriba
- NO agregues información adicional

Responde SOLO con el número real mostrado arriba.'''

            else:
                enhanced_prompt = f'''DATOS DE SHOPIFY:
{shopify_data}

Usuario pidió: "{user_input}"

Responde basándote ÚNICAMENTE en los datos mostrados arriba.'''
        else:
            enhanced_prompt = user_input
        
        self.chat_history.add_user_message(user_input)  # <<< SEMANTIC KERNEL
        try:
            if DEBUG_MODE:
                print(Colors.blue("Generando respuesta..."))
            response = await self.kernel.invoke_prompt(prompt=enhanced_prompt)  # <<< SEMANTIC KERNEL
            response_text = str(response)
            self.chat_history.add_assistant_message(response_text)  # <<< SEMANTIC KERNEL
            
            # Detener el indicador de progreso antes de mostrar la respuesta
            thinking.stop()
            print(f"\nAsistente: {response_text}")
            return response_text
        except Exception as e:
            # Detener el indicador en caso de error
            thinking.stop()
            print(f"{Colors.red('ERROR')} Error: {e}")
            if shopify_data:
                print(f"\nDatos directos de Shopify:\n{shopify_data}")
            return None

# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

async def main():
    global DEBUG_MODE, DIRECT_MODE
    
    # Parser de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Agente IA para Shopify a través de WSO2 Gateway')
    parser.add_argument('-d', '--debug', action='store_true', help='Activar modo debug')
    parser.add_argument('--direct', action='store_true', help='Modo directo: respuestas sin LLM')
    args = parser.parse_args()
    
    # Configurar modo debug
    DEBUG_MODE = args.debug
    DIRECT_MODE = args.direct
    
    if DEBUG_MODE:
        print(f"{Colors.yellow('DEBUG')} Modo debug ACTIVADO")
    if DIRECT_MODE:
        print("[35mDIRECT[0m Modo directo ACTIVADO - Respuestas directas de Shopify")
    
    if not os.getenv("OPENAI_API_KEY"):
        print(f"\n{Colors.red('ERROR')} ERROR: Falta OPENAI_API_KEY en .env")
        return
    if DEBUG_MODE:
        print("✓ Credenciales de OpenAI detectadas")
    
    kernel = sk.Kernel()  # <<< SEMANTIC KERNEL
    model_to_use = "gpt-4-turbo-preview"
    try:
        kernel.add_service(OpenAIChatCompletion(service_id="openai", api_key=os.getenv("OPENAI_API_KEY"), ai_model_id=model_to_use))  # <<< SEMANTIC KERNEL
        if DEBUG_MODE:
            print(f"✓ Modelo configurado: {model_to_use}")
            print(f"\n{Colors.yellow('DEBUG')} Verificando conexión...", end="")
            await kernel.invoke_prompt("Di 'OK'")  # <<< SEMANTIC KERNEL
            print(f" {Colors.green('OK')} Conexión exitosa")
        else:
            # Solo verificar conexión sin mostrar detalles
            await kernel.invoke_prompt("Di 'OK'")  # <<< SEMANTIC KERNEL
    except Exception as e:
        print(f"{Colors.red('ERROR')} Error de conexión: {e}")
        return
    
    shopify_plugin = ShopifyPlugin()
    kernel.add_plugin(shopify_plugin, plugin_name="Shopify")  # <<< SEMANTIC KERNEL
    if DEBUG_MODE:
        print("✓ Plugin de Shopify registrado")
    
    agent = AgentWithManualExecution(kernel, shopify_plugin)  # <<< SEMANTIC KERNEL
    
    def show_help():
        """Muestra la ayuda con ejemplos de comandos"""
        print("\n" + "=" * 60)
        print("MODO INTERACTIVO - WSO2 OAUTH2 - VERSIÓN ANTI-ALUCINACIONES")
        print("=" * 60)
        if DIRECT_MODE:
            print("[MODO DIRECTO] Las respuestas serán datos exactos de Shopify sin procesamiento")
        print("\nPrueba estas preguntas:")
        print("  - 'Lista los productos'")
        print("  - '¿Cuántos productos tienes?'")
        print("  - 'Dame la lista de productos de menor a mayor precio'")
        print("  - 'Ordena los productos de mayor a menor precio'")
        print(f"  {Colors.blue('ACTUALIZACIÓN POR ID:')}")
        print("  - 'Cambiar precio del producto ID 123456 a 99.99'")
        print("  - 'Actualizar ID 789012 a 150 euros'")
        print(f"  {Colors.blue('ACTUALIZACIÓN POR NOMBRE:')}")  
        print("  - 'Modificar el precio de Gift Card a 200'")
        print("  - 'Cambiar precio de The Draft Snowboard a 1500'")
        print(f"  {Colors.blue('OPERACIONES MATEMÁTICAS:')}")
        print("  - 'Actualiza The Complete Snowboard añadiendo 1000'")
        print("  - 'Modifica Gift Card sumando 50'")
        print("  - 'Cambia ID 123456 restando 100'")
        print(f"  {Colors.blue('RESTAURACIÓN:')}")
        print("  - 'Vuelve dejarlo al precio que estaba ID 123456'")
        print("  - 'Restaurar precio original del ID 789012'")
        print("\nEscribe 'salir' para terminar")
        print("-" * 60)
    
    # Mostrar ayuda solo en modo debug
    if DEBUG_MODE:
        show_help()
    else:
        print("\n" + Colors.green("Agente listo. Escribe tu consulta o 'ayuda' para ver ejemplos."))
    
    while True:
        try:
            user_input = input("\nTú: ")
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("\n¡Hasta luego!")
                break
            elif user_input.lower() in ['ayuda', 'help', '?']:
                show_help()
                continue
            await agent.process_with_guaranteed_execution(user_input)
        except (EOFError, KeyboardInterrupt):
            print("\n\nHasta luego!")
            break
        except Exception as e:
            print(f"\n{Colors.red('ERROR')} Error inesperado: {e}")
            break

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    asyncio.run(main())