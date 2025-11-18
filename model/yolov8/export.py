from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.export(format="onnx")

print("Done. 'yolov8n.onnx' is ready.")