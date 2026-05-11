#!/usr/bin/env bash

cd "$(dirname "$0")"

(
printf '\n===== app/agents/cpctelera_tech_agent.py =====\n'; cat app/agents/cpctelera_tech_agent.py
printf '\n===== app/agents/code_integrator_agent.py =====\n'; cat app/agents/code_integrator_agent.py
printf '\n===== app/services/project_service.py =====\n'; cat app/services/project_service.py
printf '\n===== app/graph/main_graph.py =====\n'; cat app/graph/main_graph.py
printf '\n===== generated project path =====\n'; jq -r '.project_path' pipeline_ghosts_output.json
PROJECT_DIR=$(jq -r '.project_path' pipeline_ghosts_output.json)
printf '\n===== tree src =====\n'; tree -L 3 "$PROJECT_DIR/src" 2>/dev/null || find "$PROJECT_DIR/src" -maxdepth 3 | sort
printf '\n===== %s/src/main.c =====\n' "$PROJECT_DIR"; cat "$PROJECT_DIR/src/main.c"
printf '\n===== %s/src/game.h =====\n' "$PROJECT_DIR"; [ -f "$PROJECT_DIR/src/game.h" ] && cat "$PROJECT_DIR/src/game.h" || echo 'NO EXISTE'
printf '\n===== %s/src/game.c =====\n' "$PROJECT_DIR"; [ -f "$PROJECT_DIR/src/game.c" ] && cat "$PROJECT_DIR/src/game.c" || echo 'NO EXISTE'
) > debug_dump.txt
cat debug_dump.txt