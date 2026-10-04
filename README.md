# License Number Plate Recognition

A real-time license number plate recognition system using **YOLOv8** for license plate detection and **EasyOCR** for extracting the characters from the detected plate.

## 📌 Project Overview

The system processes a traffic video and automatically:

1. Detects the license plate using YOLOv8.
2. Crops the detected license plate.
3. Uses EasyOCR to recognize the characters.
4. Cleans and validates the OCR output using a regular expression.
5. Displays the detected license number on the video.

## 🛠️ Technologies Used

* Python
* OpenCV
* YOLOv8
* EasyOCR
* Ultralytics
* Regular Expressions (Regex)

## 🔄 System Workflow

```text
Traffic Video
     ↓
Frame Extraction
     ↓
YOLOv8 License Plate Detection
     ↓
License Plate Cropping
     ↓
Image Resizing
     ↓
EasyOCR
     ↓
Text Cleaning
     ↓
License Plate Format Validation
     ↓
Detected License Number
```

## 📂 Project Structure

```text
License-Number-Plate-Recognition/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   └── best.pt
│
└── videos/
    └── traffic.mp4
```

> `best.pt` and video files are excluded from GitHub using `.gitignore`.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Shyam-S7/License-Number-Plate-Recognition.git
cd License-Number-Plate-Recognition
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Project

Place the trained YOLO license plate model at:

```text
models/best.pt
```

Place the input traffic video at:

```text
videos/cmf.mp4
```

Then run:

```bash
python main.py
```

Press **Q** to stop the video.

## 🎯 Example Output

The system displays a green bounding box around the detected license plate and shows the recognized number above it.

Example:

```text
┌─────────────────┐
│   TN07CM2026    │
└─────────────────┘
```

Terminal output:

```text
Frame 160: TN07CM2026
Frame 165: TN07CM2026
Frame 200: TN07CM2026
```

## ⚡ Performance Optimization

The project processes every fifth frame:

```python
skip_frames = 5
```

This reduces CPU usage and improves processing speed.

YOLOv8 uses:

```python
conf=0.75
imgsz=1280
```

to maintain reliable license plate detection.

## 🧠 Why YOLOv8 + EasyOCR?

**YOLOv8** is used to detect **where the license plate is**.

**EasyOCR** is used to recognize **what characters are written on the plate**.

Therefore:

```text
YOLOv8 → WHERE?
EasyOCR → WHAT?
```

## ⚠️ Limitations

* OCR accuracy depends on image quality.
* Blurred or very small license plates may not be recognized correctly.
* Poor lighting and viewing angles can affect OCR performance.
* The system is optimized for CPU-based execution and may run slower without a GPU.

## 🚀 Future Improvements

* License plate tracking across multiple frames.
* Better OCR preprocessing.
* Support for multiple vehicles simultaneously.
* Real-time camera input.
* Database storage of detected license numbers.
* Timestamp and vehicle detection history.

## 👨‍💻 Author

**Shyam S7**

B.Tech – Artificial Intelligence & Data Science
