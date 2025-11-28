# 硬件与软件差异记录模板

> 按设备型号填写，保持信息最新；遇到问题请记录“现象/原因/解决”三栏，便于复现与回溯。

## 记录表
| 字段 | 内容 |
| --- | --- |
| 设备型号 | 例：昇腾 910B / 摩尔线程 S4000 |
| 驱动版本 | 例：CANN 8.0.RC1 / MT-HIP 2.0.x |
| 固件版本 | 例：A2.x.x |
| 内核与 OS | 例：Ubuntu 22.04, 5.15 内核 |
| 关键库 | 例：torch 2.2.* + torch_npu，flash-attn 分支 |
| 编译器 | 例：gcc 9 / clang 16 |
| 已知限制 | 例：特定算子降级、最大 batch 限制 |
| 诊断命令 | 例：`npu-smi info` / `mt-smi list` |
| 参考文档 | 官网链接或内部 Wiki |

## 常见问题示例
- 显存占用异常：检查 mixed precision / gradient checkpointing 设置。
- 算子不支持：尝试降低精度或开启算子替换开关；记录替换列表。
- 通信相关性能抖动：核对 NIC 固件与 L1/L2 拓扑，评估需要的绑核与 NUMA 亲和策略。

## 示例：昇腾 910B2 ×1 + 鲲鹏 920

| 字段 | 内容 |
| --- | --- |
| 设备型号 | 昇腾 910B2 ×1 + 鲲鹏 920 |
| 驱动版本 | CANN runtime 7.7.0.1.238 / 8.1.RC1（参考 `env/snapshots/ascend_910b2x-kunpeng920-1card_report.txt`） |
| 固件版本 | 7.7.0.6.236 |
| 内核与 OS | Ubuntu 22.04, Linux 5.15.0-25-generic (aarch64) |
| 关键库 | torch 2.5.1 + torch-npu 2.5.1（详见 `env/requirements-ascend.txt`） |
| 编译器 | （参考 CANN 安装环境，待补充） |
| 已知限制 | 暂无（根据实际测试补充） |
| 诊断命令 | `npu-smi info`、`npu-smi info -t board -i 4` |
| 参考文档 | `env/snapshots/ascend_910b2x-kunpeng920-1card_report.txt`、`env/snapshots/ascend_910b2x-kunpeng920-1card_requirements_clean.txt` |
