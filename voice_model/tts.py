import asyncio
import edge_tts
import os

class TTSNode:
    def __init__(self,voice="en-IN-PrabhatNeutral"):
        self.voice = voice

    
    async def speak_async(self,text):
        file = "output.mp3"
        communicate = edge_tts.Communicate(text,self.voice)
        await communicate.save(file)
        os.system(f"start {file}")
    
    def speak(self,text):
        print("Speaking")
        asyncio.run(self.speak_async(text))