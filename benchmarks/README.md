# 性能基线记录

> 建议每次环境或配置变化后更新，确保可追踪。

## 记录格式（示例）
- 日期：2025-11-24
- 硬件：昇腾 910B ×1，CANN 8.x
- 模型：qwen1.5-1.8b
- 配置：`configs/ascend-llm-example.yaml`
- 批大小：4
- 吞吐：XXX tokens/s
- 首 token 延迟：XXX ms
- 备注：开启 bf16，graph mode

## 对比建议
- 保留“基线”与“优化后”两组数据，使用同一数据与脚本。
- 记录驱动、固件、运行时版本变化。
- 将 profiling 报告路径或摘要附在备注中。
