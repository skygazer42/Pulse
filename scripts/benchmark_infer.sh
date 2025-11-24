#!/usr/bin/env bash
set -euo pipefail

# 简单推理基线脚本占位：重复运行并统计平均吞吐。
# 用法：
#   ./scripts/benchmark_infer.sh --device ascend --repeat 3

DEVICE="ascend"
REPEAT=3
BATCH=4
MAX_LEN=256

while [[ $# -gt 0 ]]; do
  case "$1" in
    --device) DEVICE="$2"; shift 2 ;;
    --repeat) REPEAT="$2"; shift 2 ;;
    --batch) BATCH="$2"; shift 2 ;;
    --max-length) MAX_LEN="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

echo "==> Benchmark: device=${DEVICE}, repeat=${REPEAT}, batch=${BATCH}, max_length=${MAX_LEN}"

TOTAL=0
for i in $(seq 1 "${REPEAT}"); do
  echo "-- run ${i}/${REPEAT}"
  OUT=$(python examples/llm_hello_world.py \
    --device "${DEVICE}" \
    --batch-size "${BATCH}" \
    --max-length "${MAX_LEN}")
  echo "${OUT}"
  TP=$(echo "${OUT}" | awk -F'throughput=' '/throughput=/{print $2}' | sed 's/ tok\\/s//')
  TOTAL=$(python - <<PY
import sys
print(float("${TOTAL}") + float("${TP or 0}"))
PY
)
done

AVG=$(python - <<PY
print(round(float("${TOTAL}") / float("${REPEAT}"), 2))
PY
)
echo "平均吞吐: ${AVG} tok/s"
