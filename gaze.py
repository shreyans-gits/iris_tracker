import math

# Iris landmark indices
LEFT_IRIS_CENTER  = 473    # single center point of left iris
RIGHT_IRIS_CENTER = 468    # single center point of right iris

# Eye corner indices for reference bounds
LEFT_EYE_LEFT_CORNER  = 263
LEFT_EYE_RIGHT_CORNER = 362
RIGHT_EYE_LEFT_CORNER = 133
RIGHT_EYE_RIGHT_CORNER = 33

# Eye top/bottom for vertical gaze
LEFT_EYE_TOP_POINT    = 386
LEFT_EYE_BOTTOM_POINT = 374
RIGHT_EYE_TOP_POINT   = 159
RIGHT_EYE_BOTTOM_POINT = 145

# Gaze zone thresholds
HORIZONTAL_THRESHOLD = 0.40   # iris ratio below this = looking left/right
VERTICAL_THRESHOLD   = 0.40   # iris ratio below this = looking up/down

#NOSE
NOSE_TIP = 1

class GazeDetector:
    def __init__(self):
        self.gaze = "CENTER"

    def get_iris_ratio(self, landmarks, iris_center, left_corner, right_corner, top_point, bottom_point, w, h):
        p_iris   = landmarks[iris_center]
        p_left   = landmarks[left_corner]
        p_right  = landmarks[right_corner]
        p_top    = landmarks[top_point]
        p_bottom = landmarks[bottom_point]

        iris_px   = (int(p_iris.x * w), int(p_iris.y * h))
        left_px   = (int(p_left.x * w), int(p_left.y * h))
        right_px  = (int(p_right.x * w), int(p_right.y * h))
        top_px    = (int(p_top.x * w), int(p_top.y * h))
        bottom_px = (int(p_bottom.x * w), int(p_bottom.y * h))

        eye_width     = right_px[0] - left_px[0]
        iris_offset_x = iris_px[0]  - left_px[0]
        if eye_width == 0:
            h_ratio = 0.5
        else:
            h_ratio = iris_offset_x / eye_width

        return h_ratio
    
    def get_head_vertical_ratio(self, landmarks, w, h):
        all_y = [lm.y for lm in landmarks]
        face_top    = min(all_y)
        face_bottom = max(all_y)
        nose_y = landmarks[NOSE_TIP].y
        face_height = face_bottom - face_top
        if face_height == 0:
            v_ratio = 0.5
        else:
            v_ratio = (nose_y - face_top) / face_height

        return v_ratio

    def get_gaze(self, landmarks, w, h):
        l_h = self.get_iris_ratio(landmarks, LEFT_IRIS_CENTER, LEFT_EYE_LEFT_CORNER, 
                                       LEFT_EYE_RIGHT_CORNER, LEFT_EYE_TOP_POINT, LEFT_EYE_BOTTOM_POINT, w, h)
        
        r_h = self.get_iris_ratio(landmarks, RIGHT_IRIS_CENTER, RIGHT_EYE_LEFT_CORNER, 
                                       RIGHT_EYE_RIGHT_CORNER, RIGHT_EYE_TOP_POINT, RIGHT_EYE_BOTTOM_POINT, w, h)
        
        h_ratio = (l_h + r_h) / 2
        v_ratio = self.get_head_vertical_ratio(landmarks, w, h)

        if h_ratio < HORIZONTAL_THRESHOLD:
            gaze = "RIGHT"
        elif h_ratio > (1 - HORIZONTAL_THRESHOLD):
            gaze = "LEFT"
        else:
            gaze = "CENTER"

        self.gaze = gaze
        return h_ratio, v_ratio