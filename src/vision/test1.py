import sys
import os

sys.path.append(os.path.abspath("voice_model"))


from wake_word import WakeWordNode
from stt import STTNode
from voice_ai import VoiceAiNode
from tts import TTSNode

def main():
    wake = WakeWordNode()
    stt = STTNode()
    ai = VoiceAiNode()
    tts = TTSNode()

    print("🚀 System Ready... Say wake word")

    try:
        while True:
            if wake.listen():
                print("🔥 Wake word detected!")

                audio = stt.record()
                text = stt.transcribe(audio)

                print(f"👤 You: {text}")

                if text.strip() == "":
                    continue

                response = ai.ask(text)
                print(f"🤖 AI: {response}")

                tts.speak(response)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        wake.close()

if __name__ == "__main__":
    main()













# import cv2
# import numpy as np
# import time

# class RobotFace:
#     def __init__(self, width=800, height=600):
#         self.width = width
#         self.height = height
#         self.screen = np.zeros((height, width, 3), dtype=np.uint8)
#         self.state = "idle"
#         self.mouth_open = False
#         self.last_toggle = time.time()

#     def set_state(self, state):
#         self.state = state

#     def draw_eyes(self):
#         Default positions
#         left_eye = (250, 250)
#         right_eye = (550, 250)

#         if self.state == "no_face":
#             closed eyes
#             cv2.line(self.screen, (200,250), (300,250), (255,255,255), 5)
#             cv2.line(self.screen, (500,250), (600,250), (255,255,255), 5)
#         else:
#             open eyes
#             cv2.circle(self.screen, left_eye, 60, (255,255,255), -1)
#             cv2.circle(self.screen, right_eye, 60, (255,255,255), -1)

#             pupils
#             cv2.circle(self.screen, left_eye, 20, (0,0,0), -1)
#             cv2.circle(self.screen, right_eye, 20, (0,0,0), -1)

#     def draw_mouth(self):
#         center = (400, 420)

#         if self.state == "recognized":
#             smile
#             cv2.ellipse(self.screen, center, (120,60), 0, 0, 180, (255,255,255), 5)

#         elif self.state == "unknown":
#             confused (tilted line)
#             cv2.line(self.screen, (320,420), (480,440), (255,255,255), 5)

#         elif self.state == "speaking":
#             animated mouth
#             if time.time() - self.last_toggle > 0.3:
#                 self.mouth_open = not self.mouth_open
#                 self.last_toggle = time.time()

#             if self.mouth_open:
#                 cv2.ellipse(self.screen, center, (100,80), 0, 0, 360, (255,255,255), -1)
#             else:
#                 cv2.line(self.screen, (320,420), (480,420), (255,255,255), 5)

#         else:
#             neutral
#             cv2.line(self.screen, (320,420), (480,420), (255,255,255), 5)

#     def render(self):
#         self.screen[:] = (0, 0, 0)

#         self.draw_eyes()
#         self.draw_mouth()

#         cv2.imshow("Robot Face", self.screen)


# current_name = "TANISH"
# face_detected = True


# face_ui = RobotFace()
# for i in range(1000):
#     if face_detected:
#         face_ui.set_state("detected")

#     if current_name == "Unknown":
#         face_ui.set_state("unknown")

#     elif current_name != "Detecting...":
#         face_ui.set_state("recognized")

#     face_ui.render()



# import cv2
# import os
# import numpy as np
# import threading
# import time
# from deepface import DeepFace

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# # ==============================
# # 🧠 LOAD ARCFACE MODEL
# # ==============================
# print("Loading ArcFace model...")
# model = DeepFace.build_model("ArcFace")
# print("Model loaded!")

# # ==============================
# # 📂 LOAD FACE DATABASE
# # ==============================
# db_path = r"D:\Robotics\Facial recognition\face_db"

# known_embeddings = []
# known_names = []

# # def load_database():
# #     for file in os.listdir(db_path):
# #         if file.endswith(".jpg") or file.endswith(".png"):
# #             path = os.path.join(db_path, file)
# #             try:
# #                 embedding = DeepFace.represent(
# #                     img_path=path,
# #                     model_name="ArcFace",
# #                     enforce_detection=False
# #                 )[0]["embedding"]

# #                 known_embeddings.append(np.array(embedding))
# #                 known_names.append(os.path.splitext(file)[0])

# #                 print("Loaded:", file)

# #             except Exception as e:
# #                 print("Error loading:", file, e)

# def load_database():
#     for root, dirs, files in os.walk(db_path):
#         for file in files:
#             if file.endswith(".jpg") or file.endswith(".png"):
                
#                 path = os.path.join(root, file)

#                 try:
#                     embedding = DeepFace.represent(
#                         img_path=path,
#                         model_name="ArcFace",
#                         enforce_detection=False
#                     )[0]["embedding"]

#                     known_embeddings.append(np.array(embedding))

#                     name = os.path.splitext(file)[0]
#                     known_names.append(name)

#                     print(f"Loaded: {name} -> {file}")

#                 except Exception as e:
#                     print("Error loading:", path, e)

# load_database()

# # ==============================
# # ⚡ FAST RECOGNITION FUNCTION
# # ==============================
# def recognize_face(face_crop):
#     try:
#         embedding = DeepFace.represent(
#             img_path=face_crop,
#             model_name="ArcFace",
#             enforce_detection=False
#         )[0]["embedding"]

#         embedding = np.array(embedding)

#         if len(known_embeddings) == 0:
#             return "Unknown", 0

#         similarities = []
#         for db_emb in known_embeddings:
#             sim = np.dot(embedding, db_emb) / (
#                 np.linalg.norm(embedding) * np.linalg.norm(db_emb)
#             )
#             similarities.append(sim)

