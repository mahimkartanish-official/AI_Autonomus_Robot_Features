# import re
# import time

# from voice.stt import STTNode
# from voice.tts import TTSNode

# ts = TTSNode()
# st = STTNode()

# greeting = "Hello, how can I help"
# ts.speak(greeting)

# try:
#     while True:
#         file = st.record()
#         print("Recorded file:", file)

#         text = st.transcribe(file)

#         if not text:
#             print("No speech detected")
#             continue

#         print("RAW TEXT:", repr(text))

#         clean_text = re.sub(r'[^\w\s]', '', text.lower()).strip()

#         if clean_text in ["exit", "quit", "stop"]:
#             print("Exiting conversation")
#             break

#         print("You said:", text)

#         response = f"You said {text}"
#         ts.speak(response)

#         time.sleep(0.3)

# except KeyboardInterrupt:
#     print("Stopped manually")

import re
import time

from voice.tts import TTSNode
from voice.stt import STTNode

ts = TTSNode()
st = STTNode()

ts.speak("Hello, how can I help")

while True:

    # 🔴 Prevent mic recording while speaking
    if ts.is_speaking:
        continue

    file = st.record()
    text = st.transcribe(file)

    if not text.strip():
        print("No speech detected")
        continue

    print("You said:", text)

    clean_text = re.sub(r'[^\w\s]', '', text.lower()).strip()

    if clean_text in ["exit", "quit", "stop"]:
        ts.speak("Goodbye")
        break

    # 🧠 BASIC BRAIN
    if "your name" in clean_text:
        response = "I am your robot assistant"

    elif "hello" in clean_text:
        response = "Hello there"

    else:
        response = f"You said {text}"

    ts.speak(response)

    time.sleep(0.3)