NOSE_TIP = 1

class GazeDetector:
    def __init__(self):
        self.gaze_h = 0.5
        self.gaze_v = 0.5

    def _get_face_bounds(self, landmarks):
        all_x = [lm.x for lm in landmarks]
        all_y = [lm.y for lm in landmarks]
        return min(all_x), max(all_x), min(all_y), max(all_y)

    def get_gaze(self, landmarks, w, h):
        x_min, x_max, y_min, y_max = self._get_face_bounds(landmarks)
        
        nose_x = landmarks[NOSE_TIP].x
        nose_y = landmarks[NOSE_TIP].y

        face_width = x_max - x_min
        h_ratio = (nose_x - x_min) / face_width if face_width != 0 else 0.5

        face_height = y_max - y_min
        v_ratio = (nose_y - y_min) / face_height if face_height != 0 else 0.5

        self.gaze_h = h_ratio
        self.gaze_v = v_ratio
        return h_ratio, v_ratio