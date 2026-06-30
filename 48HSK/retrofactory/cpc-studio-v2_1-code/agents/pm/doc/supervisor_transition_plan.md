# Plan de transición a supervisor v1.1

## Objetivo

Evolucionar desde el agente único estable hacia una arquitectura con supervisor y subagentes, siguiendo el patrón “from one agent to many”, pero sin perder simplicidad ni trazabilidad.

## Estrategia

La transición se hará en dos pasos:

1. introducir un supervisor mínimo,
2. extraer solo dos subagentes iniciales: `design` y `runtime`.

No se crearán todavía agentes independientes para assets o QA. Esas responsabilidades seguirán dentro del flujo principal hasta justificar su separación.

## Motivo de esta estrategia

- Mantener baja la complejidad inicial.
- Reutilizar el pipeline técnico ya validado.
- Separar primero “qué slice conviene hacer” de “cómo se ejecuta técnicamente”.
- Facilitar tests con mocks antes de ampliar el número de agentes.

## Arquitectura objetivo v1.1

```text
agent/
├── router.py
├── supervisor.py
├── schemas.py
├── settings.py
├── agents/
│   ├── design_agent.py
│   └── runtime_agent.py
├── services/
│   ├── pipeline_service.py
│   ├── supervisor_service.py
│   └── ...
```

## Roles

### Supervisor

Responsable de:

- recibir el objetivo,
- construir el contexto común,
- decidir qué subagente invocar,
- consolidar respuestas,
- mantener un único punto de salida estructurado.

### DesignAgent

Responsable de:

- traducir el goal a una slice,
- generar objetivo, entregables, criterios de aceptación y riesgos,
- devolver un contrato estructurado apto para implementación.

### RuntimeAgent

Responsable de:

- convertir la slice en ejecución técnica,
- reutilizar `pipeline_service` cuando aplique,
- gestionar validación, build y emulación,
- devolver resultados técnicos agregados.

## Contratos nuevos

### SupervisorRequest

```json
{
  "goal": "planifica una slice para el proyecto testproject",
  "project_name": "testproject",
  "context": {
    "workspace_root": "...",
    "cpctelera_root": "...",
    "project_root": "..."
  }
}
```

### SupervisorResponse

```json
{
  "status": "ok",
  "selected_agent": "design",
  "summary": "Slice propuesta correctamente",
  "subagent_results": [],
  "risks": [],
  "evaluation": {
    "ok": true,
    "reason": null
  }
}
```

### SubagentResponse

```json
{
  "agent": "design",
  "ok": true,
  "summary": "...",
  "artifacts": [],
  "risks": [],
  "evaluation": {
    "ok": true,
    "reason": null
  }
}
```

## Plan de implementación

### Paso A

Crear los nuevos schemas:

- `SupervisorRequest`
- `SupervisorResponse`
- `SubagentResponse`

### Paso B

Crear `supervisor.py` con una primera política mínima:

- si el goal pide planificar o definir slice -> `DesignAgent`,
- si el goal pide ejecutar, validar, compilar o emular -> `RuntimeAgent`.

### Paso C

Crear `design_agent.py` mockeado:

- recibe `SupervisorRequest`,
- llama a la lógica de planificación ya existente o a un mock,
- devuelve `SubagentResponse`.

### Paso D

Crear `runtime_agent.py`:

- recibe slice o contrato ya preparado,
- llama a `pipeline_service`,
- devuelve `SubagentResponse`.

### Paso E

Añadir tests del supervisor:

- routing a design,
- routing a runtime,
- consolidación de errores,
- respuesta estructurada consistente.

## Regla de diseño

El supervisor no debe reimplementar lógica de dominio. Debe decidir, delegar y consolidar. La lógica especializada debe vivir en los subagentes o servicios reutilizados.

## Criterio de aceptación de v1.1

La transición a supervisor se considera válida cuando:

- existe un `SupervisorRequest` y `SupervisorResponse` estables,
- el supervisor enruta correctamente entre `design` y `runtime`,
- `runtime_agent` reutiliza el pipeline actual sin duplicarlo,
- los tests del supervisor pasan,
- el comando principal sigue ofreciendo una única salida estructurada.
