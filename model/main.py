import cv2
from ultralytics import YOLO
import sys
import time

ESP32_CAM_URL = 'http://192.168.1.6:81/stream'
YOLO_MODEL_PATH = 'yolov12/yolo12n.onnx'
CONFIDENCE_THRESHOLD = 0.40

print(f"Loading YOLO model: {YOLO_MODEL_PATH}...")
try:
    model = YOLO(YOLO_MODEL_PATH)
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    print("Please ensure you have run 'pip install ultralytics'.")
    sys.exit(1)


def process_video_stream():
    print(f"Attempting to connect to video stream at: {ESP32_CAM_URL}")
    cap = cv2.VideoCapture(ESP32_CAM_URL)

    if not cap.isOpened():
        print("Error: Cannot open video stream.")
        print("1. Check if the ESP32-CAM IP address is correct.")
        print("2. Verify the ESP32-CAM is running the CameraWebServer sketch.")
        print("3. Check firewall settings on your PC.")
        return

    print("Connection successful. Starting object detection loop. Press 'q' to exit.")
    
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to read frame from stream. Reconnecting...")
            cap.release()
            time.sleep(2)
            cap = cv2.VideoCapture(ESP32_CAM_URL)
            if not cap.isOpened():
                print("Reconnection failed. Exiting.")
                break
            continue

        results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

        annotated_frame = results[0].plot()

        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("ESP32-CAM YOLOv8 Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    process_video_stream()