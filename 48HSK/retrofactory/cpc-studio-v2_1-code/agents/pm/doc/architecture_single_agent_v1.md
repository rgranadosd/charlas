# Arquitectura single-agent v1

## Objetivo

Esta versión estabiliza un agente único en Python para asistir en el desarrollo de un videojuego estilo Ghosts ’n Goblins para Amstrad CPC con CPCtelera. La meta de esta fase es tener un flujo verificable, con contratos explícitos, herramientas controladas y una frontera clara entre configuración, routing y ejecución.

## Principios

- Empezar con un agente único antes de separar en subagentes.
- Usar contratos JSON/Pydantic entre componentes.
- Priorizar tests, mocks y validación estructurada.
- Reutilizar el pipeline real de CPCtelera cuando ya esté estable.
- Evitar lógica de negocio en settings.

## Estructura actual

```text
agent/
├── router.py
├── schemas.py
├── settings.py
├── services/
│   ├── pipeline_service.py
│   ├── planning_service.py
│   ├── stub_generation_service.py
│   ├── stub_validation_service.py
│   ├── build_service.py
│   ├── emulator_service.py
│   └── inspection_service.py
└── tools/
    └── domain/
        ├── plan_game_slice.py
        ├── generate_stub_slice.py
        ├── validate_stub_slice.py
        ├── build_project.py
        └── run_emulator.py
```

## Responsabilidades

### settings.py

Contiene exclusivamente configuración cargada mediante `AppSettings`. Define rutas, roots del workspace y parámetros de ejecución. No debe importar servicios ni tools.

### router.py

Es la puerta de entrada del agente. Sus responsabilidades son:

- inferir el contexto mínimo del proyecto,
- pedir aclaración si falta contexto,
- invocar la inspección inicial,
- construir el contrato de planificación,
- delegar la ejecución del flujo principal a `pipeline_service`.

### pipeline_service.py

Contiene la ejecución secuencial del flujo principal:

1. planificar la slice,
2. generar stubs,
3. validar stubs,
4. compilar el proyecto,
5. lanzar el smoke test del emulador.

Devuelve un resultado agregado que luego el router transforma en `AgentResponse`.

### schemas.py

Define los contratos estructurados del sistema:

- contexto de proyecto,
- contratos por tool,
- resultados por tool,
- respuesta final del agente.

## Flujo actual

```text
Goal
  -> infer_project_context
  -> inspect_project_if_needed
  -> build_plan_contract
  -> run_slice_pipeline
      -> plan_game_slice
      -> generate_stub_slice
      -> validate_stub_slice
      -> build_project
      -> run_emulator
  -> AgentResponse
```

## Contratos principales

### Entrada lógica

```json
{
  "goal": "planifica una slice para el proyecto testproject"
}
```

### Salida final

```json
{
  "status": "ok",
  "step_type": "execute",
  "summary": "...",
  "actions": [],
  "tool_results": [],
  "risks": [],
  "next_questions": [],
  "evaluation": {
    "ok": true,
    "reason": null
  }
}
```

## Fortalezas de v1

- Pipeline completo funcionando con CPCtelera y Caprice32.
- Settings desacoplado de la lógica de negocio.
- Contratos Pydantic claros.
- Tests en verde.
- Punto de partida adecuado para supervisor + subagentes.

## Límites de v1

- El agente único concentra planificación y ejecución técnica.
- El router aún conoce demasiado del caso de uso principal.
- QA y assets no están separados como responsabilidades explícitas.
- La evolución a nuevas clases de tareas será costosa si no aparece un supervisor.

## Criterio de cierre de la fase

La fase single-agent v1 se considera cerrada cuando:

- el comando principal devuelve `status=ok` para un proyecto de ejemplo,
- el build genera artefactos CPCtelera válidos,
- el emulador arranca en smoke test,
- la suite de tests pasa.
