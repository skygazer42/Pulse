# 昇腾 910B2 × 鲲鹏 920 单卡部署流程

> 目标：从裸机/新容器环境出发，在昇腾 910B2 ×1 + 鲲鹏 920 上跑通 LLM 推理/训练最小链路，并记录一套可复用的国产化部署流程。
>
> 参考环境快照：`env/snapshots/ascend_910b2x-kunpeng920-1card_report.txt` 与对应的 `*_requirements_*.txt`。

## 0. 前置条件与规划

- OS：推荐 Ubuntu 22.04，aarch64 架构，内核版本满足 CANN 官方要求（示例为 `5.15.0-25-generic`）。
- 权限：具备 root 或等价权限以安装驱动、运行时与内核相关依赖。
- 网络：确认是否为离线/半离线环境，必要时参考 `docs/offline-install.md` 先完成依赖打包。
- 目录规划：
  - 代码：`/opt/projects/Pulse`（或团队约定目录）
  - 数据：`/data/datasets/...`
  - 权重：`/data/models/...`

## 1. 安装昇腾驱动与 CANN 运行时

1. 准备与 910B2 × 鲲鹏 920 匹配的驱动和 CANN 版本，建议与快照保持一致或更高：
   - 运行时示例：`runtime_installed_version=[7.7.0.1.238:8.1.RC1]`
   - HCCL 版本：参考快照中的 `hccl_installed_version`。
2. 按华为官方文档安装驱动与 CANN（runtime/toolkit）：
   - 驱动安装完成后，重启机器。
   - 安装 CANN runtime、toolkit，并确认 `/usr/local/Ascend/ascend-toolkit/latest` 路径存在。
3. 验证：
   - 运行：`npu-smi info`
   - 运行：`npu-smi info -t board -i <card_id>`（单卡示例为 `4`，实际以机房分配为准）。
   - 检查 `version.cfg`：`cat /usr/local/Ascend/ascend-toolkit/latest/version.cfg`
4. 环境变量：
   - 确认安装脚本已经配置：
     - `ASCEND_HOME_PATH=/usr/local/Ascend/ascend-toolkit/latest`
     - `ASCEND_TOOLKIT_HOME=/usr/local/Ascend/ascend-toolkit/latest`
     - `ASCEND_OPP_PATH=/usr/local/Ascend/ascend-toolkit/latest/opp`
   - 若存在多套 CANN，请在部署用户的 shell 配置中显式导出上述变量。

## 2. 系统层配置（内核 / HugePage / NUMA）

> 如已有统一的昇腾主机调优标准，可直接引用运维标准；以下为最小建议。

1. 内核参数：
   - 确认内核版本满足官方兼容矩阵；避免使用过旧或自定义补丁过多的内核。
   - 根据 CANN 文档配置内核参数（`/etc/sysctl.conf`），如：
     - `vm.nr_hugepages`
     - `kernel.shmmax` 等。
2. HugePage：
   - 为大模型推理/训练预留足够 HugePage，按模型规模计算；示例：
     - `vm.nr_hugepages=8192`（具体数值根据实际显存需求调优）。
3. NUMA 与 CPU 亲和性：
   - `numactl --hardware` 查看 NUMA 拓扑。
   - 优先将 NPU 绑到本地 NUMA 节点，避免跨 NUMA 带宽抖动。
4. 时钟同步：
   - 部署 `chrony` 或 NTP，保证时间一致性，方便日志与监控分析。

## 3. Python 环境与依赖安装

1. 克隆代码仓库（或从内网镜像同步）至目标路径，例如 `/opt/projects/Pulse`。
2. 使用虚拟环境（推荐 venv）：
   ```bash
   cd /opt/projects/Pulse
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```
3. 安装依赖（910B2 × 鲲鹏 920 单卡基线）：
   ```bash
   # 通用依赖
   python -m pip install -r env/requirements-base.txt

   # 昇腾特定依赖（基于当前快照整理）
   python -m pip install -r env/requirements-ascend.txt
   ```
