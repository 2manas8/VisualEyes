from ultralytics import YOLO

model = YOLO("yolov5nu.onnx") 

results = model.predict("E:\BTP\sample-videos\person-bicycle-car-detection.mp4", show=True)