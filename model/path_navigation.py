import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque

# =====================================================
# CONFIG
# =====================================================

MODEL_PATH = "yolov8n-seg.pt"

CONFIDENCE_THRESHOLD = 0.4

# Ignore tiny/far obstacles
AREA_THRESHOLD = 8000

# Very close obstacle threshold
CLOSE_AREA_THRESHOLD = 45000

# Center blockage threshold for STOP
CENTER_STOP_THRESHOLD = 15000

# If center occupancy below this → GO STRAIGHT
CENTER_OCCUPANCY_THRESHOLD = 0.25


# =====================================================
# OBSTACLE CLASSES
# =====================================================

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

# =====================================================
# OBJECT PRIORITY
# =====================================================

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

# =====================================================
# DIRECTION SMOOTHING
# =====================================================

direction_history = deque(maxlen=5)

# =====================================================
# LOAD MODEL
# =====================================================

print("Loading YOLOv8 Segmentation Model...")

model = YOLO(MODEL_PATH)

print("Model loaded successfully.")

# =====================================================
# MAIN NAVIGATION FUNCTION
# =====================================================

def process_navigation(frame):

    detected_objects = []

    h, w, _ = frame.shape

    # =================================================
    # NAVIGATION REGIONS
    # =================================================

    # Narrow center corridor
    center_width = int(w * 0.30)

    center_start = (w - center_width) // 2
    center_end = center_start + center_width

    # Lower walking region
    BOTTOM_REGION_START = int(h * 0.6)

    # =================================================
    # RISKS
    # =================================================

    left_risk = 0
    center_risk = 0
    right_risk = 0

    close_object_detected = False
    very_close_center = False

    # Total center pixels
    total_center_pixels = (
        (h - BOTTOM_REGION_START)
        * center_width
    )

    # =================================================
    # MODEL PREDICTION
    # =================================================

    results = model.predict(
        source=frame,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False
    )

    # =================================================
    # PROCESS DETECTIONS
    # =================================================

    if results[0].masks is not None:

        masks = results[0].masks.data.cpu().numpy()

        boxes = results[0].boxes.xyxy.cpu().numpy()

        for i, mask in enumerate(masks):

            x1, y1, x2, y2 = boxes[i]

            x1, y1, x2, y2 = map(
                int,
                [x1, y1, x2, y2]
            )

            # =================================================
            # OBJECT INFO
            # =================================================

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

            # =================================================
            # FILTER OBJECTS
            # =================================================

            if class_name not in OBSTACLE_CLASSES:

                continue

            # Ignore tiny/far objects
            if object_area < AREA_THRESHOLD:

                continue

            detected_objects.append(class_name)

            close_object_detected = True

            # =================================================
            # OBJECT PRIORITY
            # =================================================

            priority = OBJECT_PRIORITY.get(
                class_name,
                1
            )

            # =================================================
            # DRAW BOX
            # =================================================

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

            # =================================================
            # SEGMENTATION ANALYSIS
            # =================================================

            mask_resized = cv2.resize(
                mask,
                (w, h)
            )

            # Lower walking region only
            bottom_mask = mask_resized[
                BOTTOM_REGION_START:, :
            ]

            # =================================================
            # SPLIT REGIONS
            # =================================================

            left_region = bottom_mask[
                :,
                :center_start
            ]

            center_region = bottom_mask[
                :,
                center_start:center_end
            ]

            right_region = bottom_mask[
                :,
                center_end:
            ]

            # =================================================
            # PIXEL OCCUPANCY
            # =================================================

            left_pixels = np.sum(left_region)

            center_pixels = np.sum(center_region)

            right_pixels = np.sum(right_region)

            # =================================================
            # RISK CALCULATION
            # =================================================

            left_risk += (
                left_pixels * priority
            )

            center_risk += (
                center_pixels * priority
            )

            right_risk += (
                right_pixels * priority
            )

            # =================================================
            # STOP LOGIC
            # =================================================

            if (
                object_area > CLOSE_AREA_THRESHOLD
                and center_pixels > CENTER_STOP_THRESHOLD
            ):

                very_close_center = True

    # =================================================
    # CENTER OCCUPANCY RATIO
    # =================================================

        # Add these before the detection loop
    raw_center_pixels = 0

    # Inside the loop, after calculating center_pixels:
    raw_center_pixels += center_pixels

    # After the loop, calculate the true occupancy ratio:
    true_center_occupancy = (
        raw_center_pixels / total_center_pixels
        if total_center_pixels > 0
        else 0
    )


    # =================================================
    # DECISION LOGIC
    # =================================================

    if not close_object_detected:

        direction = "GO STRAIGHT"

    # elif very_close_center:

    #     direction = "STOP"

    # Center mostly clear
    elif (
        true_center_occupancy
        < CENTER_OCCUPANCY_THRESHOLD
    ):

        direction = "GO STRAIGHT"

    # Center blocked → choose safer side
    else:

        if left_risk < right_risk:

            direction = "MOVE LEFT"

        else:

            direction = "MOVE RIGHT"

    # =================================================
    # DIRECTION SMOOTHING
    # =================================================

    direction_history.append(direction)

    direction = max(
        set(direction_history),
        key=direction_history.count
    )

    # Remove duplicates
    detected_objects = list(
        set(detected_objects)
    )

    # =================================================
    # DEBUG INFO
    # =================================================

    print(
        f"Direction: {direction} | "
        f"Center Occupancy: "
        f"{true_center_occupancy:.2f} | "
        f"Objects: {detected_objects}"
    )

    # =================================================
    # VISUALIZATION
    # =================================================

    # Left boundary
    cv2.line(
        frame,
        (center_start, 0),
        (center_start, h),
        (255, 0, 0),
        2
    )

    # Right boundary
    cv2.line(
        frame,
        (center_end, 0),
        (center_end, h),
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

    # Risks
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
        f"C:{true_center_occupancy:.2f}",
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

    # =================================================
    # RETURN
    # =================================================

    return (
        frame,
        direction,
        detected_objects
    )