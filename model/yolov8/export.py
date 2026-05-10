from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")

model.export(format="onnx")

print("Done. 'yolov8n-seg.pt' is ready.")