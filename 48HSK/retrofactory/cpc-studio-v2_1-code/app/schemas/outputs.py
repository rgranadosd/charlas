from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class RouteDecision(BaseModel):
    route: Literal["design_art_tech", "narrative_design_art_tech"]

class NarrativeOutput(BaseModel):
    premise: str
    tone: str
    characters: List[str]
    narrative_constraints: List[str]

class DesignOutput(BaseModel):
    quality_goal: str
    smoothness_strategy: str
    performance_risks: List[str]
    tradeoffs: List[str]
    gameplay_spec: str

class ArtOutput(BaseModel):
    quality_goal: str
    visual_direction: str
    sprite_budget: str
    animation_budget: str
    tradeoffs: List[str]
    art_spec: str

class TechOutput(BaseModel):
    smoothness_strategy: str
    render_strategy: str
    cpu_risks: List[str]
    memory_risks: List[str]
    build_plan: str
    tradeoffs: List[str]
    implementation_plan: str
    recommended_video_mode: Optional[str] = None

class QAOutput(BaseModel):
    control_check: str
    motion_check: str
    visual_check: str
    performance_check: str
    fixes: List[str]

class IntegrationOutput(BaseModel):
    files_to_create: List[str] = Field(default_factory=list)
    files_to_modify: List[str] = Field(default_factory=list)
    integration_notes: str

class BuildValidationOutput(BaseModel):
    expected_entrypoints: List[str]
    expected_headers: List[str]
    validation_notes: str

class BuildOutput(BaseModel):
    success: bool
    return_code: int
    stdout: str
    stderr: str
    artifacts: List[str] = Field(default_factory=list)
    build_notes: str
