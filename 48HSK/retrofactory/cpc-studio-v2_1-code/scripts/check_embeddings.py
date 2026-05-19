import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

load_dotenv(BASE / ".env")

from app.services.resource_service import (  # noqa: E402
    ensure_localdoc_index,
    format_resources_for_prompt,
    get_local_doc_snippets_for_agent,
    get_localdoc_index_stats,
)


def _print(msg: str) -> None:
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description="Healthcheck de embeddings/RAG local")
    parser.add_argument("--rebuild", action="store_true", help="Forzar rebuild del índice")
    parser.add_argument(
        "--query",
        default="cpctelera sprites tilemap collision mode 0",
        help="Consulta de prueba para retrieval",
    )
    parser.add_argument(
        "--agent",
        default="qa_agent",
        help="Rol de agente para retrieval (qa_agent, cpctelera_tech_agent, code_integrator_agent, art_agent)",
    )
    parser.add_argument("--topk", type=int, default=5, help="Número de resultados")
    args = parser.parse_args()

    _print("[INFO] Iniciando healthcheck de embeddings")

    ensure_localdoc_index(force_reindex=args.rebuild)
    stats = get_localdoc_index_stats(force_reindex=False)

    _print("[INFO] Configuración activa")
    _print(f"[INFO] provider={stats.get('provider', '')}")
    _print(f"[INFO] model={stats.get('model', '')}")
    _print(f"[INFO] embed_mode={stats.get('embed_mode', '')}")
    _print(f"[INFO] documents={stats.get('documents', 0)}")
    _print(f"[INFO] chunks={stats.get('chunks', 0)}")
    _print(f"[INFO] index_dir={stats.get('index_dir', '')}")

    snippets = get_local_doc_snippets_for_agent(args.agent, args.query, limit=max(1, args.topk))

    _print(f"[RAG] query={args.query}")
    _print(f"[RAG] agent={args.agent}")
    _print(f"[RAG] hits={len(snippets)}")

    useful = False
    for idx, item in enumerate(snippets, start=1):
        source = item.get("source_file", "")
        score = item.get("score", 0)
        excerpt = item.get("snippet", "")
        _print(f"[RAG] #{idx} score={score} source={source}")
        _print(f"[RAG]    excerpt={excerpt}")
        if source.startswith("data/") and excerpt.strip():
            useful = True

    context_preview = format_resources_for_prompt(args.agent, args.query, limit=max(1, args.topk))
    _print("[RAG] prompt_context_preview_start")
    _print(context_preview[:2000])
    _print("[RAG] prompt_context_preview_end")

    if useful:
        _print("[INFO] HEALTHCHECK OK: retrieval devuelve contenido útil desde /data")
        return 0

    _print("[WARN] HEALTHCHECK DEGRADED: no se encontró contenido útil desde /data")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
