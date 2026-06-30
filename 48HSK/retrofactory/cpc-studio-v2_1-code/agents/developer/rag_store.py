"""Developer agent RAG store — wraps common infrastructure with developer-specific paths.

Includes CPCtelera example .c files as additional source alongside doc/.
"""
from __future__ import annotations

from pathlib import Path

from common.rag_store import RagStore, ingest_dir, doc_sources, _ingest_c_file, _log, _YELLOW

_DOC_DIR      = Path(__file__).parent / "doc"
_EXAMPLES_DIR = Path(__file__).parents[2] / "cpctelera" / "examples"
_INDEX_FILE   = Path(__file__).parent / "data" / "rag_index_emb.json"
_LABEL        = "RAG-DEV"


def _ingest():
    chunks = ingest_dir(_DOC_DIR)
    if _EXAMPLES_DIR.exists():
        c_files = sorted(_EXAMPLES_DIR.rglob("*.c"))
        _log(f"[{_LABEL}] ingesting {len(c_files)} CPCtelera example .c files")
        for p in c_files:
            chunks.extend(_ingest_c_file(p))
    else:
        _log(f"[{_LABEL}] CPCtelera examples not found at {_EXAMPLES_DIR}", _YELLOW)
    return chunks


def _sources():
    return doc_sources(_DOC_DIR, extra_dirs=[_EXAMPLES_DIR])


def load_or_build() -> RagStore:
    return RagStore.load_or_build(_INDEX_FILE, _ingest, _sources, _LABEL)


def build() -> RagStore:
    return RagStore.build(_INDEX_FILE, _ingest, _sources, _LABEL)
