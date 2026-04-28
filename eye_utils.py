import math

# Left eye
LEFT_EYE_TOP    = 386
LEFT_EYE_BOTTOM = 374
LEFT_EYE_TOP2   = 385
LEFT_EYE_BOTTOM2= 380
LEFT_EYE_LEFT   = 263
LEFT_EYE_RIGHT  = 362

# Right eye
RIGHT_EYE_TOP    = 159
RIGHT_EYE_BOTTOM = 145
RIGHT_EYE_TOP2   = 158
RIGHT_EYE_BOTTOM2= 153
RIGHT_EYE_LEFT   = 133
RIGHT_EYE_RIGHT  = 33

EAR_THRESHOLD        = 0.15   # below this = eye closed
BLINK_FRAMES         = 2      # eye must be closed for this many frames to count

class EyeUtils:
    def __init__(self):
        self.left_closed_frames  = 0
        self.right_closed_frames = 0
        self.left_blink_count    = 0
        self.right_blink_count   = 0

    def get_EAR(self, landmarks, top, bottom, top2, bottom2, left, right, frame_w, frame_h):
        def get_pixel_pt(idx):
            lm = landmarks[idx]
            return (int(lm.x * frame_w), int(lm.y * frame_h))
        
        p_top     = get_pixel_pt(top)
        p_bottom  = get_pixel_pt(bottom)
        p_top2    = get_pixel_pt(top2)
        p_bottom2 = get_pixel_pt(bottom2)
        p_left    = get_pixel_pt(left)
        p_right   = get_pixel_pt(right)

        v1 = math.dist(p_top, p_bottom)
        v2 = math.dist(p_top2, p_bottom2)
        h = math.dist(p_left, p_right)

        if h == 0:
            return 0.0
        
        EAR = (v1 + v2) / (2.0 * h)
        return EAR