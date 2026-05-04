# test_metrics.py - 完整测试指标
import os
import time

import numpy as np
import torch

from ultralytics import YOLO


def get_model_info(model_path):
    """获取模型参数量和结构信息."""
    model = YOLO(model_path)

    # 参数量
    params = sum(p.numel() for p in model.parameters()) / 1e6

    # 模型文件大小
    file_size = os.path.getsize(model_path) / (1024 * 1024)

    # 类别信息
    num_classes = len(model.names)
    class_names = model.names

    return {
        "model": model,
        "params": params,
        "file_size": file_size,
        "num_classes": num_classes,
        "class_names": class_names,
    }


def measure_fps(model, img_size=640, iterations=500, warmup=100):
    """测量FPS（纯推理速度）."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    # 创建随机输入
    dummy_input = torch.randn(1, 3, img_size, img_size).to(device)

    # 预热
    print(f"预热 {warmup} 次...")
    for _ in range(warmup):
        _ = model(dummy_input, verbose=False)

    # 正式测试
    print(f"测试 {iterations} 次...")
    torch.cuda.synchronize()
    times = []

    for i in range(iterations):
        start = time.time()
        _ = model(dummy_input, verbose=False)
        torch.cuda.synchronize()
        times.append((time.time() - start) * 1000)  # 毫秒

        if (i + 1) % 100 == 0:
            print(f"  已完成 {i + 1}/{iterations}")

    # 统计
    times = np.array(times)
    avg_time = np.mean(times)
    fps = 1000 / avg_time
    std_time = np.std(times)
    min_time = np.min(times)
    max_time = np.max(times)

    return {"avg_time": avg_time, "fps": fps, "std_time": std_time, "min_time": min_time, "max_time": max_time}


def measure_map(model, data_yaml, img_size=640, batch=8):
    """测量mAP精度."""
    print("\n开始评估mAP...")
    results = model.val(data=data_yaml, split="test", imgsz=img_size, batch=batch, device=0, workers=0, verbose=False)

    return {
        "map50": results.box.map50,
        "map50_95": results.box.map,
        "precision": results.box.mp,
        "recall": results.box.mr,
    }


if __name__ == "__main__":
    # ========== 配置 ==========
    MODEL_PATH = "runs/detect/train9/weights/best.pt"  # 你的模型路径
    DATA_YAML = "VisDrone.yaml"  # 数据集配置
    IMG_SIZE = 640
    BATCH_SIZE = 4

    print("=" * 60)
    print("模型综合测试指标")
    print("=" * 60)

    # 1. 模型基本信息
    print("\n📁 加载模型...")
    info = get_model_info(MODEL_PATH)
    model = info["model"]

    print(f"模型路径: {MODEL_PATH}")
    print(f"参数量: {info['params']:.2f} M")
    print(f"模型文件大小: {info['file_size']:.2f} MB")
    print(f"类别数: {info['num_classes']}")
    print(f"类别名: {info['class_names']}")

    # 2. 测量FPS
    print("\n⚡ 测量FPS...")
    fps_results = measure_fps(model, img_size=IMG_SIZE)

    # 3. 测量mAP
    map_results = measure_map(model, DATA_YAML, IMG_SIZE, BATCH_SIZE)

    # ========== 最终结果汇总 ==========
    print("\n" + "=" * 60)
    print("✅ 最终测试结果")
    print("=" * 60)

    print("\n📊 结构指标:")
    print(f"  参数量: {info['params']:.2f} M")
    print(f"  模型文件: {info['file_size']:.2f} MB")

    print("\n⚡ 速度指标:")
    print(f"  平均推理时间: {fps_results['avg_time']:.2f} ms")
    print(f"  FPS: {fps_results['fps']:.1f}")
    print(f"  标准差: {fps_results['std_time']:.2f} ms")
    print(f"  最小/最大: {fps_results['min_time']:.2f}/{fps_results['max_time']:.2f} ms")

    print("\n🎯 精度指标:")
    print(f"  mAP50: {map_results['map50']:.4f}")
    print(f"  mAP50-95: {map_results['map50_95']:.4f}")
    print(f"  精确率(P): {map_results['precision']:.4f}")
    print(f"  召回率(R): {map_results['recall']:.4f}")

    # 论文表格格式
    print("\n" + "=" * 60)
    print("📈 论文表格格式")
    print("=" * 60)
    print("参数量(M) | FPS  | mAP50 | mAP50-95")
    print(
        f"{info['params']:.2f}     | {fps_results['fps']:.1f} | {map_results['map50']:.4f} | {map_results['map50_95']:.4f}"
    )
    print("=" * 60)
