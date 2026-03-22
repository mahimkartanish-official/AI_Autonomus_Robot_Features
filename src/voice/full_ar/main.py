import threading
import time

from audio_manager import AudioManager
from vad import VAD, AudioBuffer
from stt import STT
from tts import TTS
from brain import Brain
import config

audio = AudioManager()
vad = VAD()
buffer = AudioBuffer()
stt = STT()
tts = TTS()
brain = Brain()

is_speaking = False


def listen_loop():
    global is_speaking

    audio.start()

    silence_timer = 0
    speaking = False

    while True:
        chunk = audio.read_chunk()

        if vad.is_speech(chunk):
            if is_speaking:
                tts.stop()

            buffer.add(chunk)
            speaking = True
            silence_timer = 0

        else:
            if speaking:
                silence_timer += 0.03  # ~30ms

                if silence_timer > config.SILENCE_DURATION:
                    process_audio()
                    buffer.clear()
                    speaking = False


def process_audio():
    global is_speaking

    audio_data = buffer.get_audio()

    text = stt.transcribe(audio_data)

    if not text:
        return

    print("User:", text)

    response = brain.process(text)

    print("Bot:", response)

    threading.Thread(target=speak, args=(response,)).start()


def speak(text):
    global is_speaking

    is_speaking = True
    tts.speak(text)

    time.sleep(2)  # rough duration (can improve later)

    is_speaking = False


if __name__ == "__main__":
    listen_loop()