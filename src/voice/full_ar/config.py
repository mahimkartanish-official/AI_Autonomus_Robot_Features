SAMPLE_RATE = 16000
CHUNK_SIZE = 480  # 30ms for VAD
VAD_AGGRESSIVENESS = 2

WHISPER_MODEL = "base"  # use "small" if CPU can handle
DEVICE = "cpu"

INTERRUPT_THRESHOLD = 0.3  # seconds of speech to interrupt
SILENCE_DURATION = 0.6     # end of speech