# 部署检查清单

按顺序执行，建议在每个阶段记录时间与输出，便于排错。

## 0. 网络与镜像源
- [ ] 内网/外网策略确认：是否需要代理或白名单。
- [ ] Python / apt / pip 镜像源配置完毕。

## 1. 硬件与驱动
- [ ] 确认设备可见：`npu-smi info` / `mt-smi list` / `nvidia-smi`.
- [ ] 驱动与固件版本匹配：记录版本号并写入 `docs/hardware-notes.md`.
- [ ] 运行时库安装：CANN / MT-HIP / CUDA 均已安装且 ldconfig 可见。
- [ ] 基础算子/通信库：hccl / nccl / mpi 版本确认。

## 2. 系统与内核
- [ ] 内核版本满足官方要求；关闭不兼容的安全模块（如必要）。
- [ ] HugePage / NUMA / IRQ 亲和性已按指南配置。
- [ ] 时钟同步（NTP/Chrony）正常。

## 3. Python/依赖
- [ ] 创建隔离环境（venv/conda），已激活。
- [ ] 安装 `env/requirements-*.txt`，过程无报错。
- [ ] 验证关键依赖版本：`python - <<'PY' ...` 或 `python -c "import torch"`.

## 4. 存储与数据
- [ ] 数据集与权重路径已挂载/下载，读写测速满足要求。
- [ ] 确认路径权限与软硬链接策略。

## 5. 功能与性能冒烟
- [ ] 运行 `scripts/check_device.sh`，确保设备状态正常。
- [ ] 运行 `examples/llm_hello_world.py`，首包通过。
- [ ] 记录吞吐/延迟与系统信息，写入 `benchmarks/`.

## 6. 观测与告警（可选）
- [ ] 采集 GPU/NPU 指标（npu-smi/mt-smi 导出或 node_exporter）。
- [ ] 日志与指标接入 Prometheus/Grafana 或内部监控。

完成后，将本文件与 `docs/hardware-notes.md` 一同提交，保持信息可追溯。
