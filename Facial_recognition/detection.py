import cv2

class FaceDetector:
    def __init__(self, model_path):
        self.detector = cv2.FaceDetectorYN.create(
            model_path, "", (320, 320), score_threshold=0.6
        )

    def detect(self, frame):
        h, w, _ = frame.shape
        self.detector.setInputSize((w, h))

        _, faces = self.detector.detect(frame)

        if faces is not None:
            faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
            return faces[0]

        return None