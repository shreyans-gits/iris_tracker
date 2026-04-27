import cv2
from face_landmarker import FaceLandmarker
from visualizer import Visualizer

def main():
    landmarker = FaceLandmarker(model_path="models/face_landmarker.task")
    visualizer = Visualizer()

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
        frame = visualizer.draw_landmarks(frame, result)
        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()

if __name__ == "__main__":
    main()