#!/usr/bin/env bash
# Rebuild the orchestrator RAG index from agents/pm/doc/
# Run locally after adding or modifying documentation, then commit and push.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYTHONPATH="$(pwd):$(pwd)/agents/pm" python3 -c "
import rag_store
store = rag_store.build()
print(f'Orchestrator RAG rebuilt: {store.chunk_count} chunks')
print('Commit agents/pm/data/rag_index_orchestrator.json and push.')
"
