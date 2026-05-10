import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque
from generate_audio_1 import speak

# ---------------- CONFIG ----------------

MODEL_PATH = "yolov8n-seg.pt"

CONFIDENCE_THRESHOLD = 0.4

# Object area thresholds
AREA_THRESHOLD = 12000
CLOSE_AREA_THRESHOLD = 45000

# Center stop threshold
CENTER_STOP_THRESHOLD = 15000

# Only these objects are considered obstacles
OBSTACLE_CLASSES = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "bus",
    "truck",
    "bench",
    "chair",
    "dog",
    "cow",
    "horse",
    "potted plant",
    "dining table",
    "couch"
]

# Object priorities
OBJECT_PRIORITY = {
    "person": 5,
    "car": 5,
    "bus": 5,
    "truck": 5,

    "motorcycle": 4,
    "bicycle": 4,

    "cow": 4,
    "horse": 4,

    "chair": 3,
    "bench": 3,
    "couch": 3,
    "dining table": 3,

    "dog": 2,
    "potted plant": 1
}

# Direction smoothing
direction_history = deque(maxlen=5)

# ---------------- LOAD MODEL ----------------

print("Loading segmentation model...")
model = YOLO(MODEL_PATH)

print("Model loaded successfully.")

# ---------------- MAIN FUNCTION ----------------

def process_navigation(frame):

    detected_objects = []

    h, w, _ = frame.shape

    # Divide frame into 3 regions
    third = w // 3

    # Only lower walking region matters
    BOTTOM_REGION_START = int(h * 0.6)

    # Risks
    left_risk = 0
    center_risk = 0
    right_risk = 0

    close_object_detected = False
    very_close_center = False

    # Track main obstacle
    main_object = None
    main_object_area = 0

    # ---------------- PREDICTION ----------------

    results = model.predict(
        source=frame,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False
    )

    # ---------------- PROCESS DETECTIONS ----------------

    if results[0].masks is not None:

        masks = results[0].masks.data.cpu().numpy()
        boxes = results[0].boxes.xyxy.cpu().numpy()

        for i, mask in enumerate(masks):

            x1, y1, x2, y2 = boxes[i]

            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            box_width = x2 - x1
            box_height = y2 - y1

            object_area = box_width * box_height

            class_id = int(results[0].boxes.cls[i])
            class_name = model.names[class_id]

            confidence = float(results[0].boxes.conf[i])

            # Ignore non-obstacle objects
            if class_name not in OBSTACLE_CLASSES:
                continue

            # Ignore very small/far objects
            if object_area < AREA_THRESHOLD:
                continue

            detected_objects.append(class_name)

            close_object_detected = True

            # Track nearest/largest obstacle
            if object_area > main_object_area:
                main_object_area = object_area
                main_object = class_name

            # Priority weight
            priority = OBJECT_PRIORITY.get(class_name, 1)

            # ---------------- DRAWING ----------------

            label = (
                f"{class_name} "
                f"{confidence:.2f} "
                f"| Area:{object_area}"
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            (text_w, text_h), baseline = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )

            cv2.rectangle(
                frame,
                (x1, max(0, y1 - text_h - 8)),
                (x1 + text_w, y1),
                (0, 255, 0),
                -1
            )

            cv2.putText(
                frame,
                label,
                (x1, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )

            # ---------------- SEGMENTATION ----------------

            mask_resized = cv2.resize(mask, (w, h))

            # Use only lower walking region
            bottom_mask = mask_resized[BOTTOM_REGION_START:, :]

            # Split regions
            left_region = bottom_mask[:, :third]
            center_region = bottom_mask[:, third:2 * third]
            right_region = bottom_mask[:, 2 * third:]

            # Count occupied pixels
            left_pixels = np.sum(left_region)
            center_pixels = np.sum(center_region)
            right_pixels = np.sum(right_region)

            # Weighted risks
            left_risk += left_pixels * priority
            center_risk += center_pixels * priority
            right_risk += right_pixels * priority

            # Emergency stop condition
            if (
                object_area > CLOSE_AREA_THRESHOLD
                and center_pixels > CENTER_STOP_THRESHOLD
            ):
                very_close_center = True

    # ---------------- DECISION LOGIC ----------------

    # Center is more dangerous
    center_risk *= 2

    if not close_object_detected:

        direction = "GO STRAIGHT"

    elif very_close_center:

        direction = "STOP"

    else:

        # Choose safer side
        if left_risk < right_risk:

            direction = "MOVE LEFT"

        elif right_risk < left_risk:

            direction = "MOVE RIGHT"

        else:

            direction = "GO STRAIGHT"

    # ---------------- SMOOTHING ----------------

    direction_history.append(direction)

    direction = max(
        set(direction_history),
        key=direction_history.count
    )

    # ---------------- AUDIO MESSAGE ----------------

    if main_object is not None:

        if direction == "STOP":
            audio_message = f"{main_object} ahead. Stop."

        elif direction == "MOVE LEFT":
            audio_message = f"{main_object} ahead. Move left."

        elif direction == "MOVE RIGHT":
            audio_message = f"{main_object} ahead. Move right."

        else:
            audio_message = f"{main_object} detected. Go straight."

    else:

        audio_message = "Path is clear."

    print("Decision:", audio_message)

    # Speak audio
    speak(audio_message)

    # ---------------- VISUALIZATION ----------------

    # Region lines
    cv2.line(
        frame,
        (third, 0),
        (third, h),
        (255, 0, 0),
        2
    )

    cv2.line(
        frame,
        (2 * third, 0),
        (2 * third, h),
        (255, 0, 0),
        2
    )

    # Bottom navigation region
    cv2.line(
        frame,
        (0, BOTTOM_REGION_START),
        (w, BOTTOM_REGION_START),
        (0, 255, 255),
        2
    )

    # Show risks
    cv2.putText(
        frame,
        f"L:{int(left_risk)}",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"C:{int(center_risk)}",
        (50, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"R:{int(right_risk)}",
        (50, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # Final direction
    cv2.putText(
        frame,
        audio_message,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        3
    )

    return (
        frame,
        direction,
        audio_message,
        detected_objects
    )