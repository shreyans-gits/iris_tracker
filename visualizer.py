import cv2
from face_landmarker import FaceLandmarker
import time

class Visualizer:
    def __init__(self):
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

        self.COLOR_CLOUD = (200,200,200)
        self.COLOR_EYES = (255,255,0)
        self.COLOR_IRIS = (0,255,0)

        self.last_gesture = None
        self.gesture_timer = 0.0

    def draw_landmarks(self, frame, detection_result):
        if not detection_result or not detection_result.face_landmarks:
            return frame
        
        h,w,_ = frame.shape

        for faceLandmarks in detection_result.face_landmarks:
            for landmark in faceLandmarks:
                px, py = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (px, py), 1, self.COLOR_CLOUD, -1)

            for idx in self.LEFT_EYE + self.RIGHT_EYE:
                lm = faceLandmarks[idx]
                px, py = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (px, py), 2, self.COLOR_EYES, -1)

            for idx in self.LEFT_IRIS + self.RIGHT_IRIS:
                lm = faceLandmarks[idx]
                px, py = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (px, py), 2, self.COLOR_IRIS, -1)

        return frame

    def draw_EAR(self, frame, left_ear, right_ear):
        LEFT  = f"RIGHT EAR: {left_ear:.2f}"
        RIGHT = f"LEFT  EAR: {right_ear:.2f}"
        open_color = (0, 255, 0)
        closed_color = (0, 0, 255)

        if left_ear<0.15:
            l_color = closed_color
        else:
            l_color = open_color

        if right_ear<0.15:
            r_color = closed_color
        else:
            r_color = open_color

        cv2.putText(frame, LEFT, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, l_color, 2)
        cv2.putText(frame, RIGHT, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, r_color, 2)
        
        return frame

    def draw_gesture(self, frame, gesture):
        if gesture is not None:
            self.last_gesture = gesture
            self.gesture_timer = time.time()

        if self.last_gesture is None:
            return frame
        
        if time.time() - self.gesture_timer > 1.0:
            self.last_gesture = None
            return frame

        frame_width = frame.shape[1]
        pos = (frame_width // 2 - 100, 40)
        
        cv2.putText(frame, self.last_gesture, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        return frame
    
    def draw_gaze(self,frame,h_ratio,v_ratio):
        text = f"Gaze  H: {h_ratio:.2f}  V: {v_ratio:.2f}"
        color = (255, 191, 0)
        cv2.putText(frame, text, (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        return frame