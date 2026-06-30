"""Local RAG store — real vector embeddings via text-embedding-nomic-embed-text-v1.5.

Pipeline:
  ingest → chunk → embed (LM Studio) → persist (JSON) → cosine retrieve

No external vector-DB: pure-Python cosine similarity over stored float arrays.
Index is rebuilt when any source file is newer than the persisted index.
"""
from __future__ import annotations

import json
import logging
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from langchain_openai import OpenAIEmbeddings  # kept for possible future use

_GREEN  = "\033[32m"
_CYAN   = "\033[36m"
_YELLOW = "\033[33m"
_RESET  = "\033[0m"

logger = logging.getLogger(__name__)


def _log(msg: str, color: str = _GREEN) -> None:
    logger.info("%s%s%s", color, msg, _RESET)

_REPO_ROOT       = Path(__file__).parents[1]
_DEVELOPER_DIR   = _REPO_ROOT / "agents" / "developer" / "doc"
_AUDIO_DIR       = _REPO_ROOT / "agents" / "audio" / "doc"
_EXAMPLES_DIR    = _REPO_ROOT / "cpctelera" / "examples"
_DOC_DIR         = _REPO_ROOT / "doc"
_INDEX_FILE      = _REPO_ROOT / "agents" / "developer" / "data" / "rag_index_emb.json"
_ORCH_INDEX_FILE = _REPO_ROOT / "agents" / "pm" / "data" / "rag_index_orchestrator.json"
_AUDIO_INDEX_FILE = _REPO_ROOT / "agents" / "audio" / "data" / "rag_index_audio.json"
_REPO_ROOT_ENV   = _REPO_ROOT / ".env"

BATCH_SIZE = 32

CHUNK_SIZE    = 500
CHUNK_OVERLAP = 80


# ---------------------------------------------------------------------------
# Embedding config
# ---------------------------------------------------------------------------

def _read_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if _REPO_ROOT_ENV.exists():
        for line in _REPO_ROOT_ENV.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    id:        str
    source:    str
    text:      str
    section:   str = ""
    embedding: list[float] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Embedding backend — fastembed (local, no API key needed)
# ---------------------------------------------------------------------------

# Model: BAAI/bge-small-en-v1.5  ~130 MB, 384 dims, fast on CPU
_FASTEMBED_MODEL = "BAAI/bge-small-en-v1.5"
_fastembed_instance = None   # lazy singleton


def _get_fastembed():
    global _fastembed_instance
    if _fastembed_instance is None:
        from fastembed import TextEmbedding  # type: ignore
        _fastembed_instance = TextEmbedding(model_name=_FASTEMBED_MODEL)
    return _fastembed_instance


def embed_all(texts: list[str]) -> list[list[float]]:
    """Embed all texts locally via fastembed (BAAI/bge-small-en-v1.5).

    Runs fully offline — no API keys, no rate limits.
    Shows a single overwriting progress bar.
    """
    import logging as _logging
    total = len(texts)
    _log(f"[RAG] embedding {total} chunks con {_FASTEMBED_MODEL} (local) …", _GREEN)

    fe = _get_fastembed()

    embeddings: list[list[float]] = []
    # fastembed yields results as a generator; process in batches for the bar
    batch_size = 128   # CPU batch — larger than API batches is fine locally
    for start in range(0, total, batch_size):
        batch = texts[start: start + batch_size]
        end   = min(start + batch_size, total)
        pct   = int(end / total * 100)
        bar   = "█" * (pct // 5) + "░" * (20 - pct // 5)
        print(
            f"\r{_GREEN}[RAG] [{bar}] {end}/{total} ({pct}%)  {_RESET}",
            end="", flush=True,
        )
        batch_embs = list(fe.embed(batch))
        embeddings.extend([e.tolist() for e in batch_embs])

    print()  # newline after progress bar
    _log(f"[RAG] ✓ {total} chunks embebidos con {_FASTEMBED_MODEL}", _GREEN)
    return embeddings


def _embed_query(text: str) -> list[float]:
    """Embed a single query string for retrieval.

    In k3s, EMBED_AGENT_URL points to the shared embedding service so the heavy
    onnxruntime model loads ONCE there instead of in every agent (which OOM-ed
    the node). Falls back to local fastembed when the var is unset (dev).
    """
    import os
    url = os.environ.get("EMBED_AGENT_URL", "")
    if url:
        import httpx
        resp = httpx.post(f"{url.rstrip('/')}/embed", json={"texts": [text]}, timeout=60)
        resp.raise_for_status()
        return resp.json()["embeddings"][0]
    fe = _get_fastembed()
    result = list(fe.query_embed([text]))
    return result[0].tolist()


# ---------------------------------------------------------------------------
# Cosine similarity
# ---------------------------------------------------------------------------

def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na  = math.sqrt(sum(x * x for x in a))
    nb  = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb + 1e-10)


