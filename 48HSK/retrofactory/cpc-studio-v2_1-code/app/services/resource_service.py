import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
DATASET_PATH = BASE / "data" / "amstrad_cpc_resources.jsonl"

_PRIORITY_SCORE = {"high": 30, "normal": 20, "low": 10}

ROLE_RULES = {
    "cpctelera_tech_agent": {
        "allowed_categories": {"programming", "tooling", "examples"},
        "preferred_tech": {"cpctelera", "c", "z80", "sdcc", "macos"},
        "avoid_categories": set(),
    },
    "graphics_agent": {
        "allowed_categories": {"graphics", "examples", "tooling"},
        "preferred_tech": {"mode 0", "mode 1", "mode 2", "sprites", "pixel art"},
        "avoid_categories": {"music"},
    },
    "qa_agent": {
        "allowed_categories": {"programming", "graphics", "examples"},
        "preferred_tech": {"cpctelera", "z80", "mode 1", "sprites"},
        "avoid_categories": {"music"},
    },
}

_CACHE = None


def load_resources() -> list[dict]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    items = []
    if not DATASET_PATH.exists():
        _CACHE = items
        return items

    with DATASET_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))

    _CACHE = items
    return items


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def _tokens(text: str) -> list[str]:
    raw = _normalize(text).replace("/", " ").replace(",", " ").replace("(", " ").replace(")", " ")
    return [t for t in raw.split() if len(t) > 2]


def _score_resource(item: dict, agent_role: str, user_request: str) -> int:
    score = _PRIORITY_SCORE.get(item.get("ingestion_priority", "low"), 0)

    category = _normalize(item.get("category", ""))
    platform = _normalize(item.get("platform", ""))

    haystack = " ".join([
        item.get("title", ""),
        item.get("short_description", ""),
        item.get("notes_for_agents", ""),
        item.get("category", ""),
        item.get("sub_category", ""),
        item.get("platform", ""),
        " ".join(item.get("tech_stack", [])),
    ]).lower()

    rules = ROLE_RULES.get(agent_role, {})
    allowed = rules.get("allowed_categories", set())
    avoid = rules.get("avoid_categories", set())
    preferred_tech = rules.get("preferred_tech", set())

    if allowed and category in allowed:
        score += 10
    if avoid and category in avoid:
        score -= 15

    if "macos" in user_request.lower() and "macos" in platform:
        score += 8

    for tech in preferred_tech:
        if tech in haystack:
            score += 4

    for token in _tokens(user_request):
        if token in haystack:
            score += 2

    if item.get("resource_type") == "tool" and agent_role == "graphics_agent":
        score -= 4

    return score


def get_resources_for_agent(agent_role: str, user_request: str, limit: int = 5) -> list[dict]:
    resources = [
        item for item in load_resources()
        if item.get("target_agent_role") == agent_role
    ]

    ranked = sorted(
        resources,
        key=lambda item: _score_resource(item, agent_role, user_request),
        reverse=True,
    )
    return ranked[:limit]


def format_resources_for_prompt(agent_role: str, user_request: str, limit: int = 5) -> str:
    resources = get_resources_for_agent(agent_role, user_request, limit=limit)
    if not resources:
        return ""

    lines = [f"Retrieved knowledge for {agent_role}:"]
    for item in resources:
        lines.append(
            f"- [{item.get('ingestion_priority', 'low')}] "
            f"{item.get('title', 'Untitled')} "
            f"| category={item.get('category', '')}/{item.get('sub_category', '')} "
            f"| tech={', '.join(item.get('tech_stack', []))} "
            f"| notes={item.get('notes_for_agents', '')} "
            f"| url={item.get('url', '')}"
        )
    return "\n".join(lines)