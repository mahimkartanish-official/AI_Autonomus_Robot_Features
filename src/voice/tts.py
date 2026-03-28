# import asyncio
# import edge_tts
# import os
# import uuid
# from playsound import playsound

# class TTSNode:
#     def __init__(self,voice="en-IN-PrabhatNeural"):
#         self.voice = voice
#         self.loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(self.loop)

    
#     async def speak_async(self,text):
#         # file = "output.mp3"
#         file = f"output_{uuid.uuid4().hex}.mp3"
#         communicate = edge_tts.Communicate(text,self.voice)
#         await communicate.save(file)
#         os.system(f"start {file}")
    
#     def speak(self,text):
#         # print("Speaking")
#         # asyncio.run(self.speak_async(text))
#         self.loop.run_until_complete(self.speak_async(text))
#         playsound("output.mp3")



# # ts = TTSNode()

# # while True:
# #     query = input("Enter your text: ")

# #     ts.speak(query)


import asyncio
import edge_tts
import simpleaudio as sa
import os

class TTSNode:
    def __init__(self, voice="en-IN-PrabhatNeural"):
        self.voice = voice
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.is_speaking = False  # 🔴 important for pipeline

    async def speak_async(self, text):
        self.file = "output.wav"

        # edge-tts → save mp3 first
        temp_mp3 = "temp.mp3"
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(temp_mp3)

        # convert mp3 → wav using pure python (no ffmpeg)
        import wave
        from pydub import AudioSegment

        audio = AudioSegment.from_file(temp_mp3)
        audio.export(self.file, format="wav")

        os.remove(temp_mp3)

    def speak(self, text):
        print("Speaking:", text)
        self.is_speaking = True

        self.loop.run_until_complete(self.speak_async(text))

        wave_obj = sa.WaveObject.from_wave_file(self.file)
        play_obj = wave_obj.play()
        play_obj.wait_done()

        self.is_speaking = False