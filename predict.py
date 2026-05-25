import multiprocessing

from ultralytics import YOLO

if __name__ == "__main__":
    multiprocessing.freeze_support()

    # 加载模型
    model = YOLO("runs/detect/train4/weights/best.pt")

    # 预测测试集图片并保存结果
    results = model.predict(
        source="visdrone2019/VisDrone2019-DET-test-dev/images",  # 测试集图片文件夹
        conf=0.25,
        iou=0.45,
        imgsz=640,
        device=0,
        save=True,  # 保存带框的图片
        save_txt=True,  # 保存txt标注
        project="runs/detect/predict_test",  # 结果保存目录
        name="exp",
        exist_ok=True,
    )
    print("预测结果保存在: runs/detect/predict_test/exp")
