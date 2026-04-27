import cv2
from face_landmarker import FaceLandmarker

class Visualizer:
    def __init__(self):
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

        self.COLOR_CLOUD = (200,200,200)
        self.COLOR_EYES = (255,255,0)
        self.COLOR_IRIS = (0,255,0)

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

