import cv2
import sys
import time
import socketio
import base64
import requests

from path_navigation import process_navigation

# ---------------- CONFIG ----------------

ESP32_CAM_URL = ""
CAM_AVAILABLE = 0

SERVER_URL = "https://visualeyes.onrender.com"

IP_FETCH_ENDPOINT = "/api/stream/fetch_ip"

ROOM_ID = "1"

# Send updates faster for navigation
SEND_INTERVAL = 5

# ---------------- SOCKET IO ----------------

sio = socketio.Client()

# ---------------- SOCKET EVENTS ----------------


@sio.event
def connect():
    print("Connected to WebSocket Server")

    sio.emit("joinRoom", ROOM_ID)


@sio.event
def disconnect():
    print("Disconnected from WebSocket Server")


# ---------------- FETCH CAMERA URL ----------------


def fetch_stream_url():
    global ESP32_CAM_URL
    global CAM_AVAILABLE

    try:
        params = {"roomId": ROOM_ID}

        response = requests.get(SERVER_URL + IP_FETCH_ENDPOINT, params=params)

        if response.status_code == 200:
            data = response.json()

            ip_address = data.get("ip")

            ESP32_CAM_URL = "http://" + ip_address + ":81/stream"

            CAM_AVAILABLE = 1

            print(f"Camera URL: {ESP32_CAM_URL}")

        else:
            print(f"Error: Server returned status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")

        return None


# ---------------- MAIN VIDEO PROCESS ----------------


def process_video_stream():
    # Connect websocket
    try:
        print(f"Connecting to server at {SERVER_URL}...")

        sio.connect(SERVER_URL)

    except Exception as e:
        print(f"Could not connect to WebSocket server: {e}")

        return

    # Open ESP32 stream
    print(f"Attempting to connect to video stream at: {ESP32_CAM_URL}")

    cap = cv2.VideoCapture(ESP32_CAM_URL)

    if not cap.isOpened():
        print("Error: Cannot open video stream.")

        return

    print("Connection successful.\nStarting navigation system.\nPress 'q' to exit.")

    frame_count = 0

    start_time = time.time()

    last_ws_send_time = 0

    # ---------------- MAIN LOOP ----------------

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

        # ---------------- NAVIGATION PROCESS ----------------

        try:
            (annotated_frame, direction, detected_objects) = process_navigation(frame)

        except Exception as e:
            print(f"Navigation Error: {e}")

            continue

        # ---------------- FPS ----------------

        frame_count += 1

        elapsed_time = time.time() - start_time

        fps = frame_count / elapsed_time if elapsed_time > 0 else 0

        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        # ---------------- DISPLAY DIRECTION ----------------

        # cv2.putText(
        #     annotated_frame,
        #     f"Direction: {direction}",
        #     (20, 80),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.8,
        #     (0, 0, 255),
        #     2,
        # )

        # ---------------- WEBSOCKET SEND ----------------

        current_time = time.time()

        if current_time - last_ws_send_time >= SEND_INTERVAL:
            if sio.connected:
                try:
                    # Convert frame to jpg
                    _, buffer = cv2.imencode(".jpg", annotated_frame)

                    jpg_as_text = base64.b64encode(buffer).decode("utf-8")

                    # Send data to frontend
                    sio.emit(
                        "sendFrame",
                        {
                            "roomId": ROOM_ID,
                            "frame": jpg_as_text,
                            "objects": detected_objects,
                            "direction": direction,
                        },
                    )

                    print(
                        f"Sent frame | "
                        f"Objects: {detected_objects} | "
                        f"Direction: {direction}"
                    )

                    last_ws_send_time = current_time

                except Exception as e:
                    print(f"WebSocket Error: {e}")

        # ---------------- DISPLAY WINDOW ----------------

        cv2.imshow("VisualEyes Navigation System", annotated_frame)

        # Exit key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ---------------- CLEANUP ----------------

    cap.release()

    cv2.destroyAllWindows()

    sio.disconnect()


# ---------------- ENTRY POINT ----------------

if __name__ == "__main__":
    while CAM_AVAILABLE == 0:
        fetch_stream_url()

        if CAM_AVAILABLE == 0:
            time.sleep(2)

    process_video_stream()
