"""PM / Orchestrator agent RAG store — wraps common infrastructure with pm-specific paths."""
from __future__ import annotations

from pathlib import Path

from common.rag_store import RagStore, ingest_dir, doc_sources

_DOC_DIR    = Path(__file__).parent / "doc"
_INDEX_FILE = Path(__file__).parent / "data" / "rag_index_orchestrator.json"
_LABEL      = "RAG-ORCH"


def _ingest():
    return ingest_dir(_DOC_DIR)


def _sources():
    return doc_sources(_DOC_DIR)


def load_or_build() -> RagStore:
    return RagStore.load_or_build(_INDEX_FILE, _ingest, _sources, _LABEL)


def build() -> RagStore:
    return RagStore.build(_INDEX_FILE, _ingest, _sources, _LABEL)
