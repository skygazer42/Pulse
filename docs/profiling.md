# Profiling 指南（占位）

## 昇腾（CANN Profiler）
1. 安装/启用 profiler 工具（`ascend-dmi`/`msprof` 与 CANN 版本匹配）。
2. 启动命令占位：
   ```bash
   # TODO: 将 CMD 替换为真实任务
   msprof --application="python examples/llm_hello_world.py --device ascend" \
          --output=benchmarks/profile/ascend_run1
   ```
   或使用包装脚本：`./scripts/profile_ascend.sh --cmd "<上面命令>"`
3. 关注指标：算子耗时 TopN、E2E latency、Host/Device overlap、HCCL 通信占比。
4. 产物归档：将 `.prof`/HTML/CSV 放入 `benchmarks/profile/`，并在 `benchmarks/README.md` 标注路径与配置。

## 摩尔线程（MT Profiler 占位）
1. 确认 MT Profiler 工具与驱动匹配。
2. 启动命令占位：
   ```bash
   ./scripts/profile_mthreads.sh --cmd "python examples/llm_hello_world.py --device mthreads"
   # TODO: 将脚本内部 eval 替换为实际 MT profiler 命令
   ```
3. 关注指标：算子/内存/调度时间线，通信与同步开销。

## 通用建议
- 固定随机种子、关闭动态 shape 以获得稳定的 profile。
- 与性能基线一起提交：`配置 + 日志 + profile 产物路径`。
## 提交物清单（建议）
- 运行命令、配置文件、硬件信息（写入 `benchmarks/README.md`）
- Profiling 产物路径
- 关键瓶颈摘要（前 3 算子/通信开销）***
