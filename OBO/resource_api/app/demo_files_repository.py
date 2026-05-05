from __future__ import annotations

import json
import logging
import mimetypes
from copy import deepcopy
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.config import settings


logger = logging.getLogger(__name__)


class DemoFilesUnavailableError(RuntimeError):
    pass


class InMemoryFileRepository:
    def __init__(self, json_path: Path) -> None:
        self.json_path = json_path
        self.active = False
        self.version: str | None = None
        self.error: str | None = None
        self._files_by_owner: dict[str, list[dict[str, Any]]] = {}
        self._labels_by_owner: dict[str, str] = {}
        self._owner_aliases: dict[str, str] = {}

    @classmethod
    def disabled(cls, json_path: Path, reason: str) -> "InMemoryFileRepository":
        instance = cls(json_path)
        instance.error = reason
        return instance

    def load(self) -> None:
        self.active = False
        self.version = None
        self.error = None
        self._files_by_owner = {}
        self._labels_by_owner = {}
        self._owner_aliases = {}

        if not self.json_path.exists():
            self.error = f"Seed JSON not found: {self.json_path}"
            logger.warning(self.error)
            return

        try:
            payload = json.loads(self.json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.error = f"Unable to parse demo files JSON: {exc}"
            logger.exception("Failed to parse demo files JSON from %s", self.json_path)
            return

        try:
            self._load_payload(payload)
        except Exception as exc:
            self.error = f"Invalid demo files JSON structure: {exc}"
            logger.exception("Invalid demo files JSON structure in %s", self.json_path)
            self._files_by_owner = {}
            self._labels_by_owner = {}
            self._owner_aliases = {}
            return

        self.active = True
        logger.info(
            "Loaded demo file repository from %s with %s users and %s files",
            self.json_path,
            len(self._labels_by_owner),
            sum(len(items) for items in self._files_by_owner.values()),
        )

    def _load_payload(self, payload: Any) -> None:
        if not isinstance(payload, dict):
            raise ValueError("top-level JSON must be an object")

        self.version = str(payload.get("version") or "unknown")
        users = payload.get("users")
        if not isinstance(users, list):
            raise ValueError("users must be a list")

        for user in users:
            if not isinstance(user, dict):
                raise ValueError("each user entry must be an object")

            label = self._require_string(user, "label")
            owner_sub = self._require_string(user, "owner_sub")
            owner_sub_aliases = self._normalize_aliases(user.get("owner_sub_aliases"), owner_sub)
            files = user.get("files")
            if not isinstance(files, list):
                raise ValueError(f"files must be a list for owner_sub={owner_sub}")
            for subject in owner_sub_aliases:
                if subject in self._files_by_owner:
                    raise ValueError(f"duplicate owner_sub alias: {subject}")

            normalized_files = [
                self._normalize_file_entry(label=label, owner_sub=owner_sub, file_entry=file_entry)
                for file_entry in files
            ]
            for subject in owner_sub_aliases:
                self._labels_by_owner[subject] = label
                self._files_by_owner[subject] = deepcopy(normalized_files)
                self._owner_aliases[subject] = owner_sub

    def _normalize_file_entry(
        self,
        *,
        label: str,
        owner_sub: str,
        file_entry: Any,
    ) -> dict[str, Any]:
        if not isinstance(file_entry, dict):
            raise ValueError(f"file entry must be an object for owner_sub={owner_sub}")

        file_id = self._require_string(file_entry, "id")
        filename = self._require_string(file_entry, "filename")
        content_type = self._require_string(file_entry, "content_type")
        storage_path = self._require_string(file_entry, "storage_path")
        created_at = self._require_string(file_entry, "created_at")
        size_bytes = file_entry.get("size_bytes")
        if not isinstance(size_bytes, int):
            raise ValueError(f"size_bytes must be an integer for file id={file_id}")

        return {
            "id": file_id,
            "filename": filename,
            "name": filename,
            "content_type": content_type,
            "size_bytes": size_bytes,
            "storage_path": storage_path,
            "created_at": created_at,
            "owner_sub": owner_sub,
            "owner": owner_sub,
            "owner_label": label,
            "classification": "private",
            "shared_with": list(file_entry.get("shared_with", [])),
        }

    @staticmethod
    def _require_string(payload: dict[str, Any], field_name: str) -> str:
        value = payload.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value

    @staticmethod
    def _normalize_aliases(raw_aliases: Any, owner_sub: str) -> list[str]:
        aliases = [owner_sub]
        if raw_aliases is None:
            return aliases
        if not isinstance(raw_aliases, list):
            raise ValueError(f"owner_sub_aliases must be a list for owner_sub={owner_sub}")
        for alias in raw_aliases:
            if not isinstance(alias, str) or not alias.strip():
                raise ValueError(f"owner_sub_aliases contains an invalid value for owner_sub={owner_sub}")
            cleaned = alias.strip()
            if cleaned not in aliases:
                aliases.append(cleaned)
        return aliases

    def list_files_for_user(self, owner_sub: str) -> list[dict[str, Any]]:
        return deepcopy(self._files_by_owner.get(owner_sub, []))

    def has_seeded_user(self, owner_sub: str) -> bool:
        return owner_sub in self._files_by_owner

    def _ensure_active(self) -> None:
        if not self.active:
            raise DemoFilesUnavailableError(self.error or "Demo repository is inactive")

    def upload_file_for_user(self, owner_sub: str, file_name: str) -> dict[str, Any]:
        self._ensure_active()
        collection = self._files_by_owner.setdefault(owner_sub, [])
        if owner_sub not in self._labels_by_owner:
            self._labels_by_owner[owner_sub] = "runtime-user"
        file_id = f"usr-{len(collection) + 1}"
        content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
        created = {
            "id": file_id,
            "filename": file_name,
            "name": file_name,
            "content_type": content_type,
            "size_bytes": 0,
            "storage_path": f"in-memory://uploads/{owner_sub}/{file_name}",
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "owner_sub": owner_sub,
            "owner": owner_sub,
            "owner_label": self._labels_by_owner[owner_sub],
            "classification": "private",
            "shared_with": [],
        }
        collection.append(created)
        return deepcopy(created)

    def share_file_for_user(self, owner_sub: str, file_id: str, target: str) -> dict[str, Any]:
        self._ensure_active()
        collection = self._files_by_owner.setdefault(owner_sub, [])
        for item in collection:
            if item["id"] == file_id:
                item.setdefault("shared_with", []).append(target)
                return deepcopy(item)
        raise KeyError(file_id)

    def get_debug_state(self) -> dict[str, Any]:
        owner_subs = sorted(self._files_by_owner)
        return {
            "active": self.active,
            "json_path": str(self.json_path),
            "version": self.version,
            "seed_users": len(self._labels_by_owner),
            "total_files": sum(len(items) for items in self._files_by_owner.values()),
            "owner_subs": owner_subs,
            "canonical_owner_subs": sorted(set(self._owner_aliases.values())),
            "error": self.error,
        }


@lru_cache
def get_demo_file_repository() -> InMemoryFileRepository:
    if not settings.demo_files_enabled:
        return InMemoryFileRepository.disabled(
            settings.demo_files_json_path,
            "Demo repository disabled because APP_ENV is not local/dev or USE_IN_MEMORY_DEMO_FILES is false",
        )

    repository = InMemoryFileRepository(settings.demo_files_json_path)
    repository.load()
    return repository