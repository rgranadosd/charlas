from pathlib import Path, PurePosixPath

from app.services.file_service import write_text


def _is_valid_cpctelera_scaffold(base: Path) -> bool:
    return (
        base.exists()
        and base.is_dir()
        and (base / "src").is_dir()
        and (base / "src" / "main.c").is_file()
        and (base / "cfg").is_dir()
        and (base / "cfg" / "build_config.mk").is_file()
        and (base / "Makefile").is_file()
    )


def _normalize_src_path(raw_path: str) -> str:
    if not isinstance(raw_path, str):
        raise ValueError("All file paths must be strings.")

    candidate = raw_path.strip().replace("\\", "/")
    if not candidate:
        raise ValueError("File path cannot be empty.")

    if "/../" in f"/{candidate}/" or candidate.startswith("../") or candidate.endswith("/.."):
        raise ValueError(f"Path traversal is not allowed: {raw_path}")

    path = PurePosixPath(candidate)
    if path.is_absolute():
        raise ValueError(f"Absolute paths are not allowed: {raw_path}")

    normalized = path.as_posix()
    if not normalized.startswith("src/"):
        raise ValueError(f"Only paths under src/ are allowed: {raw_path}")

    if normalized.endswith("/") or normalized == "src":
        raise ValueError(f"Expected a file path under src/, got: {raw_path}")

    return normalized


def _normalize_scaffold_list(values, field_name: str) -> set[str]:
    if values is None:
        return set()
    if not isinstance(values, list):
        raise ValueError(f"payload['scaffold']['{field_name}'] must be a list.")
    return {_normalize_src_path(value) for value in values}


def _normalize_write_contract(payload: dict) -> tuple[set[str], set[str], set[str]]:
    scaffold = payload.get("scaffold")
    if scaffold is None:
        scaffold = {
            "allowed_files": payload.get("allowed_files", []),
            "overwrite_files": payload.get("overwrite_files", []),
            "create_if_missing": payload.get("create_if_missing", []),
        }

    if not isinstance(scaffold, dict):
        raise ValueError("payload['scaffold'] must be a dictionary.")

    allowed_files = _normalize_scaffold_list(scaffold.get("allowed_files"), "allowed_files")
    overwrite_files = _normalize_scaffold_list(scaffold.get("overwrite_files"), "overwrite_files")
    create_if_missing = _normalize_scaffold_list(scaffold.get("create_if_missing"), "create_if_missing")

    if not allowed_files:
        raise ValueError("payload write contract must declare at least one allowed file.")
    if not overwrite_files.issubset(allowed_files):
        raise ValueError("'overwrite_files' must be a subset of 'allowed_files'.")
    if not create_if_missing.issubset(allowed_files):
        raise ValueError("'create_if_missing' must be a subset of 'allowed_files'.")

    return allowed_files, overwrite_files, create_if_missing


def _ensure_inside_project(base: Path, target: Path) -> None:
    base_resolved = base.resolve()
    target_resolved = target.resolve()
    if target_resolved != base_resolved and base_resolved not in target_resolved.parents:
        raise ValueError(f"Refusing to write outside project directory: {target}")


def generate_project(base_dir: str, payload: dict) -> str:
    base = Path(base_dir)
    if not base.exists() or not base.is_dir():
        raise FileNotFoundError(f"Project directory does not exist: {base}")
    if not _is_valid_cpctelera_scaffold(base):
        raise ValueError(f"Project directory is not a valid CPCtelera scaffold: {base}")

    if not isinstance(payload, dict):
        raise ValueError("payload must be a dictionary.")

    files = payload.get("files")
    if not isinstance(files, dict):
        raise ValueError("payload['files'] must be a dictionary of path -> content.")

    allowed_files, overwrite_files, create_if_missing = _normalize_write_contract(payload)

    normalized_files: dict[str, str] = {}
    for raw_path, raw_content in files.items():
        rel_path = _normalize_src_path(raw_path)

        if rel_path not in allowed_files:
            raise ValueError(f"File not allowed by scaffold: {rel_path}")

        target = base / rel_path
        if target.exists():
            if rel_path not in overwrite_files:
                raise ValueError(f"Overwrite not allowed by scaffold: {rel_path}")
        else:
            if rel_path not in create_if_missing:
                raise ValueError(f"Creation not allowed by scaffold: {rel_path}")

        if not isinstance(raw_content, str):
            raise ValueError(f"File content must be a string for path: {rel_path}")

        normalized_files[rel_path] = raw_content

    for rel_path, content in normalized_files.items():
        target = base / rel_path
        _ensure_inside_project(base, target)
        write_text(target, content)

    return str(base)


# Backward-compatible alias for legacy import names.
generateproject = generate_project
