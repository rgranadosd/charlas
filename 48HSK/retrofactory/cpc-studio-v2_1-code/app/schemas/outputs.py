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
    allowed_files: List[str] = Field(default_factory=list)
    overwrite_files: List[str] = Field(default_factory=list)
    create_if_missing: List[str] = Field(default_factory=list)


class TechOutput(BaseModel):
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


class IntegrationOutput(BaseModel):
    files: Dict[str, str] = Field(default_factory=dict)
    integration_notes: str = ""


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