#         best_idx = np.argmax(similarities)
#         best_score = similarities[best_idx]

#         if best_score > 0.4:
#             return known_names[best_idx], best_score
#         else:
#             return "Unknown", best_score

#     except Exception as e:
#         print("Recognition error:", e)
#         return "Error", 0


# # ==============================
# # 🧵 THREAD FUNCTION
# # ==============================
# recognition_running = False
# current_name = "Detecting..."
# confidence = 0

# def run_recognition(face_crop):
#     global current_name, confidence, recognition_running

#     name, score = recognize_face(face_crop)

#     current_name = name
#     confidence = score

#     recognition_running = False


# # ==============================
# # 🎯 LOAD YUNET
# # ==============================
# model_path = r"D:\Robotics\Facial recognition\model\face_detection_yunet_2023mar.onnx"

# detector = cv2.FaceDetectorYN.create(
#     model_path,
#     "",
#     (320, 320),
#     score_threshold=0.6
# )

# cap = cv2.VideoCapture(0)

# # ==============================
# # 🎮 SERVO SETUP
# # ==============================
# servo_x, servo_y = 90, 90
# kx, ky = 0.03, 0.03
# dead_zone = 50

# prev_cx, prev_cy = None, None

# frame_count = 0

# # ==============================
# # ⏳ ADD FACE CONTROL
# # ==============================
# last_add_time = 0
# ADD_COOLDOWN = 5

# # ==============================
# # 🔁 MAIN LOOP
# # ==============================
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     h, w, _ = frame.shape

#     detector.setInputSize((w, h))
#     _, faces = detector.detect(frame)

#     center_x, center_y = w // 2, h // 2

#     if faces is not None:
#         faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
#         face = faces[0]

#         x, y, fw, fh = map(int, face[:4])

#         cx = x + fw // 2
#         cy = y + fh // 2

#         # ==============================
#         # 🔮 PREDICTION (UNCHANGED)
#         # ==============================
#         if prev_cx is not None:
#             dx = cx - prev_cx
#             dy = cy - prev_cy
#             pred_x = cx + dx
#             pred_y = cy + dy
#         else:
#             pred_x, pred_y = cx, cy

#         prev_cx, prev_cy = cx, cy

#         # ==============================
#         # 🎯 SERVO LOGIC (UNCHANGED)
#         # ==============================
#         norm_x = (cx - center_x) / center_x
#         norm_y = (cy - center_y) / center_y

#         target_x = 90 - norm_x * 60
#         target_y = 90 + norm_y * 60

#         servo_x = int(0.8 * servo_x + 0.2 * target_x)
#         servo_y = int(0.8 * servo_y + 0.2 * target_y)

#         servo_x = max(0, min(180, servo_x))
#         servo_y = max(0, min(180, servo_y))

#         frame_count += 1

#         # ==============================
#         # ⚡ RUN RECOGNITION (THREAD)
#         # ==============================
#         if frame_count % 15 == 0 and not recognition_running:

#             pad = 20
#             x1 = max(0, x - pad)
#             y1 = max(0, y - pad)
#             x2 = min(w, x + fw + pad)
#             y2 = min(h, y + fh + pad)

#             face_crop = frame[y1:y2, x1:x2]

#             if face_crop.size != 0:
#                 recognition_running = True
#                 threading.Thread(
#                     target=run_recognition,
#                     args=(face_crop.copy(),)
#                 ).start()

#         # ==============================
#         # ➕ ADD UNKNOWN FACE (PRESS S)
#         # ==============================
#         current_time = time.time()

#         if current_name == "Unknown" and (current_time - last_add_time > ADD_COOLDOWN):

#             cv2.putText(frame, "Press S to SAVE FACE",
#                         (20, 140),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

#             key = cv2.waitKey(1) & 0xFF

#             if key == ord('s'):
#                 filename = f"user_{int(current_time)}.jpg"
#                 save_path = os.path.join(db_path, filename)

#                 cv2.imwrite(save_path, face_crop)

#                 # Add embedding instantly
#                 embedding = DeepFace.represent(
#                     img_path=face_crop,
#                     model_name="ArcFace",
#                     # model=model,
#                     enforce_detection=False
#                 )[0]["embedding"]

#                 known_embeddings.append(np.array(embedding))
#                 known_names.append(os.path.splitext(filename)[0])

#                 print("✅ Face added:", filename)

#                 last_add_time = current_time

#         # ==============================
#         # 🧭 DIRECTION
#         # ==============================
#         threshold = 0.1
#         direction = []

#         if norm_x < -threshold:
#             direction.append("RIGHT")
#         elif norm_x > threshold:
#             direction.append("LEFT")

#         if norm_y < -threshold:
#             direction.append("DOWN")
#         elif norm_y > threshold:
#             direction.append("UP")

#         status = "CENTER" if not direction else "GO " + " & ".join(direction)

#         # print(f"Servo X: {servo_x}, Servo Y: {servo_y} | {status}")

#         # ==============================
#         # 🎨 DRAW
#         # ==============================
#         cv2.rectangle(frame, (x, y), (x+fw, y+fh), (0,255,0), 2)

#         cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
#         cv2.circle(frame, (int(pred_x), int(pred_y)), 5, (255,0,255), -1)

#         cv2.line(frame, (center_x, center_y), (cx, cy), (0,255,255), 2)

#         cv2.putText(frame, f"{current_name} ({confidence:.2f})",
#                     (x, y - 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

#     # center point
#     cv2.circle(frame, (center_x, center_y), 5, (255,0,0), -1)

#     cv2.imshow("YuNet Face Tracking + ArcFace", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()