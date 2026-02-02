import os
import requests
import asyncio
import json
import base64
import argparse
import threading
import time
import traceback
import http.server
import socketserver
import urllib.parse
import secrets
import hashlib
import webbrowser
import re
from decimal import Decimal, ROUND_HALF_UP
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments
from semantic_kernel.functions import kernel_function

from oauth2_apim import create_openai_client_with_gateway
from banners import get_banner, list_available_banners

# ============================================
# CONFIGURACIÓN Y UTILIDADES
# ============================================

DEBUG_MODE = False
TOKEN_CACHE_FILE = "token_cache.json"


def _auth_trace_enabled() -> bool:
    if DEBUG_MODE:
        return True
    value = os.getenv("WSO2_AUTH_TRACE")
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _thinking_enabled() -> bool:
    value = os.getenv("AGENT_SHOW_THINKING")
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_percent_adjustment(user_input: str) -> float | None:
    """Devuelve porcentaje (positivo o negativo) si el texto sugiere ajuste porcentual."""
    m = re.search(r"(\d+(?:[\.,]\d+)?)\s*(%|por\s*ciento)", user_input, flags=re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).replace(",", ".")
    try:
        pct = float(raw)
    except Exception:
        return None

    lower = user_input.lower()
    # Verbos típicos de bajada/descuento
    if any(w in lower for w in ["reduce", "reducir", "baja", "bajar", "decrementa", "decrementar", "rebaja", "rebajar", "descuento", "descuenta", "disminuye", "disminuir"]):
        pct = -abs(pct)
    else:
        # Por defecto, si aparece '%' asumimos incremento si el usuario dice incrementa/aumenta/sube.
        if any(w in lower for w in ["incrementa", "incrementar", "aumenta", "aumentar", "sube", "subir", "incremento", "aumento"]):
            pct = abs(pct)
    return pct

class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    @staticmethod
    def blue(text): return f"{Colors.BLUE}{text}{Colors.RESET}"
    @staticmethod
    def debug(text): return f"{Colors.DIM}{Colors.CYAN}[DEBUG] {text}{Colors.RESET}"
    @staticmethod
    def red(text): return f"{Colors.RED}[ERROR] {text}{Colors.RESET}"
    @staticmethod
    def green(text): return f"{Colors.GREEN}[OK] {text}{Colors.RESET}"
    @staticmethod
    def cyan(text): return f"{Colors.CYAN}{text}{Colors.RESET}"
    @staticmethod
    def yellow(text): return f"{Colors.YELLOW}{text}{Colors.RESET}"


APP_NAME = "Rafa’s Agent"
APP_VERSION = "v2.5 FINAL"


def _safe_version(module_name: str) -> str:
    try:
        mod = __import__(module_name)
        return getattr(mod, "__version__", "?")
    except Exception:
        return "?"


def print_start_motd(banner_name="default"):
    """MOTD estilo ANSI al arrancar, con banners dinámicos."""
    import sys
    import shutil

    # Colores ANSI (evitar dependencias externas)
    RESET = "\033[0m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    ORANGE = "\033[38;5;208m"

    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    sk_ver = getattr(sk, "__version__", "?")
    openai_ver = _safe_version("openai")
    httpx_ver = _safe_version("httpx")
    requests_ver = _safe_version("requests")

    info_lines = [
        f"{ORANGE}Python {python_ver}{RESET}",
        f"{ORANGE}semantic-kernel {sk_ver}{RESET}",
        f"{ORANGE}openai {openai_ver}{RESET}",
        f"{ORANGE}httpx {httpx_ver}{RESET}",
        f"{ORANGE}requests {requests_ver}{RESET}",
        f"{ORANGE}WSO2 IS {os.getenv('WSO2_AUTH_ENDPOINT','https://localhost:9443')}{RESET}",
        f"{ORANGE}WSO2 APIM {os.getenv('WSO2_APIM_TOKEN_ENDPOINT','https://localhost:9453')}{RESET}",
    ]

    # Cargar banner dinámicamente
    try:
        banner_data = get_banner(banner_name)
        big = banner_data["lines"]
        title = banner_data["title"]
    except Exception as e:
        print(f"⚠️  Error cargando banner '{banner_name}': {e}")
        # Fallback si falla la carga del banner
        big = [f"{ORANGE}{BOLD}(Banner no disponible){RESET}"]
        title = f"{ORANGE}{BOLD}{APP_NAME}{RESET} {ORANGE}{APP_VERSION}{RESET}"

    line_prefix = "\r" if getattr(sys.stdout, "isatty", lambda: False)() else ""

    # Ajustar longitud del separador al ancho real del contenido (sin pasarse del terminal)
    term_width = shutil.get_terminal_size((120, 20)).columns

    max_rows = max(len(big), len(info_lines))
    left_width = 74
    max_right = max((len(_strip_ansi(x)) for x in info_lines), default=0)

    # Longitud mínima: lo que ocupa el panel (izq + der), o el título, o 72.
    divider_len = max(72, len(_strip_ansi(title)), left_width + max_right)
    divider_len = min(divider_len, term_width)

    print("\n" + line_prefix + title)
    print(line_prefix + f"{ORANGE}{DIM}{'─' * divider_len}{RESET}")

    # Render en dos columnas (izq banner, der info)
    # Alinear el panel derecho al fondo (para que quede justo encima del separador inferior)
    right_offset = max(0, max_rows - len(info_lines))
    for i in range(max_rows):
        left = big[i] if i < len(big) else ""
        right = info_lines[i - right_offset] if i >= right_offset and (i - right_offset) < len(info_lines) else ""
        pad = " " * max(0, left_width - len(_strip_ansi(left)))
        print(line_prefix + f"{left}{pad}{right}")

    print(line_prefix + f"{ORANGE}{DIM}{'─' * divider_len}{RESET}\n")


def _strip_ansi(text: str) -> str:
    import re
    return re.sub(r"\x1b\[[0-9;]*m", "", text)

class ThinkingIndicator:
    """Animación de carga robusta que no bloquea."""
    def __init__(self, message="Thinking"):
        self.message = message
        self.running = False
        self.thread = None
        # Estilos de animación: dots, spinner, pulse, wave
        self.style = os.getenv("THINKING_STYLE", "dots")

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
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()

    def _animate(self):
        i = 0
        if self.style == "spinner":
            chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        elif self.style == "pulse":
            chars = ["●    ", " ●   ", "  ●  ", "   ● ", "    ●", "   ● ", "  ●  ", " ●   "]
        elif self.style == "wave":
            chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        else:  # dots (default)
            chars = ["   ", ".  ", ".. ", "...", ".. ", ".  "]
        
        while self.running:
            sys.stdout.write(f"\r{Colors.cyan(self.message)} {Colors.yellow(chars[i % len(chars)])}")
            sys.stdout.flush()
            time.sleep(0.25)
            i += 1

# Cargar .env desde el directorio actual
import sys
from pathlib import Path
env_file = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_file)

# ============================================
# CLIENTE OAUTH (PKCE + OBO)
# ============================================

