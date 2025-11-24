# 监控与告警（占位）

## 采集
- 设备指标：`npu-smi --export` / `mt-smi --export`（占位），建议间隔 5s。
- 节点指标：node_exporter / telegraf。
- 应用指标：在训练/推理脚本中以 Prometheus 文本或自定义日志格式输出。

### Prometheus 抓取示例（占位）
```yaml
scrape_configs:
  - job_name: "pulse-device"
    static_configs:
      - targets: ["localhost:9100"]   # node_exporter
  - job_name: "pulse-app"
    static_configs:
      - targets: ["localhost:9400"]   # 应用自暴露端口
```

## 可视化
- Grafana 看板最低字段：吞吐、延迟、显存/显存利用率、功耗、温度、HCCL/NCCL 错误计数。
- 建议与 `benchmarks/` 基线对比显示“相对变化”。

## 告警阈值（示例）
- 显存利用率 > 95% 且持续 5 分钟
- GPU/NPU 温度 > 85°C
- 吞吐下降 > 20%（相对基线）
- HCCL/NCCL error_count > 0

将实际面板 JSON 与阈值策略放入 `benchmarks/monitoring/` 或内部链接。***
