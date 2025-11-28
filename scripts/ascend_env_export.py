#!/usr/bin/env python3
"""
ascend_env_export.py

在当前机器上一键导出：
- Ascend / CANN / NPU / Python 环境报告（*.txt）
- 原始 pip freeze 结果（*_requirements_raw.txt）
- 尝试清洗后的 requirements.txt（*_requirements_clean.txt）

输出文件将写入仓库根目录下的 `env/snapshots/` 目录，
方便纳入版本管理，用于记录不同国产化环境（例如 910B2x + 鲲鹏 920）的配置。
"""

import argparse
import datetime
import io
import os
import platform
import re
import shutil
import subprocess
from textwrap import indent


def run(cmd, check=False, capture=True):
    """
    执行命令并返回 (ok, stdout_str)。
    不抛异常，方便“尽量多拿信息”。
    """
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.STDOUT if capture else None,
            text=True,
            check=check,
        )
        return True, (res.stdout or "")
    except Exception as e:
        return False, f"COMMAND FAILED: {' '.join(cmd)}\n{e}\n"


def detect_primary_card_id():
    """
    优先从 ASCEND_VISIBLE_DEVICES 里取一个卡 ID，
    没有的话默认 0。
    """
    env_val = os.environ.get("ASCEND_VISIBLE_DEVICES")
    if not env_val:
        return 0
    # 例如: "0", "0,1", "4"
    first = str(env_val).split(",")[0].strip()
    try:
        return int(first)
    except ValueError:
        return 0


def collect_env_report():
    """
    收集系统 + Ascend + CANN + 框架版本信息，
    返回文本字符串。
    """
    buf = io.StringIO()

    def log(s=""):
        print(s)
        buf.write(s + "\n")

    def print_section(title):
        log("\n" + "=" * 80)
        log(f"=== {title}")
        log("=" * 80)

    # -------- 基本系统信息 --------
    print_section("Basic system info")
    log(f"Hostname     : {platform.node()}")
    log(f"OS           : {platform.platform()}")
    log(f"Machine      : {platform.machine()}")
    log(f"Python exe   : {shutil.which('python') or shutil.which('python3')}")
    log(f"Python ver   : {platform.python_version()}")

    # -------- NPU / npu-smi --------
    print_section("Ascend NPU (npu-smi)")

    npu_smi = shutil.which("npu-smi")
    if not npu_smi:
        log("npu-smi not found in PATH，可能未安装 NPU 驱动或当前容器未挂载 npu-smi。")
    else:
        ok, out = run([npu_smi, "info"])
        log(">> npu-smi info")
        log(indent(out.strip() or "(no output)", "  "))

        # 额外：板卡信息（带 card id）
        card_id = detect_primary_card_id()
        log(f"\n>> npu-smi info -t board -i {card_id}")
        ok, out = run([npu_smi, "info", "-t", "board", "-i", str(card_id)])
        log(indent(out.strip() or "(no output)", "  "))

    # -------- CANN / Ascend Toolkit --------
    print_section("CANN / Ascend Toolkit version")

    candidate_files = []

    ascend_home = os.environ.get("ASCEND_TOOLKIT_HOME")
    if ascend_home:
        candidate_files.append(os.path.join(ascend_home, "version.cfg"))

    candidate_files.extend(
        [
            "/usr/local/Ascend/ascend-toolkit/latest/version.cfg",
            "/usr/local/Ascend/ascend-toolkit/version.cfg",
            "/usr/local/Ascend/latest/version.cfg",
        ]
    )

    seen = set()
    found_any = False
    for path in candidate_files:
        if not path or path in seen:
            continue
        seen.add(path)
        if os.path.isfile(path):
            found_any = True
            log(f">> Found CANN version file: {path}")
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().strip()
                log(indent(content if content else "(empty file)", "  "))
            except Exception as e:
                log(f"  (failed to read: {e})")

    if not found_any:
        log("未在常见路径下找到 CANN version.cfg，可手动检查 /usr/local/Ascend 下的安装结构。")

    # -------- Ascend/CANN 相关包（rpm / dpkg）--------
    log("\n>> Ascend / CANN related packages (rpm / dpkg)")

    if shutil.which("rpm"):
        ok, out = run(["rpm", "-qa"])
        if ok:
            lines = [
                l
                for l in out.splitlines()
                if any(k in l.lower() for k in ("ascend", "cann", "npu", "hccl"))
            ]
            if lines:
                log(indent("\n".join(lines), "  "))
            else:
                log("  rpm 中未找到与 Ascend/CANN 相关的包记录。")
        else:
            log(indent(out, "  "))
    elif shutil.which("dpkg"):
        ok, out = run(["dpkg", "-l"])
        if ok:
            lines = [
                l
                for l in out.splitlines()
                if any(k in l.lower() for k in ("ascend", "cann", "npu", "hccl"))
            ]
            if lines:
                log(indent("\n".join(lines), "  "))
            else:
                log("  dpkg 中未找到与 Ascend/CANN 相关的包记录。")
        else:
            log(indent(out, "  "))
    else:
        log("rpm / dpkg 都不存在（可能是容器精简镜像）。")

    # -------- 环境变量 --------
    print_section("Environment variables related to Ascend / CANN / HCCL")
    interesting_keys = []
    for k, v in os.environ.items():
        upper = k.upper()
        if any(p in upper for p in ("ASCEND", "CANN", "HCCL", "NPU", "ATLAS")):
            interesting_keys.append(f"{k}={v}")

    if interesting_keys:
        log(indent("\n".join(sorted(interesting_keys)), "  "))
    else:
        log("未发现明显与 Ascend 相关的环境变量。")

    # -------- Python 框架版本 --------
    print_section("Python AI framework versions (MindSpore / torch-npu / etc.)")

    def try_import(name, import_name=None):
        real_name = import_name or name
        try:
            mod = __import__(real_name)
            ver = getattr(mod, "__version__", "unknown")
            log(f"{name:12s}: {ver}")
        except Exception as e:
            log(f"{name:12s}: import failed: {e}")

    try_import("mindspore")
    try_import("torch")
    try_import("torch-npu", import_name="torch_npu")
    try_import("vllm")
    try_import("tensorflow")

    return buf.getvalue()


