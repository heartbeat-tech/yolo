# 精简版 val.py - 仅终端显示指标，无任何保存逻辑
import warnings

from ultralytics import YOLO

warnings.filterwarnings("ignore")  # 忽略无关警告

# 核心：所有执行代码必须放在 if __name__ == '__main__': 内部
if __name__ == "__main__":
    # 1. 配置路径（替换为你自己的路径）
    MODEL_PATH = "runs/detect/train9/weights/best.pt"  # 你的best.pt路径
    DATA_YAML_PATH = "VisDrone.yaml"  # 你的数据集配置文件路径
    IMG_SIZE = 640  # 和训练时一致的图像尺寸
    BATCH_SIZE = 4  # 适配你的GPU显存（3060 Laptop建议≤6）
    DEVICE = 0  # 使用GPU 0，CPU写 "cpu"

    # 2. 加载模型
    print("正在加载模型...")
    model = YOLO(MODEL_PATH)
    print(f"模型加载完成：{model.model.__class__.__name__}")
    print(f"模型类别数：{len(model.names)}，类别名：{model.names}")

    # 3. 执行验证（关键：关闭多进程，避免Windows报错）
    print("\n开始评估模型性能...")
    results = model.val(
        data=DATA_YAML_PATH,
        split="test",  # 评估验证集
        imgsz=IMG_SIZE,  # 输入图像尺寸
        batch=BATCH_SIZE,  # 批次大小
        device=DEVICE,  # 设备
        workers=4,  # 核心修复：Windows下设为0，关闭多进程
        save_json=False,  # 关闭JSON保存
        plots=False,  # 关闭可视化图表生成（如需保留可改为True）
        verbose=True,  # 显示详细的类别指标
    )

    # 4. 提取并打印每个类别的mAP（mAP50-95）和mAP50
    print("\n=== 每个类别的详细指标 ===")
    for cls_id, cls_name in results.names.items():
        p = results.box.p[cls_id]  # 精确率(P)
        r = results.box.r[cls_id]  # 召回率(R)
        map50 = results.box.ap50[cls_id]  # mAP50
        map50_95 = results.box.ap[cls_id]  # mAP50-95
        print(f"类别 {cls_name}：P={p:.4f} | R={r:.4f} | mAP50={map50:.4f} | mAP50-95={map50_95:.4f}")

    # 5. 打印整体指标（修复属性名错误，使用正确的mp/mr）
    print("\n=== 模型整体性能指标 ===")
    print(f"整体平均精确率(P)：{results.box.mp:.4f}")
    print(f"整体平均召回率(R)：{results.box.mr:.4f}")
    print(f"整体mAP50：{results.box.map50:.4f}")
    print(f"整体mAP50-95：{results.box.map:.4f}")
    print("\n✅ 评估完成！")
