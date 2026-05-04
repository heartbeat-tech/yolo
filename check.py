import yaml

# 指定UTF-8编码打开文件
with open("ultralytics/cfg/models/11/yolo11-m.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
    print("✅ YAML加载成功！")
    print("backbone层数:", len(data['backbone']))
    print("head层数:", len(data['head']))