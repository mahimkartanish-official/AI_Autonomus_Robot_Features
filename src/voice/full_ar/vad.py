import webrtcvad
import collections
import numpy as np
import config

class VAD:
    def __init__(self):
        self.vad = webrtcvad.Vad(config.VAD_AGGRESSIVENESS)

    def is_speech(self, audio_chunk):
        return self.vad.is_speech(audio_chunk, config.SAMPLE_RATE)


class AudioBuffer:
    def __init__(self):
        self.buffer = collections.deque(maxlen=50)

    def add(self, chunk):
        self.buffer.append(chunk)

    def get_audio(self):
        return b''.join(self.buffer)

    def clear(self):
        self.buffer.clear()