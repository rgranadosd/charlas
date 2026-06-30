#!/usr/bin/env bash
# Rebuild the developer RAG index from agents/developer/doc/
# Run locally after adding or modifying documentation, then commit and push.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYTHONPATH="$(pwd):$(pwd)/agents/developer" python3 -c "
import rag_store
store = rag_store.build()
print(f'Developer RAG rebuilt: {store.chunk_count} chunks')
print('Commit agents/developer/data/rag_index_emb.json and push.')
"
