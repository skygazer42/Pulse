# 配置模板说明

> 以 YAML 为主，便于不同硬件/场景复用。建议每个配置文件包含 hardware / model / runtime / paths / logging 几段。

## 推荐字段
- `hardware`: 设备类型、并行度、精度、运行时版本（cann_version / mt_hip_version）
- `model`: 名称、精度、max_length、量化策略
- `runtime`: batch_size、num_workers、graph_mode / gradient_checkpointing / flash_attention 等
- `paths`: 权重、tokenizer、数据集路径
- `logging`: 日志目录、间隔、是否启用 tensorboard/wandb

## 使用示例
```bash
python examples/llm_hello_world.py \
  --device ascend \
  --batch-size 4 \
  --max-length 256 \
  --config configs/ascend-llm-example.yaml  # 如脚本支持
```

新增硬件时复制最近的示例文件并修改版本与并行策略，同时在 `docs/hardware-notes.md` 记录差异。***
