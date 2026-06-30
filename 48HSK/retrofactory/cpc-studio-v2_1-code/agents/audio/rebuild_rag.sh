#!/usr/bin/env bash
# Rebuild the audio RAG index from agents/audio/doc/
# Run locally after adding or modifying documentation, then commit and push.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYTHONPATH="$(pwd):$(pwd)/agents/audio" python3 -c "
import rag_store
store = rag_store.build()
print(f'Audio RAG rebuilt: {store.chunk_count} chunks')
print('Commit agents/audio/data/rag_index_audio.json and push.')
"
