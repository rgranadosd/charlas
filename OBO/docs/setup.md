# Setup

## Aviso

No se inventan valores concretos de tu tenant ni de tu despliegue. Sustituye todos los placeholders por los datos reales de tu WSO2 IS 7.2 local.

## 1. Aplicacion SPA

Registra una aplicacion tipo SPA para el frontend.

Necesitas recopilar al menos:

- `client_id`
- `base_url` del issuer para el SDK
- redirect URI de login: `http://localhost:8091`
- redirect URI de logout: `http://localhost:8091`
- scopes para login: `openid profile email`

Rellena:

```env
VITE_ASGARDEO_CLIENT_ID=<spa-client-id>
VITE_ASGARDEO_BASE_URL=https://<is-host>:9443
VITE_ASGARDEO_SIGN_IN_REDIRECT_URL=http://localhost:8091
VITE_ASGARDEO_SIGN_OUT_REDIRECT_URL=http://localhost:8091
VITE_ASGARDEO_SCOPE=openid profile email
```

## 2. Aplicacion backend / agente

Registra una aplicacion confidencial para el backend o para la identidad del agente.

Importante: para esta PoC no basta con crear solo la SPA. Necesitas como minimo:

- una aplicacion SPA para el login del usuario en el navegador,
- una aplicacion confidencial para `client_credentials` del agente y para el exchange OBO del backend.

Puedes reutilizar la misma aplicacion confidencial para `AGENT_TOKEN` y `OBO_TOKEN`, o separar ambas si tu despliegue lo prefiere.

Necesitas:

- `client_id`
- `client_secret`
- scopes del agente
- redirect URI del exchange OBO: `http://localhost:8000/api/obo/callback`

Rellena:

```env
AGENT_CLIENT_ID=<agent-client-id>
AGENT_CLIENT_SECRET=<agent-client-secret>
AGENT_SCOPE=openid profile files.read files.write files.share

OBO_CLIENT_ID=<obo-client-id>
OBO_CLIENT_SECRET=<obo-client-secret>
OBO_REDIRECT_URI=http://localhost:8000/api/obo/callback
OBO_SCOPE=openid profile email files.read files.write files.share
```

Si reutilizas la misma aplicacion confidencial para `AGENT_TOKEN` y para el exchange OBO, puedes poner el mismo `client_id` y `client_secret` en ambos bloques.

## 3. Endpoints del Authorization Server

Necesitas mapear estas URLs reales de tu IS local:

- issuer real del JWT (`WSO2_ISSUER`)
- authorize endpoint (`WSO2_AUTHORIZE_ENDPOINT`)
- token endpoint (`WSO2_TOKEN_ENDPOINT`)
- JWKS endpoint (`WSO2_JWKS_ENDPOINT`)

Ejemplo con placeholders:

```env
WSO2_ISSUER=https://<is-host>:9443/<issuer-or-token-issuer>
WSO2_AUTHORIZE_ENDPOINT=https://<is-host>:9443/oauth2/authorize
WSO2_TOKEN_ENDPOINT=https://<is-host>:9443/oauth2/token
WSO2_JWKS_ENDPOINT=https://<is-host>:9443/oauth2/jwks
```

## 4. Scopes sugeridos para la demo

La Resource API usa estas reglas:

- `GET /files/public`: abierto o analizable con token
- `GET /files/me`: requiere contexto de usuario
- `POST /files/upload`: requiere `files.write` y delegacion
- `POST /files/{id}/share`: requiere `files.share` y delegacion

Por eso conviene registrar scopes similares a:

- `files.read`
- `files.write`
- `files.share`

## 5. Validacion JWT en la Resource API

La Resource API necesita:

- `WSO2_ISSUER`
- `WSO2_JWKS_ENDPOINT`
- `EXPECTED_AUDIENCE` si tu AS emite `aud` y quieres verificarlo

```env
WSO2_ISSUER=https://<is-host>:9443/<issuer-or-token-issuer>
WSO2_JWKS_ENDPOINT=https://<is-host>:9443/oauth2/jwks
EXPECTED_AUDIENCE=<resource-api-audience-if-your-jwt-uses-aud>
```

## 6. Ajuste fino del exchange OBO

Si el token endpoint de tu WSO2 IS 7.2 requiere nombres de parametros distintos para el flujo OBO, ajusta este bloque en `backend/.env`:

```env
OBO_GRANT_TYPE=authorization_code
OBO_AGENT_TOKEN_PARAMETER=actor_token
OBO_AGENT_TOKEN_TYPE_PARAMETER=actor_token_type
OBO_AGENT_TOKEN_TYPE_VALUE=urn:ietf:params:oauth:token-type:access_token
OBO_EXTRA_TOKEN_PARAMS_JSON={}
```

Ese mapeo se consume en `backend/app/services/oauth_service.py`.

## 7. Verificacion recomendada

Antes de abrir la demo en el navegador, verifica:

1. El frontend puede hacer login contra el IS local.
2. `POST /api/agent-token` devuelve un token real de WSO2 IS.
3. `GET /health` del backend y de la Resource API responden correctamente.
4. La callback `http://localhost:8000/api/obo/callback` esta registrada en la app confidencial.
5. El JWKS endpoint devuelve claves con las que PyJWT puede validar los access tokens.