def get_pip_freeze():
    """
    调用 pip freeze，返回文本（可能为空）和命令输出状态。
    """
    py_exe = shutil.which("python") or shutil.which("python3")
    if not py_exe:
        return False, "未找到 python/python3，可执行文件不存在。"

    ok, out = run([py_exe, "-m", "pip", "freeze"])
    if not ok:
        return False, out or "pip freeze 调用失败。"
    return True, out.strip()


def clean_requirement_line(line: str) -> str:
    """
    尝试把 "pkg @ file:///.../pkg-0.1.0-py3-none-any.whl"
    转成 "pkg==0.1.0"；失败的话加上注释留给人类处理。
    其它行原样返回。
    """
    s = line.strip()
    if not s or s.startswith("#"):
        return s

    # editable 安装（-e git+...），原样保留
    if s.startswith("-e "):
        return s

    # 形如: pkgname @ file:///path/.../pkgname-0.1.0-py3-none-any.whl
    m = re.match(r"^([A-Za-z0-9_.\-]+)\s*@\s*file:///(.+)$", s)
    if not m:
        return s

    pkg_name = m.group(1)
    path_part = m.group(2)

    # 从路径里取出文件名
    m_file = re.search(r"/([^/]+)\.whl$", path_part)
    if not m_file:
        # 解析失败，加注释提醒人工处理
        return f"# FIXME: 手动处理这一行: {s}"

    filename = m_file.group(1)  # e.g. ascendctools-0.1.0-py3-none-any
    # 经验规则：第一个 '-' 前是包名，第二个 '-' 前是版本号
    parts = filename.split("-")
    if len(parts) < 2:
        return f"# FIXME: 手动处理这一行: {s}"

    version = parts[1]
    # 如果文件名里的包名和 pkg_name 不一致，也提醒一下
    file_pkg_name = parts[0]
    if file_pkg_name.lower() != pkg_name.lower():
        return f"# FIXME: 名字不一致，请核查: {s}"

    return f"{pkg_name}=={version}"


def build_clean_requirements(raw_freeze: str) -> str:
    """
    从 raw pip freeze 文本构造一个尽量可用的 requirements.txt 文本。
    """
    lines = raw_freeze.splitlines()
    out_lines = []
    out_lines.append("# Auto-generated requirements (cleaned from pip freeze)")
    out_lines.append("# 注意：带 FIXME 的行需要人工确认或替换为正确轮子来源。")
    out_lines.append("")

    for line in lines:
        cleaned = clean_requirement_line(line)
        out_lines.append(cleaned)

    return "\n".join(out_lines)


def main():
    parser = argparse.ArgumentParser(
        description="导出 Ascend/CANN 环境 & 生成 requirements 文件。"
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="ascend_env",
        help="输出文件名前缀（默认: ascend_env）",
    )
    args = parser.parse_args()

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{args.prefix}_{ts}"

    # 输出到仓库下的 env/snapshots 目录
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    snapshot_dir = os.path.join(repo_root, "env", "snapshots")
    os.makedirs(snapshot_dir, exist_ok=True)

    report_path = os.path.join(snapshot_dir, f"{base}_report.txt")
    raw_req_path = os.path.join(snapshot_dir, f"{base}_requirements_raw.txt")
    clean_req_path = os.path.join(snapshot_dir, f"{base}_requirements_clean.txt")

    # 1. 收集环境报告
    report_text = collect_env_report()

    # 2. pip freeze
    ok, freeze_text = get_pip_freeze()
    if ok:
        print("\n获取 pip freeze 成功。")
    else:
        print("\n获取 pip freeze 失败，将把错误信息写入 raw requirements 文件。")

    # 3. 生成 clean requirements
    if ok:
        clean_text = build_clean_requirements(freeze_text)
    else:
        clean_text = (
            "# 由于 pip freeze 失败，无法生成 requirements_clean，请先解决 pip 环境问题。\n"
        )

    # 4. 写文件
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"\n[OK] 环境报告已写入: {os.path.abspath(report_path)}")
    except Exception as e:
        print(f"\n[ERR] 写入环境报告失败: {e}")

    try:
        with open(raw_req_path, "w", encoding="utf-8") as f:
            f.write(freeze_text if ok else freeze_text)
        print(f"[OK] 原始 pip freeze 已写入: {os.path.abspath(raw_req_path)}")
    except Exception as e:
        print(f"[ERR] 写入原始 requirements 失败: {e}")

    try:
        with open(clean_req_path, "w", encoding="utf-8") as f:
            f.write(clean_text)
        print(f"[OK] 清洗后的 requirements 已写入: {os.path.abspath(clean_req_path)}")
    except Exception as e:
        print(f"[ERR] 写入清洗后的 requirements 失败: {e}")

    print("\n导出完成。建议：")
    print("1) 把 *_report.txt 连同 CANN 安装包/Ascend 安装目录一起备份；")
    print("2) 新机器上先对齐 CANN/驱动，再用 *_requirements_clean.txt 来装 Python 依赖；")
    print("3) 有 # FIXME 的行，需要你自己确认对应的 wheel 或安装方式。")


if __name__ == "__main__":
    main()

