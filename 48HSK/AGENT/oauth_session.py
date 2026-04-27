"""OAuth session management shared by CLI and service modes."""

from __future__ import annotations

import base64
import http.server
import json
import secrets
import socketserver
import threading
import time
import traceback
import urllib.parse
import webbrowser
from io import StringIO
from typing import Optional

import requests

from config import TOKEN_CACHE_FILE, _auth_trace_enabled, get_debug_mode
from ui_console import Colors


class TokenStore:
    def __init__(self, path: str = TOKEN_CACHE_FILE, force_auth: bool = False):
        self.path = path
        self.force_auth = force_auth

    def load(self):
        if self.force_auth:
            return None
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception:
            return None

    def save(self, data):
        try:
            with open(self.path, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
        except Exception as exc:
            print(Colors.red(f"No se pudo guardar token: {exc}"))


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """Servidor mínimo para capturar el code de OAuth."""

    code = None
    state = None
    error = None
    error_description = None
    scopes = None
    access_token = None
    id_token_payload = None
    oauth_client = None
    user_permissions = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        OAuthCallbackHandler.error = None
        OAuthCallbackHandler.error_description = None

        if "code" in qs:
            OAuthCallbackHandler.code = qs.get("code", [None])[0]
            OAuthCallbackHandler.state = qs.get("state", [None])[0]

            code = OAuthCallbackHandler.code
            verifier = getattr(OAuthCallbackHandler, "code_verifier", None)

            if OAuthCallbackHandler.oauth_client and code and verifier:
                token_data = OAuthCallbackHandler.oauth_client._exchange_code_for_token(code, verifier)
                if token_data and token_data.get("access_token"):
                    payload = OAuthCallbackHandler.oauth_client._decode_token_payload(token_data["access_token"])
                    if get_debug_mode():
                        print(Colors.dark_green(f"[DEBUG] Access Token payload: {payload}"))

                    id_token_payload = {}
                    if "id_token" in token_data:
                        id_token_payload = OAuthCallbackHandler.oauth_client._decode_token_payload(token_data["id_token"])
                        if get_debug_mode():
                            print(Colors.dark_green(f"[DEBUG] ID Token payload: {json.dumps(id_token_payload, indent=2)}"))

                    scopes = payload.get("scope") or payload.get("scp") or payload.get("scopes") or ""
                    if not scopes and "scope" in token_data:
                        scopes = token_data["scope"]

                    id_scopes = id_token_payload.get("scope") or id_token_payload.get("scp") or id_token_payload.get("scopes") or ""

                    if get_debug_mode():
                        print(Colors.dark_green(f"[DEBUG] Scopes en token response: {token_data.get('scope', 'N/A')}"))
                        print(Colors.dark_green(f"[DEBUG] Scopes en access_token: {scopes}"))
                        print(Colors.dark_green(f"[DEBUG] Scopes en id_token: {id_scopes}"))
                        print(Colors.dark_green(f"[DEBUG] Usuario (sub): {id_token_payload.get('sub', 'N/A')}"))

                    OAuthCallbackHandler.scopes = scopes or id_scopes
                    OAuthCallbackHandler.access_token = token_data["access_token"]
                    OAuthCallbackHandler.id_token_payload = id_token_payload

                    if id_token_payload:
                        try:
                            import sys

                            old_stdout = sys.stdout
                            old_stderr = sys.stderr
                            sys.stdout = StringIO()
                            sys.stderr = StringIO()

                            user_permissions = OAuthCallbackHandler.oauth_client._check_user_permissions(id_token_payload)

                            sys.stdout = old_stdout
                            sys.stderr = old_stderr

                            OAuthCallbackHandler.user_permissions = user_permissions
                            if get_debug_mode() and user_permissions:
                                print(Colors.dark_green(f"[DEBUG] Permisos específicos: {user_permissions}"))
                        except Exception as exc:
                            try:
                                sys.stdout = old_stdout
                                sys.stderr = old_stderr
                            except Exception:
                                pass

                            if get_debug_mode():
                                print(Colors.red(f"[DEBUG] Error obteniendo permisos: {exc}"))
                            OAuthCallbackHandler.user_permissions = set()

                    if get_debug_mode():
                        print(Colors.dark_green(f"[DEBUG] Scopes finales extraídos: {OAuthCallbackHandler.scopes}"))

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            scopes_html = ""
            scopes_debug_info = ""

            if OAuthCallbackHandler.scopes:
                scopes_list = OAuthCallbackHandler.scopes.split() if isinstance(OAuthCallbackHandler.scopes, str) else OAuthCallbackHandler.scopes
                scopes_html = "<h3>Scopes OAuth:</h3><ul>"
                for scope in scopes_list:
                    scopes_html += f"<li><code>{scope}</code></li>"
                scopes_html += "</ul>"

                if hasattr(OAuthCallbackHandler, "user_permissions") and OAuthCallbackHandler.user_permissions:
                    scopes_html += "<h3>Permisos de Aplicación:</h3><ul>"
                    for permission in sorted(OAuthCallbackHandler.user_permissions):
                        scopes_html += f"<li><span style='color: green;'>OK</span> <strong>{permission}</strong></li>"
                    scopes_html += "</ul>"

                    can_view = "View Products" in OAuthCallbackHandler.user_permissions
                    can_update_prices = "Update Prices" in OAuthCallbackHandler.user_permissions
                    can_update_descriptions = "Update Descriptions" in OAuthCallbackHandler.user_permissions

                    if can_view and can_update_prices and can_update_descriptions:
                        scopes_html += "<h3 style='color: green;'>Funcionalidades del Agente Disponibles:</h3><ul>"
                        scopes_html += "<li>Ver productos del catálogo</li>"
                        scopes_html += "<li>Modificar precios de productos</li>"
                        scopes_html += "<li>Actualizar descripciones</li>"
                        scopes_html += "</ul>"
                    else:
                        scopes_html += "<h3 style='color: orange;'>Funcionalidades Limitadas:</h3><ul>"
                        if not can_view:
                            scopes_html += "<li style='color: red;'>NO puede ver productos</li>"
                        if not can_update_prices:
                            scopes_html += "<li style='color: red;'>NO puede modificar precios</li>"
                        if not can_update_descriptions:
                            scopes_html += "<li style='color: red;'>NO puede actualizar descripciones</li>"
                        scopes_html += "</ul>"
                else:
                    scopes_html += "<h3 style='color: red;'>Sin permisos de aplicación específicos</h3>"

                scopes_debug_info = f"<p><strong>Debug:</strong> Scopes raw = {OAuthCallbackHandler.scopes}</p>"

                if hasattr(OAuthCallbackHandler, "id_token_payload") and OAuthCallbackHandler.id_token_payload:
                    user_sub = OAuthCallbackHandler.id_token_payload.get("sub", "N/A")
                    scopes_debug_info += f"<p><strong>Usuario (sub):</strong> {user_sub}</p>"
                    scopes_debug_info += f"<p><strong>ID Token claims:</strong> {list(OAuthCallbackHandler.id_token_payload.keys())}</p>"
            else:
                scopes_html = "<h3>Scopes:</h3><p>No se pudieron extraer los scopes del token</p>"
                scopes_debug_info = f"<p><strong>Debug:</strong> OAuthCallbackHandler.scopes = {repr(OAuthCallbackHandler.scopes)}</p>"
                scopes_debug_info += f"<p><strong>Debug:</strong> access_token presente = {bool(OAuthCallbackHandler.access_token)}</p>"
                scopes_debug_info += f"<p><strong>Debug:</strong> id_token_payload presente = {bool(getattr(OAuthCallbackHandler, 'id_token_payload', None))}</p>"

            html = f"""
            <html>
            <head><title>Login Exitoso</title></head>
            <body style=\"font-family: Arial, sans-serif; text-align: center; padding: 50px;\">
                <h2 style=\"color: #28a745;\">Usuario Validado Correctamente</h2>
                <p>El código de autorización fue recibido exitosamente.</p>
                <p>Puedes volver a la terminal para continuar usando el agente.</p>
                {scopes_html}
                <hr>
                {scopes_debug_info}
                <small style=\"color: #666;\">State: {OAuthCallbackHandler.state or 'N/A'}</small>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            if get_debug_mode():
                print(Colors.green(f"Usuario validado - Code recibido, State: {OAuthCallbackHandler.state}"))
                if OAuthCallbackHandler.scopes:
                    print(Colors.green(f"Scopes: {OAuthCallbackHandler.scopes}"))
            elif _auth_trace_enabled():
                print(Colors.debug("Login completado. Vuelve a la terminal."))
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
                <h2 style="color: #dc3545;">Usuario NO Validado</h2>
                <p><strong>Error:</strong> {}</p>
                <p><strong>Descripción:</strong> {}</p>
                <hr>
                <p>Verifica tus credenciales e intenta de nuevo.</p>
            </body>
            </html>
            """.format(OAuthCallbackHandler.error, OAuthCallbackHandler.error_description)
            self.wfile.write(html.encode("utf-8"))
            print(Colors.red(f"Usuario NO validado - Error: {OAuthCallbackHandler.error} - {OAuthCallbackHandler.error_description}"))
        else:
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <head><title>Callback Inválido</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: #ffc107;">Callback Inválido</h2>
                <p>No se recibió código de autorización ni error.</p>
                <p>Parámetros recibidos: {}</p>
            </body>
            </html>
            """.format(list(qs.keys()))
            self.wfile.write(html.encode("utf-8"))
            print(Colors.red(f"Callback inválido - Parámetros: {list(qs.keys())}"))

    def log_message(self, format, *args):
        return


class OAuthClient:
    def __init__(self, force_auth: bool = False):
        import os

        self.auth_endpoint = os.getenv("WSO2_AUTH_ENDPOINT")
        self.token_endpoint = os.getenv("WSO2_TOKEN_ENDPOINT")
        self.client_id = os.getenv("WSO2_CONSUMER_KEY")
        self.client_secret = os.getenv("WSO2_CONSUMER_SECRET")
        self.redirect_uri = os.getenv("WSO2_REDIRECT_URI", "http://localhost:8000/callback")
        self.scopes = os.getenv("WSO2_SCOPES", "openid update_prices update_descriptions view_products offline_access")
        self.store = TokenStore(force_auth=force_auth)

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
        data = {"grant_type": "refresh_token", "refresh_token": tokens["refresh_token"]}
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.token_endpoint, data=data, headers=headers, verify=False)
        if response.status_code == 200:
            token = response.json()
            token["expires_at"] = self._now() + token.get("expires_in", 3600)
            token.setdefault("refresh_token", tokens.get("refresh_token"))
            self.store.save(token)
            return token
        return None

    def _start_callback_server(self):
        parsed = urllib.parse.urlparse(self.redirect_uri)
        port = parsed.port or 8000

        socketserver.TCPServer.allow_reuse_address = True

        try:
            server = socketserver.TCPServer(("", port), OAuthCallbackHandler)
        except OSError as exc:
            if getattr(exc, "errno", None) == 48:
                raise Exception(
                    f"El puerto {port} está en uso. Cierra instancias previas del agente o ejecuta start_agent.sh para liberar puertos."
                )
            raise

        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server

    def _stop_callback_server(self, server):
        try:
            server.shutdown()
            server.server_close()
        except Exception:
            pass

    def _print_redirect_uri_help(self):
        import os

        is_base = os.getenv("WSO2_IS_BASE", "https://localhost:9443").rstrip("/")
        wso2_federated_callback = f"{is_base}/commonauth"
        print(Colors.yellow("Si ves 'Error 400: redirect_uri_mismatch', revisa estas URIs exactas:"))
        print(Colors.yellow(f"  1) App OAuth en WSO2 (Authorization Code + PKCE): {self.redirect_uri}"))
        print(Colors.yellow(f"  2) OAuth Client en Google (federación con WSO2): {wso2_federated_callback}"))
        print(Colors.yellow("  3) Deben coincidir al 100% (schema, host, puerto, path y slash final)."))

    def _generate_pkce(self):
        import hashlib

        verifier = secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
        return verifier, challenge

    def _check_user_permissions(self, user_ref):
        """Verificar permisos del usuario autenticado (sin hardcodear roles)."""
        try:
            import os
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
                    keys = ["sub", "preferred_username", "username", "userName", "email", "upn"]
                    cands = []
                    for key in keys:
                        value = ref.get(key)
                        if value:
                            cands.append(str(value).strip())
                    return cands
                return [str(ref).strip()]

            def _get_user_by_id(scim_id):
                url = f"{wso2_base}/scim2/Users/{urllib.parse.quote(str(scim_id))}"
                response = requests.get(url, headers=headers, verify=False, timeout=3)
                if response.status_code == 200:
                    return response.json()
                return None

            def _search_user_by_username(username):
                filt = f'userName eq "{username}"'
                url = f"{wso2_base}/scim2/Users"
                response = requests.get(
                    url,
                    headers=headers,
                    params={"filter": filt, "startIndex": 1, "count": 1},
                    verify=False,
                    timeout=3,
                )
                if response.status_code == 200:
                    data = response.json()
                    resources = data.get("Resources", [])
                    if resources:
                        return resources[0]
                return None

            candidates = []
            for candidate in _as_candidates(user_ref):
                if candidate and candidate not in candidates:
                    candidates.append(candidate)

            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] Resolviendo usuario SCIM con candidatos: {candidates}"))

            user_data = None
            for candidate in candidates:
                user_data = _get_user_by_id(candidate)
                if user_data:
                    break
                user_data = _search_user_by_username(candidate)
                if user_data:
                    break

            if not user_data:
                if get_debug_mode():
                    print(Colors.red("[DEBUG] No se pudo resolver el usuario SCIM; permisos vacíos"))
                return set()

            memberships = []
            memberships.extend(user_data.get("groups", []) or [])
            memberships.extend(user_data.get("roles", []) or [])

            role_ids = []
            for membership in memberships:
                if isinstance(membership, dict):
                    role_id = membership.get("value") or membership.get("id")
                    if role_id and role_id not in role_ids:
                        role_ids.append(role_id)
                elif isinstance(membership, str):
                    if membership and membership not in role_ids:
                        role_ids.append(membership)

            if get_debug_mode():
                displays = [m.get("display") for m in memberships if isinstance(m, dict) and m.get("display")]
                print(Colors.cyan(f"[DEBUG] Roles/Groups detectados: {displays} (IDs: {role_ids})"))

            permissions = set()
            for role_id in role_ids:
                role_url = f"{wso2_base}/scim2/v2/Roles/{urllib.parse.quote(str(role_id))}"
                role_response = requests.get(role_url, headers=headers, verify=False, timeout=3)
                if role_response.status_code != 200:
                    if get_debug_mode():
                        print(Colors.red(f"[DEBUG] No se pudo obtener rol {role_id}: HTTP {role_response.status_code}"))
                    continue

                role_data = role_response.json()
                role_permissions = role_data.get("permissions", []) or []
                for permission in role_permissions:
                    if isinstance(permission, dict):
                        name = permission.get("display") or permission.get("value")
                        if name:
                            permissions.add(str(name))
                    elif isinstance(permission, str) and permission:
                        permissions.add(permission)

            return permissions
        except requests.exceptions.RequestException:
            if get_debug_mode():
                print(Colors.red("Error de red conectando a WSO2 Identity Server"))
            return set()
        except Exception as exc:
            if get_debug_mode():
                print(Colors.red(f"Error verificando permisos: {exc}"))
            return set()

    def _decode_token_payload(self, token):
        try:
            parts = token.split(".")
            if len(parts) != 3:
                if get_debug_mode():
                    print(Colors.cyan("[DEBUG] Token opaco (no JWT) - usando introspección si es necesario"))
                return {}

            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding

            decoded = base64.urlsafe_b64decode(payload)
            payload_json = json.loads(decoded)

            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] JWT payload decodificado: {json.dumps(payload_json, indent=2)}"))

            return payload_json
        except Exception as exc:
            if get_debug_mode():
                print(Colors.cyan(f"[DEBUG] Token no decodificable como JWT: {exc}"))
            return {}

    def _exchange_code_for_token(self, code, verifier):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": verifier,
        }
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(self.token_endpoint, data=data, headers=headers, verify=False)
            if response.status_code == 200:
                token = response.json()
                token["expires_at"] = self._now() + token.get("expires_in", 3600)

                if get_debug_mode():
                    print(Colors.cyan(f"[DEBUG] Token response completo: {json.dumps(token, indent=2)}"))
                    if "access_token" in token:
                        print(Colors.cyan(f"[DEBUG] Access token (primeros 100 chars): {token['access_token'][:100]}..."))
                        print(Colors.cyan(f"[DEBUG] Es JWT? {token['access_token'].count('.') == 2}"))

                return token
            if get_debug_mode():
                print(Colors.red(f"Error intercambiando token: {response.status_code} {response.text}"))
            return None
        except Exception as exc:
            if get_debug_mode():
                print(Colors.red(f"Exception intercambiando token: {exc}"))
            return None

    def _interactive_auth(self):
        verifier, challenge = self._generate_pkce()
        state = secrets.token_urlsafe(16)

        OAuthCallbackHandler.oauth_client = self
        OAuthCallbackHandler.code_verifier = verifier
        try:
            server = self._start_callback_server()
        except Exception as exc:
            print(Colors.red(str(exc)))
            return None

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "state": state,
            "prompt": "login",
        }
        url = f"{self.auth_endpoint}?{urllib.parse.urlencode(params)}"
        print(Colors.yellow("Abre este URL para autorizar (PKCE/OBO):"))
        print(url)
        self._print_redirect_uri_help()
        try:
            webbrowser.open(url)
        except Exception:
            pass

        if _auth_trace_enabled():
            print(Colors.debug(f"Esperando callback en {self.redirect_uri} ..."))
        for _ in range(300):
            if OAuthCallbackHandler.code:
                break
            time.sleep(1)
        self._stop_callback_server(server)

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

        if OAuthCallbackHandler.access_token:
            token = {
                "access_token": OAuthCallbackHandler.access_token,
                "expires_at": self._now() + 3600,
                "scope": OAuthCallbackHandler.scopes,
            }
            self.store.save(token)
            return token

        token = self._exchange_code_for_token(code, verifier)
        if token:
            access_token = token.get("access_token")
            if access_token:
                payload = self._decode_token_payload(access_token)
                token["scope"] = payload.get("scope", "")

            self.store.save(token)
            return token

        print(Colors.red("Error al intercambiar code por token"))
        return None

    def ensure_token(self):
        if get_debug_mode():
            print(Colors.cyan("[DEBUG] ensure_token() llamado"))

        tokens = self.store.load()
        if self._token_valid(tokens):
            if get_debug_mode():
                print(Colors.cyan("[DEBUG] Token válido encontrado en cache"))
            return tokens.get("access_token")

        if tokens and tokens.get("refresh_token"):
            if get_debug_mode():
                print(Colors.cyan("[DEBUG] Intentando refresh token"))
            refreshed = self._refresh(tokens)
            if refreshed and self._token_valid(refreshed):
                return refreshed.get("access_token")

        if get_debug_mode():
            print(Colors.cyan("[DEBUG] Necesita autenticación interactiva"))
        new_token = self._interactive_auth()
        return new_token.get("access_token") if new_token else None


__all__ = ["OAuthCallbackHandler", "OAuthClient", "TokenStore"]
