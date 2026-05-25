# E:\yolov11\train.py
from ultralytics import YOLO

# 使用模型名称自动下载权重（避免文件找不到错误）
model = YOLO("yolo11s.pt")  # yolov11 nano版本，适配6GB显存

# RTX 3060 6GB 专用训练配置（仅保留合法参数）
results = model.train(
    data="ultralytics/cfg/datasets/VisDrone.yaml",  # 数据集配置文件
    imgsz=640,  # 降低分辨率减少显存占用（6GB显存推荐512）
    batch=4,  # 6GB显存安全批次大小（核心优化）
    workers=0,  # Windows下禁用多进程，避免内存冲突
    epochs=150,  # 训练轮数
    device=0,  # 使用第0块GPU
    amp=True,  # 开启混合精度训练（关键！降低30%显存占用）
    patience=20,  # 早停耐心值，防止无效训练
)

# 可选：打印训练结果
print(f"训练完成！mAP50: {results.results_dict['metrics/mAP50(B)']:.3f}")
