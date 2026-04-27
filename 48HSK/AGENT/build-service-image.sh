#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_REF="${1:-rafa-agent:dev}"
CONTAINER_BUILDER="${CONTAINER_BUILDER:-}"
IMAGE_PLATFORM="${IMAGE_PLATFORM:-}"
NO_CACHE="${NO_CACHE:-false}"
K3D_CLUSTER_NAME="${K3D_CLUSTER_NAME:-}"

usage() {
    cat <<'EOF'
Uso:
  ./build-service-image.sh [imagen:tag]

Variables opcionales:
  CONTAINER_BUILDER   Builder a usar (podman o docker). Si no se define, autodetecta.
  IMAGE_PLATFORM      Plataforma opcional para el build, por ejemplo linux/arm64.
  NO_CACHE=true       Fuerza build sin cache.
  K3D_CLUSTER_NAME    Si se define, imprime el comando exacto de import para k3d.

Ejemplos:
  ./build-service-image.sh
  ./build-service-image.sh rafa-agent:dev
  CONTAINER_BUILDER=podman IMAGE_PLATFORM=linux/arm64 ./build-service-image.sh rafa-agent:dev
EOF
}

pick_builder() {
    if [[ -n "$CONTAINER_BUILDER" ]]; then
        if ! command -v "$CONTAINER_BUILDER" >/dev/null 2>&1; then
            echo "ERROR: builder no encontrado: $CONTAINER_BUILDER" >&2
            exit 1
        fi
        return
    fi

    if command -v podman >/dev/null 2>&1; then
        CONTAINER_BUILDER="podman"
        return
    fi

    if command -v docker >/dev/null 2>&1; then
        CONTAINER_BUILDER="docker"
        return
    fi

    echo "ERROR: no se encontró ni podman ni docker en PATH" >&2
    exit 1
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

pick_builder

build_args=(build --file "$SCRIPT_DIR/Dockerfile" --tag "$IMAGE_REF")

if [[ "$CONTAINER_BUILDER" == "podman" ]]; then
    build_args+=(--format docker)
fi

if [[ -n "$IMAGE_PLATFORM" ]]; then
    build_args+=(--platform "$IMAGE_PLATFORM")
fi

if [[ "$NO_CACHE" == "true" ]]; then
    build_args+=(--no-cache)
fi

build_args+=("$SCRIPT_DIR")

echo "==> Builder: $CONTAINER_BUILDER"
echo "==> Imagen:  $IMAGE_REF"
if [[ -n "$IMAGE_PLATFORM" ]]; then
    echo "==> Platform: $IMAGE_PLATFORM"
fi

"$CONTAINER_BUILDER" "${build_args[@]}"

echo
echo "Imagen generada correctamente: $IMAGE_REF"
if [[ -n "$K3D_CLUSTER_NAME" ]]; then
    echo "Siguiente paso: k3d image import $IMAGE_REF -c $K3D_CLUSTER_NAME"
else
    echo "Siguiente paso: k3d image import $IMAGE_REF -c <cluster-name>"
fi