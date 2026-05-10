from app.schemas.outputs import NarrativeOutput
from app.services.llm_service import structured_call


def run(user_request: str) -> NarrativeOutput:
    return structured_call("narrative", NarrativeOutput, user_request)
