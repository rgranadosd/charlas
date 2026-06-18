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


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest) -> EmbedResponse:
    fe = _get_model()
    # query_embed is the retrieval-side embedding (matches how the index was built)
    vecs = [v.tolist() for v in fe.query_embed(req.texts)]
    return EmbedResponse(embeddings=vecs)


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """WSO2 Agent Manager "Try it out" adapter.

    Embeds the message and returns a human-readable summary (dimension + a short
    preview) instead of the raw float array, which is useless in a chat widget.
    Use POST /embed for the machine-readable vectors.
    """
    text = (req.message or "").strip()
    if not text:
        return ChatResponse(response="Send some text and I'll return its embedding summary.", status="needs_clarification")
    vec = next(iter(_get_model().query_embed([text]))).tolist()
    preview = ", ".join(f"{v:.4f}" for v in vec[:8])
    return ChatResponse(
        response=(
            f"Embedded with `{_MODEL}`.\n"
            f"- dimension: **{len(vec)}**\n"
            f"- first 8 values: [{preview}, …]\n\n"
            f"Call POST /embed for the full machine-readable vector."
        ),
        status="ok",
    )


if __name__ == "__main__":
    # Warm the model at startup so the first real request isn't slow.
    _get_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
