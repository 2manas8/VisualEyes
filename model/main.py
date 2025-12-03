import cv2
from ultralytics import YOLO
import sys
import time
import socketio
import base64

ESP32_CAM_URL = "http://192.168.1.6:81/stream"
YOLO_MODEL_PATH = "yolov12/yolo12n.onnx"
CONFIDENCE_THRESHOLD = 0.40

SERVER_URL = "https://visualeyes.onrender.com"
ROOM_ID = "1"
SEND_INTERVAL = 5

sio = socketio.Client()

print(f"Loading YOLO model: {YOLO_MODEL_PATH}...")
try:
    model = YOLO(YOLO_MODEL_PATH)
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    print("Please ensure you have run 'pip install ultralytics'.")
    sys.exit(1)

@sio.event
def connect():
    print("Connected to WebSocket Server")
    sio.emit('joinRoom', ROOM_ID)

@sio.event
def disconnect():
    print("Disconnected from WebSocket Server")

def process_video_stream():
    try:
        print(f"Connecting to server at {SERVER_URL}...")
        sio.connect(SERVER_URL)
    except Exception as e:
        print(f"Could not connect to WebSocket server: {e}")
        print("Continuing with local video only...")
    print(f"Attempting to connect to video stream at: {ESP32_CAM_URL}")
    cap = cv2.VideoCapture(ESP32_CAM_URL)
    if not cap.isOpened():
        print("Error: Cannot open video stream.")
        return
    print("Connection successful. Starting object detection loop. Press 'q' to exit.")
    frame_count = 0
    start_time = time.time()
    last_ws_send_time = 0
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
        current_time = time.time()
        if current_time - last_ws_send_time >= SEND_INTERVAL:
            if sio.connected:
                try:
                    detected_objects = []
                    for box in results[0].boxes:
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        detected_objects.append(class_name)
                    _, buffer = cv2.imencode('.jpg', annotated_frame)
                    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                    base64_string = f"data:image/jpeg;base64,{jpg_as_text}"
                    sio.emit('sendFrame', {
                        'roomId': ROOM_ID,
                        'frame': base64_string,
                        'objects': detected_objects
                    })
                    print(f"Sent frame to server. Objects: {detected_objects}")
                    last_ws_send_time = current_time
                except Exception as e:
                    print(f"Error sending frame: {e}")
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