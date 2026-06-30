"""Agent contracts — the language between orchestrator and subagents.

Three contracts, three responsibilities:

  IntentSpec        ← orchestrator output    (WHAT + routing, no code)
  TechnicalTaskSpec ← technical subagent input  (concrete task in C/CPCtelera context)
  SubagentOutputSpec ← technical subagent output (result, status, code changes)

Designed for LangChain LCEL + JsonOutputParser:
  prompt | ChatOpenAI | JsonOutputParser() → dict → Model.model_validate(dict)
"""
from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------

class Risk(BaseModel):
    level: Literal["low", "medium", "high"]
    message: str


# ---------------------------------------------------------------------------
# IntentSpec — orchestrator output
# Chain: ChatPromptTemplate | ChatOpenAI | JsonOutputParser → IntentSpec
# Rule: NO code, NO HOW. Only WHAT, WHY, and WHO handles it.
# ---------------------------------------------------------------------------

class Intent(BaseModel):
    category: Literal["gameplay", "runtime", "hud", "assets", "build", "qa", "refactor", "unknown"]
    summary: str
    goal: str
    subgoals: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)

    @field_validator("subgoals", "constraints", "success_criteria", mode="before")
    @classmethod
    def _to_list(cls, v: Any) -> Any:
        return _coerce_to_list(v)


class Routing(BaseModel):
    mode: Literal["single", "sequential", "parallel"]
    reason: str


def _coerce_to_list(v: Any) -> list:
    """LLMs sometimes return a single string instead of a list — coerce gracefully."""
    if isinstance(v, str):
        return [v] if v else []
    return v


class TaskDef(BaseModel):
    task_id: str
    subagent: str = "technical_c_agent"
    title: str
    functional_instruction: str           # WHAT — abstract, no implementation detail
    depends_on: list[str] = Field(default_factory=list)
    priority: int = 1
    acceptance_checks: list[str] = Field(default_factory=list)
    input_context: list[str] = Field(default_factory=list)
    implementation_hint: str = ""
    # Semantic constraint the orchestrator sets when it knows the correct primitive:
    #   text/counter  → "use cpct_drawStringM0 — text, not a sprite"
    #   solid shape   → "use cpct_drawSolidBox — NOT for text"
    #   moving entity → "erase/draw pattern — no cpct_clearScreen in loop"
    #   floor rule    → "lower boundary = lose life + reset ball; distinct from block collision"
    #   block rule    → "block contact = bounce + destroy block; distinct from floor rule"
    #   HUD position  → "score at x=60,y=0  lives at x=40,y=0 (same top-right, different offsets)"

    @field_validator("input_context", "depends_on", "acceptance_checks", mode="before")
    @classmethod
    def _to_list(cls, v: Any) -> Any:
        # Coerce to list, then flatten any dict/non-str items to text — the
        # detail-rich PM sometimes returns structured items (e.g. {"rule": ...}).
        items = _coerce_to_list(v)
        out = []
        for it in items:
            if isinstance(it, dict):
                out.append("; ".join(f"{k}: {val}" for k, val in it.items()))
            elif isinstance(it, str):
                out.append(it)
            else:
                out.append(str(it))
        return out

    @field_validator("implementation_hint", "functional_instruction", "title", mode="before")
    @classmethod
    def _to_str(cls, v: Any) -> Any:
        # The PM sometimes returns a dict/list instead of a string (e.g.
        # implementation_hint as {"header_file": ...}). Flatten to text so the
        # worker still receives the guidance instead of failing validation.
        if v is None:
            return ""
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            return "; ".join(f"{k}: {val}" for k, val in v.items())
        if isinstance(v, list):
            return "; ".join(str(x) for x in v)
        return str(v)


class IntentSpec(BaseModel):
    """Orchestrator output: intent extraction + task routing. No code."""
    request_id: str
    project_name: str
    user_prompt: str
    intent: Intent
    routing: Routing
    tasks: list[TaskDef]
    risks: list[Risk] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# TechnicalTaskSpec — technical subagent input
# Built by orchestrator per task, sent to technical_c_agent.
# Contains all CPCtelera context the subagent needs to write real C code.
# ---------------------------------------------------------------------------

class TechnicalContext(BaseModel):
    language: str = "C"
    framework: str = "CPCtelera"
    target: str = "Amstrad CPC"
    project_root: str = "./"
    files: list[str] = Field(default_factory=list)
    current_state: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class FileChange(BaseModel):
    path: str
    action: Literal["create", "modify", "delete"]
    purpose: str


class ImplementationPlan(BaseModel):
    summary: str
    steps: list[str] = Field(default_factory=list)
    apis: list[str] = Field(default_factory=list)   # CPCtelera functions to use
    files_to_modify: list[FileChange] = Field(default_factory=list)


class CodeChange(BaseModel):
    path: str
    language: str = "c"
    content: str   # complete file content


class TechnicalTaskSpec(BaseModel):
    """Technical subagent input: concrete task in C/CPCtelera context."""
    task_id: str
    project_name: str
    functional_instruction: str
    technical_context: TechnicalContext
    implementation_plan: ImplementationPlan
    code_changes: list[CodeChange] = Field(default_factory=list)
    validation_expectations: list[str] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# SubagentOutputSpec — technical subagent output
# Returned by technical_c_agent after implementing a task.
# Consumed by the validator and builder.
# ---------------------------------------------------------------------------

class ValidationResult(BaseModel):
    passed: bool
    issues: list[str] = Field(default_factory=list)


class SubagentOutputSpec(BaseModel):
    """Technical subagent output: implementation result + status."""
    task_id: str
    status: Literal["ok", "needs_revision", "blocked"]
    summary: str
    files_changed: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)   # e.g. ["src/main.c"]
    notes: list[str] = Field(default_factory=list)
    validation: ValidationResult


# ---------------------------------------------------------------------------
# Development agent contracts (worker in planner/executor pattern)
# ---------------------------------------------------------------------------

class DevelopmentInput(BaseModel):
    """Input to the development worker. One task, fully specified."""
    task_id: str
    project_name: str
    goal: str
    context: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    target_files: list[str] = Field(default_factory=list)


class FilePatch(BaseModel):
    """A single file change produced by the development worker."""
    path: str
    content: str
    mode: Literal["write", "append", "patch"] = "write"


class DevelopmentOutput(BaseModel):
    """Structured output of the development worker. Ready to flush to disk."""
    task_id: str
    status: Literal["done", "blocked", "needs_clarification"]
    summary: str
    files_to_write: list[FilePatch] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    @field_validator("files_to_write", mode="before")
    @classmethod
    def _filter_patches(cls, v: Any) -> list:
        if not isinstance(v, list):
            return []
        return [item for item in v if isinstance(item, dict)]


# Backwards compat
DevelopmentTask = DevelopmentInput


# ---------------------------------------------------------------------------
# Backwards compat aliases (existing orchestrator.py references these)
# ---------------------------------------------------------------------------
OrchestratorContract = IntentSpec
TechnicalAgentContract = TechnicalTaskSpec
