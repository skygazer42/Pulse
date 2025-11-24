# 数据与权重管理（占位）

## 路径约定
- 数据集：`/data/datasets/<name>/`
- 权重：`/data/models/<model_name>/`
- 缓存：`~/.cache/huggingface/`（可重定向到本地高速盘）

## 下载与校验
- 优先内网镜像或对象存储；无网用离线包。
- 分片下载：`aria2c -x16 -s16 <url> --checksum=sha-256=<hash>`
- 合并与校验：`cat part* > file && sha256sum file`

## 权限与合规
- 为外部数据注明 License，避免混用不可商用数据。
- 数据/权重目录仅授予最小权限（典型：`chmod 750`，属组为训练账号组）。
- 敏感数据需脱敏，明确保存周期。

## 清理策略
- checkpoint 保留最近 N 份（如 3），其余按周清理。
- 定期清理 HF cache：`huggingface-cli cache delete --yes --retries 3`
- 磁盘余量保持 >20%，不足时优先清理临时数据与旧日志。
