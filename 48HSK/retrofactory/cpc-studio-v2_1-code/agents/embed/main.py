"""Embedding Agent — shared fastembed service.

Loads the BAAI/bge-small-en-v1.5 model (onnxruntime) ONCE here, so the agents
that consult the RAG don't each carry onnxruntime in their pod (5x ~1.5GB was
OOM-ing the node). Agents call POST /embed with their query and get the vector.

Endpoint: POST /embed
  body:    { "texts": ["query string", ...] }
  returns: { "embeddings": [[float, ...], ...] }
"""
from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CPC Studio — Embedding Agent")

_MODEL = "BAAI/bge-small-en-v1.5"
_fe = None


def _get_model():
    global _fe
    if _fe is None:
        from fastembed import TextEmbedding
        _fe = TextEmbedding(model_name=_MODEL)
    return _fe


class EmbedRequest(BaseModel):
    texts: list[str]


class EmbedResponse(BaseModel):
    embeddings: list[list[float]]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest) -> EmbedResponse:
    fe = _get_model()
    # query_embed is the retrieval-side embedding (matches how the index was built)
    vecs = [v.tolist() for v in fe.query_embed(req.texts)]
    return EmbedResponse(embeddings=vecs)


if __name__ == "__main__":
    # Warm the model at startup so the first real request isn't slow.
    _get_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
