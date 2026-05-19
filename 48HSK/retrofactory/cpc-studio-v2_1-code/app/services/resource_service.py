import hashlib
import json
import logging
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
DATASET_PATH = BASE / "data" / "amstrad_cpc_resources.jsonl"
LOCAL_DOCS_DIR = BASE / "data"
SAMPLES_DIR = BASE / "samples"

LOCAL_DOC_EXTENSIONS = {".md", ".json", ".jsonl", ".txt", ".pdf"}
LOCAL_DOC_EXCLUDE = set()
SAMPLE_CODE_EXTENSIONS = {".c", ".h", ".s", ".asm", ".md", ".txt", ".mk"}
SAMPLE_CODE_FILENAMES = {"makefile"}
SAMPLE_CODE_EXCLUDE_DIRS = {".git", ".vscode", "obj", "dsk", "exp", "music", "tools", "build", "dist", "__pycache__"}
SAMPLE_CODE_ROLE_ALLOWLIST = {
    "cpctelera_tech_agent",
    "code_integrator_agent",
    "design_agent",
    "art_agent",
    "qa_agent",
}

ANSI_YELLOW = "\033[33m"
ANSI_RESET = "\033[0m"

LOCAL_DOC_ROLE_ALLOWLIST = {
    "cpctelera_tech_agent",
    "graphics_agent",
    "qa_agent",
    "code_integrator_agent",
    "design_agent",
    "art_agent",
    "narrative_agent",
    "orchestrator_agent",
    "build_validation_agent",
}

MANDATORY_TECH_DOCS = {
    "cpctelera_tech_agent": [
        "data/Using Hardware on Amstrad CPC.pdf",
        "data/amstrad_cpc_hardware_reference.md",
        "data/motor_grafico.md",
        "data/tutorial_crear_video_juego.md",
    ],
    "code_integrator_agent": [
        "data/Using Hardware on Amstrad CPC.pdf",
        "data/amstrad_cpc_hardware_reference.md",
        "data/motor_grafico.md",
        "data/tutorial_crear_video_juego.md",
    ],
    "design_agent": [
        "data/amstrad_cpc_hardware_reference.md",
        "data/motor_grafico.md",
    ],
    "art_agent": [
        "data/motor_grafico.md",
        "data/amstrad_cpc_hardware_reference.md",
    ],
    "qa_agent": [
        "data/amstrad_cpc_hardware_reference.md",
        "data/tutorial_crear_video_juego.md",
    ],
}

_PRIORITY_SCORE = {"high": 30, "normal": 20, "low": 10}

ROLE_RULES = {
    "narrative_agent": {
        "allowed_categories": {"examples", "graphics", "programming"},
        "preferred_tech": {"amstrad", "cpc", "hud", "8 bit", "retro"},
        "avoid_categories": {"music"},
    },
    "design_agent": {
        "allowed_categories": {"programming", "examples", "graphics"},
        "preferred_tech": {"cpctelera", "c", "z80", "sprites", "tilemap", "mode 1"},
        "avoid_categories": {"music"},
    },
    "art_agent": {
        "allowed_categories": {"graphics", "examples", "tooling"},
        "preferred_tech": {"mode 0", "mode 1", "mode 2", "sprites", "tilemap", "palette"},
        "avoid_categories": {"music"},
    },
    "cpctelera_tech_agent": {
        "allowed_categories": {"programming", "tooling", "examples"},
        "preferred_tech": {"cpctelera", "c", "z80", "sdcc", "macos"},
        "avoid_categories": set(),
    },
    "code_integrator_agent": {
        "allowed_categories": {"programming", "tooling", "examples"},
        "preferred_tech": {"cpctelera", "c", "z80", "sdcc", "macos", "vram", "sprite", "input"},
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

RESOURCE_ROLE_ALIASES = {
    "art_agent": ["art_agent", "graphics_agent"],
    "code_integrator_agent": ["code_integrator_agent", "cpctelera_tech_agent"],
}

_RESOURCE_CACHE = None
_INDEX_CACHE = None
_EMBEDDING_CACHE = None
_SAMPLE_CODE_INDEX_CACHE = None
_PDF_IMPORT_WARNING_EMITTED = False


def _safe_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)).strip())
    except Exception:
        return default


def _safe_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)).strip())
    except Exception:
        return default


