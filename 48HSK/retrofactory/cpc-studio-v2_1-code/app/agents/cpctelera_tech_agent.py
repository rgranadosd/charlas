from app.schemas.outputs import TechOutput
from app.services.llm_service import structured_call
from app.services.resource_service import format_resources_for_prompt


def run(user_request: str, extra_context: str = "") -> TechOutput:
    resource_context = format_resources_for_prompt("cpctelera_tech_agent", user_request, limit=6)
    print("\n[cpctelera_tech_agent][retrieved_context]")
    print(resource_context)
    print("[/cpctelera_tech_agent][retrieved_context]\n")
    merged_context = "\n\n".join(x for x in [extra_context, resource_context] if x)
    return structured_call("cpctelera_tech", TechOutput, user_request, merged_context)
