# Model Architecture & Navigation System

## YOLOv8 Segmentation-Based Navigation Model

VisualEyes uses a **YOLOv8 Segmentation model (`yolov8n-seg.pt`)** to perform real-time obstacle detection and intelligent navigation assistance for visually impaired users.

Unlike traditional object detection systems that only draw bounding boxes, the segmentation model generates **pixel-level object masks**, allowing the system to better understand which areas of the walking path are blocked.

---

# Why Segmentation Instead of Normal Detection?

Traditional object detection:

[ PERSON ]

Only provides rectangular bounding boxes.

Problem:

* Includes empty areas
* Poor obstacle occupancy understanding
* Weak navigation decisions

---

YOLOv8 Segmentation:

Exact shape of obstacle


Provides:

* Precise object masks
* Better path analysis
* More accurate obstacle avoidance
* Improved navigation guidance

This significantly improves real-time navigation accuracy.

---

# Navigation Workflow

Camera Frame
      ↓
YOLOv8 Segmentation
      ↓
Obstacle Filtering
      ↓
Region-Based Risk Analysis
      ↓
Navigation Decision
      ↓
Audio Guidance
```

---

# Obstacle Detection Pipeline

The system processes each frame in real-time using:

yolov8n-seg.pt


Detected obstacles are filtered using a custom obstacle list.

Only important navigation obstacles are considered:

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


This improves reliability by ignoring unnecessary objects such as:

* bottles
* spoons
* keyboards
* books

which do not significantly affect navigation.

---

# Region-Based Navigation Logic

The frame is divided into three regions:

```
| LEFT | CENTER | RIGHT |
```

The lower walking region of the frame is analyzed because it represents the user's path.

The system calculates obstacle occupancy separately for:

* Left side
* Center side
* Right side

The center region is treated as highly dangerous because it directly blocks movement.

---

# Risk Analysis System

Each obstacle contributes to a weighted risk score.

Different obstacle types are assigned different priorities.

Example:

| Object | Priority |
| ------ | -------- |
| Person | High     |
| Car    | High     |
| Bus    | High     |
| Chair  | Medium   |
| Dog    | Medium   |
| Plant  | Low      |

Weighted risks help the system make more intelligent navigation decisions.

---

# Navigation Decisions

The model generates navigation instructions such as:

| Situation             | Decision    |
| --------------------- | ----------- |
| Heavy center blockage | STOP        |
| Left side safer       | MOVE LEFT   |
| Right side safer      | MOVE RIGHT  |
| Path mostly clear     | GO STRAIGHT |

---

# Distance Estimation Logic

Instead of relying only on object height, the system estimates obstacle proximity using:

```
object_area = width × height
```

Larger segmented objects are considered closer obstacles.

This improves distance approximation stability.

---

# Audio Guidance System

The project includes an offline real-time audio assistant using:

```
pyttsx3
```

Example outputs:

* “Person ahead. Move right.”
* “Cow ahead. Stop.”
* “Path is clear.”

A cooldown mechanism prevents repetitive voice spam during live navigation.

---

# Real-Time Processing

The model supports:

* ESP32-CAM live streaming
* Laptop webcam live detection
* Real-time obstacle analysis
* Live navigation guidance
* Frontend streaming integration

---

# Files Added & Modified

## Added

### `path_navigation.py`

Handles:

* YOLOv8 segmentation
* Obstacle filtering
* Risk calculation
* Navigation decision logic
* Region analysis

---

### `generate_audio_1.py`

Handles:

* Offline text-to-speech
* Audio cooldown logic
* Real-time navigation speech

---

## Modified

### `main.py`

Updated to:

* Integrate segmentation-based navigation
* Support real-time audio guidance
* Stream processed frames
* Send navigation decisions to frontend

---

# Real-World Optimization

The obstacle system was designed considering real-world Indian street environments.

Special attention was given to:

* stray animals
* cows
* crowded pedestrian areas
* roadside obstacles
* vehicles

This makes the navigation system more practical for real-world deployment.

---

# Future Improvements

Planned future upgrades include:

* Depth estimation
* SLAM-based navigation
* Multi-object tracking
* Edge AI optimization
* Mobile deployment
* GPS-assisted navigation
* Custom-trained obstacle datasets