def _source_weight(source: str, section: str = "") -> float:
    """Trust prior per source type.

    Higher weight for ground-truth technical material (CPCtelera code/examples,
    verified rulebook), lower for generic prose.
    """
    s = (source or "").lower()
    sec = (section or "").lower()

    # Single-game implementation references must NOT carry a global priority
    # boost: a fixed 1.50 made the Arkanoid reference outrank everything for any
    # game, contaminating e.g. a Pac-Man build with ball/paddle/brick code. Leave
    # them at neutral weight so cosine similarity decides relevance per game
    # (high for the matching game, low for others). Game-agnostic technical
    # sources below keep their boost because they apply to every game.
    if s.endswith("_working_reference.md") or s.endswith("_reference.md"):
        return 1.00   # concrete single-game example — relevance via similarity only
    if "cpctelera/examples/" in s or sec == "cpct_example":
        return 1.35
    if s.endswith("c89_sdcc_codegen_rules.md"):
        return 1.30

    # Medium-high confidence: known bug catalog and technical docs
    if s.endswith("cpc_known_bugs.md"):
        return 1.20
    # Pipeline + autogen spec: curated contract for game generation pipeline
    if s.endswith("rag_pipeline_game_autogen_spec.md"):
        return 1.25
    if s.endswith(".pdf") or s.startswith("technical/"):
        return 1.12

    # Generic markdown/jsonl knowledge
    if s.endswith(".md") or s.endswith(".jsonl"):
        return 1.00

    return 1.00


# ---------------------------------------------------------------------------
# Chunking helpers
# ---------------------------------------------------------------------------

def _fixed_chunks(text: str, source: str, section: str = "") -> list[Chunk]:
    chunks: list[Chunk] = []
    pos = 0
    while pos < len(text):
        snippet = text[pos: pos + CHUNK_SIZE].strip()
        if snippet:
            chunks.append(Chunk(
                id=f"{source}__{len(chunks)}",
                source=source,
                text=snippet,
                section=section,
            ))
        pos += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def _ingest_markdown(path: Path) -> list[Chunk]:
    text  = path.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"(?m)^#{1,3} ", text)
    chunks: list[Chunk] = []
    for i, part in enumerate(parts):
        heading = part.split("\n", 1)[0].strip()[:60]
        body    = part[len(heading):].strip()
        for c in _fixed_chunks(body, path.name, heading):
            c.id = f"{path.stem}__h{i}_c{len(chunks)}"
            chunks.append(c)
    return chunks


