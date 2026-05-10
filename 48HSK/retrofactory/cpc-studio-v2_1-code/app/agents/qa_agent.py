from app.schemas.outputs import QAOutput
from app.services.llm_service import structured_call
from app.services.resource_service import format_resources_for_prompt


def run(user_request: str, extra_context: str = "") -> QAOutput:
    tech_context = format_resources_for_prompt("cpctelera_tech_agent", user_request, limit=3)
    graphics_context = format_resources_for_prompt("graphics_agent", user_request, limit=3)
    print("\n[qa_agent][retrieved_context]")
    print(tech_context)
    print(graphics_context)
    print("[/qa_agent][retrieved_context]\n")
    merged_context = "\n\n".join(
        x for x in [extra_context, tech_context, graphics_context] if x
    )
    return structured_call("qa", QAOutput, user_request, merged_context)
