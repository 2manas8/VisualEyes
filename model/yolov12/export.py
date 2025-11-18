from ultralytics import YOLO

model = YOLO("yolo12n.pt")

model.export(format="onnx")

print("Done. 'yolov12n.onnx' is ready.")