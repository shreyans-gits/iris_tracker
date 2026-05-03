import cv2
from face_landmarker import FaceLandmarker
from visualizer import Visualizer
from eye_utils import EyeUtils, LEFT_EYE_TOP, LEFT_EYE_BOTTOM, LEFT_EYE_TOP2, LEFT_EYE_BOTTOM2, LEFT_EYE_LEFT, LEFT_EYE_RIGHT, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM, RIGHT_EYE_TOP2, RIGHT_EYE_BOTTOM2, RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT
from gestures import GestureDetector
from gaze import GazeDetector
from cursor import CursorController, calibrate

def main():
    landmarker = FaceLandmarker(model_path="models/face_landmarker.task")
    visualizer = Visualizer()
    eye_utils = EyeUtils()
    gesture_detector = GestureDetector()
    gaze_detector = GazeDetector()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if not cap.isOpened():
        print("Camera Not Opened")
        return
    
    h_min, h_max, v_min, v_max = calibrate(cap, landmarker, gaze_detector, eye_utils, w, h)
    cursor = CursorController(h_min, h_max, v_min, v_max)
    
    print("Starting Head Script... Press 'q' to quit.")
    cv2.namedWindow("Head Script", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Head Script", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        frame = cv2.flip(frame, 1)
        result = landmarker.detect(frame)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]
            frame_h, frame_w, _ = frame.shape

            left_ear = eye_utils.get_EAR(landmarks,
                LEFT_EYE_TOP, LEFT_EYE_BOTTOM,
                LEFT_EYE_TOP2, LEFT_EYE_BOTTOM2,
                LEFT_EYE_LEFT, LEFT_EYE_RIGHT, frame_w, frame_h)

            right_ear = eye_utils.get_EAR(landmarks,
                RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM,
                RIGHT_EYE_TOP2, RIGHT_EYE_BOTTOM2,
                RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT, frame_w, frame_h)
            
            gesture = gesture_detector.update(left_ear, right_ear)
            visualizer.draw_EAR(frame, left_ear, right_ear)
            visualizer.draw_gesture(frame, gesture)

            h_ratio, v_ratio = gaze_detector.get_gaze(landmarks, frame_w, frame_h)
            visualizer.draw_gaze(frame, h_ratio, v_ratio)

            cursor.move(h_ratio, v_ratio)
            cursor.scroll(v_ratio)
            if gesture == "RIGHT_WINK":
                cursor.left_click()
            elif gesture == "LEFT_WINK":
                cursor.right_click()

            freeze_changed = gesture_detector.check_freeze(left_ear, right_ear)
            if freeze_changed is not None:
                cursor.frozen = freeze_changed

            visualizer.draw_freeze_state(frame, cursor.frozen)

        frame = visualizer.draw_landmarks(frame, result)
        cv2.imshow("Head Script", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()

if __name__ == "__main__":
    main()