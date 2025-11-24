# 离线安装与内网交付（占位）

## 1. 依赖打包
- Python 依赖：`pip download -r env/requirements-ascend.txt -d wheelhouse/`
- 运行时包：准备对应硬件的驱动、CANN/MT-HIP 离线包。
- 镜像：在有网环境 `docker build` 后 `docker save > image.tar`，内网用 `docker load -i image.tar`。

## 2. 传输与验收
- 校验：`sha256sum wheelhouse/* image.tar driver*.run`
- 介质：U 盘/离线仓库，保证读写速度与剩余空间（建议冗余 10%+）。

## 3. 安装流程（建议顺序）
1) 安装驱动与运行时 → ldconfig 刷新  
2) 安装 Python 轮子：`pip install --no-index --find-links wheelhouse -r env/requirements-ascend.txt`  
3) 运行 `scripts/check_device.sh` 确认设备与库可见  
4) 运行 `examples/llm_hello_world.py` 完成冒烟  

## 4. 常见问题
- 证书与代理：内网主机缺 CA 时，pip 需 `--trusted-host` 或自建私有 PyPI。
- 内核符号缺失：驱动安装前确认内核头文件版本一致。
- 路径权限：wheelhouse/ 与 image.tar 应开放读权限给部署用户。
