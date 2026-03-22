import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

class STTNode:
    def __init__(self):
        self.model = whisper.load_model("medium")
    
    def record(self, duration=4,fs=16000) -> str:
        print("Listening........")
        audio = sd.rec(int(duration*fs),samplerate=fs,channels=1,dtype="float32")
        sd.wait()
        wav.write("input.wav",fs,audio)
        return "input.wav"
    
    def trasncribe(self,file):
        print("Transcribing.....")
        result = self.model.transcribe(file,language="en",fp16=False)
        return result["text"]