def _safe_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _localdoc_cfg() -> dict:
    provider = os.getenv("LOCALDOC_EMBED_PROVIDER", "openai_compat").strip().lower()
    if provider in {"openai", "mistral", "nvidia"}:
        provider = "openai_compat"

    chunk_size = max(200, _safe_int("LOCALDOC_CHUNK_SIZE", 1200))
    chunk_overlap = _safe_int("LOCALDOC_CHUNK_OVERLAP", 180)
    if chunk_overlap < 0:
        chunk_overlap = 0
    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size // 4)

    return {
        "provider": provider,
        "model": os.getenv("LOCALDOC_EMBED_MODEL", "text-embedding-3-small").strip(),
        "base_url": os.getenv("LOCALDOC_EMBED_BASE_URL", "").strip(),
        "api_key": os.getenv("LOCALDOC_EMBED_API_KEY", "").strip(),
        "batch_size": max(1, _safe_int("LOCALDOC_EMBED_BATCH_SIZE", 24)),
        "score_weight": max(0.0, _safe_float("LOCALDOC_EMBED_SCORE_WEIGHT", 20.0)),
        "index_dir": Path(os.getenv("LOCALDOC_INDEX_DIR", str(BASE / ".cache" / "localdoc_index"))).expanduser(),
        "force_reindex": _safe_bool("LOCALDOC_FORCE_REINDEX", False),
        "topk": max(1, _safe_int("LOCALDOC_TOPK", 5)),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "snippet_max_chars": max(120, _safe_int("LOCALDOC_SNIPPET_MAX_CHARS", 520)),
        "hashed_dim": max(64, _safe_int("LOCALDOC_HASHED_DIM", 256)),
    }


def _log(level: str, message: str) -> None:
    prefix = f"[{level}]"
    if level == "INFO":
        prefix = f"{ANSI_YELLOW}[INFO]{ANSI_RESET}"
    sys.stderr.write(f"{prefix} {message}\n")
    sys.stderr.flush()


def _activity_message(base: str, step: int) -> str:
    dots = "." * (3 + (step % 4))
    return f"{base}{dots}"


def load_resources() -> list[dict]:
    global _RESOURCE_CACHE
    if _RESOURCE_CACHE is not None:
        return _RESOURCE_CACHE

    items = []
    if not DATASET_PATH.exists():
        _RESOURCE_CACHE = items
        return items

    with DATASET_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))

    _RESOURCE_CACHE = items
    return items


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _tokens(text: str) -> list[str]:
    raw = _normalize(text).replace("/", " ").replace(",", " ").replace("(", " ").replace(")", " ")
    return [t for t in raw.split() if len(t) > 2]


def _stable_hash(value: str) -> int:
    digest = hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def _text_cache_key(value: str) -> str:
    return hashlib.blake2b(value.encode("utf-8"), digest_size=16).hexdigest()


def _embed_text_hashed(text: str, dim: int) -> list[float]:
    vec = [0.0] * dim
    for token in _tokens(text):
        idx = _stable_hash(token) % dim
        vec[idx] += 1.0

    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        inv = 1.0 / norm
        vec = [v * inv for v in vec]
    return vec


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    return sum(a * b for a, b in zip(vec_a, vec_b))


