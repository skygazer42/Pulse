# 项目概览

本仓库聚焦“大模型在国产算力上的部署与落地”最佳实践，目标是提供一份可复制的操作手册与脚本集合，帮助团队在不同国产硬件上快速完成环境准备、功能验证与性能基线采集。

## 你能在这里找到什么
- 硬件差异说明：驱动/运行时版本、常见问题与解决方案（`docs/hardware-notes.md`）。
- 部署清单：从裸机到可跑通样例的逐步操作（`docs/deployment-checklist.md`）。
- 环境文件与脚本：虚拟环境、依赖、镜像构建与设备自检脚本（`env/`, `scripts/`）。
- 配置模板：不同硬件的模型/数据/优化参数示例（`configs/`）。
- 基线记录：吞吐、延迟与系统信息的标准化记录方式（`benchmarks/`）。
- 最小可运行示例：确保链路贯通的占位代码（`examples/`）。

## 使用建议
1. 按 `docs/deployment-checklist.md` 执行，确认驱动与运行时匹配。
2. 运行 `scripts/check_device.sh` 确认设备可见且无报错。
3. 使用 `scripts/prepare_env.sh <target>` 创建虚拟环境并安装对应依赖。
4. 根据硬件选择 `configs/*.yaml`，然后运行 `examples/llm_hello_world.py` 进行首包测试。
5. 将首轮性能数据写入 `benchmarks/README.md`，方便后续对比与优化。
