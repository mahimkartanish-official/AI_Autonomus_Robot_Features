import cv2
import numpy as np
import time
import random

class RobotFace:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = np.zeros((height, width, 3), dtype=np.uint8)

        self.state = "idle"

        # Eye tracking
        self.eye_offset_x = 0
        self.eye_offset_y = 0

        # Blinking
        self.last_blink = time.time()
        self.blink_duration = 0.05
        self.is_blinking = False
        self.next_blink_time = random.uniform(2, 5)

        # Mouth animation
        self.mouth_open = False
        self.last_mouth_toggle = time.time()

    def set_state(self, state):
        self.state = state

    def update_eye_tracking(self, norm_x, norm_y):
        # Smooth tracking
        self.eye_offset_x = int(norm_x * 20)
        self.eye_offset_y = int(norm_y * 15)

    def handle_blink(self):
        current_time = time.time()

        if not self.is_blinking and current_time - self.last_blink > self.next_blink_time:
            self.is_blinking = True
            self.last_blink = current_time

        if self.is_blinking:
            if current_time - self.last_blink > self.blink_duration:
                self.is_blinking = False
                self.next_blink_time = random.uniform(2, 5)

    def draw_eyes(self):
        left_eye = (250, 250)
        right_eye = (550, 250)

        if self.is_blinking or self.state == "no_face":
            # Blink or idle = closed eyes
            cv2.line(self.screen, (200,250), (300,250), (255,255,255), 6)
            cv2.line(self.screen, (500,250), (600,250), (255,255,255), 6)
            return

        # Eye white
        cv2.circle(self.screen, left_eye, 60, (255,255,255), -1)
        cv2.circle(self.screen, right_eye, 60, (255,255,255), -1)

        # Pupils follow face
        pupil_left = (left_eye[0] + self.eye_offset_x,
                      left_eye[1] + self.eye_offset_y)

        pupil_right = (right_eye[0] + self.eye_offset_x,
                       right_eye[1] + self.eye_offset_y)

        cv2.circle(self.screen, pupil_left, 20, (0,0,0), -1)
        cv2.circle(self.screen, pupil_right, 20, (0,0,0), -1)

    def draw_mouth(self):
        center = (400, 420)

        if self.state == "recognized":
            # Smooth smile
            cv2.ellipse(self.screen, center, (130,70), 0, 0, 180, (255,255,255), 6)

        elif self.state == "unknown":
            # Confused zig-zag
            pts = np.array([[320,420],[360,430],[400,410],[440,430],[480,420]], np.int32)
            cv2.polylines(self.screen, [pts], False, (255,255,255), 5)

        elif self.state == "speaking":
            # Animated talking
            if time.time() - self.last_mouth_toggle > 0.2:
                self.mouth_open = not self.mouth_open
                self.last_mouth_toggle = time.time()

            if self.mouth_open:
                cv2.ellipse(self.screen, center, (100,90), 0, 0, 360, (255,255,255), -1)
            else:
                cv2.line(self.screen, (320,420), (480,420), (255,255,255), 5)

        else:
            # Neutral
            cv2.line(self.screen, (320,420), (480,420), (255,255,255), 4)

    def render(self):
        self.screen[:] = (0, 0, 0)

        self.handle_blink()
        self.draw_eyes()
        self.draw_mouth()

        cv2.imshow("Robot Face", self.screen)