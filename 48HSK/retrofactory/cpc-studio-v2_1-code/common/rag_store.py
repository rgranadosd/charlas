"""RAG store infrastructure — generic embedding, chunking and retrieval.

No agent-specific paths here. Each agent owns its own rag_store.py that
calls the factories below with its own doc_dir and index_file.
"""
from __future__ import annotations

import json
import logging
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

_GREEN  = "\033[32m"
_CYAN   = "\033[36m"
_YELLOW = "\033[33m"
_RESET  = "\033[0m"

logger = logging.getLogger(__name__)


def _log(msg: str, color: str = _GREEN) -> None:
    logger.info("%s%s%s", color, msg, _RESET)


CHUNK_SIZE    = 500
CHUNK_OVERLAP = 80


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

_FASTEMBED_MODEL = "BAAI/bge-small-en-v1.5"
_fastembed_instance = None


def _get_fastembed():
    global _fastembed_instance
    if _fastembed_instance is None:
        from fastembed import TextEmbedding  # type: ignore
        _fastembed_instance = TextEmbedding(model_name=_FASTEMBED_MODEL)
    return _fastembed_instance


def embed_all(texts: list[str]) -> list[list[float]]:
    """Embed texts locally via fastembed. Runs fully offline."""
    total = len(texts)
    _log(f"[RAG] embedding {total} chunks con {_FASTEMBED_MODEL} (local) …", _GREEN)
    fe = _get_fastembed()
    embeddings: list[list[float]] = []
    batch_size = 128
    for start in range(0, total, batch_size):
        batch = texts[start: start + batch_size]
        end   = min(start + batch_size, total)
        pct   = int(end / total * 100)
        bar   = "█" * (pct // 5) + "░" * (20 - pct // 5)
        print(f"\r{_GREEN}[RAG] [{bar}] {end}/{total} ({pct}%)  {_RESET}", end="", flush=True)
        batch_embs = list(fe.embed(batch))
        embeddings.extend([e.tolist() for e in batch_embs])
    print()
    _log(f"[RAG] ✓ {total} chunks embebidos con {_FASTEMBED_MODEL}", _GREEN)
    return embeddings


def _embed_query(text: str) -> list[float]:
    """Embed a single query. Uses EMBED_AGENT_URL if set, falls back to local fastembed."""
    import os
    url = os.environ.get("EMBED_AGENT_URL", "")
    if url:
        import httpx
        resp = httpx.post(f"{url.rstrip('/')}/embed", json={"texts": [text]}, timeout=60)
        resp.raise_for_status()
        return resp.json()["embeddings"][0]
    fe = _get_fastembed()
    return list(fe.query_embed([text]))[0].tolist()


# ---------------------------------------------------------------------------
# Cosine similarity
# ---------------------------------------------------------------------------

def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na  = math.sqrt(sum(x * x for x in a))
    nb  = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb + 1e-10)


def _source_weight(source: str, section: str = "") -> float:
    s   = (source or "").lower()
    sec = (section or "").lower()
    if s.endswith("_working_reference.md") or s.endswith("_reference.md"):
        return 1.00
    if "cpctelera/examples/" in s or sec == "cpct_example":
        return 1.35
    if s.endswith("c89_sdcc_codegen_rules.md"):
        return 1.30
    if s.endswith("cpc_known_bugs.md"):
        return 1.20
    if s.endswith("rag_pipeline_game_autogen_spec.md"):
        return 1.25
    if s.endswith(".pdf") or s.startswith("technical/"):
        return 1.12
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
            chunks.append(Chunk(id=f"{source}__{len(chunks)}", source=source,
                                text=snippet, section=section))
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
            text = (f"{obj.get('title','')} | {obj.get('short_description','')} | "
                    f"{obj.get('notes_for_agents','')}").strip()
            if text:
                chunks.append(Chunk(id=obj.get("id", f"res_{len(chunks)}"),
                                    source=path.name, text=text,
                                    section=obj.get("category", "")))
        except json.JSONDecodeError:
            pass
    return chunks


