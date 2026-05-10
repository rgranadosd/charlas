from app.schemas.outputs import ArtOutput
from app.services.llm_service import structured_call
from app.services.resource_service import format_resources_for_prompt


def run(user_request: str, extra_context: str = "") -> ArtOutput:
    resource_context = format_resources_for_prompt("graphics_agent", user_request, limit=5)
    print("\n[art_agent][retrieved_context]")
    print(resource_context)
    print("[/art_agent][retrieved_context]\n")
    merged_context = "\n\n".join(x for x in [extra_context, resource_context] if x)
    return structured_call("art", ArtOutput, user_request, merged_context)
