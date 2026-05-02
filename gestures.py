import time

BLINK_THRESHOLD  = 0.15   # EAR below this = eye closed
WINK_THRESHOLD   = 0.15   # same value, kept separate for clarity
MIN_BLINK_FRAMES = 2      # minimum frames eye must be closed to count
MAX_BLINK_FRAMES = 6      # if closed longer than this = hold, not blink
COOLDOWN_SEC     = 0.3    # seconds before another gesture can trigger
FREEZE_FRAMES = 20    # both eyes closed for this many frames = freeze toggle

class GestureDetector:
    def __init__(self):
        self.left_closed_frames  = 0
        self.right_closed_frames = 0
        self.last_gesture_time   = 0.0
        self.last_gesture        = None
        self.both_closed_frames = 0
        self.frozen = False

    def update(self, left_ear, right_ear):
        left_closed  = left_ear  < BLINK_THRESHOLD
        right_closed = right_ear < WINK_THRESHOLD

        if left_closed:
            self.left_closed_frames += 1
        else:
            self.left_closed_frames = 0

        if right_closed:
            self.right_closed_frames += 1
        else:
            self.right_closed_frames = 0


        if time.time() - self.last_gesture_time < COOLDOWN_SEC:
            return None
        

        both_closed  = left_closed and right_closed
        left_frames  = self.left_closed_frames  == MIN_BLINK_FRAMES
        right_frames = self.right_closed_frames == MIN_BLINK_FRAMES

        if both_closed and left_frames and right_frames:
            gesture = "BLINK"
        elif left_frames and not right_closed:
            gesture = "RIGHT_WINK"
        elif right_frames and not left_closed:
            gesture = "LEFT_WINK"
        else:
            return None
        
        self.last_gesture_time = time.time()
        self.last_gesture = gesture
        return gesture

    def _reset_state(self):
        self.left_closed_frames  = 0
        self.right_closed_frames = 0

    def check_freeze(self, left_ear, right_ear):
        both_closed = left_ear < BLINK_THRESHOLD and right_ear < BLINK_THRESHOLD
        if both_closed:
            self.both_closed_frames += 1
        else:
            self.both_closed_frames = 0

        if self.both_closed_frames == FREEZE_FRAMES:
            self.frozen = not self.frozen
            return self.frozen
        return None