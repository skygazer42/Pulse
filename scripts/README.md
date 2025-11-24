# 脚本说明

| 脚本 | 功能 | 关键参数 | 备注 |
| --- | --- | --- | --- |
| `prepare_env.sh` | 创建虚拟环境并安装依赖 | `<ascend|mthreads|cuda>` | 读取 `env/requirements-*.txt` |
| `check_device.sh` | 设备可见性与关键库自检 | 无 | 需 `npu-smi` / `mt-smi` / `nvidia-smi` |
| `benchmark_infer.sh` | 简单推理吞吐基线 | `--device` `--repeat` `--batch` `--max-length` | 依赖 `examples/llm_hello_world.py` |
| `profile_ascend.sh` | Ascend profiling 占位 | `--cmd "<实际命令>"` | 替换为真实 msprof/ascend-dmi 调用 |
| `profile_mthreads.sh` | MThreads profiling 占位 | `--cmd "<实际命令>"` | 替换为实际 profiler 调用 |
| `docker_build.sh` | 构建占位镜像 | `<ascend|mthreads|cuda>` | 使用 `env/Dockerfile.*` |

## 快速用例
- 创建环境（昇腾）：`./scripts/prepare_env.sh ascend`
- 自检：`./scripts/check_device.sh`
- 推理基线：`./scripts/benchmark_infer.sh --device ascend --repeat 3`
- Profiling 占位：`./scripts/profile_ascend.sh --cmd "python examples/llm_hello_world.py --device ascend"`
- 构建镜像：`./scripts/docker_build.sh ascend`

> 运行前可 `chmod +x scripts/*.sh`（已设好权限）。***
