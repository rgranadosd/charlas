#!/usr/bin/env bash
# Rebuild the orchestrator RAG index from doc/ (root-level markdown files)
# Run this locally after adding or modifying orchestrator documentation.
# The updated index must be committed and pushed so the pod picks it up.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYTHONPATH="$(pwd)" python3 -c "
from common.rag_store import RagStore
store = RagStore.build_orchestrator()
print(f'Orchestrator RAG rebuilt: {store.chunk_count} chunks')
print('Commit agents/pm/data/rag_index_orchestrator.json and push.')
"
