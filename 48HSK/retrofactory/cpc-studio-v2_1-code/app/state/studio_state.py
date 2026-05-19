from typing import Optional, TypedDict

from app.schemas.outputs import (
    ArtOutput,
    BuildOutput,
    BuildValidationOutput,
    ComposeOutput,
    ContractValidationOutput,
    DesignOutput,
    IntegrationOutput,
    NarrativeOutput,
    OrchestratorOutput,
    QAOutput,
    TechOutputV2,
)


class StudioState(TypedDict, total=False):
    user_request: str
    target_platform: str
    framework: str
    workflow_plan: list[str]
    completed_steps: list[str]
    current_step: str
    agent_payloads: dict[str, dict]
    orchestrator: OrchestratorOutput
    narrative: NarrativeOutput
    design: DesignOutput
    art: ArtOutput
    tech: TechOutputV2
    contractvalidation: ContractValidationOutput
    contract_validation: ContractValidationOutput
    integration: IntegrationOutput
    build_output: BuildOutput
    build_validation: BuildValidationOutput
    qa: QAOutput
    final_payload: ComposeOutput
    final_output: str
    generated_project_path: Optional[str]
    mock_generated_project_path: Optional[str]
    mock_replay: dict[str, dict]
    strict_mocks: bool