def _ingest_c_file(path: Path) -> list[Chunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel  = str(path).split("examples/")[-1] if "examples/" in str(path) else path.name
    return [Chunk(
        id=f"cpctelera_example_{rel.replace('/', '_').replace('.', '_')}",
        source=f"cpctelera/examples/{rel}",
        text=text[:CHUNK_SIZE * 2],
        section="cpct_example",
    )]


def _ingest_pdf(path: Path) -> list[Chunk]:
    try:
        import pypdf
    except ImportError:
        _log(f"[RAG] pypdf not installed — skipping {path.name}", _YELLOW)
        return []
    chunks: list[Chunk] = []
    try:
        import logging as _logging
        _pypdf_logger = _logging.getLogger("pypdf")
        _prev = _pypdf_logger.level
        _pypdf_logger.setLevel(_logging.ERROR)
        try:
            reader = pypdf.PdfReader(str(path))
        finally:
            _pypdf_logger.setLevel(_prev)
        for page_num, page in enumerate(reader.pages):
            text = (page.extract_text() or "").strip()
            if not text:
                continue
            for c in _fixed_chunks(text, path.name, f"p{page_num + 1}"):
                c.id = f"{path.stem}__p{page_num + 1}_c{len(chunks)}"
                chunks.append(c)
    except Exception as exc:
        _log(f"[RAG] error reading {path.name}: {exc}", _YELLOW)
    return chunks


def ingest_dir(doc_dir: Path) -> list[Chunk]:
    """Ingest all .md, .jsonl and .pdf files from a directory."""
    chunks: list[Chunk] = []
    if not doc_dir.exists():
        _log(f"[RAG] doc dir not found: {doc_dir}", _YELLOW)
        return chunks
    for p in sorted(doc_dir.iterdir()):
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
    return chunks


def doc_sources(doc_dir: Path, extra_dirs: list[Path] | None = None) -> list[Path]:
    """Return all source paths for a doc directory."""
    sources: list[Path] = []
    if doc_dir.exists():
        sources += [p for p in doc_dir.iterdir()
                    if p.is_file() and p.suffix in (".md", ".jsonl", ".pdf")
                    and p.stat().st_size > 0]
    for d in (extra_dirs or []):
        if d.exists():
            sources += list(d.rglob("*.c"))
    return sources


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _save_index(chunks: list[Chunk], source_paths: list[Path], index_file: Path, label: str) -> None:
    index_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model":        _FASTEMBED_MODEL,
        "dims":         len(chunks[0].embedding) if chunks else 0,
        "source_names": sorted(p.name for p in source_paths),
        "chunks":       [asdict(c) for c in chunks],
    }
    index_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    size_kb = index_file.stat().st_size // 1024
    _log(f"[{label}] ✓ index saved → {index_file.name}  ({len(chunks)} chunks, {size_kb} KB)", _GREEN)


def _load_index(index_file: Path) -> tuple[list[Chunk], set[str]]:
    payload      = json.loads(index_file.read_text(encoding="utf-8"))
    chunks       = [Chunk(**d) for d in payload["chunks"]]
    source_names = set(payload.get("source_names", []))
    return chunks, source_names


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class RagStore:

    def __init__(self, chunks: list[Chunk], label: str = "RAG"):
        self._chunks = chunks
        self._label  = label

    @classmethod
    def build(cls, index_file: Path, ingest_fn: Callable[[], list[Chunk]],
              sources_fn: Callable[[], list[Path]], label: str) -> "RagStore":
        sources = sources_fn()
        chunks  = ingest_fn()
        if not chunks:
            _log(f"[{label}] no chunks — returning empty store", _YELLOW)
            return cls([], label=label)
        embeddings = embed_all([c.text for c in chunks])
        for chunk, emb in zip(chunks, embeddings):
            chunk.embedding = emb
        _save_index(chunks, sources, index_file, label)
        return cls(chunks, label=label)

    @classmethod
    def load_or_build(cls, index_file: Path, ingest_fn: Callable[[], list[Chunk]],
                      sources_fn: Callable[[], list[Path]], label: str) -> "RagStore":
        if index_file.exists():
            chunks, _ = _load_index(index_file)
            size_kb   = index_file.stat().st_size // 1024
            _log(f"[{label}] ✓ cache hit — {index_file.name} ({size_kb} KB, {len(chunks)} chunks)", _GREEN)
            return cls(chunks, label=label)
        _log(f"[{label}] no cache — building index …", _YELLOW)
        return cls.build(index_file, ingest_fn, sources_fn, label)

    def retrieve(self, query: str, top_k: int = 5) -> list[Chunk]:
        _log(f"[{self._label}] retrieving top-{top_k} for: {query[:70]!r}", _CYAN)
        q_emb  = _embed_query(query)
        scored = [
            (_cosine(q_emb, c.embedding) * _source_weight(c.source, c.section), c)
            for c in self._chunks if c.embedding
        ]
        scored.sort(key=lambda x: -x[0])
        for rank, (score, chunk) in enumerate(scored[:top_k], 1):
            _log(f"[{self._label}]   #{rank} score={score:.3f}  {chunk.source} | {chunk.section!r:.40}", _GREEN)
        return [c for _, c in scored[:top_k]]

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)
