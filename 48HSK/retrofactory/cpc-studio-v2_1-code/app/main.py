import os
from pathlib import Path

from dotenv import load_dotenv

from app.graph.main_graph import run_studio
from app.adapters.a2a_adapter import build_local_agent_cards

BASE = Path(__file__).resolve().parents[1]
load_dotenv(BASE / ".env")


def ensure_env() -> None:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "mistral":
        if not os.getenv("MISTRAL_API_KEY"):
            raise RuntimeError(
                "No se ha encontrado MISTRAL_API_KEY en el archivo .env de la raíz del proyecto."
            )
        return

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "No se ha encontrado OPENAI_API_KEY en el archivo .env de la raíz del proyecto."
        )


if __name__ == "__main__":
    ensure_env()
    request = "Crea una base de shooter lateral para Amstrad CPC 6128 con control suave, scroll contenido y gran legibilidad visual."
    print("Local agent cards:")
    for card in build_local_agent_cards():
        print(card)
    result = run_studio(request)
    print("\n" + result["final_output"])
    print("\nGenerated project path:", result.get("generated_project_path"))
