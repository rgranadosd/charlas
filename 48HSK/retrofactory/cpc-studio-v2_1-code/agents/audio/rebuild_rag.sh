#!/usr/bin/env bash
# Rebuild the audio RAG index from agents/audio/doc/
# Run this locally after adding or modifying documentation.
# The updated index must be committed and pushed so the pod picks it up.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYTHONPATH="$(pwd)" python3 -c "
from common.rag_store import RagStore
store = RagStore.build_audio()
print(f'Audio RAG rebuilt: {store.chunk_count} chunks')
print('Commit agents/audio/data/rag_index_audio.json and push.')
"
