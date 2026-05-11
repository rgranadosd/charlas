#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# Massive Attack Demo — lanzador de servicios
# Servicio 1: deepface_analyzer.py  (massiveattack_env)
# Servicio 2: massive_attack_v3.py  (liveportrait_env)
# ─────────────────────────────────────────────────────────

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEEPFACE_VENV="$PROJECT_DIR/massiveattack_env"
DEEPFACE_SCRIPT="$PROJECT_DIR/deepface_analyzer.py"

LP_DIR="$PROJECT_DIR/LivePortrait"
LP_VENV="$LP_DIR/liveportrait_env"
LP_SCRIPT="$PROJECT_DIR/massive_attack_v3.py"

PROJECT_PROCESS_PATTERNS=(
  "$DEEPFACE_SCRIPT"
  "$LP_SCRIPT"
)

# ── Validaciones ──────────────────────────────────────────
for path in "$DEEPFACE_VENV" "$DEEPFACE_SCRIPT" "$LP_VENV" "$LP_DIR" "$LP_SCRIPT"; do
  [[ -e "$path" ]] || { echo "❌  No encontrado: $path"; exit 1; }
done

kill_existing_project_processes() {
  local found=0
  echo "🧹  Limpiando procesos previos del proyecto..."

  for pattern in "${PROJECT_PROCESS_PATTERNS[@]}"; do
    mapfile -t pids < <(pgrep -f "$pattern" || true)
    if [[ ${#pids[@]} -gt 0 ]]; then
      found=1
      echo "   · Terminando PIDs (${pattern##*/}): ${pids[*]}"
      kill "${pids[@]}" 2>/dev/null || true
    fi
  done

  sleep 1

  for pattern in "${PROJECT_PROCESS_PATTERNS[@]}"; do
    mapfile -t pids < <(pgrep -f "$pattern" || true)
    if [[ ${#pids[@]} -gt 0 ]]; then
      echo "   · Forzando cierre PIDs (${pattern##*/}): ${pids[*]}"
      kill -9 "${pids[@]}" 2>/dev/null || true
    fi
  done

  if [[ $found -eq 0 ]]; then
    echo "   · No había procesos previos."
  fi
}

kill_existing_project_processes

# ── Limpieza al salir (Ctrl+C o fin normal) ───────────────
PIDS=()
cleanup() {
  echo ""
  echo "⏹  Deteniendo servicios..."
  for pid in "${PIDS[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
  wait 2>/dev/null
  echo "✅  Listo."
}
trap cleanup EXIT INT TERM

# ── Servicio 1: DeepFace analyzer ────────────────────────
echo "▶  Iniciando DeepFace analyzer..."
(
  source "$DEEPFACE_VENV/bin/activate"
  python3 "$DEEPFACE_SCRIPT"
) &
PIDS+=($!)

# Pequeña pausa para que la cámara se inicialice antes del segundo proceso
sleep 2

# ── Servicio 2: Massive Attack v3 (LivePortrait) ─────────
echo "▶  Iniciando Massive Attack v3..."
(
  cd "$LP_DIR"
  source "$LP_VENV/bin/activate"
  PYTORCH_ENABLE_MPS_FALLBACK=1 python3 "$LP_SCRIPT"
) &
PIDS+=($!)

echo ""
echo "✅  Ambos servicios corriendo. Presiona Ctrl+C para parar todo."
echo ""

# Esperar a que ambos terminen
wait "${PIDS[@]}"
