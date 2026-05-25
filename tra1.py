import multiprocessing
import random

import numpy as np
import torch

from ultralytics import YOLO


def set_seed(seed=42):
    """完整的随机种子设置."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    print(f"✅ 随机种子已固定为: {seed}")


if __name__ == "__main__":
    # 解决Windows多进程问题
    multiprocessing.freeze_support()

    # 固定随机种子
    set_seed(42)

    # 清空显存缓存
    torch.cuda.empty_cache()

    # 显示GPU信息
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✅ 显存总量: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

    # 加载模型
    # model = YOLO("ultralytics/cfg/models/11/yolo11s-SE.yaml")
    # model.load('yolo11s.pt')
    # 训练参数（保持你的主要设置）
    model = YOLO("yolo11s.pt")
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

    # 输出结果
    print("\n✅ 训练完成！")
    print(f"📊 mAP50: {results.results_dict['metrics/mAP50(B)']:.3f}")
