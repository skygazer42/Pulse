#!/usr/bin/env bash
set -euo pipefail

# 构建占位镜像，需按硬件修改 Dockerfile 与源。
# 用法：
#   ./scripts/docker_build.sh ascend
#   ./scripts/docker_build.sh mthreads

TARGET="${1:-}"
if [[ -z "${TARGET}" ]]; then
  echo "用法: $0 <ascend|mthreads|cuda>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "${TARGET}" in
  ascend) DOCKERFILE="${ROOT_DIR}/env/Dockerfile.ascend" ;;
  mthreads) DOCKERFILE="${ROOT_DIR}/env/Dockerfile.mthreads" ;;
  cuda) DOCKERFILE="${ROOT_DIR}/env/Dockerfile.cuda" ;;
  *)
    echo "未知目标: ${TARGET}"
    exit 1
    ;;
esac

TAG="pulse-${TARGET}:dev"
echo "==> build ${TAG} using ${DOCKERFILE}"
docker build -f "${DOCKERFILE}" -t "${TAG}" "${ROOT_DIR}"
echo "完成。运行示例： docker run --rm -it ${TAG} bash"
