import cv2
from face_landmarker import FaceLandmarker
from visualizer import Visualizer
from eye_utils import EyeUtils, LEFT_EYE_TOP, LEFT_EYE_BOTTOM, LEFT_EYE_TOP2, LEFT_EYE_BOTTOM2, LEFT_EYE_LEFT, LEFT_EYE_RIGHT, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM, RIGHT_EYE_TOP2, RIGHT_EYE_BOTTOM2, RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT
from gestures import GestureDetector
from gaze import GazeDetector

def main():
    landmarker = FaceLandmarker(model_path="models/face_landmarker.task")
    visualizer = Visualizer()
    eye_utils = EyeUtils()
    gesture_detector = GestureDetector()
    gaze_detector = GazeDetector()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("Camera Not Opened")
        return
    
    print("Starting Iris Tracker... Press 'q' to quit.")
    window_name = "Iris Tracker"
    cv2.namedWindow("Iris Tracker", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Iris Tracker", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
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
            
            gesture = gesture_detector.update(left_ear, right_ear)
            if gesture:
                print(f"GESTURE DETECTED: {gesture}")
            visualizer.draw_EAR(frame, left_ear, right_ear)
            visualizer.draw_gesture(frame, gesture)

            h_ratio, v_ratio = gaze_detector.get_gaze(landmarks, w, h)
            visualizer.draw_gaze(frame, h_ratio, v_ratio)

        cv2.imshow("Iris Tracker", frame)
        frame = visualizer.draw_landmarks(frame, result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()

if __name__ == "__main__":
    main()