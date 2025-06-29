# ✋ Hand Gesture Tracker

This project uses **MediaPipe** and **OpenCV** to track both hand in real time using your webcam. It detects finger positions and displays how many fingers are currently raised.

---

## 📸 Features

- Detects 2 hand using MediaPipe
- Labels each finger landmark in real time
- Counts number of raised fingers
- Displays results as overlay on live webcam feed

---

## 🛠 Requirements

Install dependencies with:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
