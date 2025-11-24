#!/usr/bin/env bash
set -euo pipefail

# 摩尔线程 Profiling 占位脚本。
# 用法：
#   ./scripts/profile_mthreads.sh --cmd "python examples/llm_hello_world.py --device mthreads"

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

echo "==> MThreads Profiling (占位): ${CMD}"
# TODO: 替换为实际 profiler 命令
eval "${CMD}"
