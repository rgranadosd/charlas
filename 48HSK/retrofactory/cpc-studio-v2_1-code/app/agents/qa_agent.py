import json

from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def run(
    user_request: str,
    orchestrator_output: dict | None = None,
    design_output: dict | None = None,
    art_output: dict | None = None,
    tech_output: dict | None = None,
    integration_output: dict | None = None,
    build_validation_output: dict | None = None,
    build_output: dict | None = None,
) -> dict:
    if isinstance(build_validation_output, dict):
        validation_status = str(build_validation_output.get("status", "fail")).strip().lower()
        if validation_status == "fail":
            issues = _as_list(build_validation_output.get("suspected_compile_errors"))
            fixes = _as_list(build_validation_output.get("fix_recommendations"))
            return {
                "status": "fail",
                "playability_checks": [
                    "{'check': 'pipeline_gate', 'description': 'QA no puede aprobar un build que ya ha fallado la validación estructural.', 'result': 'fail', 'details': 'build_validation devolvió status=fail y QA fue cortocircuitado para evitar falsos positivos.'}"
                ],
                "missing_gameplay_elements": issues,
                "usability_issues": issues,
                "next_iteration_goals": fixes,
            }

    blocks = []
    if orchestrator_output:
        blocks.append("Orchestrator JSON:\n" + json.dumps(orchestrator_output, ensure_ascii=False, indent=2))
    if design_output:
        blocks.append("Design JSON:\n" + json.dumps(design_output, ensure_ascii=False, indent=2))
    if art_output:
        blocks.append("Art JSON:\n" + json.dumps(art_output, ensure_ascii=False, indent=2))
    if tech_output:
        blocks.append("Tech JSON:\n" + json.dumps(tech_output, ensure_ascii=False, indent=2))
    if integration_output:
        blocks.append("Integration JSON:\n" + json.dumps(integration_output, ensure_ascii=False, indent=2))
    if build_validation_output:
        blocks.append("Build validation JSON:\n" + json.dumps(build_validation_output, ensure_ascii=False, indent=2))
    if build_output:
        blocks.append("Build output JSON:\n" + json.dumps(build_output, ensure_ascii=False, indent=2))

    payload = json_call("qa", user_request, "\n\n".join(blocks))
    status = str(payload.get("status", "fail")).strip().lower()
    if status not in {"pass", "fail"}:
        status = "fail"

    return {
        "status": status,
        "playability_checks": _as_list(payload.get("playability_checks")),
        "missing_gameplay_elements": _as_list(payload.get("missing_gameplay_elements")),
        "usability_issues": _as_list(payload.get("usability_issues")),
        "next_iteration_goals": _as_list(payload.get("next_iteration_goals")),
    }
