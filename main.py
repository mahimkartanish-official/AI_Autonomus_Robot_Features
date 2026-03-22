import sys
import os

sys.path.append(os.path.abspath("Facial_recognition"))

import cv2
import threading

from detection import FaceDetector
from tracking import FaceTracker
from recognition import FaceRecognizer
from robot_face import RobotFace

model_path = r"D:\Robotics\facial_recognition\model\face_detection_yunet_2023mar.onnx"
db_path = r"D:\Robotics\facial_recognition\face_db"

detector = FaceDetector(model_path)
tracker = FaceTracker()
recognizer = FaceRecognizer(db_path)

cap = cv2.VideoCapture(0)

current_name = "Detecting..."
recognition_running = False
frame_count = 0

face_ui = RobotFace()


def run_recognition(face_crop):
    global current_name, recognition_running
    current_name = recognizer.recognize(face_crop)
    recognition_running = False


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    face = detector.detect(frame)

    if face is not None:
        data = tracker.track(face, frame.shape)

        x, y, fw, fh = data["bbox"]
        cx, cy = data["center"]
        pred_x, pred_y = data["pred"]
        offset_x, offset_y = data["offset"]
        servo_x, servo_y = data["servo"]
        status = data["status"]
        norm_x,norm_y = data["norm"]

        frame_count += 1

        # Recognition (every 15 frames)
        if frame_count % 15 == 0 and not recognition_running:
            face_crop = frame[y:y+fh, x:x+fw]

            if face_crop.size != 0:
                recognition_running = True
                threading.Thread(target=run_recognition, args=(face_crop.copy(),)).start()

        print(f"Servo X: {servo_x}, Servo Y: {servo_y} | {status}")

        face_ui.update_eye_tracking(norm_x, norm_y)
        if data:
            face_ui.set_state("detected")

        if current_name == "Unknown":
            face_ui.set_state("unknown")

        elif current_name != "Detecting...":
            face_ui.set_state("recognized")

            if face is None:
                face_ui.set_state("no_face")

            elif current_name == "Unknown":
                face_ui.set_state("unknown")

            else:
                face_ui.set_state("recognized")

        face_ui.render()

        # Draw EVERYTHING (same as original)
        cv2.rectangle(frame, (x, y), (x+fw, y+fh), (0,255,0), 2)
        cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
        cv2.circle(frame, (int(pred_x), int(pred_y)), 5, (255,0,255), -1)

        center_x, center_y = frame.shape[1]//2, frame.shape[0]//2
        cv2.circle(frame, (center_x, center_y), 5, (255,0,0), -1)

        cv2.line(frame, (center_x, center_y), (cx, cy), (0,255,255), 2)

        cv2.putText(frame, f"Face: ({cx}, {cy})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        cv2.putText(frame, f"Offset: ({offset_x}, {offset_y})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

        cv2.putText(frame, current_name, (x, y-30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.putText(frame, status, (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.imshow("YuNet Face Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()