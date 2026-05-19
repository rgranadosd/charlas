from pydantic import BaseModel, Field


class AgentContract(BaseModel):
    mission: str
    limits: list[str] = Field(default_factory=list)
    expected_inputs: list[str] = Field(default_factory=list)
    structured_output: dict[str, str] = Field(default_factory=dict)
    handoff_notes: list[str] = Field(default_factory=list)


AGENT_CONTRACTS: dict[str, AgentContract] = {
    "orchestrator_agent": AgentContract(
        mission="Actuar como supervisor del pipeline y fijar el plan secuencial del vertical slice CPCtelera.",
        limits=[
            "No genera archivos.",
            "No compila ni valida build.",
            "No redefine el scaffold CPCtelera.",
        ],
        expected_inputs=["user_request"],
        structured_output={
            "game_concept": "str",
            "genre_hint": "str",
            "reference_games": "list[str]",
            "player_fantasy": "str",
            "must_have_features": "list[str]",
            "nice_to_have_features": "list[str]",
            "scope": "dict",
            "constraints": "dict",
        },
        handoff_notes=[
            "Entrega restricciones de alcance y plataforma a narrative/design/art/tech.",
            "El plan de ejecución del grafo se deriva de este payload supervisor.",
        ],
    ),
    "narrative_agent": AgentContract(
        mission="Definir marco ficcional, tono y vocabulario diegético compatible con CPC 6128.",
        limits=[
            "No define módulos técnicos ni rutas de archivos.",
            "No prescribe assets fuera del presupuesto del proyecto.",
        ],
        expected_inputs=["user_request", "orchestrator"],
        structured_output={
            "theme": "str",
            "tone": "str",
            "setting": "str",
            "player_role": "str",
            "goal_fiction": "str",
            "enemy_fantasy": "list[str]",
            "world_keywords": "list[str]",
            "hud_text_style": "str",
        },
        handoff_notes=[
            "Entrega semántica y tono a design/art/tech.",
        ],
    ),
    "design_agent": AgentContract(
        mission="Definir bucle jugable, estados, objetivos y progresión compatible con el alcance CPCtelera.",
        limits=[
            "No decide estructura física de archivos.",
            "No genera código ni assets finales.",
        ],
        expected_inputs=["user_request", "orchestrator", "narrative"],
        structured_output={
            "core_loop": "str",
            "win_condition": "str",
            "lose_condition": "str",
            "player_actions": "list[str]",
            "game_states": "list[str]",
            "enemy_roles": "list[str]",
            "level_flow": "list[str]",
            "difficulty_curve": "str",
            "score_model": "str",
            "lives_model": "str",
        },
        handoff_notes=[
            "Entrega reglas y flujo a art, tech y qa.",
        ],
    ),
    "art_agent": AgentContract(
        mission="Definir modo gráfico, paleta y plan de assets compatible con CPC y CPCtelera.",
        limits=[
            "No escribe ficheros.",
            "No decide build ni scaffold.",
        ],
        expected_inputs=["user_request", "orchestrator", "narrative", "design"],
        structured_output={
            "video_mode_recommendation": "str",
            "palette_strategy": "str",
            "tileset_plan": "list[str]",
            "sprite_plan": "list[str]",
            "hud_plan": "list[str]",
            "asset_list": "list[str]",
            "conversion_hints": "list[str]",
        },
        handoff_notes=[
            "Entrega constraints visuales y lista de assets a tech e integrator.",
        ],
    ),
    "cpctelera_tech_agent": AgentContract(
        mission="Traducir diseño y arte a arquitectura técnica, contratos de módulos y scaffold escribible.",
        limits=[
            "No materializa archivos en disco.",
            "No compila.",
            "Debe mantener compatibilidad con scaffold real de CPCtelera.",
        ],
        expected_inputs=["user_request", "orchestrator", "narrative", "design", "art"],
        structured_output={
            "archetype": "str",
            "video_mode": "str",
            "modules": "list[str]",
            "scaffold": "dict",
            "runtime_contract": "dict",
            "module_contracts": "list[dict]",
            "asset_contract": "dict",
            "integration_blueprint": "dict",
        },
        handoff_notes=[
            "Entrega contrato de scaffold y ownership de módulos a code_integrator.",
            "Entrega metadata validable a contract_validation y qa.",
        ],
    ),
    "code_integrator_agent": AgentContract(
        mission="Generar únicamente el mapa de archivos permitidos que se escribirá dentro del scaffold CPCtelera.",
        limits=[
            "No escribe disco directamente.",
            "No puede emitir rutas fuera del scaffold permitido.",
            "No debe devolver narrativa libre.",
        ],
        expected_inputs=["user_request", "orchestrator", "narrative", "design", "art", "tech"],
        structured_output={
            "files": "dict[str, str]",
            "assumptions": "list[str]",
            "integration_notes": "list[str]",
            "manual_followups": "list[str]",
            "prebuild_validation_errors": "list[str]",
        },
        handoff_notes=[
            "Entrega payload de escritura a project_service.",
            "Entrega errores prebuild al nodo build.",
        ],
    ),
    "qa_agent": AgentContract(
        mission="Evaluar jugabilidad y consistencia final usando sólo payloads estructurados del pipeline.",
        limits=[
            "No puede aprobar si build_validation falla.",
            "No genera archivos ni altera el build.",
        ],
        expected_inputs=["user_request", "orchestrator", "design", "art", "tech", "integration", "build_validation", "build_output"],
        structured_output={
            "status": "pass|fail",
            "playability_checks": "list[str]",
            "missing_gameplay_elements": "list[str]",
            "usability_issues": "list[str]",
            "next_iteration_goals": "list[str]",
        },
        handoff_notes=[
            "Entrega evaluación final consumible por compose_node.",
        ],
    ),
    "build_validation_agent": AgentContract(
        mission="Validar de forma determinista scaffold, build, artifacts y archivos críticos del proyecto generado.",
        limits=[
            "No usa decisiones creativas ni altera archivos.",
            "No depende de texto libre de otros agentes.",
        ],
        expected_inputs=["project_path", "build_output"],
        structured_output={
            "status": "pass|fail",
            "scaffold_valid": "bool",
            "build_succeeded": "bool",
            "project_path": "str",
            "expected_artifacts": "list[str]",
            "found_artifacts": "list[str]",
            "missing_files": "list[str]",
            "invalid_paths": "list[str]",
            "header_source_mismatches": "list[str]",
            "suspected_compile_errors": "list[str]",
            "fix_recommendations": "list[str]",
            "validation_notes": "list[str]",
        },
        handoff_notes=[
            "Entrega validación estructurada a qa y compose_node.",
        ],
    ),
}
