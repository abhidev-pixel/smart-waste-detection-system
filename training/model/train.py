from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="dataset/garbage_classification/data.yaml",
    epochs=3,
    imgsz=416,
    batch=4,
    device="cpu",
    workers=2,
    project="training/model",
    name="sanity_test",
    exist_ok=True
)
