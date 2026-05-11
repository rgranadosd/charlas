import json

from app.services.llm_service import json_call


def _normalize_files(payload: dict, allowed_files: set[str]) -> dict[str, str]:
    raw_files = payload.get("files")
    if not isinstance(raw_files, dict):
        return {}

    normalized: dict[str, str] = {}
    for path, content in raw_files.items():
        if not isinstance(path, str):
            continue
        rel_path = path.strip().replace("\\", "/")
        if not rel_path.startswith("src/"):
            continue
        if allowed_files and rel_path not in allowed_files:
            continue
        normalized[rel_path] = str(content)

    return normalized


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    narrative_output: dict | None = None,
    design_output: dict | None = None,
    art_output: dict | None = None,
    tech_output: dict | None = None,
) -> dict:
    blocks = []
    if orchestrator_output:
        blocks.append("Orchestrator JSON:\n" + json.dumps(orchestrator_output, ensure_ascii=False, indent=2))
    if narrative_output:
        blocks.append("Narrative JSON:\n" + json.dumps(narrative_output, ensure_ascii=False, indent=2))
    if design_output:
        blocks.append("Design JSON:\n" + json.dumps(design_output, ensure_ascii=False, indent=2))
    if art_output:
        blocks.append("Art JSON:\n" + json.dumps(art_output, ensure_ascii=False, indent=2))
    if tech_output:
        blocks.append("Tech JSON:\n" + json.dumps(tech_output, ensure_ascii=False, indent=2))

    payload = json_call("code_integrator", user_request, "\n\n".join(blocks))

    scaffold = tech_output.get("scaffold", {}) if isinstance(tech_output, dict) else {}
    allowed_files = set(scaffold.get("allowed_files", [])) if isinstance(scaffold, dict) else set()

    return {
        "files": _normalize_files(payload, allowed_files),
    }
