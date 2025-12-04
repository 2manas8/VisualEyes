# VisualEyes
VisualEyes is a project focused on developing a smart, real-time object detection system using wearable technology. It creates a fully functional, highly accessible prototype to offer non-intrusive and reliable navigational assistance, thereby enhancing the mobility, safety, and independence of the visually impaired.

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
4. Make sure to update the `ESP32_CAM_URL` to the correct address in `main.py` and the device is connected to the same WiFi.

## 4. Running the System

1. Ensure the Node.js backend is running in Terminal A.
2. Run the Python detection script in Terminal B:
   ```bash
   python main.py
   ```
3. The system should open a window showing the live feed with bounding boxes around detected objects.