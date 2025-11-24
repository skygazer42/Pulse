#!/usr/bin/env bash
set -euo pipefail

# 创建 Python 虚拟环境并安装对应硬件的依赖。
# 用法：
#   ./scripts/prepare_env.sh ascend     # 昇腾
#   ./scripts/prepare_env.sh mthreads   # 摩尔线程
#   ./scripts/prepare_env.sh cuda       # 通用 GPU

TARGET="${1:-}"
if [[ -z "${TARGET}" ]]; then
  echo "用法: $0 <ascend|mthreads|cuda>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

case "${TARGET}" in
  ascend) REQ="env/requirements-ascend.txt" ;;
  mthreads) REQ="env/requirements-mthreads.txt" ;;
  cuda) REQ="env/requirements-cuda.txt" ;;
  *)
    echo "未知目标: ${TARGET}. 请选择 ascend / mthreads / cuda"
    exit 1
    ;;
esac

REQ_PATH="${ROOT_DIR}/${REQ}"
if [[ ! -f "${REQ_PATH}" ]]; then
  echo "依赖文件不存在: ${REQ_PATH}"
  exit 1
fi

echo "==> 创建虚拟环境: ${VENV_DIR}"
python -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip

echo "==> 安装公共依赖"
python -m pip install -r "${ROOT_DIR}/env/requirements-base.txt"

echo "==> 安装硬件特定依赖: ${REQ}"
python -m pip install -r "${REQ_PATH}"

echo "完成。激活环境: source ${VENV_DIR}/bin/activate"
