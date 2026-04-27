import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time

class FaceLandmarker:
    def __init__(self, model_path, num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_faces=num_faces,
            min_face_detection_confidence=min_detection_confidence,
            min_face_presence_confidence=min_tracking_confidence,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
        )
        self.start_time = time.time()
        self.detector = vision.FaceLandmarker.create_from_options(options)
        self.timestamp_ms = 0

    def detect(self,frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        self.timestamp_ms = int((time.time() - self.start_time) * 1000)
        result = self.detector.detect_for_video(mp_image, self.timestamp_ms)
        return result
    
    def close(self):
        self.detector.close()
    