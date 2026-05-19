"""RAG service — CPCtelera Reference Manual.

Builds (on first use) a cosine-similarity index over the CPCtelera Reference
Manual PDF and exposes a single query function used by technical agents to
retrieve relevant API/hardware excerpts before each LLM call.

Index is persisted in  <project_root>/.cache/cpct_manual_index/
  embeddings.npy  — float32 matrix (n_chunks × embedding_dim)
  chunks.json     — list of raw text chunks (parallel to rows of embeddings.npy)

No external vector-DB required: pure numpy cosine similarity.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

import numpy as np
from dotenv import load_dotenv
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_BASE = Path(__file__).resolve().parents[2]
_DATA = _BASE / "data"
_CACHE = _BASE / ".cache" / "cpct_manual_index"

PDF_PATH = _DATA / "CPCtelera Reference Manual - Completo.pdf"

# Load .env so OPENAI_API_KEY is available even when rag_service is imported
# standalone (outside the main pipeline entry point).
load_dotenv(_BASE / ".env")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
_EMBED_MODEL = "text-embedding-3-small"
_CHUNK_SIZE = 1200      # chars per chunk
_CHUNK_OVERLAP = 180    # chars of overlap between consecutive chunks
_BATCH_SIZE = 100       # embeddings per API call

# ---------------------------------------------------------------------------
# In-memory state (lazy-loaded once per process)
# ---------------------------------------------------------------------------
_chunks: list[str] = []
_embeddings: Optional[np.ndarray] = None


# ---------------------------------------------------------------------------
# PDF extraction + chunking
# ---------------------------------------------------------------------------

def _extract_chunks() -> list[str]:
    """Return overlapping text chunks extracted from the PDF."""
    import pypdf  # already in requirements.txt

    reader = pypdf.PdfReader(str(PDF_PATH))
    sys.stderr.write(f"[RAG] Reading PDF ({len(reader.pages)} pages)…\n")
    sys.stderr.flush()

    buffer = ""
    chunks: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        buffer += text + "\n"
        while len(buffer) >= _CHUNK_SIZE:
            chunk = buffer[:_CHUNK_SIZE].strip()
            if chunk:
                chunks.append(chunk)
            buffer = buffer[_CHUNK_SIZE - _CHUNK_OVERLAP:]

    # Flush remainder
    remainder = buffer.strip()
    if remainder:
        chunks.append(remainder)

    sys.stderr.write(f"[RAG] Extracted {len(chunks)} chunks.\n")
    sys.stderr.flush()
    return chunks


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

def _embed_texts(texts: list[str]) -> np.ndarray:
    """Call OpenAI Embeddings API and return (n, dim) float32 array."""
    import openai

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    all_vecs: list[list[float]] = []
    batches = range(0, len(texts), _BATCH_SIZE)
    bar = tqdm(batches, desc="[RAG] Embedding chunks", unit="batch",
               total=len(batches), file=sys.stderr, leave=True)

    for i in bar:
        batch = texts[i : i + _BATCH_SIZE]
        response = client.embeddings.create(model=_EMBED_MODEL, input=batch)
        sorted_items = sorted(response.data, key=lambda x: x.index)
        all_vecs.extend(item.embedding for item in sorted_items)
        bar.set_postfix(chunks=min(i + _BATCH_SIZE, len(texts)))

    return np.array(all_vecs, dtype=np.float32)


# ---------------------------------------------------------------------------
# Index build / load
# ---------------------------------------------------------------------------

def _build_index() -> tuple[list[str], np.ndarray]:
    sys.stderr.write("[RAG] Building CPCtelera manual index (first run — may take ~1 min)…\n")
    sys.stderr.flush()

    chunks = _extract_chunks()
    embeddings = _embed_texts(chunks)

    _CACHE.mkdir(parents=True, exist_ok=True)
    np.save(str(_CACHE / "embeddings.npy"), embeddings)
    with open(_CACHE / "chunks.json", "w", encoding="utf-8") as fh:
        json.dump(chunks, fh, ensure_ascii=False)

    sys.stderr.write(f"[RAG] Index saved → {_CACHE}\n")
    sys.stderr.flush()
    return chunks, embeddings


def _load_index() -> tuple[list[str], np.ndarray]:
    embeddings = np.load(str(_CACHE / "embeddings.npy"))
    with open(_CACHE / "chunks.json", "r", encoding="utf-8") as fh:
        chunks = json.load(fh)
    sys.stderr.write(f"[RAG] Index loaded from cache ({len(chunks)} chunks).\n")
    sys.stderr.flush()
    return chunks, embeddings


def _ensure_loaded() -> bool:
    """Load or build the index into module-level globals. Returns True on success."""
    global _chunks, _embeddings

    if _embeddings is not None:
        return True

    if not PDF_PATH.exists():
        sys.stderr.write(f"[RAG] WARNING: PDF not found at {PDF_PATH} — skipping RAG.\n")
        sys.stderr.flush()
        return False

    try:
        if (_CACHE / "embeddings.npy").exists() and (_CACHE / "chunks.json").exists():
            _chunks, _embeddings = _load_index()
        else:
            _chunks, _embeddings = _build_index()
        return True
    except Exception as exc:
        sys.stderr.write(f"[RAG] ERROR initialising index: {exc}\n")
        sys.stderr.flush()
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def query_cpct_manual(query: str, k: int = 5) -> str:
    """Return the top-k most relevant CPCtelera manual passages for *query*.

    Returns a plain string ready to embed in an LLM prompt, or '' on failure.
    """
    if not _ensure_loaded():
        return ""

    if not query or not query.strip():
        return ""

    try:
        import openai

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(model=_EMBED_MODEL, input=[query.strip()])
        q_vec = np.array(response.data[0].embedding, dtype=np.float32)

        # Cosine similarity: (E @ q) / (||E|| * ||q||)
        norms = np.linalg.norm(_embeddings, axis=1)
        q_norm = np.linalg.norm(q_vec)
        if q_norm < 1e-10:
            return ""

        sims = (_embeddings @ q_vec) / (norms * q_norm + 1e-10)
        top_indices = np.argsort(sims)[::-1][:k]

        parts = [
            f"[CPCtelera Manual — extracto {i + 1}]\n{_chunks[idx].strip()}"
            for i, idx in enumerate(top_indices)
            if _chunks[idx].strip()
        ]
        return "\n\n".join(parts)

    except Exception as exc:
        sys.stderr.write(f"[RAG] query error: {exc}\n")
        sys.stderr.flush()
        return ""


def rebuild_index() -> None:
    """Force a full rebuild of the index (deletes cache first)."""
    global _chunks, _embeddings
    import shutil

    if _CACHE.exists():
        shutil.rmtree(_CACHE)
        sys.stderr.write("[RAG] Cache cleared.\n")
        sys.stderr.flush()

    _chunks = []
    _embeddings = None
    _ensure_loaded()
