import cv2
from insightface.app import FaceAnalysis

class FaceDetector:
    def __init__(self):
        self.app = FaceAnalysis(name="buffalo_s")
        self.app.prepare(ctx_id=0)  # GPU=0, CPU=-1

    def detect(self, frame):
        faces = self.app.get(frame)

        if len(faces) > 0:
            face = faces[0]  # biggest face automatically
            x1, y1, x2, y2 = map(int, face.bbox)

            return {
                "bbox": (x1, y1, x2 - x1, y2 - y1),
                "embedding": face.embedding
            }

        return None



# import cv2

# class FaceDetector:
#     def __init__(self, model_path):
#         self.detector = cv2.FaceDetectorYN.create(
#             model_path, "", (320, 320), score_threshold=0.6
#         )

#     def detect(self, frame):
#         h, w, _ = frame.shape
#         self.detector.setInputSize((w, h))

#         _, faces = self.detector.detect(frame)

#         if faces is not None:
#             faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
#             return faces[0]

#         return None