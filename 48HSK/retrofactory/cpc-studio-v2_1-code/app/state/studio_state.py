from typing import Optional, TypedDict
from app.schemas.outputs import NarrativeOutput, DesignOutput, ArtOutput, TechOutput, QAOutput, IntegrationOutput, BuildValidationOutput, BuildOutput

class StudioState(TypedDict, total=False):
    user_request: str
    route: str
    target_platform: str
    framework: str
    narrative: NarrativeOutput
    design: DesignOutput
    art: ArtOutput
    tech: TechOutput
    qa: QAOutput
    integration: IntegrationOutput
    build_validation: BuildValidationOutput
    build_output: BuildOutput
    final_output: str
    generated_project_path: Optional[str]
