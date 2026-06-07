"""
Prueba: ¿Está el agente de desarrollo recuperando RAG_PIPELINE_GAME_AUTOGEN_SPEC.md?

Ejecutar desde el directorio raíz del proyecto:
  python -m scene_agent.test_rag_autogen_spec

Verifica que las consultas relevantes al spec devuelven chunks de ese documento
en el top-5. Imprime un resumen pass/fail por consulta.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Aseguramos que el paquete sea importable
sys.path.insert(0, str(Path(__file__).parents[1]))

from scene_agent.rag_store import RagStore

TARGET_FILE = "RAG_PIPELINE_GAME_AUTOGEN_SPEC.md"

# Consultas diseñadas para recuperar secciones específicas del documento.
# Se priorizan términos únicos del spec que no están en c89_sdcc_codegen_rules.md.
QUERIES = [
    # Sección 7 — fases del pipeline: términos exclusivos del spec
    ("GameSpec tipo juego entidades condiciones victoria derrota HUD pipeline normalizacion prompt",
     "Sección 7 — Fase A: normalización de prompt"),

    # Sección 7 — plantillas por género: breakout_like shooter_like
    ("breakout_like shooter_like platform_like topdown_like plantilla genero seleccion",
     "Sección 7 — Fase B: selección de plantilla por género"),

    # Sección 8 — DoD: términos exclusivos del spec
    ("juego generado valido DoD definition done input basico colisiones funcionales HUD legible",
     "Sección 8 — DoD checklist"),

    # Sección 10 — salida JSON del pipeline
    ("pipeline emitir resumen JSON build_status ok fail template runtime_notes trazabilidad",
     "Sección 10 — JSON output estructurado"),

    # Sección 11 — fallback automático
    ("juego compila no jugable diagnostico visual marcadores grandes entidades parche precision",
     "Sección 11 — Política de fallback automático"),

    # Sección 12 — integración RAG
    ("indexar especificacion ejemplos validos genero anti-patrones recuperar constraints hard",
     "Sección 12 — Integración RAG"),
]


def _chunk_from_target(chunks) -> bool:
    return any(TARGET_FILE in c.source for c in chunks)


def run():
    print(f"\n{'='*64}")
    print(f"  RAG smoke-test: ¿se recupera {TARGET_FILE}?")
    print(f"{'='*64}\n")

    # load_or_build detectará que el spec es más nuevo que el índice y reconstruirá
    store = RagStore.load_or_build()
    print(f"\n  Chunks en índice: {store.chunk_count}\n")

    passed = 0
    failed_queries = []

    for query, label in QUERIES:
        chunks = store.retrieve(query, top_k=5)
        hit = _chunk_from_target(chunks)

        sources = [c.source for c in chunks]
        target_found = [s for s in sources if TARGET_FILE in s]
        other = [s for s in sources if TARGET_FILE not in s]

        status = "✅ PASS" if hit else "❌ FAIL"
        if hit:
            passed += 1
        else:
            failed_queries.append(label)

        print(f"  {status}  [{label}]")
        if target_found:
            for s in target_found:
                print(f"           → {s}")
        else:
            print(f"           (no aparece {TARGET_FILE} en top-5)")
            for s in other[:3]:
                print(f"           → {s}")
        print()

    print(f"{'='*64}")
    print(f"  Resultado: {passed}/{len(QUERIES)} consultas recuperan el documento\n")

    if failed_queries:
        print("  Consultas sin hit:")
        for q in failed_queries:
            print(f"    - {q}")
        print()

    if passed == len(QUERIES):
        print("  ✅  El agente entiende el documento — todas las consultas lo recuperan.")
    elif passed >= len(QUERIES) // 2:
        print("  ⚠️   Recuperación parcial — revisar chunks del documento.")
    else:
        print("  ❌  El documento NO está siendo recuperado correctamente.")
        print("      Ejecuta: python -m scene_agent.rag_store  (para forzar rebuild)")

    print(f"{'='*64}\n")
    return passed, len(QUERIES)


if __name__ == "__main__":
    run()
