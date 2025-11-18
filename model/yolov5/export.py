from ultralytics import YOLO

model = YOLO("yolov5nu.pt")

model.export(format="onnx")

print("Done. 'yolov8n.onnx' is ready.")