def _normalize_vector(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm <= 0:
        return []
    inv = 1.0 / norm
    return [v * inv for v in vec]


def _embed_texts_remote(texts: list[str], cfg: dict) -> list[list[float]]:
    if not texts:
        return []

    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError(f"openai client is not available: {exc}") from exc

    if not cfg.get("api_key"):
        raise RuntimeError("LOCALDOC_EMBED_API_KEY is empty for remote embedding provider")

    client_kwargs = {"api_key": cfg["api_key"]}
    if cfg.get("base_url"):
        client_kwargs["base_url"] = cfg["base_url"]

    client = OpenAI(**client_kwargs)

    vectors = [None] * len(texts)
    pending_texts = []
    pending_indices = []

    cache = _load_embedding_cache(cfg)
    for idx, text in enumerate(texts):
        key = _text_cache_key(text)
        cached = cache.get(key)
        if cached is not None:
            vectors[idx] = cached
            continue
        pending_texts.append(text)
        pending_indices.append(idx)

    if not pending_texts:
        return [item or [] for item in vectors]

    total = len(pending_texts)
    done = 0
    batch_size = cfg["batch_size"]
    for batch_i, start in enumerate(range(0, total, batch_size), start=1):
        end = min(start + batch_size, total)
        batch_texts = pending_texts[start:end]
        _log("EMBED", f"Generando embeddings: {end}/{total}")
        _log("INFO", _activity_message("Embeddings: generando vectores", batch_i))

        response = client.embeddings.create(model=cfg["model"], input=batch_texts)
        for offset, item in enumerate(response.data):
            vec = _normalize_vector(list(item.embedding or []))
            source_index = pending_indices[start + offset]
            vectors[source_index] = vec
            cache[_text_cache_key(batch_texts[offset])] = vec

        done = end

    _save_embedding_cache(cfg, cache)
    return [item or [] for item in vectors]


def _load_embedding_cache(cfg: dict) -> dict:
    global _EMBEDDING_CACHE
    if _EMBEDDING_CACHE is not None:
        return _EMBEDDING_CACHE

    cache_file = cfg["index_dir"] / "embed_cache.json"
    if cache_file.exists():
        try:
            _EMBEDDING_CACHE = json.loads(cache_file.read_text(encoding="utf-8"))
            return _EMBEDDING_CACHE
        except Exception:
            _EMBEDDING_CACHE = {}
            return _EMBEDDING_CACHE

    _EMBEDDING_CACHE = {}
    return _EMBEDDING_CACHE


def _save_embedding_cache(cfg: dict, cache: dict) -> None:
    cache_file = cfg["index_dir"] / "embed_cache.json"
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        _log("WARN", f"No se pudo persistir embed cache: {exc}")


def _pdf_parser_fingerprint() -> str:
    try:
        import pypdf
    except Exception:
        return "missing"

    return getattr(pypdf, "__version__", "present")


def _sample_code_cfg() -> dict:
    return {
        "index_dir": BASE / ".cache" / "sample_code_index",
        "chunk_lines": 80,
        "chunk_line_overlap": 16,
        "snippet_max_chars": 900,
    }


def _read_local_doc(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        try:
            payload = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
            return json.dumps(payload, ensure_ascii=False, indent=2)
        except Exception:
            return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".jsonl":
        items = []
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as file_obj:
                for line_number, line in enumerate(file_obj, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                        items.append(json.dumps(payload, ensure_ascii=False, indent=2))
                    except Exception:
                        items.append(f"[line {line_number}] {line}")
        except Exception:
            return ""
        return "\n\n".join(items)

    if suffix in {".md", ".txt"}:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1", errors="ignore")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except Exception:
            global _PDF_IMPORT_WARNING_EMITTED
            if not _PDF_IMPORT_WARNING_EMITTED:
                _log("WARN", f"PDF omitido porque falta pypdf en el entorno activo: {path.name}")
                _PDF_IMPORT_WARNING_EMITTED = True
            return ""

        logging.getLogger("pypdf").setLevel(logging.ERROR)
        logging.getLogger("pypdf._reader").setLevel(logging.ERROR)

        try:
            reader = PdfReader(str(path), strict=False)
        except Exception:
            return ""

        pages = []
        for page_index, page in enumerate(reader.pages):
            try:
                extracted = page.extract_text() or ""
            except Exception:
                extracted = ""
            extracted = _clean_text(extracted)
            if extracted:
                pages.append(f"[page {page_index + 1}] {extracted}")
        return "\n".join(pages)

    return ""


def _split_chunks(text: str, max_chars: int, overlap: int) -> list[str]:
    compact = _clean_text(text)
    if not compact:
        return []
    if len(compact) <= max_chars:
        return [compact]

    chunks = []
    start = 0
    while start < len(compact):
        end = min(start + max_chars, len(compact))

        if end < len(compact):
            break_at = compact.rfind(". ", start + (max_chars // 2), end)
            if break_at == -1:
                break_at = compact.rfind(" ", start + (max_chars // 2), end)
            if break_at > start:
                end = break_at + 1

        chunk = compact[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(compact):
            break

        next_start = max(0, end - overlap)
        if next_start <= start:
            next_start = end
        start = next_start

    return chunks


def _split_code_chunks(text: str, max_lines: int, overlap: int) -> list[dict]:
    lines = text.splitlines()
    if not lines:
        return []

    chunks: list[dict] = []
    start = 0
    total = len(lines)
    while start < total:
        end = min(start + max_lines, total)
        chunk_lines = lines[start:end]
        chunk_text = "\n".join(chunk_lines).strip()
        if chunk_text:
            chunks.append(
                {
                    "text": chunk_text,
                    "start_line": start + 1,
                    "end_line": end,
                }
            )

        if end >= total:
            break

        next_start = max(0, end - overlap)
        if next_start <= start:
            next_start = end
        start = next_start

    return chunks


def _discover_local_docs() -> list[Path]:
    if not LOCAL_DOCS_DIR.exists():
        return []

    documents: list[Path] = []
    for path in sorted(LOCAL_DOCS_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.name in LOCAL_DOC_EXCLUDE:
            continue
        if path.suffix.lower() not in LOCAL_DOC_EXTENSIONS:
            continue
        documents.append(path)
    return documents


def _discover_sample_code_files() -> list[Path]:
    if not SAMPLES_DIR.exists():
        return []

    files: list[Path] = []
    for path in sorted(SAMPLES_DIR.rglob("*")):
        if not path.is_file():
            continue

        rel_parts = path.relative_to(SAMPLES_DIR).parts[:-1]
        if any(part in SAMPLE_CODE_EXCLUDE_DIRS for part in rel_parts):
            continue

        suffix = path.suffix.lower()
        name = path.name.lower()
        if suffix not in SAMPLE_CODE_EXTENSIONS and name not in SAMPLE_CODE_FILENAMES:
            continue

        files.append(path)

    return files


def _document_signature(paths: list[Path], cfg: dict) -> str:
    signature_payload = {
        "chunk_size": cfg["chunk_size"],
        "chunk_overlap": cfg["chunk_overlap"],
        "extensions": sorted(LOCAL_DOC_EXTENSIONS),
        "excluded": sorted(LOCAL_DOC_EXCLUDE),
        "pdf_parser": _pdf_parser_fingerprint(),
        "files": [
            {
                "path": str(path.relative_to(BASE)).replace("\\", "/"),
                "size": path.stat().st_size,
                "mtime_ns": path.stat().st_mtime_ns,
            }
            for path in paths
        ],
    }
    raw = json.dumps(signature_payload, sort_keys=True, ensure_ascii=False)
    return hashlib.blake2b(raw.encode("utf-8"), digest_size=16).hexdigest()


def _sample_code_signature(paths: list[Path], cfg: dict) -> str:
    signature_payload = {
        "chunk_lines": cfg["chunk_lines"],
        "chunk_line_overlap": cfg["chunk_line_overlap"],
        "extensions": sorted(SAMPLE_CODE_EXTENSIONS),
        "filenames": sorted(SAMPLE_CODE_FILENAMES),
        "excluded_dirs": sorted(SAMPLE_CODE_EXCLUDE_DIRS),
        "files": [
            {
                "path": str(path.relative_to(BASE)).replace("\\", "/"),
                "size": path.stat().st_size,
                "mtime_ns": path.stat().st_mtime_ns,
            }
            for path in paths
        ],
    }
    raw = json.dumps(signature_payload, sort_keys=True, ensure_ascii=False)
    return hashlib.blake2b(raw.encode("utf-8"), digest_size=16).hexdigest()


def _index_paths(cfg: dict) -> tuple[Path, Path, Path]:
    index_dir = cfg["index_dir"]
    return (
        index_dir / "meta.json",
        index_dir / "chunks.jsonl",
        index_dir / "vectors.json",
    )


def _sample_index_paths(cfg: dict) -> tuple[Path, Path]:
    index_dir = cfg["index_dir"]
    return index_dir / "meta.json", index_dir / "chunks.jsonl"


def _load_index_from_disk(cfg: dict) -> dict | None:
    meta_path, chunks_path, vectors_path = _index_paths(cfg)
    if not (meta_path.exists() and chunks_path.exists() and vectors_path.exists()):
        return None

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        chunks = []
        with chunks_path.open("r", encoding="utf-8") as file_obj:
            for line in file_obj:
                line = line.strip()
                if not line:
                    continue
                chunks.append(json.loads(line))
        vectors = json.loads(vectors_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _log("WARN", f"Índice local corrupto; se reconstruirá. detalle={exc}")
        return None

    if len(chunks) != len(vectors):
        _log("WARN", "Índice local inconsistente (chunks != vectors); se reconstruirá")
        return None

    return {
        "meta": meta,
        "chunks": chunks,
        "vectors": vectors,
    }


def _persist_index(cfg: dict, chunks: list[dict], vectors: list[list[float]], signature: str, embed_mode: str) -> dict:
    meta_path, chunks_path, vectors_path = _index_paths(cfg)
    meta = {
        "signature": signature,
        "embed_mode": embed_mode,
        "provider": cfg["provider"],
        "model": cfg["model"],
        "documents": len({item.get("source_file") for item in chunks}),
        "chunks": len(chunks),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    cfg["index_dir"].mkdir(parents=True, exist_ok=True)
    _log("EMBED", "Guardando índice...")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    with chunks_path.open("w", encoding="utf-8") as file_obj:
        for item in chunks:
            file_obj.write(json.dumps(item, ensure_ascii=False) + "\n")
    vectors_path.write_text(json.dumps(vectors, ensure_ascii=False), encoding="utf-8")

    return {
        "meta": meta,
        "chunks": chunks,
        "vectors": vectors,
    }


def _load_sample_code_index_from_disk(cfg: dict) -> dict | None:
    meta_path, chunks_path = _sample_index_paths(cfg)
    if not (meta_path.exists() and chunks_path.exists()):
        return None

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        chunks = []
        with chunks_path.open("r", encoding="utf-8") as file_obj:
            for line in file_obj:
                line = line.strip()
                if not line:
                    continue
                chunks.append(json.loads(line))
    except Exception as exc:
        _log("WARN", f"Índice de samples corrupto; se reconstruirá. detalle={exc}")
        return None

    return {
        "meta": meta,
        "chunks": chunks,
    }


def _persist_sample_code_index(cfg: dict, chunks: list[dict], signature: str) -> dict:
    meta_path, chunks_path = _sample_index_paths(cfg)
    meta = {
        "signature": signature,
        "documents": len({item.get("source_file") for item in chunks}),
        "chunks": len(chunks),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    cfg["index_dir"].mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    with chunks_path.open("w", encoding="utf-8") as file_obj:
        for item in chunks:
            file_obj.write(json.dumps(item, ensure_ascii=False) + "\n")

    return {
        "meta": meta,
        "chunks": chunks,
    }


def _read_sample_code_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="ignore")
    except Exception:
        return ""


def _build_sample_code_index(force_reindex: bool = False) -> dict:
    global _SAMPLE_CODE_INDEX_CACHE

    cfg = _sample_code_cfg()
    files = _discover_sample_code_files()
    signature = _sample_code_signature(files, cfg)
    indexed = _load_sample_code_index_from_disk(cfg)
    if (
        not force_reindex
        and indexed is not None
        and indexed["meta"].get("signature") == signature
    ):
        _SAMPLE_CODE_INDEX_CACHE = indexed
        return indexed

    chunks: list[dict] = []
    for path in files:
        relpath = str(path.relative_to(BASE)).replace("\\", "/")
        content = _read_sample_code_file(path)
        if not content.strip():
            continue

        current_chunks = _split_code_chunks(
            content,
            max_lines=cfg["chunk_lines"],
            overlap=cfg["chunk_line_overlap"],
        )
        for chunk_id, chunk in enumerate(current_chunks, start=1):
            chunks.append(
                {
                    "source_file": relpath,
                    "chunk_id": chunk_id,
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "doc_ext": path.suffix.lower(),
                    "title": path.stem,
                    "text": chunk["text"],
                }
            )

    result = _persist_sample_code_index(cfg, chunks, signature)
    _SAMPLE_CODE_INDEX_CACHE = result
    return result


def ensure_sample_code_index(force_reindex: bool = False) -> dict:
    global _SAMPLE_CODE_INDEX_CACHE
    if _SAMPLE_CODE_INDEX_CACHE is not None and not force_reindex:
        return _SAMPLE_CODE_INDEX_CACHE
    return _build_sample_code_index(force_reindex=force_reindex)


def _score_sample_code_chunk(item: dict, user_request: str) -> float:
    text = _normalize(item.get("text", ""))
    source = _normalize(item.get("source_file", ""))
    score = 0.0

    if source.endswith(".c"):
        score += 6.0
    elif source.endswith(".h"):
        score += 4.0
    elif source.endswith("readme.md"):
        score += 2.0

    request_tokens = _tokens(user_request)
    token_hits = 0
    for token in request_tokens:
        if token in text or token in source:
            token_hits += 1
    score += min(token_hits, 16) * 3.0

    api_markers = [
        "cpct_",
        "cpctm_",
        "tilemap",
        "sprite",
        "keyboard",
        "interrupt",
        "palette",
        "vram",
        "mode 0",
        "mode 1",
        "mode 2",
    ]
    for marker in api_markers:
        if marker in text or marker in source:
            score += 2.0

    if "samples/rpg_carlos" in source:
        score += 2.5
    if "samples/the-return-of-traxtor-cpc" in source:
        score += 2.5

    return score


def get_sample_code_snippets_for_agent(agent_role: str, user_request: str, limit: int = 4) -> list[dict]:
    if agent_role not in SAMPLE_CODE_ROLE_ALLOWLIST:
        return []

    indexed = ensure_sample_code_index(force_reindex=False)
    chunks = indexed.get("chunks", [])
    if not chunks:
        return []

    ranked = sorted(
        ((item, _score_sample_code_chunk(item, user_request)) for item in chunks),
        key=lambda pair: pair[1],
        reverse=True,
    )

    cfg = _sample_code_cfg()
    selected: list[dict] = []
    per_file: dict[str, int] = {}
    for item, score in ranked:
        if score <= 0:
            continue

        source = item.get("source_file", "")
        if per_file.get(source, 0) >= 2:
            continue

        snippet = item.get("text", "")
        if len(snippet) > cfg["snippet_max_chars"]:
            snippet = snippet[: cfg["snippet_max_chars"] - 3].rstrip() + "..."

        selected.append(
            {
                "source_file": source,
                "chunk_id": item.get("chunk_id", 0),
                "start_line": item.get("start_line", 1),
                "end_line": item.get("end_line", 1),
                "score": round(score, 2),
                "snippet": snippet,
            }
        )
        per_file[source] = per_file.get(source, 0) + 1
        if len(selected) >= max(1, limit):
            break

    return selected


def format_sample_code_for_prompt(agent_role: str, user_request: str, limit: int = 4) -> str:
    snippets = get_sample_code_snippets_for_agent(agent_role, user_request, limit=limit)
    if not snippets:
        return ""

    lines = ["Relevant code examples from /samples:"]
    for snippet in snippets:
        lines.append(
            f"- [score={snippet.get('score', 0)}] "
            f"file={snippet.get('source_file', '')} "
            f"lines={snippet.get('start_line', 1)}-{snippet.get('end_line', 1)} "
            f"| excerpt={snippet.get('snippet', '')}"
        )
    return "\n".join(lines)


def _build_index(cfg: dict, force_reindex: bool = False) -> dict:
    global _INDEX_CACHE

    docs = _discover_local_docs()
    signature = _document_signature(docs, cfg)
    indexed = _load_index_from_disk(cfg)
    if (
        not force_reindex
        and indexed is not None
        and indexed["meta"].get("signature") == signature
    ):
        _log("INFO", f"Índice local cargado de caché ({indexed['meta'].get('chunks', 0)} chunks)")
        _INDEX_CACHE = indexed
        return indexed

    _log("INFO", "Reconstruyendo índice local de documentación")

    total_docs = len(docs)
    pdf_docs = [path for path in docs if path.suffix.lower() == ".pdf"]
    pdf_total = len(pdf_docs)

    chunks: list[dict] = []
    embed_texts: list[str] = []

    pdf_seen = 0
    for index, path in enumerate(docs, start=1):
        relpath = str(path.relative_to(BASE)).replace("\\", "/")
        _log("EMBED", f"Leyendo documentos: {index}/{total_docs} ({relpath})")

        if path.suffix.lower() == ".pdf":
            pdf_seen += 1
            _log("EMBED", f"Parseando PDF: {pdf_seen}/{pdf_total} ({relpath})")

        content = _read_local_doc(path)
        if not _clean_text(content):
            continue

        current_chunks = _split_chunks(content, max_chars=cfg["chunk_size"], overlap=cfg["chunk_overlap"])
        for chunk_idx, chunk_text in enumerate(current_chunks, start=1):
            chunks.append(
                {
                    "source_file": relpath,
                    "chunk_id": chunk_idx,
                    "doc_ext": path.suffix.lower(),
                    "title": path.stem,
                    "text": chunk_text,
                    "char_count": len(chunk_text),
                }
            )
            embed_texts.append(chunk_text)

        _log("EMBED", f"Chunking: {index}/{total_docs}")

    if not chunks:
        empty = _persist_index(cfg, [], [], signature, embed_mode="empty")
        _INDEX_CACHE = empty
        return empty

    embed_mode = "remote"
    try:
        if cfg["provider"] == "hashed":
            raise RuntimeError("forced hashed provider")
        vectors = _embed_texts_remote(embed_texts, cfg)
    except Exception as exc:
        embed_mode = "hashed"
        _log("WARN", f"Fallo proveedor de embeddings; fallback hashed activado. detalle={exc}")
        vectors = []
        total = len(embed_texts)
        for idx, text in enumerate(embed_texts, start=1):
            vectors.append(_embed_text_hashed(text, cfg["hashed_dim"]))
            if idx == 1 or idx == total or idx % max(1, total // 10) == 0:
                _log("EMBED", f"Generando embeddings: {idx}/{total}")

    vectors = [_normalize_vector(vector) for vector in vectors]
    result = _persist_index(cfg, chunks, vectors, signature, embed_mode=embed_mode)
    _INDEX_CACHE = result
    return result


def ensure_localdoc_index(force_reindex: bool = False) -> dict:
    cfg = _localdoc_cfg()
    should_force = force_reindex or cfg["force_reindex"]
    return _build_index(cfg, force_reindex=should_force)


def rebuild_localdoc_index() -> dict:
    return ensure_localdoc_index(force_reindex=True)


def get_localdoc_index_stats(force_reindex: bool = False) -> dict:
    index = ensure_localdoc_index(force_reindex=force_reindex)
    meta = index.get("meta", {})
    return {
        "provider": meta.get("provider", "unknown"),
        "model": meta.get("model", ""),
        "embed_mode": meta.get("embed_mode", ""),
        "documents": int(meta.get("documents", 0) or 0),
        "chunks": int(meta.get("chunks", 0) or 0),
        "index_dir": str(_localdoc_cfg()["index_dir"]),
    }


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


def _score_local_chunk(item: dict, agent_role: str, user_request: str) -> float:
    text = _normalize(item.get("text", ""))
    source = _normalize(item.get("source_file", ""))
    score = 0.0

    if agent_role in LOCAL_DOC_ROLE_ALLOWLIST:
        score += 5.0

    if "using hardware on amstrad cpc" in source:
        score += 18.0 if agent_role == "cpctelera_tech_agent" else 8.0
    if "amstrad_cpc_hardware_reference" in source:
        score += 14.0
    if "motor_grafico" in source:
        score += 10.0
    if "tutorial_crear_video_juego" in source:
        score += 8.0

    # Art retrieval is constrained to technical/graphics context.
    if agent_role == "art_agent":
        if "motor_grafico" in source or "hardware" in source or "sprite" in text or "tile" in text:
            score += 10.0
        else:
            score -= 2.0

    request_tokens = _tokens(user_request)
    token_hits = 0
    for token in request_tokens:
        if token in text:
            token_hits += 1
    score += min(token_hits, 12) * 2.5

    preferred_tech = ROLE_RULES.get(agent_role, {}).get("preferred_tech", set())
    for tech in preferred_tech:
        if tech in text or tech in source:
            score += 1.5

    return score


def _score_local_chunk_with_hash_semantic(
    item: dict,
    agent_role: str,
    user_request: str,
    query_embedding: list[float],
) -> float:
    score = _score_local_chunk(item, agent_role, user_request)

    chunk_embedding = item.get("embedding", [])
    score += _cosine_similarity(query_embedding, chunk_embedding) * LOCAL_EMBED_SCORE_WEIGHT
    return score


def _embed_query(query: str, cfg: dict, embed_mode: str) -> list[float]:
    if not query.strip():
        return []
    if embed_mode == "hashed":
        return _embed_text_hashed(query, cfg["hashed_dim"])

    try:
        vector = _embed_texts_remote([query], cfg)[0]
        return _normalize_vector(vector)
    except Exception as exc:
        _log("WARN", f"Query embedding fallback a hashed por error remoto: {exc}")
        return _embed_text_hashed(query, cfg["hashed_dim"])


def get_local_doc_snippets_for_agent(agent_role: str, user_request: str, limit: int = 5) -> list[dict]:
    if agent_role not in LOCAL_DOC_ROLE_ALLOWLIST:
        return []

    cfg = _localdoc_cfg()
    effective_limit = max(1, limit or cfg["topk"])

    _log("RAG", f"Recuperando contexto para {agent_role}...")
    indexed = ensure_localdoc_index(force_reindex=False)
    chunks = indexed.get("chunks", [])
    vectors = indexed.get("vectors", [])
    embed_mode = indexed.get("meta", {}).get("embed_mode", "hashed")

    if not chunks or not vectors:
        _log("WARN", "Índice sin chunks/vectores; retrieval vacío")
        return []

    query_embedding = _embed_query(user_request, cfg, embed_mode)
    ranked = sorted(
        (
            (
                item,
                _score_local_chunk(item, agent_role, user_request)
                + (_cosine_similarity(query_embedding, vectors[idx]) * cfg["score_weight"]),
            )
            for idx, item in enumerate(chunks)
        ),
        key=lambda pair: pair[1],
        reverse=True,
    )

    selected = []
    per_file = {}
    selected_keys = set()

    mandatory_sources = MANDATORY_TECH_DOCS.get(agent_role, [])
    if mandatory_sources:
        for source_file in mandatory_sources:
            candidate = next((pair for pair in ranked if pair[0].get("source_file") == source_file), None)
            if not candidate:
                continue
            item, score = candidate
            snippet = item.get("text", "")
            if len(snippet) > cfg["snippet_max_chars"]:
                snippet = snippet[: cfg["snippet_max_chars"] - 3].rstrip() + "..."
            selected.append(
                {
                    "source_file": source_file,
                    "chunk_id": item.get("chunk_id", 0),
                    "score": round(score, 2),
                    "snippet": snippet,
                }
            )
            per_file[source_file] = per_file.get(source_file, 0) + 1
            selected_keys.add((source_file, item.get("chunk_id", 0)))

    target_limit = max(effective_limit, len(selected))

    for item, score in ranked:
        if score <= 0 and not mandatory_sources:
            continue

        source = item.get("source_file", "")
        key = (source, item.get("chunk_id", 0))
        if key in selected_keys:
            continue
        if per_file.get(source, 0) >= 2:
            continue

        snippet = item.get("text", "")
        if len(snippet) > cfg["snippet_max_chars"]:
            snippet = snippet[: cfg["snippet_max_chars"] - 3].rstrip() + "..."

        selected.append(
            {
                "source_file": source,
                "chunk_id": item.get("chunk_id", 0),
                "score": round(score, 2),
                "snippet": snippet,
            }
        )
        per_file[source] = per_file.get(source, 0) + 1
        selected_keys.add(key)

        if len(selected) >= target_limit:
            break

    top_sources = []
    seen_sources = set()
    for item in selected:
        source = item.get("source_file", "")
        if source and source not in seen_sources:
            seen_sources.add(source)
            top_sources.append(source)
        if len(top_sources) >= 5:
            break
    _log("RAG", f"Top sources: {', '.join(top_sources) if top_sources else '(none)'}")

    return selected


def get_resources_for_agent(agent_role: str, user_request: str, limit: int = 5) -> list[dict]:
    role_aliases = RESOURCE_ROLE_ALIASES.get(agent_role, [agent_role])
    resources = [
        item for item in load_resources()
        if item.get("target_agent_role") in role_aliases
    ]

    ranked = sorted(
        resources,
        key=lambda item: _score_resource(item, agent_role, user_request),
        reverse=True,
    )
    return ranked[:limit]


def format_resources_for_prompt(agent_role: str, user_request: str, limit: int = 5) -> str:
    resources = get_resources_for_agent(agent_role, user_request, limit=limit)
    local_cfg = _localdoc_cfg()
    local_snippets = get_local_doc_snippets_for_agent(
        agent_role,
        user_request,
        limit=max(local_cfg["topk"], limit),
    )

    if not resources and not local_snippets:
        return ""

    lines = [f"Retrieved knowledge for {agent_role}:"]

    if resources:
        lines.append("Curated web/tool references:")
        for item in resources:
            lines.append(
                f"- [{item.get('ingestion_priority', 'low')}] "
                f"{item.get('title', 'Untitled')} "
                f"| category={item.get('category', '')}/{item.get('sub_category', '')} "
                f"| tech={', '.join(item.get('tech_stack', []))} "
                f"| notes={item.get('notes_for_agents', '')} "
                f"| url={item.get('url', '')}"
            )

    if local_snippets:
        lines.append("Local project documentation snippets (/data):")
        for snippet in local_snippets:
            lines.append(
                f"- [score={snippet.get('score', 0)}] "
                f"file={snippet.get('source_file', '')} "
                f"chunk={snippet.get('chunk_id', 0)} "
                f"| excerpt={snippet.get('snippet', '')}"
            )

    return "\n".join(lines)