def _ingest_jsonl(path: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj  = json.loads(line)
            text = (
                f"{obj.get('title','')} | "
                f"{obj.get('short_description','')} | "
                f"{obj.get('notes_for_agents','')}"
            ).strip()
            if text:
                chunks.append(Chunk(
                    id=obj.get("id", f"res_{len(chunks)}"),
                    source=path.name,
                    text=text,
                    section=obj.get("category", ""),
                ))
        except json.JSONDecodeError:
            pass
    return chunks


def _ingest_c_file(path: Path) -> list[Chunk]:
    """Ingest a CPCtelera example .c file as a single chunk (real working code)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    # Use the relative path from examples/ as the id
    rel = str(path).split("examples/")[-1] if "examples/" in str(path) else path.name
    return [Chunk(
        id=f"cpctelera_example_{rel.replace('/', '_').replace('.', '_')}",
        source=f"cpctelera/examples/{rel}",
        text=text[:CHUNK_SIZE * 2],   # allow bigger chunks for code
        section="cpct_example",
    )]


def _ingest_pdf(path: Path) -> list[Chunk]:
    """Extract text from a PDF page by page and chunk it."""
    try:
        import pypdf
    except ImportError:
        _log(f"[RAG] pypdf not installed — skipping {path.name}", _YELLOW)
        return []

    chunks: list[Chunk] = []
    try:
        # Silence pypdf's "Ignoring wrong pointing object" warnings — these come
        # from corrupt XRef entries in the PDF and do not affect text extraction.
        import logging as _logging
        _pypdf_logger = _logging.getLogger("pypdf")
        _prev_level = _pypdf_logger.level
        _pypdf_logger.setLevel(_logging.ERROR)
        try:
            reader = pypdf.PdfReader(str(path))
        finally:
            _pypdf_logger.setLevel(_prev_level)

        _log(f"[RAG] PDF {path.name}: {len(reader.pages)} pages", _CYAN)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text = text.strip()
            if not text:
                continue
            for c in _fixed_chunks(text, path.name, f"p{page_num + 1}"):
                c.id = f"{path.stem}__p{page_num + 1}_c{len(chunks)}"
                chunks.append(c)
    except Exception as exc:
        _log(f"[RAG] error reading {path.name}: {exc}", _YELLOW)
    return chunks


def _ingest_all() -> list[Chunk]:
    chunks: list[Chunk] = []

    # Developer agent documentation (agents/developer/doc/)
    if _DEVELOPER_DIR.exists():
        for p in sorted(_DEVELOPER_DIR.iterdir()):
            if not p.is_file() or p.stat().st_size == 0:
                continue
            if p.suffix == ".md":
                _log(f"[RAG] ingesting {p.name}", _CYAN)
                chunks.extend(_ingest_markdown(p))
            elif p.suffix == ".jsonl":
                _log(f"[RAG] ingesting {p.name}", _CYAN)
                chunks.extend(_ingest_jsonl(p))
            elif p.suffix == ".pdf":
                _log(f"[RAG] ingesting PDF {p.name}", _CYAN)
                chunks.extend(_ingest_pdf(p))
    else:
        _log(f"[RAG] developer doc dir not found: {_DEVELOPER_DIR}", _YELLOW)

    # CPCtelera example code (real working C — highest value for the expert)
    if _EXAMPLES_DIR.exists():
        c_files = sorted(_EXAMPLES_DIR.rglob("*.c"))
        _log(f"[RAG] ingesting {len(c_files)} CPCtelera example .c files", _CYAN)
        for p in c_files:
            chunks.extend(_ingest_c_file(p))
    else:
        _log(f"[RAG] CPCtelera examples not found at {_EXAMPLES_DIR}", _YELLOW)

    _log(f"[RAG] total chunks: {len(chunks)}", _GREEN)
    return chunks


def _ingest_orchestrator() -> list[Chunk]:
    """Ingest only the root-level markdown files in doc/ (no subdirectories).

    These contain architecture and system design knowledge for the orchestrator:
    e.g. architecture_single_agent_v1.md, supervisor_transition_plan.md.
    """
    chunks: list[Chunk] = []
    if not _DOC_DIR.exists():
        _log(f"[RAG-ORCH] doc dir not found: {_DOC_DIR}", _YELLOW)
        return chunks

    # Only files directly in doc/ — skip subdirectories like doc/technical/
    for p in sorted(_DOC_DIR.iterdir()):
        if p.is_file() and p.suffix == ".md" and p.stat().st_size > 0:
            _log(f"[RAG-ORCH] ingesting {p.name}", _CYAN)
            chunks.extend(_ingest_markdown(p))

    _log(f"[RAG-ORCH] total chunks: {len(chunks)}", _GREEN)
    return chunks


# ---------------------------------------------------------------------------
# Source-path helpers (single source of truth for each RAG's inputs)
# ---------------------------------------------------------------------------

def _tech_rag_sources() -> list[Path]:
    """All file paths that feed the TECH-RAG (developer) index."""
    return (
        ([p for p in _DEVELOPER_DIR.iterdir()
          if p.is_file() and p.suffix in (".md", ".jsonl", ".pdf") and p.stat().st_size > 0]
         if _DEVELOPER_DIR.exists() else []) +
        (list(_EXAMPLES_DIR.rglob("*.c"))
         if _EXAMPLES_DIR.exists() else [])
    )


def _orch_rag_sources() -> list[Path]:
    """All file paths that feed the RAG-ORCH index."""
    if not _DOC_DIR.exists():
        return []
    return [p for p in _DOC_DIR.iterdir() if p.is_file() and p.suffix == ".md"]


def _audio_rag_sources() -> list[Path]:
    """All file paths that feed the AUDIO-RAG index (data/audio/ only)."""
    if not _AUDIO_DIR.exists():
        return []
    return [p for p in sorted(_AUDIO_DIR.iterdir())
            if p.is_file() and p.suffix in (".md", ".jsonl", ".pdf") and p.stat().st_size > 0]


def _ingest_audio() -> list[Chunk]:
    """Ingest .md, .jsonl and .pdf files from data/audio/ for the audio agent."""
    chunks: list[Chunk] = []
    if not _AUDIO_DIR.exists():
        _log(f"[RAG-AUDIO] audio dir not found: {_AUDIO_DIR}", _YELLOW)
        return chunks
    for p in sorted(_AUDIO_DIR.iterdir()):
        if not p.is_file() or p.stat().st_size == 0:
            continue
        if p.suffix == ".md":
            _log(f"[RAG-AUDIO] ingesting {p.name}", _CYAN)
            chunks.extend(_ingest_markdown(p))
        elif p.suffix == ".jsonl":
            _log(f"[RAG-AUDIO] ingesting {p.name}", _CYAN)
            chunks.extend(_ingest_jsonl(p))
        elif p.suffix == ".pdf":
            _log(f"[RAG-AUDIO] ingesting PDF {p.name}", _CYAN)
            chunks.extend(_ingest_pdf(p))
    _log(f"[RAG-AUDIO] total chunks: {len(chunks)}", _GREEN)
    return chunks


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _save(chunks: list[Chunk], source_paths: list[Path]) -> None:
    payload = {
        "model":        _FASTEMBED_MODEL,
        "dims":         len(chunks[0].embedding) if chunks else 0,
        "source_names": sorted(p.name for p in source_paths),
        "chunks":       [asdict(c) for c in chunks],
    }
    _INDEX_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    size_kb = _INDEX_FILE.stat().st_size // 1024
    _log(f"[TECH-RAG] ✓ index saved → {_INDEX_FILE.name}  ({len(chunks)} chunks, {size_kb} KB)", _GREEN)


def _save_orchestrator(chunks: list[Chunk], source_paths: list[Path]) -> None:
    payload = {
        "model":        _FASTEMBED_MODEL,
        "dims":         len(chunks[0].embedding) if chunks else 0,
        "source_names": sorted(p.name for p in source_paths),
        "chunks":       [asdict(c) for c in chunks],
    }
    _ORCH_INDEX_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    size_kb = _ORCH_INDEX_FILE.stat().st_size // 1024
    _log(f"[RAG-ORCH] ✓ index saved → {_ORCH_INDEX_FILE.name}  ({len(chunks)} chunks, {size_kb} KB)", _GREEN)


def _save_audio(chunks: list[Chunk], source_paths: list[Path]) -> None:
    payload = {
        "model":        _FASTEMBED_MODEL,
        "dims":         len(chunks[0].embedding) if chunks else 0,
        "source_names": sorted(p.name for p in source_paths),
        "chunks":       [asdict(c) for c in chunks],
    }
    _AUDIO_INDEX_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    size_kb = _AUDIO_INDEX_FILE.stat().st_size // 1024
    _log(f"[RAG-AUDIO] ✓ index saved → {_AUDIO_INDEX_FILE.name}  ({len(chunks)} chunks, {size_kb} KB)", _GREEN)


def _read_index(index_file: Path) -> tuple[list[Chunk], set[str]]:
    """Load chunks + stored source names from an index file."""
    payload = json.loads(index_file.read_text(encoding="utf-8"))
    chunks = [Chunk(**d) for d in payload["chunks"]]
    source_names = set(payload.get("source_names", []))
    return chunks, source_names


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class RagStore:

    def __init__(self, chunks: list[Chunk], label: str = "TECH-RAG"):
        self._chunks = chunks
        self._label  = label

    # -- construction --------------------------------------------------------

    @classmethod
    def build(cls) -> "RagStore":
        """Ingest docs, embed every chunk locally via fastembed, persist."""
        sources = _tech_rag_sources()
        chunks  = _ingest_all()
        texts   = [c.text for c in chunks]
        embeddings = embed_all(texts)
        for chunk, emb in zip(chunks, embeddings):
            chunk.embedding = emb
        _save(chunks, sources)
        return cls(chunks, label="TECH-RAG")

    @classmethod
    def load_or_build(cls) -> "RagStore":
        label = "TECH-RAG"
        if _INDEX_FILE.exists():
            current_sources = _tech_rag_sources()
            current_names   = {p.name for p in current_sources}
            index_mtime     = _INDEX_FILE.stat().st_mtime

            chunks, stored_names = _read_index(_INDEX_FILE)

            added   = current_names - stored_names
            removed = stored_names  - current_names
            stale   = []  # mtime no es fiable en contenedores (git no preserva mtime); el cache se invalida solo por ficheros añadidos/borrados, no por mtime

            # Imagen inmutable: el índice horneado es la fuente de verdad. No
            # reconstruir por ficheros fuente ausentes (no versionados) — el
            # texto+embeddings ya viven en el índice. (borra el índice en dev
            # para forzar rebuild.)
            if True:
                size_kb = _INDEX_FILE.stat().st_size // 1024
                _log(
                    f"[{label}] ✓ cache hit — loading {_INDEX_FILE.name} ({size_kb} KB, "
                    f"no source changes)",
                    _GREEN,
                )
                store = cls(chunks, label=label)
                _log(f"[{label}] ✓ {store.chunk_count} chunks ready", _GREEN)
                return store

            if added:
                _log(f"[{label}] nuevos ficheros: {sorted(added)} — rebuilding …", _YELLOW)
            if removed:
                _log(f"[{label}] ficheros borrados: {sorted(removed)} — rebuilding …", _YELLOW)
            if stale:
                _log(f"[{label}] ficheros modificados: {stale[:5]} — rebuilding …", _YELLOW)
        else:
            _log(f"[{label}] no cache found — building embedding index …", _YELLOW)
        return cls.build()

    # -- orchestrator RAG (doc/ root only) -----------------------------------

    @classmethod
    def build_orchestrator(cls) -> "RagStore":
        """Ingest doc/ root .md files, embed locally, persist to rag_index_orchestrator.json."""
        sources = _orch_rag_sources()
        chunks  = _ingest_orchestrator()
        texts   = [c.text for c in chunks]
        embeddings = embed_all(texts)
        for chunk, emb in zip(chunks, embeddings):
            chunk.embedding = emb
        _save_orchestrator(chunks, sources)
        return cls(chunks, label="RAG-ORCH")

    @classmethod
    def load_or_build_orchestrator(cls) -> "RagStore":
        """Load orchestrator RAG from cache or rebuild from doc/ root .md files."""
        label = "RAG-ORCH"
        if _ORCH_INDEX_FILE.exists():
            current_sources = _orch_rag_sources()
            current_names   = {p.name for p in current_sources}
            index_mtime     = _ORCH_INDEX_FILE.stat().st_mtime

            chunks, stored_names = _read_index(_ORCH_INDEX_FILE)

            added   = current_names - stored_names
            removed = stored_names  - current_names
            stale   = []  # mtime no es fiable en contenedores (git no preserva mtime); el cache se invalida solo por ficheros añadidos/borrados, no por mtime

            # Imagen inmutable: el índice horneado es la fuente de verdad. No
            # reconstruir por ficheros fuente ausentes (no versionados) — el
            # texto+embeddings ya viven en el índice. (borra el índice en dev
            # para forzar rebuild.)
            if True:
                size_kb = _ORCH_INDEX_FILE.stat().st_size // 1024
                _log(
                    f"[{label}] ✓ cache hit — loading {_ORCH_INDEX_FILE.name} ({size_kb} KB, "
                    f"no source changes)",
                    _GREEN,
                )
                store = cls(chunks, label=label)
                _log(f"[{label}] ✓ {store.chunk_count} chunks ready", _GREEN)
                return store

            if added:
                _log(f"[{label}] nuevos ficheros: {sorted(added)} — rebuilding …", _YELLOW)
            if removed:
                _log(f"[{label}] ficheros borrados: {sorted(removed)} — rebuilding …", _YELLOW)
            if stale:
                _log(f"[{label}] ficheros modificados: {stale} — rebuilding …", _YELLOW)
        else:
            _log(f"[{label}] no cache found — building orchestrator index …", _YELLOW)
        return cls.build_orchestrator()

    # -- audio RAG (data/audio/ only) ----------------------------------------

    @classmethod
    def build_audio(cls) -> "RagStore":
        """Ingest data/audio/ .md/.jsonl files, embed locally, persist to rag_index_audio.json."""
        sources = _audio_rag_sources()
        chunks  = _ingest_audio()
        if not chunks:
            _log("[RAG-AUDIO] no audio files found — returning empty store", _YELLOW)
            return cls([], label="RAG-AUDIO")
        texts = [c.text for c in chunks]
        embeddings = embed_all(texts)
        for chunk, emb in zip(chunks, embeddings):
            chunk.embedding = emb
        _save_audio(chunks, sources)
        return cls(chunks, label="RAG-AUDIO")

    @classmethod
    def load_or_build_audio(cls) -> "RagStore":
        """Load audio RAG from cache or rebuild from data/audio/ files."""
        label = "RAG-AUDIO"
        if _AUDIO_INDEX_FILE.exists():
            current_sources = _audio_rag_sources()
            current_names   = {p.name for p in current_sources}
            index_mtime     = _AUDIO_INDEX_FILE.stat().st_mtime

            chunks, stored_names = _read_index(_AUDIO_INDEX_FILE)

            added   = current_names - stored_names
            removed = stored_names  - current_names
            stale   = []  # mtime no es fiable en contenedores (git no preserva mtime); el cache se invalida solo por ficheros añadidos/borrados, no por mtime

            # Imagen inmutable: el índice horneado es la fuente de verdad. No
            # reconstruir por ficheros fuente ausentes (no versionados) — el
            # texto+embeddings ya viven en el índice. (borra el índice en dev
            # para forzar rebuild.)
            if True:
                size_kb = _AUDIO_INDEX_FILE.stat().st_size // 1024
                _log(
                    f"[{label}] ✓ cache hit — loading {_AUDIO_INDEX_FILE.name} ({size_kb} KB, "
                    f"no source changes)",
                    _GREEN,
                )
                store = cls(chunks, label=label)
                _log(f"[{label}] ✓ {store.chunk_count} chunks ready", _GREEN)
                return store

            if added:
                _log(f"[{label}] nuevos ficheros: {sorted(added)} — rebuilding …", _YELLOW)
            if removed:
                _log(f"[{label}] ficheros borrados: {sorted(removed)} — rebuilding …", _YELLOW)
            if stale:
                _log(f"[{label}] ficheros modificados: {stale} — rebuilding …", _YELLOW)
        else:
            _log(f"[{label}] no cache found — building audio index …", _YELLOW)
        return cls.build_audio()

    # -- retrieval -----------------------------------------------------------

    def retrieve(self, query: str, top_k: int = 5) -> list[Chunk]:
        _log(f"[{self._label}] retrieving top-{top_k} for: {query[:70]!r}", _CYAN)
        q_emb = _embed_query(query)
        scored = []
        for c in self._chunks:
            if not c.embedding:
                continue
            base = _cosine(q_emb, c.embedding)
            weight = _source_weight(c.source, c.section)
            scored.append((base * weight, base, weight, c))

        scored.sort(key=lambda x: -x[0])
        top = scored[:top_k]
        for rank, (score, base, weight, chunk) in enumerate(top, 1):
            _log(
                f"[{self._label}]   #{rank} score={score:.3f} (base={base:.3f} * w={weight:.2f})  "
                f"{chunk.source} | {chunk.section!r:.40}",
                _GREEN,
            )
        return [c for _, _, _, c in top]

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)
