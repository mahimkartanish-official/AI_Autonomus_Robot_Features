import sounddevice as sd
import numpy as np
import config

class AudioManager:
    def __init__(self):
        self.stream = sd.InputStream(
            samplerate=config.SAMPLE_RATE,
            channels=1,
            dtype='int16',
            blocksize=config.CHUNK_SIZE
        )

    def start(self):
        self.stream.start()

    def read_chunk(self):
        data, _ = self.stream.read(config.CHUNK_SIZE)
        return data.tobytes()