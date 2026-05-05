from __future__ import annotations

from typing import Any

PUBLIC_FILES = [
    {
        "id": "pub-1",
        "name": "public-onboarding.pdf",
        "classification": "public",
        "owner": "system",
    },
    {
        "id": "pub-2",
        "name": "obo-protocol-cheatsheet.md",
        "classification": "public",
        "owner": "system",
    },
]

USER_FILES: dict[str, list[dict[str, Any]]] = {
    "demo-user": [
        {
            "id": "usr-1",
            "name": "quarterly-plan.docx",
            "classification": "private",
            "owner": "demo-user",
            "shared_with": [],
        }
    ]
}


def list_public_files() -> list[dict[str, Any]]:
    return PUBLIC_FILES


def list_user_files(subject: str) -> list[dict[str, Any]]:
    return USER_FILES.setdefault(subject, [])


def upload_user_file(subject: str, file_name: str) -> dict[str, Any]:
    collection = USER_FILES.setdefault(subject, [])
    new_file = {
        "id": f"usr-{len(collection) + 1}",
        "name": file_name,
        "classification": "private",
        "owner": subject,
        "shared_with": [],
    }
    collection.append(new_file)
    return new_file


def share_user_file(subject: str, file_id: str, target: str) -> dict[str, Any]:
    collection = USER_FILES.setdefault(subject, [])
    for item in collection:
        if item["id"] == file_id:
            item.setdefault("shared_with", []).append(target)
            return item
    raise KeyError(file_id)
