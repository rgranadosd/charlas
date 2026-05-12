from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class OrchestratorScope(BaseModel):
    target: str = "vertical_slice"
    complexity: str = "small"


class OrchestratorConstraints(BaseModel):
    target_platform: str = "Amstrad CPC"
    engine: str = "CPCtelera"


class OrchestratorOutput(BaseModel):
    game_concept: str = ""
    genre_hint: str = ""
    reference_games: List[str] = Field(default_factory=list)
    player_fantasy: str = ""
    must_have_features: List[str] = Field(default_factory=list)
    nice_to_have_features: List[str] = Field(default_factory=list)
    scope: OrchestratorScope = Field(default_factory=OrchestratorScope)
    constraints: OrchestratorConstraints = Field(default_factory=OrchestratorConstraints)


class NarrativeOutput(BaseModel):
    theme: str = ""
    tone: str = ""
    setting: str = ""
    player_role: str = ""
    goal_fiction: str = ""
    enemy_fantasy: List[str] = Field(default_factory=list)
    world_keywords: List[str] = Field(default_factory=list)
    hud_text_style: str = ""


class DesignOutput(BaseModel):
    core_loop: str = ""
    win_condition: str = ""
    lose_condition: str = ""
    player_actions: List[str] = Field(default_factory=list)
    game_states: List[str] = Field(default_factory=list)
    enemy_roles: List[str] = Field(default_factory=list)
    level_flow: List[str] = Field(default_factory=list)
    difficulty_curve: str = ""
    score_model: str = ""
    lives_model: str = ""


class ArtOutput(BaseModel):
    video_mode_recommendation: str = ""
    palette_strategy: str = ""
    tileset_plan: List[str] = Field(default_factory=list)
    sprite_plan: List[str] = Field(default_factory=list)
    hud_plan: List[str] = Field(default_factory=list)
    asset_list: List[str] = Field(default_factory=list)
    conversion_hints: List[str] = Field(default_factory=list)


class TechScaffold(BaseModel):
    """Declares which source files are required, optional and writable."""

    required_files: List[str] = Field(default_factory=list)
    base_scaffold_files: List[str] = Field(default_factory=list)
    optional_files: List[str] = Field(default_factory=list)
    allowed_files: List[str] = Field(default_factory=list)
    overwrite_files: List[str] = Field(default_factory=list)
    create_if_missing: List[str] = Field(default_factory=list)


class ModuleContract(BaseModel):
    """Describes module-level includes, symbol contracts and dependencies."""

    module: str = ""
    header: str = ""
    local_includes: List[str] = Field(default_factory=list)
    declared_symbols: List[str] = Field(default_factory=list)
    defined_symbols: List[str] = Field(default_factory=list)
    # Legacy compatibility: previous payloads may still send exports only.
    exports: List[str] = Field(default_factory=list)
    required_symbols: List[str] = Field(default_factory=list)
    required_assets: List[str] = Field(default_factory=list)
    critical: bool = False
    integrated: bool = True
    allows_stub: bool = False


class AssetContract(BaseModel):
    """Lists required assets and whether they are declared and defined."""

    required_assets: List[str] = Field(default_factory=list)
    declared_assets: List[str] = Field(default_factory=list)
    defined_assets: List[str] = Field(default_factory=list)


class BuildContract(BaseModel):
    """Defines build-profile expectations before integration and compilation."""

    compile_profile: Literal["prototype", "vertical_slice", "playable_slice"] = "playable_slice"
    critical_modules: List[str] = Field(default_factory=list)
    integrated_modules: List[str] = Field(default_factory=list)
    required_entrypoints: List[str] = Field(
        default_factory=lambda: ["game_init", "game_update", "game_render"]
    )
    main_loop_file: str = "src/main.c"
    reject_empty_main_loop: bool = True


class TechOutput(BaseModel):
    """Technical architecture payload produced by the tech agent."""

    archetype: str = ""
    video_mode: str = "Mode 1"
    level_structure: str = ""
    camera: str = ""
    modules: List[str] = Field(default_factory=list)
    input_model: Dict[str, object] = Field(default_factory=dict)
    entity_model: Dict[str, object] = Field(default_factory=dict)
    collision_model: Dict[str, object] = Field(default_factory=dict)
    rendering_model: Dict[str, object] = Field(default_factory=dict)
    data_model: Dict[str, object] = Field(default_factory=dict)
    update_order: List[str] = Field(default_factory=list)
    scaffold: TechScaffold = Field(default_factory=TechScaffold)
    runtime_contract: BuildContract | None = None
    module_contracts: List[ModuleContract] = Field(default_factory=list)
    asset_contract: AssetContract | None = None
    integration_blueprint: Dict[str, object] = Field(default_factory=dict)


class TechOutputV2(TechOutput):
    """Backward-compatible alias while migrating callers to extended TechOutput."""


class IntegrationOutput(BaseModel):
    files: Dict[str, str] = Field(default_factory=dict)
    integration_notes: str = ""
    prebuild_validation_errors: List[str] = Field(default_factory=list)


class BuildOutput(BaseModel):
    success: bool = False
    return_code: int = -1
    stdout: str = ""
    stderr: str = ""
    artifacts: List[str] = Field(default_factory=list)
    build_notes: str = ""


class BuildValidationOutput(BaseModel):
    status: Literal["pass", "fail"] = "fail"
    missing_files: List[str] = Field(default_factory=list)
    invalid_paths: List[str] = Field(default_factory=list)
    header_source_mismatches: List[str] = Field(default_factory=list)
    suspected_compile_errors: List[str] = Field(default_factory=list)
    fix_recommendations: List[str] = Field(default_factory=list)


class QAOutput(BaseModel):
    status: Literal["pass", "fail"] = "fail"
    playability_checks: List[str] = Field(default_factory=list)
    missing_gameplay_elements: List[str] = Field(default_factory=list)
    usability_issues: List[str] = Field(default_factory=list)
    next_iteration_goals: List[str] = Field(default_factory=list)


class ContractValidationIssue(BaseModel):
    """Represents one concrete contract validation issue."""

    code: str = ""
    message: str = ""
    severity: Literal["error", "warning"] = "error"
    file: str = ""
    related_items: List[str] = Field(default_factory=list)
    symbol: str = ""
    asset: str = ""


class ContractValidationOutput(BaseModel):
    """Aggregates contract validation results for early pipeline gating."""

    status: Literal["pass", "fail"] = "fail"
    issues: List[ContractValidationIssue] = Field(default_factory=list)
    checks: Dict[str, bool] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    out_of_scaffold_files: List[str] = Field(default_factory=list)
    missing_includes: List[str] = Field(default_factory=list)
    missing_symbols: List[str] = Field(default_factory=list)
    duplicate_symbols: List[str] = Field(default_factory=list)
    missing_assets: List[str] = Field(default_factory=list)
    missing_required_files: List[str] = Field(default_factory=list)
    build_profile_issues: List[str] = Field(default_factory=list)
