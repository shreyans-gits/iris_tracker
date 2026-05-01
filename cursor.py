import pyautogui as pag
import time
import cv2

# Smoothing
SMOOTH_FACTOR = 0.1   # lower = smoother but slower, higher = faster but jittery

# Click cooldown
CLICK_COOLDOWN = 1.0  # seconds between clicks

DEADZONE = 0.08      # ignore small movements near center
SENSITIVITY = 1.8    # stretch the range outward

def calibrate(cap, landmarker, gaze_detector, eye_utils, w, h):
        CALIBRATION_POINTS = [
            ("TOP-LEFT",     "Look at TOP-LEFT corner of screen, then press SPACE"),
            ("TOP-RIGHT",    "Look at TOP-RIGHT corner of screen, then press SPACE"),
            ("BOTTOM-LEFT",  "Look at BOTTOM-LEFT corner of screen, then press SPACE"),
            ("BOTTOM-RIGHT", "Look at BOTTOM-RIGHT corner of screen, then press SPACE"),
        ]
        readings = []
        for label, instruction in CALIBRATION_POINTS:
            while True:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                
                cv2.putText(frame, instruction, (30, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, "Press SPACE to capture", (30, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.imshow("Calibrate", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord(' '):
                    result = landmarker.detect(frame)
                    if result.face_landmarks:
                        landmarks = result.face_landmarks[0]
                        h_ratio, v_ratio = gaze_detector.get_gaze(landmarks, w, h)
                        readings.append((h_ratio, v_ratio))
                    break

        h_vals = [r[0] for r in readings]
        v_vals = [r[1] for r in readings]

        h_min = min(h_vals)
        h_max = max(h_vals)
        v_min = min(v_vals)
        v_max = max(v_vals)

        h_center = (h_min + h_max) / 2
        v_center = (v_min + v_max) / 2

        h_min = h_center - 0.12
        h_max = h_center + 0.12
        v_min = v_center - 0.10
        v_max = v_center + 0.10

        print(f"Calibration complete:")
        print(f"H_MIN: {h_min:.3f}  H_MAX: {h_max:.3f}")
        print(f"V_MIN: {v_min:.3f}  V_MAX: {v_max:.3f}")
        cv2.destroyWindow("Calibrate")
        return h_min, h_max, v_min, v_max

class CursorController:
    def __init__(self, h_min, h_max, v_min, v_max):
        self.H_MIN = h_min
        self.H_MAX = h_max
        self.V_MIN = v_min
        self.V_MAX = v_max
        self.screen_w, self.screen_h = pag.size()
        self.current_x = self.screen_w // 2
        self.current_y = self.screen_h // 2
        self.last_click_time = 0.0
        pag.FAILSAFE = False  # prevents pyautogui from raising exception at screen corners

    def move(self, h_ratio, v_ratio):
        # h_ratio = 1 - h_ratio

        h_clamped = (h_ratio - self.H_MIN) / (self.H_MAX - self.H_MIN)
        v_clamped = (v_ratio - self.V_MIN) / (self.V_MAX - self.V_MIN)

        h_clamped = max(0.0, min(1.0, h_clamped))
        v_clamped = max(0.0, min(1.0, v_clamped))

        # center both axes around 0.5
        h_centered = h_clamped - 0.5
        v_centered = v_clamped - 0.5

        # apply deadzone
        if abs(h_centered) < DEADZONE:
            h_centered = 0
        if abs(v_centered) < DEADZONE:
            v_centered = 0

        # apply sensitivity and re-center
        h_final = max(0.0, min(1.0, (h_centered * SENSITIVITY) + 0.5))
        v_final = max(0.0, min(1.0, (v_centered * SENSITIVITY) + 0.5))

        target_x = int(h_final * self.screen_w)
        target_y = int(v_final * self.screen_h)

        self.current_x += SMOOTH_FACTOR * (target_x - self.current_x)
        self.current_y += SMOOTH_FACTOR * (target_y - self.current_y)
        pag.moveTo(int(self.current_x), int(self.current_y))

    def left_click(self):
        if time.time() - self.last_click_time > CLICK_COOLDOWN:
            pag.click()
            self.last_click_time = time.time()

    def right_click(self):
        if time.time() - self.last_click_time > CLICK_COOLDOWN:
            pag.rightClick()
            self.last_click_time = time.time()