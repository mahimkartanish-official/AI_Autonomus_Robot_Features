import os
import cv2
import numpy as np
from numpy.linalg import norm

class FaceRecognizer:
    def __init__(self, db_path, detector):
        self.db_path = db_path
        self.detector = detector

        self.known_embeddings = []
        self.known_names = []

        self.load_database()

    def load_database(self):
        for person_name in os.listdir(self.db_path):
            person_path = os.path.join(self.db_path, person_name)
    
            # check if it's a folder
            if os.path.isdir(person_path):
            
                for img_name in os.listdir(person_path):
                    img_path = os.path.join(person_path, img_name)
    
                    img = cv2.imread(img_path)
    
                    if img is None:
                        print(f"[WARNING] Skipping invalid image: {img_path}")
                        continue
                    
                    result = self.detector.detect(img)
    
                    if result is not None:
                        emb = result["embedding"]
    
                        self.known_embeddings.append(emb)
                        self.known_names.append(person_name)
    
        print(f"[INFO] Loaded {len(self.known_names)} face samples")

    # def load_database(self):
    #     for file in os.listdir(self.db_path):
    #         path = os.path.join(self.db_path, file)

    #         img = cv2.imread(path)
    #         result = self.detector.detect(img)

    #         if result is not None:
    #             emb = result["embedding"]
    #             name = os.path.splitext(file)[0]

    #             self.known_embeddings.append(emb)
    #             self.known_names.append(name)

    #     print(f"[INFO] Loaded {len(self.known_names)} faces")

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (norm(a) * norm(b))

    def recognize(self, embedding):
        best_score = -1
        best_match = None

        for i, known_emb in enumerate(self.known_embeddings):
            score = self.cosine_similarity(embedding, known_emb)

            if score > best_score:
                best_score = score
                best_match = i

        if best_score > 0.5:
            return self.known_names[best_match]
        else:
            return "Unknown"


# from deepface import DeepFace
# import os

# class FaceRecognizer:
#     def __init__(self, db_path):
#         self.db_path = db_path

#     def recognize(self, face_crop):
#         try:
#             result = DeepFace.find(
#                 img_path=face_crop,
#                 db_path=self.db_path,
#                 enforce_detection=False,
#                 model_name="ArcFace"
#             )

#             if len(result) > 0 and len(result[0]) > 0:
#                 identity_path = result[0].iloc[0]['identity']
#                 distance = result[0].iloc[0]['distance']

#                 if distance < 0.6:
#                     return os.path.basename(identity_path).split('.')[0]
#                 else:
#                     return "Unknown"

#         except Exception as e:
#             print("Error:", e)

#         return "Error"