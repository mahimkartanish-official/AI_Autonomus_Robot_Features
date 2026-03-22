import sounddevice as sd
import numpy as np
from openwakeword.model import Model

class WakeWordNode:
    def __init__(self):
        print("Loading OpenWakeWord...")

        self.model = Model(
            wakeword_models=["hey_jarvis"]  # built-in model
        )

        self.sample_rate = 16000
        self.chunk_size = 1280  # small chunk = low latency

    def listen(self):
        audio = sd.rec(self.chunk_size,
                       samplerate=self.sample_rate,
                       channels=1,
                       dtype='int16')
        sd.wait()

        audio = audio.flatten()

        prediction = self.model.predict(audio)

        for key, score in prediction.items():
            if score > 0.5:  # threshold
                print(f"🔥 Wake detected ({key}) score={score}")
                return True

        return False

    def close(self):
        pass













# import pvporcupine
# import sounddevice as sd
# import numpy as np

# class WakeWordNode:
#     def __init__(self,keyword="computer"):
#         self.porcupine  = pvporcupine.create(,keywords=[keyword])
#         self.stream = sd.InputStream(
#             samplerate=self.porcupine.sample_rate,
#             channels=1,
#             dtype='int16'
#         )
#         self.stream.start()

#     def listen(self):
#         pcm,_ = self.stream.read(self.porcupine.frame_length)
#         pcm = np.frombuffer(pcm,dtype=np.int16)
#         return self.porcupine.process(pcm) >= 0
    
#     def close(self):
#         self.stream.close()
#         self.porcupine.delete()