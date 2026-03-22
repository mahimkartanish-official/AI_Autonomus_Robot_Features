from deepface import DeepFace
import os

class FaceRecognizer:
    def __init__(self, db_path):
        self.db_path = db_path

    def recognize(self, face_crop):
        try:
            result = DeepFace.find(
                img_path=face_crop,
                db_path=self.db_path,
                enforce_detection=False,
                model_name="ArcFace"
            )

            if len(result) > 0 and len(result[0]) > 0:
                identity_path = result[0].iloc[0]['identity']
                distance = result[0].iloc[0]['distance']

                if distance < 0.6:
                    return os.path.basename(identity_path).split('.')[0]
                else:
                    return "Unknown"

        except Exception as e:
            print("Error:", e)

        return "Error"