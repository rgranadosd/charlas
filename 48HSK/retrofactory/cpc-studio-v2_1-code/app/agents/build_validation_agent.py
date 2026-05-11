import json
from pathlib import Path

from app.services.llm_service import json_call


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _build_output_dict(build_output) -> dict:
    if build_output is None:
        return {}
    if isinstance(build_output, dict):
        return build_output
    if hasattr(build_output, "model_dump"):
        return build_output.model_dump()
    return {}


def _project_snapshot(project_path: str | None) -> dict:
    if not project_path:
        return {"exists": False, "files": []}

    base = Path(project_path)
    if not base.exists():
        return {"exists": False, "files": []}

    files = []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(base)).replace("\\", "/")
        if rel.startswith("obj/"):
            continue
        files.append(rel)

    return {"exists": True, "files": files[:400]}


def run(user_request: str, project_path: str | None, build_output=None) -> dict:
    build_payload = _build_output_dict(build_output)
    snapshot = _project_snapshot(project_path)

    extra_context = "\n\n".join(
        [
            "Project snapshot JSON:\n" + json.dumps(snapshot, ensure_ascii=False, indent=2),
            "Build output JSON:\n" + json.dumps(build_payload, ensure_ascii=False, indent=2),
        ]
    )

    validation_request = user_request or "Validate generated CPCtelera project coherence."
    payload = json_call("build_validation", validation_request, extra_context)

    status = str(payload.get("status", "fail")).strip().lower()
    if status not in {"pass", "fail"}:
        status = "fail"

    return {
        "status": status,
        "missing_files": _as_list(payload.get("missing_files")),
        "invalid_paths": _as_list(payload.get("invalid_paths")),
        "header_source_mismatches": _as_list(payload.get("header_source_mismatches")),
        "suspected_compile_errors": _as_list(payload.get("suspected_compile_errors")),
        "fix_recommendations": _as_list(payload.get("fix_recommendations")),
    }
