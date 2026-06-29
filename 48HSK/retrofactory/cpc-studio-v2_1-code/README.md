# CPC Studio V2.1 Code

Proyecto modular para generar e integrar código de juegos Amstrad CPC 6128 con
CPCtelera. El **agente orquestador** (PM) recibe el prompt del usuario, lo
disecciona en tareas y las reparte a los agentes worker (developer, audio, qa).

Entry point del orquestador: `main.py` (FastAPI/uvicorn en el puerto `8000`,
expone `POST /chat`).

## Ejecutar en local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# define las variables de entorno (ver abajo) en un .env o en el shell
python main.py
```

---

## Variables de entorno

El orquestador resuelve el LLM en `scene_agent/orchestrator_agent.py::_build_llm`
con esta prioridad:

1. **Gateway LLM de AMP** (si hay binding o `AMP_LLM_URL`).
2. **Mistral directo** (si hay `MISTRAL_API_KEY`) — pensado para local.
3. Si no hay ninguno → error.

El **modelo** se toma de: `ORCHESTRATOR_MODEL` → `AMP_GENAI_MODEL` → `codestral-latest`
(se elimina un prefijo `PROVIDER/` si lo trae, p. ej. `MISTRAL/codestral-latest`).

### A) Desplegado DENTRO de AMP (camino gobernado)

No hay que poner la URL ni la key del LLM a mano: al **asociar un LLM Provider**
al agente, AMP inyecta el par del binding y el código lo autodetecta.

| Variable | Quién la pone | Para qué |
|---|---|---|
| `ORCHESTRATOR_MODEL` | **Tú**, en *Environment Variables* del agente | Modelo a pedir (ej. `codestral-latest`) |
| `<AGENTE>_<N>_URL` (ej. `CPC_STUDIO_PM_1_URL`) | AMP (binding del LLM Provider) | URL externa del gateway; el código la reescribe al servicio interno |
| `<AGENTE>_<N>_API_KEY` (ej. `CPC_STUDIO_PM_1_API_KEY`) | AMP (binding del LLM Provider) | Key del gateway (cabecera `API-Key`) |
| `AMP_AGENT_API_KEY` | AMP | Auth del agente / export OTEL |
| `AMP_OTEL_ENDPOINT` | AMP | A dónde exporta las trazas |

> El gateway enruta por `Host` y solo es accesible por su DNS interno, así que el
> código conserva el *context path* del binding, sustituye el host por el servicio
> interno y añade el sufijo `/v1` y las cabeceras `API-Key` + `Host`. Todo
> automático; tú solo defines `ORCHESTRATOR_MODEL` y asocias el provider.

### B) Fuera de AMP (local / Mistral directo)

Sin gateway: el orquestador llama directamente a la API de Mistral.

| Variable | Obligatoria | Default | Para qué |
|---|---|---|---|
| `MISTRAL_API_KEY` | sí (o `MISTRAL_ORCHESTRATOR_API_KEY`) | — | Key real de Mistral |
| `ORCHESTRATOR_MODEL` | no | `codestral-latest` | Modelo a pedir |
| `MISTRAL_BASE_URL` | no | `https://api.mistral.ai/v1` | Endpoint OpenAI-compatible |

`.env` mínimo para local:
```env
MISTRAL_API_KEY=sk-...
ORCHESTRATOR_MODEL=mistral-large-latest
```

### Overrides avanzados (opcionales)

Útiles para forzar valores o si cambia el entorno del cluster:

| Variable | Default | Para qué |
|---|---|---|
| `AMP_LLM_URL` + `AMP_LLM_API_KEY` | — | Fijar el gateway a mano (gana sobre la autodetección del binding) |
| `AMP_LLM_GATEWAY_AUTHORITY` | `gateway-default.openchoreo-data-plane:19080` | DNS/puerto interno del gateway |
| `AMP_LLM_GATEWAY_SCHEME` | `http` | Esquema hacia el gateway interno |
| `AMP_GENAI_MODEL` | — | Modelo alternativo si AMP lo inyecta (`PROVIDER/model`) |

---

## Audio Agent

El agente de audio (`scene_agent/audio_agent.py`) corre **en proceso** dentro del
pod del PM cuando `AUDIO_AGENT_URL` no está definida, o como servicio independiente
cuando sí lo está. Resuelve su LLM con la misma prioridad que el orquestador:

1. **Gateway LLM de AMP** (binding o `AMP_LLM_URL`).
2. **Mistral directo** (`MISTRAL_WORKER_API_KEY` / `MISTRAL_API_KEY`) — local.
3. Sin ninguno → error inmediato (ya no cuelga esperando a `192.168.1.175`).

El **modelo** se toma de: `AUDIO_MODEL` → `AMP_GENAI_MODEL` → `codestral-latest`.

### Variables de entorno del audio agent

#### Dentro de AMP

| Variable | Quién la pone | Para qué |
|---|---|---|
| `AUDIO_MODEL` | **Tú** | Modelo a pedir (ej. `codestral-latest`) |
| `<AGENTE>_<N>_URL` | AMP (binding LLM Provider) | URL externa; el código la reescribe al gateway interno |
| `<AGENTE>_<N>_API_KEY` | AMP (binding LLM Provider) | Key del gateway |

#### Fuera de AMP (local / Mistral directo)

| Variable | Obligatoria | Default | Para qué |
|---|---|---|---|
| `MISTRAL_API_KEY` (o `MISTRAL_WORKER_API_KEY`) | sí | — | Key real de Mistral |
| `AUDIO_MODEL` | no | `codestral-latest` | Modelo a pedir |
| `MISTRAL_BASE_URL` | no | `https://api.mistral.ai/v1` | Endpoint OpenAI-compatible |
| `AUDIO_TIMEOUT_SECONDS` | no | `180` | Timeout de la llamada al LLM |

### RAG del audio agent

El audio agent usa un RAG propio (`rag_index_audio.json`, ~129 chunks) construido
sobre `scene_agent/data/audio/`. Carga en caché automáticamente al arrancar.
Si `fastembed` no está instalado en el pod, el RAG se salta con un warning y el
agente continúa sin contexto de recuperación — **no es un error bloqueante**.

---

## Despliegue en Agent Manager (resumen)

| Campo | Valor |
|---|---|
| Build | **Docker** (imagen nativa; evita la emulación amd64→arm64) |
| Dockerfile Path | `/Dockerfile` |
| Repo / Branch | `rgranadosd/charlas` / `main` |
| Project Path | `48HSK/retrofactory/cpc-studio-v2_1-code` |
| Agent Type | Chat Agent (`POST /chat`) |
| Env var | `ORCHESTRATOR_MODEL=codestral-latest` |
| LLM Provider | asociado (o `AMP_LLM_URL` + `AMP_LLM_API_KEY`) |

> La instrumentación OTEL la trae la propia app (`otel/sitecustomize.py`); en modo
> Docker no se añade el trait de auto-instrumentación de AMP.
