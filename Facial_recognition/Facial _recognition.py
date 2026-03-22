import cv2

# Load YuNet model
model_path = r"D:\Robotics\Facial recognition\model\face_detection_yunet_2023mar.onnx"

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

    # Center point
    cv2.circle(frame, (center_x, center_y), 5, (255,0,0), -1)

    cv2.imshow("YuNet Face Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



























# import cv2

# model_path = "models/face_detection_yunet_2023mar.onnx"

# # Load cascades
# front_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
# )

# profile_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + 'haarcascade_profileface.xml'
# )

# cap = cv2.VideoCapture(0)

# alpha = 0.7
# prev = None

# # Initial angles (outside loop)
# servo_x = 90
# servo_y = 90

# kx = 0.03   # sensitivity
# ky = 0.03

# dead_zone = 50



# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     h, w, _ = frame.shape

#     # 🎯 Screen center
#     center_x = w // 2
#     center_y = h // 2

#     # Draw center square
#     box_size = 100
#     cv2.rectangle(frame,
#                   (center_x - box_size, center_y - box_size),
#                   (center_x + box_size, center_y + box_size),
#                   (255, 0, 0), 2)

#     faces = []

#     # Detect frontal faces
#     faces_front = front_cascade.detectMultiScale(gray, 1.2, 6)

#     # Detect profile faces (left)
#     faces_profile = profile_cascade.detectMultiScale(gray, 1.2, 6)

#     # Detect right profile
#     flipped = cv2.flip(gray, 1)
#     faces_profile_flip = profile_cascade.detectMultiScale(flipped, 1.2, 6)

#     for (x, y, fw, fh) in faces_profile_flip:
#         faces.append((gray.shape[1] - x - fw, y, fw, fh))

#     faces.extend(faces_front)
#     faces.extend(faces_profile)

#     for (x, y, fw, fh) in faces:

#         # Smooth movement
#         if prev is not None:
#             px, py, pw, ph = prev
#             x = int(alpha * px + (1 - alpha) * x)
#             y = int(alpha * py + (1 - alpha) * y)
#             fw = int(alpha * pw + (1 - alpha) * fw)
#             fh = int(alpha * ph + (1 - alpha) * fh)

#         prev = (x, y, fw, fh)

#         # 🎯 Face center
#         face_cx = x + fw // 2
#         face_cy = y + fh // 2

#         # Offset from screen center
#         offset_x = face_cx - center_x
#         offset_y = face_cy - center_y

#         # Apply dead zone FIRST
#         if abs(offset_x) > dead_zone:
#             servo_x -= int(offset_x * kx)

#         if abs(offset_y) > dead_zone:
#             servo_y += int(offset_y * ky)

#         # Clamp angles
#         servo_x = max(0, min(180, servo_x))
#         servo_y = max(0, min(180, servo_y))

#         print(f"Servo X: {servo_x}, Servo Y: {servo_y}")

#         # Draw face box
#         cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 255, 0), 2)

#         # Draw face center
#         cv2.circle(frame, (face_cx, face_cy), 5, (0, 0, 255), -1)

#         # Draw line to center
#         cv2.line(frame, (center_x, center_y), (face_cx, face_cy), (0, 255, 255), 2)

#         # Show coordinates
#         cv2.putText(frame, f"Face: ({face_cx}, {face_cy})",
#                     (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         cv2.putText(frame, f"Offset: ({offset_x}, {offset_y})",
#                     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

#     # Draw screen center point
#     cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

#     cv2.imshow("Face Tracking Centered", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# # # Initial angles (keep outside loop ideally)
# # servo_x = 90   # left-right
# # servo_y = 90   # up-down

# # # Sensitivity (tune this)
# # kx = 0.05
# # ky = 0.05

# # # Update angles
# # servo_x += int(offset_x * kx)
# # servo_y += int(offset_y * ky)

# # # Clamp angles (IMPORTANT)
# # servo_x = max(0, min(180, servo_x))
# # servo_y = max(0, min(180, servo_y))

# # print(f"Servo X: {servo_x}, Servo Y: {servo_y}")

# # dead_zone = 20  # ignore small movement

# # if abs(offset_x) > dead_zone:
# #     servo_x += int(offset_x * 0.03)

# # if abs(offset_y) > dead_zone:
# #     servo_y += int(offset_y * 0.03)

# # servo_x = max(0, min(180, servo_x))
# # servo_y = max(0, min(180, servo_y))