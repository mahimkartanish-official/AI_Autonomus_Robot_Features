class FaceTracker:
    def __init__(self):
        self.prev_cx = None
        self.prev_cy = None
        self.servo_x = 90
        self.servo_y = 90

    def track(self, face, frame_shape):
        h, w, _ = frame_shape
        x, y, fw, fh = map(int, face[:4])

        center_x, center_y = w // 2, h // 2

        cx = x + fw // 2
        cy = y + fh // 2

        # Prediction (your original logic)
        if self.prev_cx is not None:
            dx = cx - self.prev_cx
            dy = cy - self.prev_cy
            pred_x = cx + dx
            pred_y = cy + dy
        else:
            pred_x, pred_y = cx, cy

        self.prev_cx, self.prev_cy = cx, cy

        # Offset (REAL FACE)
        offset_x = cx - center_x
        offset_y = cy - center_y

        # Normalized
        norm_x = offset_x / center_x
        norm_y = offset_y / center_y

        # Servo control (your smooth logic)
        target_x = 90 - norm_x * 60
        target_y = 90 + norm_y * 60

        self.servo_x = int(0.8 * self.servo_x + 0.2 * target_x)
        self.servo_y = int(0.8 * self.servo_y + 0.2 * target_y)

        self.servo_x = max(0, min(180, self.servo_x))
        self.servo_y = max(0, min(180, self.servo_y))

        # Direction detection (UNCHANGED)
        threshold = 0.1
        direction = []

        if norm_x < -threshold:
            direction.append("RIGHT")
        elif norm_x > threshold:
            direction.append("LEFT")

        if norm_y < -threshold:
            direction.append("DOWN")
        elif norm_y > threshold:
            direction.append("UP")

        status = "CENTER" if not direction else "GO " + " & ".join(direction)

        return {
            "bbox": (x, y, fw, fh),
            "center": (cx, cy),
            "pred": (pred_x, pred_y),
            "offset": (offset_x, offset_y),
            "servo": (self.servo_x, self.servo_y),
            "norm":(norm_x,norm_y),
            "status": status
        }