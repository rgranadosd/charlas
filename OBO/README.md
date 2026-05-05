# wso2-obo-file-exchange-poc

PoC didactica para explicar un flujo On-Behalf-Of con tres identidades distintas:

- usuario humano autenticado en una SPA React,
- agente autenticado con su propia identidad,
- token delegado OBO emitido tras consentimiento y token exchange.

La PoC esta preparada para trabajar contra WSO2 Identity Server 7.2 local como Authorization Server / Identity Provider. El frontend usa `@asgardeo/auth-react` por el ecosistema del ejemplo, pero todas las URLs y credenciales vienen de variables de entorno configurables y deben apuntar a tu instalacion local de IS.

## Objetivo

No es una demo de "pulsa y magia". El foco es mostrar de forma visible y ejecutable:

- `USER_TOKEN`
- `AGENT_TOKEN`
- `AUTHORIZATION_CODE`
- `OBO_TOKEN`
- `state`, `code_verifier`, `code_challenge`
- claims como `sub`, `act`, `scope`, `aud`, `exp`

## Modelo de identidad del agente

Este lab sigue el modelo de WSO2 IS 7.2 / Agent Identity / OBO y separa tres identidades que no deben confundirse:

- `AGENT_ID`: identidad logica del agente registrada en WSO2. Viene de configuracion y no se deduce del token.
- `client_id`: identidad tecnica del cliente OAuth autenticado con `AGENT_TOKEN`.
- `sub`: sujeto principal del token. En `AGENT_TOKEN` puede coincidir o no con el cliente OAuth, pero el lab no lo usa para redefinir `AGENT_ID`.
- `act.sub`: actor delegado dentro del `OBO_TOKEN`. Aqui es donde debe aparecer el agente que actua en nombre del usuario.

La regla de diseno del lab es explicita:

- no asumir `agent_id == client_id`
- no asumir `agent_id == sub`
- no asumir `client_id == sub`

Antes del OBO:

- `AGENT_ID` identifica logicamente al agente registrado.
- `AGENT_TOKEN` autentica tecnicamente al cliente OAuth del agente.
- el token puede traer `client_id` o `sub`, pero eso no sustituye al `AGENT_ID` logico.

Despues del OBO:

- `sub` identifica al usuario delegado.
- `act.sub` identifica al agente delegado.
- esa es la trazabilidad correcta para auditoria y autorizacion.

## Arquitectura

- `frontend/`: SPA React + TypeScript. Usa `@asgardeo/auth-react` para autenticar al usuario contra WSO2 IS 7.2 local y muestra un panel de control del protocolo.
- `backend/`: FastAPI. Obtiene el token del agente, genera y mantiene `state` y `code_verifier`, recibe el callback, intercambia el codigo y llama a la API protegida.
- `resource_api/`: FastAPI. Simula la API de ficheros, valida JWT con JWKS del IS y diferencia claramente entre token autonomo y token delegado.
- `docs/`: setup, arquitectura y diagrama de secuencia.

## Flujo didactico esperado

1. El usuario inicia sesion en la SPA.
2. La SPA sincroniza el `USER_TOKEN` con el backend para poblar el inspector.
3. El backend obtiene el `AGENT_TOKEN` desde WSO2 IS usando `client_credentials`.
4. Se intenta un acceso privado con `AGENT_TOKEN` y la API lo rechaza.
5. El backend inicia la delegacion OBO y genera `state`, `code_verifier`, `code_challenge` y `authorization_url`.
6. El usuario abre la pantalla de consentimiento y WSO2 IS redirige a `/api/obo/callback`.
7. El backend valida `state` y conserva el `AUTHORIZATION_CODE`.
8. El backend canjea `authorization_code + code_verifier + agent_token` contra el token endpoint real.
9. Si WSO2 IS emite el token delegado, la PoC expone `OBO_TOKEN` y sus claims.
10. La API protegida acepta la operacion con delegacion y lo explica en `token_analysis`.

## Estructura

```text
wso2-obo-file-exchange-poc/
  frontend/
  backend/
  resource_api/
  docs/
  docker-compose.yml
  README.md
```

## Arranque rapido local

1. Copia cada `.env.example` a su correspondiente `.env`.
2. Rellena con tus valores reales de WSO2 IS 7.2 local.
3. Arranca los servicios por separado o con Docker Compose.

### Script unico

Desde la raiz del proyecto puedes levantar todo con:

```bash
./start-obo-demo.sh
```

El script arranca:

- frontend en `http://localhost:8091`
- backend en `http://localhost:8000`
- resource API en `http://localhost:8001`

Y deja logs en `.run/`. Para parar todo, pulsa `Ctrl+C`.

### Opcion A: servicios locales

Frontend:

```bash
cd frontend
npm install
npm run dev
```

La SPA queda disponible en `http://localhost:8091`.

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Resource API:

