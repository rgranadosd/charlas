#!/usr/bin/env bash
# Rebuild the developer RAG index from agents/developer/doc/
# Run this locally after adding or modifying documentation.
# The updated index must be committed and pushed so the pod picks it up.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYTHONPATH="$(pwd)" python3 -c "
from common.rag_store import RagStore
store = RagStore.build()
print(f'Developer RAG rebuilt: {store.chunk_count} chunks')
print('Commit agents/developer/data/rag_index_emb.json and push.')
"
