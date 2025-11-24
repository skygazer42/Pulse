"""
最小可运行示例：验证推理链路是否贯通。
占位脚本，不依赖真实模型；可替换为具体框架调用。
"""

import argparse
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", default="qwen1.5-1.8b")
    parser.add_argument("--device", default="ascend", choices=["ascend", "mthreads", "cuda", "cpu"])
    parser.add_argument("--precision", default="bf16")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=64)
    return parser.parse_args()


def mock_generate(args):
    # 这里仅模拟加载与生成时间，避免真实依赖
    print(f"[load] model={args.model_name}, device={args.device}, precision={args.precision}")
    time.sleep(0.5)
    print(f"[generate] batch={args.batch_size}, max_length={args.max_length}")
    start = time.time()
    # 模拟生成
    time.sleep(0.8)
    elapsed = time.time() - start
    tokens = args.batch_size * args.max_length
    print(f"[result] tokens={tokens}, elapsed={elapsed:.3f}s, throughput={tokens/elapsed:.2f} tok/s")


def main():
    args = parse_args()
    mock_generate(args)


if __name__ == "__main__":
    main()
