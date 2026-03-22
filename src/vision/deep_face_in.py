import cv2
from deepface import DeepFace
import os
import threading

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

recognition_running = False

def run_recognition(face_crop):
    global current_name, recognition_running

    try:
        result = DeepFace.find(
            img_path=face_crop,
            db_path=r"D:\Robotics\Facial_recognition\face_db",
            enforce_detection=False,
            model_name="ArcFace"
        )

        if len(result) > 0 and len(result[0]) > 0:
            identity_path = result[0].iloc[0]['identity']
            distance = result[0].iloc[0]['distance']

            print("Distance:", distance)

            if distance < 0.6:
                current_name = os.path.basename(identity_path).split('.')[0]
            else:
                current_name = "Unknown"

    except Exception as e:
        print("Error:", e)
        current_name = "Error"

    recognition_running = False


# Load YuNet model
model_path = r"D:\Robotics\Facial_recognition\model\face_detection_yunet_2023mar.onnx"

detector = cv2.FaceDetectorYN.create(
    model_path,
    "",
    (320, 320),
    score_threshold=0.6
)

cap = cv2.VideoCapture(0)

# Servo setup
servo_x, servo_y = 90, 90
kx, ky = 0.03, 0.03
dead_zone = 50

# Prediction
prev_cx, prev_cy = None, None

frame_count = 0
current_name = "Detecting..."

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    center_x, center_y = w // 2, h // 2

    if faces is not None:
        # Pick largest face
        faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
        face = faces[0]

        x, y, fw, fh = map(int, face[:4])

        # Face center
        cx = x + fw // 2
        cy = y + fh // 2

        # ---- Prediction ----
        if prev_cx is not None:
            dx = cx - prev_cx
            dy = cy - prev_cy

            pred_x = cx + dx
            pred_y = cy + dy
        else:
            pred_x, pred_y = cx, cy

        prev_cx, prev_cy = cx, cy

        # # Offset
        # offset_x = pred_x - center_x
        # offset_y = pred_y - center_y

        # Offset (USE REAL FACE, NOT PREDICTED)
        offset_x = cx - center_x
        offset_y = cy - center_y

        # Servo control
        if abs(offset_x) > dead_zone:
            target_x = servo_x - int(offset_x * kx)
            servo_x = int(0.8 * servo_x + 0.2 * target_x)

        if abs(offset_y) > dead_zone:
            target_y = servo_y + int(offset_y * ky)
            servo_y = int(0.8 * servo_y + 0.2 * target_y)

        # servo_x = max(0, min(180, servo_x))
        # servo_y = max(0, min(180, servo_y))
        norm_x = (cx - center_x) / center_x
        norm_y = (cy - center_y) / center_y

        target_x = 90 - norm_x * 60
        target_y = 90 + norm_y * 60

        servo_x = int(0.8 * servo_x + 0.2 * target_x)
        servo_y = int(0.8 * servo_y + 0.2 * target_y)

        servo_x = max(0, min(180, servo_x))
        servo_y = max(0, min(180, servo_y))

        frame_count += 1

        # ---- FACE RECOGNITION (every 10 frames) ----
        if frame_count % 15 == 0 and not recognition_running:

            pad = 20
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(w, x + fw + pad)
            y2 = min(h, y + fh + pad)

            face_crop = frame[y1:y2, x1:x2]

            if face_crop.size != 0:
                recognition_running = True
                threading.Thread(target=run_recognition, args=(face_crop.copy(),)).start()


        # ---- Direction Detection ----
        threshold = 0.1   # same scale as norm_x, norm_y

        direction = []

        # Horizontal
        if norm_x < -threshold:
            direction.append("RIGHT")
        elif norm_x > threshold:
            direction.append("LEFT")

        # Vertical
        if norm_y < -threshold:
            direction.append("DOWN")
        elif norm_y > threshold:
            direction.append("UP")

        # tells the side the face is in
        # # Horizontal
        # if norm_x < -threshold:
        #     direction.append("LEFT")
        # elif norm_x > threshold:
        #     direction.append("RIGHT")

        # # Vertical
        # if norm_y < -threshold:
        #     direction.append("UP")
        # elif norm_y > threshold:
        #     direction.append("DOWN")

        # Final status
        if not direction:
            status = "CENTER"
        else:
            status = "GO "+" & ".join(direction)

        print(f"Servo X: {servo_x}, Servo Y: {servo_y} | {status}")



        # Draw
        cv2.rectangle(frame, (x, y), (x+fw, y+fh), (0,255,0), 2)
        cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
        cv2.circle(frame, (int(pred_x), int(pred_y)), 5, (255,0,255), -1)

        # Draw line to center
        cv2.line(frame, (center_x, center_y), (cx, cy), (0, 255, 255), 2)

        # Show coordinates
        cv2.putText(frame, f"Face: ({cx}, {cy})",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.putText(frame, f"Offset: ({offset_x}, {offset_y})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.putText(frame, current_name, (x, y - 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        

    # Center point
    cv2.circle(frame, (center_x, center_y), 5, (255,0,0), -1)
    cv2.putText(frame, f"Name: {current_name}", (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("YuNet Face Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
