"""Training script for YOLOv11s with P2 head + SimAM attention on VisDrone2019."""

import multiprocessing
import random

import numpy as np
import torch

from ultralytics import YOLO


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    print(f"[OK] Random seed fixed to: {seed}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    set_seed(42)
    torch.cuda.empty_cache()

    print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")
    print(f"[INFO] VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

    model = YOLO("ultralytics/cfg/models/11/yolo11s-p2-simam.yaml")
    model.load("yolo11s.pt")

    results = model.train(
        data="VisDrone.yaml",
        epochs=150,
        batch=32,
        imgsz=640,
        device=0,
        workers=4,
        amp=True,
        optimizer="AdamW",
        lr0=0.001,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        mosaic=0.8,
        mixup=0.1,
        copy_paste=0.1,
        close_mosaic=15,
        patience=30,
        seed=42,
        plots=True,
        val=True,
        save=True,
    )

    print("\n[OK] Training complete!")
    print(f"[RESULT] mAP50: {results.results_dict['metrics/mAP50(B)']:.4f}")
    print(f"[RESULT] mAP50-95: {results.results_dict['metrics/mAP50-95(B)']:.4f}")
