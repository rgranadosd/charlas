from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class AgentCard:
    name: str
    description: str
    skills: List[str]
    input_schema: str
    output_schema: str

    def to_dict(self) -> Dict:
        return asdict(self)


def build_local_agent_cards() -> list[dict]:
    cards = [
        AgentCard("orchestrator_agent", "Routes requests", ["routing", "delegation"], "user_request", "RouteDecision"),
        AgentCard("design_agent", "Creates gameplay specs", ["gameplay", "control feel"], "request+context", "DesignOutput"),
        AgentCard("art_agent", "Creates art budgets", ["sprites", "visual direction"], "request+context", "ArtOutput"),
        AgentCard("cpctelera_tech_agent", "Plans CPCtelera implementation", ["render", "performance"], "request+context", "TechOutput"),
        AgentCard("code_integrator_agent", "Creates project files", ["workspace", "integration"], "state", "IntegrationOutput"),
    ]
    return [c.to_dict() for c in cards]
