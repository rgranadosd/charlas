from app.schemas.outputs import DesignOutput
from app.services.llm_service import structured_call
from app.services.resource_service import format_resources_for_prompt


def run(user_request: str, extra_context: str = "") -> DesignOutput:
    graphics_context = format_resources_for_prompt("graphics_agent", user_request, limit=3)
    examples_context = format_resources_for_prompt("example_code_agent", user_request, limit=3)
    print("\n[design_agent][retrieved_context]")
    print(graphics_context)
    print(examples_context)
    print("[/design_agent][retrieved_context]\n")
    merged_context = "\n\n".join(
        x for x in [extra_context, graphics_context, examples_context] if x
    )
    return structured_call("design", DesignOutput, user_request, merged_context)
