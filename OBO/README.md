# WSO2 OBO File Exchange Lab

PoC didactica para explicar un flujo On-Behalf-Of (OBO) con tres identidades separadas:

- Usuario humano autenticado en la SPA (`USER_TOKEN`)
- Agente con identidad propia (`AGENT_TOKEN`)
- Token delegado emitido tras consentimiento (`OBO_TOKEN`)

El laboratorio esta pensado para WSO2 Identity Server 7.2 en local.

## Que incluye

- `frontend/`: React + TypeScript + Asgardeo Auth SDK
- `backend/`: FastAPI para orquestar state, PKCE, callback y exchange OBO
- `resource_api/`: FastAPI protegida para validar JWT/introspeccion y simular recursos
- `dev-data/`: datos de demo
- `docs/`: arquitectura, secuencia y setup detallado

## Requisitos

- Node.js 20+ (recomendado)
- Python 3.11+ (recomendado)
- npm
- WSO2 IS 7.2 accesible desde local

## Arranque rapido

Desde la raiz del proyecto:

```bash
./start-obo-demo.sh
```

Servicios esperados:

- Frontend: `http://localhost:8091`
- Backend: `http://localhost:8000`
- Resource API: `http://localhost:8001`

## Ejecucion manual

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Resource API

```bash
cd resource_api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## Variables de entorno clave

Configura los `.env` de cada modulo a partir de sus `.env.example`.

Frontend:

- `VITE_ASGARDEO_CLIENT_ID`
- `VITE_ASGARDEO_BASE_URL`
- `VITE_ASGARDEO_SIGN_IN_REDIRECT_URL`
- `VITE_ASGARDEO_SIGN_OUT_REDIRECT_URL`
- `VITE_ASGARDEO_SCOPE`
- `VITE_BACKEND_BASE_URL`

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

Resource API:

- `WSO2_ISSUER`
- `WSO2_JWKS_ENDPOINT`
- `WSO2_INTROSPECTION_ENDPOINT`
- `INTROSPECTION_CLIENT_ID`
- `INTROSPECTION_CLIENT_SECRET`
- `EXPECTED_AUDIENCE`

## Flujo OBO esperado

1. Login del usuario en la SPA.
2. Sincronizacion de `USER_TOKEN` al backend.
3. Backend obtiene `AGENT_TOKEN` con `client_credentials`.
4. El acceso privado con `AGENT_TOKEN` debe fallar (sin delegacion).
5. Inicio de delegacion OBO (state + PKCE + URL de consentimiento).
6. Callback con `authorization_code` y validacion de `state`.
7. Exchange final para obtener `OBO_TOKEN`.
8. Llamadas delegadas a Resource API con trazabilidad (`sub` y `act.sub`).

## Endpoints principales

Backend:

- `GET /api/health`
- `GET /api/session`
- `POST /api/session/user-token`
- `POST /api/agent-token`
- `POST /api/obo/start`
- `GET /api/obo/callback`
- `POST /api/obo/exchange`
- `POST /api/test/agent-access`
- `POST /api/test/obo-access`

Resource API:

- `GET /files/public`
- `GET /files/me`
- `POST /files/upload`
- `POST /files/{id}/share`

## Limpieza aplicada en este repo

Se eliminaron artefactos generados innecesarios del frontend y se ignoran para evitar ruido:

- `frontend/vite.config.js`
- `frontend/vite.config.d.ts`
- `frontend/*.tsbuildinfo`

## UI personalizada

La cabecera del dashboard incluye el logo actual de WSO2 servido desde el dominio oficial y mantiene contraste correcto en tema claro/oscuro.

## Documentacion adicional

- `docs/setup.md`
- `docs/architecture.md`
- `docs/sequence-flow.md`
- `docs/demo-files.md`
