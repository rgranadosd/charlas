import json
import hashlib
import logging
import math
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
DATASET_PATH = BASE / "data" / "amstrad_cpc_resources.jsonl"
LOCAL_DOCS_DIR = BASE / "data"
LOCAL_DOC_EXTENSIONS = {".md", ".txt", ".pdf"}
LOCAL_DOC_EXCLUDE = {"amstrad_cpc_resources.jsonl"}
LOCAL_DOC_ROLE_ALLOWLIST = {"cpctelera_tech_agent", "graphics_agent", "qa_agent", "code_integrator_agent"}
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
}
LOCAL_EMBED_PROVIDER = os.getenv("LOCAL_DOC_EMBED_PROVIDER", "mistral").strip().lower()
LOCAL_EMBED_DIM = int(os.getenv("LOCAL_DOC_EMBED_DIM", "256"))
LOCAL_EMBED_SCORE_WEIGHT = float(os.getenv("LOCAL_DOC_EMBED_SCORE_WEIGHT", "20.0"))
LOCAL_MISTRAL_EMBED_MODEL = os.getenv("LOCAL_DOC_MISTRAL_EMBED_MODEL", os.getenv("MISTRAL_EMBED_MODEL", "mistral-embed"))
LOCAL_MISTRAL_BASE_URL = os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
LOCAL_MISTRAL_EMBED_CANDIDATES = int(os.getenv("LOCAL_DOC_MISTRAL_EMBED_CANDIDATES", "80"))
LOCAL_MISTRAL_EMBED_BATCH_SIZE = int(os.getenv("LOCAL_DOC_MISTRAL_EMBED_BATCH_SIZE", "32"))
LOCAL_CHUNK_SIZE = int(os.getenv("LOCAL_DOC_CHUNK_SIZE", "1200"))
LOCAL_CHUNK_OVERLAP = int(os.getenv("LOCAL_DOC_CHUNK_OVERLAP", "160"))
LOCAL_SNIPPET_MAX_CHARS = int(os.getenv("LOCAL_DOC_SNIPPET_MAX_CHARS", "520"))
LOCAL_DEFAULT_LIMIT = int(os.getenv("LOCAL_DOC_RESULTS_LIMIT", "4"))

_PRIORITY_SCORE = {"high": 30, "normal": 20, "low": 10}

ROLE_RULES = {
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
    "code_integrator_agent": ["code_integrator_agent", "cpctelera_tech_agent"],
}

_RESOURCE_CACHE = None
_LOCAL_CHUNK_CACHE = None
_MISTRAL_EMBEDDER = None
_MISTRAL_EMBED_CACHE = {}


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


def _resolve_embed_provider() -> str:
    provider = LOCAL_EMBED_PROVIDER
    if provider in {"mistral", "mistral_api", "openai", "openai_api"}:
        # Keep openai/openai_api as backward-compatible aliases for existing envs.
        return "mistral"
    return "hashed"


def _embed_text_hashed(text: str, dim: int = LOCAL_EMBED_DIM) -> list[float]:
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


def _get_mistral_embedder():
    global _MISTRAL_EMBEDDER

    if _MISTRAL_EMBEDDER is not None:
        return _MISTRAL_EMBEDDER

    if not os.getenv("MISTRAL_API_KEY"):
        return None

    try:
        from langchain_openai import OpenAIEmbeddings

        _MISTRAL_EMBEDDER = OpenAIEmbeddings(
            model=LOCAL_MISTRAL_EMBED_MODEL,
            api_key=os.getenv("MISTRAL_API_KEY"),
            base_url=LOCAL_MISTRAL_BASE_URL,
            tiktoken_enabled=False,
            check_embedding_ctx_length=False,
        )
    except Exception:
        _MISTRAL_EMBEDDER = None

    return _MISTRAL_EMBEDDER


