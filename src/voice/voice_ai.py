import requests

class VoiceAiNode:
    def __init__(self,model="llama3"):
        self.model = model

    def ask(self,prompt):
        print("Thinking..........")
        if prompt.toLower() == "Hello":
            json = {
                "name":"Tanish",
                "text":"Hello how are you"
            }
            return json
        else:
            json = {
                "name":"Error",
                "text":"Please say it again"
            }
            return json

    # def ask(self,prompt):
    #     print("Thinking......")
    #     response = requests.post(
    #         url="http://localhost:11434/api/generate",
    #         json={
    #             "model":self.model,
    #             "prompt":prompt,
    #             "stream":False
    #         }
    #     )
    #     return response