4. 验证关键包版本：
   ```bash
   python - <<'PY'
   import torch
   import torch_npu
   import transformers
   print("torch:", torch.__version__)
   print("torch_npu:", torch_npu.__version__)
   print("transformers:", transformers.__version__)
   print("cuda/npu available:", torch.npu.is_available())
   PY
   ```
5. 若在离线环境，请先在有网机器按 `docs/offline-install.md` 中的流程下载 wheel 后，再在目标机使用 `--no-index --find-links` 安装。

## 4. 设备自检与最小示例

1. 确认设备可见：
   ```bash
   npu-smi info
   ```
2. 运行仓库内自检脚本：
   ```bash
   cd /opt/projects/Pulse
   source .venv/bin/activate
   ./scripts/check_device.sh
   ```
   - 检查点包括：
     - `npu-smi` 输出是否正常；
     - `python -c "import torch, torch_npu"` 是否成功；
     - `ASCEND_*` 环境变量是否就绪。
3. 运行 LLM 最小示例（以占位脚本为例，可根据实际修改）：
   ```bash
   python examples/llm_hello_world.py \
     --model-name qwen1.5-1.8b \
     --device ascend \
     --precision bf16
   ```
4. 若首包输出正常且无算子不支持报错，说明功能链路已打通。

## 5. 性能基线与配置参考

1. 确定模型与配置文件（示例）：
   - 模型：`qwen1.5-1.8b`
   - Ascend 配置：`configs/ascend-llm-example.yaml`（可按实际 batch / precision 调整）。
2. 运行基线脚本：
   ```bash
   ./scripts/benchmark_infer.sh \
     --device ascend \
     --config configs/ascend-llm-example.yaml \
     --repeat 3 \
     --batch 4 \
     --max-length 1024
   ```
3. 记录结果至 `benchmarks/README.md`：
   - 日期、设备（910B2 ×1 + 鲲鹏 920）、CANN 版本。
   - 模型、batch size、max length。
   - 吞吐（tokens/s）、首 token 延迟、平均延迟。
   - 是否开启 bf16、graph mode 等。
4. 若进行优化（绑核、图模式、静态 shape、算子白名单等），建议另存一条“优化后”记录，方便对比。

## 6. 环境快照与复用

> 本仓库已经提供环境导出脚本，便于在不同机房/版本之间对齐配置。

1. 在已调通的环境中执行：
   ```bash
   cd /opt/projects/Pulse
   source .venv/bin/activate
   python scripts/ascend_env_export.py --prefix ascend_910b2x-kunpeng920-1card
   ```
2. 输出会保存在：
   - `env/snapshots/ascend_910b2x-kunpeng920-1card_report.txt`
   - `env/snapshots/ascend_910b2x-kunpeng920-1card_requirements_raw.txt`
   - `env/snapshots/ascend_910b2x-kunpeng920-1card_requirements_clean.txt`
3. 将上述文件纳入版本管理，并在 `docs/hardware-notes.md` 中补充/更新对应条目，形成“环境 → 依赖 → 基线”的完整闭环。

## 7. 监控、日志与后续扩展

1. 监控建议（占位，详见 `docs/monitoring.md`）：
   - 使用 `npu-smi` 或 CANN 提供的监控接口采集：
     - NPU 利用率、HBM 显存、核心温度、功耗等。
   - 将指标接入 Prometheus/Grafana 或内部平台。
2. 日志：
   - 为训练/推理脚本统一配置日志路径，如 `/var/log/pulse/` 或项目内 `runs/ascend/`。
   - 建议按“日期/任务名/版本号”组织目录，便于回溯。
3. 多机/多卡扩展：
   - 参考 HCCL 官方文档配置 `HCCL_WHITELIST_DISABLE=1`、`HCCL_IF_NAME` 等变量。
   - 对应修改启动脚本与配置文件中的 `rank_size` 与分布式策略。

完成以上步骤后，即形成了一套围绕昇腾 910B2 × 鲲鹏 920 单卡的标准部署流程。后续如需适配其他国产算力（多卡、集群或不同型号），推荐复用本文件结构，新增对应的 `deploy-*.md` 文档。***

