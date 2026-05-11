from typing import Any, Optional, TypedDict

class StudioState(TypedDict, total=False):
    user_request: str
    target_platform: str
    framework: str
    orchestrator: dict[str, Any]
    narrative: dict[str, Any]
    design: dict[str, Any]
    art: dict[str, Any]
    tech: dict[str, Any]
    qa: dict[str, Any]
    integration: dict[str, Any]
    build_validation: dict[str, Any]
    build_output: dict[str, Any]
    final_output: str
    generated_project_path: Optional[str]
