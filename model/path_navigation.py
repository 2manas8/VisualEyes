import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque

# ---------------- CONFIG ----------------

MODEL_PATH = "yolov8n-seg.pt"

CONFIDENCE_THRESHOLD = 0.4

# Ignore tiny/far obstacles
AREA_THRESHOLD = 8000

# Very close obstacle threshold
CLOSE_AREA_THRESHOLD = 45000

# Center blockage threshold
CENTER_STOP_THRESHOLD = 15000

# ---------------- OBSTACLE CLASSES ----------------

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

# ---------------- OBJECT PRIORITY ----------------

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

# ---------------- DIRECTION SMOOTHING ----------------

direction_history = deque(maxlen=5)

# ---------------- LOAD MODEL ----------------

print("Loading YOLOv8 Segmentation Model...")

model = YOLO(MODEL_PATH)

print("Model loaded successfully.")

# ---------------- MAIN NAVIGATION FUNCTION ----------------

def process_navigation(frame):

    detected_objects = []

    h, w, _ = frame.shape

    # Divide frame into 3 navigation regions
    third = w // 3

    # Analyze only lower walking region
    BOTTOM_REGION_START = int(h * 0.6)

    # Risk values
    left_risk = 0
    center_risk = 0
    right_risk = 0

    close_object_detected = False
    very_close_center = False

    # ---------------- MODEL PREDICTION ----------------

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

            x1, y1, x2, y2 = map(
                int,
                [x1, y1, x2, y2]
            )

            box_width = x2 - x1

            box_height = y2 - y1

            object_area = (
                box_width * box_height
            )

            class_id = int(
                results[0].boxes.cls[i]
            )

            class_name = model.names[class_id]

            confidence = float(
                results[0].boxes.conf[i]
            )

            # ---------------- FILTER OBJECTS ----------------

            if class_name not in OBSTACLE_CLASSES:

                continue

            # Ignore very small/far objects
            if object_area < AREA_THRESHOLD:

                continue

            detected_objects.append(class_name)

            close_object_detected = True

            # Object priority
            priority = OBJECT_PRIORITY.get(
                class_name,
                1
            )

            # ---------------- DRAW BOUNDING BOX ----------------

            label = (
                f"{class_name} "
                f"{confidence:.2f}"
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            (text_w, text_h), baseline = (
                cv2.getTextSize(
                    label,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    2
                )
            )

            cv2.rectangle(
                frame,
                (
                    x1,
                    max(0, y1 - text_h - 8)
                ),
                (
                    x1 + text_w,
                    y1
                ),
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

            # ---------------- SEGMENTATION ANALYSIS ----------------

            mask_resized = cv2.resize(
                mask,
                (w, h)
            )

            # Lower walking region only
            bottom_mask = mask_resized[
                BOTTOM_REGION_START:, :
            ]

            # Split into left/center/right
            left_region = bottom_mask[:, :third]

            center_region = bottom_mask[
                :,
                third:2 * third
            ]

            right_region = bottom_mask[
                :,
                2 * third:
            ]

            # Count occupied pixels
            left_pixels = np.sum(left_region)

            center_pixels = np.sum(center_region)

            right_pixels = np.sum(right_region)

            # Weighted risks
            left_risk += (
                left_pixels * priority
            )

            center_risk += (
                center_pixels * priority
            )

            right_risk += (
                right_pixels * priority
            )

            # ---------------- EMERGENCY STOP ----------------

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

    # ---------------- DIRECTION SMOOTHING ----------------

    direction_history.append(direction)

    direction = max(
        set(direction_history),
        key=direction_history.count
    )

    # Remove duplicate object names
    detected_objects = list(
        set(detected_objects)
    )

    # ---------------- DEBUG PRINT ----------------

    print(
        f"Direction: {direction} | "
        f"Objects: {detected_objects}"
    )

    # ---------------- VISUALIZATION ----------------

    # Left/Center/Right lines
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

    # Bottom navigation line
    cv2.line(
        frame,
        (0, BOTTOM_REGION_START),
        (w, BOTTOM_REGION_START),
        (0, 255, 255),
        2
    )

    # Risk display
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
        f"Direction: {direction}",
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        3
    )

    # ---------------- RETURN ----------------

    return (
        frame,
        direction,
        detected_objects
    )