```bash
cd resource_api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Opcion B: Docker Compose

```bash
cp backend/.env.example backend/.env
cp resource_api/.env.example resource_api/.env
cp frontend/.env.example frontend/.env
docker compose up
```

## Variables de entorno importantes

Frontend:

- `VITE_ASGARDEO_CLIENT_ID`
- `VITE_ASGARDEO_BASE_URL`
- `VITE_ASGARDEO_SIGN_IN_REDIRECT_URL`
- `VITE_ASGARDEO_SIGN_OUT_REDIRECT_URL`
- `VITE_ASGARDEO_SCOPE`
- `VITE_BACKEND_BASE_URL`

Si usas el puerto web `8091`, registra tambien `http://localhost:8091` como redirect URI permitido en tu aplicacion SPA de WSO2 IS / Asgardeo.

Backend:

- `WSO2_ISSUER`
- `WSO2_AUTHORIZE_ENDPOINT`
- `WSO2_TOKEN_ENDPOINT`
- `WSO2_INTROSPECTION_ENDPOINT`
- `WSO2_JWKS_ENDPOINT`
- `AGENT_ID`
- `AGENT_CLIENT_ID`
- `AGENT_CLIENT_SECRET`
- `INTROSPECTION_CLIENT_ID`
- `INTROSPECTION_CLIENT_SECRET`
- `OBO_CLIENT_ID`
- `OBO_CLIENT_SECRET`
- `OBO_REDIRECT_URI`
- `OBO_SCOPE`
- `OBO_AGENT_TOKEN_PARAMETER`
- `OBO_EXTRA_TOKEN_PARAMS_JSON`

Si en tu despliegue el mismo cliente OAuth se usa tanto para `AGENT_TOKEN` como para el exchange OBO, puedes poner el mismo valor en `AGENT_CLIENT_ID` y `OBO_CLIENT_ID`. El lab lo permite, pero ya no usa esa coincidencia para inferir la identidad logica del agente.

Resource API:

- `WSO2_INTROSPECTION_ENDPOINT`
- `INTROSPECTION_CLIENT_ID`
- `INTROSPECTION_CLIENT_SECRET`

La Resource API de este lab valida JWT por JWKS y, si WSO2 devuelve access tokens opacos, cae a introspeccion. Eso permite ejecutar el laboratorio con ambas estrategias de emision sin romper la explicacion del flujo.

## Configuracion verificada en este lab

Sobre la aplicacion OIDC del backend en WSO2 (`obo-demo-backend-agent`):

- el `accessToken.type` se ha dejado en `JWT` via Application Management API.
- con esa configuracion, `AGENT_TOKEN` y `OBO_TOKEN` salen como JWT firmados por WSO2 y el lab los valida por JWKS.
- aun asi, en este despliegue concreto de WSO2 el `OBO_TOKEN` emitido no esta incluyendo `act.sub`; por eso `delegated_agent_id` sigue en `null` aunque el token ya sea JWT y el usuario aparezca correctamente en `sub`.

En otras palabras:

- punto 1 resuelto: la Resource API acepta tokens opacos y JWT.
- punto 2 resuelto: la aplicacion de WSO2 ya emite JWT access tokens.
- limitacion restante del servidor: este tenant no esta emitiendo todavia el claim `act.sub` en el `OBO_TOKEN`.

Resource API:

- `WSO2_ISSUER`
- `WSO2_JWKS_ENDPOINT`
- `EXPECTED_AUDIENCE`

## Sobre WSO2 IS 7.2 y la ambiguedad del exchange OBO

El punto mas sensible del flujo es el intercambio final del codigo por el token delegado. La PoC deja esta logica aislada en `backend/app/services/oauth_service.py` y parametriza:

- grant type,
- nombre del parametro que transporta el token del agente,
- valor del tipo de token del actor,
- parametros extra JSON.

Si tu despliegue de WSO2 IS 7.2 usa un grant o nombres de parametros ligeramente distintos, toca solo ese servicio y deja intacta la UI, el store y la Resource API.

## Endpoints principales

Backend:

- `GET /api/health`
- `GET /api/session`
- `POST /api/session/user-token`
- `POST /api/agent-token`
- `POST /api/obo/start`
- `GET /api/obo/callback`
- `POST /api/obo/exchange`
- `GET /api/debug/artifacts`
- `POST /api/test/agent-access`
- `POST /api/test/obo-access`

Resource API:

- `GET /files/public`
- `GET /files/me`
- `POST /files/upload`
- `POST /files/{id}/share`

## Limitaciones

- Es una PoC orientada a explicacion tecnica, no una implementacion productiva.
- El frontend usa `@asgardeo/auth-react` porque lo pediste expresamente, aunque el propio paquete ya esta deprecado.
- La emision exacta de claims OBO en WSO2 IS puede variar segun tu configuracion. La UI mostrara `act` si existe, pero no inventa claims.
- El backend desactiva `verify=False` en las llamadas salientes para facilitar laboratorios locales con TLS self-signed. Para un entorno serio, sustituye eso por una CA valida.
