from __future__ import annotations

from typing import Any

from app.demo_files_repository import get_demo_file_repository

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

def list_public_files() -> list[dict[str, Any]]:
    return PUBLIC_FILES


def list_user_files(subject: str) -> list[dict[str, Any]]:
    repository = get_demo_file_repository()
    if not repository.active:
        return []
    return repository.list_files_for_user(subject)


def upload_user_file(subject: str, file_name: str) -> dict[str, Any]:
    repository = get_demo_file_repository()
    return repository.upload_file_for_user(subject, file_name)


def share_user_file(subject: str, file_id: str, target: str) -> dict[str, Any]:
    repository = get_demo_file_repository()
    return repository.share_file_for_user(subject, file_id, target)


def demo_files_debug_state() -> dict[str, Any]:
    return get_demo_file_repository().get_debug_state()