class TokenStore:
    def __init__(self, path=TOKEN_CACHE_FILE, force_auth=False):
        self.path = path
        self.force_auth = force_auth

    def load(self):
        if self.force_auth:
            return None  # Ignora cache si se pide --force-auth
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def save(self, data):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(Colors.red(f"No se pudo guardar token: {e}"))


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """Servidor mínimo para capturar el code de OAuth."""
    code = None
    state = None
    error = None
    error_description = None
    scopes = None  # Scopes del usuario
    access_token = None  # Token para extraer info
    id_token_payload = None  # Payload del ID token
    oauth_client = None  # Referencia al cliente OAuth para intercambiar token
    user_permissions = None  # Permisos específicos del usuario

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        
        # Reset de valores anteriores
        OAuthCallbackHandler.error = None
        OAuthCallbackHandler.error_description = None
        
        if "code" in qs:
            OAuthCallbackHandler.code = qs.get("code", [None])[0]
            OAuthCallbackHandler.state = qs.get("state", [None])[0]
            
            # NUEVO: Intercambiar code por token AQUÍ para obtener scopes inmediatamente
            code = OAuthCallbackHandler.code
            verifier = getattr(OAuthCallbackHandler, 'code_verifier', None)
            
            if OAuthCallbackHandler.oauth_client and code and verifier:
                token_data = OAuthCallbackHandler.oauth_client._exchange_code_for_token(code, verifier)
                if token_data and token_data.get("access_token"):
                    payload = OAuthCallbackHandler.oauth_client._decode_token_payload(token_data["access_token"])
                    if DEBUG_MODE:
                        print(f"[DEBUG] Access Token payload: {payload}")
                    
                    # También revisar el ID token que SÍ es JWT
                    id_token_payload = {}
                    if "id_token" in token_data:
                        id_token_payload = OAuthCallbackHandler.oauth_client._decode_token_payload(token_data["id_token"])
                        if DEBUG_MODE:
                            print(f"[DEBUG] ID Token payload: {json.dumps(id_token_payload, indent=2)}")
                    
                    # Intentar diferentes campos para scopes
                    scopes = payload.get("scope") or payload.get("scp") or payload.get("scopes") or ""
                    if not scopes and "scope" in token_data:
                        scopes = token_data["scope"]  # A veces está en el response del token
                    
                    # También revisar si hay scopes en el id_token
                    id_scopes = id_token_payload.get("scope") or id_token_payload.get("scp") or id_token_payload.get("scopes") or ""
                    
                    if DEBUG_MODE:
                        print(f"[DEBUG] Scopes en token response: {token_data.get('scope', 'N/A')}")
                        print(f"[DEBUG] Scopes en access_token: {scopes}")
                        print(f"[DEBUG] Scopes en id_token: {id_scopes}")
                        print(f"[DEBUG] Usuario (sub): {id_token_payload.get('sub', 'N/A')}")
                    
                    OAuthCallbackHandler.scopes = scopes or id_scopes
                    OAuthCallbackHandler.access_token = token_data["access_token"]
                    OAuthCallbackHandler.id_token_payload = id_token_payload
                    
                    # NUEVO: Verificar permisos específicos del usuario
                    # `sub` no siempre es el ID SCIM; pasamos todos los claims relevantes y resolvemos en backend
                    if id_token_payload:
                        # Hacer la consulta de permisos completamente silenciosa
                        try:
                            # Suprimir TODA salida durante la consulta de permisos
                            import sys
                            from io import StringIO
                            old_stdout = sys.stdout
                            old_stderr = sys.stderr
                            sys.stdout = StringIO()
                            sys.stderr = StringIO()
                            
                            user_permissions = OAuthCallbackHandler.oauth_client._check_user_permissions(id_token_payload)
                            
                            # Restaurar salida
                            sys.stdout = old_stdout
                            sys.stderr = old_stderr
                            
                            OAuthCallbackHandler.user_permissions = user_permissions
                            if DEBUG_MODE and user_permissions:
                                print(f"[DEBUG] Permisos específicos: {user_permissions}")
                        except Exception as e:
                            # Restaurar salida en caso de error
                            try:
                                sys.stdout = old_stdout
                                sys.stderr = old_stderr
                            except:
                                pass
                            
                            if DEBUG_MODE:
                                print(Colors.red(f"[DEBUG] Error obteniendo permisos: {e}"))
                            # Usar permisos vacíos por defecto
                            OAuthCallbackHandler.user_permissions = set()
                    
                    if DEBUG_MODE:
                        print(f"[DEBUG] Scopes finales extraídos: {OAuthCallbackHandler.scopes}")
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            # Construir lista de scopes si existen
            scopes_html = ""
            scopes_debug_info = ""
            
            if OAuthCallbackHandler.scopes:
                scopes_list = OAuthCallbackHandler.scopes.split() if isinstance(OAuthCallbackHandler.scopes, str) else OAuthCallbackHandler.scopes
                scopes_html = "<h3>📋 Scopes OAuth:</h3><ul>"
                for scope in scopes_list:
                    scopes_html += f"<li><code>{scope}</code></li>"
                scopes_html += "</ul>"
                
                # NUEVO: Mostrar permisos específicos de aplicación
                if hasattr(OAuthCallbackHandler, 'user_permissions') and OAuthCallbackHandler.user_permissions:
                    scopes_html += "<h3>🔑 Permisos de Aplicación:</h3><ul>"
                    for permission in sorted(OAuthCallbackHandler.user_permissions):
                        scopes_html += f"<li><span style='color: green;'>✓</span> <strong>{permission}</strong></li>"
                    scopes_html += "</ul>"
                    
                    # Mapear a funcionalidades del agente
                    can_view = "View Products" in OAuthCallbackHandler.user_permissions
                    can_update_prices = "Update Prices" in OAuthCallbackHandler.user_permissions  
                    can_update_descriptions = "Update Descriptions" in OAuthCallbackHandler.user_permissions
                    
                    if can_view and can_update_prices and can_update_descriptions:
                        scopes_html += "<h3 style='color: green;'>🟢 Funcionalidades del Agente Disponibles:</h3><ul>"
                        scopes_html += "<li>✓ Ver productos del catálogo</li>"
                        scopes_html += "<li>✓ Modificar precios de productos</li>"
                        scopes_html += "<li>✓ Actualizar descripciones</li>"
                        scopes_html += "</ul>"
                    else:
                        scopes_html += "<h3 style='color: orange;'>⚠️ Funcionalidades Limitadas:</h3><ul>"
                        if not can_view:
                            scopes_html += "<li style='color: red;'>❌ NO puede ver productos</li>"
                        if not can_update_prices:
                            scopes_html += "<li style='color: red;'>❌ NO puede modificar precios</li>"
                        if not can_update_descriptions:
                            scopes_html += "<li style='color: red;'>❌ NO puede actualizar descripciones</li>"
                        scopes_html += "</ul>"
                else:
                    scopes_html += "<h3 style='color: red;'>❌ Sin permisos de aplicación específicos</h3>"
                
                scopes_debug_info = f"<p><strong>Debug:</strong> Scopes raw = {OAuthCallbackHandler.scopes}</p>"
                
                # Agregar info del usuario del id_token
                if hasattr(OAuthCallbackHandler, 'id_token_payload') and OAuthCallbackHandler.id_token_payload:
                    user_sub = OAuthCallbackHandler.id_token_payload.get('sub', 'N/A')
                    scopes_debug_info += f"<p><strong>Usuario (sub):</strong> {user_sub}</p>"
                    scopes_debug_info += f"<p><strong>ID Token claims:</strong> {list(OAuthCallbackHandler.id_token_payload.keys())}</p>"
            else:
                scopes_html = "<h3>⚠️ Scopes:</h3><p>No se pudieron extraer los scopes del token</p>"
                scopes_debug_info = f"<p><strong>Debug:</strong> OAuthCallbackHandler.scopes = {repr(OAuthCallbackHandler.scopes)}</p>"
                scopes_debug_info += f"<p><strong>Debug:</strong> access_token presente = {bool(OAuthCallbackHandler.access_token)}</p>"
                scopes_debug_info += f"<p><strong>Debug:</strong> id_token_payload presente = {bool(getattr(OAuthCallbackHandler, 'id_token_payload', None))}</p>"
            
            html = f"""
            <html>
            <head><title>Login Exitoso</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: #28a745;">✅ Usuario Validado Correctamente</h2>
                <p>El código de autorización fue recibido exitosamente.</p>
                <p>Puedes volver a la terminal para continuar usando el agente.</p>
                {scopes_html}
                <hr>
                {scopes_debug_info}
                <small style="color: #666;">State: {OAuthCallbackHandler.state or "N/A"}</small>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            if DEBUG_MODE:
                print(Colors.green(f"Usuario validado - Code recibido, State: {OAuthCallbackHandler.state}"))
                if OAuthCallbackHandler.scopes:
                    print(Colors.green(f"Scopes: {OAuthCallbackHandler.scopes}"))
            else:
                # Mensaje opcional (traza) para confirmar que llegó el callback
                if _auth_trace_enabled():
                    print(Colors.debug("✅ Login completado. Vuelve a la terminal."))
        elif "error" in qs:
            OAuthCallbackHandler.error = qs.get("error", [None])[0]
            OAuthCallbackHandler.error_description = qs.get("error_description", ["Sin descripción"])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <head><title>Error de Autenticación</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: #dc3545;">❌ Usuario NO Validado</h2>
                <p><strong>Error:</strong> {}</p>
                <p><strong>Descripción:</strong> {}</p>
                <hr>
                <p>Verifica tus credenciales e intenta de nuevo.</p>
            </body>
            </html>
            """.format(OAuthCallbackHandler.error, OAuthCallbackHandler.error_description)
            self.wfile.write(html.encode('utf-8'))
            print(Colors.red(f"Usuario NO validado - Error: {OAuthCallbackHandler.error} - {OAuthCallbackHandler.error_description}"))
        else:
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <head><title>Callback Inválido</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: #ffc107;">⚠️ Callback Inválido</h2>
                <p>No se recibió código de autorización ni error.</p>
                <p>Parámetros recibidos: {}</p>
            </body>
            </html>
            """.format(list(qs.keys()))
            self.wfile.write(html.encode('utf-8'))
            print(Colors.red(f"Callback inválido - Parámetros: {list(qs.keys())}"))

    def log_message(self, format, *args):
        return  # Silencia logs HTTP


class OAuthClient:
    def __init__(self, force_auth=False):
        self.auth_endpoint = os.getenv("WSO2_AUTH_ENDPOINT")
        self.token_endpoint = os.getenv("WSO2_TOKEN_ENDPOINT")
        self.client_id = os.getenv("WSO2_CONSUMER_KEY")
        self.client_secret = os.getenv("WSO2_CONSUMER_SECRET")
        self.redirect_uri = os.getenv("WSO2_REDIRECT_URI", "http://localhost:8000/callback")
        self.scopes = os.getenv("WSO2_SCOPES", "openid update_prices update_descriptions view_products offline_access")
        self.store = TokenStore(force_auth=force_auth)
        
        # Si se fuerza autenticación, limpiar datos anteriores del callback handler
        if force_auth:
            OAuthCallbackHandler.code = None
            OAuthCallbackHandler.state = None
            OAuthCallbackHandler.error = None
            OAuthCallbackHandler.error_description = None
            OAuthCallbackHandler.scopes = None
            OAuthCallbackHandler.access_token = None
            OAuthCallbackHandler.id_token_payload = None
            OAuthCallbackHandler.user_permissions = None

    def _now(self):
        return int(time.time())

    def _token_valid(self, tokens):
        return tokens and tokens.get("access_token") and tokens.get("expires_at", 0) > self._now() + 30

    def _refresh(self, tokens):
        if not tokens or not tokens.get("refresh_token"):
            return None
        data = {
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
        }
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(self.token_endpoint, data=data, headers=headers, verify=False)
        if r.status_code == 200:
            tok = r.json()
            tok["expires_at"] = self._now() + tok.get("expires_in", 3600)
            tok.setdefault("refresh_token", tokens.get("refresh_token"))
            self.store.save(tok)
            return tok
        return None

    def _start_callback_server(self):
        parsed = urllib.parse.urlparse(self.redirect_uri)
        port = parsed.port or 8000

        # Evita falsos "Address already in use" tras reinicios rápidos
        socketserver.TCPServer.allow_reuse_address = True

        # NO cambiar de puerto automáticamente: WSO2 suele tener redirect_uri fijo registrado
        try:
            server = socketserver.TCPServer(("", port), OAuthCallbackHandler)
        except OSError as e:
            if getattr(e, "errno", None) == 48:  # Address already in use (macOS)
                raise Exception(
                    f"El puerto {port} está en uso. Cierra instancias previas del agente o ejecuta start_agent.sh para liberar puertos."
                )
            raise

        th = threading.Thread(target=server.serve_forever)
        th.daemon = True
        th.start()
        return server

    def _stop_callback_server(self, server):
        try:
            server.shutdown()
            server.server_close()
        except Exception:
            pass

    def _generate_pkce(self):
        verifier = secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
        return verifier, challenge

    def _check_user_permissions(self, user_ref):
        """Verificar permisos del usuario autenticado (sin hardcodear roles).

        `user_ref` puede ser:
        - string (SCIM user id, username, email, etc.)
        - dict (claims del ID Token)
        - lista/tupla de candidatos
        """
        try:
            import requests
            import base64
            import urllib3

            urllib3.disable_warnings()

            wso2_base = os.getenv("WSO2_IS_BASE", "https://localhost:9443")
            admin_user = os.getenv("WSO2_ADMIN_USER", "admin")
            admin_pass = os.getenv("WSO2_ADMIN_PASS", "admin")
            encoded = base64.b64encode(f"{admin_user}:{admin_pass}".encode()).decode()
            headers = {"Authorization": f"Basic {encoded}", "Content-Type": "application/json"}

            def _as_candidates(ref):
                if ref is None:
                    return []
                if isinstance(ref, (list, tuple, set)):
                    return [str(x).strip() for x in ref if x]
                if isinstance(ref, dict):
                    keys = [
                        "sub",
                        "preferred_username",
                        "username",
                        "userName",
                        "email",
                        "upn",
                    ]
                    cands = []
                    for k in keys:
                        v = ref.get(k)
                        if v:
                            cands.append(str(v).strip())
                    return cands
                return [str(ref).strip()]

            def _get_user_by_id(scim_id):
                url = f"{wso2_base}/scim2/Users/{urllib.parse.quote(str(scim_id))}"
                r = requests.get(url, headers=headers, verify=False, timeout=3)
                if r.status_code == 200:
                    return r.json()
                return None

            def _search_user_by_username(username):
                # SCIM filter needs quotes; keep it simple and safe
                filt = f'userName eq "{username}"'
                url = f"{wso2_base}/scim2/Users"
                r = requests.get(
                    url,
                    headers=headers,
                    params={"filter": filt, "startIndex": 1, "count": 1},
                    verify=False,
                    timeout=3,
                )
                if r.status_code == 200:
                    data = r.json()
                    resources = data.get("Resources", [])
                    if resources:
                        return resources[0]
                return None

            candidates = []
            for c in _as_candidates(user_ref):
                if c and c not in candidates:
                    candidates.append(c)

            if DEBUG_MODE:
                print(Colors.cyan(f"[DEBUG] Resolviendo usuario SCIM con candidatos: {candidates}"))

            user_data = None
            for cand in candidates:
                # 1) Probar como SCIM id directamente
                user_data = _get_user_by_id(cand)
                if user_data:
                    break
                # 2) Probar como username
                user_data = _search_user_by_username(cand)
                if user_data:
                    break

            if not user_data:
                if DEBUG_MODE:
                    print(Colors.red("[DEBUG] No se pudo resolver el usuario SCIM; permisos vacíos"))
                return set()

            # WSO2 suele devolver pertenencia en `groups` (y a veces también en `roles`)
            memberships = []
            memberships.extend(user_data.get("groups", []) or [])
            memberships.extend(user_data.get("roles", []) or [])

            role_ids = []
            for m in memberships:
                if isinstance(m, dict):
                    rid = m.get("value") or m.get("id")
                    if rid and rid not in role_ids:
                        role_ids.append(rid)
                elif isinstance(m, str):
                    if m and m not in role_ids:
                        role_ids.append(m)

            if DEBUG_MODE:
                displays = [m.get("display") for m in memberships if isinstance(m, dict) and m.get("display")]
                print(Colors.cyan(f"[DEBUG] Roles/Groups detectados: {displays} (IDs: {role_ids})"))

            permissions = set()
            for rid in role_ids:
                role_url = f"{wso2_base}/scim2/v2/Roles/{urllib.parse.quote(str(rid))}"
                rr = requests.get(role_url, headers=headers, verify=False, timeout=3)
                if rr.status_code != 200:
                    if DEBUG_MODE:
                        print(Colors.red(f"[DEBUG] No se pudo obtener rol {rid}: HTTP {rr.status_code}"))
                    continue

                role_data = rr.json()
                role_permissions = role_data.get("permissions", []) or []
                for perm in role_permissions:
                    if isinstance(perm, dict):
                        name = perm.get("display") or perm.get("value")
                        if name:
                            permissions.add(str(name))
                    elif isinstance(perm, str) and perm:
                        permissions.add(perm)

            return permissions

        except requests.exceptions.RequestException:
            if DEBUG_MODE:
                print(Colors.red("❌ Error de red conectando a WSO2 Identity Server"))
            return set()
        except Exception as e:
            if DEBUG_MODE:
                print(Colors.red(f"Error verificando permisos: {e}"))
            return set()

    def _decode_token_payload(self, token):
        """Decodifica el payload JWT sin verificar firma (solo para lectura)."""
        try:
            # JWT format: header.payload.signature
            parts = token.split('.')
            if len(parts) != 3:
                if DEBUG_MODE:
                    print(Colors.red(f"Token no tiene formato JWT válido: {len(parts)} partes"))
                return {}
            
            # Decodificar payload (agregar padding si es necesario)
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            
            decoded = base64.urlsafe_b64decode(payload)
            payload_json = json.loads(decoded)
            
            if DEBUG_MODE:
                print(Colors.cyan(f"[DEBUG] JWT payload decodificado: {json.dumps(payload_json, indent=2)}"))
            
            return payload_json
        except Exception as e:
            if DEBUG_MODE:
                print(Colors.red(f"Error al decodificar token: {e}"))
                print(Colors.red(f"Token (primeros 50 chars): {token[:50]}..."))
            return {}

    def _exchange_code_for_token(self, code, verifier):
        """Intercambia el authorization code por un access token usando PKCE"""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": verifier,
        }
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"}
        
        try:
            r = requests.post(self.token_endpoint, data=data, headers=headers, verify=False)
            if r.status_code == 200:
                tok = r.json()
                tok["expires_at"] = self._now() + tok.get("expires_in", 3600)
                
                # Debug: mostrar todo el token response
                if DEBUG_MODE:
                    print(Colors.cyan(f"[DEBUG] Token response completo: {json.dumps(tok, indent=2)}"))
                    if "access_token" in tok:
                        print(Colors.cyan(f"[DEBUG] Access token (primeros 100 chars): {tok['access_token'][:100]}..."))
                        print(Colors.cyan(f"[DEBUG] Es JWT? {tok['access_token'].count('.') == 2}"))
                
                return tok
            else:
                if DEBUG_MODE:
                    print(Colors.red(f"Error intercambiando token: {r.status_code} {r.text}"))
                return None
        except Exception as e:
            if DEBUG_MODE:
                print(Colors.red(f"Exception intercambiando token: {e}"))
            return None

    def _interactive_auth(self):
        verifier, challenge = self._generate_pkce()
        state = secrets.token_urlsafe(16)

        # Arrancar servidor de callback ANTES de construir el URL, por si hay que cambiar puerto
        OAuthCallbackHandler.oauth_client = self
        OAuthCallbackHandler.code_verifier = verifier
        try:
            server = self._start_callback_server()
        except Exception as e:
            print(Colors.red(str(e)))
            return None
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "state": state,
            "prompt": "login"  # Forzar login incluso si hay sesión activa
        }
        url = f"{self.auth_endpoint}?{urllib.parse.urlencode(params)}"
        print(Colors.yellow("Abre este URL para autorizar (PKCE/OBO):"))
        print(url)
        try:
            webbrowser.open(url)
        except Exception:
            pass

        if _auth_trace_enabled():
            print(Colors.debug(f"Esperando callback en {self.redirect_uri} ..."))
        # Espera hasta que el handler capture el code
        for _ in range(300):
            if OAuthCallbackHandler.code:
                break
            time.sleep(1)
        self._stop_callback_server(server)

        # Verificar si hubo error de autenticación
        if OAuthCallbackHandler.error:
            error = OAuthCallbackHandler.error
            desc = OAuthCallbackHandler.error_description
            OAuthCallbackHandler.error = None
            OAuthCallbackHandler.error_description = None
            print(Colors.red(f"Autenticación fallida: {error} - {desc}"))
            return None

        code = OAuthCallbackHandler.code
        OAuthCallbackHandler.code = None
        if not code:
            print(Colors.red("No se recibió code. Intenta de nuevo."))
            return None

        if _auth_trace_enabled():
            print(Colors.debug("Código de autorización recibido. Intercambiando por token..."))
        
        # Si el token ya fue intercambiado en el callback, usarlo
        if OAuthCallbackHandler.access_token:
            # Crear estructura de token para guardar
            tok = {
                "access_token": OAuthCallbackHandler.access_token,
                "expires_at": self._now() + 3600,  # Asumir 1 hora por defecto
                "scope": OAuthCallbackHandler.scopes
            }
            self.store.save(tok)
            return tok
        
        # Fallback: intercambiar aquí si no se hizo en callback
        tok = self._exchange_code_for_token(code, verifier)
        if tok:
            # Extraer scopes del token (por si acaso)
            access_token = tok.get("access_token")
            if access_token:
                payload = self._decode_token_payload(access_token)
                scopes = payload.get("scope", "")
                tok["scope"] = scopes
            
            self.store.save(tok)
            return tok
        
        print(Colors.red("Error al intercambiar code por token"))
        return None

    def ensure_token(self):
        if DEBUG_MODE:
            print(Colors.cyan("[DEBUG] ensure_token() llamado"))
        
        tokens = self.store.load()
        if self._token_valid(tokens):
            if DEBUG_MODE:
                print(Colors.cyan("[DEBUG] Token válido encontrado en cache"))
            return tokens.get("access_token")
            
        if tokens and tokens.get("refresh_token"):
            if DEBUG_MODE:
                print(Colors.cyan("[DEBUG] Intentando refresh token"))
            refreshed = self._refresh(tokens)
            if refreshed and self._token_valid(refreshed):
                return refreshed.get("access_token")
                
        if DEBUG_MODE:
            print(Colors.cyan("[DEBUG] Necesita autenticación interactiva"))
        new_tok = self._interactive_auth()
        return new_tok.get("access_token") if new_tok else None

# ============================================
# LÓGICA WEATHER MCP (Plugin)
# ============================================

class WeatherPlugin:
    """Plugin para interactuar con el MCP Weather a través de WSO2 APIM"""
    
    def __init__(self, force_auth=False):
        # Weather MCP usa Client Credentials, no requiere autenticación de usuario
        # Las credenciales se toman de WSO2_APIM_CONSUMER_KEY/SECRET
        self._token_cache = None
        self._token_expires_at = 0
        
        # URL del MCP Weather a través de APIM
        self.mcp_base_url = os.getenv("WSO2_WEATHER_MCP_URL", "https://localhost:9453/weather-mcp/1.0.0")
        
        if DEBUG_MODE:
            print(Colors.cyan(f"[DEBUG] WeatherPlugin inicializado - URL: {self.mcp_base_url}"))
    
    def _get_apim_token(self):
        """Obtener token OAuth2 usando Client Credentials (mismo método que el Gateway)"""
        # Reusar token si todavía es válido
        now = time.time()
        if self._token_cache and now < (self._token_expires_at - 30):
            return self._token_cache
        
        # Obtener nuevo token
        try:
            from oauth2_apim import _fetch_oauth2_token_sync
            token, expires_in = _fetch_oauth2_token_sync()
            self._token_cache = token
            self._token_expires_at = time.time() + expires_in
            return token
        except Exception as e:
            if DEBUG_MODE:
                print(Colors.red(f"Error obteniendo token APIM: {e}"))
            return None
    
    def _call_mcp(self, tool_name: str, params: dict = None):
        """Llamar a una herramienta del MCP a través de APIM"""
        token = self._get_apim_token()
        if not token:
            return {"error": "No se pudo obtener token de autenticación"}
        
        url = f"{self.mcp_base_url}/tools/{tool_name}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            if DEBUG_MODE:
                print(Colors.cyan(f"[MCP] Llamando a {tool_name} con params: {params}"))
                print(Colors.cyan(f"[MCP] URL: {url}"))
            
            response = requests.post(
                url,
                headers=headers,
                json={"params": params or {}},
                verify=False  # Para localhost con certificados self-signed
            )
            
            if DEBUG_MODE:
                print(Colors.cyan(f"[MCP] Status: {response.status_code}"))
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {"error": "Token de autenticación inválido o expirado"}
            elif response.status_code == 403:
                return {"error": "Sin permisos para esta operación"}
            else:
                if DEBUG_MODE:
                    print(Colors.red(f"MCP Error {response.status_code}: {response.text}"))
                return {"error": f"Error MCP {response.status_code}"}
        
        except requests.exceptions.ConnectionError:
            return {"error": f"No se pudo conectar al MCP Weather: {self.mcp_base_url}"}
        except Exception as e:
            if DEBUG_MODE:
                print(Colors.red(f"Exception en MCP call: {str(e)}"))
            return {"error": f"Error inesperado: {str(e)}"}
    
    @kernel_function(
        name="get_current_weather",
        description="Obtiene el clima actual de una ciudad española. Ciudades disponibles: madrid, barcelona, valencia, sevilla, malaga, bilbao, zaragoza, murcia, palma, las_palmas, alicante, cordoba, valladolid, vigo, gijon, la_coruna, granada, vitoria, elche, oviedo, santa_cruz_tenerife, pamplona, almeria, san_sebastian, burgos, santander, castellon, albacete, logrono, badajoz, salamanca, huelva, lleida, tarragona, leon, cadiz, jaen, orense, lugo, caceres, melilla, ceuta"
    )
    def get_current_weather(self, city: str = "madrid"):
        """Obtiene el clima actual de una ciudad española"""
        result = self._call_mcp("get_current_weather", {"city": city.lower()})
        
        if "error" in result:
            return Colors.red(f"Error: {result['error']}")
        
        return result.get("content", "No se pudo obtener información del clima")
    
    @kernel_function(
        name="get_weather_forecast",
        description="Obtiene el pronóstico del clima para los próximos días en una ciudad española. Parámetros: city (nombre de la ciudad), days (número de días, máximo 7)"
    )
    def get_weather_forecast(self, city: str = "madrid", days: int = 5):
        """Obtiene el pronóstico del clima para los próximos días"""
        result = self._call_mcp("get_weather_forecast", {"city": city.lower(), "days": min(days, 7)})
        
        if "error" in result:
            return Colors.red(f"Error: {result['error']}")
        
        return result.get("content", "No se pudo obtener el pronóstico del clima")
    
    @kernel_function(
        name="get_retail_weather_insights",
        description="Obtiene insights de clima enfocados en retail y e-commerce para una ciudad española. Incluye recomendaciones de inventario y estrategias de marketing basadas en el pronóstico del clima."
    )
    def get_retail_weather_insights(self, city: str = "madrid", days: int = 3):
        """Obtiene insights de clima para decisiones de retail"""
        result = self._call_mcp("get_retail_weather_insights", {"city": city.lower(), "days": min(days, 7)})
        
        if "error" in result:
            return Colors.red(f"Error: {result['error']}")
        
        return result.get("content", "No se pudieron obtener insights de retail")

# ============================================
# LÓGICA SHOPIFY (Plugin)
# ============================================

class PriceMemory:
    def __init__(self): self.history = {}
    def remember(self, pid, old, new): self.history[pid] = {'old': old, 'new': new}
    def get_old(self, pid): return self.history.get(pid, {}).get('old')

class ShopifyPlugin:
    def __init__(self, force_auth=False):
        self.memory = PriceMemory()
        self.oauth = OAuthClient(force_auth=force_auth)
        self._token_cache = None
        self._token_initialized = False
        self._user_permissions = set()  # Permisos del usuario autenticado
        self._force_auth = force_auth  # Recordar si se fuerza autenticación
        
        # Si se fuerza autenticación, limpiar permisos anteriores
        if force_auth:
            self._user_permissions = set()
            self._token_initialized = False
            
        if DEBUG_MODE:
            print(Colors.cyan("[DEBUG] ShopifyPlugin inicializado (sin autenticación aún)"))

    def _get_token(self):
        # Solo inicializar token cuando realmente se necesite una operación
        # O si se está forzando autenticación, permitir reinicialización
        if not self._token_initialized or self._force_auth:
            if self._force_auth:
                if _auth_trace_enabled():
                    print(Colors.debug("🔄 Forzando nueva autenticación completa..."))
                # Limpiar permisos anteriores
                self._user_permissions = set()
            else:
                if _auth_trace_enabled():
                    print(Colors.debug("🔐 Autenticación OAuth iniciada..."))
            
            self._token_initialized = True
            
            # Primero obtener el token (esto desencadena la autenticación)
            token = self.oauth.ensure_token()
            
            if not token:
                print(Colors.red("❌ No se pudo obtener token OAuth. Verifica WSO2 Identity Server."))
                # Sin token => no hay permisos
                self._user_permissions = set()
                return None

            # Si llegamos aquí, ya hay token: desactivar "force auth" para evitar re-login en cada llamada
            self._force_auth = False
            try:
                self.oauth.store.force_auth = False
            except Exception:
                pass
            
            # Luego obtener los permisos del usuario autenticado desde el callback
            # Si hay problemas con WSO2, usar permisos por defecto
            if hasattr(OAuthCallbackHandler, 'user_permissions') and OAuthCallbackHandler.user_permissions is not None:
                self._user_permissions = OAuthCallbackHandler.user_permissions
                if self._user_permissions:
                    if DEBUG_MODE:
                        print(Colors.green(f"🔑 Permisos OAuth cargados: {sorted(self._user_permissions)}"))
                else:
                    print(Colors.yellow("⚠️ Usuario autenticado pero sin permisos."))
            else:
                print(Colors.yellow("⚠️ No se pudieron verificar permisos WSO2."))
                self._user_permissions = set()
                
            return token
                
        return self.oauth.ensure_token()
    
    def _has_permission(self, required_permission):
        """Verificar si el usuario tiene un permiso específico"""
        return required_permission in self._user_permissions
    
    def _check_permission(self, required_permission, action_name):
        """Verificar permiso y retornar mensaje de error si no lo tiene"""
        # Si aún no hay sesión/token inicializado, pedir login al primer uso
        if not self._token_initialized:
            token = self._get_token()
            if not token:
                return Colors.red(f"Necesitas iniciar sesión para {action_name}.")

        if not self._has_permission(required_permission):
            if DEBUG_MODE:
                print(Colors.cyan(f"[DEBUG] Permisos actuales: {sorted(self._user_permissions)}"))
                print(Colors.cyan(f"[DEBUG] Permiso requerido: {required_permission}"))
                print(Colors.cyan(f"[DEBUG] Token inicializado: {self._token_initialized}"))
            
            # Mensaje simple y directo como prefiere el usuario
            return Colors.red(f"No tienes permisos para {action_name}.")
        return None

    def _api(self, method, path, data=None):
        # Nota: OAuth solo se usa para permisos. Las llamadas a Shopify NO deben disparar OAuth.
        # Los permisos se validan en los métodos (vía _check_permission).
        
        # Verificar que el token de Shopify esté configurado
        shopify_token = os.getenv("SHOPIFY_API_TOKEN")
        if not shopify_token:
            return {"error": "SHOPIFY_API_TOKEN no configurado en el archivo .env"}
        
        # Usar Shopify directamente
        shopify_store = os.getenv("SHOPIFY_STORE_URL", "https://rafa-ecommerce.myshopify.com")
        url = f"{shopify_store}/admin/api/2024-01{path}"
        
        headers = {
            "X-Shopify-Access-Token": shopify_token,
            "Content-Type": "application/json"
        }
        
        if DEBUG_MODE:
            print(Colors.cyan(f"[API] {method} {url}"))
            print(Colors.cyan(f"[DEBUG] Token Shopify configurado: {shopify_token[:10]}..."))
        
        try:
            if method == 'GET': 
                r = requests.get(url, headers=headers, verify=False)
            else: 
                r = requests.put(url, headers=headers, json=data, verify=False)
            
            # Manejar errores específicos de Shopify
            if r.status_code == 401:
                error_msg = "Token de Shopify inválido o expirado. Verifica SHOPIFY_API_TOKEN en .env"
                print(Colors.red(f"[SHOPIFY ERROR 401] {error_msg}"))
                if DEBUG_MODE:
                    print(Colors.red(f"Response: {r.text}"))
                return {"error": error_msg}
            elif r.status_code == 403:
                error_msg = "Sin permisos para esta operación en Shopify. Verifica los scopes del token."
                print(Colors.red(f"[SHOPIFY ERROR 403] {error_msg}"))
                return {"error": error_msg}
            elif r.status_code not in [200, 201]:
                if DEBUG_MODE:
                    print(Colors.red(f"API Error {r.status_code}: {r.text}"))
                return {"error": f"Shopify API Error {r.status_code}: {r.text[:200]}"}
            
            return r.json() if r.content else {}
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"No se pudo conectar a Shopify. Verifica SHOPIFY_STORE_URL: {shopify_store}"
            print(Colors.red(f"[CONNECTION ERROR] {error_msg}"))
            return {"error": error_msg}
        except Exception as e: 
            if DEBUG_MODE:
                print(Colors.red(f"Exception en API call: {str(e)}"))
            return {"error": f"Error inesperado: {str(e)}"}

    def find_id_by_name(self, name):
        # Este método hace llamadas a Shopify => requiere permiso de lectura
        permission_error = self._check_permission("View Products", "buscar productos")
        if permission_error:
            return None

        data = self._api("GET", "/products.json")
        if "products" in data:
            for p in data["products"]:
                if name.lower() in p["title"].lower():
                    return str(p['id'])
        return None

    def get_product_price(self, product_id):
        # Verificar permisos antes de consultar precios
        permission_error = self._check_permission("View Products", "consultar precios de productos")
        if permission_error:
            return permission_error
            
        curr = self._api("GET", f"/products/{product_id}.json")
        if "product" in curr:
            title = curr["product"]["title"]
            price = curr["product"]["variants"][0]["price"]
            return f"El precio de '{title}' es ${price}"
        return Colors.red("Producto no encontrado")

    @kernel_function(name="get_products_list")
    def get_products_list(self, show_price=True):
        # Verificar permisos antes de listar productos
        permission_error = self._check_permission("View Products", "ver productos del catálogo")
        if permission_error:
            return permission_error
            
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
        # Verificar permisos antes de actualizar precios
        permission_error = self._check_permission("Update Prices", "modificar precios de productos")
        if permission_error:
            return permission_error
            
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

    def update_product_price_by_percent(self, product_id: str, percent: float):
        """Actualiza el precio aplicando un porcentaje al precio actual."""
        permission_error = self._check_permission("Update Prices", "modificar precios de productos")
        if permission_error:
            return permission_error

        curr = self._api("GET", f"/products/{product_id}.json")
        if "product" not in curr:
            return Colors.red("Producto no encontrado")

        title = curr["product"].get("title", "")
        old_str = str(curr["product"]["variants"][0]["price"])
        try:
            old = Decimal(old_str)
        except Exception:
            return Colors.red("No pude leer el precio actual del producto")

        factor = Decimal("1") + (Decimal(str(percent)) / Decimal("100"))
        new = (old * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        res = self.update_product_price(product_id, str(new))
        # Añadir contexto útil (sin ser debug)
        if res.startswith(Colors.GREEN):
            return Colors.green(f"Precio actualizado ({percent:+g}%): ${old_str} -> ${new} ({title})")
        return res

    @kernel_function(name="update_description")
    def update_description(self, product_id, text):
        # Verificar permisos antes de actualizar descripciones
        permission_error = self._check_permission("Update Descriptions", "actualizar descripciones de productos")
        if permission_error:
            return permission_error
            
        payload = {"product": {"id": int(product_id), "body_html": text}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        return Colors.green("Descripción actualizada") if "product" in res else Colors.red("Error")

    @kernel_function(name="get_product_description")
    def get_product_description(self, product_id):
        # Verificar permisos antes de consultar descripciones
        permission_error = self._check_permission("View Products", "consultar descripciones de productos")
        if permission_error:
            return permission_error

        curr = self._api("GET", f"/products/{product_id}.json")
        if "product" in curr:
            title = curr["product"].get("title", "")
            body_html = curr["product"].get("body_html") or ""
            # No tocamos HTML: lo devolvemos tal cual para verificar que se actualizó
            return f"Descripción de '{title}':\n{body_html}"
        return Colors.red("Producto no encontrado")

    @kernel_function(name="update_title")
    def update_title(self, product_id, title):
        # Por ahora reutilizamos el permiso de descripciones para cambios de contenido del producto.
        # Si quieres separar permisos, cambia "Update Descriptions" por "Update Titles" y crea ese permiso en WSO2.
        permission_error = self._check_permission("Update Descriptions", "actualizar títulos de productos")
        if permission_error:
            return permission_error

        payload = {"product": {"id": int(product_id), "title": str(title)}}
        res = self._api("PUT", f"/products/{product_id}.json", payload)
        return Colors.green("Título actualizado") if "product" in res else Colors.red("Error")

    @kernel_function(name="revert_price")
    def revert_price(self, product_id):
        old = self.memory.get_old(product_id)
        if old: return self.update_product_price(product_id, old)
        return Colors.red("No hay historial")

    @kernel_function(name="count_products")
    def count_products(self):
        # Verificar permisos antes de contar productos
        permission_error = self._check_permission("View Products", "contar productos")
        if permission_error:
            return permission_error
            
        d = self._api("GET", "/products/count.json")
        return f"Total: {d.get('count', 0)}"

    @kernel_function(name="sort_products")
    def sort_products(self):
        permission_error = self._check_permission("View Products", "ver productos del catálogo")
        if permission_error:
            return permission_error

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
    def __init__(self, kernel, shopify_plugin, weather_plugin=None):
        self.kernel = kernel
        self.shopify_plugin = shopify_plugin
        self.weather_plugin = weather_plugin

    def _clean_json(self, text):
        try:
            if text is None:
                return None

            s = str(text).strip()
            if not s:
                return None

            # Si viene dentro de un bloque markdown ```...```, quítalo sin regex
            if s.startswith("```"):
                lines = s.splitlines()
                # eliminar primera línea ``` o ```json
                if lines:
                    lines = lines[1:]
                # eliminar última línea ```
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                s = "\n".join(lines).strip()

            # Intento directo
            try:
                return json.loads(s)
            except Exception:
                pass

            # Intento recortando al primer/último delimitador (sin regex)
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

    async def _extract_json(self, function_name: str, user_input: str):
        try:
            res = await self.kernel.invoke(
                function_name=function_name,
                plugin_name="extractor",
                arguments=KernelArguments(input=user_input),
            )
            return self._clean_json(str(res))
        except Exception:
            return None

    async def run(self, user_input):
        # Instanciamos el indicador nuevo CADA VEZ para evitar errores de hilo
        indicator = ThinkingIndicator("")
        if not DEBUG_MODE and _thinking_enabled():
            indicator.start()
        
        result = ""
        try:
            # 1. CLASIFICAR INTENCIÓN (Prompt Mejorado con Weather)
            intent_prompt = (
                "Clasifica la intención en: ['listar', 'consultar_precio', 'actualizar_precio', 'consultar_descripcion', 'descripcion', 'actualizar_titulo', 'revertir', 'contar', 'ordenar', 'clima_actual', 'pronostico_clima', 'insights_retail', 'general']\n"
                "EJEMPLOS SHOPIFY:\n"
                "User: 'Cuanto vale la gift card?' -> {\"category\": \"consultar_precio\"}\n"
                "User: 'Pon la Gift Card a 50' -> {\"category\": \"actualizar_precio\"}\n"
                "User: 'Dame la descripción de la Camiseta' -> {\"category\": \"consultar_descripcion\"}\n"
                "User: 'Actualiza la descripcion de la Camiseta a Nueva camiseta' -> {\"category\": \"descripcion\"}\n"
                "User: 'Cambia el nombre de la Camiseta a Camiseta Apicuriosa' -> {\"category\": \"actualizar_titulo\"}\n"
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
            indicator.start()
            raw = str(await self.kernel.invoke_prompt(intent_prompt))
            data = self._clean_json(raw)
            intent = data.get("category", "general") if data else "general"

            # Heurísticas para evitar confusiones frecuentes
            u_lower = user_input.lower()

            # Consultar descripción vs actualizar descripción
            if any(k in u_lower for k in ["descripción", "descripcion", "description", "body_html"]):
                if any(v in u_lower for v in ["dame", "muestra", "muéstrame", "ver", "enseña", "cual es", "cuál es"]):
                    intent = "consultar_descripcion"
                if any(v in u_lower for v in ["actualiza", "modifica", "cambia", "pon", "actualizar", "modificar", "cambiar"]):
                    intent = "descripcion"

            # Actualizar título/nombre
            if any(k in u_lower for k in ["título", "titulo", "nombre", "renombra", "renombrar"]):
                if any(v in u_lower for v in ["actualiza", "modifica", "cambia", "pon", "actualizar", "modificar", "cambiar", "renombra", "renombrar"]):
                    intent = "actualizar_titulo"
            
            if DEBUG_MODE:
                indicator.stop()
                print(f"\nDEBUG Intent: {intent}")
                indicator = ThinkingIndicator("")
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
                
                result = self.shopify_plugin.get_products_list(show_price=show_p)

            elif intent == "contar": result = self.shopify_plugin.count_products()
            elif intent == "ordenar": result = self.shopify_plugin.sort_products()
            
            elif intent == "consultar_precio":
                # Si no puede ver productos, devolver error de permisos directamente
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
                # Si no puede modificar precios, devolver error de permisos directamente
                permission_error = self.shopify_plugin._check_permission("Update Prices", "modificar precios de productos")
                if permission_error:
                    result = permission_error
                else:
                    pct = _parse_percent_adjustment(user_input)
                    if pct is not None:
                        # Caso: "incrementa/baja X% el precio de <producto>"
                        pref = await self._extract_json("extract_product_ref", user_input)
                        pname = str((pref or {}).get("product") or "").strip()
                        if not pname:
                            # fallback: intentar al menos extraer product desde extractor de precio
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
                        # Caso clásico: el usuario da un precio absoluto
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
                # Si no puede actualizar descripciones, devolver error de permisos directamente
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
                        if DEBUG_MODE:
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
                # Reutilizamos el mismo permiso que descripciones para cambios de contenido del producto
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
                # Revertir precio implica modificar precios
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
            
            # INTENCIONES DE WEATHER MCP
            elif intent == "clima_actual":
                if self.weather_plugin:
                    # Extraer ciudad del input
                    prompt = f"Extrae SOLO el nombre de la ciudad española mencionada en: '{user_input}'. Si no hay ciudad, devuelve 'madrid'. Solo la ciudad, nada más."
                    city = str(await self.kernel.invoke_prompt(prompt)).strip().lower()
                    result = self.weather_plugin.get_current_weather(city=city)
                else:
                    result = Colors.red("Plugin de clima no disponible")
            
            elif intent == "pronostico_clima":
                if self.weather_plugin:
                    # Extraer ciudad y días del input
                    prompt = f"Extrae la ciudad española y número de días (si se menciona) de: '{user_input}'. Devuelve JSON con {{\"city\": \"nombre\", \"days\": numero}}. Si no hay ciudad, usa 'madrid'. Si no hay días, usa 5."
                    extraction = str(await self.kernel.invoke_prompt(prompt)).strip()
                    data = self._clean_json(extraction)
                    city = data.get("city", "madrid").lower() if data else "madrid"
                    days = int(data.get("days", 5)) if data and data.get("days") else 5
                    result = self.weather_plugin.get_weather_forecast(city=city, days=days)
                else:
                    result = Colors.red("Plugin de clima no disponible")
            
            elif intent == "insights_retail":
                if self.weather_plugin:
                    # Extraer ciudad del input
                    prompt = f"Extrae SOLO el nombre de la ciudad española mencionada en: '{user_input}'. Si no hay ciudad, devuelve 'madrid'. Solo la ciudad, nada más."
                    city = str(await self.kernel.invoke_prompt(prompt)).strip().lower()
                    result = self.weather_plugin.get_retail_weather_insights(city=city)
                else:
                    result = Colors.red("Plugin de clima no disponible")

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
        parser = argparse.ArgumentParser(description="Rafa's Agent - Agente Shopify con WSO2")
        parser.add_argument('-d', '--debug', action='store_true', help='Modo debug con logs detallados')
        parser.add_argument('--force-auth', action='store_true', help='Fuerza nuevo login, ignorando cache')
        parser.add_argument('--custom', type=str, default='default', help='Banner personalizado (nombre del archivo en banners/)')
        parser.add_argument('--list-banners', action='store_true', help='Lista todos los banners disponibles')
        args = parser.parse_args()
        
        if args.list_banners:
            available = list_available_banners()
            print("Banners disponibles:")
            for banner in available:
                print(f"  - {banner}")
            return
        
        DEBUG_MODE = args.debug

        print_start_motd(banner_name=args.custom)
        print(Colors.cyan("=== AGENTE SHOPIFY IA (v2.5 FINAL) ==="))
        if DEBUG_MODE: print(Colors.cyan("[DEBUG MODE ON]"))
        if args.force_auth and _auth_trace_enabled():
            print(Colors.cyan("[Forzando nueva autenticación...]"))

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
            if gateway_client:
                print(Colors.green("Usando Gateway APIM con OAuth2"))
            else:
                print(Colors.yellow("No se pudo crear cliente Gateway; usando OpenAI directo"))

        try:
            if gateway_client:
                kernel.add_service(
                    OpenAIChatCompletion(
                        service_id="openai",
                        ai_model_id="gpt-4o-mini",
                        async_client=gateway_client,
                        api_key="unused",
                    )
                )
            else:
                if not os.getenv("OPENAI_API_KEY"):
                    return print(Colors.red("Falta OPENAI_API_KEY (o configura WSO2_* para usar el Gateway)"))
                kernel.add_service(
                    OpenAIChatCompletion(
                        service_id="openai",
                        api_key=os.getenv("OPENAI_API_KEY"),
                        ai_model_id="gpt-4o-mini",
                    )
                )
        except Exception as e:
            if DEBUG_MODE:
                print(Colors.yellow(f"Detalles error OpenAI: {e}"))
                traceback.print_exc()
            return print(Colors.red("Error OpenAI"))

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

        shopify_plugin = ShopifyPlugin(force_auth=args.force_auth)
        
        # Inicializar Weather Plugin si está configurado
        weather_plugin = None
        if os.getenv("WSO2_WEATHER_MCP_URL") or os.getenv("WSO2_APIM_CONSUMER_KEY"):
            try:
                weather_plugin = WeatherPlugin(force_auth=args.force_auth)
                print(Colors.green("✓ Weather MCP Plugin inicializado"))
            except Exception as e:
                if DEBUG_MODE:
                    print(Colors.yellow(f"⚠ No se pudo inicializar Weather Plugin: {e}"))
        
        agent = Agent(kernel, shopify_plugin, weather_plugin)
        print(Colors.green("Listo. Escribe 'salir' para terminar."))

        while True:
            try:
                u = input(f"{Colors.cyan('Tú >')} ")
                if u.lower() in ['exit', 'quit', 'salir']: break
                if u.strip(): await agent.run(u)
            except KeyboardInterrupt: break
    
    try: asyncio.run(main())
    except: pass
