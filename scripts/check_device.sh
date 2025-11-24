#!/usr/bin/env bash
set -euo pipefail

# 简单的设备可见性与关键版本检查，适用于国产硬件适配的首轮自检。

echo "==> 基础信息"
uname -a
python --version || true

echo "==> 显卡/NPU 设备列表"
if command -v npu-smi >/dev/null 2>&1; then
  echo "[Ascend] npu-smi info"
  npu-smi info || true
fi

if command -v mt-smi >/dev/null 2>&1; then
  echo "[MThreads] mt-smi list"
  mt-smi list || true
fi

if command -v nvidia-smi >/dev/null 2>&1; then
  echo "[NVIDIA] nvidia-smi"
  nvidia-smi || true
fi

echo "==> 关键 Python 库"
python - <<'PY' || true
import sys
def try_import(name):
    try:
        mod = __import__(name)
        ver = getattr(mod, "__version__", "unknown")
        print(f"{name}: OK ({ver})")
    except Exception as e:
        print(f"{name}: FAILED ({e})")

for lib in ["torch", "torch_npu", "torch_mthreads", "transformers"]:
    try_import(lib)
PY

echo "==> 完成"
