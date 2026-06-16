#!/usr/bin/env bash
# pick_and_play.sh
# 1. Lista los runs del pod cpc-pm
# 2. Descarga main.c (y audio.c/audio.h si existen) del run elegido
# 3. Los copia en pruebacpct/src/ (que ya tiene el Makefile local correcto)
# 4. Compila con make local
# 5. Lanza el DSK en Caprice32
#
# Uso:
#   ./pick_and_play.sh            modo normal: elegir run, compilar y jugar
#   ./pick_and_play.sh --delete   muestra la misma lista pero BORRA del pod el run elegido

set -uo pipefail

# ── Modo (normal | delete) ─────────────────────────────────────────────────
MODE="play"
for arg in "$@"; do
  case "$arg" in
    --delete|-d) MODE="delete" ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Argumento desconocido: $arg (usa -h)"; exit 2 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRUEBA="$SCRIPT_DIR/pruebacpct"
CAP32="$SCRIPT_DIR/cpctelera/tools/caprice32/cap32"
NS="dp-default-retro-factory-default-92f5b12e"
CONTEXT="k3d-amp-local"
LABEL="openchoreo.dev/component=cpc-pm"

G="\033[32m"; R="\033[31m"; Y="\033[33m"; B="\033[36m"; W="\033[1m"; RS="\033[0m"

echo -e "${B}${W}══════════════════════════════════════════${RS}"
if [ "$MODE" = "delete" ]; then
  echo -e "${B}${W}  CPC Studio — DELETE run from pod${RS}"
else
  echo -e "${B}${W}  CPC Studio — pick, compile & play${RS}"
fi
echo -e "${B}${W}══════════════════════════════════════════${RS}\n"

# ── 1. Obtener pod ─────────────────────────────────────────────────────────
# Solo el pod en ejecución (un rollout deja pods Succeeded/Terminating viejos
# con outputs/ vacío; .items[0] podía caer en uno de esos).
POD=$(kubectl get pod -n "$NS" --context "$CONTEXT" -l "$LABEL" \
  --field-selector=status.phase=Running \
  -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)
if [ -z "$POD" ]; then
  echo -e "${R}  Error: pod cpc-pm no encontrado.${RS}"; exit 1
fi
echo -e "  Pod: ${W}$POD${RS}\n"

# ── 2. Listar runs del pod ─────────────────────────────────────────────────
RUNS=()
while IFS= read -r line; do
  [ -n "$line" ] && RUNS+=("$line")
done < <(
  kubectl exec -n "$NS" --context "$CONTEXT" "$POD" -- \
    ls /app/scene_agent/outputs/ 2>/dev/null | sort -r | head -10 || true
)

if [ ${#RUNS[@]} -eq 0 ]; then
  echo -e "${Y}  El pod no tiene runs aún.${RS}"; exit 1
fi

echo -e "${W}  Últimos runs en el pod:${RS}\n"
for i in "${!RUNS[@]}"; do
  echo -e "  ${W}[$((i+1))]${RS}  ${RUNS[$i]}"
done

# ── 3. Elegir ─────────────────────────────────────────────────────────────
echo ""
if [ "$MODE" = "delete" ]; then
  read -rp "  Elige cuál BORRAR (1-${#RUNS[@]}): " CHOICE
else
  read -rp "  Elige (1-${#RUNS[@]}) o Enter para el más reciente: " CHOICE
  [ -z "$CHOICE" ] && CHOICE=1
fi

if ! echo "$CHOICE" | grep -qE '^[0-9]+$' || \
   [ "$CHOICE" -lt 1 ] || [ "$CHOICE" -gt "${#RUNS[@]}" ]; then
  echo -e "${Y}  Opción no válida.${RS}"; exit 1
fi

RUN="${RUNS[$((CHOICE-1))]}"
POD_SRC="/app/scene_agent/outputs/$RUN/src"

# ── 3b. Modo borrado: eliminar el run del pod y salir ──────────────────────
if [ "$MODE" = "delete" ]; then
  RUN_DIR="/app/scene_agent/outputs/$RUN"
  echo ""
  echo -e "  Vas a borrar del pod: ${W}$RUN_DIR${RS}"
  read -rp "  ¿Seguro? Escribe 'si' para confirmar: " CONFIRM
  if [ "$CONFIRM" != "si" ]; then
    echo -e "${Y}  Cancelado. No se ha borrado nada.${RS}"; exit 0
  fi
  if kubectl exec -n "$NS" --context "$CONTEXT" "$POD" -- \
       rm -rf "$RUN_DIR"; then
    echo -e "  ${G}✓ Borrado del pod: $RUN${RS}"
  else
    echo -e "  ${R}✗ Error al borrar $RUN del pod.${RS}"; exit 1
  fi
  exit 0
fi

# ── 4. Descargar src/ del run elegido ────────────────────────────────────
echo -e "\n  Descargando fuentes de ${W}$RUN${RS}..."

for f in main.c audio.c audio.h; do
  EXISTS=$(kubectl exec -n "$NS" --context "$CONTEXT" "$POD" -- \
    ls "$POD_SRC/$f" 2>/dev/null || true)
  if [ -n "$EXISTS" ]; then
    kubectl cp --context "$CONTEXT" \
      "$NS/$POD:$POD_SRC/$f" "$PRUEBA/src/$f" 2>/dev/null
    echo -e "  ${G}✓${RS}  $f"
  else
    echo -e "  ${Y}—${RS}  $f (no existe en el pod)"
  fi
done

# ── 5. Parchear PROJNAME a "scene" para que el binario se llame SCENE.BIN ──
CFG="$PRUEBA/cfg/build_config.mk"
sed -i.bak "s|^PROJNAME[[:space:]]*:=.*|PROJNAME := scene|" "$CFG"
echo -e "  ${G}✓${RS}  PROJNAME parcheado → scene"

# ── 6. Limpiar obj/ y compilar ────────────────────────────────────────────
echo -e "\n  Limpiando compilación anterior..."
make -C "$PRUEBA" clean 2>/dev/null || rm -rf "$PRUEBA/obj" && mkdir -p "$PRUEBA/obj"

echo -e "\n${G}${W}  Compilando $RUN ...${RS}"
if ! make -C "$PRUEBA"; then
  echo -e "\n  ${R}✗ compilación fallida.${RS}"; exit 1
fi
echo -e "  ${G}✓ compilación OK${RS}"

# ── 6. Lanzar en Caprice32 ────────────────────────────────────────────────
DSK="$PRUEBA/scene.dsk"
if [ ! -f "$DSK" ]; then
  DSK=$(find "$PRUEBA" -name "*.dsk" | head -1)
fi

echo -e "\n${G}${W}  Lanzando en Caprice32...${RS}"
if [ ! -x "$CAP32" ]; then
  echo -e "${Y}  cap32 no encontrado. DSK en: ${W}$DSK${RS}"; exit 1
fi
"$CAP32" "$DSK" -a 'run"SCENE.BIN'
