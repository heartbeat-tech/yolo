import multiprocessing
import random

import numpy as np
import torch

from ultralytics import YOLO


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    print(f"✅ 随机种子已固定为: {seed}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    set_seed(42)
    torch.cuda.empty_cache()

    # 加载模型
    model = YOLO("yolo11s.pt")

    # ⭐ 无数据增强训练配置
    results = model.train(
        data="VisDrone.yaml",
        epochs=150,
        batch=4,  # 先保持8，观察显存
        imgsz=640,
        device=0,
        workers=4,  # 如果不稳，降到2
        amp=True,
        optimizer="AdamW",
        lr0=0.002,  # 稍微提高一点
        mosaic=0.8,
        mixup=0.2,
        copy_paste=0.2,
        close_mosaic=15,
        patience=30,
        seed=42,  # 双重保险
        deterministic=True,  # 增加确定性模式
        plots=True,  # 画训练曲线
    )

    print("\n✅ 训练完成！")
    print(f"📊 mAP50: {results.results_dict['metrics/mAP50(B)']:.3f}")
