# Pulse: 大模型国产化适配模板

本仓库旨在为国产算力（如华为昇腾、摩尔线程 GPU 等）上的大模型训练/推理提供一套可复用的脚手架与实践指南，帮助团队快速完成环境搭建、性能验证与工程落地。

## 功能定位
- 适配与封装：统一抽象昇腾 NPU、摩尔线程 GPU 等设备的启动、算子兼容、日志采集与监控。
- 训练与推理示例：提供主流模型（LLM/多模态）在国产硬件上的最小可运行示例与性能基线脚本。
- 工程实践：包含镜像构建、CI 校验、数据/权重管理、观测与告警的示例配置。

## 支持矩阵（初版）
| 领域 | 设备/框架 | 备注 |
| --- | --- | --- |
| 训练 | 昇腾 910B + Ascend CANN | 需要 CANN >= 8.x，开启混合精度 |
| 训练 | 摩尔线程 MTT S4000 + MT-HIP | 需要安装 MT-HIP 运行时与对应驱动 |
| 推理 | 昇腾/摩尔线程 + OpenVINO / TensorRT-LLM（若可用） | 结合自定义算子 |
> 后续可扩展至昆仑芯、寒武纪、海光 DCU 等；请在 `docs/hardware-notes.md` 中补充具体版本与差异。

## 目录结构（建议）
```
Pulse/
├── README.md
├── docs/                # 硬件与环境差异说明、FAQ
├── scripts/             # 一键拉起/测速脚本（训练、推理、profiling）
├── env/                 # 环境文件：conda、pip、dockerfile、驱动校验脚本
├── configs/             # 设备/模型/数据集配置模板
├── benchmarks/          # 性能基线记录与对比结果
├── examples/            # 最小可运行示例（LLM/多模态）
└── .github/workflows/   # CI：lint、单测、静态检查、镜像构建
```

## 快速开始
1) **准备依赖**
   - OS：建议 Ubuntu 22.04+，内核与驱动需满足对应硬件要求。  
   - Python ≥ 3.10；推荐使用 `conda` 或 `python -m venv` 管理。
   - 已安装设备驱动与运行时：Ascend CANN / MT-HIP；`npu-smi` 或 `mt-smi` 可正常查询设备。

2) **创建环境**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
# 占位：根据硬件选择安装依赖
pip install -r env/requirements-cuda.txt      # 若使用通用 GPU
pip install -r env/requirements-ascend.txt    # 若使用昇腾
pip install -r env/requirements-mthreads.txt  # 若使用摩尔线程
```

3) **校验设备**
```bash
# 昇腾
npu-smi info
# 摩尔线程
mt-smi list
```

4) **运行最小示例**
```bash
python examples/llm_hello_world.py \
  --model-name qwen1.5-1.8b \
  --device ascend \
  --precision bf16
```
> 以上为示例占位，请根据实际脚本命名与参数调整。

## 性能基线 & Benchmark
- 在 `benchmarks/` 维护按硬件、模型、batch size 的吞吐与延迟数据。
- 推荐记录：驱动版本、运行时版本、算子黑名单/白名单、混合精度策略、算子降级情况。
- 使用 `scripts/profile_*.sh` 统一生成 profiling 报告（如 CANN Profiler、Nsight、MT Profiler）。

## 开发规范
- 代码风格：Python 采用 `ruff` + `black`；Shell 采用 `shellcheck`。
- 提交前运行 `scripts/precommit.sh`（占位）以完成格式化、单测与静态检查。
- 对硬件特定变更，请在 PR 描述中标注设备型号、驱动/固件版本与复现指令。

## 贡献指南
1. Fork 后新建分支，避免直接推送 `main`。  
2. 变更需附带最小可复现示例或基线更新。  
3. 新增硬件适配请补充 `docs/hardware-notes.md` 与 `benchmarks/` 数据。  
4. 提交 PR 前确保本地 `pytest` 全量通过。  

## 路线图（示例）
- [ ] 昇腾 LLM 推理链路（CANN 8.x）最小样例
- [ ] 摩尔线程 GPU 训练示例（MT-HIP + FlashAttention 适配）
- [ ] 多模态模型（LLava/InternVL）在国产硬件的对齐与推理
- [ ] 基于 Prometheus/Grafana 的训练指标采集模板
- [ ] 镜像与包管理（Apt/Yum+内网源、私有镜像仓库）最佳实践

## 常见问题
- **驱动/固件不匹配**：先用官方诊断脚本；若版本不符请在 `docs/hardware-notes.md` 记录现象与修复步骤。  
- **算子不支持/性能退化**：尝试开启混合精度、算子替换或降级；查看对应硬件的算子白名单。  
- **内存不足**：启用张量并行/激活重计算/ZeRO；必要时使用蒸馏或量化。  

## 许可证
默认使用 `Apache-2.0`（可按团队要求调整）。在正式发布前，请确认依赖项的许可证兼容性。 
