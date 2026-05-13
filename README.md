# VisualEyes
VisualEyes is a project focused on developing a smart, real-time object detection system using wearable technology. It creates a fully functional, highly accessible prototype to offer non-intrusive and reliable navigational assistance, thereby enhancing the mobility, safety, and independence of the visually impaired.

---

# What's New

The project was upgraded from a basic object detection system into a real-time AI navigation assistant for visually impaired users.

The new system now includes:

- YOLOv8 Segmentation-based obstacle understanding
- Smart navigation decision system
- Region-based path analysis
- Audio guidance system
- Real-time obstacle avoidance
- ESP32-CAM + webcam support
- Risk-based navigation logic

Instead of only drawing bounding boxes around detected objects, the system now analyzes obstacle positions and provides real-time navigation instructions such as:

- "Person ahead. Move left."
- "Chair ahead. Stop."
- "Path is clear."

---

# Installation & Setup

Follow these steps to set up the **VisualEyes** system locally. The system consists of a Python script for real-time object detection and a Node.js backend for data handling and the user interface.


### Prerequisites:
- Python 3.8+ (and `pip`)
- Node.js (v14+ LTS recommended) and `npm`
- ESP32CAM and a programmer board

## 1. Clone the Repository

Start by cloning the project to your local machine:
```bash
git clone https://github.com/your-username/VisualEyes.git
cd VisualEyes
```

## 2. Backend Setup (Node.js)

The backend handles API requests and serves the front-end interface.

1. Navigate to the server directory:
   ```bash
   cd backend
   ```
2. Install the required dependencies:
   ```bash
   npm install
   ```
3. **Configuration:** Create a `.env` file in the `backend` folder and add your environment configurations:
   ```bash
   PORT = <your_port_number_here>
   DATABASE_URL = "<your_database_url_here>"
   ```
4. Start the server:
   ```bash
   npm start
   ```
   The server should now be running at `http://localhost:<your_port_number_here>`.

## 3. Object Detection Setup (Python)

The Python script utilizes computer vision libraries to detect objects and communicate with the backend.

1. Open a new terminal and navigate to the python scripts directory:
   ```bash
   cd ../model
   ```
2. Create a Virtual Environment (Recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate.bat
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Make sure to update the `ESP32_CAM_URL` and `SERVER_URL` to the correct addresses in `main.py` and the device is connected to the same WiFi.

# AI Navigation System

## YOLOv8 Segmentation Upgrade

The original system used standard object detection with bounding boxes.

The upgraded system now uses:

```python
yolov8n-seg.pt
```

which is a YOLOv8 segmentation model.

Unlike traditional object detection, segmentation generates precise object masks instead of only rectangular boxes.

This allows the system to:

* Understand obstacle occupancy
* Analyze blocked walking regions
* Detect safer navigation directions
* Improve obstacle avoidance accuracy

---

# Smart Navigation Logic

The frame is divided into three navigation regions:

```text
| LEFT | CENTER | RIGHT |
```

The lower walking region of the frame is analyzed to determine whether the path is blocked.

The system calculates obstacle risks separately for:

* Left region
* Center region
* Right region

The center region is treated as highly dangerous because it directly blocks the user's walking path.

---

# Obstacle Priority System

Different objects are assigned different navigation priorities.

Example:

| Object | Priority |
| ------ | -------- |
| Person | High     |
| Car    | High     |
| Bus    | High     |
| Chair  | Medium   |
| Dog    | Medium   |
| Plant  | Low      |

This improves real-world navigation performance.

---

# Audio Navigation Assistance

A real-time offline audio guidance system was implemented using:

```python
pyttsx3
```

The system generates navigation instructions such as:

* "Person ahead. Move right."
* "Cow ahead. Stop."
* "Path is clear."

A cooldown system prevents repetitive audio spam during live detection.

---

# New Files Added

## `path_navigation.py`

Handles:

* YOLOv8 segmentation
* Region analysis
* Risk calculation
* Navigation decision making
* Obstacle prioritization

---

## `generate_audio_1.py`

Handles:

* Offline text-to-speech
* Real-time audio guidance
* Smart audio cooldown system

---

# main.py Improvements

`main.py` was updated to:

* Integrate segmentation-based navigation
* Support audio guidance
* Stream processed frames
* Send navigation decisions to frontend
* Work with ESP32-CAM live feed

---

# Supported Navigation Obstacles

The system focuses on important real-world navigation obstacles:

```python
[
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
```

Special focus was given to Indian road and street environments where stray animals and crowded paths are common.

---

# System Workflow

```text
ESP32-CAM / Webcam
        ↓
main.py
        ↓
path_navigation.py
        ↓
YOLOv8 Segmentation
        ↓
Obstacle Risk Analysis
        ↓
Navigation Decision
        ↓
Audio Guidance
        ↓
Frontend Streaming
```

---

## 4. Running the System

1. Ensure the Node.js backend is running in Terminal A.
2. Run the Python detection script in Terminal B:
   ```bash
   python main.py
   ```
3. The system should open a live video window showing:

- Segmented obstacle detection
- Smart navigation guidance
- Region-based path analysis
- Real-time audio instructions
- Obstacle-aware movement suggestions

Example outputs:

- "Person ahead. Move left."
- "Chair ahead. Stop."
- "Path is clear."

---

# Future Improvements

Planned upgrades include:

- Depth estimation
- SLAM-based navigation
- Multi-object tracking
- Mobile deployment
- Edge AI optimization
- Indoor/outdoor adaptive navigation
- GPS integration
- Custom-trained navigation models

---

# Project Goal

VisualEyes aims to improve mobility assistance for visually impaired individuals using affordable AI-powered computer vision technology.
