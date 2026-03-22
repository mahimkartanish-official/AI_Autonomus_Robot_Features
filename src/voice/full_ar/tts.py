import subprocess
import threading

class TTS:
    def __init__(self):
        self.process = None
        self.lock = threading.Lock()

    def speak(self, text):
        with self.lock:
            self.stop()

            self.process = subprocess.Popen(
                ["piper", "--model", "en_US-lessac-medium.onnx"],
                stdin=subprocess.PIPE
            )

            self.process.stdin.write(text.encode())
            self.process.stdin.close()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None