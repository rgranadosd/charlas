"""CLI entrypoint for the interactive Rafa agent."""

from __future__ import annotations

import argparse
import asyncio
import os
import traceback

import urllib3

from agent_core import RafaAgent
from banners import list_available_banners
from config import _auth_trace_enabled, load_profile
from ui_console import Colors, print_start_motd


async def async_main() -> None:
    parser = argparse.ArgumentParser(description="Rafa's Agent - Agente Shopify con WSO2")
    parser.add_argument("-d", "--debug", action="store_true", help="Modo debug con logs detallados")
    parser.add_argument("--force-auth", action="store_true", help="Fuerza nuevo login, ignorando cache")
    parser.add_argument("--custom", type=str, default="default", help="Banner personalizado (nombre del archivo en banners/)")
    parser.add_argument("--list-banners", action="store_true", help="Lista todos los banners disponibles")
    args = parser.parse_args()

    if args.list_banners:
        print("Banners disponibles:")
        for banner in list_available_banners():
            print(f"  - {banner}")
        return

    urllib3.disable_warnings()
    load_profile("cli")

    print_start_motd(banner_name=args.custom)
    print(Colors.cyan("=== AGENTE SHOPIFY IA (v2.5 FINAL) ==="))
    if args.debug:
        print(Colors.cyan("[DEBUG MODE ON]"))
    if args.force_auth and _auth_trace_enabled():
        print(Colors.cyan("[Forzando nueva autenticación...]"))

    agent = RafaAgent(
        force_auth=args.force_auth,
        debug_mode=args.debug,
        env_profile="cli",
        model_id=os.getenv("AGENT_MODEL_ID", "gpt-4o-mini"),
    )
    agent.initialize()

    if getattr(getattr(agent, "agent", None), "weather_plugin", None) is not None:
        print(Colors.green("Weather MCP Plugin inicializado"))

    print(Colors.green("Listo. Escribe 'salir' para terminar."))
    while True:
        try:
            user_input = input(f"{Colors.cyan('Tú >')} ")
            if user_input.lower() in ["exit", "quit", "salir"]:
                break
            if user_input.strip():
                await agent.ask(user_input, silent=False)
        except KeyboardInterrupt:
            break


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(Colors.red(f"Fallo al arrancar el agente: {exc}"))
        traceback.print_exc()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
