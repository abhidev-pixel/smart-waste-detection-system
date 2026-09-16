from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="dataset/garbage_classification/data.yaml",
    epochs=10,
    imgsz=416,
    batch=4,
    device=0,
    workers=0,
    project="training/model",
    name="final",
    exist_ok=True
)
