import json

from app.services.resource_service import format_resources_for_prompt, format_sample_code_for_prompt


def build_agent_extra_context(
    agent_role: str,
    user_request: str,
    upstream_payloads: dict[str, dict] | None = None,
    retrieval_limit: int = 5,
) -> str:
    blocks: list[str] = []

    normalized_upstream = {
        key: value
        for key, value in (upstream_payloads or {}).items()
        if isinstance(value, dict) and value
    }
    if normalized_upstream:
        blocks.append(
            json.dumps(
                {"upstream_payloads": normalized_upstream},
                ensure_ascii=False,
                indent=2,
            )
        )

    if retrieval_limit > 0:
        resource_context = format_resources_for_prompt(agent_role, user_request, limit=retrieval_limit)
        if resource_context:
            blocks.append(resource_context)

        sample_code_context = format_sample_code_for_prompt(agent_role, user_request, limit=max(3, retrieval_limit))
        if sample_code_context:
            blocks.append(sample_code_context)

    return "\n\n".join(blocks)
