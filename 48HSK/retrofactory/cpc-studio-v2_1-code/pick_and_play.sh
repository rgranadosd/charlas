#!/usr/bin/env bash
# pick_and_play.sh
# 1. Lista los runs del pod cpc-pm
# 2. Descarga main.c (y audio.c/audio.h si existen) del run elegido
# 3. Los copia en pruebacpct/src/ (que ya tiene el Makefile local correcto)
# 4. Compila con make local
# 5. Lanza el DSK en Caprice32

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRUEBA="$SCRIPT_DIR/pruebacpct"
CAP32="$SCRIPT_DIR/cpctelera/tools/caprice32/cap32"
NS="dp-default-retro-factory-default-92f5b12e"
CONTEXT="k3d-amp-local"
LABEL="openchoreo.dev/component=cpc-pm"

G="\033[32m"; R="\033[31m"; Y="\033[33m"; B="\033[36m"; W="\033[1m"; RS="\033[0m"

echo -e "${B}${W}══════════════════════════════════════════${RS}"
echo -e "${B}${W}  CPC Studio — pick, compile & play${RS}"
echo -e "${B}${W}══════════════════════════════════════════${RS}\n"

# ── 1. Obtener pod ─────────────────────────────────────────────────────────
POD=$(kubectl get pod -n "$NS" --context "$CONTEXT" -l "$LABEL" \
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
    ls /app/scene_agent/outputs/ 2>/dev/null | sort -r | head -5 || true
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
read -rp "  Elige (1-${#RUNS[@]}) o Enter para el más reciente: " CHOICE
[ -z "$CHOICE" ] && CHOICE=1

if ! echo "$CHOICE" | grep -qE '^[0-9]+$' || \
   [ "$CHOICE" -lt 1 ] || [ "$CHOICE" -gt "${#RUNS[@]}" ]; then
  echo -e "${Y}  Opción no válida.${RS}"; exit 1
fi

RUN="${RUNS[$((CHOICE-1))]}"
POD_SRC="/app/scene_agent/outputs/$RUN/src"

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
