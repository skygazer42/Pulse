#!/usr/bin/env bash
set -euo pipefail

# Ascend Profiling 占位脚本。
# 用法示例：
#   ./scripts/profile_ascend.sh --cmd "python examples/llm_hello_world.py --device ascend"

CMD=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --cmd)
      CMD="$2"
      shift 2
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

if [[ -z "${CMD}" ]]; then
  echo "必须指定 --cmd \"<要执行的命令>\""
  exit 1
fi

echo "==> Ascend Profiling (占位): ${CMD}"
# TODO: 将下方替换为实际的 msprof/ascend-dmi 调用
# msprof --application="${CMD}" --output=./benchmarks/profile/ascend
eval "${CMD}"
