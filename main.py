import cv2
from face_landmarker import FaceLandmarker
from visualizer import Visualizer
from eye_utils import *

def main():
    landmarker = FaceLandmarker(model_path="models/face_landmarker.task")
    visualizer = Visualizer()
    eye_utils = EyeUtils()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera Not Opened")
        return
    
    print("Starting Eye Tracker... Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        frame = cv2.flip(frame, 1)
        result = landmarker.detect(frame)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]
            h, w, _ = frame.shape

            left_ear = eye_utils.get_EAR(landmarks,
                LEFT_EYE_TOP, LEFT_EYE_BOTTOM,
                LEFT_EYE_TOP2, LEFT_EYE_BOTTOM2,
                LEFT_EYE_LEFT, LEFT_EYE_RIGHT, w, h)

            right_ear = eye_utils.get_EAR(landmarks,
                RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM,
                RIGHT_EYE_TOP2, RIGHT_EYE_BOTTOM2,
                RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT, w, h)

        frame = visualizer.draw_landmarks(frame, result)
        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()

if __name__ == "__main__":
    main()