"""Generic scene schemas — reusable for any CPC game genre."""
from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field


class PromptInput(BaseModel):
    text: str
    language: str = "es"


class Position(BaseModel):
    x: int | str = 0   # int (bytes) or named anchor: "left", "center", "right"
    y: int = 0          # pixel row


class Size(BaseModel):
    w: int = 1
    h: int = 1


class EntitySpec(BaseModel):
    id: str
    type: str                           # "paddle", "ball", "blocks_group", "text", "background", …
    layer: str                          # which layer owns this entity
    color: Optional[str] = None
    position: Optional[Position] = None
    size: Optional[Size] = None
    properties: dict = Field(default_factory=dict)
    visual_pen: int = 1                 # CPCtelera pen index used to draw this entity
    render_hint: str = "sprite"         # "sprite" | "solid_box" | "text"


class ControlSpec(BaseModel):
    entity_id: str
    action: str                         # "move_left", "move_right", "fire", …
    key: str                            # CPCtelera key constant
    axis: Optional[Literal["horizontal", "vertical"]] = None


class LayerSpec(BaseModel):
    name: str
    order: int                          # draw order: 0 = bottom
    entities: list[str] = Field(default_factory=list)   # entity ids
    clear_on_frame: bool = True         # True = full-redraw strategy per frame


class SceneSpec(BaseModel):
    id: str
    title: str
    description: str
    video_mode: int = 0                 # CPCtelera video mode
    background_color: Optional[str] = None
    layers: list[LayerSpec]
    entities: list[EntitySpec]
    controls: list[ControlSpec] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    # Game mechanics
    lives: int = 0                      # 0 = not tracked; >0 = number of lives
    scoring: bool = False               # True = score increments on block hit


class RenderStep(BaseModel):
    layer: str
    entity_id: Optional[str] = None    # None = layer-wide op (clear, fill)
    operation: str                      # "clear", "fill_rect", "draw_sprite",
                                        # "draw_string", "draw_blocks"
    params: dict = Field(default_factory=dict)


class RenderPlan(BaseModel):
    scene_id: str
    strategy: Literal["full_redraw_per_frame"] = "full_redraw_per_frame"
    steps: list[RenderStep]
    notes: list[str] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    level: Literal["error", "warning", "info"]
    code: str
    message: str
    entity_id: Optional[str] = None


class ValidationReport(BaseModel):
    scene_id: str
    ok: bool
    issues: list[ValidationIssue] = Field(default_factory=list)


class ScenePatch(BaseModel):
    """A single atomic change to apply to a SceneSpec before code generation."""
    op: str                         # "update_entity" | "update_scene"
    entity_id: Optional[str] = None # for update_entity ops
    field: str = ""                 # field name to change
    value: object = None            # new value
    reason: str = ""                # why this patch is needed



class DeveloperContract(BaseModel):
    """Structured task handed from orchestrator to the programming subagent."""
    objective: str
    slice_name: str
    scene_spec: SceneSpec
    current_main_c: str = ""             # existing src/main.c (empty = generate from scratch)
    constraints: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    developer_notes: list[str] = Field(default_factory=list)


class ProgrammerOutput(BaseModel):
    """What the programming subagent returns to the orchestrator."""
    main_c: str                          # complete src/main.c content
    justification: str                   # what was implemented and why
    risks: list[str] = Field(default_factory=list)
    validation_status: str = "ok"        # "ok" | "needs_review" | "failed"


class AgentOutput(BaseModel):
    prompt: PromptInput
    scene_spec: SceneSpec
    render_plan: RenderPlan
    validation_report: ValidationReport
    artifacts: dict[str, str] = Field(default_factory=dict)  # name → file path
    simulation: dict = Field(default_factory=dict)
