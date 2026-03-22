from faster_whisper import WhisperModel
import numpy as np
import config

class STT:
    def __init__(self):
        self.model = WhisperModel(
            config.WHISPER_MODEL,
            device=config.DEVICE,
            compute_type="int8"
        )

    def transcribe(self, audio_bytes):
        audio = np.frombuffer(audio_bytes, np.int16).astype(np.float32) / 32768.0
        
        segments, _ = self.model.transcribe(audio, beam_size=1)

        text = ""
        for seg in segments:
            text += seg.text

        return text.strip()