# HeadScript 🎯

Control your computer with your head. No special hardware required — just a standard webcam.

NosePilot uses MediaPipe's Face Landmarker to track 478 facial landmarks in real time, using head pose and eye gestures to move your cursor, click, scroll, and more — entirely hands-free.

---

## Features

- **Head-based cursor control** — turn your head to move the cursor across the screen
- **Left click** — wink your left eye
- **Right click** — wink your right eye
- **Scroll** — tilt your head up or down
- **Freeze mode** — hold both eyes closed for ~1 second to pause/resume cursor control
- **Calibration** — quick 4-point calibration on startup to personalise tracking to your face and setup
- **Live overlay** — real-time gesture and freeze state feedback on the webcam feed

---

## Project Structure

```
head_script/
│
├── main.py                  # Entry point — webcam loop and orchestration
├── face_landmarker.py       # MediaPipe Face Landmarker setup and detection
├── eye_utils.py             # EAR (Eye Aspect Ratio) calculation
├── gaze.py                  # Head pose tracking via nose tip position
├── gestures.py              # Blink, wink, and freeze state machine
├── cursor.py                # Cursor movement, clicks, scroll, calibration
├── visualizer.py            # Landmark drawing and overlay rendering
│
├── models/
│   └── face_landmarker.task # MediaPipe model file (download separately)
│
└── requirements.txt
```

---

## Installation

**1 — Clone the repository**
```bash
git clone https://github.com/shreyans-gits/head_script
cd head_script
```

**2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**3 — Download the MediaPipe model**

Download `face_landmarker.task` from the link below and place it in the `models/` folder:

```
https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task
```

---

## How to Run

```bash
python main.py
```

---

## Calibration

On startup, a calibration screen will appear. Follow the on-screen instructions:

1. Look at the **top-left** corner of your screen and press `SPACE`
2. Look at the **top-right** corner and press `SPACE`
3. Look at the **bottom-left** corner and press `SPACE`
4. Look at the **bottom-right** corner and press `SPACE`

> Tip: Don't just move your eyes — slightly turn your head toward each corner for best results.

Calibration takes about 10 seconds and only needs to be done once per session.

---

## Controls

| Action | Gesture |
|---|---|
| Move cursor | Turn head left / right / up / down |
| Left click | Wink right eye |
| Right click | Wink left eye |
| Scroll up | Tilt head up |
| Scroll down | Tilt head down |
| Freeze / unfreeze cursor | Hold both eyes closed for ~1 second |
| Quit | Press `Q` |

---

## Known Limitations

- **Glasses** — reflective lenses can affect iris landmark detection. Cursor control still works well since it relies on head pose rather than iris tracking.
- **Lighting** — works best in consistent, well-lit environments. Strong backlighting or shadows on the face reduce detection stability.
- **Scroll requires focus** — the scroll gesture fires at the current cursor position. Make sure the cursor is over the window you want to scroll.
- **Coarse control** — this is intentionally designed for coarse navigation, not pixel-precise cursor movement. It works well for clicking large targets, scrolling, and general navigation.

---

## Built With

- [MediaPipe](https://developers.google.com/mediapipe) — face landmark detection
- [OpenCV](https://opencv.org/) — webcam capture and overlay rendering
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — cursor control and click simulation
