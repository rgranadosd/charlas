from app.schemas.outputs import RouteDecision
from app.services.llm_service import build_model


def run(user_request: str) -> RouteDecision:
    llm = build_model().with_structured_output(RouteDecision)
    return llm.invoke([
        {"role": "system", "content": "Clasifica la petición en design_art_tech o narrative_design_art_tech."},
        {"role": "user", "content": user_request},
    ])