def _embed_texts_mistral(texts: list[str]) -> list[list[float]]:
    embedder = _get_mistral_embedder()
    if embedder is None:
        raise RuntimeError("Mistral embedder is not available")

    vectors = [None] * len(texts)
    pending_texts = []
    pending_indices = []

    for idx, text in enumerate(texts):
        key = _text_cache_key(text)
        cached = _MISTRAL_EMBED_CACHE.get(key)
        if cached is not None:
            vectors[idx] = cached
            continue
        pending_texts.append(text)
        pending_indices.append(idx)

    for start in range(0, len(pending_texts), LOCAL_MISTRAL_EMBED_BATCH_SIZE):
        batch_texts = pending_texts[start : start + LOCAL_MISTRAL_EMBED_BATCH_SIZE]
        batch_vectors = embedder.embed_documents(batch_texts)
        for offset, raw_vec in enumerate(batch_vectors):
            vec = _normalize_vector(raw_vec or [])
            vector_index = pending_indices[start + offset]
            vectors[vector_index] = vec
            _MISTRAL_EMBED_CACHE[_text_cache_key(batch_texts[offset])] = vec

    return [vec or [] for vec in vectors]


def _read_local_doc(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1", errors="ignore")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except Exception:
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


def _split_chunks(text: str, max_chars: int = LOCAL_CHUNK_SIZE, overlap: int = LOCAL_CHUNK_OVERLAP) -> list[str]:
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


def load_local_doc_chunks() -> list[dict]:
    global _LOCAL_CHUNK_CACHE
    if _LOCAL_CHUNK_CACHE is not None:
        return _LOCAL_CHUNK_CACHE

    chunks = []
    if not LOCAL_DOCS_DIR.exists():
        _LOCAL_CHUNK_CACHE = chunks
        return chunks

    for path in sorted(LOCAL_DOCS_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.name in LOCAL_DOC_EXCLUDE:
            continue
        if path.suffix.lower() not in LOCAL_DOC_EXTENSIONS:
            continue

        text = _read_local_doc(path)
        if not text.strip():
            continue

        relpath = str(path.relative_to(BASE)).replace("\\", "/")
        for index, chunk in enumerate(_split_chunks(text), start=1):
            chunks.append(
                {
                    "source_file": relpath,
                    "chunk_id": index,
                    "text": chunk,
                    "embedding": _embed_text_hashed(chunk),
                }
            )

    _LOCAL_CHUNK_CACHE = chunks
    return chunks


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


def get_local_doc_snippets_for_agent(agent_role: str, user_request: str, limit: int = LOCAL_DEFAULT_LIMIT) -> list[dict]:
    if agent_role not in LOCAL_DOC_ROLE_ALLOWLIST:
        return []

    chunks = load_local_doc_chunks()
    if not chunks:
        return []

    provider = _resolve_embed_provider()

    # Base lexical/domain ranking is always available and deterministic.
    base_ranked = sorted(
        ((item, _score_local_chunk(item, agent_role, user_request)) for item in chunks),
        key=lambda pair: pair[1],
        reverse=True,
    )

    ranked = []
    if provider == "mistral":
        candidate_size = max(limit * 10, LOCAL_MISTRAL_EMBED_CANDIDATES)
        semantic_candidates = [item for item, _ in base_ranked[:candidate_size]]

        try:
            semantic_texts = [user_request] + [item.get("text", "") for item in semantic_candidates]
            semantic_vectors = _embed_texts_mistral(semantic_texts)
            query_embedding = semantic_vectors[0]
            semantic_bonus = {}

            for item, vec in zip(semantic_candidates, semantic_vectors[1:]):
                semantic_bonus[(item.get("source_file", ""), item.get("chunk_id", 0))] = (
                    _cosine_similarity(query_embedding, vec) * LOCAL_EMBED_SCORE_WEIGHT
                )

            for item, base_score in base_ranked:
                bonus = semantic_bonus.get((item.get("source_file", ""), item.get("chunk_id", 0)), 0.0)
                ranked.append((item, base_score + bonus))
        except Exception:
            provider = "hashed"

    if provider == "hashed":
        query_embedding = _embed_text_hashed(user_request)
        ranked = sorted(
            (
                (
                    item,
                    _score_local_chunk_with_hash_semantic(item, agent_role, user_request, query_embedding),
                )
                for item in chunks
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
            if len(snippet) > LOCAL_SNIPPET_MAX_CHARS:
                snippet = snippet[: LOCAL_SNIPPET_MAX_CHARS - 3].rstrip() + "..."
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

    target_limit = max(limit, len(selected))

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
        if len(snippet) > LOCAL_SNIPPET_MAX_CHARS:
            snippet = snippet[: LOCAL_SNIPPET_MAX_CHARS - 3].rstrip() + "..."

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
    local_snippets = get_local_doc_snippets_for_agent(
        agent_role,
        user_request,
        limit=max(LOCAL_DEFAULT_LIMIT, limit),
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