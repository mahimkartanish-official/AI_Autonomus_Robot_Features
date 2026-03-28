# import whisper
# import sounddevice as sd
# import numpy as np
# import scipy.io.wavfile as wav
# import webrtcvad
# import collections

# class STTNode:
#     def __init__(self):
#         self.model = whisper.load_model("base")
#         self.fs = 16000
#         self.vad = webrtcvad.Vad(2)  # 0–3 (3 = aggressive)

#     def record_until_silence(self):
#         print("Listening...")

#         frame_duration = 30  # ms
#         frame_size = int(self.fs * frame_duration / 1000)

#         ring_buffer = collections.deque(maxlen=10)
#         triggered = False

#         voiced_frames = []

#         while True:
#             frame = sd.rec(frame_size, samplerate=self.fs, channels=1, dtype="int16")
#             sd.wait()

#             frame = frame.flatten()
#             frame_bytes = frame.tobytes()

#             if len(frame_bytes) != frame_size * 2:
#                 continue

#             is_speech = self.vad.is_speech(frame_bytes, self.fs)
#             print("Speech:", is_speech)

#             if not triggered:
#                 ring_buffer.append((frame, is_speech))
#                 num_voiced = len([f for f, speech in ring_buffer if speech])

#                 if num_voiced > 0.5 * ring_buffer.maxlen:
#                     triggered = True
#                     print("Speech started")
#                     voiced_frames.extend([f for f, s in ring_buffer])
#                     ring_buffer.clear()

#             else:
#                 voiced_frames.append(frame)
#                 ring_buffer.append((frame, is_speech))

#                 num_unvoiced = len([f for f, speech in ring_buffer if not speech])

#                 if num_unvoiced > 0.5 * ring_buffer.maxlen:
#                     print("Speech ended")
#                     break

#         audio = np.concatenate(voiced_frames, axis=0)
#         wav.write("input.wav", self.fs, audio)
#         return "input.wav"
    
#     def transcribe(self, file):
#         print("Transcribing...")
#         result = self.model.transcribe(file, language="en", fp16=False)
#         return result["text"]
    




# import whisper
# import sounddevice as sd
# import numpy as np
# import scipy.io.wavfile as wav

# class STTNode:
#     def __init__(self):
#         self.model = whisper.load_model("small")
#         self.fs = 16000
#         self.silence_threshold = 0.01
#         self.silence_duration = 1.5  # seconds
    
    

#     def record_until_silence(self):
#         print("Listening...")

#         audio_buffer = []
#         silence_counter = 0
#         chunk_duration = 0.5  # seconds
#         chunk_size = int(self.fs * chunk_duration)
#         min_speech_time = 1.5
#         total_audio_time = 0

#         while True:
#             chunk = sd.rec(chunk_size, samplerate=self.fs, channels=1, dtype="float32")
#             sd.wait()

#             audio_buffer.append(chunk)

#             volume = np.linalg.norm(chunk) / len(chunk)

#             if volume < self.silence_threshold:
#                 silence_counter += chunk_duration
#             else:
#                 silence_counter = 0

#             # stop if silence lasts long enough
#             if silence_counter >= self.silence_duration:
#                 break

#         audio = np.concatenate(audio_buffer, axis=0)
#         wav.write("input.wav", self.fs, audio)
#         return "input.wav"

#     def transcribe(self, file):
#         print("Transcribing...")
#         result = self.model.transcribe(file, language="en", fp16=False)
#         return result["text"]



# import whisper
# import sounddevice as sd
# import numpy as np
# import scipy.io.wavfile as wav
# import re
# import playsound


# class STTNode:
#     def __init__(self):
#         self.model = whisper.load_model("base")
    
#     def record(self, duration=4,fs=16000) -> str:
#         print("Listening........")
#         audio = sd.rec(int(duration*fs),samplerate=fs,channels=1,dtype="float32")
#         sd.wait()
#         wav.write("input.wav",fs,audio)
#         return "input.wav"
    
#     def transcribe(self,file):
#         print("Transcribing.....")
#         result = self.model.transcribe(file,language="en",fp16=False)
#         return result["text"]
    
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

class STTNode:
    def __init__(self):
        self.model = whisper.load_model("base")

    def record(self, duration=4, fs=16000):
        print("Listening...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="float32")
        sd.wait()

        wav.write("input.wav", fs, audio)
        return "input.wav"

    def transcribe(self, file):
        print("Transcribing...")
        result = self.model.transcribe(file, language="en", fp16=False)
        return result["text"]